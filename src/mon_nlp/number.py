"""Number to Mongolian words conversion."""

NUMBER_NAMES = {
    0: ("тэг", "тэг"),
    1: ("нэг", "нэгэн"),
    2: ("хоёр", "хоёр"),
    3: ("гурав", "гурван"),
    4: ("дөрөв", "дөрвөн"),
    5: ("тав", "таван"),
    6: ("зургаа", "зургаан"),
    7: ("долоо", "долоон"),
    8: ("найм", "найман"),
    9: ("ес", "есөн"),
    10: ("арав", "арван"),
    20: ("хорь", "хорин"),
    30: ("гуч", "гучин"),
    40: ("дөч", "дөчин"),
    50: ("тавь", "тавин"),
    60: ("жар", "жаран"),
    70: ("дал", "далан"),
    80: ("ная", "наян"),
    90: ("ер", "ерэн"),
    100: ("зуу", "зуун"),
    1000: ("мянга", "мянга"),
    1_000_000: ("сая", "сая"),
    1_000_000_000: ("тэрбум", "тэрбум"),
    1_000_000_000_000: ("их наяд", "их наяд"),
}

FRACTION_NAMES = {
    10: "аравны",
    100: "зууны",
    1000: "мянганы",
    10_000: "арван мянганы",
    100_000: "зуун мянганы",
    1_000_000: "саяны",
    10_000_000: "арван саяны",
    100_000_000: "зуун саяны",
    1_000_000_000: "тэрбумны",
    10_000_000_000: "арван тэрбумны",
    100_000_000_000: "зуун тэрбумны",
    1_000_000_000_000: "их наядны",
}

ROMAN_NUMERALS = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman2num(roman: str) -> int:
    """Convert Roman numeral to integer."""
    if not roman:
        return 0

    roman = roman.upper()
    total = 0
    prev_value = 0

    for char in reversed(roman):
        if char not in ROMAN_NUMERALS:
            raise ValueError(f"Invalid Roman numeral character: {char}")
        current_value = ROMAN_NUMERALS[char]
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value
        prev_value = current_value

    return total


def _num2words_3digits(number: int, cont: bool = False, include_leading_one: bool = True) -> str:
    """Convert 3-digit number (0-999) to Mongolian words."""
    if number == 0:
        return NUMBER_NAMES[0][0]

    unit = number % 10
    ten = (number // 10) % 10
    hundred = (number // 100) % 10

    parts = []
    if unit:
        parts.append(NUMBER_NAMES[unit][1 if cont else 0])
    if ten:
        parts.append(NUMBER_NAMES[ten * 10][1 if parts else (1 if cont else 0)])
    if hundred:
        parts.append(NUMBER_NAMES[100][1 if parts else (1 if cont else 0)])
        if hundred == 1 and include_leading_one:
            parts.append(NUMBER_NAMES[hundred][0])
        elif hundred > 1:
            parts.append(NUMBER_NAMES[hundred][1])

    return " ".join(reversed(parts))


def _num2words(
    number: int,
    by_n_digits: int = 0,
    include_leading_one: bool = True,
) -> str:
    """Convert integer to Mongolian words (internal)."""
    if number == 0:
        return NUMBER_NAMES[0][0]

    parts = []
    negative = number < 0
    remaining = abs(number)

    MAX_UNIT = 1_000_000_000_000
    if by_n_digits == 0 and remaining > 999 * MAX_UNIT:
        by_n_digits = 3

    if by_n_digits > 0:
        while remaining > 0:
            chunk = remaining % (10**by_n_digits)
            remaining = remaining // (10**by_n_digits)

            if chunk > 0:
                parts.append(_num2words(chunk, include_leading_one=include_leading_one))
            else:
                parts.append(", ".join([NUMBER_NAMES[0][0]] * by_n_digits))

        text = ", ".join(reversed(parts))
    else:
        current_unit = 1
        while remaining > 0:
            chunk = remaining % 1000
            remaining = remaining // 1000

            if chunk > 0:
                if current_unit != 1:
                    if current_unit not in NUMBER_NAMES:
                        return _num2words(
                            abs(number) if not negative else -abs(number),
                            by_n_digits=3,
                            include_leading_one=include_leading_one,
                        )
                    parts.append(NUMBER_NAMES[current_unit][0])
                if chunk > 1 or include_leading_one:
                    parts.append(
                        _num2words_3digits(
                            chunk,
                            cont=(len(parts) > 0 and chunk > 1),
                            include_leading_one=include_leading_one,
                        )
                    )
            current_unit *= 1000
        text = " ".join(reversed(parts))

    if negative:
        text = "хасах " + text

    return text


def num2words(
    number: int | float,
    by_n_digits: int = 0,
    use_dot: bool = False,
    include_leading_one: bool = True,
) -> str:
    """Convert number to Mongolian words.

    Args:
        number: Number to convert (int or float)
        by_n_digits: If > 0, converts digit-by-digit in groups
        use_dot: Use "цэг" for decimal point instead of fraction names
        include_leading_one: Include "нэг" for units like 1000

    Returns:
        Mongolian word representation of the number

    Examples:
        >>> num2words(123)
        'нэгэн зуун хорин гурав'
        >>> num2words(3.14)
        'гурав зууны арван дөрөв'
        >>> num2words(3.14, use_dot=True)
        'гурав цэг арван дөрөв'
    """
    if isinstance(number, int):
        return _num2words(number, by_n_digits=by_n_digits, include_leading_one=include_leading_one)

    # Convert to string avoiding scientific notation
    abs_num = abs(number)
    num_str = f"{abs_num:.15f}".rstrip("0").rstrip(".")

    if "." in num_str:
        int_str, frac_str = num_str.split(".")
    else:
        int_str, frac_str = num_str, ""

    int_part = int(int_str)
    frac_part_int = int(frac_str) if frac_str else 0

    text = _num2words(int_part, by_n_digits=by_n_digits, include_leading_one=include_leading_one)

    if number < 0:
        text = "хасах " + text

    if frac_part_int == 0:
        return text

    frac_text = _num2words(frac_part_int, include_leading_one=include_leading_one)

    if use_dot or by_n_digits > 0:
        return f"{text} цэг {frac_text}"

    frac_denominator = 10 ** len(frac_str)
    frac_den_text = FRACTION_NAMES.get(frac_denominator, "")

    if frac_den_text:
        return f"{text} {frac_den_text} {frac_text}"
    return f"{text} цэг {frac_text}"
