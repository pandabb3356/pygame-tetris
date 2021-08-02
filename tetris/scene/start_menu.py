from typing import Optional

import pygame as pg

from tetris.helper import Position, RGB
from .base import Scene, SceneParameter


class StartMenu(Scene):
    """Start menu"""

    font: Optional[pg.font.SysFont] = None

    FONT_COLOR: RGB = (0, 128, 128)
    FONT_STYLE: str = "comicsansms"
    TEXT: str = "Press any key to start ..."

    def init(self):
        self.font = pg.font.SysFont(self.FONT_STYLE, self.font_size)
        self.to_surface()

    def to_surface(self):
        self.surface.blit(
            self.render_text(),
            self.text_pos,
        )

    def render_text(self) -> pg.font.SysFont:
        return self.font.render(
            self.TEXT,
            True,
            self.FONT_COLOR,
        )

    @property
    def text_length(self) -> int:
        return len(self.TEXT)

    @property
    def font_size(self) -> int:
        return self.surface_width // 20

    @property
    def text_pos(self) -> Position:
        len(self.TEXT)
        return Position(
            self.surface.get_width() // 4,
            self.surface.get_height() // 4 + self.font_size * 2.5,
        )

    def run(self, scene_parameter: SceneParameter):
        for e in scene_parameter.events:
            if e.type == pg.KEYDOWN:
                return 1
        return 0
