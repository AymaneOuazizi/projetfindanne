import re
import unicodedata


def normalize_entity_id(
    name: str,
) -> str:
    normalized = unicodedata.normalize(
        "NFKD",
        name,
    )

    normalized = normalized.encode(
        "ascii",
        "ignore",
    ).decode(
        "ascii"
    )

    normalized = normalized.lower()

    normalized = re.sub(
        r"[^a-z0-9]+",
        "_",
        normalized,
    )

    normalized = normalized.strip("_")

    return normalized   