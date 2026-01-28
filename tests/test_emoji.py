"""Tests for emoji module."""

from mon_nlp import emoji


def test_emoji_to_words_plain():
    result = emoji.emoji_to_words("Сайн 😀")
    assert "инээмсэглэсэн царай" in result
    assert "😀" not in result


def test_emoji_to_words_brackets():
    result = emoji.emoji_to_words("Сайн 😀", format="brackets")
    assert "[инээмсэглэсэн царай]" in result


def test_emoji_to_words_parentheses():
    result = emoji.emoji_to_words("Сайн 😀", format="parentheses")
    assert "(инээмсэглэсэн царай)" in result


def test_multiple_emojis():
    result = emoji.emoji_to_words("😀😄")
    assert result == "инээмсэглэсэн царай мишээсэн нүдтэй инээж буй царай"


def test_multiple_emojis_brackets():
    result = emoji.emoji_to_words("😀😄", format="brackets")
    assert result == "[инээмсэглэсэн царай] [мишээсэн нүдтэй инээж буй царай]"


def test_remove_emoji():
    assert emoji.remove_emoji("Сайн 😀 байна") == "Сайн  байна"


def test_add_remove_mapping():
    emoji.add_emoji_mapping("🆕", "шинэ")
    assert emoji.emoji_to_words("🆕") == "шинэ"
    emoji.remove_emoji_mapping("🆕")
    assert emoji.emoji_to_words("🆕") == "🆕"


def test_get_mappings():
    mappings = emoji.get_emoji_mappings()
    assert "😀" in mappings
    assert mappings["😀"] == "инээмсэглэсэн царай"


def test_no_emoji():
    assert emoji.emoji_to_words("Сайн байна") == "Сайн байна"
