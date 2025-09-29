# Translate Bot

A translation bot built with LXMFy and Argos Translate that provides offline translation capabilities through the Reticulum Network.

## Features

- Offline translation using Argos Translate
- Support for multiple languages

## Requirements

- sentencepiece

## Installation

```bash
# Install from PyPI
pip install lxmfy-translate-bot
```

## Usage

1. Start the bot:
```bash
lxmfy-translate-bot
```

2. Pre-download models (optional, speeds up first translations):
```bash
# Download all available models
lxmfy-translate-bot --download-all

# Download specific language pairs
lxmfy-translate-bot --download en-es fr-de it-en
```

3. Available commands:
- `translate <source_lang> <target_lang> <text>` - Translate text between languages
  Example: `translate en es Hello world`
- `languages` - List all available languages for translation
- `stats` - Show bot statistics and performance metrics
- `help` - Show detailed help and usage information

## Language Codes

The bot uses standard language codes (e.g., 'en' for English, 'es' for Spanish). Use the `languages` command to see all available language codes.

## License

MIT License