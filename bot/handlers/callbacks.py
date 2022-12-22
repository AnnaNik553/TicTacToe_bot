from contextlib import suppress
from uuid import uuid4
from random import randint

from aiogram import types, Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest


from cbdata import ClickCallbackFactory
from keyboards.kb_newgame import make_newgame_keyboard, make_replay_keyboard
from tictactoe.game import get_game_start_settings, ai_move, make_text_table, check_to_win, there_free_cells


router = Router()
HUM = 0
AI = 1


@router.callback_query(text="help")
async def callback_help(call: types.CallbackQuery):
    text = f"Правила игры: \nПобеждает игрок, построивший линию из 3 фигур в ряд" \
           f"(горизонтально, вертикально или по диагонали)."
    await call.message.answer(text=text)
    await call.answer()


@router.callback_query(text="new_game")
async def callback_newgame(call: types.CallbackQuery, state: FSMContext):
    hum_figure, ai_figure, crosses, game_id, cells = get_game_start_settings()

    if crosses == AI:
        ai_move(cells, ai_figure, hum_figure)

    newgame_dict = {"game_id": game_id, "crosses": crosses, "hum_figure": hum_figure, "ai_figure": ai_figure, "cells": cells}
    await state.set_data(newgame_dict)

    text = f"Ход: {call.message.chat.first_name} {hum_figure} \n\nХод: ИИ {ai_figure}\n"
    kb = make_newgame_keyboard(game_id, cells)
    await call.message.answer(text=text, reply_markup=kb)
    await call.answer()


@router.callback_query(ClickCallbackFactory.filter(), flags={"need_check_game": True})
async def callback_motion(call: types.CallbackQuery, state: FSMContext,
                               callback_data: ClickCallbackFactory):
    """
    Called when the player has pressed the button of the playing field
    """
    fsm_data = await state.get_data()
    game_id = fsm_data.get("game_id")
    cells = fsm_data.get("cells", {})
    crosses = fsm_data.get("crosses")
    hum_figure = fsm_data.get("hum_figure")
    ai_figure = fsm_data.get("ai_figure")

    x: int = callback_data.number

    # проверить свободна ли клетка
    if cells[x] == " ":
        cells[x] = hum_figure
    else:
        await call.answer()
        return

    # проверить на выйгрыш человека
    if check_to_win(cells, hum_figure):
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f"{call.message.chat.first_name} {hum_figure} \nИИ {ai_figure}"
                f"\n\n{make_text_table(cells)}\n\n<b>Вы выйграли!</b> 🎉",
                reply_markup=make_replay_keyboard()
            )
            await call.answer()
            return

    # проверить на свободные клетки
    if not there_free_cells(cells):
        # ничья
        with suppress(TelegramBadRequest):
            await call.message.edit_text(
                f"{call.message.chat.first_name} {hum_figure} \nИИ {ai_figure}"
                f"\n\n{make_text_table(cells)}\n\n<b>Ничья</b>",
                reply_markup=make_replay_keyboard()
            )
            await call.answer()
            return

    # сходить ИИ если есть свободные клетки
    if there_free_cells(cells):
        ai_move(cells, ai_figure, hum_figure)

        # проверить на выйгрыш ИИ
        if check_to_win(cells, ai_figure):
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"{call.message.chat.first_name} {hum_figure} \nИИ {ai_figure}"
                    f"\n\n{make_text_table(cells)}\n\n<b>Вы проиграли!</b> 😞",
                    reply_markup=make_replay_keyboard()
                )
                await call.answer()
                return

        # проверить на свободные клетки
        if not there_free_cells(cells):
            # ничья
            with suppress(TelegramBadRequest):
                await call.message.edit_text(
                    f"{call.message.chat.first_name} {hum_figure} \nИИ {ai_figure}"
                    f"\n\n{make_text_table(cells)}\n\n<b>Ничья</b>",
                    reply_markup=make_replay_keyboard()
                )
                await call.answer()
                return

        # если игра не окончена после хода ии, сохраняем новые данные
        await state.update_data(cells=cells)
        with suppress(TelegramBadRequest):
            await call.message.edit_reply_markup(
                make_newgame_keyboard(game_id, cells)
            )
        await call.answer()

    await call.answer(cache_time=2)
