# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

- Setup (first time):
  - python -m venv .venv
  - source .venv/bin/activate
  - pip install -r requirements.txt
- Configure env:
  - cp .env.example .env
  - Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in .env
- Run the bot once (sends one random word):
  - python -m jpbot.send_word
- Schedule daily run (example, 09:00 every day):
  - crontab -e
  - 0 9 * * * cd "$HOME/projects/telegram-japanese-word-bot" && . .venv/bin/activate && python -m jpbot.send_word >> logs.txt 2>&1
- Linting/Testing:
  - Not configured in this repo. No test framework or linter config is present.

## Architecture and structure (high-level)

- Language/runtime: Python 3.10+
- Layout: src-based package at src/jpbot
- Data source: src/jpbot/words.json (array of entries). Each entry maps to the Word dataclass with fields: kanji, kana, romaji, meaning, en, ru.
- Core flow (jpbot/send_word.py):
  - load_dotenv() loads .env (python-dotenv)
  - Reads TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID from env
  - Loads all words from words.json, picks one at random
  - Formats a multiline message (Japanese headers + EN/RU)
  - Uses python-telegram-bot’s Bot to send a single message to the target chat
  - Runs as a one-shot async program (asyncio.run(main())) suitable for schedulers (cron). There is no long-running update handler/dispatcher.
- Dependencies: requirements.txt (python-telegram-bot, python-dotenv). No packaging, Dockerfiles, CI, or editor/AI rules files are present in the repo.

## Notes from README (essentials)

- Ensure the bot is allowed to post in the target chat. For groups/channels, add the bot and obtain the numeric chat ID.
