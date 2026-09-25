from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from database.db import db
from locales.texts import t
from keyboards.inline import get_referral_keyboard

router = Router()

@router.message(F.text.in_([
    "⭐ Stars ishlash",
    "⭐ Заработать Stars",
    "⭐ Earn Stars",
    "👥 Do'stlarni taklif qilish (Referal)",
    "👥 Пригласить друзей (Рефералы)",
    "👥 Invite Friends (Referrals)"
]) | Command("stars", "earn", "ref", "referral", "invite"))
async def cmd_referral(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    if not user:
        user, _, _ = await db.get_or_create_user(user_id, message.from_user.username, message.from_user.full_name)

    lang = user.get("lang", "uz")
    ref_count = await db.get_referrals_count(user_id)
    balance = user.get("balance_stars", 0)
    reward = await db.get_referral_reward()

    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"

    ref_users = await db.get_referral_users(user_id, limit=5)
    recent_list = ""
    if ref_users:
        lines = []
        for ru in ref_users:
            uname = f"@{ru['username']}" if ru.get("username") else (ru.get("full_name") or f"ID: {ru['user_id']}")
            uname = uname.replace("<", "&lt;").replace(">", "&gt;")
            date = ru["created_at"].split()[0] if " " in ru["created_at"] else ru["created_at"]
            lines.append(f"• 👤 <b>{uname}</b> <i>({date})</i>")
        recent_list = "\n\n📋 <b>So'nggi taklif qilingan do'stlar:</b>\n" + "\n".join(lines)

    text = t(
        "referral_title",
        lang=lang,
        reward=reward,
        ref_count=ref_count,
        balance=balance,
        ref_link=ref_link
    ) + recent_list

    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_referral_keyboard(ref_link, lang)
    )
