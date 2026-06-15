import easyocr

_reader: easyocr.Reader | None = None


def get_reader() -> easyocr.Reader:
    # Loaded lazily: building the Reader loads the OCR models, so the first
    # call (or first test) is slow but every later call reuses it.
    global _reader
    if _reader is None:
        _reader = easyocr.Reader(["en", "ru"], gpu=False)
    return _reader


def extract_text(image_bytes: bytes) -> str:
    reader = get_reader()
    lines = reader.readtext(image_bytes, detail=0)
    return "\n".join(lines)
