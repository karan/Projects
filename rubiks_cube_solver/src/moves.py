"""
Moves: Rubik's Cube move definitions and execution.

This module implements the 6 basic moves (U, R, F, D, L, B) and their variations.
Each move rotates one face and cycles adjacent stickers.

Move notation:
    X   - Clockwise 90° turn of face X
    X'  - Counter-clockwise 90° turn of face X (inverse)
    X2  - 180° turn of face X (apply X twice)
"""

from typing import List
from src.cube_state import CubeState


def rotate_face_cw(face: List[str]) -> List[str]:
    """
    Rotate a face 90° clockwise.

    Original:       After rotation:
    0 1 2           6 3 0
    3 4 5    =>     7 4 1
    6 7 8           8 5 2

    Args:
        face: List of 9 stickers

    Returns:
        Rotated face
    """
    return [
        face[6], face[3], face[0],
        face[7], face[4], face[1],
        face[8], face[5], face[2]
    ]


def rotate_face_ccw(face: List[str]) -> List[str]:
    """
    Rotate a face 90° counter-clockwise.

    Original:       After rotation:
    0 1 2           2 5 8
    3 4 5    =>     1 4 7
    6 7 8           0 3 6

    Args:
        face: List of 9 stickers

    Returns:
        Rotated face
    """
    return [
        face[2], face[5], face[8],
        face[1], face[4], face[7],
        face[0], face[3], face[6]
    ]


def apply_U(cube: CubeState) -> CubeState:
    """
    Apply U (Up) move: Rotate top face clockwise.

    This affects:
    - U face: rotates clockwise
    - Top row of F, R, B, L: cycle clockwise (F -> R -> B -> L -> F)

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate U face clockwise
    u_face = rotate_face_cw(new_cube.get_face('U'))
    for i in range(9):
        new_cube.set_sticker('U', i, u_face[i])

    # Save the top row of each affected face
    f_top = [cube.get_sticker('F', i) for i in [0, 1, 2]]
    r_top = [cube.get_sticker('R', i) for i in [0, 1, 2]]
    b_top = [cube.get_sticker('B', i) for i in [0, 1, 2]]
    l_top = [cube.get_sticker('L', i) for i in [0, 1, 2]]

    # Cycle: F -> R -> B -> L -> F
    for i in range(3):
        new_cube.set_sticker('R', i, f_top[i])
        new_cube.set_sticker('B', i, r_top[i])
        new_cube.set_sticker('L', i, b_top[i])
        new_cube.set_sticker('F', i, l_top[i])

    return new_cube


def apply_U_prime(cube: CubeState) -> CubeState:
    """
    Apply U' (Up inverse): Rotate top face counter-clockwise.

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate U face counter-clockwise
    u_face = rotate_face_ccw(new_cube.get_face('U'))
    for i in range(9):
        new_cube.set_sticker('U', i, u_face[i])

    # Save the top row of each affected face
    f_top = [cube.get_sticker('F', i) for i in [0, 1, 2]]
    r_top = [cube.get_sticker('R', i) for i in [0, 1, 2]]
    b_top = [cube.get_sticker('B', i) for i in [0, 1, 2]]
    l_top = [cube.get_sticker('L', i) for i in [0, 1, 2]]

    # Cycle: F -> L -> B -> R -> F
    for i in range(3):
        new_cube.set_sticker('L', i, f_top[i])
        new_cube.set_sticker('B', i, l_top[i])
        new_cube.set_sticker('R', i, b_top[i])
        new_cube.set_sticker('F', i, r_top[i])

    return new_cube


