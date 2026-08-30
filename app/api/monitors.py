from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.monitor import Monitor
from app.schemas.monitor import (
    MonitorCreate,
    MonitorResponse,
)


router = APIRouter(
    prefix="/api/monitors",
    tags=["Monitors"],
)


@router.post(
    "",
    response_model=MonitorResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_monitor(
    data: MonitorCreate,
    db: AsyncSession = Depends(get_db),
):
    monitor = Monitor(
        name=data.name,
        url=str(data.url),
        interval=data.interval,
    )

    db.add(monitor)

    await db.commit()
    await db.refresh(monitor)

    return monitor


@router.get(
    "",
    response_model=list[MonitorResponse],
)
async def get_monitors(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Monitor).order_by(Monitor.created_at.desc())
    )

    return result.scalars().all()


@router.get(
    "/{monitor_id}",
    response_model=MonitorResponse,
)
async def get_monitor(
    monitor_id: int,
    db: AsyncSession = Depends(get_db),
):
    monitor = await db.get(Monitor, monitor_id)

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found",
        )

    return monitor


@router.delete(
    "/{monitor_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_monitor(
    monitor_id: int,
    db: AsyncSession = Depends(get_db),
):
    monitor = await db.get(Monitor, monitor_id)

    if not monitor:
        raise HTTPException(
            status_code=404,
            detail="Monitor not found",
        )

    await db.delete(monitor)
    await db.commit()
