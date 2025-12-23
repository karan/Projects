"""
Cube Inspection Tools - For debugging and analyzing cube states.

This module provides tools to inspect cube state, find pieces,
and verify solver progress.

DESIGN PHILOSOPHY:
- No silent failures: Always raise exceptions with full context
- Bounded iterations: Prevent infinite loops with max_iterations guards
- Structured data: Use dataclasses instead of tuples for clarity
- Helpful errors: Include cube state in exceptions for debugging

WHY THIS MODULE EXISTS:
The original solver had "silent failure" bugs where find_edge would
return None and the solver would give up without explanation. This
made debugging nearly impossible.

New approach:
1. find_edge raises PieceNotFoundError with full cube state
2. Max iteration guards prevent infinite loops
3. Structured EdgeRef/CornerRef make code self-documenting
4. Verification functions (edge_solved, etc.) catch bugs early

See GUIDE_FOR_BEGINNERS.md for detailed examples.
"""

from typing import Tuple, Optional, List
from dataclasses import dataclass
from src.cube_state import CubeState


class PieceNotFoundError(Exception):
    """
    Raised when a piece cannot be found on the cube.

    WHY THIS IS BETTER THAN RETURNING None:
    - Old way: find_edge returns None → solver silently gives up
    - New way: find_edge raises exception → immediate, clear error

    The exception includes:
    1. Which piece was being searched for (colors)
    2. The full cube state (for debugging)
    3. Clear error message explaining what went wrong

    Example:
        >>> try:
        ...     edge = find_edge(cube, 'W', 'B')
        ... except PieceNotFoundError as e:
        ...     print(e)
        Piece with colors ('W', 'B') not found on cube.
        Cube state:
        [full cube visualization shown]

    This makes debugging 100x easier than "returned None somewhere."
    """

    def __init__(self, colors: Tuple[str, ...], cube_state: CubeState):
        self.colors = colors
        self.cube_state = cube_state
        super().__init__(
            f"Piece with colors {colors} not found on cube.\n"
            f"Cube state:\n{cube_state}"
        )


@dataclass
class EdgeRef:
    """
    Reference to an edge piece on the cube.

    WHY USE A DATACLASS INSTEAD OF A TUPLE?

    Old way (tuple):
        edge = ('U', 7, 'F', 1, 'W', 'B')  # What does each element mean? 🤔
        face1 = edge[0]  # Which index was face1? Must look it up every time

    New way (dataclass):
        edge = EdgeRef(face1='U', pos1=7, face2='F', pos2=1,
                       color1='W', color2='B')
        face1 = edge.face1  # Crystal clear! Self-documenting code ✓

    Benefits:
    1. Named fields make code self-documenting
    2. Impossible to mix up field order
    3. IDE autocomplete works
    4. Type hints prevent bugs
    5. __str__ method provides nice debugging output

    An edge piece has 2 stickers (one on each adjacent face):
    - face1, pos1: Location of first sticker
    - face2, pos2: Location of second sticker
    - color1, color2: Colors of those stickers
    """
    face1: str      # Face containing first sticker ('U', 'R', 'F', 'D', 'L', 'B')
    pos1: int       # Position on face1 (0-8)
    face2: str      # Face containing second sticker
    pos2: int       # Position on face2 (0-8)
    color1: str     # Color of sticker on face1
    color2: str     # Color of sticker on face2

    def __str__(self):
        return f"Edge({self.face1}[{self.pos1}]={self.color1}, {self.face2}[{self.pos2}]={self.color2})"


@dataclass
class CornerRef:
    """
    Reference to a corner piece on the cube.

    A corner piece has 3 stickers (one on each adjacent face):
    - face1, pos1: Location of first sticker
    - face2, pos2: Location of second sticker
    - face3, pos3: Location of third sticker
    - color1, color2, color3: Colors of those stickers

    Same benefits as EdgeRef - see EdgeRef docstring for explanation.
    """
    face1: str      # Face containing first sticker
    pos1: int       # Position on face1 (0-8)
    face2: str      # Face containing second sticker
    pos2: int       # Position on face2 (0-8)
    face3: str      # Face containing third sticker
    pos3: int       # Position on face3 (0-8)
    color1: str     # Color of sticker on face1
    color2: str     # Color of sticker on face2
    color3: str     # Color of sticker on face3

    def __str__(self):
        return f"Corner({self.face1}[{self.pos1}]={self.color1}, {self.face2}[{self.pos2}]={self.color2}, {self.face3}[{self.pos3}]={self.color3})"


