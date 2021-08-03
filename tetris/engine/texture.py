from typing import Generic, TypeVar, Set, Iterable

T = TypeVar("T")


class Texture(Generic[T]):
    # TODO: make more clearly
    """Texture of piece for each tile"""

    pools: Set[T]

    def __init__(self, content: T):
        self.content: T = content

    @classmethod
    def load_pools(cls, contents: Iterable[T]):
        cls.pools = set()
        for content in contents:
            cls.pools.add(content)
