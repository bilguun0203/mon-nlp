"""Mongolian Cyrillic text normalization and processing library."""

from mon_nlp.abbreviation import AbbreviationExpander
from mon_nlp.abbreviation import expand as expand_abbreviations
from mon_nlp.case import to_lowercase, to_sentence_case, to_uppercase
from mon_nlp.emoji import (
    add_emoji_mapping,
    emoji_to_words,
    get_emoji_mappings,
    remove_emoji,
    remove_emoji_mapping,
)
from mon_nlp.g2p import G2P, syllabify
from mon_nlp.g2p import convert as g2p_convert
from mon_nlp.number import num2words, roman2num
from mon_nlp.punctuation import normalize as normalize_punctuation
from mon_nlp.punctuation import remove as remove_punctuation
from mon_nlp.punctuation import to_words as punctuation_to_words

__version__ = "0.1.0"

__all__ = [
    # Case
    "to_uppercase",
    "to_lowercase",
    "to_sentence_case",
    # Punctuation
    "normalize_punctuation",
    "punctuation_to_words",
    "remove_punctuation",
    # Abbreviation
    "AbbreviationExpander",
    "expand_abbreviations",
    # Number
    "num2words",
    "roman2num",
    # Emoji
    "emoji_to_words",
    "remove_emoji",
    "add_emoji_mapping",
    "remove_emoji_mapping",
    "get_emoji_mappings",
    # G2P
    "G2P",
    "g2p_convert",
    "syllabify",
]


def transliterate(text: str, language: str = "en-us", output_ipa: bool = False) -> str:
    """Transliterate English text to Mongolian Cyrillic.

    Requires optional dependency: pip install mon-nlp[transliterate]

    Args:
        text: English text to transliterate
        language: Source language code (default: "en-us")
        output_ipa: If True, return IPA instead of Cyrillic

    Returns:
        Mongolian Cyrillic transliteration, or IPA if output_ipa=True
    """
    from mon_nlp.transliterate import transliterate as _transliterate

    return _transliterate(text, language, output_ipa)
