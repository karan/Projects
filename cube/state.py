"""
Rubik's Cube State Representation.

This module implements a 54-sticker (facelet) model of a Rubik's Cube.

Why 54-sticker model?
---------------------
A Rubik's Cube has 6 faces × 9 stickers per face = 54 stickers total.

Advantages of this representation:
  - Intuitive: directly maps to physical cube appearance
  - Simple: no need to track permutation + orientation separately
  - Debuggable: easy to visualize and print
  - Beginner-friendly: matches how people think about cubes

Disadvantages:
  - Redundant: only 20 moveable pieces, but we track 54 positions
  - Cannot detect impossible states easily (needs validation)

Face Ordering: URFDLB
---------------------
We use standard cube notation face order:
  U (Up)    - index 0-8   - typically WHITE
  R (Right) - index 9-17  - typically RED
  F (Front) - index 18-26 - typically GREEN
  D (Down)  - index 27-35 - typically YELLOW
  L (Left)  - index 36-44 - typically ORANGE
  B (Back)  - index 45-53 - typically BLUE

Position Indexing (within each face):
-------------------------------------
Each face is indexed 0-8 in reading order:

    0 1 2
    3 4 5
    6 7 8

For example, U face positions:
    U0 U1 U2
    U3 U4 U5
    U6 U7 U8

Absolute indexing:
    U: 0-8, R: 9-17, F: 18-26, D: 27-35, L: 36-44, B: 45-53

Mathematical Properties:
-----------------------
A valid cube state must satisfy:
  1. Exactly 9 stickers of each color
  2. Center stickers never move (indices 4, 13, 22, 31, 40, 49)
  3. Corner pieces have 3 stickers, edges have 2
  4. Sum of corner orientations ≡ 0 (mod 3)
  5. Sum of edge orientations ≡ 0 (mod 2)
  6. Even permutation parity

This module does NOT enforce all invariants at construction time.
Use validation functions or tests to verify cube validity.
"""

from typing import List, Literal, Tuple
from dataclasses import dataclass
from copy import deepcopy


# Type aliases for clarity
FaceName = Literal['U', 'R', 'F', 'D', 'L', 'B']
Color = str
Position = int  # 0-53


# Standard solved cube colors (Western color scheme)
SOLVED_COLORS = {
    'U': 'W',  # Up = White
    'R': 'R',  # Right = Red
    'F': 'G',  # Front = Green
    'D': 'Y',  # Down = Yellow
    'L': 'O',  # Left = Orange
    'B': 'B',  # Back = Blue
}

# Face index ranges
FACE_RANGES = {
    'U': range(0, 9),
    'R': range(9, 18),
    'F': range(18, 27),
    'D': range(27, 36),
    'L': range(36, 45),
    'B': range(45, 54),
}

# Face name to starting index
FACE_OFFSETS = {'U': 0, 'R': 9, 'F': 18, 'D': 27, 'L': 36, 'B': 45}

# Center positions (never move during legal moves)
CENTER_POSITIONS = [4, 13, 22, 31, 40, 49]


