#!/bin/bash

# This script must be run with sudo
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (use sudo)"
  exit
fi

echo "Updating SDDM configuration..."
cat <<EOF > /etc/sddm.conf
[Autologin]
User=sarath
Session=hyprland-uwsm
EOF

echo "Updating GRUB configuration..."
sed -i 's/splash//g' /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg

echo "Done! Please reboot to see the changes."
