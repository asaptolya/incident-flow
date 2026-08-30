from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def incident_keyboard(incident_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Acknowledge",
                    callback_data=f"incident:ack:{incident_id}",
                ),
                InlineKeyboardButton(
                    text="✅ Resolve",
                    callback_data=f"incident:resolve:{incident_id}",
                ),
            ]
        ]
    )