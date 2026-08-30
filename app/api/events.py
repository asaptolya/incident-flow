from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.event import Event
from app.schemas.event import (
    EventCreate,
    EventResponse,
)
from app.services.incident_service import IncidentService
from app.services.notification_service import NotificationService


router = APIRouter(
    prefix="/api/events",
    tags=["Events"],
)


@router.post(
    "",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_event(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
):
    incident = await IncidentService.create_from_event(
        db=db,
        service=data.service,
        level=data.level,
        message=data.message,
    )

    event = Event(
        service=data.service,
        level=data.level.lower(),
        message=data.message,
        incident_id=incident.id,
    )

    db.add(event)

    await db.commit()
    await db.refresh(event)
    await db.refresh(incident)

    await NotificationService.send_incident(incident)

    return event