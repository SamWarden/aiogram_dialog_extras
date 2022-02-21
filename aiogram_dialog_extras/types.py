from typing import Optional, Protocol


class Gettext(Protocol):
    def __call__(self, singular: str, *, locale: Optional[str] = None) -> str:
        ...


class NGettext(Protocol):
    def __call__(
        self, singular: str, plural: Optional[str] = None, n: int = 1, locale: Optional[str] = None,
    ) -> str:
        ...
