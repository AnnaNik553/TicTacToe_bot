from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_commands(bot: Bot):
    data = [
        (
            [
                BotCommand(command="start", description="Приветствие"),
                BotCommand(command="new_game", description="Начать новую игру"),
                BotCommand(command="help", description="Правила игры в крестики-нолики"),
            ],
            BotCommandScopeAllPrivateChats()
        )
    ]
    for commands_list, commands_scope in data:
        await bot.set_my_commands(commands=commands_list, scope=commands_scope)
