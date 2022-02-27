from operator import itemgetter
from typing import Callable, Union, Any, Sequence, Optional

from aiogram.types import InlineKeyboardButton
from aiogram_dialog.manager.manager import DialogManager
from aiogram_dialog.widgets.kbd.select import (
    Select as _Select, ItemIdGetter, OnItemClick,
)
from aiogram_dialog.widgets.text import Text
from aiogram_dialog.widgets.widget_event import WidgetEventProcessor

ItemUrlGetter = Callable[[Any], Optional[str]]


class Select(_Select):
    async def _render_keyboard(
        self, data: dict, manager: DialogManager,
    ) -> list[list[InlineKeyboardButton]]:
        # Additionaly filter buttons to return only a list of buttons with text
        return [[
            btn for pos, item in enumerate(self.items_getter(data))
            if (btn := await self._render_button(pos, item, data, manager)) and btn.text
        ]]

    async def _render_button(
        self, pos: int, item: Any, data: dict, manager: DialogManager,
    ) -> InlineKeyboardButton:
        data = {"data": data, "item": item, "pos": pos + 1, "pos0": pos}
        text = await self.text.render_text(data, manager)
        if not text:
            return InlineKeyboardButton(text='')

        return InlineKeyboardButton(
            text=text,
            callback_data=self.callback_data_prefix + str(self.item_id_getter(item))
        )


class SelectUrl(Select):
    def __init__(
        self, text: Text,
        id: str,
        item_id_getter: ItemIdGetter,
        items: Union[str, Sequence],
        item_url_getter: Optional[ItemUrlGetter] = None,
        on_click: Union[OnItemClick, WidgetEventProcessor, None] = None,
        when: Union[str, Callable] = None,
    ):
        super(_Select, self).__init__(id, item_id_getter, items, on_click, when)

        if isinstance(items, str):
            self.item_url_getter: ItemUrlGetter = itemgetter(items)
        elif callable(items):
            self.item_url_getter = item_url_getter
        else:
            self.item_url_getter = lambda item: None

    async def _render_button(
        self, pos: int, item: Any, data: dict, manager: DialogManager,
    ) -> InlineKeyboardButton:
        data = {"data": data, "item": item, "pos": pos + 1, "pos0": pos}
        text = await self.text.render_text(data, manager)
        if not text:
            return InlineKeyboardButton(text='')

        return InlineKeyboardButton(
            text=text,
            callback_data=self.callback_data_prefix + str(self.item_id_getter(item)),
            url=self.item_url_getter(item),
        )
