#!/usr/bin/env python3
import os
import shutil
import subprocess
import tarfile
from datetime import datetime

# Define color codes for pretty output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

def log_info(msg):
    print(f"{BLUE}[INFO]{RESET} {msg}")

def log_success(msg):
    print(f"{GREEN}[SUCCESS] {msg}{RESET}")

def log_warn(msg):
    print(f"{YELLOW}[WARNING] {msg}{RESET}")

def log_error(msg):
    print(f"{RED}[ERROR] {msg}{RESET}")

def main():
    print(f"\n{BOLD}{BLUE}=================================================={RESET}")
    print(f"{BOLD}{GREEN}      PIKA HYPRLAND CONFIGURATION BACKUP TOOL     {RESET}")
    print(f"{BOLD}{BLUE}=================================================={RESET}\n")

    home = os.path.expanduser("~")
    projects_dir = "/home/sarath/projects"
    backup_name = "user_config_backup"
    temp_backup_dir = os.path.join(projects_dir, backup_name)
    tarball_path = os.path.join(projects_dir, f"{backup_name}.tar.gz")

    # 1. Clean up old backups/temp dirs if they exist
    if os.path.exists(temp_backup_dir):
        shutil.rmtree(temp_backup_dir)
    if os.path.exists(tarball_path):
        os.remove(tarball_path)

    os.makedirs(temp_backup_dir, exist_ok=True)
    os.makedirs(os.path.join(temp_backup_dir, ".config"), exist_ok=True)

    # 2. Key configuration directories to backup
    config_dirs = [
        "hypr",
        "pikabar-quickshell",
        "kitty",
        "rofi",
        "wlogout",
        "fish",
        "waybar",
        "cava",
        "fastfetch",
        "btop",
        "swaync",
        "walker",
        "waypaper",
        "qt6ct",
        "matugen",
        "ml4w",
        "nwg-look",
        "pipewire",
        "pulse",
        "corectrl",
        "mpv",
        "yazi",
        "systemd"
    ]

    log_info("Backing up .config directories...")
    for d in config_dirs:
        src = os.path.join(home, ".config", d)
        dst = os.path.join(temp_backup_dir, ".config", d)
        if os.path.exists(src):
            log_info(f"  -> Copying .config/{d}...")
            shutil.copytree(src, dst, symlinks=True)
        else:
            log_warn(f"  .config/{d} not found, skipping.")

    # 3. Individual home files to backup
    home_files = [
        ".bashrc",
        ".profile",
        ".zshrc",
        ".gtkrc-2.0",
        ".Xresources"
    ]

    log_info("Backing up home configuration files...")
    for f in home_files:
        src = os.path.join(home, f)
        dst = os.path.join(temp_backup_dir, f)
        if os.path.exists(src):
            log_info(f"  -> Copying {f}...")
            shutil.copy2(src, dst)
        else:
            log_warn(f"  {f} not found in home, skipping.")

    # 3.5 Backup .local/bin directory
    log_info("Backing up .local/bin custom scripts...")
    src_bin = os.path.join(home, ".local", "bin")
    dst_bin = os.path.join(temp_backup_dir, ".local", "bin")
    if os.path.exists(src_bin):
        os.makedirs(os.path.join(temp_backup_dir, ".local"), exist_ok=True)
        shutil.copytree(src_bin, dst_bin, symlinks=True)
        log_success("  -> Copied .local/bin successfully.")
    else:
        log_warn("  .local/bin not found, skipping.")

    # 4. Export Package Lists
    log_info("Exporting lists of installed packages...")
    
    # APT packages
    try:
        apt_cmd = "dpkg-query -f '${binary:Package}\n' -W"
        apt_list = subprocess.check_output(apt_cmd, shell=True, text=True)
        with open(os.path.join(temp_backup_dir, "apt_packages.txt"), "w") as f:
            f.write(apt_list)
        log_success("  -> Exported APT packages to apt_packages.txt")
    except Exception as e:
        log_error(f"Failed to export APT packages: {e}")

    # Flatpak packages
    try:
        if shutil.which("flatpak"):
            flatpak_cmd = "flatpak list --columns=application"
            flatpak_list = subprocess.check_output(flatpak_cmd, shell=True, text=True)
            # Remove header line if present
            flatpak_lines = [l.strip() for l in flatpak_list.split("\n") if l.strip() and "Application ID" not in l]
            with open(os.path.join(temp_backup_dir, "flatpak_packages.txt"), "w") as f:
                f.write("\n".join(flatpak_lines))
            log_success("  -> Exported Flatpak packages to flatpak_packages.txt")
        else:
            log_warn("  Flatpak not installed, skipping flatpak export.")
    except Exception as e:
        log_error(f"Failed to export Flatpak packages: {e}")

    # 5. Compress into tar.gz
    log_info(f"Compressing backup into {tarball_path}...")
    try:
        with tarfile.open(tarball_path, "w:gz") as tar:
            tar.add(temp_backup_dir, arcname=backup_name)
        log_success(f"Backup compressed successfully! ({os.path.getsize(tarball_path)/1024/1024:.2f} MB)")
    except Exception as e:
        log_error(f"Compression failed: {e}")
        return

    # Clean up temp folder
    shutil.rmtree(temp_backup_dir)
    log_info("Temporary backup directory cleaned up.")

    # 6. Copy to external BTRFS SSD mount point (/mnt/data or /mnt/backup) if available
    search_mounts = ["/mnt/data", "/mnt/backup"]
    btrfs_mount = ""
    for mount in search_mounts:
        if os.path.ismount(mount):
            btrfs_mount = mount
            break

    if btrfs_mount:
        log_info(f"BTRFS Backup SSD detected at {btrfs_mount}. Copying files...")
        try:
            shutil.copy2(tarball_path, os.path.join(btrfs_mount, f"{backup_name}.tar.gz"))
            shutil.copy2(os.path.join(projects_dir, "restore_system.py"), os.path.join(btrfs_mount, "restore_system.py"))
            shutil.copy2(os.path.join(projects_dir, "backup_system.py"), os.path.join(btrfs_mount, "backup_system.py"))
            if os.path.exists(os.path.join(projects_dir, "README.md")):
                shutil.copy2(os.path.join(projects_dir, "README.md"), os.path.join(btrfs_mount, "README.md"))
            log_success(f"Successfully copied backups and scripts to BTRFS SSD at {btrfs_mount}!")
            
            # Sync wallpapers and pictures directly to SSD to avoid bloat in Git tarball
            log_info("Syncing high-resolution wallpapers and video backgrounds to BTRFS SSD...")
            wp_src = os.path.join(home, "wallpapers")
            wp_dst = os.path.join(btrfs_mount, "wallpapers")
            if os.path.exists(wp_src):
                if os.path.exists(wp_dst):
                    shutil.rmtree(wp_dst)
                shutil.copytree(wp_src, wp_dst, symlinks=True)
                log_success("  -> Synced live video wallpapers successfully!")
                
            pics_src = os.path.join(home, "Pictures", "Wallpapers")
            pics_dst = os.path.join(btrfs_mount, "Pictures", "Wallpapers")
            if os.path.exists(pics_src):
                os.makedirs(os.path.dirname(pics_dst), exist_ok=True)
                if os.path.exists(pics_dst):
                    shutil.rmtree(pics_dst)
                shutil.copytree(pics_src, pics_dst, symlinks=True)
                log_success("  -> Synced static wallpapers successfully!")
        except Exception as e:
            log_error(f"Failed to copy/sync backups to BTRFS SSD: {e}")
    else:
        log_warn(f"BTRFS Backup SSD not mounted at {btrfs_mount}. Backup only saved locally.")

    print(f"\n{BOLD}{GREEN}=================================================={RESET}")
    print(f"{BOLD}{GREEN}   BACKUP CREATED SUCCESSFULLY!                  {RESET}")
    print(f"{BOLD}{GREEN}   Tarball location: {tarball_path}              {RESET}")
    if os.path.ismount(btrfs_mount):
        print(f"{BOLD}{GREEN}   SSD Backup location: {btrfs_mount}/{backup_name}.tar.gz{RESET}")
    print(f"{BOLD}{GREEN}=================================================={RESET}\n")

if __name__ == "__main__":
    main()
