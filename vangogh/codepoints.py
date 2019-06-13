import sys
import unicodedata


def characters(string):
    return sorted(set([c for c in string]))


def is_unicode(char):
    try:
        char.encode("ascii")
    except UnicodeEncodeError:
        return True
    return False


def normalized(char):
    return unicodedata.normalize("NFKD", char)[0]


def process(text):
    chars = []
    for c in characters(text):
        if is_unicode(c):
            chars.append(
                {
                    "character": c,
                    "codepoint": f"0x{ord(c):04x}",
                    "name": unicodedata.name(c),
                    "normalized": normalized(c),
                }
            )
    return chars


if __name__ == "__main__":
    inf = sys.argv[1]
    with open(inf, "r") as f:
        chars = process(f.read())
    if chars:
        for c in chars:
            print(
                f"{c['character']:8}{c['codepoint']:8}\t{c['name']:40}\t{c['normalized']:8}"
            )
