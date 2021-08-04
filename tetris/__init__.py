from typing import Optional, Type

import pygame as pg

from .scene import StartMenu, Scene
from .scene.base import SceneParameter


def scene_check(func):
    def wrapper(game: "Game", *args, **kwargs):
        if game.scene is None:
            raise ValueError("Scene is empty !!")
        return func(game, *args, **kwargs)

    return wrapper


class Game:
    """Main game process"""

    WIN_SIZE = (1000, 800)
    INIT_SCENE_CLS: Type[Scene] = StartMenu

    _surface: pg.Surface

    _scene: Optional[Scene]

    def __init__(self):
        self.set_surface(pg.display.set_mode(self.WIN_SIZE))

    def set_surface(self, surface: pg.Surface):
        self._surface = surface

    def init(self):
        # start to load
        self._scene = self.INIT_SCENE_CLS(self._surface)

    @scene_check
    def scene_run(self, scene_parameter: SceneParameter) -> int:
        return self._scene.run(scene_parameter)  # type: ignore

    @scene_check
    def switch_scene(self, value: int):
        scene_cls_map = {1: self._scene.next, -1: self._scene.previous}  # type: ignore

        scene_cls = scene_cls_map.get(value)
        if scene_cls:
            self._scene = scene_cls(self._surface)

    @property
    def scene(self) -> Optional[Scene]:
        return self._scene

    def run(self):
        pg.init()
        clock = pg.time.Clock()
        clock.tick()

        self.init()

        done = 0

        while not done:
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT or (e.type == pg.KEYUP and e.key == pg.K_ESCAPE):
                    done = 1
                    break

            self.switch_scene(
                self.scene_run(
                    SceneParameter(
                        events=events,
                        clock=clock,
                    )
                ),
            )

            pg.display.flip()
            pg.display.update()

        pg.quit()
