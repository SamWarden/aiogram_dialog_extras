from dataclasses import dataclass
from typing import Any

from aiogram.dispatcher.filters.state import State


@dataclass
class DialogResult:
    state: State
    data: Any
