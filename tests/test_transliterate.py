"""Tests for transliterate module (skipped if phonemizer not installed)."""

from importlib.util import find_spec

import pytest

HAS_PHONEMIZER = find_spec("phonemizer") is not None


def test_ipa_to_cyrillic():
    from mon_nlp.transliterate import ipa_to_cyrillic

    # Basic test without stress marks
    assert ipa_to_cyrillic("həloʊ wɜːld") == "хэлоүү виоурлд"


@pytest.mark.skipif(not HAS_PHONEMIZER, reason="Requires phonemizer with espeak backend")
def test_transliterate():
    from mon_nlp.transliterate import transliterate

    assert transliterate("hello") == "хэлоүү"

    # Test a pangram sentence
    input_text = (
        "The beige hue on the waters of the loch impressed all, "
        "including the French queen, before she heard that symphony again, "
        "just as young Arthur wanted."
    )
    expected = (
        "дэ бэйж хюу ондэ воотэрс авдэ лаах импрэйст оол, "
        "ингклуудинг дэ фрэйнч квийн, бифоор ший хиоурд дэайт симфэни айгэйн, "
        "жаст эайс ианг аартэр вонтид."
    )
    assert transliterate(input_text) == expected


@pytest.mark.skipif(not HAS_PHONEMIZER, reason="Requires phonemizer with espeak backend")
def test_transliterate_output_ipa():
    from mon_nlp.transliterate import transliterate

    assert transliterate("hello", output_ipa=True) == "həloʊ"
    assert transliterate("hello", output_ipa=False) == "хэлоүү"
    assert transliterate("on the", output_ipa=True) == "ɔnðə"
    assert transliterate("I am John", output_ipa=True) == "aɪɐm dʒɑːn"
