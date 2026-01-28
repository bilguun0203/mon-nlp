"""Abbreviation expansion for Mongolian text."""

import json
import re
from pathlib import Path

_DATA_DIR = Path(__file__).parent / "data"


class AbbreviationExpander:
    """Expands abbreviations in Mongolian text."""

    def __init__(self, custom: dict[str, str] | None = None):
        self._abbrevs = self._load_defaults()
        if custom:
            self._abbrevs.update(custom)

    def _load_defaults(self) -> dict[str, str]:
        with open(_DATA_DIR / "abbreviations.json", encoding="utf-8") as f:
            return json.load(f)

    def expand(self, text: str) -> str:
        """Expand abbreviations in text."""
        for abbrev, expansion in sorted(self._abbrevs.items(), key=lambda x: -len(x[0])):
            pattern = rf"\b{re.escape(abbrev)}\b"
            text = re.sub(pattern, expansion, text)
        return text

    def add(self, abbrev: str, expansion: str) -> None:
        """Add a new abbreviation mapping."""
        self._abbrevs[abbrev] = expansion

    def remove(self, abbrev: str) -> None:
        """Remove an abbreviation mapping."""
        self._abbrevs.pop(abbrev, None)

    def get_all(self) -> dict[str, str]:
        """Get all abbreviation mappings."""
        return self._abbrevs.copy()


_default_expander: AbbreviationExpander | None = None


def _get_default_expander() -> AbbreviationExpander:
    global _default_expander
    if _default_expander is None:
        _default_expander = AbbreviationExpander()
    return _default_expander


def expand(text: str) -> str:
    """Expand abbreviations using default mappings."""
    return _get_default_expander().expand(text)
