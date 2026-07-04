#!/bin/bash

# Build flatpak
if [ $1 == "flatpak" ]; then
    ./build/flatpak/build-flatpak.sh
fi

# Build flatpak Devel variant (installs alongside the release build as com.nomm.Nomm.Devel)
if [ $1 == "flatpak-devel" ]; then
    chmod +x ./build/flatpak/build-flatpak-devel.sh
    ./build/flatpak/build-flatpak-devel.sh
fi

# Build AUR package
if [ $1 == "aur" ]; then
    cd "$(dirname "$0")/aur"
    makepkg -si
fi