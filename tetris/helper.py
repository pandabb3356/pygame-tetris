from typing import NamedTuple, Union


class Position(NamedTuple):
    x: Union[int, float]
    y: Union[int, float]

    def __add__(self, other: "Vector") -> "Position":
        return Position(self.x + other.x, self.y + other.y)


class Vector(NamedTuple):
    x: Union[int, float]
    y: Union[int, float]

    def __add__(self, vector: "Vector") -> "Vector":
        return Vector(self.x + vector.x, self.y + vector.y)

    def __sub__(self, vector: "Vector") -> "Vector":
        return Vector(self.x - vector.x, self.y - vector.y)

    def __mul__(self, value: int) -> "Vector":
        return Vector(self.x * value, self.y * value)

    def __bool__(self) -> bool:
        return False if (not self.x and not self.y) else True

    def __eq__(self, vector: "Vector") -> bool:
        return self.x == vector.x and self.y == vector.y

    def clone(self) -> "Vector":
        return Vector(*self)


class RGB(NamedTuple):
    r: int
    g: int
    b: int
