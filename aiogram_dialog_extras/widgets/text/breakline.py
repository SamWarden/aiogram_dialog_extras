from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.when import WhenCondition


class Br(Const):
    def __init__(self, when: WhenCondition = None):
        super().__init__(' ', when)
