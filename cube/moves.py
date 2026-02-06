"""
Rubik's Cube Move Transformations.

This module defines all legal moves on a Rubik's Cube as pure permutations.

Move Notation:
-------------
  U, R, F, D, L, B    - 90° clockwise rotation of that face
  U', R', F', D', L', B' - 90° counter-clockwise (inverse)
  U2, R2, F2, D2, L2, B2 - 180° rotation (double turn)

Mathematical Properties:
-----------------------
Every move M satisfies:
  1. M^4 = identity (four 90° turns return to start)
  2. M · M' = identity (move followed by inverse returns to start)
  3. (M2)^2 = identity (double turn twice returns to start)
  4. Moves are bijections (permutations of 54 positions)
  5. Opposite faces commute: U·D = D·U, R·L = L·R, F·B = B·F

Implementation:
--------------
Moves are defined as permutation arrays mapping old indices to new indices.
This ensures:
  - Deterministic behavior
  - Easy composition
  - Mathematically verifiable correctness

Face Rotation Pattern:
---------------------
When rotating a face clockwise (viewed from that face):
  Corner cycle: 0→2→8→6→0
  Edge cycle: 1→5→7→3→1
  Center (4) stays fixed

Adjacent sticker cycles depend on the specific face being rotated.
See individual move functions for detailed mappings.
"""

from typing import List, Tuple
from .state import CubeState


# ============================================================================
# Core Move Definitions
# ============================================================================

def _apply_permutation(cube: CubeState, perm: List[int]) -> CubeState:
    """
    Apply a permutation to cube stickers.

    Args:
        cube: Current cube state
        perm: List of 54 integers where perm[i] = j means
              new_stickers[i] = old_stickers[j]

    Returns:
        New CubeState with permutation applied

    Mathematical note:
        This implements permutation composition: new = perm ∘ old
        where ∘ denotes function composition.
    """
    new_stickers = [cube.stickers[perm[i]] for i in range(54)]
    return CubeState(new_stickers)


def _rotate_face_cw(face_offset: int) -> List[int]:
    """
    Generate permutation for clockwise 90° face rotation.

    When viewing a face directly, clockwise rotation transforms:
        0 1 2       6 3 0
        3 4 5  -->  7 4 1
        6 7 8       8 5 2

    Cycles:
        Corners: 0→2→8→6→0
        Edges:   1→5→7→3→1
        Center:  4→4 (fixed)

    Args:
        face_offset: Starting index of face (0 for U, 9 for R, etc.)

    Returns:
        Permutation indices for this face's rotation
    """
    # Identity for all 54 positions
    perm = list(range(54))

    # Apply the rotation cycle to this face
    # Corner cycle: 0→2, 2→8, 8→6, 6→0
    perm[face_offset + 0] = face_offset + 6
    perm[face_offset + 2] = face_offset + 0
    perm[face_offset + 8] = face_offset + 2
    perm[face_offset + 6] = face_offset + 8

    # Edge cycle: 1→5, 5→7, 7→3, 3→1
    perm[face_offset + 1] = face_offset + 3
    perm[face_offset + 5] = face_offset + 1
    perm[face_offset + 7] = face_offset + 5
    perm[face_offset + 3] = face_offset + 7

    # Center stays fixed (perm[face_offset + 4] = face_offset + 4)

    return perm


def apply_U(cube: CubeState) -> CubeState:
    """
    Apply U (Up face clockwise 90°).

    Face rotation: U face rotates clockwise
    Adjacent cycles: Top row of F, R, B, L cycle clockwise

    Cycles:
        U face: 0→2→8→6→0, 1→5→7→3→1
        Adjacent: F[0,1,2] → R[0,1,2] → B[0,1,2] → L[0,1,2] → F[0,1,2]

    Mathematical verification:
        - U^4 = identity
        - U · U' = identity
        - U commutes with D (U·D = D·U)
    """
    perm = _rotate_face_cw(0)  # Rotate U face (offset 0)

    # Cycle top rows: F → R → B → L → F
    # F top row: 18, 19, 20
    # R top row: 9, 10, 11
    # B top row: 45, 46, 47
    # L top row: 36, 37, 38

    for i in range(3):
        perm[9 + i] = 18 + i    # R gets F
        perm[45 + i] = 9 + i     # B gets R
        perm[36 + i] = 45 + i    # L gets B
        perm[18 + i] = 36 + i    # F gets L

    return _apply_permutation(cube, perm)


def apply_U_prime(cube: CubeState) -> CubeState:
    """
    Apply U' (Up face counter-clockwise 90°).

    This is the inverse of apply_U.
    Equivalent to applying U three times: U' = U^3

    Mathematical property: U · U' = identity
    """
    # Apply U three times (U' = U^3)
    cube = apply_U(cube)
    cube = apply_U(cube)
    cube = apply_U(cube)
    return cube


