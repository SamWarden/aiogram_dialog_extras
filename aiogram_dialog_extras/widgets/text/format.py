from string import Formatter
from typing import ClassVar, Type

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format as _Format
from aiogram_dialog.widgets.when import WhenCondition


class ExtendedFormatter(Formatter):
    """An extended format string formatter

    Formatter with extended conversion symbol
    """
    def convert_field(self, value, conversion) -> str:
        """ Extend conversion symbol
        Following additional symbol has been added
        * l: convert to string and low case
        * u: convert to string and up case
        * c: convert to string and capitalize
        * d: format datetime

        default are:
        * s: convert with str()
        * r: convert with repr()
        * a: convert with ascii()
        """

        if conversion == 'u':
            return str(value).upper()
        elif conversion == 'l':
            return str(value).lower()
        elif conversion == 'c':
            return str(value).capitalize()
        elif conversion == 'd':
            try:
                return value.strftime('%Y-%m-%d %H:%M%Z')
            except AttributeError:
                return ''

        # Do the default conversion or raise error if no matching conversion found
        return super().convert_field(value, conversion)


class Format(_Format):
    formatter: ClassVar[Type[Formatter]] = ExtendedFormatter

    def __init__(self, text: str, when: WhenCondition = None):
        super().__init__(text, when)

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        formatter = self.formatter()
        return formatter.format(self.text, **data)