def apply_R(cube: CubeState) -> CubeState:
    """
    Apply R (Right) move: Rotate right face clockwise.

    This affects:
    - R face: rotates clockwise
    - Right column of U, F, D, B: cycle (U -> F -> D -> B -> U)

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate R face clockwise
    r_face = rotate_face_cw(new_cube.get_face('R'))
    for i in range(9):
        new_cube.set_sticker('R', i, r_face[i])

    # Save the right column of each affected face
    # U right column: positions 2, 5, 8
    # F right column: positions 2, 5, 8
    # D right column: positions 2, 5, 8
    # B left column (when viewed from front): positions 6, 3, 0
    u_col = [cube.get_sticker('U', i) for i in [2, 5, 8]]
    f_col = [cube.get_sticker('F', i) for i in [2, 5, 8]]
    d_col = [cube.get_sticker('D', i) for i in [2, 5, 8]]
    b_col = [cube.get_sticker('B', i) for i in [6, 3, 0]]  # Reversed

    # Cycle: U -> F -> D -> B -> U
    for i, pos in enumerate([2, 5, 8]):
        new_cube.set_sticker('F', pos, u_col[i])
        new_cube.set_sticker('D', pos, f_col[i])

    # B is reversed
    for i, pos in enumerate([6, 3, 0]):
        new_cube.set_sticker('B', pos, d_col[i])

    for i, pos in enumerate([2, 5, 8]):
        new_cube.set_sticker('U', pos, b_col[2 - i])

    return new_cube


def apply_R_prime(cube: CubeState) -> CubeState:
    """
    Apply R' (Right inverse): Rotate right face counter-clockwise.

    CRITICAL: This is the inverse of apply_R. It must undo R exactly.
    Mathematical property: apply_R(apply_R_prime(cube)) = cube

    The R' move cycles edge stickers in the OPPOSITE direction of R:
    - R cycles: U -> F -> D -> B -> U (clockwise when viewing from right)
    - R' cycles: U -> B -> D -> F -> U (counter-clockwise)

    Args:
        cube: Current cube state

    Returns:
        New cube state after move

    Bug History:
        - Original bug (line 209): Used b_col[2-i] instead of b_col[i]
        - This caused R followed by R' to NOT return to identity
        - Fixed 2024: Changed to b_col[i] (correct indexing)
        - See DEBUGGING_NOTES.md for full analysis
    """
    new_cube = cube.copy()

    # Rotate R face counter-clockwise (this part was always correct)
    r_face = rotate_face_ccw(new_cube.get_face('R'))
    for i in range(9):
        new_cube.set_sticker('R', i, r_face[i])

    # Save the edge columns that will be cycled
    # WHY these positions? The R face touches:
    # - U face right column: positions 2, 5, 8
    # - F face right column: positions 2, 5, 8
    # - D face right column: positions 2, 5, 8
    # - B face LEFT column (when viewed from behind): positions 6, 3, 0
    #   (reversed because back face is mirror image)
    u_col = [cube.get_sticker('U', i) for i in [2, 5, 8]]
    f_col = [cube.get_sticker('F', i) for i in [2, 5, 8]]
    d_col = [cube.get_sticker('D', i) for i in [2, 5, 8]]
    b_col = [cube.get_sticker('B', i) for i in [6, 3, 0]]  # Reversed order

    # Cycle stickers in COUNTER-CLOCKWISE direction: U -> B -> D -> F -> U

    # Step 1: U -> B (reversed because back face orientation)
    # WHY reversed? The U[2,5,8] column maps to B[6,3,0] in reverse order
    # U[2] (top-right of U) connects to B[6] (bottom-left when viewed from behind)
    for i, pos in enumerate([6, 3, 0]):
        new_cube.set_sticker('B', pos, u_col[2 - i])  # Reverse mapping

    # Step 2: F -> U (direct mapping, same order)
    # Step 3: D -> F (direct mapping, same order)
    for i, pos in enumerate([2, 5, 8]):
        new_cube.set_sticker('U', pos, f_col[i])
        new_cube.set_sticker('F', pos, d_col[i])

    # Step 4: B -> D (direct mapping - CRITICAL BUG WAS HERE!)
    # BEFORE (BUGGY): new_cube.set_sticker('D', pos, b_col[2 - i])
    # - This incorrectly reversed the B column again
    # - Combined with the already-reversed b_col indices, this double-reversed
    # - Result: D face got wrong sticker order after R'
    # - When doing R then R', the D face didn't return to original
    #
    # AFTER (CORRECT): new_cube.set_sticker('D', pos, b_col[i])
    # - b_col is already in positions [6,3,0] (reversed)
    # - We apply it directly to D[2,5,8] (no additional reversal)
    # - This gives correct mapping: B[6]->D[2], B[3]->D[5], B[0]->D[8]
    for i, pos in enumerate([2, 5, 8]):
        new_cube.set_sticker('D', pos, b_col[i])  # ✓ FIXED: No reversal here!

    return new_cube


def apply_F(cube: CubeState) -> CubeState:
    """
    Apply F (Front) move: Rotate front face clockwise.

    This affects:
    - F face: rotates clockwise
    - Bottom row of U, right column of L, top row of D, left column of R

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate F face clockwise
    f_face = rotate_face_cw(new_cube.get_face('F'))
    for i in range(9):
        new_cube.set_sticker('F', i, f_face[i])

    # Save affected edges
    u_bottom = [cube.get_sticker('U', i) for i in [6, 7, 8]]
    r_left = [cube.get_sticker('R', i) for i in [0, 3, 6]]
    d_top = [cube.get_sticker('D', i) for i in [2, 1, 0]]  # Reversed
    l_right = [cube.get_sticker('L', i) for i in [8, 5, 2]]  # Reversed

    # Cycle: U -> R -> D -> L -> U
    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('R', pos, u_bottom[i])

    for i, pos in enumerate([2, 1, 0]):
        new_cube.set_sticker('D', pos, r_left[i])

    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('L', pos, d_top[i])

    for i, pos in enumerate([6, 7, 8]):
        new_cube.set_sticker('U', pos, l_right[i])

    return new_cube


