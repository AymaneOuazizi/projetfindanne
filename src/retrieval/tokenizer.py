import re


def tokenize(text: str) -> list[str]:
    text = text.lower()

    tokens = re.findall(
        r"\b\w+\b",
        text,
    )

    return tokens