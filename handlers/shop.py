from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
from database.db import db
from locales.texts import t
from keyboards.inline import get_products_keyboard, get_product_detail_keyboard

router = Router()

@router.message(F.text.in_(["🛍 Stars Do'koni", "🛍 Магазин Stars", "🛍 Stars Shop"]) | Command("shop"))
async def cmd_shop(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"
    products = await db.get_products()

    await message.answer(
        t("shop_title", lang),
        parse_mode="HTML",
        reply_markup=get_products_keyboard(products, lang)
    )

@router.callback_query(F.data == "shop_back")
async def cb_shop_back(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"
    products = await db.get_products()

    await callback.message.edit_text(
        t("shop_title", lang),
        parse_mode="HTML",
        reply_markup=get_products_keyboard(products, lang)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("prod_view:"))
async def cb_prod_view(callback: CallbackQuery):
    product_id = int(callback.data.split(":")[1])
    product = await db.get_product(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi / Товар не найден", show_alert=True)
        return

    user = await db.get_user(callback.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    text = t(
        "product_detail",
        lang=lang,
        title=product["title"],
        description=product["description"],
        price=product["price_stars"]
    )

    await callback.message.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=get_product_detail_keyboard(product_id, product["price_stars"], lang)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("prod_buy:"))
async def cb_prod_buy(callback: CallbackQuery, bot: Bot):
    product_id = int(callback.data.split(":")[1])
    product = await db.get_product(product_id)
    if not product:
        await callback.answer("Mahsulot topilmadi / Товар не найден", show_alert=True)
        return

    user = await db.get_user(callback.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    # Telegram Stars Invoice
    prices = [LabeledPrice(label=product["title"], amount=product["price_stars"])]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=t("invoice_title", lang, title=product["title"]),
        description=t("invoice_description", lang, description=product["description"][:240]),
        payload=f"shop_prod_{product['id']}_{callback.from_user.id}",
        provider_token="",  # Telegram Stars (XTR) requires empty provider_token
        currency="XTR",
        prices=prices,
        start_parameter=f"buy_prod_{product['id']}"
    )
    await callback.answer("To'lov oynasi ochilmoqda...")

# Pre-checkout query handler for Telegram Stars
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    # Always approve pre_checkout if conditions are met
    await pre_checkout_query.answer(ok=True)

# Successful payment handler
@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment = message.successful_payment
    payload = payment.invoice_payload
    user_id = message.from_user.id
    user = await db.get_user(user_id)
    lang = user.get("lang", "uz") if user else "uz"

    charge_id = payment.telegram_payment_charge_id
    total_stars = payment.total_amount

    if payload.startswith("shop_prod_"):
        parts = payload.split("_")
        prod_id = int(parts[2])
        product = await db.get_product(prod_id)
        prod_title = product["title"] if product else "Mahsulot"
        prod_content = product["content"] if product else "Rahmat!"

        # Save transaction
        await db.add_transaction(
            user_id=user_id,
            charge_id=charge_id,
            amount=total_stars,
            tx_type="shop_purchase",
            description=f"Xarid: {prod_title}"
        )

        # Update user spent stars & stats
        await db.add_spent_stars(user_id, total_stars)

        # Update VIP if applicable
        if product and product.get("category") == "vip":
            if "Ultra" in product["title"]:
                await db.set_user_vip(user_id, "VIP Ultra 💎", days=90)
            else:
                await db.set_user_vip(user_id, "VIP Pro 👑", days=30)

        await message.answer(
            t(
                "purchase_success",
                lang=lang,
                title=prod_title,
                amount=total_stars,
                charge_id=charge_id,
                content=prod_content
            ),
            parse_mode="HTML"
        )
