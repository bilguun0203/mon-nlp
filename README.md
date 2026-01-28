# mon-nlp

Cyrillic Mongolian text normalization and processing library.

## Installation

```bash
pip install mon-nlp
```

For English to Cyrillic transliteration support (Needs eSpeak for IPA conversion):

```bash
pip install mon-nlp[transliterate]
```

## Features

- **Text Case Normalization**: Convert text to uppercase, lowercase, or sentence case
- **Punctuation Normalization**: Normalize, convert to words, or remove punctuation
- **Abbreviation Expansion**: Expand common Mongolian abbreviations
- **Number to Words**: Convert numbers to Mongolian words (integers, floats, negatives, Roman numerals)
- **Emoji to Words**: Convert emojis to Mongolian descriptions
- **English to Cyrillic**: Transliterate English text to Mongolian Cyrillic via IPA
- **Grapheme to Phoneme**: Convert Mongolian text to phoneme representation with syllabification

## Usage

### Text Case

```python
from mon_nlp import to_uppercase, to_lowercase, to_sentence_case

to_uppercase("сайн байна уу")  # "САЙН БАЙНА УУ"
to_lowercase("САЙН БАЙНА УУ")  # "сайн байна уу"
to_sentence_case("САЙН. БАЙНА")  # "Сайн. Байна"
```

### Punctuation

```python
from mon_nlp import normalize_punctuation, punctuation_to_words, remove_punctuation

normalize_punctuation("“Сайн”")  # '"Сайн"'
punctuation_to_words("Сайн.")  # "Сайн цэг"
remove_punctuation("Сайн, байна!")  # "Сайн байна"
```

### Abbreviations

```python
from mon_nlp import expand_abbreviations, AbbreviationExpander

expand_abbreviations("МУ нь")  # "Монгол Улс нь"

# Custom abbreviations
expander = AbbreviationExpander({"ПХ": "программ хангамж"})
expander.expand("ПХ хөгжүүлэх")  # "программ хангамж хөгжүүлэх"
```

### Numbers

```python
from mon_nlp import num2words, roman2num

num2words(123)  # "нэг зуун хорин гурав"
num2words(3.14)  # "гурав зууны арван дөрөв"
num2words(3.14, use_dot=True)  # "гурав цэг арван дөрөв"
num2words(-42)  # "хасах дөчин хоёр"
num2words(1000, include_leading_one=False)  # "мянга"
num2words(1234, by_n_digits=2)  # "арван хоёр, гучин дөрөв"

roman2num("XIV")  # 14
roman2num("MCMXCIV")  # 1994
```

### Emojis

```python
from mon_nlp import emoji_to_words, remove_emoji

emoji_to_words("Сайн 😀")  # "Сайн инээмсэглэсэн царай"
emoji_to_words("Сайн 😀", format="brackets")  # "Сайн [инээмсэглэсэн царай]"
emoji_to_words("Сайн 😀", format="parentheses")  # "Сайн (инээмсэглэсэн царай)"
emoji_to_words("😀😄")  # "инээмсэглэсэн царай мишээсэн нүдтэй инээж буй царай"
remove_emoji("Сайн 😀 байна")  # "Сайн  байна"

# Custom emoji mappings
from mon_nlp import add_emoji_mapping, remove_emoji_mapping, get_emoji_mappings

add_emoji_mapping("🎉", "баяр хүргэе")
remove_emoji_mapping("😀")
get_emoji_mappings()  # Returns all current mappings
```

### English to Cyrillic

Requires optional dependency: `pip install mon-nlp[transliterate]`

```python
from mon_nlp import transliterate

transliterate("hello world")  # "хэлоүү виоурлд"
transliterate("hello world", output_ipa=True)  # "həloʊ wɜːld"
```

### Grapheme to Phoneme

```python
from mon_nlp import g2p_convert, syllabify, G2P

# Convert text to phoneme representation
g2p_convert("сайн")  # "s-ay1-ng|"
g2p_convert("байна")  # "b-ay1|n-a0|"
g2p_convert("сайн байна уу")  # "s-ay1-ng|*b-ay1|n-a0|*u:1|"

# Syllabification
syllabify("байна")  # ["бай", "на"]
syllabify("монгол")  # ["мон", "гол"]
syllabify("байна уу")  # ["бай", "на", "уу"]

# Using the G2P class directly
converter = G2P()
converter.convert("монгол")  # "m-o1-ng|G-o0-l|"
converter.syllabify("сайн")  # ["сайн"]
```

## CLI

The package includes a command-line interface:

```bash
# Case conversion
mon-nlp case --upper "сайн байна"
mon-nlp case --lower "САЙН БАЙНА"
mon-nlp case --sentence "сайн. байна"

# Punctuation
mon-nlp punct --normalize "«текст»"
mon-nlp punct --to-words "Сайн."
mon-nlp punct --remove "Сайн!"

# Abbreviations
mon-nlp abbrev "МУ байна"

# Numbers
mon-nlp num 123
mon-nlp num --by-digits 2 1234
mon-nlp num --use-dot 3.14

# Emojis
mon-nlp emoji "Сайн 😀"
mon-nlp emoji --format brackets "Сайн 😀"

# Transliteration (requires transliterate extra)
mon-nlp transliterate "hello"
mon-nlp transliterate --language en-us "world"
mon-nlp transliterate --ipa "hello world"  # Output IPA instead of Cyrillic

# Grapheme to Phoneme
mon-nlp g2p "сайн байна"
```

All commands support reading from stdin:

```bash
echo "сайн байна" | mon-nlp case --upper
```

## Development

```bash
# Install with dev dependencies
make dev

# Run tests
make test

# Run linter
make lint

# Format code
make format

# Build package
make build

# Clean build artifacts
make clean
```

## License

GPL-3.0-or-later

See the [LICENSE](LICENSE) file for details.
