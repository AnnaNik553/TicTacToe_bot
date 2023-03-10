from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware, html
from aiogram.dispatcher.flags.getter import get_flag
from aiogram.types import CallbackQuery

from cbdata import ClickCallbackFactory


class CheckActiveGameMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any],
    ) -> Any:
        """
        Check whether game is active. This middleware is intended for CallbackQuery only!
        """
        need_check_handler = get_flag(data, "need_check_game")
        if not need_check_handler:
            return await handler(event, data)
        state = data["state"]
        user_data = await state.get_data()
        fsm_game_id = user_data.get("game_id")
        if not fsm_game_id:
            await event.message.edit_text(
                text=f"{html.italic('Эта игра больше не доступна')}",
                reply_markup=None
            )
            return
        else:
            callback_data = data.get("callback_data")
            if isinstance(callback_data, ClickCallbackFactory):
                if callback_data.game_id != fsm_game_id:
                    await event.message.edit_text(
                        text=f"{html.italic('Эта игра больше не доступна')}",
                        reply_markup=None
                    )
                    await event.answer(
                        text="Эта игра недоступна, потому что уже есть новее!",
                        show_alert=True
                    )
                    return
        return await handler(event, data)
