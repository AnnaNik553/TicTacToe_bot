from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hide_link
from aiogram.dispatcher.fsm.context import FSMContext

from keyboards.kb_newgame import menu_btns, make_newgame_keyboard
from tictactoe.game import get_game_start_settings, ai_move


router = Router()
HUM = 0
AI = 1


@router.message(commands=["start"])
async def cmd_start(message: Message):
    await message.answer(
        f"{hide_link('https://media.istockphoto.com/photos/tic-tac-toe-picture-id172445550?b=1&k=20&m=172445550&s=170667a&w=0&h=PrWp46npSKfiKT2KHzevBMHc99BNtzBt5Vl0R9ijDX4=')}"
        "Игра Крестики-нолики - постройте линию из фигур раньше соперника.\n",
        reply_markup=menu_btns()
    )


@router.message(commands=["new_game"])
async def cmd_new_game(message: Message, state: FSMContext):
    hum_figure, ai_figure, crosses, game_id, cells = get_game_start_settings()

    if crosses == AI:
        ai_move(cells, ai_figure, hum_figure)

    newgame_dict = {"game_id": game_id, "crosses": crosses, "hum_figure": hum_figure, "ai_figure": ai_figure, "cells": cells}
    await state.set_data(newgame_dict)

    await message.answer(
        f"Ход: {message.from_user.first_name} {hum_figure} \n\nХод: ИИ {ai_figure}\n",
        reply_markup=make_newgame_keyboard(game_id, cells)
    )

@router.message(commands=["help"])
async def cmd_help(message: Message):
    await message.answer("Правила игры: \nПобеждает игрок, построивший линию из 3 фигур в ряд"
                         " (горизонтально, вертикально или по диагонали).")