@dataclass(frozen=True)
class CubeState:
    """
    Immutable representation of a Rubik's Cube state.

    Attributes:
        stickers: Tuple of 54 color strings in URFDLB order

    The immutability ensures:
      - Thread safety
      - Hashable (can use as dict key or in sets)
      - Prevents accidental mutation bugs
      - Clear semantics: moves return new states

    Examples:
        >>> cube = CubeState.solved()
        >>> cube.is_solved()
        True

        >>> cube.get_sticker('U', 0)
        'W'

        >>> cube.get_face('U')
        ('W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W')
    """

    stickers: Tuple[Color, ...] = None

    def __init__(self, stickers: List[Color] | Tuple[Color, ...] = None):
        """
        Create a cube state.

        Args:
            stickers: List or tuple of 54 colors in URFDLB order.
                     If None, creates a solved cube.

        Raises:
            ValueError: If stickers is not length 54
        """
        if stickers is None:
            stickers = CubeState._create_solved_stickers()

        if len(stickers) != 54:
            raise ValueError(f"Expected 54 stickers, got {len(stickers)}")

        # Convert to tuple for immutability
        object.__setattr__(self, 'stickers', tuple(stickers))

    @staticmethod
    def _create_solved_stickers() -> List[Color]:
        """Create sticker list for a solved cube."""
        stickers = []
        for face in ['U', 'R', 'F', 'D', 'L', 'B']:
            color = SOLVED_COLORS[face]
            stickers.extend([color] * 9)
        return stickers

    @classmethod
    def solved(cls) -> 'CubeState':
        """
        Factory method to create a solved cube.

        Returns:
            CubeState in solved position (all faces uniform color)

        Example:
            >>> cube = CubeState.solved()
            >>> cube.is_solved()
            True
        """
        return cls(cls._create_solved_stickers())

    def is_solved(self) -> bool:
        """
        Check if cube is in solved state.

        A cube is solved when all 9 stickers on each face have the same color
        as their center sticker.

        Returns:
            True if cube is solved, False otherwise

        Time Complexity: O(1) - checks 54 stickers exactly once
        """
        for face_name, face_range in FACE_RANGES.items():
            # Get center color for this face
            center_idx = list(face_range)[4]  # Center is always at position 4
            center_color = self.stickers[center_idx]

            # Check all stickers on this face match center
            for idx in face_range:
                if self.stickers[idx] != center_color:
                    return False

        return True

    def get_sticker(self, face: FaceName, pos: int) -> Color:
        """
        Get the color at a specific position on a face.

        Args:
            face: Face name ('U', 'R', 'F', 'D', 'L', 'B')
            pos: Position on face (0-8)

        Returns:
            Color at that position

        Raises:
            ValueError: If face invalid or pos out of range

        Example:
            >>> cube = CubeState.solved()
            >>> cube.get_sticker('U', 4)  # Center of Up face
            'W'
        """
        if face not in FACE_OFFSETS:
            raise ValueError(f"Invalid face: {face}. Must be U/R/F/D/L/B")
        if not 0 <= pos <= 8:
            raise ValueError(f"Invalid position: {pos}. Must be 0-8")

        abs_idx = FACE_OFFSETS[face] + pos
        return self.stickers[abs_idx]

    def get_face(self, face: FaceName) -> Tuple[Color, ...]:
        """
        Get all 9 stickers for a face.

        Args:
            face: Face name ('U', 'R', 'F', 'D', 'L', 'B')

        Returns:
            Tuple of 9 colors in reading order (0-8)

        Example:
            >>> cube = CubeState.solved()
            >>> cube.get_face('U')
            ('W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W')
        """
        if face not in FACE_RANGES:
            raise ValueError(f"Invalid face: {face}")

        return tuple(self.stickers[i] for i in FACE_RANGES[face])

    def with_sticker(self, face: FaceName, pos: int, color: Color) -> 'CubeState':
        """
        Return a new cube with one sticker changed.

        Since CubeState is immutable, this creates a new cube with the change.

        Args:
            face: Face to modify
            pos: Position on face (0-8)
            color: New color for that sticker

        Returns:
            New CubeState with the single sticker modified

        Example:
            >>> cube = CubeState.solved()
            >>> cube2 = cube.with_sticker('U', 0, 'R')
            >>> cube2.get_sticker('U', 0)
            'R'
            >>> cube.get_sticker('U', 0)  # Original unchanged
            'W'
        """
        if face not in FACE_OFFSETS:
            raise ValueError(f"Invalid face: {face}")
        if not 0 <= pos <= 8:
            raise ValueError(f"Invalid position: {pos}")

        abs_idx = FACE_OFFSETS[face] + pos
        new_stickers = list(self.stickers)
        new_stickers[abs_idx] = color
        return CubeState(new_stickers)

    def __eq__(self, other: object) -> bool:
        """
        Check equality based on sticker configuration.

        Two cubes are equal if all 54 stickers match.
        """
        if not isinstance(other, CubeState):
            return NotImplemented
        return self.stickers == other.stickers

    def __hash__(self) -> int:
        """
        Hash based on sticker tuple.

        Enables use in sets and as dict keys.
        """
        return hash(self.stickers)

    def __repr__(self) -> str:
        """
        Compact representation for debugging.
        """
        if self.is_solved():
            return "CubeState(solved)"
        return f"CubeState({len(self.stickers)} stickers)"

    def __str__(self) -> str:
        """
        Pretty-print the cube in unfolded format.

        Format:
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
        lines = []

        # Helper to get a row of 3 stickers
        def row(face: str, start_pos: int) -> str:
            offset = FACE_OFFSETS[face]
            return ' '.join(self.stickers[offset + start_pos + i] for i in range(3))

        # Up face (indented)
        for i in [0, 3, 6]:
            lines.append(f"      {row('U', i)}")

        # Middle row: L F R B
        for i in [0, 3, 6]:
            lines.append(f"{row('L', i)}   {row('F', i)}   {row('R', i)}   {row('B', i)}")

        # Down face (indented)
        for i in [0, 3, 6]:
            lines.append(f"      {row('D', i)}")

        return '\n'.join(lines)

    def validate(self) -> Tuple[bool, List[str]]:
        """
        Validate cube state for correctness.

        Checks:
          1. Exactly 9 stickers of each color
          2. Center stickers match expected colors

        Returns:
            (is_valid, error_messages)

        Note: This does NOT check orientation parity or permutation parity,
        which would require piece-level analysis.

        Example:
            >>> cube = CubeState.solved()
            >>> cube.validate()
            (True, [])
        """
        errors = []

        # Check color counts
        color_counts = {}
        for color in self.stickers:
            color_counts[color] = color_counts.get(color, 0) + 1

        for color, count in color_counts.items():
            if count != 9:
                errors.append(f"Color {color} appears {count} times (expected 9)")

        # Check we have exactly 6 colors
        if len(color_counts) != 6:
            errors.append(f"Found {len(color_counts)} colors (expected 6)")

        # Check center stickers match expected positions
        expected_centers = {
            4: SOLVED_COLORS['U'],   # U center
            13: SOLVED_COLORS['R'],  # R center
            22: SOLVED_COLORS['F'],  # F center
            31: SOLVED_COLORS['D'],  # D center
            40: SOLVED_COLORS['L'],  # L center
            49: SOLVED_COLORS['B'],  # B center
        }

        for idx, expected_color in expected_centers.items():
            actual_color = self.stickers[idx]
            if actual_color != expected_color:
                errors.append(
                    f"Center at position {idx} is {actual_color} "
                    f"(expected {expected_color})"
                )

        return (len(errors) == 0, errors)