def apply_U2(cube: CubeState) -> CubeState:
    """
    Apply U2 (Up face 180°).

    This is a double turn.
    Equivalent to applying U twice: U2 = U · U

    Mathematical property: (U2)^2 = identity
    """
    cube = apply_U(cube)
    cube = apply_U(cube)
    return cube


def apply_R(cube: CubeState) -> CubeState:
    """
    Apply R (Right face clockwise 90°).

    Face rotation: R face rotates clockwise (when viewing from right)
    Adjacent cycles: Right column of U, F, D, B cycle

    Cycles:
        R face: 9→11→17→15→9, 10→14→16→12→10
        Adjacent: U[2,5,8] → F[2,5,8] → D[2,5,8] → B[6,3,0] → U[2,5,8]
                  (Note: B column is reversed due to orientation)

    Mathematical verification:
        - R^4 = identity
        - R · R' = identity
        - R commutes with L (R·L = L·R)
    """
    perm = _rotate_face_cw(9)  # Rotate R face (offset 9)

    # Cycle right columns: U → F → D → B → U
    # U right column: 2, 5, 8
    # F right column: 20, 23, 26
    # D right column: 29, 32, 35
    # B left column (reversed): 51, 48, 45

    perm[20] = 2    # F[2] gets U[2]
    perm[23] = 5    # F[5] gets U[5]
    perm[26] = 8    # F[8] gets U[8]

    perm[29] = 20   # D[2] gets F[2]
    perm[32] = 23   # D[5] gets F[5]
    perm[35] = 26   # D[8] gets F[8]

    perm[51] = 29   # B[6] gets D[2]
    perm[48] = 32   # B[3] gets D[5]
    perm[45] = 35   # B[0] gets D[8]

    perm[2] = 51    # U[2] gets B[6]
    perm[5] = 48    # U[5] gets B[3]
    perm[8] = 45    # U[8] gets B[0]

    return _apply_permutation(cube, perm)


def apply_R_prime(cube: CubeState) -> CubeState:
    """
    Apply R' (Right face counter-clockwise 90°).

    This is the inverse of apply_R.
    Mathematical property: R · R' = identity
    """
    cube = apply_R(cube)
    cube = apply_R(cube)
    cube = apply_R(cube)
    return cube


def apply_R2(cube: CubeState) -> CubeState:
    """
    Apply R2 (Right face 180°).

    Mathematical property: (R2)^2 = identity
    """
    cube = apply_R(cube)
    cube = apply_R(cube)
    return cube


def apply_F(cube: CubeState) -> CubeState:
    """
    Apply F (Front face clockwise 90°).

    Face rotation: F face rotates clockwise (when viewing from front)
    Adjacent cycles: Bottom row of U, right column of L, top row of D,
                     left column of R cycle

    Cycles:
        F face: 18→20→26→24→18, 19→23→25→21→19
        Adjacent: U[6,7,8] → R[0,3,6] → D[2,1,0] → L[8,5,2] → U[6,7,8]

    Mathematical verification:
        - F^4 = identity
        - F · F' = identity
        - F commutes with B (F·B = B·F)
    """
    perm = _rotate_face_cw(18)  # Rotate F face (offset 18)

    # Cycle adjacent pieces: U bottom → R left → D top → L right → U bottom
    # U bottom row: 6, 7, 8
    # R left column: 9, 12, 15
    # D top row: 27, 28, 29 (reversed to 29, 28, 27)
    # L right column: 44, 41, 38 (reversed)

    perm[9] = 6      # R[0] gets U[6]
    perm[12] = 7     # R[3] gets U[7]
    perm[15] = 8     # R[6] gets U[8]

    perm[29] = 9     # D[2] gets R[0]
    perm[28] = 12    # D[1] gets R[3]
    perm[27] = 15    # D[0] gets R[6]

    perm[38] = 29    # L[2] gets D[2]
    perm[41] = 28    # L[5] gets D[1]
    perm[44] = 27    # L[8] gets D[0]

    perm[6] = 38     # U[6] gets L[2]
    perm[7] = 41     # U[7] gets L[5]
    perm[8] = 44     # U[8] gets L[8]

    return _apply_permutation(cube, perm)


def apply_F_prime(cube: CubeState) -> CubeState:
    """
    Apply F' (Front face counter-clockwise 90°).

    This is the inverse of apply_F.
    Mathematical property: F · F' = identity
    """
    cube = apply_F(cube)
    cube = apply_F(cube)
    cube = apply_F(cube)
    return cube


def apply_F2(cube: CubeState) -> CubeState:
    """
    Apply F2 (Front face 180°).

    Mathematical property: (F2)^2 = identity
    """
    cube = apply_F(cube)
    cube = apply_F(cube)
    return cube


