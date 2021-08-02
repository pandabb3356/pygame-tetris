import abc
from typing import Optional, Type

import pygame as pg


class SceneMeta(type):
    def __rshift__(self, other: Type["Scene"]):
        self.next = other
        other.previous = self

    def __lshift__(self, other: Type["Scene"]):
        self.previous = other
        other.next = self


class Scene(metaclass=SceneMeta):
    surface: pg.Surface

    previous: Optional[Type["Scene"]] = None
    next: Optional[Type["Scene"]] = None

    def __init__(self, surface: pg.Surface):
        self.surface = surface

        self.init()

    @abc.abstractmethod
    def init(self):
        pass

    @abc.abstractmethod
    def run(self, events):
        pass

    @property
    def surface_width(self) -> int:
        return self.surface.get_width()

    @property
    def surface_height(self) -> int:
        return self.surface.get_height()