def apply_F_prime(cube: CubeState) -> CubeState:
    """
    Apply F' (Front inverse): Rotate front face counter-clockwise.

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate F face counter-clockwise
    f_face = rotate_face_ccw(new_cube.get_face('F'))
    for i in range(9):
        new_cube.set_sticker('F', i, f_face[i])

    # Save affected edges
    u_bottom = [cube.get_sticker('U', i) for i in [6, 7, 8]]
    r_left = [cube.get_sticker('R', i) for i in [0, 3, 6]]
    d_top = [cube.get_sticker('D', i) for i in [2, 1, 0]]
    l_right = [cube.get_sticker('L', i) for i in [8, 5, 2]]

    # Cycle: U -> L -> D -> R -> U
    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('L', pos, u_bottom[i])

    for i, pos in enumerate([6, 7, 8]):
        new_cube.set_sticker('U', pos, r_left[i])

    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('R', pos, d_top[i])

    for i, pos in enumerate([2, 1, 0]):
        new_cube.set_sticker('D', pos, l_right[i])

    return new_cube


def apply_D(cube: CubeState) -> CubeState:
    """
    Apply D (Down) move: Rotate bottom face clockwise.

    This affects:
    - D face: rotates clockwise
    - Bottom row of F, L, B, R: cycle (F -> L -> B -> R -> F)

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate D face clockwise
    d_face = rotate_face_cw(new_cube.get_face('D'))
    for i in range(9):
        new_cube.set_sticker('D', i, d_face[i])

    # Save bottom rows
    f_bottom = [cube.get_sticker('F', i) for i in [6, 7, 8]]
    l_bottom = [cube.get_sticker('L', i) for i in [6, 7, 8]]
    b_bottom = [cube.get_sticker('B', i) for i in [6, 7, 8]]
    r_bottom = [cube.get_sticker('R', i) for i in [6, 7, 8]]

    # Cycle: F -> L -> B -> R -> F
    for i in range(3):
        new_cube.set_sticker('L', 6 + i, f_bottom[i])
        new_cube.set_sticker('B', 6 + i, l_bottom[i])
        new_cube.set_sticker('R', 6 + i, b_bottom[i])
        new_cube.set_sticker('F', 6 + i, r_bottom[i])

    return new_cube


