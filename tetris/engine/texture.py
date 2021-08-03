from typing import Generic, TypeVar, Set, Iterable

T = TypeVar("T")


class Texture(Generic[T]):
    # TODO: make more clearly
    """Texture of piece for each tile"""

    _pools: Set[T] = set()

    def __init__(self, content: T):
        self.content: T = content

    @classmethod
    def load_pools(cls, contents: Iterable[T]):
        for content in contents:
            cls._pools.add(content)

    @property
    def pools(self) -> Set[T]:
        return self._pools
