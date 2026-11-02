import asyncio
import logging
import os
import threading

from aiogram import Dispatcher
from flask import Flask

from app.bot_instance import bot
from app.database.base import init_db
from app.handlers import admin as admin_handlers
from app.handlers import drugs as drugs_handlers
from app.handlers import register as register_handlers
from app.handlers import shartnoma as shartnoma_handlers
from app.handlers import spetsifikatsiya as spets_handlers
from app.handlers import start as start_handlers
from app.middlewares.auth import AuthMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Aiogram sozlamalari ---
dp = Dispatcher()
dp.message.middleware(AuthMiddleware())
dp.callback_query.middleware(AuthMiddleware())

dp.include_router(start_handlers.router)
dp.include_router(register_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(shartnoma_handlers.router)
dp.include_router(spets_handlers.router)
dp.include_router(drugs_handlers.router)


# --- Flask (Render uchun "health check") ---
web_app = Flask(__name__)


@web_app.route("/")
@web_app.route("/health")
def health():
    return "Bot is running", 200


def run_bot():
    """Telegram botni alohida oqimda ishga tushirish."""
    async def main():
        try:
            await init_db()
            # Webhook'ni o'chirib, eski xabarlarni tozalaymiz
            await bot.delete_webhook(drop_pending_updates=True)
            logger.info("Telegram bot polling boshlandi...")
            
            # handle_signals=False qo'shildi
            await dp.start_polling(
                bot,
                drop_pending_updates=True,
                handle_signals=False,
            )
        except Exception as e:
            logger.error(f"Bot ishga tushishda xato: {e}")

    asyncio.run(main())


if __name__ == "__main__":
    # Botni fonda ishga tushirish
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Flask serverni Render bergan PORT'da ishga tushirish
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Flask server {port}-portda ishga tushmoqda...")
    web_app.run(host="0.0.0.0", port=port)