def apply_D(cube: CubeState) -> CubeState:
    """
    Apply D (Down face clockwise 90°).

    Face rotation: D face rotates clockwise (when viewing from bottom)
    Adjacent cycles: Bottom row of F, L, B, R cycle clockwise

    Cycles:
        D face: 27→29→35→33→27, 28→32→34→30→28
        Adjacent: F[6,7,8] → L[6,7,8] → B[6,7,8] → R[6,7,8] → F[6,7,8]

    Mathematical verification:
        - D^4 = identity
        - D · D' = identity
        - D commutes with U (D·U = U·D)
    """
    perm = _rotate_face_cw(27)  # Rotate D face (offset 27)

    # Cycle bottom rows: F → L → B → R → F
    # F bottom row: 24, 25, 26
    # L bottom row: 42, 43, 44
    # B bottom row: 51, 52, 53
    # R bottom row: 15, 16, 17

    for i in range(3):
        perm[42 + i] = 24 + i    # L gets F
        perm[51 + i] = 42 + i    # B gets L
        perm[15 + i] = 51 + i    # R gets B
        perm[24 + i] = 15 + i    # F gets R

    return _apply_permutation(cube, perm)


def apply_D_prime(cube: CubeState) -> CubeState:
    """
    Apply D' (Down face counter-clockwise 90°).

    This is the inverse of apply_D.
    Mathematical property: D · D' = identity
    """
    cube = apply_D(cube)
    cube = apply_D(cube)
    cube = apply_D(cube)
    return cube


def apply_D2(cube: CubeState) -> CubeState:
    """
    Apply D2 (Down face 180°).

    Mathematical property: (D2)^2 = identity
    """
    cube = apply_D(cube)
    cube = apply_D(cube)
    return cube


def apply_L(cube: CubeState) -> CubeState:
    """
    Apply L (Left face clockwise 90°).

    Face rotation: L face rotates clockwise (when viewing from left)
    Adjacent cycles: Left column of U, B, D, F cycle

    Cycles:
        L face: 36→38→44→42→36, 37→41→43→39→37
        Adjacent: U[0,3,6] → B[8,5,2] → D[0,3,6] → F[0,3,6] → U[0,3,6]
                  (Note: B column is reversed due to orientation)

    Mathematical verification:
        - L^4 = identity
        - L · L' = identity
        - L commutes with R (L·R = R·L)
    """
    perm = _rotate_face_cw(36)  # Rotate L face (offset 36)

    # Cycle left columns: U → F → D → B → U
    # U left column: 0, 3, 6
    # F left column: 18, 21, 24
    # D left column: 27, 30, 33
    # B right column (reversed): 53, 50, 47

    perm[18] = 0     # F[0] gets U[0]
    perm[21] = 3     # F[3] gets U[3]
    perm[24] = 6     # F[6] gets U[6]

    perm[27] = 18    # D[0] gets F[0]
    perm[30] = 21    # D[3] gets F[3]
    perm[33] = 24    # D[6] gets F[6]

    perm[53] = 33    # B[8] gets D[6] (reversed)
    perm[50] = 30    # B[5] gets D[3]
    perm[47] = 27    # B[2] gets D[0]

    perm[0] = 53     # U[0] gets B[8]
    perm[3] = 50     # U[3] gets B[5]
    perm[6] = 47     # U[6] gets B[2]

    return _apply_permutation(cube, perm)


def apply_L_prime(cube: CubeState) -> CubeState:
    """
    Apply L' (Left face counter-clockwise 90°).

    This is the inverse of apply_L.
    Mathematical property: L · L' = identity
    """
    cube = apply_L(cube)
    cube = apply_L(cube)
    cube = apply_L(cube)
    return cube


def apply_L2(cube: CubeState) -> CubeState:
    """
    Apply L2 (Left face 180°).

    Mathematical property: (L2)^2 = identity
    """
    cube = apply_L(cube)
    cube = apply_L(cube)
    return cube


