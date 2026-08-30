from sqlalchemy.ext.asyncio import AsyncSession

from app.models.incident import (
    Incident,
    IncidentSeverity,
)


class IncidentService:

    @staticmethod
    async def create_from_event(
        db: AsyncSession,
        service: str,
        level: str,
        message: str,
    ) -> Incident:

        severity_map = {
            "info": IncidentSeverity.LOW,
            "warning": IncidentSeverity.MEDIUM,
            "error": IncidentSeverity.HIGH,
            "critical": IncidentSeverity.CRITICAL,
        }

        severity = severity_map.get(
            level.lower(),
            IncidentSeverity.MEDIUM,
        )

        incident = Incident(
            title=message[:255],
            description=message,
            service=service,
            severity=severity,
        )

        db.add(incident)

        await db.flush()

        return incident