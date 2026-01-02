"""
Utilities: Helper functions for the Rubik's Cube solver.

This module provides utility functions to:
- Find specific pieces on the cube
- Check piece orientations
- Identify piece positions
"""

from typing import Tuple, List, Optional
from src.cube_state import CubeState


# Edge piece positions: (face, position, adjacent_face, adjacent_position)
# Each edge is defined by its two stickers
EDGES = [
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

# Corner piece positions: (face, position, adjacent_face1, position1, adjacent_face2, position2)
# Each corner is defined by its three stickers
CORNERS = [
    ('U', 0, 'L', 2, 'B', 2),   # ULB corner
    ('U', 2, 'B', 0, 'R', 2),   # UBR corner
    ('U', 6, 'F', 0, 'L', 0),   # UFL corner
    ('U', 8, 'R', 0, 'F', 2),   # URF corner
    ('D', 0, 'F', 6, 'L', 8),   # DFL corner
    ('D', 2, 'L', 6, 'B', 8),   # DLB corner
    ('D', 6, 'R', 8, 'F', 8),   # DRF corner
    ('D', 8, 'B', 6, 'R', 6),   # DBR corner
]


def find_edge(cube: CubeState, color1: str, color2: str) -> Optional[Tuple]:
    """
    Find an edge piece with the given colors.

    Args:
        cube: Current cube state
        color1: First color
        color2: Second color

    Returns:
        Tuple (face, position, adjacent_face, adjacent_position) or None if not found
    """
    for edge in EDGES:
        face, pos, adj_face, adj_pos = edge
        sticker1 = cube.get_sticker(face, pos)
        sticker2 = cube.get_sticker(adj_face, adj_pos)

        if (sticker1 == color1 and sticker2 == color2) or \
           (sticker1 == color2 and sticker2 == color1):
            return edge

    return None


def find_corner(cube: CubeState, color1: str, color2: str, color3: str) -> Optional[Tuple]:
    """
    Find a corner piece with the given colors (in any order).

    Args:
        cube: Current cube state
        color1: First color
        color2: Second color
        color3: Third color

    Returns:
        Tuple (face, pos, adj_face1, pos1, adj_face2, pos2) or None if not found
    """
    colors = {color1, color2, color3}

    for corner in CORNERS:
        face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner
        sticker1 = cube.get_sticker(face, pos)
        sticker2 = cube.get_sticker(adj_face1, adj_pos1)
        sticker3 = cube.get_sticker(adj_face2, adj_pos2)

        if {sticker1, sticker2, sticker3} == colors:
            return corner

    return None


def get_edge_colors(cube: CubeState, edge: Tuple) -> Tuple[str, str]:
    """
    Get the colors of an edge piece.

    Args:
        cube: Current cube state
        edge: Edge definition tuple

    Returns:
        Tuple of (color1, color2)
    """
    face, pos, adj_face, adj_pos = edge
    return (cube.get_sticker(face, pos), cube.get_sticker(adj_face, adj_pos))


def get_corner_colors(cube: CubeState, corner: Tuple) -> Tuple[str, str, str]:
    """
    Get the colors of a corner piece.

    Args:
        cube: Current cube state
        corner: Corner definition tuple

    Returns:
        Tuple of (color1, color2, color3)
    """
    face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner
    return (
        cube.get_sticker(face, pos),
        cube.get_sticker(adj_face1, adj_pos1),
        cube.get_sticker(adj_face2, adj_pos2)
    )


def is_white_cross_solved(cube: CubeState) -> bool:
    """
    Check if the white cross is solved.

    The white cross is solved when:
    1. All 4 edges on U face are white
    2. The side colors match the center colors

    Args:
        cube: Current cube state

    Returns:
        True if white cross is solved
    """
    # Check U face edges are white
    if cube.get_sticker('U', 1) != 'W':
        return False
    if cube.get_sticker('U', 3) != 'W':
        return False
    if cube.get_sticker('U', 5) != 'W':
        return False
    if cube.get_sticker('U', 7) != 'W':
        return False

    # Check side colors match centers
    if cube.get_sticker('F', 1) != 'B':  # Front center is Blue
        return False
    if cube.get_sticker('R', 1) != 'R':  # Right center is Red
        return False
    if cube.get_sticker('B', 1) != 'G':  # Back center is Green
        return False
    if cube.get_sticker('L', 1) != 'O':  # Left center is Orange
        return False

    return True


def is_white_face_solved(cube: CubeState) -> bool:
    """
    Check if the entire white face is solved (cross + corners).

    Args:
        cube: Current cube state

    Returns:
        True if white face is solved
    """
    # Check all U face stickers are white
    u_face = cube.get_face('U')
    if not all(sticker == 'W' for sticker in u_face):
        return False

    # Check first row of side faces match centers
    if cube.get_sticker('F', 0) != 'B' or cube.get_sticker('F', 2) != 'B':
        return False
    if cube.get_sticker('R', 0) != 'R' or cube.get_sticker('R', 2) != 'R':
        return False
    if cube.get_sticker('B', 0) != 'G' or cube.get_sticker('B', 2) != 'G':
        return False
    if cube.get_sticker('L', 0) != 'O' or cube.get_sticker('L', 2) != 'O':
        return False

    return True


def is_middle_layer_solved(cube: CubeState) -> bool:
    """
    Check if the middle layer is solved (first two layers complete).

    Args:
        cube: Current cube state

    Returns:
        True if middle layer is solved
    """
    # White face must be solved
    if not is_white_face_solved(cube):
        return False

    # Check middle row of side faces
    for face in ['F', 'R', 'B', 'L']:
        center = cube.get_sticker(face, 4)
        if cube.get_sticker(face, 3) != center:
            return False
        if cube.get_sticker(face, 5) != center:
            return False

    return True
