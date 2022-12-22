import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from magic_filter import F

from commands import set_commands
from config_reader import config
from handlers import default_commands, callbacks
from middlewares.check_active_game import CheckActiveGameMiddleware


async def main():
    # Logging to stdout
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    session = AiohttpSession(proxy="http://proxy.server:3128/")

    # Creating bot and its dispatcher
    bot = Bot(token=config.bot_token.get_secret_value(), session=session, parse_mode="HTML")

    dp = Dispatcher()

    # Allow interaction in private chats (not groups or channels) only
    dp.message.filter(F.chat.type == "private")

    # Register middlewares
    dp.callback_query.middleware(CheckActiveGameMiddleware())

    dp.include_router(default_commands.router)
    dp.include_router(callbacks.router)

    # Register /-commands in UI
    await set_commands(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())