def apply_B(cube: CubeState) -> CubeState:
    """
    Apply B (Back face clockwise 90°).

    Face rotation: B face rotates clockwise (when viewing from back)
    Adjacent cycles: Top row of U, left column of R, bottom row of D,
                     right column of L cycle

    Cycles:
        B face: 45→47→53→51→45, 46→50→52→48→46
        Adjacent: U[0,1,2] → L[6,3,0] → D[8,7,6] → R[2,5,8] → U[0,1,2]

    Mathematical verification:
        - B^4 = identity
        - B · B' = identity
        - B commutes with F (B·F = F·B)
    """
    perm = _rotate_face_cw(45)  # Rotate B face (offset 45)

    # Cycle adjacent pieces: U top → L left → D bottom → R right → U top
    # U top row: 0, 1, 2 (reversed)
    # L left column: 36, 39, 42
    # D bottom row: 33, 34, 35 (reversed to 35, 34, 33)
    # R right column: 11, 14, 17

    perm[36] = 2     # L[0] gets U[2]
    perm[39] = 1     # L[3] gets U[1]
    perm[42] = 0     # L[6] gets U[0]

    perm[35] = 42    # D[8] gets L[6]
    perm[34] = 39    # D[7] gets L[3]
    perm[33] = 36    # D[6] gets L[0]

    perm[11] = 33    # R[2] gets D[6]
    perm[14] = 34    # R[5] gets D[7]
    perm[17] = 35    # R[8] gets D[8]

    perm[0] = 17     # U[0] gets R[8]
    perm[1] = 14     # U[1] gets R[5]
    perm[2] = 11     # U[2] gets R[2]

    return _apply_permutation(cube, perm)


def apply_B_prime(cube: CubeState) -> CubeState:
    """
    Apply B' (Back face counter-clockwise 90°).

    This is the inverse of apply_B.
    Mathematical property: B · B' = identity
    """
    cube = apply_B(cube)
    cube = apply_B(cube)
    cube = apply_B(cube)
    return cube


def apply_B2(cube: CubeState) -> CubeState:
    """
    Apply B2 (Back face 180°).

    Mathematical property: (B2)^2 = identity
    """
    cube = apply_B(cube)
    cube = apply_B(cube)
    return cube


# ============================================================================
# Move Dispatch and Utilities
# ============================================================================

# Mapping from move notation to function
MOVE_FUNCTIONS = {
    'U': apply_U,
    "U'": apply_U_prime,
    'U2': apply_U2,
    'R': apply_R,
    "R'": apply_R_prime,
    'R2': apply_R2,
    'F': apply_F,
    "F'": apply_F_prime,
    'F2': apply_F2,
    'D': apply_D,
    "D'": apply_D_prime,
    'D2': apply_D2,
    'L': apply_L,
    "L'": apply_L_prime,
    'L2': apply_L2,
    'B': apply_B,
    "B'": apply_B_prime,
    'B2': apply_B2,
}


def apply_move(cube: CubeState, move: str) -> CubeState:
    """
    Apply a single move to the cube.

    Args:
        cube: Current cube state
        move: Move notation (U, R, F, D, L, B, or with ' or 2)

    Returns:
        New CubeState after applying the move

    Raises:
        ValueError: If move notation is invalid

    Example:
        >>> cube = CubeState.solved()
        >>> cube = apply_move(cube, 'R')
        >>> cube = apply_move(cube, "R'")
        >>> cube.is_solved()
        True

    Time Complexity: O(1) - always processes exactly 54 stickers
    """
    if move not in MOVE_FUNCTIONS:
        valid = ', '.join(sorted(MOVE_FUNCTIONS.keys()))
        raise ValueError(
            f"Invalid move: '{move}'. Valid moves: {valid}"
        )

    return MOVE_FUNCTIONS[move](cube)


def apply_sequence(cube: CubeState, moves: List[str]) -> CubeState:
    """
    Apply a sequence of moves to the cube.

    Args:
        cube: Current cube state
        moves: List of move notations

    Returns:
        New CubeState after applying all moves in order

    Example:
        >>> cube = CubeState.solved()
        >>> cube = apply_sequence(cube, ['R', 'U', "R'", "U'"])
        >>> # Applied "sexy move"

    Time Complexity: O(n) where n is number of moves
    """
    for move in moves:
        cube = apply_move(cube, move)
    return cube


def invert_move(move: str) -> str:
    """
    Get the inverse of a move.

    Args:
        move: Move notation

    Returns:
        Inverse move notation

    Examples:
        >>> invert_move('R')
        "R'"
        >>> invert_move("R'")
        'R'
        >>> invert_move('R2')
        'R2'

    Mathematical property:
        apply_move(cube, move) followed by apply_move(cube, invert_move(move))
        returns cube to original state.
    """
    if move.endswith("'"):
        return move[:-1]  # R' -> R
    elif move.endswith('2'):
        return move  # R2 is self-inverse
    else:
        return move + "'"  # R -> R'


def invert_sequence(moves: List[str]) -> List[str]:
    """
    Get the inverse of a move sequence.

    The inverse is the reversed sequence with each move inverted.

    Args:
        moves: List of move notations

    Returns:
        Inverse sequence

    Example:
        >>> invert_sequence(['R', 'U', 'R2', "F'"])
        ['F', 'R2', "U'", "R'"]

    Mathematical property:
        apply_sequence(cube, moves) followed by
        apply_sequence(cube, invert_sequence(moves))
        returns cube to original state.
    """
    return [invert_move(m) for m in reversed(moves)]
