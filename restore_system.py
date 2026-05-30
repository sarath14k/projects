#!/usr/bin/env python3
import os
import shutil
import subprocess
import tarfile

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
    print(f"{BOLD}{GREEN}      PIKA HYPRLAND CONFIGURATION RESTORE TOOL    {RESET}")
    print(f"{BOLD}{BLUE}=================================================={RESET}\n")

    home = os.path.expanduser("~")
    projects_dir = "/home/sarath/projects"
    backup_name = "user_config_backup"
    temp_extract_dir = os.path.join(projects_dir, f"{backup_name}_extracted")

    # Search paths for the backup archive
    search_mounts = ["/mnt/data", "/mnt/backup"]
    tarball_path = ""
    active_mount = ""
    
    for mount in search_mounts:
        test_path = os.path.join(mount, f"{backup_name}.tar.gz")
        if os.path.exists(test_path):
            tarball_path = test_path
            active_mount = mount
            log_info(f"Using backup archive from BTRFS SSD: {tarball_path}")
            break
            
    if not tarball_path:
        local_tarball = os.path.join(projects_dir, f"{backup_name}.tar.gz")
        if os.path.exists(local_tarball):
            tarball_path = local_tarball
            log_info(f"Using local backup archive: {tarball_path}")
        else:
            log_error(f"Backup archive not found in /mnt/data/, /mnt/backup/, or {projects_dir}!")
            log_info("Please ensure your BTRFS SSD is mounted at /mnt/data or /mnt/backup, or run backup_system.py first.")
            return

    # 1. Extract tarball
    log_info(f"Extracting {tarball_path}...")
    if os.path.exists(temp_extract_dir):
        shutil.rmtree(temp_extract_dir)
        
    try:
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=temp_extract_dir)
        log_success("Backup extracted successfully.")
    except Exception as e:
        log_error(f"Failed to extract backup: {e}")
        return

    extracted_root = os.path.join(temp_extract_dir, backup_name)
    extracted_config = os.path.join(extracted_root, ".config")

    # 2. Restore .config directories
    if os.path.exists(extracted_config):
        log_info("Restoring .config directories...")
        for d in os.listdir(extracted_config):
            src = os.path.join(extracted_config, d)
            dst = os.path.join(home, ".config", d)
            if os.path.isdir(src):
                # Backup existing config folder if it exists
                if os.path.exists(dst):
                    backup_dst = dst + f"_pre_restore_backup"
                    if os.path.exists(backup_dst):
                        shutil.rmtree(backup_dst)
                    shutil.move(dst, backup_dst)
                    log_warn(f"  Existing .config/{d} backed up to .config/{d}_pre_restore_backup")
                
                shutil.copytree(src, dst, symlinks=True)
                log_success(f"  -> Restored .config/{d}")

    # 3. Restore individual home files
    log_info("Restoring home files...")
    for f in os.listdir(extracted_root):
        src = os.path.join(extracted_root, f)
        if os.path.isfile(src) and f.startswith("."):
            dst = os.path.join(home, f)
            if os.path.exists(dst):
                backup_dst = dst + f"_pre_restore_backup"
                if os.path.exists(backup_dst):
                    os.remove(backup_dst)
                shutil.move(dst, backup_dst)
                log_warn(f"  Existing {f} backed up to {f}_pre_restore_backup")
            
            shutil.copy2(src, dst)
            log_success(f"  -> Restored {f}")

    # 3.5 Restore .local/bin directory
    extracted_local = os.path.join(extracted_root, ".local")
    if os.path.exists(extracted_local):
        log_info("Restoring .local/bin custom scripts...")
        src_bin = os.path.join(extracted_local, "bin")
        dst_bin = os.path.join(home, ".local", "bin")
        if os.path.exists(src_bin):
            if os.path.exists(dst_bin):
                backup_dst = dst_bin + "_pre_restore_backup"
                if os.path.exists(backup_dst):
                    shutil.rmtree(backup_dst)
                shutil.move(dst_bin, backup_dst)
                log_warn("  Existing .local/bin backed up to .local/bin_pre_restore_backup")
            
            os.makedirs(os.path.dirname(dst_bin), exist_ok=True)
            shutil.copytree(src_bin, dst_bin, symlinks=True)
            log_success("  -> Restored .local/bin successfully.")

    # 3.6 Restore SSH keys from BTRFS SSD (Secure physical copy)
    ssh_mount = active_mount if active_mount else ""
    if not ssh_mount:
        for mount in search_mounts:
            if os.path.ismount(mount):
                ssh_mount = mount
                break
                
    if ssh_mount:
        src_ssh = os.path.join(ssh_mount, ".ssh")
        dst_ssh = os.path.join(home, ".ssh")
        if os.path.exists(src_ssh):
            log_info("Restoring secure SSH keys from BTRFS SSD...")
            if os.path.exists(dst_ssh):
                backup_dst = dst_ssh + "_pre_restore_backup"
                if os.path.exists(backup_dst):
                    shutil.rmtree(backup_dst)
                shutil.move(dst_ssh, backup_dst)
                log_warn("  Existing ~/.ssh backed up to ~/.ssh_pre_restore_backup")
            
            shutil.copytree(src_ssh, dst_ssh, symlinks=True)
            # Ensure correct, tight Unix permissions for SSH keys
            os.chmod(dst_ssh, 0o700)
            for f in os.listdir(dst_ssh):
                file_path = os.path.join(dst_ssh, f)
                if os.path.isfile(file_path):
                    if "pub" in f or f == "known_hosts":
                        os.chmod(file_path, 0o644)
                    else:
                        os.chmod(file_path, 0o600)
            log_success("  -> Restored secure SSH keys successfully with correct permissions!")

    # 3.7 Restore high-resolution wallpapers and video backgrounds
    wp_mount = active_mount if active_mount else ""
    if not wp_mount:
        for mount in search_mounts:
            if os.path.ismount(mount):
                wp_mount = mount
                break
                
    if wp_mount:
        log_info(f"Restoring high-resolution wallpapers and video backgrounds from BTRFS SSD at {wp_mount}...")
        
        # Restore live video wallpapers
        wp_src = os.path.join(wp_mount, "wallpapers")
        wp_dst = os.path.join(home, "wallpapers")
        if os.path.exists(wp_src):
            if os.path.exists(wp_dst):
                shutil.rmtree(wp_dst)
            shutil.copytree(wp_src, wp_dst, symlinks=True)
            log_success("  -> Restored live video wallpapers successfully!")
            
        # Restore static wallpapers
        pics_src = os.path.join(wp_mount, "Pictures", "Wallpapers")
        pics_dst = os.path.join(home, "Pictures", "Wallpapers")
        if os.path.exists(pics_src):
            os.makedirs(os.path.dirname(pics_dst), exist_ok=True)
            if os.path.exists(pics_dst):
                shutil.rmtree(pics_dst)
            shutil.copytree(pics_src, pics_dst, symlinks=True)
            log_success("  -> Restored static wallpapers successfully!")

    # 4. Reinstall Packages
    apt_file = os.path.join(extracted_root, "apt_packages.txt")
    flatpak_file = os.path.join(extracted_root, "flatpak_packages.txt")

    print(f"\n{BOLD}{GREEN}=================================================={RESET}")
    print(f"{BOLD}{GREEN}          AUTOMATIC PACKAGE INSTALLATION          {RESET}")
    print(f"{BOLD}{GREEN}=================================================={RESET}\n")

    try:
        install_choice = input(f"{BOLD}{YELLOW}Do you want to automatically reinstall all APT and Flatpak packages now? [Y/n]: {RESET}").strip().lower()
    except (KeyboardInterrupt, EOFError):
        install_choice = "n"
        
    if install_choice in ["", "y", "yes"]:
        # Reinstall APT packages
        if os.path.exists(apt_file):
            log_info("Reinstalling APT packages...")
            try:
                with open(apt_file, "r") as f:
                    apt_pkgs = [line.strip() for line in f if line.strip()]
                
                if apt_pkgs:
                    log_info("Running sudo apt update...")
                    subprocess.run(["sudo", "apt", "update"], check=True)
                    
                    log_info("Installing packages via apt...")
                    cmd = f"sudo apt install -y {' '.join(apt_pkgs)}"
                    subprocess.run(cmd, shell=True, check=True)
                    log_success("APT packages reinstalled successfully.")
            except Exception as e:
                log_error(f"Failed to reinstall APT packages: {e}")
        
        # Reinstall Flatpak packages
        if os.path.exists(flatpak_file):
            log_info("Reinstalling Flatpak applications...")
            try:
                with open(flatpak_file, "r") as f:
                    flatpak_pkgs = [line.strip() for line in f if line.strip()]
                
                if flatpak_pkgs:
                    log_info("Installing Flatpak packages...")
                    cmd = f"flatpak install -y {' '.join(flatpak_pkgs)}"
                    subprocess.run(cmd, shell=True, check=True)
                    log_success("Flatpak applications reinstalled successfully.")
            except Exception as e:
                log_error(f"Failed to reinstall Flatpak packages: {e}")
    else:
        log_info("Skipping automatic package installation. You can run them manually later:")
        if os.path.exists(apt_file):
            print(f"  APT: sudo apt update && sudo apt install -y $(cat {apt_file} | tr '\\n' ' ')")
        if os.path.exists(flatpak_file):
            print(f"  Flatpak: xargs -a {flatpak_file} flatpak install -y")

    # Clean up extracted temp directory
    shutil.rmtree(temp_extract_dir)
    log_info("Temporary extraction directory cleaned up.")

    print(f"\n{BOLD}{GREEN}=================================================={RESET}")
    print(f"{BOLD}{GREEN}      RESTORE PROCESS COMPLETED SUCCESSFULLY!    {RESET}")
    print(f"{BOLD}{GREEN}=================================================={RESET}\n")

if __name__ == "__main__":
    main()
