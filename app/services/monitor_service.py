import asyncio
import time
from datetime import datetime

import httpx
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.incident import Incident, IncidentSeverity
from app.models.monitor import Monitor
from app.services.notification_service import NotificationService


async def check_monitor(monitor: Monitor):
    started_at = time.perf_counter()

    status_code = None
    is_up = False

    try:
        async with httpx.AsyncClient(
            timeout=10.0,
            follow_redirects=True,
        ) as client:
            response = await client.get(monitor.url)

        status_code = response.status_code

        is_up = 200 <= response.status_code < 400

    except httpx.HTTPError:
        is_up = False

    response_time = time.perf_counter() - started_at

    return is_up, status_code, response_time


async def process_monitor(monitor_id: int):
    async with AsyncSessionLocal() as db:
        monitor = await db.get(Monitor, monitor_id)

        if not monitor or not monitor.is_active:
            return

        previous_state = monitor.is_up

        is_up, status_code, response_time = await check_monitor(monitor)

        monitor.is_up = is_up
        monitor.last_status_code = status_code
        monitor.last_response_time = round(response_time, 3)
        monitor.last_checked_at = datetime.utcnow()

        incident = None

        if previous_state is True and is_up is False:
            incident = Incident(
                title=f"{monitor.name} is down",
                description=(
                    f"Monitor detected that {monitor.url} is unavailable. "
                    f"Status code: {status_code or 'connection failed'}"
                ),
                service=monitor.name,
                severity=IncidentSeverity.CRITICAL,
            )

            db.add(incident)

        await db.commit()

        if incident:
            await db.refresh(incident)
            await NotificationService.send_incident(incident)


async def monitor_loop():
    while True:
        async with AsyncSessionLocal() as db:
            result = await db.execute(
                select(Monitor).where(Monitor.is_active.is_(True))
            )

            monitors = result.scalars().all()

        for monitor in monitors:
            try:
                await process_monitor(monitor.id)
            except Exception as error:
                print(
                    f"Monitor {monitor.id} failed:",
                    error,
                )

        await asyncio.sleep(10)