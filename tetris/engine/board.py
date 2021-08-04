import random
from typing import List, Optional, Tuple, Sequence

from tetris.engine.piece import Piece
from tetris.engine.texture import Texture
from tetris.helper import Vector, Position

type_of_grid_mapping = List[List[Optional[Texture]]]


def piece_generator(position: Position, pools: Sequence) -> Piece:
    """Piece generator"""

    shape_cls = random.choice(Piece.SHAPES)
    content = random.choice(pools)
    rot: int = random.randint(0, 3)

    return Piece(position.x, position.y, shape_cls, content, rot=rot)


class Grid:
    """Board grid"""

    n_rows: int
    n_cols: int

    def __init__(self, n_rows: int, n_cols: int):
        self.n_rows = n_rows
        self.n_cols = n_cols

        self._mapping: type_of_grid_mapping = [[None] * n_cols for __ in range(n_rows)]

    def __iter__(self):
        for y, rows in enumerate(self._mapping):
            for x, v in enumerate(rows):
                yield Position(x, y), v

    def set(self, value: Tuple[Position, Texture]):
        pos, t = value
        self._mapping[int(pos.y)][int(pos.x)] = t

    def clear_rows(self) -> int:
        mapping = []
        cleared = 0

        for y, rows in enumerate(self._mapping):
            if all(v is not None for v in rows):
                cleared += 1
            else:
                mapping += [rows]

        self._mapping = [[None] * self.n_cols for _ in range(cleared)] + mapping  # type: ignore

        return cleared

    def is_occupied(self, position: Position) -> bool:
        return self.get_cell(position) is not None  # type: ignore

    def get_cell(self, position: Position):
        return self._mapping[int(position.y)][int(position.x)]


class Board:
    n_rows: int
    n_cols: int

    _piece: Piece
    _next_piece: Piece

    _grid: Grid

    _texture_pools: set

    def init(self, n_rows: int, n_cols: int, texture_pools: set):
        """Initialize"""
        self.n_rows = n_rows
        self.n_cols = n_cols
        self._texture_pools = texture_pools
        self.reset()

    def reset(self):
        """Reset"""
        self._grid = Grid(self.n_rows, self.n_cols)
        self._next_piece = self.generate_piece()
        self.switch_piece()

    def set_piece(self, piece: Piece):
        """Set the piece"""
        self._piece = piece

    def switch_piece(self):
        """Switch the current piece & next piece"""
        self.set_piece(self._next_piece)
        self._next_piece = self.generate_piece()

    def generate_piece(self) -> Piece:
        """Generate the piece"""
        return piece_generator(
            Position(self.n_cols // 2, -2), list(self._texture_pools)
        )

    def move_piece(self, vector: Vector) -> Piece:
        """Move the piece"""
        return self._piece.move(vector)

    def lock_piece(self):
        """Lock the collapsed piece"""
        for vec in self._piece:
            self._grid.set((vec, self._piece.texture))

    def rotate_piece(self, clockwise: bool = False):
        """Rotate the piece"""
        self._piece.rotate(-1 if not clockwise else 1)

    @property
    def piece(self) -> Optional[Piece]:
        return self._piece

    @property
    def next_piece(self) -> Optional[Piece]:
        return self._next_piece

    @property
    def is_piece_collapsed(self) -> bool:
        return self._piece.collapsed

    @property
    def grid(self) -> Grid:
        return self._grid

    def clear_lines(self) -> int:
        """Get the cleared lines"""
        return self._grid.clear_rows()

    def check_move(self, vector: Vector) -> Tuple[bool, Vector]:
        """Check is overflow and get the coordinate vector with given vector"""
        overflow = False

        v_x, v_y = 0.0, 0.0

        for pos in self._piece:
            moved_pos = pos + vector
            if moved_pos.x < 0:
                v_x = max(v_x, -moved_pos.x, 0)
            elif moved_pos.x > self.n_cols - 1:
                v_x = min(v_x, self.n_cols - moved_pos.x - 1, 0)
            elif moved_pos.y > self.n_rows - 1:
                v_y = 0
                self._piece.collapsed = True
            elif moved_pos.y > 0 and self._grid.is_occupied(moved_pos):
                new_vec = vector.clone()
                collapsed = True
                while new_vec.x:
                    if new_vec.x != 0:
                        new_vec += Vector(-new_vec.x, 0)
                        if not self._grid.is_occupied(pos + new_vec):
                            collapsed = False
                            break

                v_x, v_y = new_vec - vector
                self._piece.collapsed = collapsed

            overflow = overflow or (pos + vector).y < 0 or pos.y < 0

        return overflow, vector + Vector(v_x, v_y)
