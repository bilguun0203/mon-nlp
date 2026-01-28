"""Tests for punctuation module."""

from mon_nlp import punctuation


def test_normalize():
    assert punctuation.normalize("\u201cСайн\u201d") == '"Сайн"'
    assert punctuation.normalize("\u2018тест\u2019") == "'тест'"
    assert punctuation.normalize("текст\u2026") == "текст..."
    assert punctuation.normalize("а\u2013б\u2014в") == "а-б-в"


def test_to_words():
    assert punctuation.to_words("Сайн.") == "Сайн цэг"
    assert punctuation.to_words("Сайн, байна") == "Сайн таслал байна"
    assert punctuation.to_words("Юу?") == "Юу асуултын тэмдэг"


def test_remove():
    assert punctuation.remove("Сайн, байна уу?") == "Сайн байна уу"
    assert punctuation.remove("Тест!") == "Тест"
    assert punctuation.remove("а.б.в") == "а б в"


def test_empty_string():
    assert punctuation.normalize("") == ""
    assert punctuation.to_words("") == ""
    assert punctuation.remove("") == ""
