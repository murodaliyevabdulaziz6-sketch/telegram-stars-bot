import os
import sys
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, BotCommandScopeDefault
from config import BOT_TOKEN
from database.db import db
from handlers import routers
from locales.texts import t

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def start_health_server():
    """
    Starts a light HTTP health server when deployed on Render / Koyeb (when PORT is provided).
    This keeps Render Free Web Service running 24/7 without port binding errors.
    """
    port_str = os.getenv("PORT")
    if not port_str:
        return

    try:
        port = int(port_str)
    except ValueError:
        return

    try:
        app = web.Application()

        async def handle_ping(request):
            return web.Response(text="⭐️ Telegram Stars Bot is running 24/7! OK")

        app.router.add_get("/", handle_ping)
        app.router.add_get("/health", handle_ping)

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"🌐 Health-check server successfully started on port {port}")
    except Exception as e:
        logger.error(f"❌ Failed to start health-check server: {e}", exc_info=True)

async def setup_bot_profile(bot: Bot):
    """
    Automatically configure the Bot's Bio, Description and Command list via Telegram Bot API.
    """
    try:
        # 1. Set Bot Short Description (Bio shown on profile)
        await bot.set_my_short_description(
            short_description=t("bot_bio", "uz")
        )
        logger.info("✅ Bot Bio (Short Description) updated successfully.")

        # 2. Set Bot Detailed Description (Shown before pressing Start)
        await bot.set_my_description(
            description=t("bot_description", "uz")
        )
        logger.info("✅ Bot Description updated successfully.")

        # 3. Set Bot Commands
        commands = [
            BotCommand(command="start", description="🚀 Botni ishga tushirish / Start"),
            BotCommand(command="stars", description="⭐ Stars ishlash / Earn Stars"),
            BotCommand(command="profile", description="👤 Profil & Hamyon / Profile"),
            BotCommand(command="leaderboard", description="🏆 Top Reyting / Leaderboard"),
            BotCommand(command="language", description="🌐 Tilni tanlash / Language"),
            BotCommand(command="help", description="ℹ️ Yordam / Help"),
            BotCommand(command="admin", description="🛠 Admin Panel"),
        ]
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
        logger.info("✅ Bot Commands menu updated successfully.")

    except Exception as e:
        logger.warning(f"⚠️ Error while setting bot profile: {e}")

async def on_startup(bot: Bot):
    logger.info("🚀 Database initsializatsiya qilinmoqda...")
    await db.init_db()
    logger.info("✅ Ma'lumotlar bazasi tayyor.")

    logger.info("⚙️ Bot profili va sozlamalari yangilanmoqda...")
    await setup_bot_profile(bot)

    bot_info = await bot.get_me()
    logger.info(f"🌟 Bot muvaffaqiyatli ishga tushdi: @{bot_info.username} (ID: {bot_info.id})")

async def main():
    logger.info("🚀 Bot tizimi ishga tushmoqda...")

    # Start health server immediately for Render
    await start_health_server()

    if not BOT_TOKEN or "TOKEN" in BOT_TOKEN:
        logger.error("❌ BOT_TOKEN topilmadi yoki noto'g'ri ko'rsatilgan (.env faylini tekshiring)!")
        if os.getenv("PORT"):
            logger.warning("⚠️ Web server ochiq saqlanadi, iltimos BOT_TOKEN ni sozlang.")
            while True:
                await asyncio.sleep(3600)
        return

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Register all routers
    for router in routers:
        dp.include_router(router)

    # Startup hook
    dp.startup.register(on_startup)

    try:
        # Delete webhook and start polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Polling xatosi: {e}", exc_info=True)
        if os.getenv("PORT"):
            while True:
                await asyncio.sleep(3600)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("🛑 Bot to'xtatildi.")
    except Exception as e:
        logger.critical(f"💥 Kritik xatolik: {e}", exc_info=True)
