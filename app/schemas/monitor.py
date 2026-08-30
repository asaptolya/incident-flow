from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class MonitorCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    url: HttpUrl

    interval: int = Field(
        default=60,
        ge=10,
        le=3600,
    )


class MonitorResponse(BaseModel):
    id: int
    name: str
    url: str
    interval: int
    is_active: bool
    is_up: bool | None
    last_status_code: int | None
    last_response_time: float | None
    last_checked_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
