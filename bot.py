import os
import sys
from pathlib import Path

# Ensure project root is always at the top of sys.path on any platform or cloud provider
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Force UTF-8 stdout and stderr safely on all platforms
for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        except Exception:
            pass

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
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

async def handle_ping(request):
    return web.Response(
        text="Telegram Stars Bot is running 24/7! OK\n",
        content_type="text/plain"
    )

def create_web_app():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    app.router.add_get("/ping", handle_ping)
    return app

async def start_health_server():
    """
    Starts HTTP server immediately on 0.0.0.0:$PORT (default 10000).
    Render checks this port to verify the service is Live.
    """
    port_str = os.getenv("PORT", "10000")
    try:
        port = int(port_str)
    except ValueError:
        port = 10000

    print(f"[RENDER] Starting HTTP Health Server on port {port}...", flush=True)
    try:
        app = create_web_app()
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        print(f"[RENDER] [OK] HTTP Health Server is LIVE on 0.0.0.0:{port}!", flush=True)
        return runner
    except Exception as e:
        print(f"[RENDER WARNING] Could not bind port {port}: {e}", flush=True)
        return None

async def setup_bot_profile(bot: Bot):
    """
    Configure the Bot's Bio, Description and Command list in pure Uzbek.
    """
    try:
        desc_uz = (
            "🌟 Telegram Stars Ishlash Botiga xush kelibsiz!\n\n"
            "Do'stlaringizni taklif qiling va har bir do'stingiz uchun hisobingizga Telegram Stars oling! 💫\n\n"
            "Boshlash uchun pastdagi «Start» tugmasini bosing 👇"
        )
        bio_uz = "⭐ Do'stlarni taklif qilib Telegram Stars ishlang! Rasmiy Stars boti."
        name_uz = "⭐ STARS ISHLASH BOT"

        for lang_code in ["", "uz", "ru", "en"]:
            try:
                await bot.set_my_description(description=desc_uz, language_code=lang_code or None)
            except Exception:
                pass
            try:
                await bot.set_my_short_description(short_description=bio_uz, language_code=lang_code or None)
            except Exception:
                pass
            try:
                await bot.set_my_name(name=name_uz, language_code=lang_code or None)
            except Exception:
                pass

        commands = [
            BotCommand(command="start", description="Botni ishga tushirish"),
            BotCommand(command="stars", description="Stars ishlash"),
            BotCommand(command="profile", description="Profil va Hamyon"),
            BotCommand(command="leaderboard", description="Top Reyting"),
            BotCommand(command="language", description="Tilni tanlash"),
            BotCommand(command="help", description="Yordam"),
            BotCommand(command="admin", description="Admin Panel"),
        ]
        await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
        print("[BOT] [OK] Bot commands and profile updated in Uzbek successfully.", flush=True)
    except Exception as e:
        print(f"[BOT WARNING] Could not update profile/commands: {e}", flush=True)

async def run_bot_polling(bot: Bot, dp: Dispatcher):
    """
    Runs database init and Telegram bot polling loop with automatic reconnect.
    """
    print("[BOT] Initializing database...", flush=True)
    await db.init_db()
    print("[BOT] [OK] Database is ready.", flush=True)

    print("[BOT] Configuring profile...", flush=True)
    await setup_bot_profile(bot)

    try:
        bot_info = await bot.get_me()
        print(f"[BOT] Connected as @{bot_info.username} (ID: {bot_info.id})", flush=True)
    except Exception as e:
        print(f"[BOT WARNING] Could not fetch bot info: {e}", flush=True)

    while True:
        try:
            print("[BOT] Starting Telegram polling...", flush=True)
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)
        except Exception as e:
            print(f"[BOT POLLING ERROR] {e}. Reconnecting in 10 seconds...", flush=True)
            await asyncio.sleep(10)

async def main():
    print("========================================", flush=True)
    print("[START] TELEGRAM STARS BOT STARTING...", flush=True)
    print("========================================", flush=True)

    # 1. Start HTTP Server immediately so Render healthcheck succeeds instantly
    health_runner = await start_health_server()

    if not BOT_TOKEN:
        print("[FATAL] BOT_TOKEN environment variable is missing!", flush=True)
        while True:
            await asyncio.sleep(3600)

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    # 2. Run bot polling concurrently
    try:
        await run_bot_polling(bot, dp)
    finally:
        if health_runner:
            await health_runner.cleanup()
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("[STOP] Bot stopped.", flush=True)
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}", flush=True)
