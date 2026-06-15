from app.services.parsers import extract_fields, parse_invoice, parse_passport, parse_receipt


def test_parse_passport():
    text = "PASSPORT\nName: John Smith\nDate of Birth: 01.01.1990\nPassport No: AB1234567"

    result = parse_passport(text)

    assert result["full_name"] == "John Smith"
    assert result["birth_date"] == "01.01.1990"
    assert result["passport_number"] == "AB1234567"


def test_parse_invoice():
    text = "INVOICE\nInvoice No: INV-2026-001\nDate: 10.01.2026\nSupplier: Acme Corp\nTotal: 1500.00"

    result = parse_invoice(text)

    assert result["number"] == "INV-2026-001"
    assert result["date"] == "10.01.2026"
    assert result["supplier"] == "Acme Corp"
    assert result["amount"] == "1500.00"


def test_parse_invoice_russian():
    text = "Накладная №357\nДата: 14.06.2026\nПоставщик: ООО Ромашка\nИтого: 15 000,50"

    result = parse_invoice(text)

    assert result["number"] == "357"
    assert result["date"] == "14.06.2026"
    assert result["supplier"] == "ООО Ромашка"
    assert result["amount"] == "15 000,50"


def test_parse_receipt():
    text = "RECEIPT\nStore: SuperMart\nDate: 14.06.2026\nTotal: 45.67"

    result = parse_receipt(text)

    assert result["store"] == "SuperMart"
    assert result["date"] == "14.06.2026"
    assert result["total"] == "45.67"


def test_extract_fields_dispatch():
    text = "Store: SuperMart\nTotal: 10.00"

    assert extract_fields("receipt", text)["store"] == "SuperMart"
    assert extract_fields(None, text) is None
