"""Mongolian Cyrillic grapheme-to-phoneme converter."""

VOWELS_NORMAL = "аэиоуөүый"
VOWELS_YA = "яеёю"
VOWELS_MASCULINE = "аоуяёю"
CONSONANTS = "бвгджзклмнпрстфхцчшщ"
SIGNS = "ьъ"
ALPHABETS_LOWER = "абвгдеёжзийклмноөпрстуүхфчцшщьъыэюя"
ALPHABETS_UPPER = "АБВГДЕЁЖЗИЙКЛМНОӨПРСТУҮХФЧЦШЩЬЪЫЭЮЯ"

CONSONANTS_REGULAR = [
    ("б", "b-"),
    ("в", "v-"),
    ("г", "g-"),
    ("д", "d-"),
    ("ж", "w-"),
    ("з", "z-"),
    ("к", "k-"),
    ("л", "l-"),
    ("м", "m-"),
    ("н", "n-"),
    ("п", "p-"),
    ("р", "r-"),
    ("с", "s-"),
    ("т", "t-"),
    ("ф", "f-"),
    ("х", "x-"),
    ("ц", "c-"),
    ("ч", "h-"),
    ("ш", "S-"),
    ("щ", "S-"),
]

CONSONANTS_SOFT_I = [
    ("би", "B-и"),
    ("ви", "V-и"),
    ("ги", "C-и"),
    ("ди", "D-и"),
    ("ли", "L-и"),
    ("ми", "M-и"),
    ("ни", "N-и"),
    ("ри", "R-и"),
    ("ти", "T-и"),
    ("хи", "X-и"),
]

CONSONANTS_SOFT_SIGN = [
    ("бь", "B-"),
    ("вь", "V-"),
    ("гь", "C-"),
    ("дь", "D-"),
    ("ль", "L-"),
    ("мь", "M-"),
    ("нь", "N-"),
    ("рь", "R-"),
    ("ть", "T-"),
    ("хь", "X-"),
    ("кь", "K-"),
    ("пь", "P-"),
]

YA_VOWELS = [("я", "j-а"), ("е", "j-э"), ("ё", "j-о"), ("ю", "j-у")]

DOUBLE_VOWELS = [
    ("ай", "ay"),
    ("эй", "ey"),
    ("ой", "oy"),
    ("уй", "uy"),
    ("үй", "^y"),
    ("аа", "a:"),
    ("ээ", "e:"),
    ("оо", "o:"),
    ("уу", "u:"),
    ("үү", "^:"),
    ("өө", "@:"),
    ("ий", "i:"),
]

SINGLE_VOWELS = [
    ("а", "a"),
    ("э", "e"),
    ("и", "i"),
    ("о", "o"),
    ("у", "u"),
    ("ү", "^"),
    ("ө", "@"),
    ("ы", "y:"),
]

G_SPECIAL = [("га", "G-а"), ("го", "G-о"), ("гу", "G-у"), ("гы", "G-ы")]
IA_VOWELS = [("иа", "A:"), ("ио", "O:"), ("иу", "U:")]

PO_VOWELS = "aeiou^@y"
PO_BACK_MASCULINE = "aou"
PO_FRONT_MASCULINE = "AOU"


