from typing import Optional, Type, Callable

import pygame as pg

from .scene import StartMenu, Scene
from .scene.base import SceneParameter


def scene_check(func) -> Callable:
    def wrapper(game: "Game", *args, **kwargs):
        if game.scene is None:
            raise ValueError("Scene is empty !!")
        return func(game, *args, **kwargs)

    return wrapper


class Game:
    """Main game process"""

    WIN_SIZE = (1000, 800)
    INIT_SCENE_CLS: Type[Scene] = StartMenu

    _surface: pg.surface.Surface

    _scene: Optional[Scene]

    def __init__(self) -> None:
        self.set_surface(pg.display.set_mode(self.WIN_SIZE))

    def set_surface(self, surface: pg.surface.Surface) -> None:
        self._surface = surface

    def init(self) -> None:
        # start to load
        self._scene = self.INIT_SCENE_CLS(self._surface)

    @scene_check
    def scene_run(self, scene_parameter: SceneParameter) -> int:
        return self._scene.run(scene_parameter)  # type: ignore

    @scene_check
    def switch_scene(self, value: int) -> None:
        scene_cls_map = {
            1: self._scene.next,  # type: ignore
            -1: self._scene.previous,  # type: ignore
        }

        scene_cls = scene_cls_map.get(value)
        if scene_cls:
            self._scene = scene_cls(self._surface)

    @property
    def scene(self) -> Optional[Scene]:
        return self._scene

    def run(self) -> None:
        pg.init()
        clock = pg.time.Clock()

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
                        pressed=pg.key.get_pressed(),
                    )
                ),
            )

            pg.display.flip()
            clock.tick()
            pg.display.update()

        pg.quit()
