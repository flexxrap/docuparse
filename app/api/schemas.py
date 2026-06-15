import datetime

from pydantic import BaseModel, ConfigDict


class DocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    filename: str
    raw_text: str
    doc_type: str | None
    parsed_data: dict | None
    created_at: datetime.datetime
