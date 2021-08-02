import abc
from typing import Optional, Type, List

import pygame as pg


class SceneMeta(type):
    def __rshift__(self, other: Type["Scene"]):
        self.next = other
        other.previous = self

    def __lshift__(self, other: Type["Scene"]):
        self.previous = other
        other.next = self


class SceneParameter:
    """Parameter for running scene"""

    events: List[pg.event.Event]
    clock: pg.time.Clock

    def __init__(self, events: List[pg.event.Event], clock: pg.time.Clock):
        self.events = events
        self.clock = clock


class Scene(metaclass=SceneMeta):
    surface: pg.Surface

    previous: Optional[Type["Scene"]] = None
    next: Optional[Type["Scene"]] = None

    PARAMETER_CLS: Type[SceneParameter] = SceneParameter

    def __init__(self, surface: pg.Surface):
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
