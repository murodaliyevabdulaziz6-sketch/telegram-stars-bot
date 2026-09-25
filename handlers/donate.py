from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import MIN_STARS, MAX_STARS
from database.db import db
from locales.texts import t
from keyboards.inline import get_donate_keyboard

router = Router()

class DonateStates(StatesGroup):
    waiting_for_amount = State()

@router.message(F.text.in_(["⭐ Homiylik (Donate)", "⭐ Донат (Поддержка)", "⭐ Donate (Support)"]) | Command("donate"))
async def cmd_donate(message: Message, state: FSMContext):
    await state.clear()
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    await message.answer(
        t("donate_title", lang),
        parse_mode="HTML",
        reply_markup=get_donate_keyboard(lang)
    )

@router.callback_query(F.data.startswith("donate_stars:"))
async def cb_donate_stars(callback: CallbackQuery, bot: Bot):
    amount = int(callback.data.split(":")[1])
    if amount < MIN_STARS or amount > MAX_STARS:
        await callback.answer(f"Cheklov: {MIN_STARS} - {MAX_STARS} Stars", show_alert=True)
        return

    user = await db.get_user(callback.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    prices = [LabeledPrice(label=f"⭐ {amount} Stars Donation", amount=amount)]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=t("donate_invoice_title", lang),
        description=t("donate_invoice_desc", lang, amount=amount),
        payload=f"donate_{amount}_{callback.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter=f"donate_{amount}"
    )
    await callback.answer("Homiylik oynasi ochilmoqda...")

@router.callback_query(F.data == "donate_custom")
async def cb_donate_custom(callback: CallbackQuery, state: FSMContext):
    user = await db.get_user(callback.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    await state.set_state(DonateStates.waiting_for_amount)
    await callback.message.answer(
        t("donate_custom_prompt", lang),
        parse_mode="HTML"
    )
    await callback.answer()

@router.message(DonateStates.waiting_for_amount)
async def process_custom_amount(message: Message, state: FSMContext, bot: Bot):
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    text = message.text.strip()
    if not text.isdigit() or int(text) < MIN_STARS or int(text) > MAX_STARS:
        await message.answer(t("donate_invalid_amount", lang), parse_mode="HTML")
        return

    amount = int(text)
    await state.clear()

    prices = [LabeledPrice(label=f"⭐ {amount} Stars Donation", amount=amount)]

    await bot.send_invoice(
        chat_id=message.from_user.id,
        title=t("donate_invoice_title", lang),
        description=t("donate_invoice_desc", lang, amount=amount),
        payload=f"donate_{amount}_{message.from_user.id}",
        provider_token="",
        currency="XTR",
        prices=prices,
        start_parameter=f"donate_{amount}"
    )

# Successful payment handler for donations
@router.message(F.successful_payment, F.successful_payment.invoice_payload.startswith("donate_"))
async def process_donate_payment(message: Message):
    payment = message.successful_payment
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    charge_id = payment.telegram_payment_charge_id
    total_stars = payment.total_amount

    # Save transaction
    await db.add_transaction(
        user_id=user_id,
        charge_id=charge_id,
        amount=total_stars,
        tx_type="donation",
        description=f"Homiylik: {total_stars} Stars"
    )

    # Update user donated stats
    await db.add_donated_stars(user_id, total_stars)

    await message.answer(
        t(
            "donate_success",
            lang=lang,
            name=message.from_user.full_name,
            amount=total_stars
        ),
        parse_mode="HTML"
    )