# Edge piece definitions: (face, position, adjacent_face, adjacent_position)
EDGE_POSITIONS = [
    ('U', 1, 'B', 1),   # UB edge
    ('U', 3, 'L', 1),   # UL edge
    ('U', 5, 'R', 1),   # UR edge
    ('U', 7, 'F', 1),   # UF edge
    ('F', 3, 'L', 5),   # FL edge
    ('F', 5, 'R', 3),   # FR edge
    ('F', 7, 'D', 1),   # FD edge
    ('B', 3, 'R', 5),   # BR edge
    ('B', 5, 'L', 3),   # BL edge
    ('B', 7, 'D', 5),   # BD edge
    ('L', 7, 'D', 3),   # LD edge
    ('R', 7, 'D', 7),   # RD edge
]

# Corner piece definitions: (face, position, adjacent_face1, position1, adjacent_face2, position2)
CORNER_POSITIONS = [
    ('U', 0, 'L', 2, 'B', 2),   # ULB corner
    ('U', 2, 'B', 0, 'R', 2),   # UBR corner
    ('U', 6, 'F', 0, 'L', 0),   # UFL corner
    ('U', 8, 'R', 0, 'F', 2),   # URF corner
    ('D', 0, 'F', 6, 'L', 8),   # DFL corner
    ('D', 2, 'L', 6, 'B', 8),   # DLB corner
    ('D', 6, 'R', 8, 'F', 8),   # DRF corner
    ('D', 8, 'B', 6, 'R', 6),   # DBR corner
]


def find_edge(cube: CubeState, color1: str, color2: str,
              max_iterations: int = 24) -> EdgeRef:
    """
    Find an edge piece with the given colors.

    WHY max_iterations PARAMETER?
    Safety guard to prevent infinite loops in buggy solver code.

    Scenario without max_iterations:
        while not edge_at_target:
            edge = find_edge(cube, 'W', 'B')  # If buggy, might loop forever
            cube = try_to_move_edge(cube)     # If this never works, infinite loop!

    Scenario with max_iterations:
        while not edge_at_target:
            edge = find_edge(cube, 'W', 'B', max_iterations=24)
            # After 24 failed attempts, raises PieceNotFoundError
            # Program stops with helpful error instead of freezing!

    WHY 24? There are only 12 edges on a cube, so searching 24 positions
    (double the maximum) is more than enough. If we don't find it by then,
    something is fundamentally wrong with the cube state or search logic.

    Args:
        cube: Current cube state
        color1: First color
        color2: Second color
        max_iterations: Maximum search iterations (default 24, prevents infinite loops)

    Returns:
        EdgeRef containing edge information

    Raises:
        PieceNotFoundError: If edge not found within max_iterations
                           (Includes full cube state for debugging)
    """
    iterations = 0

    # Search all 12 edge positions on the cube
    for edge_def in EDGE_POSITIONS:
        iterations += 1

        # SAFETY: Check iteration count to prevent infinite loops
        if iterations > max_iterations:
            raise PieceNotFoundError((color1, color2), cube)

        # Extract position information from edge definition
        face1, pos1, face2, pos2 = edge_def

        # Get actual colors at these positions
        sticker1 = cube.get_sticker(face1, pos1)
        sticker2 = cube.get_sticker(face2, pos2)

        # Check if this edge matches (order doesn't matter)
        # Example: ('W', 'B') matches both ('W', 'B') and ('B', 'W')
        if (sticker1 == color1 and sticker2 == color2) or \
           (sticker1 == color2 and sticker2 == color1):
            # Found it! Return structured reference
            return EdgeRef(face1, pos1, face2, pos2, sticker1, sticker2)

    # Searched all 12 edges, none matched
    # This means either:
    # 1. Cube state is corrupted (bug in moves)
    # 2. Colors specified incorrectly
    # 3. Piece doesn't exist (invalid color combination)
    raise PieceNotFoundError((color1, color2), cube)


def find_corner(cube: CubeState, color1: str, color2: str, color3: str,
                max_iterations: int = 24) -> CornerRef:
    """
    Find a corner piece with the given colors (in any order).

    Args:
        cube: Current cube state
        color1: First color
        color2: Second color
        color3: Third color
        max_iterations: Maximum search iterations

    Returns:
        CornerRef containing corner information

    Raises:
        PieceNotFoundError: If corner not found within max_iterations
    """
    colors = {color1, color2, color3}
    iterations = 0

    for corner_def in CORNER_POSITIONS:
        iterations += 1
        if iterations > max_iterations:
            raise PieceNotFoundError((color1, color2, color3), cube)

        face1, pos1, face2, pos2, face3, pos3 = corner_def
        sticker1 = cube.get_sticker(face1, pos1)
        sticker2 = cube.get_sticker(face2, pos2)
        sticker3 = cube.get_sticker(face3, pos3)

        if {sticker1, sticker2, sticker3} == colors:
            return CornerRef(face1, pos1, face2, pos2, face3, pos3,
                           sticker1, sticker2, sticker3)

    raise PieceNotFoundError((color1, color2, color3), cube)


