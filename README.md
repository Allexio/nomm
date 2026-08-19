[![Watch the video](https://i.imgur.com/Qdn83As.png)](https://www.youtube.com/watch?v=3UWBQxQY9kk)
<div align="center">
  <a href="https://discord.gg/WFRePSjEQY"><img src="https://img.shields.io/discord/1472479817512521772?color=0098DB&label=Discord&logo=discord&logoColor=0098DB"></a>
</div>

# NOMM (Native Open Mod Manager)

## The project

NOMM is a stupid simple, super clean "native" (as in it runs on Linux without having to use translation tools...) mod manager for Linux.
The goal here is to keep the setup really simple for idiots like me who don't need complex features and all that jazz.
Just a few clicks, a clean, modern interface, and you're done :)

Don't come here expecting it to manage mods for something like Skyrim. There are specific tools for that (see [NaK](https://github.com/SulfurNitride/NaK) or [Jackify](https://github.com/Omni-guides/Jackify)).

Instead, think of NOMM as more of a general purpose tool for most games that just need you to point to a directory and extract some zip files.

> [!WARNING]
> Gemini had a **supporting** role in this project, mainly as a learning tool on the UI development side.
> 
> For the full AI disclaimer head to the [dedicated page on our website](https://nomm.moe/docs/about/values).

### Our Guiding Principles

- No Ads
- No Telemetry
- No User Account Requirement
- Clean & Modern UI/UX
- Beginner-friendly
- Fully open

## Supported Games

NOMM supports a growing library of PC and emulated titles out of the box:

<details>
<summary><b>PC Games (Steam / GOG / Epic Games) - 34+ Games</b></summary>

- 7 Days to Die
- Abiotic Factor
- Baldur's Gate 3
- Blade & Sorcery
- Cat Quest II
- Crash Bandicoot 4: It’s About Time
- Cyberpunk 2077
- Dead as Disco
- FINAL FANTASY VII REBIRTH
- FINAL FANTASY VII REMAKE INTERGRADE
- KINGDOM HEARTS III
- Marvel Rivals
- Metal Gear Solid Δ: Snake Eater
- Monster Hunter Wilds
- Pacific Drive
- Palworld
- Paralives
- PRAGMATA
- Ready or Not
- Resident Evil 2
- Resident Evil 3
- Resident Evil 4
- Resident Evil 7 Biohazard
- Resident Evil Village
- SpongeBob SquarePants: Battle for Bikini Bottom - Rehydrated
- SpongeBob SquarePants: The Cosmic Shake
- Spyro Reignited Trilogy
- STAR WARS Jedi: Fallen Order
- Stellar Blade
- Subnautica
- The Sims 4
- The Witcher 3: Wild Hunt
- Valheim
- Warhammer 40,000: Darktide
</details>

<details>
<summary><b>Nintendo Switch (Ryujinx / Eden / Citron) - 150+ Games</b></summary>

- Animal Crossing: New Horizons
- Bayonetta 1, 2, 3 & Origins
- Fire Emblem: Three Houses & Engage
- Kirby and the Forgotten Land & Star Allies
- Luigi's Mansion 2 HD & 3
- Mario Kart 8 Deluxe
- Mario Party Superstars & Super Mario Party
- Metroid Dread & Metroid Prime Remastered
- Monster Hunter Rise & Generations Ultimate
- Paper Mario: The Origami King & Thousand-Year Door
- Pikmin 1, 2, 3 Deluxe & 4
- Pokémon: Scarlet, Violet, Sword, Shield, Legends: Arceus, Let's Go Pikachu/Eevee, Brilliant Diamond/Shining Pearl
- Splatoon 2 & 3
- Super Mario 3D World + Bowser's Fury
- Super Mario Bros. Wonder
- Super Mario Odyssey
- Super Mario RPG
- Super Smash Bros. Ultimate
- The Legend of Zelda: Breath of the Wild
- The Legend of Zelda: Tears of the Kingdom
- The Legend of Zelda: Link's Awakening & Echoes of Wisdom
- Xenoblade Chronicles: Definitive Edition, 2 & 3
- *...and over 120 more titles!*
</details>

## How can you add support for a game?

One of the main ideas behind this project is that games are defined by easy to create config `.yaml` files.
This means that anyone can create a simple yaml for their game and submit it to the project with little to no coding knowledge and the tool will automate the rest.

You can find out more info on how to add support for your game [here](https://nomm.moe/docs/adding-your-game).

## "Roadmap"

Phase 1 Development Progress:
- [x] Auto-detect Steam libraries
- [x] Auto-detect Steam library games
- [x] Obtain cool images for game tiles from Steam cache folder
- [x] Display results in a super clean library-style window
- [x] Let user choose a downloads folder location
- [x] Create a whole new window with a cool header from Steam cache folder
- [x] Associate app w/ nexusmods download links
- [x] Let user navigate downloaded mods and delete downloaded mods
- [x] Figure out how mod staging and symlinks and whatnot work because I have no idea
- [x] Let user enable/disable mods
- [x] Prepare "essential utilities" section in game config file that lets the community define some essential custom tools that are needed for a game to work, so that the process is easier for people who just want to mod the game (i.e. SKSE, Darktide mod loader, that kind of stuff)
- [x] Let user launch the game directly from the interface
- [x] Add a button to return to launcher from the main window

Phase 2 Development Progress:
- [x] Rudimentary FOMOD support
- [x] Add mod update checker
- [x] Let user skip launcher and go straight to game
- [x] Figure out how to create a flatpak for the app
- [x] Add language-specific strings
- [X] Let user define load orders
- [x] Add support for GOG libraries / games (through Heroic)
- [x] Add support for Epic libraries / games (through Heroic)
- [x] Add support for Nintendo Switch emulation (Ryujinx/Ryubing, Eden, Citron)
- [x] Detect conflicts

Phase 3 Development Progress:
- [x] Manage conflicts (for sure this will be hard without an actually good developer)
- [x] Review access rights to be more restrictive
- [ ] Make a Flathub build
- [x] Handle more complex FOMOD, and handle them cleanly
- [x] Scan & migrate legacy/unmanaged mods in game directories
- [x] GameBanana integration for Switch titles

Bonus (nice to have)
- [ ] Game profiles?
- [ ] ???

## Installing/Running

### Flatpak
The easiest way to run the app is with flatpak!

To do so:

1. Go to the [releases](https://github.com/Allexio/nomm/releases) tab.
2. Expand the `Assets` box of the latest version
3. Click on the `nomm.flatpak` file to download it
4. Once downloaded, if you have KDE/GNOME you may simply double click the file. This should boot up `KDE Discover` or `Gnome Software`.
5. Once there you should have a button to install the app, click it.
6. Once installed, you will see a `Launch` or `Run` button appear, click it.

Or via command line:
```bash
flatpak install nomm.flatpak
flatpak run moe.nomm.Nomm
```

### Arch Linux / AUR
NOMM is available on the Arch User Repository (AUR):
```bash
yay -S nomm
# or for the latest development version:
yay -S nomm-nightly-git
```

## Building

### Dependencies

The app is built with:
- [Python](https://www.python.org/) (>= 3.10)
- [GTK](https://www.gtk.org/) (4.0) & [Libadwaita](https://gnome.pages.gitlab.gnome.org/libadwaita/) (via `python-gobject`)
- [Requests](https://pypi.org/project/requests/) -> API requests to Nexus Mods, GameBanana, etc.
- [rarfile](https://pypi.org/project/rarfile/) & [7-Zip](https://www.7-zip.org/) (`p7zip`) -> extraction of mod archives
- [vdf](https://github.com/ValvePython/vdf) -> read Steam library and config files
- [PyYAML](https://pyyaml.org/) -> read and write game definitions and staging metadata

### Running directly from source

Make sure dependencies are installed, then run:
```bash
python3 src/main.py
```

### Building packages

1. Clone the repository:
```bash
git clone https://github.com/Allexio/nomm.git
cd nomm
```

2. Make `build.sh` executable:
```bash
chmod +x ./build/build.sh
```

#### Flatpak
```bash
./build/build.sh flatpak
```
This will create `nomm.flatpak` in the repository root.

#### AUR (Arch Linux)
- To build and install the release package:
```bash
./build/build.sh aur
```
- To build and install the latest nightly version:
```bash
./build/build.sh aur-nightly
```
