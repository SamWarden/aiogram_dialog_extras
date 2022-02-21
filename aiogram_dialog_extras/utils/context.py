from aiogram_dialog import DialogManager
from aiogram_dialog.context.context import Context

from aiogram_dialog_extras.exceptions import ContextNotFound


def get_context(manager: DialogManager) -> Context:
    context = manager.current_context()
    if context is None:
        raise ContextNotFound('Current context of this manager is None')

    return context
