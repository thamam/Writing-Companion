# Text Style Converter

A powerful Linux desktop tool for converting selected text into different styles using Claude AI. Transform your writing instantly with right-click or keyboard shortcut activation.

## Features

### 10 Conversion Modes

1. **More Formal** - Professional/academic style with elevated language
2. **More Stylish** - Engaging format with rhetorical flair and vivid language
3. **WhatsApp Appropriate** - Casual messaging style for everyday chat
4. **LinkedIn Post Material** - Professional social media content with engagement hooks
5. **Discord Material** - Community chat style with internet-aware language
6. **Casual Format** - Friendly, relaxed tone for informal communication
7. **Natural - Fix Typos & Grammar** - Comprehensive error correction while maintaining style
8. **Typos Only** - Fix spelling errors without changing structure
9. **Grammar Only** - Correct grammar and punctuation without rephrasing
10. **Add Emojis** - Enhance expressiveness with appropriate emoji placement

### Key Features

- **System-wide integration**: Works in any application (browsers, text editors, chat apps)
- **Quick conversion**: Select text → shortcut → choose mode → paste
- **Smart clipboard**: Automatically copies converted text
- **Desktop notifications**: Visual feedback for each step
- **Dual UI options**: Uses rofi (preferred) or zenity (fallback)
- **High-quality output**: Powered by Claude Sonnet 4 for natural conversions

## Installation

### 1. Prerequisites

Install required system packages:

**Ubuntu/Debian:**
```bash
sudo apt install python3 python3-pip xclip rofi
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip xclip rofi
```

**Arch Linux:**
```bash
sudo pacman -S python xclip rofi
```

**Optional:** Install `zenity` as fallback if you don't want `rofi`:
```bash
sudo apt install zenity  # Ubuntu/Debian
```

### 2. Clone and Install

```bash
# Clone the repository
git clone https://github.com/thamam/Writing-Companion.git
cd Writing-Companion

# Make scripts executable
chmod +x install.sh setup_context_menu.sh text_converter.py

# Run installation
./install.sh
```

The installer will:
- Check for required dependencies
- Install Python packages (anthropic)
- Copy script to `/usr/local/bin/`
- Install desktop entry
- Display setup instructions

### 3. Configure API Key

