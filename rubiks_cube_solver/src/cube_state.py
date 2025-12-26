"""
CubeState: The 54-sticker representation of a Rubik's Cube.

This module implements the cube state using a simple list of 54 stickers.
Each face has 9 stickers indexed 0-8 in reading order (left-to-right, top-to-bottom).

Face order: U R F D L B (Up, Right, Front, Down, Left, Back)
Color scheme: W-White, R-Red, B-Blue, Y-Yellow, O-Orange, G-Green
Standard orientation: White top, Blue front
"""

from typing import List, Dict
from copy import deepcopy


class CubeState:
    """
    Represents a Rubik's Cube state using 54 stickers.

    Sticker Layout (per face):
        0 1 2
        3 4 5
        6 7 8

    Face indices in the sticker array:
        U (Up):    0-8    (White in solved state)
        R (Right): 9-17   (Red in solved state)
        F (Front): 18-26  (Blue in solved state)
        D (Down):  27-35  (Yellow in solved state)
        L (Left):  36-44  (Orange in solved state)
        B (Back):  45-53  (Green in solved state)
    """

    # Face name to index mapping
    FACES = {'U': 0, 'R': 1, 'F': 2, 'D': 3, 'L': 4, 'B': 5}
    FACE_NAMES = ['U', 'R', 'F', 'D', 'L', 'B']

    # Color to letter mapping (standard cube coloring)
    COLORS = {'U': 'W', 'R': 'R', 'F': 'B', 'D': 'Y', 'L': 'O', 'B': 'G'}

    def __init__(self, stickers: List[str] = None):
        """
        Initialize a cube state.

        Args:
            stickers: List of 54 sticker colors. If None, creates a solved cube.
        """
        if stickers is None:
            # Create a solved cube
            self.stickers = []
            for face_name in self.FACE_NAMES:
                color = self.COLORS[face_name]
                self.stickers.extend([color] * 9)
        else:
            if len(stickers) != 54:
                raise ValueError(f"Expected 54 stickers, got {len(stickers)}")
            self.stickers = list(stickers)

    def get_face(self, face: str) -> List[str]:
        """
        Get all 9 stickers of a face.

        Args:
            face: Face name ('U', 'R', 'F', 'D', 'L', 'B')

        Returns:
            List of 9 sticker colors for that face
        """
        face_idx = self.FACES[face]
        start = face_idx * 9
        return self.stickers[start:start + 9]

    def get_sticker(self, face: str, position: int) -> str:
        """
        Get a specific sticker on a face.

        Args:
            face: Face name
            position: Position on face (0-8)

        Returns:
            Sticker color
        """
        face_idx = self.FACES[face]
        return self.stickers[face_idx * 9 + position]

    def set_sticker(self, face: str, position: int, color: str):
        """
        Set a specific sticker on a face.

        Args:
            face: Face name
            position: Position on face (0-8)
            color: New sticker color
        """
        face_idx = self.FACES[face]
        self.stickers[face_idx * 9 + position] = color

    def copy(self) -> 'CubeState':
        """Create a deep copy of this cube state."""
        return CubeState(deepcopy(self.stickers))

    def is_solved(self) -> bool:
        """
        Check if the cube is in a solved state.

        Returns:
            True if all faces are uniform (all stickers same color)
        """
        for face_name in self.FACE_NAMES:
            face_stickers = self.get_face(face_name)
            if len(set(face_stickers)) != 1:
                return False
        return True

    def __str__(self) -> str:
        """
        Return a visual representation of the cube.

        The layout shows the unfolded cube:
                U U U
                U U U
                U U U
        L L L   F F F   R R R   B B B
        L L L   F F F   R R R   B B B
        L L L   F F F   R R R   B B B
                D D D
                D D D
                D D D
        """
        U = self.get_face('U')
        R = self.get_face('R')
        F = self.get_face('F')
        D = self.get_face('D')
        L = self.get_face('L')
        B = self.get_face('B')

        lines = []
        # Top face (U)
        for i in range(3):
            lines.append('      ' + ' '.join(U[i*3:(i+1)*3]))

        # Middle row (L, F, R, B)
        for i in range(3):
            line = ' '.join(L[i*3:(i+1)*3]) + '   '
            line += ' '.join(F[i*3:(i+1)*3]) + '   '
            line += ' '.join(R[i*3:(i+1)*3]) + '   '
            line += ' '.join(B[i*3:(i+1)*3])
            lines.append(line)

        # Bottom face (D)
        for i in range(3):
            lines.append('      ' + ' '.join(D[i*3:(i+1)*3]))

        return '\n'.join(lines)

    def __eq__(self, other) -> bool:
        """Check if two cube states are equal."""
        if not isinstance(other, CubeState):
            return False
        return self.stickers == other.stickers

    def __hash__(self) -> int:
        """Make CubeState hashable for use in sets/dicts."""
        return hash(tuple(self.stickers))
