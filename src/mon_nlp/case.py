"""Text case normalization for Mongolian Cyrillic text."""


def to_uppercase(text: str) -> str:
    """Convert text to uppercase."""
    return text.upper()


def to_lowercase(text: str) -> str:
    """Convert text to lowercase."""
    return text.lower()


def to_sentence_case(text: str) -> str:
    """Convert text to sentence case (capitalize first letter of each sentence)."""
    if not text:
        return text

    result = []
    capitalize_next = True

    for char in text:
        if capitalize_next and char.isalpha():
            result.append(char.upper())
            capitalize_next = False
        else:
            result.append(char.lower())

        if char in ".!?":
            capitalize_next = True

    return "".join(result)
