# DocuParse

OCR-сервис распознавания документов: принимает фото/скан документа (паспорт,
накладная, счёт), распознаёт текст через OCR и извлекает структурированные
поля в JSON. Имитирует кейс "фото документа -> данные в CRM".

## Status

- [ ] Phase 1 - OCR parsing, save/get results
- [ ] Phase 2 - per-document-type field extraction (passport/invoice/receipt)
- [ ] Phase 3 - CI/CD + final docs

## Stack

Python 3.12, FastAPI, EasyOCR, Pillow, PostgreSQL (SQLAlchemy async), pytest,
Docker.
