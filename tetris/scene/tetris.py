from typing import List, Type

import pygame as pg

from .base import Scene, SceneParameter
from ..engine.board import Board
from ..engine.speed import create_accelerator, Factor, create_speed_generator
from ..engine.texture import ColorTexture, ColorContent
from ..engine.typing import (
    type_of_level,
    type_of_score,
    type_of_speed,
    type_of_count,
)
from ..helper import Vector, Position
from ..render.tetris import TetrisRender, TetrisRenderParameter


class Tetris(Scene):
    """Tetris scene"""

    BLOCK_SIZE: int = 30
    N_ROWS: int = 20
    N_COLS: int = 10
    INIT_LEVEL: int = 1
    SCORE_UNIT: int = 10

    ACCELERATOR_TYPE: str = "linear"
    ACCELERATOR_FACTOR: Factor = Factor(a=0.005)
    SPEED_FACTOR: Factor = Factor(a=1.0, b=0.05)
    TEXTURE_CLS: Type[ColorTexture] = ColorTexture
    TEXTURE_CONTENTS: List[ColorContent] = [
        ColorContent.red,
        ColorContent.blue,
        ColorContent.yellow,
        ColorContent.orange,
        ColorContent.purple,
        ColorContent.dark_green,
    ]

    _board: Board

    _level: type_of_level
    _score: type_of_score

    _falling_speed: type_of_speed
    _fall_time: float

    _game_over: bool

    _accelerate_count: type_of_count

    # move vector of each run
    _move_vector: Vector

    _render: TetrisRender

    def init(self):
        """Initialize"""
        self.TEXTURE_CLS.load_pools(self.TEXTURE_CONTENTS)
        self.reset()
        self._board = Board()
        self._board.init(self.N_ROWS, self.N_COLS, self.TEXTURE_CLS.pools)

        self._render = TetrisRender(
            self.surface,
            self._board,
            Position(
                self.surface.get_width() // 2 - self.N_COLS * self.BLOCK_SIZE // 2,
                self.surface.get_height() // 2 - self.N_ROWS * self.BLOCK_SIZE // 2,
            ),
        )

    def reset(self):
        """Reset Tetris"""
        self.reset_score()
        self.set_level(self.INIT_LEVEL)

        self.reset_falling_speed()
        self.reset_fall_time()

        self._game_over = False

        self.reset_accelerate_count()

        self.reset_move_vector()

    def reset_move_vector(self):
        """Reset move vector"""
        self._move_vector = Vector(0, 0)

    def accelerate(self):
        """Accelerate the falling speed"""
        self._accelerate_count += 1
        accelerator = create_accelerator(self.ACCELERATOR_TYPE)
        self._falling_speed = accelerator(
            self.get_level_speed(),
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
        self._accelerate_count = 0
        self._falling_speed = self.get_level_speed()

    def reset_fall_time(self):
        """Reset the fall time"""
        self._fall_time = 0.0

    def calculate_level(self) -> type_of_level:
        """Calculate level based on score"""
        return (self._score // 100) + 1

    def set_level(self, level: type_of_level):
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

    def add_score(self, cleared_lines: int):
        """Add score according to cleared lines"""
        self._score = cleared_lines * self.SCORE_UNIT

    def show(self):
        """Show the render result"""
        if self._render:
            self._render.render(
                TetrisRenderParameter(
                    self._score,
                    self._level,
                )
            )

    def move_left(self):
        self._move_vector += Vector(-1, 0)

    def move_right(self):
        self._move_vector += Vector(1, 0)

    def move_down(self):
        self._move_vector += Vector(0, 1)

    def rotate(self, clockwise: bool = False):
        self._board.rotate_piece(clockwise=clockwise)

    def event_detect(self, events: List[pg.event.Event]):
        keydown_map = {
            pg.K_LEFT: (self.move_left, {}),
            pg.K_RIGHT: (self.move_right, {}),
            pg.K_DOWN: (self.move_down, {}),
            pg.K_z: (self.rotate, {"clockwise": False}),
            pg.K_x: (self.rotate, {"clockwise": True}),
        }

        for e in events:
            if not self._game_over and e.type == pg.KEYUP and keydown_map.get(e.key):
                func, func_kwargs = keydown_map[e.key]
                func(**func_kwargs)  # type: ignore

    def pressed_detect(self, pressed):
        pressed_map = {pg.K_DOWN: (self.accelerate, {})}

        not_pressed_map = {pg.K_DOWN: (self.reset_falling_speed, {})}

        for press_key, (func, func_kwargs) in pressed_map.items():
            if pressed[press_key]:
                func(**func_kwargs)

        for press_key, (func, func_kwargs) in not_pressed_map.items():
            if not pressed[press_key]:
                func(**func_kwargs)

    def run(self, scene_parameter: SceneParameter):
        """Tetris main run"""
        # # TODO: add tetris run
        self.reset_move_vector()

        self.event_detect(scene_parameter.events)
        self.pressed_detect(scene_parameter.pressed)

        if self._fall_time / 1000 >= self._falling_speed:
            self._fall_time = 0
            self.move_down()

        overflow, checked_move_vector = self._board.check_move(self._move_vector)
        self._game_over = overflow and self._board.is_piece_collapsed

        if not self._game_over:
            if self._board.is_piece_collapsed:
                self._board.lock_piece()
                cleared = self._board.clear_lines()
                self._score += cleared * 10
                self._board.switch_piece()
                self._falling_speed = self.get_level_speed()
            else:
                self._board.set_piece(self._board.move_piece(checked_move_vector))
        else:
            return -1

        self.show()

        if self.should_upgrade_level():
            self.upgrade_level()

        # increase fall time by clock
        self._fall_time += scene_parameter.clock.get_rawtime()
