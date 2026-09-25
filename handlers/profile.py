from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from database.db import db
from locales.texts import t
from keyboards.inline import get_profile_keyboard

router = Router()

@router.message(F.text.in_(["👤 Profil & Hamyon", "👤 Профиль и Кошелек", "👤 Profile & Wallet"]) | Command("profile", "wallet", "me"))
async def cmd_profile(message: Message, bot: Bot):
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    if not user:
        user, _, _ = await db.get_or_create_user(user_id, message.from_user.username, message.from_user.full_name)

    lang = user.get("lang", "uz")
    ref_count = await db.get_referrals_count(user_id)
    bot_info = await bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start=ref_{user_id}"

    profile_msg = t(
        "profile_text",
        lang=lang,
        user_id=user_id,
        name=user.get("full_name") or message.from_user.full_name,
        balance=user.get("balance_stars", 0),
        vip_status=user.get("vip_level", "Oddiy"),
        total_spent=user.get("total_spent", 0),
        ref_count=ref_count,
        created_at=user.get("created_at", "Noma'lum"),
        ref_link=ref_link
    )

    await message.answer(
        profile_msg,
        parse_mode="HTML",
        reply_markup=get_profile_keyboard(lang)
    )

@router.callback_query(F.data == "my_history")
async def cb_my_history(callback: CallbackQuery):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    txs = await db.get_user_transactions(user_id, limit=10)
    if not txs:
        await callback.answer(t("no_history", lang), show_alert=True)
        return

    history_lines = []
    for tx in txs:
        date_str = tx["created_at"].split()[0] if " " in tx["created_at"] else tx["created_at"]
        history_lines.append(f"• <b>{tx['amount']} ⭐</b> — {tx['description']} <i>({date_str})</i>")

    history_text = t("history_title", lang, history="\n".join(history_lines))

    await callback.message.answer(history_text, parse_mode="HTML")
    await callback.answer()
