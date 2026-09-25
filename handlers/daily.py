from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import db
from locales.texts import t

router = Router()

@router.message(F.text.in_(["📅 Kunlik Bonus", "📅 Ежедневный бонус", "📅 Daily Bonus"]) | Command("bonus", "daily"))
async def cmd_daily_bonus(message: Message):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    if not user:
        user = await db.get_or_create_user(user_id, message.from_user.username, message.from_user.full_name)

    lang = user.get("lang", "uz")

    can_claim, bonus_amount, streak, rem_h, rem_m = await db.claim_daily_bonus(user_id)

    if can_claim:
        await message.answer(
            t("daily_claimed", lang=lang, amount=bonus_amount, streak=streak),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            t("daily_already_claimed", lang=lang, remaining_hours=rem_h, remaining_mins=rem_m),
            parse_mode="HTML"
        )
