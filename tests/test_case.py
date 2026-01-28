"""Tests for case module."""

from mon_nlp import case


def test_to_uppercase():
    assert case.to_uppercase("сайн байна уу") == "САЙН БАЙНА УУ"
    assert case.to_uppercase("өглөөний мэнд") == "ӨГЛӨӨНИЙ МЭНД"


def test_to_lowercase():
    assert case.to_lowercase("САЙН БАЙНА УУ") == "сайн байна уу"
    assert case.to_lowercase("ӨГЛӨӨ МЭНД") == "өглөө мэнд"


def test_to_sentence_case():
    assert case.to_sentence_case("САЙН БАЙНА УУ") == "Сайн байна уу"
    assert case.to_sentence_case("сайн. байна") == "Сайн. Байна"
    assert case.to_sentence_case("юу? тийм үү!") == "Юу? Тийм үү!"


def test_empty_string():
    assert case.to_uppercase("") == ""
    assert case.to_lowercase("") == ""
    assert case.to_sentence_case("") == ""


def test_mixed_case():
    assert case.to_uppercase("СаЙн БаЙнА") == "САЙН БАЙНА"
    assert case.to_lowercase("СаЙн БаЙнА") == "сайн байна"