class G2P:
    """Grapheme-to-phoneme converter for Mongolian Cyrillic."""

    def syllabify(self, text: str) -> list[str]:
        """Split text into syllables (handles multiple words)."""
        if not text:
            return [""]
        words = text.split()
        all_syllables = []
        for word in words:
            all_syllables.extend(self._syllabify_word(word))
        return all_syllables

    def _to_lower(self, text: str) -> str:
        result = []
        for char in text:
            idx = ALPHABETS_UPPER.find(char)
            result.append(ALPHABETS_LOWER[idx] if idx >= 0 else char)
        return "".join(result)

    def _syllable_to_phoneme(self, syl: str, is_masculine: bool, stressed: bool) -> str:
        # Handle н at end or before consonants
        for i in range(len(syl)):
            if syl[i] == "н":
                if i + 1 == len(syl):
                    syl = syl[:i] + "ng-"
                    break
                if i + 1 < len(syl) and syl[i + 1] in CONSONANTS:
                    syl = syl[:i] + "ng-" + syl[i + 1 :]
                    break

        if is_masculine:
            for cy, ph in CONSONANTS_SOFT_I:
                syl = syl.replace(cy, ph)

        for cy, ph in CONSONANTS_SOFT_SIGN:
            syl = syl.replace(cy, ph)

        for cy, ph in G_SPECIAL:
            syl = syl.replace(cy, ph)

        # е after consonants becomes э
        syl_list = list(syl)
        for i in range(1, len(syl_list)):
            if syl_list[i] == "е" and syl[i - 1] in CONSONANTS:
                syl_list[i] = "э"
        syl = "".join(syl_list)

        for cy, ph in YA_VOWELS:
            syl = syl.replace(cy, ph)

        stress = "1-" if stressed else "0-"

        for cy, ph in IA_VOWELS:
            syl = syl.replace(cy, ph + stress)

        for cy, ph in DOUBLE_VOWELS:
            syl = syl.replace(cy, ph + stress)

        for cy, ph in SINGLE_VOWELS:
            syl = syl.replace(cy, ph + stress)

        for cy, ph in CONSONANTS_REGULAR:
            syl = syl.replace(cy, ph)

        if syl.endswith("-"):
            syl = syl[:-1]

        return syl

    def _convert_syllables(self, syllables: list[str]) -> str:
        if not syllables:
            return ""

        result = []
        masculine = False

        for i, syl in enumerate(syllables):
            if not syl:
                continue

            if i == 0:
                masculine = any(c in VOWELS_MASCULINE for c in syl)

            if masculine and syl.endswith("ъ"):
                if i + 1 < len(syllables) and syllables[i + 1] and syllables[i + 1][0] in VOWELS_YA:
                    syl = syl[:-1]
            elif not masculine and syl.endswith("ь"):
                if i + 1 < len(syllables) and syllables[i + 1] and syllables[i + 1][0] in VOWELS_YA:
                    syl = syl[:-1]

            result.append(self._syllable_to_phoneme(syl, masculine, i == 0))

        return "|".join(result) + "|"

    def convert(self, text: str) -> str:
        """Convert text to phoneme representation."""
        words = text.split()
        results = []
        for word in words:
            cleaned = "".join(c for c in word.lower() if c in ALPHABETS_LOWER)
            if cleaned:
                syllables = self._syllabify_word(cleaned)
                results.append(self._convert_syllables(syllables))
        return "*".join(results)

    def _syllabify_word(self, word: str) -> list[str]:
        """Split a single word into syllables (internal)."""
        word = self._to_lower(word)
        syllables = []
        start = 0

        for i in range(1, len(word)):
            if word[i] in VOWELS_NORMAL:
                if word[i - 1] not in CONSONANTS:
                    continue
                if start == 0 and i == 1:
                    continue
                syllables.append(word[start : i - 1])
                start = i - 1
            elif word[i] in VOWELS_YA:
                if word[i - 1] in SIGNS or word[i - 1] in VOWELS_NORMAL:
                    syllables.append(word[start:i])
                    start = i
                    continue
                if word[i - 1] in CONSONANTS:
                    if start == 0 and i == 1:
                        continue
                    syllables.append(word[start : i - 1])
                    start = i - 1

        syllables.append(word[start:])
        return syllables


_default_g2p: G2P | None = None


def _get_g2p() -> G2P:
    global _default_g2p
    if _default_g2p is None:
        _default_g2p = G2P()
    return _default_g2p


def convert(text: str) -> str:
    """Convert Mongolian text to phoneme representation."""
    return _get_g2p().convert(text)


def syllabify(word: str) -> list[str]:
    """Split Mongolian word into syllables."""
    return _get_g2p().syllabify(word)
