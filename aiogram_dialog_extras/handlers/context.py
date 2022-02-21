from typing import Callable, Optional

import aiogram.types as tg
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from aiogram_dialog_extras.utils import get_context


async def copy_start_data_to_ctx(_, dialog_manager: DialogManager) -> None:
    ctx = get_context(dialog_manager)
    if not isinstance(ctx.start_data, dict):
        raise TypeError('Context start_data is not a dict')

    ctx.dialog_data.update(ctx.start_data)


async def map_start_data_to_ctx(mapping: Optional[dict] = None) -> Callable:
    async def _map_start_data_to_ctx(_, dialog_manager: DialogManager) -> None:
        ctx = get_context(dialog_manager)
        if not isinstance(ctx.start_data, dict):
            raise TypeError('Context start_data is not a dict')

        if mapping is None:
            start_data = ctx.start_data
        else:
            start_data = {new_key: ctx.start_data[key] for new_key, key in mapping.items()}

        ctx.dialog_data.update(start_data)

    return _map_start_data_to_ctx


def clear_dialog_ctx(*keys: str) -> Callable:
    async def _clear_dialog_ctx(
        callback: tg.CallbackQuery, button: Button, manager: DialogManager,
    ) -> None:
        ctx = get_context(manager)
        for key in keys:
            if key in ctx.dialog_data:
                del ctx.dialog_data[key]

    return _clear_dialog_ctx
