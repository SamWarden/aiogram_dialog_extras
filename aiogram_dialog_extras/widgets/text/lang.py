from operator import itemgetter
from typing import Optional, Callable, Union

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.when import WhenCondition

from aiogram_dialog_extras.types import Gettext, NGettext

from .format import Format, ExtendedFormatter

NGetter = Callable[[dict], int]
_N = Union[int, str, NGetter]


class ExtendedLangFormatter(ExtendedFormatter):
    def __init__(self, gettext: Union[Gettext, NGettext]):
        super().__init__()
        self.gettext = gettext

    def convert_field(self, value, conversion) -> str:
        if conversion == 't':
            return self.gettext(str(value))

        return super().convert_field(value, conversion)


class Lang(Format):
    formatter = ExtendedLangFormatter

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        _: Gettext = manager.data['_']
        formatter = self.formatter(_)
        text = str(_(self.text))
        return formatter.convert_field(text, **data)


class NLang(Lang):
    def __init__(
        self, text: str, plural: Optional[str] = None, n: _N = 1,
        locale: Optional[str] = None, when: WhenCondition = None
    ):
        super().__init__(text, when)
        self.plural = plural
        self.locale = locale
        if isinstance(n, int):
            self.ngetter = lambda data: n
        elif isinstance(n, str):
            self.ngetter = itemgetter(n)
        else:
            self.ngetter = n

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        __: NGettext = manager.data['__']
        formatter = self.formatter(__)
        text = str(__(self.text, self.plural, self.ngetter(data), self.locale))
        return formatter.convert_field(text, **data)
