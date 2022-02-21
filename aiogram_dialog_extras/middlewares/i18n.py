from typing import Any, Optional

import aiogram.types as tg
from aiogram.contrib.middlewares.i18n import I18nMiddleware as _I18nMiddleware
from aiogram.dispatcher.middlewares import MiddlewareManager
from babel import Locale


class I18nMiddleware(_I18nMiddleware):
    def setup(self, manager: MiddlewareManager):
        super().setup(manager)
        manager.bot['_'] = self.gettext
        manager.bot['__'] = self.gettext

    def gettext(
        self, singular: str, plural: Optional[str] = None,
        n: int = 1, locale: Optional[str] = None,
    ) -> str:
        # Return an empty string if singular is empty, otherwise gettext will return its metadata
        if singular == '':
            return ''

        res = super().gettext(singular, plural, n, locale)

        if not isinstance(res, str):
            return res

        # Replace %% with % to avoid using precent symbol in a .pot file because its formatting
        return res.replace('%%', '%')

    # noinspection PyMethodMayBeStatic,PyUnusedLocal
    async def get_user_locale(self, action: str, args: tuple[Any]) -> str:
        """
        User locale getter

        :param action: event name
        :param args: event arguments
        :return: locale name or None
        """
        # Get current user

        user: Optional[tg.User] = tg.User.get_current()
        locale: Optional[Locale] = user.locale if user else None

        *_, data = args
        if locale and locale.language in self.locales:
            language = locale.language
        else:
            language = self.default

        data['locale'] = language
        data['i18n'] = self
        data['_'] = self.gettext
        data['__'] = self.gettext
        return language

    async def trigger(self, action, args):
        """
        Event trigger

        :param action: event name
        :param args: event arguments
        :return:
        """
        if (
            'update' not in action and
            # 'error' not in action and
            action.startswith('pre_process')
        ) or action == 'pre_process_aiogd_update':
            locale = await self.get_user_locale(action, args)
            self.ctx_locale.set(locale)
            return True
