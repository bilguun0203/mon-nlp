"""English to Mongolian Cyrillic transliteration via IPA."""

IPA_MAP = [
    ("aɪ", "ай"),
    ("b", "б"),
    ("d", "д"),
    ("dz", "з"),
    ("dʒ", "ж"),
    ("e", "э"),
    ("eə", "эа"),
    ("eɪ", "эй"),
    ("eɪə", "эйа"),
    ("eː", "ээ"),
    ("f", "ф"),
    ("g", "г"),
    ("h", "х"),
    ("i", "и"),
    ("iː", "ий"),
    ("j", "и"),
    ("ja", "я"),
    ("je", "е"),
    ("jeɪ", "ей"),
    ("jeː", "ее"),
    ("jo", "ё"),
    ("joʊ", "ёо"),
    ("joː", "ёо"),
    ("ju", "ю"),
    ("juː", "юу"),
    ("jæ", "я"),
    ("jæː", "яа"),
    ("jœ", "ё"),
    ("jœː", "ёо"),
    ("jɑ", "я"),
    ("jɑː", "яа"),
    ("jɔ", "ё"),
    ("jɔː", "ёо"),
    ("jə", "е"),
    ("jɪ", "еи"),
    ("jɵ", "ё"),
    ("jɵː", "ёо"),
    ("k", "к"),
    ("kh", "к"),
    ("l", "л"),
    ("lh", "лх"),
    ("m", "м"),
    ("n", "н"),
    ("o", "о"),
    ("oi", "ой"),
    ("oː", "оо"),
    ("p", "п"),
    ("pʰ", "п"),
    ("q", "г"),
    ("r", "р"),
    ("s", "с"),
    ("t", "т"),
    ("ts", "ц"),
    ("tʃ", "ч"),
    ("tʰ", "т"),
    ("u", "у"),
    ("ui", "үй"),
    ("uː", "уу"),
    ("v", "в"),
    ("w", "в"),
    ("waː", "уа"),
    ("wæː", "уай"),
    ("x", "х"),
    ("y", "ү"),
    ("yː", "үй"),
    ("z", "с"),
    ("æ", "эай"),
    ("æː", "ай"),
    ("ð", "д"),
    ("ŋ", "нг"),
    ("œ", "о"),
    ("œː", "оо"),
    ("ɐ", "ай"),
    ("ɑ", "а"),
    ("ɑː", "аа"),
    ("ɒ", "о"),
    ("ɔ", "о"),
    ("ɔɪ", "ой"),
    ("ɔː", "оо"),
    ("ə", "э"),
    ("ɚ", "эр"),
    ("ɛ", "эй"),
    ("ɜ", "ой"),
    ("ɜː", "иоур"),
    ("ɝ", "эр"),
    ("ɡ", "г"),
    ("ɣ", "г"),
    ("ɪ", "и"),
    ("ɪə", "иа"),
    ("ɬ", "л"),
    ("ɵ", "ө"),
    ("ɵː", "өө"),
    ("ɸ", "в"),
    ("ɹ", "р"),
    ("ɾ", "т"),
    ("ʁ", "г"),
    ("ʃ", "ш"),
    ("ʊ", "үү"),
    ("ʊə", "уа"),
    ("ʌ", "а"),
    ("ʏ", "у"),
    ("ʏː", "уу"),
    ("ʒ", "ж"),
    ("ʝ", "и"),
    ("ʦ", "з"),
    ("ʦʰ", "ц"),
    ("ʧ", "ж"),
    ("ʧʰ", "ч"),
    ("ʼ", ""),
    ("ˈ", ""),
    ("ˌ", ""),
    ("ː", ""),
    ("θ", "т"),
    ("χ", "х"),
    ("ᵻ", "и"),
]

IPA_MAP_SORTED = sorted(IPA_MAP, key=lambda x: len(x[0]), reverse=True)


class EnglishToCyrillic:
    """Transliterates English text to Mongolian Cyrillic via IPA."""

    def __init__(self):
        self._phonemizer = None

    def _get_phonemizer(self):
        if self._phonemizer is None:
            try:
                from phonemizer import phonemize

                self._phonemizer = phonemize
            except ImportError:
                raise ImportError(
                    "phonemizer package is required for English transliteration. "
                    "Install with: pip install mon-nlp[transliterate]"
                )
        return self._phonemizer

    def get_ipa(self, text: str, language: str = "en-us") -> str:
        """Get IPA representation of English text."""
        phonemize = self._get_phonemizer()
        try:
            return phonemize(
                text,
                language=language,
                backend="espeak",
                strip=True,
                preserve_punctuation=True,
                with_stress=False,
                language_switch="remove-flags",
            )
        except Exception:
            return ""

    def ipa_to_cyrillic(self, ipa_text: str) -> str:
        """Convert IPA text to Cyrillic."""
        result = ipa_text
        for ipa_seq, cyrillic in IPA_MAP_SORTED:
            result = result.replace(ipa_seq, cyrillic)
        return result

    def transliterate(self, text: str, language: str = "en-us", output_ipa: bool = False) -> str:
        """Transliterate English text to Mongolian Cyrillic.

        Args:
            text: English text to transliterate
            language: Source language code (default: "en-us")
            output_ipa: If True, return IPA instead of Cyrillic

        Returns:
            Mongolian Cyrillic transliteration, or IPA if output_ipa=True
        """
        ipa = self.get_ipa(text, language)
        if not ipa:
            return ""
        return ipa if output_ipa else self.ipa_to_cyrillic(ipa)


_default_converter: EnglishToCyrillic | None = None


def _get_converter() -> EnglishToCyrillic:
    global _default_converter
    if _default_converter is None:
        _default_converter = EnglishToCyrillic()
    return _default_converter


def transliterate(text: str, language: str = "en-us", output_ipa: bool = False) -> str:
    """Transliterate English text to Mongolian Cyrillic.

    Args:
        text: English text to transliterate
        language: Source language code (default: "en-us")
        output_ipa: If True, return IPA instead of Cyrillic

    Returns:
        Mongolian Cyrillic transliteration, or IPA if output_ipa=True
    """
    return _get_converter().transliterate(text, language, output_ipa)


def get_ipa(text: str, language: str = "en-us") -> str:
    """Get IPA representation of English text."""
    return _get_converter().get_ipa(text, language)


def ipa_to_cyrillic(ipa_text: str) -> str:
    """Convert IPA text to Cyrillic."""
    return _get_converter().ipa_to_cyrillic(ipa_text)
