"""Emoji to Mongolian words conversion."""

import json
import re
from pathlib import Path
from typing import Literal

_DATA_DIR = Path(__file__).parent / "data"
_EMOJI_DATA: dict[str, str] | None = None

FormatType = Literal["plain", "brackets", "parentheses"]


def _load_data() -> dict[str, str]:
    global _EMOJI_DATA
    if _EMOJI_DATA is None:
        with open(_DATA_DIR / "emojis.json", encoding="utf-8") as f:
            _EMOJI_DATA = json.load(f)
    assert _EMOJI_DATA is not None
    return _EMOJI_DATA


def _format_word(word: str, fmt: FormatType) -> str:
    if fmt == "brackets":
        return f"[{word}]"
    elif fmt == "parentheses":
        return f"({word})"
    return word


def emoji_to_words(text: str, format: FormatType = "plain") -> str:
    """Replace emojis with Mongolian descriptions.

    Args:
        text: Input text containing emojis
        format: Output format - "plain", "brackets", or "parentheses"

    Returns:
        Text with emojis replaced by Mongolian words
    """
    data = _load_data()
    for emoji, word in data.items():
        replacement = _format_word(word, format)
        text = text.replace(emoji, f" {replacement} ")
    # Clean up multiple spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text


def remove_emoji(text: str) -> str:
    """Remove all emojis from text."""
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"
        "\U0001f300-\U0001f5ff"
        "\U0001f680-\U0001f6ff"
        "\U0001f1e0-\U0001f1ff"
        "\U00002702-\U000027b0"
        "\U0001f900-\U0001f9ff"
        "\U0001fa00-\U0001fa6f"
        "\U0001fa70-\U0001faff"
        "\U00002600-\U000026ff"
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def add_emoji_mapping(emoji: str, description: str) -> None:
    """Add a custom emoji mapping."""
    data = _load_data()
    data[emoji] = description


def remove_emoji_mapping(emoji: str) -> None:
    """Remove an emoji mapping."""
    data = _load_data()
    data.pop(emoji, None)


def get_emoji_mappings() -> dict[str, str]:
    """Get all emoji mappings."""
    return _load_data().copy()
