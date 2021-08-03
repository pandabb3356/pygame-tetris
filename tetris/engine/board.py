from tetris.engine.piece import Piece
from tetris.helper import Vector


class Board:
    BLOCK_SIZE: int = 30

    _piece: Piece
    _next_piece: Piece

    def init(self):
        """Initialize"""
        self.reset()

    def reset(self):
        """Reset"""

    def set_piece(self, piece: Piece):
        """Set the piece"""
        self._piece = piece

    def switch_piece(self, piece: Piece):
        """Switch the current piece & next piece"""
        self.set_piece(piece)
        self._next_piece = self.generate_piece()

    @classmethod
    def generate_piece(cls) -> Piece:
        """Generate the piece"""

    def lock_piece(self):
        """Lock the collapsed piece"""

    def rotate_piece(self, clockwise: bool = False):
        """Rotate the piece"""

    def clear_lines(self) -> int:
        """Get the cleared lines"""

    def check_move(self, vector: Vector) -> Vector:
        """Get the coordinate vector with given vector"""
