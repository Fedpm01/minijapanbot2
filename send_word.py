import asyncio
import json
import os
import random
import hashlib
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv
from telegram import Bot


@dataclass
class Word:
    kanji: str
    kana: str
    romaji: str
    meaning: str
    en: str
    ru: str


def load_words() -> list[Word]:
    here = Path(__file__).parent
    data_path = here / "words.json"
    with data_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return [Word(**entry) for entry in data]


def format_message(w: Word) -> str:
    # Multiline message with clear structure
    # Includes Japanese headers and English for clarity
    return (
        "今日の言葉 — Word of the Day\n\n"
        f"単語: {w.kanji} ({w.kana} / {w.romaji})\n"
        f"意味: {w.meaning}\n"
        f"EN: {w.en}\n"
        f"RU: {w.ru}"
    )


def word_id(w: Word) -> str:
    # Stable hash over canonicalized fields to identify entries regardless of index/order
    payload = json.dumps(asdict(w), ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_history(root_dir: Path) -> dict:
    path = root_dir / ".jpbot_history.json"
    if not path.exists():
        return {"recent": []}
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"recent": []}


def save_history(root_dir: Path, history: dict) -> None:
    path = root_dir / ".jpbot_history.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


async def main() -> None:
    load_dotenv()  # load .env if present

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        raise SystemExit("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID env vars.")

    here = Path(__file__).parent
    # project root: .../project (parents[1] of src/jpbot)
    project_root = here.parents[1]

    words = load_words()
    ids = [word_id(w) for w in words]

    # Load history and compute recent window
    history = load_history(project_root)
    recent = list(history.get("recent", []))
    try:
        recent_window = int(os.getenv("JP_WORD_RECENT_WINDOW", "60"))
    except ValueError:
        recent_window = 60
    if recent_window < 0:
        recent_window = 0

    # Build eligible pool (avoid near-duplicates)
    eligible_indices = [i for i, _id in enumerate(ids) if _id not in set(recent)]
    if not eligible_indices:
        # If window exhausted, reset recent and re-eligible all
        eligible_indices = list(range(len(words)))
        recent = []

    idx = random.choice(eligible_indices)
    choice = words[idx]

    # Update history (append and trim)
    chosen_id = ids[idx]
    recent.append(chosen_id)
    if recent_window > 0 and len(recent) > recent_window:
        recent = recent[-recent_window:]
    history["recent"] = recent
    save_history(project_root, history)

    message = format_message(choice)

    bot = Bot(token=token)
    await bot.send_message(chat_id=chat_id, text=message, disable_web_page_preview=True)


if __name__ == "__main__":
    asyncio.run(main())
