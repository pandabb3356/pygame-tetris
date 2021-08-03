from unittest import TestCase, mock

from tetris.engine.piece import Piece
from tetris.engine.shape import Shape
from tetris.engine.texture import Texture
from tetris.helper import Position, Vector


class TestPiece(TestCase):
    def setUp(self) -> None:
        self.position = Position(0, 0)
        self.texture = mock.MagicMock(spec=Texture)
        self.content = "content"
        self.shape_cls = mock.MagicMock()
        self.shape = mock.MagicMock(spec=Shape, rot=0)

    def test_init(self):
        piece = Piece(
            self.position.x,
            self.position.y,
            Shape,
            self.content,
        )

        assert piece.position == self.position
        assert piece.rot == 0
        assert piece.collapsed is False
        assert piece.texture.content == self.content
        assert isinstance(piece.shape, Shape) is True

    def test_move(self):
        piece = Piece(
            self.position.x,
            self.position.y,
            Shape,
            self.content,
        )

        vector = Vector(1, 0)

        moved_piece = piece.move(vector)

        assert moved_piece.position == self.position + vector

    def test_iter(self):
        def shape_iterator(*args, **kwargs):
            for i in range(4):
                yield Vector(i, i)

        self.shape.__iter__ = shape_iterator

        piece = Piece(
            self.position.x,
            self.position.y,
            Shape,
            self.content,
        )

        for vi, vec in enumerate(piece):
            assert vec == (piece.position + Vector(vi, vi))

    def test_rotate(self):
        self.shape.rot = 0
        piece = Piece(
            self.position.x,
            self.position.y,
            Shape,
            self.content,
            rot=0,
        )

        piece.rotate(2)
        assert piece.rot == 2
        assert piece.shape.rot == 2

        piece.rotate(8)
        assert piece.rot == 2
        assert piece.shape.rot == 2
