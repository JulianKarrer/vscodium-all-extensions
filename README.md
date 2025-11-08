# Transfer all Extensions from VSCode to VSCodium

Automatically migrate all extensions from VSCode to [VSCodium](https://vscodium.com/), which is the exact VSCode source code but packaged without telemetry and tracking.

Gets the installed extensions, downloads them, fixes the resulting broken ZIP archives, which requires `bsdtar` (Linux: `sudo apt install libarchive-tools`) and installs the extensions to `codium`. 