def apply_D_prime(cube: CubeState) -> CubeState:
    """
    Apply D' (Down inverse): Rotate bottom face counter-clockwise.

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate D face counter-clockwise
    d_face = rotate_face_ccw(new_cube.get_face('D'))
    for i in range(9):
        new_cube.set_sticker('D', i, d_face[i])

    # Save bottom rows
    f_bottom = [cube.get_sticker('F', i) for i in [6, 7, 8]]
    l_bottom = [cube.get_sticker('L', i) for i in [6, 7, 8]]
    b_bottom = [cube.get_sticker('B', i) for i in [6, 7, 8]]
    r_bottom = [cube.get_sticker('R', i) for i in [6, 7, 8]]

    # Cycle: F -> R -> B -> L -> F
    for i in range(3):
        new_cube.set_sticker('R', 6 + i, f_bottom[i])
        new_cube.set_sticker('B', 6 + i, r_bottom[i])
        new_cube.set_sticker('L', 6 + i, b_bottom[i])
        new_cube.set_sticker('F', 6 + i, l_bottom[i])

    return new_cube


def apply_L(cube: CubeState) -> CubeState:
    """
    Apply L (Left) move: Rotate left face clockwise.

    This affects:
    - L face: rotates clockwise
    - Left column of U, B, D, F: cycle

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate L face clockwise
    l_face = rotate_face_cw(new_cube.get_face('L'))
    for i in range(9):
        new_cube.set_sticker('L', i, l_face[i])

    # Save left columns
    u_col = [cube.get_sticker('U', i) for i in [0, 3, 6]]
    f_col = [cube.get_sticker('F', i) for i in [0, 3, 6]]
    d_col = [cube.get_sticker('D', i) for i in [0, 3, 6]]
    b_col = [cube.get_sticker('B', i) for i in [8, 5, 2]]  # Reversed

    # Cycle: U -> B -> D -> F -> U
    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('B', pos, u_col[2 - i])

    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('U', pos, f_col[i])
        new_cube.set_sticker('F', pos, d_col[i])

    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('D', pos, b_col[2 - i])

    return new_cube


def apply_L_prime(cube: CubeState) -> CubeState:
    """
    Apply L' (Left inverse): Rotate left face counter-clockwise.

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate L face counter-clockwise
    l_face = rotate_face_ccw(new_cube.get_face('L'))
    for i in range(9):
        new_cube.set_sticker('L', i, l_face[i])

    # Save left columns
    u_col = [cube.get_sticker('U', i) for i in [0, 3, 6]]
    f_col = [cube.get_sticker('F', i) for i in [0, 3, 6]]
    d_col = [cube.get_sticker('D', i) for i in [0, 3, 6]]
    b_col = [cube.get_sticker('B', i) for i in [8, 5, 2]]

    # Cycle: U -> F -> D -> B -> U
    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('F', pos, u_col[i])
        new_cube.set_sticker('D', pos, f_col[i])

    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('B', pos, d_col[2 - i])

    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('U', pos, b_col[2 - i])

    return new_cube


def apply_B(cube: CubeState) -> CubeState:
    """
    Apply B (Back) move: Rotate back face clockwise.

    This affects:
    - B face: rotates clockwise
    - Top row of U, left column of R, bottom row of D, right column of L

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate B face clockwise
    b_face = rotate_face_cw(new_cube.get_face('B'))
    for i in range(9):
        new_cube.set_sticker('B', i, b_face[i])

    # Save affected edges
    u_top = [cube.get_sticker('U', i) for i in [2, 1, 0]]  # Reversed
    l_left = [cube.get_sticker('L', i) for i in [0, 3, 6]]
    d_bottom = [cube.get_sticker('D', i) for i in [6, 7, 8]]
    r_right = [cube.get_sticker('R', i) for i in [8, 5, 2]]  # Reversed

    # Cycle: U -> L -> D -> R -> U
    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('L', pos, u_top[i])

    for i, pos in enumerate([6, 7, 8]):
        new_cube.set_sticker('D', pos, l_left[i])

    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('R', pos, d_bottom[i])

    for i, pos in enumerate([2, 1, 0]):
        new_cube.set_sticker('U', pos, r_right[i])

    return new_cube


