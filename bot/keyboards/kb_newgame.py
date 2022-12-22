from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from cbdata import ClickCallbackFactory


def menu_btns() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text="Правила", callback_data="help")
    keyboard.button(text="Начать игру", callback_data="new_game")
    return keyboard.as_markup()


def make_newgame_keyboard(game_id: str, cells: dict) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    for number, value in cells.items():
        btn = InlineKeyboardButton(text=value)
        btn.callback_data = ClickCallbackFactory(game_id=game_id, number=number).pack()
        keyboard.add(btn)
    keyboard.adjust(3)
    return keyboard.as_markup()


def make_replay_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="Еще раз", callback_data="new_game"))
    return keyboard.as_markup()
