from aiogram.dispatcher.filters.callback_data import CallbackData

class ClickCallbackFactory(CallbackData, prefix="click"):
    game_id: str
    number: int
