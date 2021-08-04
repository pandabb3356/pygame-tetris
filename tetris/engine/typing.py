from typing import Callable, TypeVar, Dict

from tetris.helper import Factor

# Tetris
type_of_level = int
type_of_speed = float
type_of_count = int
type_of_score = int

type_of_speed_generator = Callable[[type_of_level, Factor], float]
type_of_accelerator = Callable[[type_of_speed, type_of_count, Factor], float]

# Texture
TextureContent = TypeVar("TextureContent")
TextureTransform = TypeVar("TextureTransform")

type_of_texture_mapping = Dict[TextureContent, TextureTransform]
