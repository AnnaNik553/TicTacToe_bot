from typing import Dict, List, Tuple, Union, Set
from aiogram.dispatcher.fsm.context import FSMContext
from uuid import uuid4
from random import randint, choice

from texttable import Texttable

HUM = 0
AI = 1

def get_game_start_settings():
    game_id = str(uuid4())
    cells = {}
    for x in range(1, 10):
        cells[x] = " "

    crosses, hum_figure, ai_figure = get_who_crosses()

    return hum_figure, ai_figure, crosses, game_id, cells

def get_who_crosses():
    # выбрать кто будет X
    crosses = randint(0, 1)

    if crosses == HUM:
        hum_figure = "❌"
        ai_figure = "⭕"

    if crosses == AI:
        hum_figure = "⭕"
        ai_figure = "❌"
    return crosses, hum_figure, ai_figure

def ai_move(cells, ai_figure, hum_figure):
    # выбор клетки для хода ИИ
    move_number = len([x for x in cells.values() if x == ai_figure])
    lines = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))

    if move_number == 0:
        if cells[5] == " ":
            cells[5] = ai_figure
            return
        else:
            random_cell = choice([1, 3, 7, 9])
            cells[random_cell] = ai_figure
            return
    if move_number == 1:
        # сначала ищем ряд с двумя крестиками и без ноликов
        # если его нет, ставим в любую угловую клетку
        combination = tuple(tuple(cells[x] for x in comb) for comb in lines)
        for i, comb in enumerate(combination):
            if ''.join(comb).strip() in (hum_figure + hum_figure, hum_figure + ' ' + hum_figure):
                line = lines[i]
                for num in line:
                    if cells[num] == " ":
                        cells[num] = ai_figure
                        return
        for num in (1, 3, 7, 9):
                if cells[num] == " ":
                    cells[num] = ai_figure
                    return
    if move_number >= 2:
        # сначала ищем ряд с двумя ноликами и без крестиков
        # если его нет, ищем ряд с двумя крестиками и без ноликов
        # если и его нет, ищем ряд с одним ноликом и без крестиков
        # если и такого нет, то ставим случайно
        combination = tuple(tuple(cells[x] for x in comb) for comb in lines)
        for i, comb in enumerate(combination):
            if ''.join(comb).strip() in (ai_figure + ai_figure, ai_figure + ' ' + ai_figure):
                line = lines[i]
                for num in line:
                    if cells[num] == " ":
                        cells[num] = ai_figure
                        return
        for i, comb in enumerate(combination):
            if ''.join(comb).strip() in (hum_figure + hum_figure, hum_figure + ' ' + hum_figure):
                line = lines[i]
                for num in line:
                    if cells[num] == " ":
                        cells[num] = ai_figure
                        return
        for i, comb in enumerate(combination):
            if ''.join(comb).strip() == ai_figure:
                line = lines[i]
                for num in line:
                    if cells[num] == " ":
                        cells[num] = ai_figure
                        return
        number_cell = randint(1, 9)
        while cells[number_cell] in ('❌', '⭕'):
            number_cell = randint(1, 9)
        if cells[number_cell] == " ":
            cells[number_cell] = ai_figure
            return


def check_to_win(cells, check_figure):
    # проверить на выйгрыш
    win_comb = ((1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (1, 5, 9), (3, 5, 7))
    combination = tuple(tuple(cells[x] for x in comb) for comb in win_comb)
    check_comb = (check_figure, check_figure, check_figure)
    return  check_comb in combination

def there_free_cells(cells):
    return bool(list(filter(lambda x: x == " ", cells.values())))

def make_text_table(cells: Dict) -> str:
    """
    Makes a text representation of game field using texttable library

    :param cells: dictionary with cells
    :return: a pretty-formatted field
    """
    table = Texttable()
    cells_size = 3
    table.set_cols_width([2] * cells_size)
    table.set_cols_align(["c"] * cells_size)

    data_rows = []
    data_single_row = []
    for cell in cells:
        data_single_row.append(cells[cell])
        if cell % 3 == 0:
            data_rows.append(data_single_row)
            data_single_row = []
    table.add_rows(data_rows, header=False)
    return f"<code>{table.draw()}</code>"


