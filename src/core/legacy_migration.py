import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple

from core.tools import load_yaml, write_yaml
from core.mod_manager import load_staging_metadata

# Common files/extensions to ignore during legacy scanning
IGNORED_FILES = {
    ".ds_store", "thumbs.db", "desktop.ini", ".git", ".gitignore",
    ".staging.nomm.yaml", ".downloads.nomm.yaml"
}

IGNORED_EXTENSIONS = {
    ".tmp", ".bak", ".log", ".txt", ".md"
}

# Base game pak patterns in Unreal Engine (when scanning Content/Paks directly)
BASE_PAK_PREFIXES = (
    "pakchunk0", "pakchunk1", "global"
)

# Known mod subdirectories relative to game_path when mods_path is "" or game root
KNOWN_GAME_MOD_DIRS = [
    # Cyberpunk 2077
    ("archive/pc/mod", "flat"),
    ("bin/x64/plugins/cyber_engine_tweaks/mods", "folders"),
    ("r6/scripts", "tree"),
    ("r6/tweaks", "tree"),
    ("red4ext/plugins", "folders"),
    ("mods", "tree"),
    ("Mods", "tree"),
    # RE Engine (Resident Evil, Monster Hunter)
    ("natives", "tree"),
    ("reframework/autorun", "flat"),
    ("reframework/plugins", "flat"),
    # Unity / BepInEx
    ("BepInEx/plugins", "tree"),
    ("BepInEx/patchers", "tree"),
    # Unreal Engine
    ("Content/Paks/~mods", "flat"),
]


def scan_legacy_mods(game_info: dict, staging_path: Path | str) -> List[Dict[str, Any]]:
    """
    Scans the game directory for unmanaged (non-symlink) legacy mod files.
    Returns a list of detected mod definitions ready for migration.
    """
    game_path = Path(game_info["path"])
    staging_path = Path(staging_path)
    staging_meta_path = staging_path / ".staging.nomm.yaml"
    staging_metadata = load_staging_metadata(str(staging_meta_path))

    existing_mod_names = set(staging_metadata.get("mods", {}).keys())

    # Build set of already-managed relative file paths
    managed_rel_files = set()
    for mod_data in staging_metadata.get("mods", {}).values():
        for f in mod_data.get("mod_files", []):
            managed_rel_files.add(os.path.normpath(f))

    deployment_targets = game_info.get("mod_paths", [])
    if not deployment_targets:
        deployment_targets = [{"name": "default", "path": str(game_path)}]

    detected_mods = []
    processed_sources = set()
    scanned_directories = set()

    # 1. Inspect explicit deployment targets (e.g. BepInEx/plugins, Content/Paks/~mods, mods/)
    for target in deployment_targets:
        target_path_str = target.get("path")
        if not target_path_str:
            continue
        target_path = Path(target_path_str)
        if not target_path.exists():
            continue

        resolved_target = str(target_path.resolve())
        # If deployment target is a dedicated mod folder (not the game root)
        if target_path.resolve() != game_path.resolve():
            scanned_directories.add(resolved_target)
            _scan_directory(
                target_path,
                deployment_base=target_path,
                game_path=game_path,
                managed_rel_files=managed_rel_files,
                processed_sources=processed_sources,
                detected_mods=detected_mods,
                existing_mod_names=existing_mod_names,
                scan_mode="tree"
            )

    # 2. Inspect known mod subdirectories under game_path
    for rel_dir, scan_mode in KNOWN_GAME_MOD_DIRS:
        full_dir = game_path / rel_dir
        resolved_full_dir = str(full_dir.resolve())
        if full_dir.exists() and full_dir.is_dir() and resolved_full_dir not in scanned_directories:
            scanned_directories.add(resolved_full_dir)
            _scan_directory(
                full_dir,
                deployment_base=game_path,
                game_path=game_path,
                managed_rel_files=managed_rel_files,
                processed_sources=processed_sources,
                detected_mods=detected_mods,
                existing_mod_names=existing_mod_names,
                scan_mode=scan_mode
            )

    return detected_mods


