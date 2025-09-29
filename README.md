# Translate Bot

A translation bot built with LXMFy and Argos Translate that provides offline translation capabilities through the Reticulum Network.

## Features

- Offline translation using Argos Translate
- Support for multiple languages

## Requirements

- sentencepiece

## Installation

```bash
pipx install git+https://github.com/LXMFy/translate-bot.git
```

## Usage

1. Start the bot:
```bash
lxmfy-translate-bot
```

2. Pre-download models (optional, speeds up first translations):
```bash
# Download all available models (skips already installed)
lxmfy-translate-bot --download-all

# Download specific language pairs (skips already installed)
lxmfy-translate-bot --download en-es fr-de it-en
```
Note: Download commands automatically detect and skip already installed models.

3. Enable message signing and verification (optional):
```bash
# Enable optional signature verification (recommended)
lxmfy-translate-bot --enable-signatures

# Require signatures for all messages (strict mode)
lxmfy-translate-bot --require-signatures
```

4. Available commands:
- `translate <source_lang> <target_lang> <text>` - Translate text between languages
  Example: `translate en es Hello world`
- `languages` - List all available languages for translation
- `stats` - Show bot statistics and performance metrics
- `help` - Show detailed help and usage information

## Language Codes

The bot uses standard language codes (e.g., 'en' for English, 'es' for Spanish). Use the `languages` command to see all available language codes.

## Message Signing & Verification

The bot supports cryptographic message signing and verification for enhanced security:

- **Signature Verification**: Verify that incoming messages are cryptographically signed using RNS identities
- **Optional vs Required**: Choose whether to allow unsigned messages or require signatures for all messages
- **Command-line flags**:
  - `--enable-signatures`: Enable optional signature verification (recommended)
  - `--require-signatures`: Require signatures for all messages (strict mode)

When signature verification is enabled, the bot will automatically sign outgoing messages and verify incoming message signatures when present. Unsigned messages are rejected only in strict mode.

## License

MIT License