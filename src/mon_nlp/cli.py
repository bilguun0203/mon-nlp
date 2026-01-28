"""Command-line interface for mon-nlp."""

import argparse
import sys


def cmd_case(args):
    from mon_nlp import case

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    if args.upper:
        print(case.to_uppercase(text))
    elif args.lower:
        print(case.to_lowercase(text))
    elif args.sentence:
        print(case.to_sentence_case(text))


def cmd_punct(args):
    from mon_nlp import punctuation

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    if args.normalize:
        print(punctuation.normalize(text))
    elif args.to_words:
        print(punctuation.to_words(text))
    elif args.remove:
        print(punctuation.remove(text))


def cmd_abbrev(args):
    from mon_nlp import abbreviation

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    print(abbreviation.expand(text))


def cmd_num(args):
    from mon_nlp import number

    num_str = args.number
    try:
        if "." in num_str or "," in num_str:
            num = float(num_str.replace(",", "."))
        else:
            num = int(num_str)
        print(number.num2words(num, by_n_digits=args.by_digits, use_dot=args.use_dot))
    except ValueError:
        print(f"Error: Invalid number '{num_str}'", file=sys.stderr)
        sys.exit(1)


def cmd_emoji(args):
    from mon_nlp import emoji

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    print(emoji.emoji_to_words(text, format=args.format))


def cmd_transliterate(args):
    from mon_nlp.transliterate import transliterate

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    try:
        print(transliterate(text, language=args.language, output_ipa=args.ipa))
    except ImportError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_g2p(args):
    from mon_nlp import g2p

    text = " ".join(args.text) if args.text else sys.stdin.read().strip()
    print(g2p.convert(text))


def main():
    parser = argparse.ArgumentParser(
        prog="mon-nlp",
        description="Mongolian Cyrillic text normalization and processing",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # case
    p_case = subparsers.add_parser("case", help="Text case conversion")
    case_group = p_case.add_mutually_exclusive_group(required=True)
    case_group.add_argument("--upper", "-u", action="store_true", help="Convert to uppercase")
    case_group.add_argument("--lower", "-l", action="store_true", help="Convert to lowercase")
    case_group.add_argument(
        "--sentence", "-s", action="store_true", help="Convert to sentence case"
    )
    p_case.add_argument("text", nargs="*", help="Text to convert")
    p_case.set_defaults(func=cmd_case)

    # punct
    p_punct = subparsers.add_parser("punct", help="Punctuation normalization")
    punct_group = p_punct.add_mutually_exclusive_group(required=True)
    punct_group.add_argument("--normalize", "-n", action="store_true", help="Normalize punctuation")
    punct_group.add_argument("--to-words", "-w", action="store_true", help="Convert to words")
    punct_group.add_argument("--remove", "-r", action="store_true", help="Remove punctuation")
    p_punct.add_argument("text", nargs="*", help="Text to process")
    p_punct.set_defaults(func=cmd_punct)

    # abbrev
    p_abbrev = subparsers.add_parser("abbrev", help="Expand abbreviations")
    p_abbrev.add_argument("text", nargs="*", help="Text with abbreviations")
    p_abbrev.set_defaults(func=cmd_abbrev)

    # num
    p_num = subparsers.add_parser("num", help="Convert number to words")
    p_num.add_argument("number", help="Number to convert")
    p_num.add_argument("--by-digits", "-d", type=int, default=0, help="Group by N digits")
    p_num.add_argument("--use-dot", action="store_true", help="Use 'цэг' for decimal")
    p_num.set_defaults(func=cmd_num)

    # emoji
    p_emoji = subparsers.add_parser("emoji", help="Convert emojis to words")
    p_emoji.add_argument("text", nargs="*", help="Text with emojis")
    p_emoji.add_argument(
        "--format",
        "-f",
        choices=["plain", "brackets", "parentheses"],
        default="plain",
        help="Output format",
    )
    p_emoji.set_defaults(func=cmd_emoji)

    # transliterate
    p_trans = subparsers.add_parser("transliterate", help="English to Cyrillic")
    p_trans.add_argument("text", nargs="*", help="English text")
    p_trans.add_argument("--language", "-l", default="en-us", help="Source language")
    p_trans.add_argument("--ipa", "-i", action="store_true", help="Output IPA instead of Cyrillic")
    p_trans.set_defaults(func=cmd_transliterate)

    # g2p
    p_g2p = subparsers.add_parser("g2p", help="Grapheme to phoneme conversion")
    p_g2p.add_argument("text", nargs="*", help="Mongolian text")
    p_g2p.set_defaults(func=cmd_g2p)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
