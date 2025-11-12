#!/usr/bin/env python3
"""
Text Style Converter - Linux Desktop Tool
Converts selected text into different styles using Claude API
"""

import os
import sys
import subprocess
import json
from anthropic import Anthropic

# Configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
MODEL = "claude-sonnet-4-20250514"

# Style conversion prompts
CONVERSION_MODES = {
    "1": {
        "name": "More Formal",
        "prompt": """Convert the following text to a more formal style suitable for professional or academic contexts.
Maintain the core message but elevate the language, use proper grammar, avoid contractions, and adopt a professional tone.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "2": {
        "name": "More Stylish",
        "prompt": """Convert the following text to a more stylish, engaging format with better flow and rhetorical flair.
Use varied sentence structures, vivid language, and compelling phrasing while maintaining the original meaning.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "3": {
        "name": "WhatsApp Appropriate",
        "prompt": """Convert the following text to be appropriate for WhatsApp messaging.
Use casual, friendly tone, shorter sentences, common abbreviations where natural, and conversational style.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "4": {
        "name": "LinkedIn Post Material",
        "prompt": """Convert the following text into LinkedIn post material.
Use professional yet engaging tone, include relevant insights, format for readability with line breaks, and add a call-to-action or thought-provoking question if appropriate.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "5": {
        "name": "Discord Material",
        "prompt": """Convert the following text to be appropriate for Discord messaging.
Use casual, community-friendly tone, internet-aware language, and format suitable for Discord's chat environment.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "6": {
        "name": "Casual Format",
        "prompt": """Convert the following text to a casual, friendly format.
Use relaxed language, contractions, simple words, and conversational tone as if speaking to a friend.

Text: {text}

Converted text (output only the converted text, no explanations):"""
    },
    "7": {
        "name": "Natural - Fix Typos & Grammar",
        "prompt": """Fix all typos and grammar errors in the following text while maintaining the original style and tone.
Make minimal changes - only fix errors, don't rephrase or restructure.

Text: {text}

Corrected text (output only the corrected text, no explanations):"""
    },
    "8": {
        "name": "Typos Only",
        "prompt": """Fix ONLY the typos in the following text. Do not change grammar, punctuation, or structure.
Only correct misspelled words.

Text: {text}

Corrected text (output only the corrected text, no explanations):"""
    },
    "9": {
        "name": "Grammar Only",
        "prompt": """Fix ONLY the grammar in the following text. Do not change typos (unless they affect grammar), style, or tone.
Correct grammatical errors, sentence structure, and punctuation.

Text: {text}

Corrected text (output only the corrected text, no explanations):"""
    },
    "10": {
        "name": "Add Emojis",
        "prompt": """Add appropriate emojis to the following text to enhance expressiveness and engagement.
Place emojis naturally - at the end of sentences, to emphasize points, or to add emotional context. Don't overdo it - 3-5 emojis for typical text.

Text: {text}

Text with emojis (output only the text with emojis, no explanations):"""
    }
}


def get_selected_text():
    """Get currently selected text using xclip"""
    try:
        result = subprocess.run(
            ['xclip', '-o', '-selection', 'primary'],
            capture_output=True,
            text=True,
            timeout=2
        )
        return result.stdout.strip()
    except Exception as e:
        return None


def set_clipboard(text):
    """Set text to clipboard using xclip"""
    try:
        process = subprocess.Popen(
            ['xclip', '-selection', 'clipboard'],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=text)
        return True
    except Exception as e:
        return False


def show_mode_selector():
    """Show mode selection using rofi"""
    modes_list = [f"{k}. {v['name']}" for k, v in CONVERSION_MODES.items()]
    modes_text = '\n'.join(modes_list)

    try:
        result = subprocess.run(
            ['rofi', '-dmenu', '-i', '-p', 'Select conversion mode:', '-format', 's'],
            input=modes_text,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            return None

        selected = result.stdout.strip()
        # Extract mode number (first character)
        mode_num = selected.split('.')[0].strip()
        return mode_num
    except FileNotFoundError:
        # Fallback to zenity if rofi not available
        try:
            modes_formatted = '|'.join([f"{k}. {v['name']}" for k, v in CONVERSION_MODES.items()])
            result = subprocess.run(
                ['zenity', '--list', '--title=Text Converter',
                 '--text=Select conversion mode:', '--column=Mode'] +
                [f"{k}. {v['name']}" for k, v in CONVERSION_MODES.items()],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0:
                return None

            selected = result.stdout.strip()
            mode_num = selected.split('.')[0].strip()
            return mode_num
        except Exception as e:
            show_notification(f"Error: {e}\nInstall rofi or zenity", "error")
            return None


def convert_text(text, mode):
    """Convert text using Claude API"""
    if not ANTHROPIC_API_KEY:
        return None, "Error: ANTHROPIC_API_KEY not set"

    if mode not in CONVERSION_MODES:
        return None, f"Error: Invalid mode {mode}"

    try:
        client = Anthropic(api_key=ANTHROPIC_API_KEY)

        prompt = CONVERSION_MODES[mode]["prompt"].format(text=text)

        message = client.messages.create(
            model=MODEL,
            max_tokens=2000,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        converted_text = message.content[0].text.strip()
        return converted_text, None

    except Exception as e:
        return None, f"Error: {str(e)}"


def show_notification(message, urgency="normal"):
    """Show desktop notification"""
    try:
        subprocess.run(
            ['notify-send', '-u', urgency, 'Text Converter', message],
            timeout=2
        )
    except Exception:
        pass


def main():
    # Check for API key
    if not ANTHROPIC_API_KEY:
        show_notification(
            "ANTHROPIC_API_KEY environment variable not set!\n"
            "Set it in ~/.bashrc or ~/.zshrc:\n"
            "export ANTHROPIC_API_KEY='your-key-here'",
            "critical"
        )
        sys.exit(1)

    # Get selected text
    selected_text = get_selected_text()

    if not selected_text:
        show_notification("No text selected", "normal")
        sys.exit(1)

    # Show mode selector
    mode = show_mode_selector()

    if not mode:
        # User cancelled
        sys.exit(0)

    # Show processing notification
    show_notification(f"Converting to: {CONVERSION_MODES[mode]['name']}...", "normal")

    # Convert text
    converted, error = convert_text(selected_text, mode)

    if error:
        show_notification(error, "critical")
        sys.exit(1)

    # Copy to clipboard
    if set_clipboard(converted):
        show_notification(
            f"Converted text copied to clipboard!\n"
            f"Mode: {CONVERSION_MODES[mode]['name']}",
            "normal"
        )
    else:
        show_notification("Error copying to clipboard", "critical")
        sys.exit(1)


if __name__ == "__main__":
    main()
