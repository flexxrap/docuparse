import re

# only horizontal whitespace, so patterns never accidentally span lines
SP = r"[ \t]*"


def _search(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None


def parse_passport(text: str) -> dict:
    return {
        "full_name": _search(rf"(?:name|фио|имя){SP}[:\-]?{SP}(.+)", text),
        "passport_number": _search(
            rf"(?:passport{SP}(?:no\.?|number)?|серия и номер|№){SP}[:\-]?{SP}([a-zа-я0-9 ]{{6,}})",
            text,
        ),
        "birth_date": _search(
            rf"(?:date of birth|dob|дата рождения){SP}[:\-]?{SP}(\d{{1,2}}[./-]\d{{1,2}}[./-]\d{{2,4}})",
            text,
        ),
    }


def parse_invoice(text: str) -> dict:
    return {
        "number": _search(
            rf"(?:invoice{SP}(?:no\.?|number)?|накладная|сч[её]т){SP}№?{SP}[:\-]?{SP}(\S+)", text
        ),
        "date": _search(
            rf"(?:date|дата){SP}[:\-]?{SP}(\d{{1,2}}[./-]\d{{1,2}}[./-]\d{{2,4}}|\d{{4}}-\d{{2}}-\d{{2}})",
            text,
        ),
        "amount": _search(rf"(?:total|сумма|итого){SP}[:\-]?{SP}([\d .,]+)", text),
        "supplier": _search(rf"(?:supplier|поставщик){SP}[:\-]?{SP}(.+)", text),
    }


def parse_receipt(text: str) -> dict:
    return {
        "store": _search(rf"(?:store|shop|магазин){SP}[:\-]?{SP}(.+)", text),
        "date": _search(
            rf"(?:date|дата){SP}[:\-]?{SP}(\d{{1,2}}[./-]\d{{1,2}}[./-]\d{{2,4}}|\d{{4}}-\d{{2}}-\d{{2}})",
            text,
        ),
        "total": _search(rf"(?:total|итого|сумма){SP}[:\-]?{SP}([\d .,]+)", text),
    }


PARSERS = {
    "passport": parse_passport,
    "invoice": parse_invoice,
    "receipt": parse_receipt,
}


def extract_fields(doc_type: str | None, text: str) -> dict | None:
    parser = PARSERS.get(doc_type) if doc_type else None
    return parser(text) if parser else None
