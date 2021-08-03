from .base import Scene, SceneParameter
from ..engine.board import Board
from ..engine.speed import create_accelerator, Factor, create_speed_generator
from ..engine.typing import (
    type_of_level,
    type_of_score,
    type_of_speed,
    type_of_count,
    type_of_accelerator,
    type_of_speed_generator,
)


class Tetris(Scene):
    """Tetris scene"""

    BLOCK_SIZE: int = 30
    N_ROWS: int = 10
    N_COLS: int = 20
    INIT_LEVEL: int = 1

    ACCELERATOR_TYPE: str = "linear"
    ACCELERATOR_FACTOR: Factor = Factor(a=1.0)
    SPEED_FACTOR: Factor = Factor(a=1.0, b=0.05)

    _board: Board

    _level: type_of_level
    _score: type_of_score

    _falling_speed: type_of_speed
    _fall_time: float

    _game_over: bool

    _accelerate_count: type_of_count

    def init(self):
        """Initialize"""
        self.reset()
        self._board = Board()

    def reset(self):
        """Reset Tetris"""
        self.reset_score()
        self.set_level(self.INIT_LEVEL)

        self.reset_falling_speed()
        self.reset_fall_time()

        self._game_over = False

        self.reset_accelerate_count()

    def accelerate(self):
        """Accelerate the falling speed"""
        accelerator = create_accelerator(self.ACCELERATOR_TYPE)
        accelerator(
            self._falling_speed,
            self._accelerate_count,
            self.ACCELERATOR_FACTOR,
        )

    def reset_score(self):
        """Reset the score"""
        self._score = 0

    def reset_accelerate_count(self):
        """Reset accelerate count"""
        self._accelerate_count = 0

    def reset_falling_speed(self):
        """Reset the falling speed based on current level"""
        self._falling_speed = 0.0

    def reset_fall_time(self):
        """Reset the fall time"""
        self._fall_time = 0.0

    def calculate_level(self) -> type_of_level:
        """Calculate level based on score"""
        return (self._score // 100) + 1

    def set_level(self, level: int):
        """Set level"""
        self._level = level

    def get_level_speed(self) -> type_of_speed:
        speed_generator = create_speed_generator()
        return speed_generator(self._level, self.SPEED_FACTOR)

    def should_upgrade_level(self) -> bool:
        """Check level should upgrade or not"""
        return self.calculate_level() > self._level

    def upgrade_level(self):
        """Upgrade level using calculated level"""
        self.set_level(self.calculate_level())

    def run(self, scene_parameter: SceneParameter):
        """Tetris main run"""
        # TODO: add tetris run
        self.surface.fill((10, 10, 20))
