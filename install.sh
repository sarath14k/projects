#!/bin/bash

# Define paths
INSTALL_DIR="$HOME/.local/share/vocalpulse"
BIN_DIR="$HOME/.local/bin"
APP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/scalable/apps"

echo "Installing VocalPulse..."

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$APP_DIR"
mkdir -p "$ICON_DIR"

# Copy application files
cp vocal_analyzer.py gui.py "$INSTALL_DIR/"
cp -r venv "$INSTALL_DIR/"

# Install icon
cp vocalpulse.svg "$ICON_DIR/vocalpulse.svg"

# Create wrapper script
cat <<EOF > "$BIN_DIR/vocalpulse"
#!/bin/bash
export GI_TYPELIB_PATH=/usr/lib/x86_64-linux-gnu/girepository-1.0
cd "$INSTALL_DIR"
./venv/bin/python3 gui.py "\$@"
EOF

chmod +x "$BIN_DIR/vocalpulse"

# Install desktop file
cp vocalpulse.desktop "$APP_DIR/"

# Update desktop database
update-desktop-database "$APP_DIR" 2>/dev/null || true

echo "Installation complete! You can now find VocalPulse in your application menu."
