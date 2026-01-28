"""Punctuation normalization for Mongolian text."""

import json
import re
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"
_PUNCT_DATA: dict | None = None


def _load_data() -> dict:
    global _PUNCT_DATA
    if _PUNCT_DATA is None:
        with open(_DATA_DIR / "punctuations.json", encoding="utf-8") as f:
            _PUNCT_DATA = json.load(f)
    assert _PUNCT_DATA is not None
    return _PUNCT_DATA


def normalize(text: str) -> str:
    """Replace uncommon punctuation marks with ASCII equivalents."""
    data = _load_data()
    for old, new in data["normalize"].items():
        text = text.replace(old, new)
    return text


def to_words(text: str) -> str:
    """Replace punctuation marks with their Mongolian word equivalents."""
    data = _load_data()
    for punct, word in data["to_words"].items():
        text = text.replace(punct, f" {word} ")
    return re.sub(r"\s+", " ", text).strip()


def remove(text: str) -> str:
    """Remove all punctuation marks from text."""
    data = _load_data()
    all_puncts = set(data["normalize"].keys()) | set(data["to_words"].keys())
    for punct in all_puncts:
        text = text.replace(punct, " ")
    return re.sub(r"\s+", " ", text).strip()
