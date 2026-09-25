from urllib.parse import quote
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Dict, Any
from locales.texts import t

def get_language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz"),
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en"),
            ]
        ]
    )

def get_subscription_keyboard(unsubscribed_channels: List[Dict[str, Any]], lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = []
    for ch in unsubscribed_channels:
        title = ch.get("title") or ch.get("channel_id")
        link = ch.get("invite_link") or f"https://t.me/{ch['channel_id'].lstrip('@')}"
        buttons.append([
            InlineKeyboardButton(text=f"📢 {title}", url=link)
        ])
    
    buttons.append([
        InlineKeyboardButton(text=t("btn_check_sub", lang), callback_data="check_subscription")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_referral_keyboard(ref_link: str, lang: str = "uz") -> InlineKeyboardMarkup:
    share_text = t("share_text", lang)
    share_url = f"https://t.me/share/url?url={quote(ref_link)}&text={quote(share_text)}"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_share_ref", lang), url=share_url)
            ]
        ]
    )

def get_products_keyboard(products: List[Dict[str, Any]], lang: str = "uz") -> InlineKeyboardMarkup:
    buttons = []
    for p in products:
        buttons.append([
            InlineKeyboardButton(
                text=f"{p['title']} — {p['price_stars']} ⭐",
                callback_data=f"prod_view:{p['id']}"
            )
        ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_product_detail_keyboard(product_id: int, price: int, lang: str = "uz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t("btn_buy_stars", lang, price=price),
                    callback_data=f"prod_buy:{product_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=t("btn_back", lang),
                    callback_data="shop_back"
                )
            ]
        ]
    )

def get_donate_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⭐ 15", callback_data="donate_stars:15"),
                InlineKeyboardButton(text="⭐ 25", callback_data="donate_stars:25"),
                InlineKeyboardButton(text="⭐ 50", callback_data="donate_stars:50"),
            ],
            [
                InlineKeyboardButton(text="⭐ 100", callback_data="donate_stars:100"),
                InlineKeyboardButton(text="⭐ 250", callback_data="donate_stars:250"),
                InlineKeyboardButton(text="⭐️ 500", callback_data="donate_stars:500"),
            ],
            [
                InlineKeyboardButton(text="✍️ Boshqa miqdor (15 - 500 ⭐)", callback_data="donate_custom")
            ]
        ]
    )

def get_profile_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_my_history", lang), callback_data="my_history"),
            ]
        ]
    )

def get_admin_keyboard(lang: str = "uz", ref_reward: int = 1) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=t("btn_admin_stats", lang), callback_data="admin_stats"),
                InlineKeyboardButton(text=t("btn_users_list", lang), callback_data="admin_users:1"),
            ],
            [
                InlineKeyboardButton(text=t("btn_export_excel", lang), callback_data="admin_export_excel"),
                InlineKeyboardButton(text=t("btn_set_ref_reward", lang, reward=ref_reward), callback_data="admin_set_ref_reward"),
            ],
            [
                InlineKeyboardButton(text=t("btn_broadcast", lang), callback_data="admin_broadcast"),
                InlineKeyboardButton(text=t("btn_manage_channels", lang), callback_data="admin_channels"),
            ]
        ]
    )

def get_admin_users_keyboard(page: int, total_pages: int, lang: str = "uz") -> InlineKeyboardMarkup:
    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"admin_users:{page-1}"))
    
    nav_buttons.append(InlineKeyboardButton(text=f"📄 {page}/{total_pages}", callback_data="admin_noop"))
    
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"admin_users:{page+1}"))

    return InlineKeyboardMarkup(
        inline_keyboard=[
            nav_buttons,
            [
                InlineKeyboardButton(text=t("btn_export_excel", lang), callback_data="admin_export_excel")
            ],
            [
                InlineKeyboardButton(text=t("btn_back", lang), callback_data="admin_back")
            ]
        ]
    )

def get_admin_channels_keyboard(channels: List[Dict[str, Any]]) -> InlineKeyboardMarkup:
    buttons = []
    for ch in channels:
        buttons.append([
            InlineKeyboardButton(text=f"❌ O'chirish: {ch['channel_id']}", callback_data=f"del_channel:{ch['channel_id']}")
        ])
    buttons.append([
        InlineKeyboardButton(text="➕ Yangi kanal qo'shish", callback_data="add_channel"),
        InlineKeyboardButton(text="⬅️ Orqaga", callback_data="admin_back")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
