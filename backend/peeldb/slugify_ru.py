"""Russian text helpers for catalog slugs."""

from django.utils.text import slugify as django_slugify

_TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "",
    "ы": "y",
    "ь": "",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def slugify_ru(value: str, *, max_length: int = 180) -> str:
    """ASCII slug that keeps meaning for Cyrillic job titles."""
    text = (value or "").strip().lower()
    out = []
    for ch in text:
        if ch in _TRANSLIT:
            out.append(_TRANSLIT[ch])
        elif ch.isascii() and (ch.isalnum() or ch in "-_"):
            out.append(ch)
        elif ch in " /\\.,+«»()[]":
            out.append("-")
        else:
            out.append("-")
    raw = "".join(out)
    while "--" in raw:
        raw = raw.replace("--", "-")
    slug = django_slugify(raw.strip("-")) or "job"
    return slug[:max_length].rstrip("-")
