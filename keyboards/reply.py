from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from locales.texts import t

def get_main_menu_keyboard(lang: str = "uz", is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text=t("btn_referral", lang))
        ],
        [
            KeyboardButton(text=t("btn_profile", lang)),
            KeyboardButton(text=t("btn_leaderboard", lang))
        ],
        [
            KeyboardButton(text=t("btn_language", lang)),
            KeyboardButton(text=t("btn_help", lang))
        ]
    ]

    if is_admin:
        buttons.append([KeyboardButton(text=t("btn_admin", lang))])

    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Menyudan tanlang..."
    )
