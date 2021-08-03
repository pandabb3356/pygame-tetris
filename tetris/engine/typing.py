from typing import Callable, TypeVar

from tetris.helper import Factor

type_of_level = int
type_of_speed = float
type_of_count = int
type_of_score = int

type_of_speed_generator = Callable[[type_of_level, Factor], float]
type_of_accelerator = Callable[[type_of_speed, type_of_count, Factor], float]

TContent = TypeVar("TContent")
