from typing import Optional

from aiogram.contrib.middlewares.environment import EnvironmentMiddleware as _EnvironmentMiddleware


class EnvironmentMiddleware(_EnvironmentMiddleware):
    async def trigger(self, action: str, args: list[dict]) -> Optional[bool]:
        # Remove a condition to allow use this middleware before error handlers
        if action.startswith('pre_process_'):
            self.update_data(args[-1])
            return True
        return None