def _scan_directory(
    directory: Path,
    deployment_base: Path,
    game_path: Path,
    managed_rel_files: set,
    processed_sources: set,
    detected_mods: list,
    existing_mod_names: set,
    scan_mode: str = "tree"
):
    """
    Helper to scan a specific directory for unmanaged non-symlink mod files/folders.
    """
    if not directory.exists() or not directory.is_dir():
        return

    # Mode 1: Flat folder (e.g. archive/pc/mod, Content/Paks/~mods)
    # Group files sharing the same stem into one mod
    if scan_mode == "flat":
        stem_groups: Dict[str, list] = {}
        for entry in os.scandir(directory):
            if entry.is_symlink():
                continue
            if not entry.is_file():
                continue
            if entry.name.lower() in IGNORED_FILES or entry.name.startswith("."):
                continue
            if any(entry.name.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue
            if any(entry.name.lower().startswith(p) for p in BASE_PAK_PREFIXES):
                continue

            file_path = Path(entry.path)
            if str(file_path.resolve()) in processed_sources:
                continue

            rel_to_deploy = os.path.normpath(file_path.relative_to(deployment_base))
            if rel_to_deploy in managed_rel_files:
                continue

            # Group by file stem (e.g. MyMod.archive + MyMod.xl -> "MyMod")
            stem = file_path.stem
            stem_groups.setdefault(stem, []).append({
                "source": file_path,
                "rel_path": rel_to_deploy
            })
            processed_sources.add(str(file_path.resolve()))

        for stem, file_entries in stem_groups.items():
            mod_name = _get_unique_mod_name(stem, existing_mod_names, [m["name"] for m in detected_mods])
            detected_mods.append({
                "name": mod_name,
                "folder_name": mod_name,
                "deployment_path": str(deployment_base),
                "files": file_entries,
                "category": "flat_files"
            })

    # Mode 2: Folder-based mod directory (e.g. CET mods, red4ext plugins, Witcher 3 mods/)
    elif scan_mode == "folders":
        for entry in os.scandir(directory):
            if entry.is_symlink():
                continue
            if not entry.is_dir():
                continue
            if entry.name.startswith("."):
                continue

            folder_path = Path(entry.path)
            if str(folder_path.resolve()) in processed_sources:
                continue

            file_entries = []
            for root, _, files in os.walk(folder_path):
                for f in files:
                    fp = Path(root) / f
                    if fp.is_symlink():
                        continue
                    if f.lower() in IGNORED_FILES or f.startswith("."):
                        continue
                    rel_to_deploy = os.path.normpath(fp.relative_to(deployment_base))
                    if rel_to_deploy in managed_rel_files:
                        continue
                    file_entries.append({
                        "source": fp,
                        "rel_path": rel_to_deploy
                    })
                    processed_sources.add(str(fp.resolve()))

            if file_entries:
                mod_name = _get_unique_mod_name(folder_path.name, existing_mod_names, [m["name"] for m in detected_mods])
                detected_mods.append({
                    "name": mod_name,
                    "folder_name": mod_name,
                    "deployment_path": str(deployment_base),
                    "files": file_entries,
                    "category": "folder"
                })

    # Mode 3: General tree (handles both loose files and subfolders)
    elif scan_mode == "tree":
        stem_groups: Dict[str, list] = {}
        for entry in os.scandir(directory):
            if entry.is_symlink():
                continue
            if entry.name.lower() in IGNORED_FILES or entry.name.startswith("."):
                continue

            if entry.is_dir():
                folder_path = Path(entry.path)
                if str(folder_path.resolve()) in processed_sources:
                    continue

                file_entries = []
                for root, _, files in os.walk(folder_path):
                    for f in files:
                        fp = Path(root) / f
                        if fp.is_symlink():
                            continue
                        if f.lower() in IGNORED_FILES or f.startswith("."):
                            continue
                        rel_to_deploy = os.path.normpath(fp.relative_to(deployment_base))
                        if rel_to_deploy in managed_rel_files:
                            continue
                        file_entries.append({
                            "source": fp,
                            "rel_path": rel_to_deploy
                        })
                        processed_sources.add(str(fp.resolve()))

                if file_entries:
                    processed_sources.add(str(folder_path.resolve()))
                    mod_name = _get_unique_mod_name(folder_path.name, existing_mod_names, [m["name"] for m in detected_mods])
                    detected_mods.append({
                        "name": mod_name,
                        "folder_name": mod_name,
                        "deployment_path": str(deployment_base),
                        "files": file_entries,
                        "category": "folder"
                    })
            elif entry.is_file():
                if any(entry.name.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
                    continue
                if any(entry.name.lower().startswith(p) for p in BASE_PAK_PREFIXES):
                    continue

                file_path = Path(entry.path)
                if str(file_path.resolve()) in processed_sources:
                    continue

                rel_to_deploy = os.path.normpath(file_path.relative_to(deployment_base))
                if rel_to_deploy in managed_rel_files:
                    continue

                stem = file_path.stem
                stem_groups.setdefault(stem, []).append({
                    "source": file_path,
                    "rel_path": rel_to_deploy
                })
                processed_sources.add(str(file_path.resolve()))

        for stem, file_entries in stem_groups.items():
            mod_name = _get_unique_mod_name(stem, existing_mod_names, [m["name"] for m in detected_mods])
            detected_mods.append({
                "name": mod_name,
                "folder_name": mod_name,
                "deployment_path": str(deployment_base),
                "files": file_entries,
                "category": "flat_files"
            })


def _get_unique_mod_name(base_name: str, existing_names: set, current_detected_names: list) -> str:
    """Returns a unique mod name avoiding collisions with existing or newly detected mods."""
    sanitized = base_name.strip()
    if not sanitized:
        sanitized = "unnamed_mod"

    candidate = sanitized
    counter = 1
    taken = existing_names.union(set(current_detected_names))
    while candidate in taken:
        candidate = f"{sanitized}_{counter}"
        counter += 1
    return candidate


def migrate_legacy_mods(
    game_info: dict,
    staging_path: Path | str,
    staging_metadata_path: Path | str,
    legacy_mods: List[Dict[str, Any]]
) -> Tuple[int, List[str]]:
    """
    Migrates the detected legacy mods to NOMM's staging directory and creates symlinks.
    Returns (success_count, error_messages).
    """
    staging_path = Path(staging_path)
    staging_meta_path = Path(staging_metadata_path)
    staging_metadata = load_staging_metadata(str(staging_meta_path))

    success_count = 0
    errors = []

    for mod in legacy_mods:
        mod_name = mod["name"]
        folder_name = mod["folder_name"]
        deployment_path = Path(mod["deployment_path"])
        files = mod["files"]

        staging_mod_dir = staging_path / folder_name
        migrated_rel_files = []
        mod_failed = False

        for file_entry in files:
            source_file = Path(file_entry["source"])
            rel_path = file_entry["rel_path"]
            dest_staging_file = staging_mod_dir / rel_path

            if not source_file.exists() and not source_file.is_symlink():
                continue

            try:
                # 1. Create parent folders in staging
                dest_staging_file.parent.mkdir(parents=True, exist_ok=True)

                # 2. Move the real file into staging
                # Note: shutil.move works across different filesystems / mounts
                shutil.move(str(source_file), str(dest_staging_file))

                # 3. Create symlink in place of original file
                source_file.parent.mkdir(parents=True, exist_ok=True)
                os.symlink(dest_staging_file, source_file)

                migrated_rel_files.append(rel_path)
                print(f"[+] Migrated legacy mod file: {source_file} -> {dest_staging_file}")
            except Exception as e:
                err_msg = f"Failed to migrate {source_file}: {e}"
                print(f"[!] {err_msg}")
                errors.append(err_msg)
                mod_failed = True

        if migrated_rel_files and not mod_failed:
            now = datetime.now()
            staging_metadata["mods"][mod_name] = {
                "folder_name": folder_name,
                "display_name": mod_name,
                "mod_files": migrated_rel_files,
                "deployment_path": str(deployment_path),
                "install_timestamp": now,
                "enabled_timestamp": now,
                "is_migrated": True
            }
            if mod_name not in staging_metadata["index"]:
                staging_metadata["index"].append(mod_name)

            success_count += 1

    # Save updated metadata
    write_yaml(staging_metadata, str(staging_meta_path))

    return success_count, errors
