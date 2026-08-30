from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventCreate(BaseModel):
    service: str = Field(
        min_length=2,
        max_length=100,
        examples=["payment-api"],
    )

    level: str = Field(
        examples=["critical"],
    )

    message: str = Field(
        min_length=3,
        examples=["Database connection failed"],
    )


class EventResponse(BaseModel):
    id: int
    service: str
    level: str
    message: str
    incident_id: int | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)