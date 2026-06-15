import re


def _search(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
    return match.group(1).strip() if match else None


def parse_passport(text: str) -> dict:
    return {
        "full_name": _search(r"(?:name|фио|имя)\s*[:\-]?\s*(.+)", text),
        "passport_number": _search(
            r"(?:passport\s*(?:no\.?|number)?|серия и номер|№)\s*[:\-]?\s*([a-zа-я0-9 ]{6,})",
            text,
        ),
        "birth_date": _search(
            r"(?:date of birth|dob|дата рождения)\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4})",
            text,
        ),
    }


def parse_invoice(text: str) -> dict:
    return {
        "number": _search(
            r"(?:invoice\s*(?:no\.?|number)?|накладная|сч[её]т)\s*№?\s*[:\-]?\s*(\S+)", text
        ),
        "date": _search(
            r"(?:date|дата)\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})", text
        ),
        "amount": _search(r"(?:total|сумма|итого)\s*[:\-]?\s*([\d\s.,]+)", text),
        "supplier": _search(r"(?:supplier|поставщик)\s*[:\-]?\s*(.+)", text),
    }


def parse_receipt(text: str) -> dict:
    return {
        "store": _search(r"(?:store|shop|магазин)\s*[:\-]?\s*(.+)", text),
        "date": _search(
            r"(?:date|дата)\s*[:\-]?\s*(\d{1,2}[./-]\d{1,2}[./-]\d{2,4}|\d{4}-\d{2}-\d{2})", text
        ),
        "total": _search(r"(?:total|итого|сумма)\s*[:\-]?\s*([\d\s.,]+)", text),
    }


PARSERS = {
    "passport": parse_passport,
    "invoice": parse_invoice,
    "receipt": parse_receipt,
}


def extract_fields(doc_type: str | None, text: str) -> dict | None:
    parser = PARSERS.get(doc_type) if doc_type else None
    return parser(text) if parser else None
