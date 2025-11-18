# Telegram Japanese Word Bot

A Telegram bot that sends a daily Japanese word with English and Russian translations, meaning, and readings.

## Features
- Sends a random word with: kanji, kana, romaji, meaning, EN and RU translations.
- Simple script you can schedule via cron or any scheduler.

## Requirements
- Python 3.10+
- A Telegram Bot Token (from @BotFather)
- A target chat ID (your user ID, group ID, or channel ID)

## Setup
1. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure environment variables. Copy `.env.example` to `.env` and fill in values:

   ```bash
   cp .env.example .env
   ```

   Required vars:
   - `TELEGRAM_BOT_TOKEN`: Bot token from BotFather
   - `TELEGRAM_CHAT_ID`: Chat ID to send the daily message to

## Usage
- Send one word now:

  ```bash
  python -m jpbot.send_word
  ```

- Schedule daily (example: every day at 9:00):

  ```bash
  # crontab -e
  0 9 * * * cd "$HOME/projects/telegram-japanese-word-bot" && . .venv/bin/activate && python -m jpbot.send_word >> logs.txt 2>&1
  ```

## Data
Word entries are stored in `src/jpbot/words.json`. You can add more words following the existing schema.

## Notes
- Ensure the bot has permission to write in the target chat.
- For groups/channels, you may need to add the bot and/or collect the chat ID using a helper bot or a temporary handler.
