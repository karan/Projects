"""
Rubik's Cube State Representation and Move Engine.

This package provides a mathematically correct, well-tested implementation
of Rubik's Cube state and transformations.

Modules:
    state: CubeState class using 54-sticker representation
    moves: Pure move transformations with mathematical guarantees
"""

from .state import CubeState
from .moves import apply_move, apply_sequence, invert_move, invert_sequence

__all__ = [
    'CubeState',
    'apply_move',
    'apply_sequence',
    'invert_move',
    'invert_sequence',
]
