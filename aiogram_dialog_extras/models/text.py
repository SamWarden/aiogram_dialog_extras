from dataclasses import dataclass, field
from typing import TypeVar, Generic, Sequence

PositionalData = TypeVar('PositionalData')


@dataclass
class PositionalVM(Generic[PositionalData]):
    pos0: int
    data: PositionalData
    pos: int = field(init=False)

    def __post_init__(self):
        self.pos = self.pos0 + 1

    @classmethod
    def from_iter(cls, items: Sequence[PositionalData]) -> 'list[PositionalVM[PositionalData]]':
        return [PositionalVM(i, data) for i, data in enumerate(items)]
