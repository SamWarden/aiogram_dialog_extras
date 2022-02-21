from operator import itemgetter
from typing import Optional, Callable, Union

from aiogram_dialog import DialogManager
from aiogram_dialog.manager.protocols import MediaAttachment
from aiogram_dialog.widgets.media import Media
from aiogram_dialog.widgets.when import WhenCondition

MediaSelector = Callable[[dict], MediaAttachment]


class DynamicMedia(Media):
    def __init__(
        self,
        selector: Union[str, MediaSelector],
        when: WhenCondition = None,
    ):
        super().__init__(when)
        if isinstance(selector, str):
            self.selector: MediaSelector = itemgetter(selector)
        else:
            self.selector = selector

    async def _render_media(self, data: dict, manager: DialogManager) -> Optional[MediaAttachment]:
        media: Optional[MediaAttachment] = self.selector(data)
        return media
