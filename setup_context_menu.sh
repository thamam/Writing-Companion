#!/bin/bash

# This script sets up right-click context menu integration
# Note: Implementation varies by desktop environment

DE=$(echo "$XDG_CURRENT_DESKTOP" | tr '[:upper:]' '[:lower:]')

echo "Detected Desktop Environment: $DE"
echo ""

case "$DE" in
    *gnome*|*ubuntu*)
        echo "For GNOME/Ubuntu:"
        echo "1. Install nautilus-actions (for Nautilus file manager):"
        echo "   sudo apt install nautilus-actions"
        echo ""
        echo "2. Or add a custom keyboard shortcut:"
        echo "   Settings → Keyboard → Custom Shortcuts"
        echo "   Command: /usr/local/bin/text-converter.py"
        echo "   Shortcut: Ctrl+Alt+T (or your choice)"
        ;;

    *kde*|*plasma*)
        echo "For KDE Plasma:"
        echo "1. Add custom keyboard shortcut:"
        echo "   System Settings → Shortcuts → Custom Shortcuts"
        echo "   Command: /usr/local/bin/text-converter.py"
        echo "   Trigger: Ctrl+Alt+T (or your choice)"
        echo ""
        echo "2. For Dolphin context menu:"
        echo "   Create: ~/.local/share/kservices5/text-converter.desktop"
        ;;

    *xfce*)
        echo "For XFCE:"
        echo "1. Add keyboard shortcut:"
        echo "   Settings → Keyboard → Application Shortcuts"
        echo "   Command: /usr/local/bin/text-converter.py"
        echo "   Shortcut: Ctrl+Alt+T (or your choice)"
        ;;

    *)
        echo "Generic setup:"
        echo "Add a keyboard shortcut in your DE settings:"
        echo "  Command: /usr/local/bin/text-converter.py"
        echo "  Suggested shortcut: Ctrl+Alt+T"
        ;;
esac

echo ""
echo "Recommended approach for all DEs:"
echo "  Set up a keyboard shortcut - most reliable across environments"
echo ""
