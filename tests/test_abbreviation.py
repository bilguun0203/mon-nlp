"""Tests for abbreviation module."""

from mon_nlp import abbreviation
from mon_nlp.abbreviation import AbbreviationExpander


def test_expand_default():
    assert abbreviation.expand("МУ байна") == "Монгол Улс байна"
    assert abbreviation.expand("УБ хот") == "Улаанбаатар хот"


def test_expand_multiple():
    result = abbreviation.expand("МУ-ын нийслэл УБ хот")
    assert "Монгол Улс" in result
    assert "Улаанбаатар" in result


def test_custom_expander():
    expander = AbbreviationExpander({"ХБХ": "хэл боловсруулах хэрэгсэл"})
    assert expander.expand("ХБХ хэрэглэх") == "хэл боловсруулах хэрэгсэл хэрэглэх"
    assert expander.expand("МУ") == "Монгол Улс"


def test_add_remove():
    expander = AbbreviationExpander()
    expander.add("ТТ", "тест текст")
    assert expander.expand("ТТ") == "тест текст"
    expander.remove("ТТ")
    assert expander.expand("ТТ") == "ТТ"


def test_get_all():
    expander = AbbreviationExpander()
    abbrevs = expander.get_all()
    assert "МУ" in abbrevs
    assert abbrevs["МУ"] == "Монгол Улс"
