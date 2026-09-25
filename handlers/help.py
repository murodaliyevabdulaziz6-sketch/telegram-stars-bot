from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import db
from locales.texts import t

router = Router()

@router.message(F.text.in_(["ℹ️ Yordam & Ma'lumot", "ℹ️ Помощь и Инфо", "ℹ️ Help & Info"]) | Command("help"))
async def cmd_help(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    await message.answer(
        t("help_text", lang),
        parse_mode="HTML"
    )
