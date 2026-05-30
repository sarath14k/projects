# 🚀 Pika Hyprland System Backup & Restore Guide

Your system configuration backup is **100% complete, verified, and safely pushed to your remote GitHub repository**! 

Everything has been committed to a dedicated backup branch named `pre-reinstall-backup` on your GitHub repository (`git@github.com:sarath14k/projects.git`). This guarantees that even if you format your entire drive, not a single line of your custom configurations or active code projects will be lost.

---

## 📦 What Was Backed Up?

We created an intelligent, lightweight backup script (`backup_system.py`) that gathered your entire personal desktop experience, omitting large cache and browser directories to keep it extremely fast and compact (only **1.21 MB**).

Inside the compressed `user_config_backup.tar.gz` archive (committed in your git repo):
* **Live Desktop Configs (`.config/`)**:
  * `hypr` — Your exact active tiling window manager binds, flat-file structures, wallpaper setups, and settings.
  * `pikabar-quickshell` — Your custom-made premium MacBook-style neon docks/bars.
  * `kitty` — Terminal configuration.
  * `rofi` — Launcher configs.
  * `wlogout` — Lock/session manager styles.
  * `fish` — Custom shell environment and bindings.
  * `cava` — Audio visualizer settings.
  * `pipewire` & `pulse` — Audio routing properties (critical for MeetShare audio matrix!).
  * `qt6ct` & `nwg-look` — System-wide GTK and Qt styling preferences.
  * `corectrl` — Custom GPU/CPU performance profiles.
* **Home Profiles**:
  * `.bashrc` & `.profile` — Shell startup routines, custom environment variables, and active aliases.
* **Package Lists**:
  * `apt_packages.txt` — List of all installed system packages.
  * `flatpak_packages.txt` — List of all custom flatpak apps (Protontricks, Proton VPN, FreeTube, LocalSend).

---

## 🔍 GitHub Folder Status: **PERFECTLY OK!**

Your GitHub folder (`/home/sarath/projects`) has been checked. We successfully staged **all** of your:
1. **Local modifications** (such as NeetCode practice programs, VocalPulse audio files, custom style sheets, etc.).
2. **Untracked projects** (like the `pareto-practice-tracker`, `webremote-pro`, Java files, compile scripts).
3. **Backup scripts and tarball** (`backup_system.py`, `restore_system.py`, `user_config_backup.tar.gz`).

All of these have been securely pushed. If you visit your GitHub repository page, you will see the `pre-reinstall-backup` branch contains everything in its exact state.

---

## 🛠️ How to Restore (Reload Your Configurations)

After installing your fresh **Pika Hyprland** system, restoring your entire workspace to the exact state it is in right now takes just a few steps:

### Step 1: Install Git & Clone Your Repository
Open a terminal in your fresh install and run:
```bash
# Install git
sudo apt update && sudo apt install -y git

# Create projects directory and clone the backup branch
mkdir -p ~/projects
cd ~/projects
git clone -b pre-reinstall-backup git@github.com:sarath14k/projects.git .
```

### Step 2: Restore All System Configurations
We wrote a powerful automated restore tool (`restore_system.py`) that handles all extracting, directory creation, and configuration safety checks. Simply run:
```bash
# Run the automated restore script
python3 restore_system.py
```
> [!NOTE]
> `restore_system.py` will automatically look for `user_config_backup.tar.gz` in `~/projects`, extract it, copy it to your home directory (`~/.config`, etc.), and **safely move any pre-existing configs to a backup folder** so nothing is ever overwritten or lost!

### Step 3: Reinstall All APT Packages
To install all system packages you previously had, run this single command:
```bash
sudo apt update && sudo apt install -y $(cat ~/projects/user_config_backup/apt_packages.txt | tr '\n' ' ')
```

### Step 4: Reinstall All Flatpak Applications
To restore your Flatpaks (ProtonVPN, Protontricks, FreeTube, LocalSend, etc.) instantly, run:
```bash
xargs -a ~/projects/user_config_backup/flatpak_packages.txt flatpak install -y
```

### Step 5: Merge Backup to Main (Optional)
Once you are fully satisfied with the restore and everything is working perfectly, you can merge your backup branch back to `main`:
```bash
git checkout main
git merge pre-reinstall-backup
git push origin main
```

---

## 🛡️ Timeshift vs. Personal Config Backup (Crucial Info)

> [!WARNING]
> **Why Timeshift shouldn't be used for clean reinstalls:**
> Timeshift is an operating system utility designed for system rollback points (it takes BTRFS or Rsync snapshots of system directories like `/etc`, `/usr`, `/var`, `/boot`). By default, it **excludes your home directory (`/home/sarath`)**.
> 
> If you reinstall your OS, the installer formats the root partition, wiping old Timeshift snapshots. Even if you back up Timeshift to an external drive, restoring an operating system backup from one installation onto a new installation is highly dangerous. It will overwrite critical system libraries, systemd configurations, and display managers, causing black screens, boot loops, or immediate crashes.
> 
> The **Personal Config Backup** we completed is the industry standard for OS migration. It leaves system libraries untouched but completely restores your user interface, styling, keybindings, and packages, giving you a 100% clean boot with 100% familiar settings!
