import asyncio
from datetime import datetime
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import ADMIN_IDS
from database.db import db
from locales.texts import t
from keyboards.inline import get_admin_keyboard, get_admin_channels_keyboard, get_admin_users_keyboard
from utils.excel import generate_users_excel

router = Router()

class AdminStates(StatesGroup):
    waiting_for_broadcast = State()
    waiting_for_channel = State()
    waiting_for_ref_reward = State()

def is_admin(user_id: int) -> bool:
    if ADMIN_IDS:
        return user_id in ADMIN_IDS
    return True

@router.message(F.text.in_(["🛠 Admin Panel", "🛠 Админ-панель", "🛠 Admin Control Panel"]) | Command("admin"))
async def cmd_admin(message: Message, state: FSMContext):
    await state.clear()
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.answer("❌ Bu buyruq faqat bot adminlari uchun!")
        return

    if user_id not in ADMIN_IDS:
        ADMIN_IDS.append(user_id)

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"
    stats = await db.get_admin_stats()

    await message.answer(
        t(
            "admin_title",
            lang=lang,
            total_users=stats["total_users"],
            total_stars=stats["total_stars"],
            total_txs=stats["total_txs"],
            vip_users=stats["vip_users"],
            channel_count=stats["channel_count"],
            ref_reward=stats["ref_reward"]
        ),
        parse_mode="HTML",
        reply_markup=get_admin_keyboard(lang, stats["ref_reward"])
    )

@router.callback_query(F.data == "admin_back")
async def cb_admin_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = callback.from_user.id
    if not is_admin(user_id):
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"
    stats = await db.get_admin_stats()

    await callback.message.edit_text(
        t(
            "admin_title",
            lang=lang,
            total_users=stats["total_users"],
            total_stars=stats["total_stars"],
            total_txs=stats["total_txs"],
            vip_users=stats["vip_users"],
            channel_count=stats["channel_count"],
            ref_reward=stats["ref_reward"]
        ),
        parse_mode="HTML",
        reply_markup=get_admin_keyboard(lang, stats["ref_reward"])
    )
    await callback.answer()