def edge_solved(cube: CubeState, edge: EdgeRef) -> bool:
    """
    Check if an edge is in its solved position with correct orientation.

    Args:
        cube: Current cube state
        edge: Edge reference

    Returns:
        True if edge is solved
    """
    # Get target colors based on center colors
    target1 = cube.get_sticker(edge.face1, 4)  # Center of face1
    target2 = cube.get_sticker(edge.face2, 4)  # Center of face2

    # Check if edge matches center colors
    current1 = cube.get_sticker(edge.face1, edge.pos1)
    current2 = cube.get_sticker(edge.face2, edge.pos2)

    return current1 == target1 and current2 == target2


def corner_solved(cube: CubeState, corner: CornerRef) -> bool:
    """
    Check if a corner is in its solved position with correct orientation.

    Args:
        cube: Current cube state
        corner: Corner reference

    Returns:
        True if corner is solved
    """
    # Get target colors based on center colors
    target1 = cube.get_sticker(corner.face1, 4)
    target2 = cube.get_sticker(corner.face2, 4)
    target3 = cube.get_sticker(corner.face3, 4)

    # Check if corner matches center colors
    current1 = cube.get_sticker(corner.face1, corner.pos1)
    current2 = cube.get_sticker(corner.face2, corner.pos2)
    current3 = cube.get_sticker(corner.face3, corner.pos3)

    return (current1 == target1 and current2 == target2 and current3 == target3)


def edge_oriented(cube: CubeState, edge: EdgeRef, primary_face: str) -> bool:
    """
    Check if an edge is oriented correctly relative to a primary face.

    An edge is "oriented" if its primary face color (e.g., white for top layer)
    is on the correct face.

    Args:
        cube: Current cube state
        edge: Edge reference
        primary_face: The primary face to check orientation against

    Returns:
        True if edge is oriented correctly
    """
    primary_color = cube.get_sticker(primary_face, 4)  # Center color

    # Check if the primary color is on the primary face side of the edge
    if edge.face1 == primary_face:
        return cube.get_sticker(edge.face1, edge.pos1) == primary_color
    elif edge.face2 == primary_face:
        return cube.get_sticker(edge.face2, edge.pos2) == primary_color
    else:
        # Edge doesn't touch primary face
        return False


def cube_to_pretty_string(cube: CubeState, highlight_positions: Optional[List[Tuple[str, int]]] = None) -> str:
    """
    Create a pretty string representation of the cube with optional highlighting.

    Args:
        cube: Cube state to display
        highlight_positions: List of (face, position) tuples to highlight

    Returns:
        Pretty formatted string
    """
    highlight_set = set(highlight_positions) if highlight_positions else set()

    def format_sticker(face: str, pos: int) -> str:
        sticker = cube.get_sticker(face, pos)
        if (face, pos) in highlight_set:
            return f"[{sticker}]"
        return f" {sticker} "

    lines = []
    lines.append("=" * 60)
    lines.append("CUBE STATE")
    lines.append("=" * 60)
    lines.append("")

    # Top face (U)
    lines.append("         UP (U)")
    for row in range(3):
        line = "      "
        for col in range(3):
            pos = row * 3 + col
            line += format_sticker('U', pos)
        lines.append(line)

    lines.append("")
    lines.append("LEFT(L)   FRONT(F)   RIGHT(R)   BACK(B)")

    # Middle row
    for row in range(3):
        line = ""
        for face in ['L', 'F', 'R', 'B']:
            for col in range(3):
                pos = row * 3 + col
                line += format_sticker(face, pos)
            line += "  "
        lines.append(line)

    lines.append("")
    lines.append("        DOWN (D)")

    # Bottom face (D)
    for row in range(3):
        line = "      "
        for col in range(3):
            pos = row * 3 + col
            line += format_sticker('D', pos)
        lines.append(line)

    lines.append("")
    lines.append("=" * 60)

    return '\n'.join(lines)


def count_solved_pieces(cube: CubeState) -> Tuple[int, int]:
    """
    Count how many edges and corners are solved.

    Args:
        cube: Cube state

    Returns:
        Tuple of (solved_edges, solved_corners)
    """
    solved_edges = 0
    solved_corners = 0

    # Check edges
    for edge_def in EDGE_POSITIONS:
        face1, pos1, face2, pos2 = edge_def
        edge = EdgeRef(face1, pos1, face2, pos2,
                      cube.get_sticker(face1, pos1),
                      cube.get_sticker(face2, pos2))
        if edge_solved(cube, edge):
            solved_edges += 1

    # Check corners
    for corner_def in CORNER_POSITIONS:
        face1, pos1, face2, pos2, face3, pos3 = corner_def
        corner = CornerRef(face1, pos1, face2, pos2, face3, pos3,
                          cube.get_sticker(face1, pos1),
                          cube.get_sticker(face2, pos2),
                          cube.get_sticker(face3, pos3))
        if corner_solved(cube, corner):
            solved_corners += 1

    return (solved_edges, solved_corners)
