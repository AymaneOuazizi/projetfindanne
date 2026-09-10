from pathlib import Path

from pypdf import PdfReader

UPLOAD_DIR = Path(
    "data/raw/uploads"
)


def save_uploaded_file(
    filename: str,
    content: bytes,
) -> Path:
    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_filename = (
        Path(filename).name
    )

    file_path = (
        UPLOAD_DIR
        / safe_filename
    )

    file_path.write_bytes(
        content
    )

    return file_path


def extract_uploaded_text(
    file_path: Path,
) -> str:
    suffix = (
        file_path.suffix.lower()
    )
    if suffix in {".txt", ".md", ".markdown"}:
            return file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
    if suffix == ".txt":
        return file_path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    if suffix == ".pdf":
        reader = PdfReader(
            str(file_path)
        )

        pages = []

        for page in reader.pages:
            text = (
                page.extract_text()
                or ""
            )

            if text.strip():
                pages.append(
                    text.strip()
                )

        return "\n\n".join(
            pages
        )

    raise ValueError(
        "Unsupported file type: "
        f"{suffix}"
    )