@router.callback_query(F.data == "admin_stats")
async def cb_admin_stats(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("Ruxsat berilmagan!", show_alert=True)
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"
    stats = await db.get_admin_stats()

    await callback.message.edit_text(
        t(
            "admin_title",
            lang=lang,
            total_users=stats["total_users"],
            total_stars=stats["total_stars"],
            total_txs=stats["total_txs"],
            vip_users=stats["vip_users"],
            channel_count=stats["channel_count"],
            ref_reward=stats["ref_reward"]
        ),
        parse_mode="HTML",
        reply_markup=get_admin_keyboard(lang, stats["ref_reward"])
    )
    await callback.answer("Statistika yangilandi!")

@router.callback_query(F.data == "admin_noop")
async def cb_admin_noop(callback: CallbackQuery):
    await callback.answer()

# Users List Browser (Pagination)
@router.callback_query(F.data.startswith("admin_users:"))
async def cb_admin_users(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("Ruxsat berilmagan!", show_alert=True)
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    page_str = callback.data.split(":")[1]
    page = int(page_str) if page_str.isdigit() else 1

    users_list, total_count, total_pages = await db.get_users_paginated(page=page, page_size=8)

    lines = []
    start_num = (page - 1) * 8 + 1
    for i, u in enumerate(users_list, start=start_num):
        uname = f"@{u['username']}" if u.get("username") else (u.get("full_name") or f"ID: {u['user_id']}")
        uname = uname.replace("<", "&lt;").replace(">", "&gt;")
        stars = u.get("balance_stars", 0) or 0
        refs = u.get("referrals_count", 0) or 0
        lines.append(
            f"<b>{i}. {uname}</b>\n"
            f"   🆔 <code>{u['user_id']}</code> | 💎 <b>{stars} ⭐</b> | 👥 <b>{refs} ref</b>"
        )

    users_formatted = "\n\n".join(lines) if lines else "Foydalanuvchilar mavjud emas."

    text = t(
        "admin_users_title",
        lang=lang,
        total_count=total_count,
        page=page,
        total_pages=total_pages,
        users_list=users_formatted
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_admin_users_keyboard(page, total_pages, lang)
    )
    await callback.answer()

# Export Users to Excel (.xlsx)
@router.callback_query(F.data == "admin_export_excel")
async def cb_admin_export_excel(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("Ruxsat berilmagan!", show_alert=True)
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    await callback.answer(t("excel_generating", lang), show_alert=False)

    users = await db.get_all_users_detailed()
    excel_file = generate_users_excel(users)

    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"users_{now_str}.xlsx"

    caption = t(
        "excel_caption",
        lang=lang,
        total_count=len(users),
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    document = BufferedInputFile(excel_file.read(), filename=filename)
    await callback.message.answer_document(
        document=document,
        caption=caption,
        parse_mode="HTML"
    )

# Referral Reward Configuration
@router.callback_query(F.data == "admin_set_ref_reward")
async def cb_admin_set_ref_reward(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("Ruxsat berilmagan!", show_alert=True)
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    await state.set_state(AdminStates.waiting_for_ref_reward)
    await callback.message.answer(
        t("prompt_set_ref_reward", lang),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_ref_reward)
async def process_set_ref_reward(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    text = message.text.strip()
    if not text.isdigit() or int(text) < 1:
        await message.answer(t("ref_reward_invalid", lang), parse_mode="HTML")
        return

    new_reward = int(text)
    await db.set_referral_reward(new_reward)
    await state.clear()

    stats = await db.get_admin_stats()
    await message.answer(
        t("ref_reward_updated", lang, reward=new_reward),
        parse_mode="HTML",
        reply_markup=get_admin_keyboard(lang, new_reward)
    )

# Channels Management
@router.callback_query(F.data == "admin_channels")
async def cb_admin_channels(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        return

    channels = await db.get_active_channels()
    text = (
        "📢 <b>Majburiy Obuna Kanallari</b>\n\n"
        "Foydalanuvchilar botdan foydalanishi uchun quyidagi kanallarga a'zo bo'lishi shart.\n"
        "<i>(Bot ushbu kanallarda admin bo'lishi kerak!)</i>"
    )
    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_admin_channels_keyboard(channels)
    )
    await callback.answer()

@router.callback_query(F.data == "add_channel")
async def cb_add_channel(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        return

    await state.set_state(AdminStates.waiting_for_channel)
    await callback.message.answer(
        "✍️ Yangi majburiy kanal username yoki ID sini kiriting (Masalan: <code>@mening_kanalim</code> yoki <code>-1001234567890</code>):",
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_channel)
async def process_add_channel(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    ch_text = message.text.strip()
    await db.add_channel(channel_id=ch_text)
    await state.clear()

    channels = await db.get_active_channels()
    await message.answer(
        f"✅ <b>{ch_text}</b> majburiy kanallar ro'yxatiga muvaffaqiyatli qo'shildi!",
        parse_mode="HTML",
        reply_markup=get_admin_channels_keyboard(channels)
    )

@router.callback_query(F.data.startswith("del_channel:"))
async def cb_del_channel(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        return

    channel_id = callback.data.split("del_channel:")[1]
    await db.delete_channel(channel_id)

    channels = await db.get_active_channels()
    await callback.message.edit_text(
        f"🗑 <b>{channel_id}</b> o'chirildi.\n\n📢 <b>Majburiy Kanallar:</b>",
        parse_mode="HTML",
        reply_markup=get_admin_channels_keyboard(channels)
    )
    await callback.answer("Kanal o'chirildi")

# Broadcast
@router.callback_query(F.data == "admin_broadcast")
async def cb_admin_broadcast(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    if not is_admin(user_id):
        await callback.answer("Ruxsat berilmagan!", show_alert=True)
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    await state.set_state(AdminStates.waiting_for_broadcast)
    await callback.message.answer(
        t("broadcast_prompt", lang),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(AdminStates.waiting_for_broadcast)
async def process_broadcast(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return

    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    await state.clear()
    status_msg = await message.answer(t("broadcast_started", lang))

    user_ids = await db.get_all_user_ids()
    success_count = 0
    fail_count = 0

    for uid in user_ids:
        try:
            await message.copy_to(chat_id=uid)
            success_count += 1
            await asyncio.sleep(0.05)
        except Exception:
            fail_count += 1

    await status_msg.edit_text(
        t("broadcast_finished", lang, success=success_count, failed=fail_count)
    )
