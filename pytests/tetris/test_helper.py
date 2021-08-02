from unittest import TestCase

from tetris.helper import Position, Vector


class TestPosition(TestCase):
    def test_add(self):
        result = Position(1, 0) + Vector(1, 1)

        assert (result.x, result.y) == (2, 1)

    def test_equal(self):
        assert Position(1, 0) == Position(1, 0)

    def test_subtraction(self):
        result = Position(1, 0) - Vector(1, 0)

        assert (result.x, result.y) == (0, 0)


class TestVector(TestCase):
    def test_add(self):
        result = Vector(1, 0) + Vector(1, 1)

        assert (result.x, result.y) == (2, 1)

    def test_subtraction(self):
        result = Vector(1, 0) - Vector(1, 1)

        assert (result.x, result.y) == (0, -1)

    def test_multiply(self):
        result = Vector(1, 2) * 30

        assert (result.x, result.y) == (30, 60)

    def test_bool(self):
        assert bool(Vector(1, 1)) is True
        assert bool(Vector(0, 0)) is False

    def test_equal(self):
        assert Vector(1, 2) == Vector(1, 2)

    def test_clone(self):
        assert Vector(1, 2).clone() == Vector(1, 2)


class TestRGB(TestCase):
    pass
