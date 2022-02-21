from typing import Awaitable, Callable, Optional, Union

from aiogram import Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.types import CallbackQuery, Message

ThrottlingHandler = Callable[[Message, Throttled], Awaitable[None]]


async def message_throttled(
    message: Union[Message, CallbackQuery], throttled: Throttled,
) -> None:
    if throttled.exceeded_count <= 2:
        await message.answer('Too many requests!')


# A simple middleware from an aiogram example
# https://github.com/aiogram/aiogram/blob/df294e579f104e2ae7e9f37b0c69490782d33091/examples/middleware_and_antiflood.py
class ThrottlingMiddleware(BaseMiddleware):
    def __init__(
        self, limit: float = DEFAULT_RATE_LIMIT,
        key_prefix: str = 'antiflood_', throttling_handler: Optional[ThrottlingHandler] = None,
    ):
        self.rate_limit = limit
        self.prefix = key_prefix
        if throttling_handler:
            self.throttling_handler = throttling_handler
        else:
            self.throttling_handler = message_throttled

        super().__init__()

    # noinspection PyUnusedLocal
    async def on_process_message(
        self, message: Message, data: dict,
    ) -> None:
        handler = current_handler.get()
        dp: Dispatcher = data['dispatcher']

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.throttling_handler(message, t)
            raise CancelHandler()

    async def on_process_callback_query(
        self, callback_query: CallbackQuery, data: dict,
    ) -> None:
        handler = current_handler.get()
        dp: Dispatcher = data['dispatcher']

        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_callback_query"
        try:
            await dp.throttle(key, rate=limit)
        except Throttled as t:
            await self.throttling_handler(callback_query, t)
            raise CancelHandler()
