"""Tests for g2p module."""

from mon_nlp import g2p
from mon_nlp.g2p import G2P


def test_syllabify():
    assert g2p.syllabify("сайн") == ["сайн"]
    assert g2p.syllabify("байна") == ["бай", "на"]
    assert g2p.syllabify("байна уу") == ["бай", "на", "уу"]
    assert g2p.syllabify("монгол") == ["мон", "гол"]


def test_convert():
    assert g2p.convert("сайн") == "s-ay1-ng|"
    assert g2p.convert("байна") == "b-ay1|n-a0|"
    assert g2p.convert("биологи") == "B-O:1|l-o0|C-i0|"
    assert (
        g2p.convert("магадгүй тэртээ олон зуун жилийн өмнө")
        == "m-a1|G-a0-d|g-^y0|*t-e1-r|t-e:0|*o1|l-o0-ng|*z-u:1-ng|*w-i1|l-i:0-ng|*@1-m|n-@0|"
    )


def test_convert_multiple_words():
    assert g2p.convert("сайн байна уу") == "s-ay1-ng|*b-ay1|n-a0|*u:1|"


def test_g2p_class():
    converter = G2P()
    assert converter.convert("монгол") == "m-o1-ng|G-o0-l|"


def test_empty():
    assert g2p.convert("") == ""
    assert g2p.syllabify("") == [""]