1. **Get your API key** from [Anthropic Console](https://console.anthropic.com/)

2. **Add to shell configuration:**

   For Bash (edit `~/.bashrc`):
   ```bash
   echo "export ANTHROPIC_API_KEY='sk-ant-your-key-here'" >> ~/.bashrc
   source ~/.bashrc
   ```

   For Zsh (edit `~/.zshrc`):
   ```bash
   echo "export ANTHROPIC_API_KEY='sk-ant-your-key-here'" >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Verify it's set:**
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

### 4. Set Up Activation Method

Run the context menu setup helper:
```bash
./setup_context_menu.sh
```

**Recommended: Keyboard Shortcut (Works on all DEs)**

**GNOME/Ubuntu:**
- Settings → Keyboard → Keyboard Shortcuts → Custom Shortcuts
- Click "+" to add new shortcut
- Name: "Text Style Converter"
- Command: `/usr/local/bin/text-converter.py`
- Shortcut: `Ctrl+Alt+T` (or your preference)

**KDE Plasma:**
- System Settings → Shortcuts → Custom Shortcuts
- Edit → New → Global Shortcut → Command/URL
- Command: `/usr/local/bin/text-converter.py`
- Trigger: `Ctrl+Alt+T`

**XFCE:**
- Settings → Keyboard → Application Shortcuts
- Add → `/usr/local/bin/text-converter.py`
- Press your desired key combo

## Usage

### Basic Workflow

1. **Select text** in any application (browser, editor, chat, etc.)
2. **Press your keyboard shortcut** (e.g., `Ctrl+Alt+T`)
3. **Choose conversion mode** from the popup menu
4. **Wait for notification** confirming conversion
5. **Paste** the converted text with `Ctrl+V`

### Example Use Cases

**Making professional communication:**
```
Original (casual): "hey can u check this out when u get a chance?"
Mode: More Formal
Result: "Hello, would you please review this at your earliest convenience?"
```

**Creating LinkedIn content:**
```
Original: "Just launched our new feature. It's pretty cool."
Mode: LinkedIn Post Material
Result: "Excited to announce the launch of our new feature! 🚀

After months of development, we've built something that will transform how teams collaborate...

What features would you like to see next?"
```

**Quick typo fixes:**
```
Original: "Recieved the documment, will reveiw it tomorow."
Mode: Typos Only
Result: "Received the document, will review it tomorrow."
```

## How It Works

### Technical Flow

1. **Text Capture**: Uses `xclip` to read selected text from X11 primary selection
2. **Mode Selection**: Displays rofi/zenity dialog with 10 conversion options
3. **API Call**: Sends text to Claude API with mode-specific prompt
4. **Clipboard Copy**: Uses `xclip` to copy result to clipboard
5. **Notification**: Shows desktop notification via `notify-send`

### Architecture

```
┌─────────────────┐
│  Selected Text  │
└────────┬────────┘
         │ xclip -o
         ▼
┌─────────────────┐
│ Mode Selector   │ rofi/zenity
│ (10 options)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Claude API     │ Anthropic Python SDK
│  (Sonnet 4)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Clipboard     │ xclip -selection clipboard
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Notification   │ notify-send
└─────────────────┘
```

## Configuration

### Changing the Model

Edit `text_converter.py` and modify the `MODEL` constant:

```python
MODEL = "claude-sonnet-4-20250514"  # Latest Sonnet
# or
MODEL = "claude-3-5-sonnet-20241022"  # Older Sonnet
```

### Adding Custom Modes

Edit the `CONVERSION_MODES` dictionary in `text_converter.py`:

```python
"11": {
    "name": "Your Custom Mode",
    "prompt": """Your conversion instructions here.

Text: {text}

Converted text:"""
}
```

### Keyboard Shortcut Alternatives

Common alternatives to `Ctrl+Alt+T`:
- `Super+T` (Windows/Command key + T)
- `Ctrl+Shift+T`
- `Alt+T`
- Any F-key (F9, F10, etc.)

## Troubleshooting

### "No text selected" notification
- Ensure text is highlighted before pressing shortcut
- Try selecting with mouse, not keyboard
- Some apps may not expose selection to X11 - try copying to clipboard first

### "ANTHROPIC_API_KEY not set"
- Check environment variable: `echo $ANTHROPIC_API_KEY`
- Restart terminal after editing `~/.bashrc`
- For current session: `export ANTHROPIC_API_KEY='your-key'`
- Verify in your shell config file

### rofi/zenity not found
- Install rofi (recommended): `sudo apt install rofi`
- Or install zenity as fallback: `sudo apt install zenity`
- Check installation: `which rofi`

### Conversion fails or hangs
- Check internet connection
- Verify API key is valid at [Anthropic Console](https://console.anthropic.com/)
- Check Anthropic API status: [status.anthropic.com](https://status.anthropic.com/)
- Look for error in notification

### Permission denied
- Ensure script is executable: `chmod +x /usr/local/bin/text-converter.py`
- Re-run installer: `./install.sh`

### Doesn't work in specific application
- Some apps (like secure terminals) may block clipboard access
- Try copying text first, then select from clipboard manager
- Wayland apps may have limitations - try X11 session

## Cost Estimates

Using Claude Sonnet 4 pricing (as of 2024):

| Text Length | Approx. Tokens | Estimated Cost |
|-------------|----------------|----------------|
| Short (100 words) | ~150 tokens | ~$0.001 |
| Medium (500 words) | ~750 tokens | ~$0.005 |
| Long (2000 words) | ~3000 tokens | ~$0.02 |

**Note:** Costs are estimates. Check [Anthropic pricing](https://www.anthropic.com/api) for current rates.

## Comparison to Prompt Enhancer

This tool is inspired by [Prompt Enhancer Extension](https://github.com/thamam/prompt-enhancer-extension) but designed for broader use:

| Feature | Prompt Enhancer | Text Style Converter |
|---------|----------------|---------------------|
| Platform | Browser extension | Linux desktop (system-wide) |
| Use case | Enhance AI prompts | Convert any text style |
| Modes | Prompt-specific | 10 diverse styles |
| Integration | Browser only | All applications |
| Activation | Extension button | Keyboard shortcut |

## Future Plans

- [ ] Browser extension version (Chrome/Firefox)
- [ ] Windows/macOS support
- [ ] Multi-language support (Spanish, French, etc.)
- [ ] Custom conversion mode templates
- [ ] Local model option (no API required)
- [ ] Batch file processing
- [ ] History and favorites
- [ ] GUI configuration tool
- [ ] Wayland native support

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

- Inspired by [Prompt Enhancer Extension](https://github.com/thamam/prompt-enhancer-extension)
- Powered by [Anthropic Claude API](https://www.anthropic.com/)
- Uses [rofi](https://github.com/davatorium/rofi) for menu display

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/thamam/Writing-Companion/issues)
- Check existing issues for solutions
- Include error messages and system info in bug reports

## Changelog

### v1.0.0 (2024-11-11)
- Initial release
- 10 conversion modes
- Linux desktop integration
- Claude Sonnet 4 support
- Rofi/Zenity UI
- Comprehensive documentation
