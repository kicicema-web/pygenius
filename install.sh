#!/bin/bash
# PyGenius AI - Linux Installer

set -e

echo "========================================"
echo "  PyGenius AI - Linux Installer"
echo "========================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>/dev/null | grep -oP '\d+\.\d+' | head -1)
if [ -z "$PYTHON_VERSION" ]; then
    echo "Error: Python 3 is not installed!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

REQUIRED_VERSION="3.8"
if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then 
    echo "Error: Python $PYTHON_VERSION is too old!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python $PYTHON_VERSION found"

# Install requests if not present
if ! python3 -c "import requests" 2>/dev/null; then
    echo "Installing requests package..."
    pip3 install --user requests
fi

echo "✓ Dependencies OK"

# Create install directory
INSTALL_DIR="$HOME/.local/share/pygenius"
mkdir -p "$INSTALL_DIR"

# Copy files
cp pygenius_desktop.py "$INSTALL_DIR/"
cp pygenius "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/pygenius"
chmod +x "$INSTALL_DIR/pygenius_desktop.py"

# Create symlink in ~/.local/bin
mkdir -p "$HOME/.local/bin"
ln -sf "$INSTALL_DIR/pygenius" "$HOME/.local/bin/pygenius"

# Create desktop entry
DESKTOP_DIR="$HOME/.local/share/applications"
mkdir -p "$DESKTOP_DIR"

cat > "$DESKTOP_DIR/pygenius.desktop" << 'EOF'
[Desktop Entry]
Name=PyGenius AI
Comment=Python coding assistant with AI-powered features
Exec=pygenius
Type=Application
Icon=applications-python
Categories=Development;IDE;Education;
Terminal=false
EOF

echo ""
echo "========================================"
echo "  Installation Complete!"
echo "========================================"
echo ""
echo "PyGenius AI has been installed to:"
echo "  $INSTALL_DIR"
echo ""
echo "To run:"
echo "  pygenius"
echo ""
echo "Or find it in your applications menu."
echo ""
echo "Make sure ~/.local/bin is in your PATH:"
echo '  export PATH="$HOME/.local/bin:$PATH"'
echo ""