def apply_B_prime(cube: CubeState) -> CubeState:
    """
    Apply B' (Back inverse): Rotate back face counter-clockwise.

    Args:
        cube: Current cube state

    Returns:
        New cube state after move
    """
    new_cube = cube.copy()

    # Rotate B face counter-clockwise
    b_face = rotate_face_ccw(new_cube.get_face('B'))
    for i in range(9):
        new_cube.set_sticker('B', i, b_face[i])

    # Save affected edges
    u_top = [cube.get_sticker('U', i) for i in [2, 1, 0]]
    l_left = [cube.get_sticker('L', i) for i in [0, 3, 6]]
    d_bottom = [cube.get_sticker('D', i) for i in [6, 7, 8]]
    r_right = [cube.get_sticker('R', i) for i in [8, 5, 2]]

    # Cycle: U -> R -> D -> L -> U
    for i, pos in enumerate([8, 5, 2]):
        new_cube.set_sticker('R', pos, u_top[i])

    for i, pos in enumerate([2, 1, 0]):
        new_cube.set_sticker('U', pos, l_left[i])

    for i, pos in enumerate([0, 3, 6]):
        new_cube.set_sticker('L', pos, d_bottom[i])

    for i, pos in enumerate([6, 7, 8]):
        new_cube.set_sticker('D', pos, r_right[i])

    return new_cube


# Move registry: maps move notation to function
MOVE_FUNCTIONS = {
    'U': apply_U,
    "U'": apply_U_prime,
    'R': apply_R,
    "R'": apply_R_prime,
    'F': apply_F,
    "F'": apply_F_prime,
    'D': apply_D,
    "D'": apply_D_prime,
    'L': apply_L,
    "L'": apply_L_prime,
    'B': apply_B,
    "B'": apply_B_prime,
}


def apply_move(cube: CubeState, move: str) -> CubeState:
    """
    Apply a single move to a cube.

    Args:
        cube: Current cube state
        move: Move notation (e.g., 'U', "R'", 'F2')

    Returns:
        New cube state after applying the move

    Raises:
        ValueError: If move notation is invalid
    """
    # Handle double moves (X2)
    if move.endswith('2'):
        base_move = move[0]
        cube = apply_move(cube, base_move)
        cube = apply_move(cube, base_move)
        return cube

    if move not in MOVE_FUNCTIONS:
        raise ValueError(f"Invalid move: {move}")

    return MOVE_FUNCTIONS[move](cube)


def apply_algorithm(cube: CubeState, algorithm: str) -> CubeState:
    """
    Apply a sequence of moves (algorithm) to a cube.

    Args:
        cube: Current cube state
        algorithm: Space-separated moves (e.g., "R U R' U'")

    Returns:
        New cube state after applying all moves
    """
    moves = algorithm.split()
    for move in moves:
        if move:  # Skip empty strings
            cube = apply_move(cube, move)
    return cube


def apply_move_sequence(cube: CubeState, moves: List[str]) -> CubeState:
    """
    Apply a sequence of moves to a cube.

    Args:
        cube: Current cube state
        moves: List of move notations

    Returns:
        New cube state after applying all moves
    """
    for move in moves:
        cube = apply_move(cube, move)
    return cube
