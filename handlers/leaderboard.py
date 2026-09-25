from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from database.db import db
from locales.texts import t

router = Router()

MEDALS = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

@router.message(F.text.in_(["🏆 Reyting", "🏆 Рейтинг", "🏆 Leaderboard"]) | Command("leaderboard", "top"))
async def cmd_leaderboard(message: Message):
    user = await db.get_user(message.from_user.id)
    lang = user.get("lang", "uz") if user else "uz"

    top_users = await db.get_top_referrers(limit=10)

    if not top_users:
        leaderboard_str = t("no_donors", lang)
    else:
        lines = []
        for i, u in enumerate(top_users):
            medal = MEDALS[i] if i < len(MEDALS) else f"#{i+1}"
            name = u.get("full_name") or (f"@{u['username']}" if u.get("username") else f"Foydalanuvchi {u['user_id']}")
            name = name.replace("<", "&lt;").replace(">", "&gt;")
            stars = u.get("balance_stars", 0)
            refs = u.get("referrals_count", 0)
            lines.append(f"{medal} <b>{name}</b> — <b>{stars} ⭐</b> <i>({refs} ta do'st)</i>")
        leaderboard_str = "\n".join(lines)

    await message.answer(
        t("leaderboard_title", lang, leaderboard=leaderboard_str),
        parse_mode="HTML"
    )
