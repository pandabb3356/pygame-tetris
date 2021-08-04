from enum import Enum
from typing import Generic, Set, Iterable, Union

from tetris.engine.typing import (
    TextureContent,
    TextureTransform,
    type_of_texture_mapping,
)
from tetris.helper import RGB


class Texture(Generic[TextureContent, TextureTransform]):
    # TODO: make more clearly
    """Texture of piece for each tile"""

    pools: Set[TextureContent] = set()
    mapping: type_of_texture_mapping

    def __init__(self, content: TextureContent):
        self.content: TextureContent = content

    @classmethod
    def load_pools(cls, contents: Iterable[TextureContent]):
        cls.pools = set()
        for content in contents:
            cls.pools.add(content)

    @classmethod
    def load_mapping(cls, texture_mapping: type_of_texture_mapping):
        cls.mapping = texture_mapping

    @classmethod
    def transform(cls, content: TextureContent) -> TextureTransform:
        return cls.mapping[content]


class ColorContent(Enum):
    red = "red"
    blue = "blue"
    green = "green"
    yellow = "yellow"
    orange = "orange"
    purple = "purple"
    dark_blue = "dark_blue"
    dark_green = "dark_green"
    black = "black"
    white = "white"


class ColorTexture(Texture[Union[ColorContent, RGB], RGB]):
    mapping = {
        ColorContent.red: RGB(255, 0, 0),
        ColorContent.blue: RGB(0, 255, 0),
        ColorContent.dark_blue: RGB(20, 20, 40),
        ColorContent.green: RGB(0, 0, 255),
        ColorContent.dark_green: RGB(0, 128, 0),
        ColorContent.yellow: RGB(255, 255, 0),
        ColorContent.orange: RGB(255, 165, 0),
        ColorContent.purple: RGB(128, 0, 128),
        ColorContent.white: RGB(255, 255, 255),
        ColorContent.black: RGB(20, 20, 40),
    }
