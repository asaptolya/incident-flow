from aiogram import Bot

from app.bot.keyboards import incident_keyboard
from app.core.config import settings
from app.models.incident import Incident


class NotificationService:
    @staticmethod
    async def send_incident(incident: Incident) -> None:
        if not settings.TELEGRAM_BOT_TOKEN:
            return

        if not settings.TELEGRAM_CHAT_ID:
            return

        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

        text = (
            f"🚨 <b>{incident.severity.value.upper()} INCIDENT</b>\n\n"
            f"<b>Service:</b> {incident.service}\n"
            f"<b>Incident:</b> #{incident.id}\n\n"
            f"{incident.description or incident.title}\n\n"
            f"<b>Status:</b> {incident.status.value}"
        )

        try:
            await bot.send_message(
                chat_id=settings.TELEGRAM_CHAT_ID,
                text=text,
                parse_mode="HTML",
                reply_markup=incident_keyboard(incident.id),
            )
        finally:
            await bot.session.close()