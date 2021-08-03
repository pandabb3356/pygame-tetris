from typing import Generic, Set, Iterable

from tetris.engine.typing import TContent


class Texture(Generic[TContent]):
    # TODO: make more clearly
    """Texture of piece for each tile"""

    pools: Set[TContent]

    def __init__(self, content: TContent):
        self.content: TContent = content

    @classmethod
    def load_pools(cls, contents: Iterable[TContent]):
        cls.pools = set()
        for content in contents:
            cls.pools.add(content)
