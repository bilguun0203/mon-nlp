"""Tests for number module."""

from mon_nlp import number


def test_single_digits():
    assert number.num2words(0) == "тэг"
    assert number.num2words(1) == "нэг"
    assert number.num2words(5) == "тав"
    assert number.num2words(9) == "ес"


def test_tens():
    assert number.num2words(10) == "арав"
    assert number.num2words(20) == "хорь"
    assert number.num2words(11) == "арван нэг"
    assert number.num2words(25) == "хорин тав"
    assert number.num2words(99) == "ерэн ес"


def test_hundreds():
    assert number.num2words(100) == "нэг зуу"
    assert number.num2words(123) == "нэг зуун хорин гурав"
    assert number.num2words(500) == "таван зуу"


def test_thousands():
    assert number.num2words(1000) == "нэг мянга"
    assert number.num2words(1234) == "нэг мянга хоёр зуун гучин дөрөв"


def test_millions():
    assert number.num2words(1_000_000) == "нэг сая"


def test_negative():
    assert number.num2words(-5) == "хасах тав"
    assert number.num2words(-42) == "хасах дөчин хоёр"


def test_float():
    assert number.num2words(3.14) == "гурав зууны арван дөрөв"
    assert number.num2words(123.5678901) == (
        "нэг зуун хорин гурав арван саяны таван сая зургаан зуун далан найман мянга есөн зуун нэг"
    )
    assert number.num2words(-0.001) == "хасах тэг мянганы нэг"
    assert number.num2words(-0.000001) == "хасах тэг саяны нэг"


def test_float_with_dot():
    result = number.num2words(3.14, use_dot=True)
    assert result == "гурав цэг арван дөрөв"


def test_by_digits():
    test_cases = [
        (8, "найм"),
        (12, "арван хоёр"),
        (345, "гурав, дөчин тав"),
        (6789, "жаран долоо, наян ес"),
    ]
    for number_input, expected_output in test_cases:
        assert number.num2words(number_input, by_n_digits=2) == expected_output


def test_by_3_digits():
    test_cases = [
        (7, "долоо"),
        (89, "наян ес"),
        (456, "дөрвөн зуун тавин зургаа"),
        (1234, "нэг, хоёр зуун гучин дөрөв"),
        (567890, "таван зуун жаран долоо, найман зуун ер"),
        (1000000, "нэг, тэг, тэг, тэг, тэг, тэг, тэг"),
    ]
    for number_input, expected_output in test_cases:
        assert number.num2words(number_input, by_n_digits=3) == expected_output


def test_roman2num():
    assert number.roman2num("I") == 1
    assert number.roman2num("IV") == 4
    assert number.roman2num("XIV") == 14
    assert number.roman2num("MCMXCIV") == 1994


def test_include_leading_one():
    test_cases = [
        (10, "арав"),
        (100, "зуу"),
        (1000, "мянга"),
        (100000, "зуун мянга"),
        (1000000, "сая"),
    ]
    for number_input, expected_output in test_cases:
        assert number.num2words(number_input, include_leading_one=False) == expected_output


def test_extra_large_number():
    test_cases = [
        (1_000_000_000_000, "нэг их наяд"),
        (
            2_345_678_901_234,
            "хоёр их наяд гурван зуун дөчин таван тэрбум "
            "зургаан зуун далан найман сая есөн зуун нэгэн мянга хоёр зуун гучин дөрөв",
        ),
        (1_000_000_000_000_000, "нэг, " + ", ".join(["тэг"] * 15)),
    ]
    for number_input, expected_output in test_cases:
        assert number.num2words(number_input) == expected_output
