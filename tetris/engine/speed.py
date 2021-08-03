from typing import Dict

from tetris.engine.typing import (
    type_of_level,
    type_of_speed,
    type_of_count,
    type_of_accelerator,
    type_of_speed_generator,
)
from tetris.helper import Factor


def speed_generator(level: type_of_level, factor: Factor) -> type_of_speed:
    return factor.a - level * factor.b


def linear_accelerator(
    start_speed: type_of_speed, count: type_of_count, factor: Factor
) -> type_of_speed:
    return start_speed - factor.a * count


def non_linear_accelerator(
    start_speed: type_of_speed, count: type_of_count, factor: Factor
) -> type_of_speed:
    return start_speed - factor.a * (count ** factor.b)


_accelerator_map: Dict[str, type_of_accelerator] = {
    "linear": linear_accelerator,
    "nonlinear": non_linear_accelerator,
}


def create_accelerator(_type: str) -> type_of_accelerator:
    return _accelerator_map.get(_type) or linear_accelerator


def create_speed_generator() -> type_of_speed_generator:
    return speed_generator
