#!/bin/bash

echo "Installing Text Style Converter..."

# Check for required dependencies
REQUIRED_DEPS=("python3" "xclip")
MISSING_DEPS=()

for dep in "${REQUIRED_DEPS[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        MISSING_DEPS+=("$dep")
    fi
done

# Check for either rofi or zenity
if ! command -v rofi &> /dev/null && ! command -v zenity &> /dev/null; then
    MISSING_DEPS+=("rofi (or zenity)")
fi

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "Error: Missing required dependencies:"
    printf '  - %s\n' "${MISSING_DEPS[@]}"
    echo ""
    echo "Install them with:"
    echo "  Ubuntu/Debian: sudo apt install python3 xclip rofi"
    echo "  Fedora: sudo dnf install python3 xclip rofi"
    echo "  Arch: sudo pacman -S python xclip rofi"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --user anthropic

# Copy main script
echo "Installing main script..."
sudo cp text_converter.py /usr/local/bin/text-converter.py
sudo chmod +x /usr/local/bin/text-converter.py

# Install desktop entry
echo "Installing desktop entry..."
mkdir -p ~/.local/share/applications
cp text-converter.desktop ~/.local/share/applications/

# Update desktop database
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

echo ""
echo "Installation complete!"
echo ""
echo "⚠️  IMPORTANT: Set your Anthropic API key:"
echo "  1. Get your API key from: https://console.anthropic.com/"
echo "  2. Add to ~/.bashrc or ~/.zshrc:"
echo "     export ANTHROPIC_API_KEY='your-key-here'"
echo "  3. Reload: source ~/.bashrc (or restart terminal)"
echo ""
echo "Usage:"
echo "  1. Select any text"
echo "  2. Assign a keyboard shortcut to run: /usr/local/bin/text-converter.py"
echo "  3. Or right-click and add to context menu (see setup_context_menu.sh)"
echo ""
