from fastapi import FastAPI

from app.api import documents

app = FastAPI(title="DocuParse")

app.include_router(documents.router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
