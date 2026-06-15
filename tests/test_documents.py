import io

from PIL import Image, ImageDraw


def make_text_image(text: str) -> io.BytesIO:
    img = Image.new("RGB", (400, 100), color="white")
    draw = ImageDraw.Draw(img)
    draw.text((10, 35), text, fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


async def test_parse_document(client):
    img = make_text_image("HELLO WORLD")

    resp = await client.post(
        "/documents/parse",
        files={"file": ("test.png", img, "image/png")},
    )

    assert resp.status_code == 201
    body = resp.json()
    assert body["filename"] == "test.png"
    assert isinstance(body["id"], int)
    # OCR output on a synthetic image can be imperfect, just check we got text back
    assert isinstance(body["raw_text"], str)


async def test_get_document(client):
    img = make_text_image("SAMPLE DOCUMENT")
    create_resp = await client.post(
        "/documents/parse",
        files={"file": ("sample.png", img, "image/png")},
    )
    document_id = create_resp.json()["id"]

    resp = await client.get(f"/documents/{document_id}")

    assert resp.status_code == 200
    body = resp.json()
    assert body["id"] == document_id
    assert body["filename"] == "sample.png"


async def test_get_document_not_found(client):
    resp = await client.get("/documents/999999")

    assert resp.status_code == 404
