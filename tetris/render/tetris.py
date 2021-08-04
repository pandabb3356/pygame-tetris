import itertools

import pygame as pg

from .base import RenderParameter, Render
from ..engine.board import Board
from ..engine.texture import ColorTexture
from ..engine.typing import (
    type_of_level,
    type_of_score,
)
from ..helper import Vector, Position


class TetrisRenderParameter(RenderParameter):
    def __init__(self, score: type_of_score, level: type_of_level):
        self.score = score
        self.level = level


class TetrisRender(Render):
    BLOCK_SIZE: int = 30

    BACKGROUND_COLOR = (0, 0, 0)
    GRID_BORDER_COLOR = (255, 255, 255)
    BOARD_BORDER_COLOR = (255, 255, 255)
    BOARD_BACKGROUND_COLOR = (10, 10, 20)
    BOARD_BORDER_SIZE = 5

    TITLE_TEXT = "Tetris"
    TITLE_FONT_STYLE = "comicsansms"
    TITLE_FONT_SIZE = 100
    TITLE_COLOR = (0, 128, 0)

    SCORE_TEXT = "Score"
    SCORE_FONT_STYLE = "comicsansms"
    SCORE_FONT_SIZE = 50
    SCORE_FONT_COLOR = (0, 128, 0)

    NEXT_TEXT = "Next"
    NEXT_FONT_STYLE = "comicsansms"
    NEXT_FONT_SIZE = 50
    NEXT_FONT_COLOR = (0, 128, 0)

    def __init__(
        self, surface: pg.surface.Surface, board: Board, board_start_pos: Position
    ):
        self._surface = surface
        self._board = board
        self._board_start_pos = board_start_pos

    def render(self, render_parameter: TetrisRenderParameter) -> None:  # type: ignore
        self.render_background()
        self.render_title()
        self.render_outer_border()
        self.render_piece()
        self.render_grid_line(self._board.n_cols, self._board.n_rows)
        self.render_grid()
        self.render_next_piece()
        self.render_score_box(render_parameter.score)

    def render_background(self) -> None:
        self._surface.fill(self.BACKGROUND_COLOR)

    def render_title(self) -> None:
        font = pg.font.SysFont(self.TITLE_FONT_STYLE, self.TITLE_FONT_SIZE)
        text = font.render(
            self.TITLE_TEXT,
            True,
            self.TITLE_COLOR,
        )
        self._surface.blit(text, self._board_start_pos + Vector(0, -120))

    def render_piece(self) -> None:
        if self._board.piece:
            for vec in self._board.piece:
                surface_pos = self._board_start_pos + Vector(*vec) * self.BLOCK_SIZE

                if not (
                    surface_pos.x >= self._board_start_pos.x
                    and surface_pos.y >= self._board_start_pos.y
                ):
                    continue

                pg.draw.rect(
                    self._surface,
                    ColorTexture.transform(self._board.piece.texture.content),
                    rect=(
                        int(surface_pos.x),
                        int(surface_pos.y),
                        self.BLOCK_SIZE,
                        self.BLOCK_SIZE,
                    ),
                )

    def render_grid_line(self, n_cols: int, n_rows: int) -> None:
        for i, j in itertools.product(range(n_cols + 1), range(n_rows + 1)):
            # horizon line
            pg.draw.line(
                self._surface,
                self.GRID_BORDER_COLOR,
                self._board_start_pos + Vector(0, j) * self.BLOCK_SIZE,
                self._board_start_pos + Vector(n_cols, j) * self.BLOCK_SIZE,
            )

            # vertical line
            pg.draw.line(
                self._surface,
                self.GRID_BORDER_COLOR,
                self._board_start_pos + Vector(i, 0) * self.BLOCK_SIZE,
                self._board_start_pos + Vector(i, n_rows) * self.BLOCK_SIZE,
            )

    def render_next_piece(self) -> None:
        vector = Vector(self._board.n_cols + 2, 2)
        box_start_pos = self._board_start_pos + vector * self.BLOCK_SIZE

        def _render_next_text() -> None:
            font = pg.font.SysFont(self.NEXT_FONT_STYLE, self.NEXT_FONT_SIZE)

            text = font.render(
                self.NEXT_TEXT,
                True,
                self.NEXT_FONT_COLOR,
            )
            self._surface.blit(text, box_start_pos + Vector(0, -3) * self.BLOCK_SIZE)

        def _render_shape():
            piece_pos_vec = Vector(
                self._board.next_piece.position.x, self._board.next_piece.position.y
            )
            for pos in self._board.next_piece:
                surface_pos = (
                    box_start_pos
                    + (Vector(*pos) - piece_pos_vec + Vector(2, 2)) * self.BLOCK_SIZE
                )
                pg.draw.rect(
                    self._surface,
                    ColorTexture.transform(self._board.next_piece.texture.content),
                    (surface_pos.x, surface_pos.y, self.BLOCK_SIZE, self.BLOCK_SIZE),
                )

        _render_next_text()
        if self._board.next_piece:
            _render_shape()

    def render_score_box(self, score: type_of_score) -> None:
        vector = Vector(self._board.n_cols + 2, 10)
        box_start_pos = self._board_start_pos + vector * self.BLOCK_SIZE

        font = pg.font.SysFont(self.SCORE_FONT_STYLE, self.SCORE_FONT_SIZE)

        text = font.render(self.SCORE_TEXT, True, self.SCORE_FONT_COLOR)
        self._surface.blit(text, box_start_pos + Vector(0, -3) * self.BLOCK_SIZE)

        text = font.render(f"{score}", True, self.SCORE_FONT_COLOR)
        self._surface.blit(text, box_start_pos + Vector(0, 0) * self.BLOCK_SIZE)

    def render_outer_border(self) -> None:
        # outer rect
        pg.draw.rect(
            self._surface,
            self.BOARD_BORDER_COLOR,
            (
                int(self._board_start_pos.x) - self.BOARD_BORDER_SIZE,
                int(self._board_start_pos.y) - self.BOARD_BORDER_SIZE,
                self.BLOCK_SIZE * self._board.n_cols + self.BOARD_BORDER_SIZE * 2 + 1,
                self.BLOCK_SIZE * self._board.n_rows + self.BOARD_BORDER_SIZE * 2 + 1,
            ),
        )

        # inner rect
        pg.draw.rect(
            self._surface,
            self.BOARD_BACKGROUND_COLOR,
            (
                int(self._board_start_pos.x),
                int(self._board_start_pos.y),
                self.BLOCK_SIZE * self._board.n_cols,
                self.BLOCK_SIZE * self._board.n_rows,
            ),
        )

    def render_grid(self) -> None:
        for (x, y) in itertools.product(
            range(self._board.n_cols), range(self._board.n_rows)
        ):
            pos = Position(x, y)
            texture = self._board.grid.get_cell(pos)
            if not texture:
                continue

            rect_pos = self._board_start_pos + Vector(*pos) * self.BLOCK_SIZE

            pg.draw.rect(
                self._surface,
                ColorTexture.transform(texture.content),
                (
                    int(rect_pos.x),
                    int(rect_pos.y),
                    self.BLOCK_SIZE,
                    self.BLOCK_SIZE,
                ),
            )

        # grid border
        self.render_grid_line(self._board.n_cols, self._board.n_rows)
