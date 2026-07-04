# Builds and installs the Devel variant (com.nomm.Nomm.Devel) alongside the release build.
# Reuses the already-generated python3-modules.json — rerun build-flatpak.sh's generator step
# first if you've changed Python dependencies.

flatpak-builder --user --install --force-clean --repo=repo-devel build-dir-devel ./build/flatpak/com.nomm.Nomm.Devel.yaml

flatpak build-bundle ./repo-devel NOMM-devel.flatpak com.nomm.Nomm.Devel
