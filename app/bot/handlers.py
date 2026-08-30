from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery

from app.core.database import AsyncSessionLocal
from app.models.incident import Incident, IncidentStatus


router = Router()


@router.callback_query(F.data.startswith("incident:ack:"))
async def acknowledge_incident(callback: CallbackQuery):
    incident_id = int(callback.data.split(":")[2])

    async with AsyncSessionLocal() as db:
        incident = await db.get(Incident, incident_id)

        if not incident:
            await callback.answer(
                "Incident not found",
                show_alert=True,
            )
            return

        if incident.status == IncidentStatus.RESOLVED:
            await callback.answer(
                "Incident is already resolved",
                show_alert=True,
            )
            return

        incident.status = IncidentStatus.ACKNOWLEDGED

        await db.commit()
        await db.refresh(incident)

    await callback.answer("Incident acknowledged")

    await callback.message.edit_text(
        callback.message.text.replace(
            "Status: open",
            "Status: acknowledged",
        ),
        reply_markup=callback.message.reply_markup,
    )


@router.callback_query(F.data.startswith("incident:resolve:"))
async def resolve_incident(callback: CallbackQuery):
    incident_id = int(callback.data.split(":")[2])

    async with AsyncSessionLocal() as db:
        incident = await db.get(Incident, incident_id)

        if not incident:
            await callback.answer(
                "Incident not found",
                show_alert=True,
            )
            return

        incident.status = IncidentStatus.RESOLVED
        incident.resolved_at = datetime.utcnow()

        await db.commit()

    await callback.answer("Incident resolved")

    await callback.message.edit_text(
        callback.message.text.replace(
            "Status: open",
            "Status: resolved",
        ).replace(
            "Status: acknowledged",
            "Status: resolved",
        )
    )