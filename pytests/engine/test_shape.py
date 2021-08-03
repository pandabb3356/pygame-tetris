from unittest import TestCase

from tetris.engine.shape import Shape, OShape


class TestShape(TestCase):
    def test_init(self):
        shape = Shape.init(0)
        assert shape.rot == 0

        o_shape = OShape.init(0)
        assert o_shape.rot == 0
