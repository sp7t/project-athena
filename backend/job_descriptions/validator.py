import re

# Common low-effort or placeholder words
GARBAGE_WORDS = {
    "asdf",
    "1234",
    "blah",
    "test",
    "testing",
    "qwerty",
    "hello",
    "abc",
    "xyz",
    "none",
    "something",
    "whatever",
    "thing",
    "thingy",
    "nope",
    "random",
    "fake",
    "dummy",
}

# Banned characters or sequences
EMOJIS_OR_SCRIPTS = ["😂", "<script>", "!!!"]


def is_irrelevant(text: str) -> bool:
    """Return True if the text is irrelevant, unprofessional,
    or likely a placeholder (e.g., symbols, emojis, short junk).
    """  # noqa: D205
    text_clean = text.strip().lower()

    # Empty input or too short
    if not text_clean or len(text_clean) < 3:  # noqa: PLR2004
        return True

    # Only symbols (no letters/numbers)
    if re.fullmatch(r"[^\w\s]+", text_clean):
        return True

    # Contains junk phrases or known emoji/script snippets
    if text_clean in GARBAGE_WORDS or any(
        bad in text_clean for bad in EMOJIS_OR_SCRIPTS
    ):
        return True

    # No alphabet letters at all
    return bool(not re.search(r"[a-zA-Z]", text_clean))
