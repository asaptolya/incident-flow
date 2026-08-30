from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.incidents import router as incidents_router
from app.core.config import settings
from app.core.database import engine
from app.api.events import router as events_router
from app.bot.bot import start_bot, stop_bot
import asyncio
from app.api.monitors import router as monitors_router
from app.services.monitor_service import monitor_loop

@asynccontextmanager
async def lifespan(app: FastAPI):
    bot_task = None

    if settings.TELEGRAM_BOT_TOKEN:
        bot_task = asyncio.create_task(
            start_bot()
        )

    monitor_task = asyncio.create_task(
        monitor_loop()
    )

    yield

    monitor_task.cancel()

    try:
        await monitor_task
    except asyncio.CancelledError:
        pass

    if bot_task:
        bot_task.cancel()

        try:
            await bot_task
        except asyncio.CancelledError:
            pass

        await stop_bot()

    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Incident monitoring and alert management system",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(incidents_router)
app.include_router(events_router)
app.include_router(monitors_router)

@app.get("/", tags=["Root"])
async def root():
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
    }
