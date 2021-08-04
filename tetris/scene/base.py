import abc
from typing import Optional, Type, List

import pygame as pg
from pygame.key import ScancodeWrapper  # type: ignore


class SceneMeta(type):
    def __rshift__(self, other: Optional[Type["Scene"]]):
        self.next = other
        if other:
            other.previous = self  # type: ignore

    def __lshift__(self, other: Optional[Type["Scene"]]):
        self.previous = other
        if other:
            other.next = self  # type: ignore


class SceneParameter:
    """Parameter for running scene"""

    events: List[pg.event.Event]
    clock: pg.time.Clock
    pressed: ScancodeWrapper

    def __init__(
        self,
        events: List[pg.event.Event],
        clock: pg.time.Clock,
        pressed: ScancodeWrapper,
    ):
        self.events = events
        self.clock = clock
        self.pressed = pressed


class Scene(metaclass=SceneMeta):
    surface: pg.surface.Surface

    previous: Optional[Type["Scene"]] = None
    next: Optional[Type["Scene"]] = None

    PARAMETER_CLS: Type[SceneParameter] = SceneParameter

    def __init__(self, surface: pg.surface.Surface):
        self.surface = surface

        self.init()

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def run(self, scene_parameter: SceneParameter):
        pass

    @property
    def surface_width(self) -> int:
        return self.surface.get_width()

    @property
    def surface_height(self) -> int:
        return self.surface.get_height()
