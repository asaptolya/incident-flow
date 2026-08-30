from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.incident import IncidentSeverity, IncidentStatus


class IncidentCreate(BaseModel):
    title: str
    description: str | None = None
    service: str
    severity: IncidentSeverity = IncidentSeverity.MEDIUM


class IncidentUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str | None
    service: str
    severity: IncidentSeverity
    status: IncidentStatus
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)