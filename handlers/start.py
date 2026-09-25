from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from config import ADMIN_IDS
from database.db import db
from locales.texts import t
from keyboards.reply import get_main_menu_keyboard
from keyboards.inline import get_language_keyboard, get_subscription_keyboard
from utils.subscription import check_user_subscription

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name

    # Check for referral parameter in /start ref_123456
    referrer_id = None
    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        ref_str = args[1].replace("ref_", "")
        if ref_str.isdigit():
            referrer_id = int(ref_str)

    user, is_new, reward_given = await db.get_or_create_user(
        user_id=user_id,
        username=username,
        full_name=full_name,
        referrer_id=referrer_id
    )

    # Notify referrer if a new user joined
    if is_new and referrer_id and referrer_id != user_id:
        ref_user = await db.get_user(referrer_id)
        if ref_user:
            ref_lang = ref_user.get("lang", "uz")
            try:
                await bot.send_message(
                    chat_id=referrer_id,
                    text=t("new_referral_notify", ref_lang, reward=reward_given),
                    parse_mode="HTML"
                )
            except Exception:
                pass

    lang = user.get("lang", "uz")
    is_admin = user_id in ADMIN_IDS

    # Check mandatory subscription
    is_subscribed, unsubscribed = await check_user_subscription(bot, user_id)
    if not is_subscribed:
        await message.answer(
            t("must_subscribe", lang),
            parse_mode="HTML",
            reply_markup=get_subscription_keyboard(unsubscribed, lang)
        )
        return

    welcome_text = t(
        "welcome",
        lang=lang,
        name=full_name,
        balance=user.get("balance_stars", 0),
        vip_status=user.get("vip_level", "Oddiy")
    )

    await message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(lang, is_admin)
    )

@router.callback_query(F.data == "check_subscription")
async def cb_check_subscription(callback: CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    is_subscribed, unsubscribed = await check_user_subscription(bot, user_id)
    if not is_subscribed:
        await callback.answer(t("sub_not_completed", lang), show_alert=True)
        return

    await callback.answer(t("sub_success", lang), show_alert=False)
    await callback.message.delete()

    is_admin = user_id in ADMIN_IDS

    welcome_text = t(
        "welcome",
        lang=lang,
        name=callback.from_user.full_name,
        balance=user.get("balance_stars", 0) if user else 0,
        vip_status=user.get("vip_level", "Oddiy") if user else "Oddiy"
    )

    await callback.message.answer(
        welcome_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(lang, is_admin)
    )

@router.message(F.text.in_(["🌐 Tilni o'zgartirish", "🌐 Сменить язык", "🌐 Change Language"]) | Command("language"))
async def cmd_language(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"
    await message.answer(
        t("lang_select", lang),
        parse_mode="HTML",
        reply_markup=get_language_keyboard()
    )

@router.callback_query(F.data.startswith("set_lang:"))
async def cb_set_language(callback: CallbackQuery):
    lang_code = callback.data.split(":")[1]
    user_id = callback.from_user.id

    await db.set_user_lang(user_id, lang_code)
    is_admin = user_id in ADMIN_IDS

    await callback.message.delete()
    await callback.message.answer(
        t("lang_changed", lang_code),
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard(lang_code, is_admin)
    )
    await callback.answer()
