from typing import Type

from tetris.helper import Position, Vector
from .shape import (
    Shape,
    OShape,
    LShape,
    JShape,
    SShape,
    ZShape,
    TShape,
    IShape,
)
from .texture import Texture
from .typing import TextureContent


class Piece:
    SHAPES = (
        OShape,
        LShape,
        JShape,
        SShape,
        ZShape,
        TShape,
        IShape,
    )

    _shape: Shape
    _texture: Texture
    _rot: int
    _collapsed: bool

    def __init__(
        self,
        x: float,
        y: float,
        shape_cls: Type[Shape],
        content: TextureContent,
        rot: int = 0,
    ):
        self.x = x
        self.y = y

        self._shape = shape_cls.init(rot=rot)
        self._texture = Texture(content)
        self._rot = rot
        self._shape.rot = rot
        self._collapsed = False

    def move(self, vector: Vector) -> "Piece":
        pos = self.position + vector
        return Piece(
            pos.x, pos.y, self._shape.__class__, self.texture.content, self.rot
        )

    def __iter__(self):
        for i, j in self.shape:
            yield self.position + Vector(i, j)

    @property
    def position(self) -> Position:
        return Position(self.x, self.y)

    @property
    def collapsed(self) -> bool:
        return self._collapsed

    @collapsed.setter
    def collapsed(self, v: bool):
        self._collapsed = v

    @property
    def shape(self) -> Shape:
        return self._shape

    @property
    def texture(self) -> Texture:
        return self._texture

    @property
    def rot(self) -> int:
        return self._rot

    def rotate(self, rot: int):
        rot = (self._rot + rot) % 4
        self._rot = self.shape.rot = rot
