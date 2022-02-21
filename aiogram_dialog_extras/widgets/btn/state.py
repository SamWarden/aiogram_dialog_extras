from typing import Any, Optional, Union, Sequence, Callable, Mapping

from aiogram.dispatcher.filters.state import State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.context.events import Data, StartMode
from aiogram_dialog.context.context import Context
from aiogram_dialog.widgets.kbd import Button, Cancel as _Cancel, Start as _Start
from aiogram_dialog.widgets.kbd.button import OnClick
from aiogram_dialog.widgets.text import Text, Const
from aiogram_dialog.widgets.when import WhenCondition

from aiogram_dialog_extras.manager.dialog import DialogResult
from aiogram_dialog_extras.utils.context import get_context

DataSelector = Callable[[dict], Data]


def get_merged_data(aiogd_context: Context) -> dict:
    if isinstance(aiogd_context.start_data, dict):
        data = aiogd_context.start_data
    else:
        data = {}

    if isinstance(aiogd_context.dialog_data, dict):
        data |= aiogd_context.dialog_data

    return data


def dict_selector(keys: Sequence) -> Callable[[Mapping], dict]:
    def _selector(data: Mapping) -> dict:
        return {key: data[key] for key in keys}
    return _selector


class Start(_Start):
    def __init__(self, text: Text, id: str, state: State,
                 data: Union[DataSelector, str, Sequence, Data] = None,
                 on_click: Optional[OnClick] = None,
                 mode: StartMode = StartMode.NORMAL,
                 when: WhenCondition = None):
        super(_Start, self).__init__(text, id, self._on_click, when)
        self.text = text

        if callable(data):
            self.selector: DataSelector = data
        elif isinstance(data, str):
            self.selector = dict_selector((data,))
        elif isinstance(data, Sequence):
            self.selector = dict_selector(data)
        else:
            self.selector = lambda _: data

        self.user_on_click = on_click
        self.state = state
        self.mode = mode

    async def _on_click(self, c: CallbackQuery, button: Button, manager: DialogManager):
        if self.user_on_click:
            await self.user_on_click(c, self, manager)

        aiogd_context = get_context(manager)
        data = get_merged_data(aiogd_context)
        start_data = self.selector(data)
        await manager.start(self.state, start_data, self.mode)


class Cancel(_Cancel):
    def __init__(self, text: Text = Const("Cancel"), id: str = "__cancel__",
                 result: Any = None,
                 on_click: Optional[Callable] = None,
                 when: WhenCondition = None):
        super(_Cancel, self).__init__(text, id, self._on_click, when)
        self.text = text

        if result is None:
            self.selector: DataSelector = lambda data: {}
        elif callable(result):
            self.selector = result
        elif isinstance(result, str):
            self.selector = dict_selector((result,))
        elif isinstance(result, Sequence):
            self.selector = dict_selector(result)
        else:
            self.selector = lambda _: result

        self.user_on_click = on_click

    async def _on_click(self, c: CallbackQuery, button: Button, manager: DialogManager):
        if self.user_on_click:
            await self.user_on_click(c, self, manager)

        current_state: State = manager.data['state']
        aiogd_context = get_context(manager)
        data = get_merged_data(aiogd_context)
        result = self.selector(data)

        await manager.done(DialogResult(current_state, result))
