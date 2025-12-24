"""
BeginnerSolver: A layer-by-layer Rubik's Cube solver.

This solver uses the beginner's method to solve the cube:
1. White cross (4 edges)
2. White corners (4 corners)
3. Middle layer edges (4 edges)
4. Yellow cross
5. Position yellow corners
6. Orient yellow corners

The focus is on clarity and educational value, not optimal move count.
"""

from typing import List
from src.cube_state import CubeState
from src.moves import apply_move, apply_algorithm
from src.utils import (
    find_edge, find_corner,
    is_white_cross_solved, is_white_face_solved, is_middle_layer_solved
)


class BeginnerSolver:
    """
    A beginner-friendly Rubik's Cube solver using layer-by-layer method.

    This solver prioritizes:
    - Clarity: Each step is clearly documented
    - Correctness: Always produces a valid solution
    - Determinism: Same scramble always produces same solution
    - Teachability: Code structure mirrors how humans learn to solve
    """

    def __init__(self):
        """Initialize the solver."""
        self.solution = []  # List of moves in the solution

    def solve(self, cube: CubeState) -> List[str]:
        """
        Solve a Rubik's Cube and return the solution.

        Args:
            cube: Scrambled cube state

        Returns:
            List of moves that solve the cube
        """
        self.solution = []
        current_cube = cube.copy()

        # Step 1: Solve white cross
        current_cube = self._solve_white_cross(current_cube)

        # Step 2: Solve white corners
        current_cube = self._solve_white_corners(current_cube)

        # Step 3: Solve middle layer
        current_cube = self._solve_middle_layer(current_cube)

        # Step 4: Solve yellow cross
        current_cube = self._solve_yellow_cross(current_cube)

        # Step 5: Position yellow edges
        current_cube = self._position_yellow_edges(current_cube)

        # Step 6: Position yellow corners
        current_cube = self._position_yellow_corners(current_cube)

        # Step 7: Orient yellow corners
        current_cube = self._orient_yellow_corners(current_cube)

        return self.solution

    def _add_moves(self, cube: CubeState, moves: str) -> CubeState:
        """
        Add moves to solution and apply to cube.

        Args:
            cube: Current cube state
            moves: Space-separated move sequence

        Returns:
            New cube state after moves
        """
        move_list = moves.split()
        for move in move_list:
            if move:
                self.solution.append(move)
                cube = apply_move(cube, move)
        return cube

    def _solve_white_cross(self, cube: CubeState) -> CubeState:
        """
        Solve the white cross on the top face.

        Strategy:
        1. Find each white edge piece
        2. Move it to the top layer
        3. Align it with the correct center color
        4. Position it correctly

        Args:
            cube: Current cube state

        Returns:
            Cube with white cross solved
        """
        # Solve each white edge in order: F, R, B, L
        target_edges = [
            ('W', 'B'),  # White-Blue edge (front)
            ('W', 'R'),  # White-Red edge (right)
            ('W', 'G'),  # White-Green edge (back)
            ('W', 'O'),  # White-Orange edge (left)
        ]

        for white_color, side_color in target_edges:
            cube = self._solve_white_edge(cube, white_color, side_color)

        return cube

    def _solve_white_edge(self, cube: CubeState, white: str, side: str) -> CubeState:
        """
        Solve a single white edge piece.

        Args:
            cube: Current cube state
            white: White color ('W')
            side: Side color ('B', 'R', 'G', or 'O')

        Returns:
            Cube with this edge in correct position
        """
        # Determine target face based on side color
        target_face = {'B': 'F', 'R': 'R', 'G': 'B', 'O': 'L'}[side]

        # Find the edge
        edge = find_edge(cube, white, side)
        if edge is None:
            return cube

        face, pos, adj_face, adj_pos = edge

        # If edge is already correctly placed, skip
        if face == 'U' and adj_face == target_face and \
           cube.get_sticker('U', pos) == 'W' and cube.get_sticker(adj_face, adj_pos) == side:
            return cube

        # Move edge to D layer if it's in U layer (but not correctly placed)
        if face == 'U':
            # Rotate U to align with a side face, then move down
            while cube.get_sticker('U', 7) == 'W' or cube.get_sticker('F', 1) == 'W':
                cube = self._add_moves(cube, 'U')
                edge = find_edge(cube, white, side)
                if edge is None:
                    return cube
                face, pos, adj_face, adj_pos = edge

            cube = self._add_moves(cube, 'F F')
            edge = find_edge(cube, white, side)
            if edge is None:
                return cube
            face, pos, adj_face, adj_pos = edge

        # Now edge is in middle or bottom layer
        # Move to D layer if in middle layer
        if face in ['F', 'R', 'B', 'L'] and pos in [3, 5]:
            # Edge is in middle layer
            if pos == 3:  # Left side
                cube = self._add_moves(cube, f'{face} D')
            else:  # Right side (pos == 5)
                cube = self._add_moves(cube, f"{face}' D")
            edge = find_edge(cube, white, side)
            if edge is None:
                return cube
            face, pos, adj_face, adj_pos = edge

        # Edge should now be in D layer
        # Rotate D to align side color with target center
        for _ in range(4):
            edge = find_edge(cube, white, side)
            if edge is None:
                return cube
            face, pos, adj_face, adj_pos = edge

            # Check if white is on D face or on side face
            if face == 'D':
                # White is on bottom, side color is on side face
                if adj_face == target_face:
                    break
            else:
                # White is on side face, side color is on D face
                if face == target_face:
                    break
            cube = self._add_moves(cube, 'D')

        # Now edge is aligned, move it up
        edge = find_edge(cube, white, side)
        if edge is None:
            return cube
        face, pos, adj_face, adj_pos = edge

        if face == 'D':
            # White is on D face, do F2
            cube = self._add_moves(cube, f'{adj_face} {adj_face}')
        else:
            # White is on side face, do F
            # But first rotate D to align
            for _ in range(4):
                edge = find_edge(cube, white, side)
                if edge is None:
                    return cube
                face, pos, adj_face, adj_pos = edge
                if face == target_face and adj_face == 'D':
                    break
                cube = self._add_moves(cube, 'D')

            edge = find_edge(cube, white, side)
            if edge is None:
                return cube
            face, pos, adj_face, adj_pos = edge

            # Apply: D' F' (to flip edge up)
            cube = self._add_moves(cube, f"D' {face} {face}")

        return cube

    def _solve_white_corners(self, cube: CubeState) -> CubeState:
        """
        Solve the white corners to complete the white face.

        Strategy:
        1. Find each white corner
        2. Move to D layer if needed
        3. Position below target slot
        4. Use R' D' R D algorithm to insert

        Args:
            cube: Current cube state (with white cross solved)

        Returns:
            Cube with white face solved
        """
        # Solve corners in order: URF, UFL, ULB, UBR
        corners = [
            ('W', 'B', 'R'),  # White-Blue-Red (URF)
            ('W', 'O', 'B'),  # White-Orange-Blue (UFL)
            ('W', 'G', 'O'),  # White-Green-Orange (ULB)
            ('W', 'R', 'G'),  # White-Red-Green (UBR)
        ]

        for corner_colors in corners:
            cube = self._solve_white_corner(cube, *corner_colors)

        return cube

    def _solve_white_corner(self, cube: CubeState, c1: str, c2: str, c3: str) -> CubeState:
        """
        Solve a single white corner.

        Args:
            cube: Current cube state
            c1, c2, c3: Corner colors

        Returns:
            Cube with this corner solved
        """
        # Determine target position based on the two non-white colors
        colors = {c1, c2, c3}
        white_removed = colors.copy()
        white_removed.remove('W')
        side_colors = list(white_removed)

        # Determine which corner slot this belongs in
        if set(side_colors) == {'B', 'R'}:
            target_u_pos = 8
            right_face = 'R'
        elif set(side_colors) == {'B', 'O'}:
            target_u_pos = 6
            right_face = 'F'
        elif set(side_colors) == {'G', 'O'}:
            target_u_pos = 0
            right_face = 'L'
        elif set(side_colors) == {'G', 'R'}:
            target_u_pos = 2
            right_face = 'B'
        else:
            return cube

        # Check if already solved
        corner = find_corner(cube, c1, c2, c3)
        if corner is None:
            return cube

        face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner
        if face == 'U' and pos == target_u_pos and cube.get_sticker('U', target_u_pos) == 'W':
            return cube

        # If corner is in U layer but wrong, move to D layer
        if face == 'U':
            # First, rotate U to position corner at URF
            for _ in range(4):
                corner = find_corner(cube, c1, c2, c3)
                if corner is None:
                    break
                face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner
                if cube.get_sticker('U', 8) in colors or \
                   cube.get_sticker('R', 0) in colors or \
                   cube.get_sticker('F', 2) in colors:
                    break
                cube = self._add_moves(cube, 'U')

            cube = self._add_moves(cube, "R' D' R D")
            corner = find_corner(cube, c1, c2, c3)
            if corner is None:
                return cube
            face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner

        # Corner is now in D layer
        # Rotate D to position under target slot
        for _ in range(4):
            corner = find_corner(cube, c1, c2, c3)
            if corner is None:
                return cube
            face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner

            # Check if positioned correctly
            # The corner should be in D layer directly below target
            if face == 'D':
                # White on D face
                if target_u_pos == 8 and pos == 6:  # DRF position for URF
                    break
                elif target_u_pos == 6 and pos == 0:  # DFL position for UFL
                    break
                elif target_u_pos == 0 and pos == 2:  # DLB position for ULB
                    break
                elif target_u_pos == 2 and pos == 8:  # DBR position for UBR
                    break
            else:
                # White on side face
                if target_u_pos == 8 and face == 'R' and pos == 8:
                    break
                elif target_u_pos == 8 and face == 'F' and pos == 8:
                    break
                elif target_u_pos == 6 and face == 'F' and pos == 6:
                    break
                elif target_u_pos == 6 and face == 'L' and pos == 8:
                    break
                elif target_u_pos == 0 and face == 'L' and pos == 6:
                    break
                elif target_u_pos == 0 and face == 'B' and pos == 8:
                    break
                elif target_u_pos == 2 and face == 'B' and pos == 6:
                    break
                elif target_u_pos == 2 and face == 'R' and pos == 6:
                    break

            cube = self._add_moves(cube, 'D')

        # Now insert the corner using the standard algorithm
        # We need to determine the correct algorithm based on white orientation
        corner = find_corner(cube, c1, c2, c3)
        if corner is None:
            return cube
        face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner

        # Use the right_face we already determined above (lines 261-273)

        # Apply algorithm until corner is solved
        for _ in range(5):  # Maximum 5 iterations needed
            corner = find_corner(cube, c1, c2, c3)
            if corner is None:
                return cube
            face, pos, adj_face1, adj_pos1, adj_face2, adj_pos2 = corner

            # Check if solved
            if face == 'U' and cube.get_sticker('U', target_u_pos) == 'W':
                break

            # Apply: R' D' R D
            cube = self._add_moves(cube, f"{right_face}' D' {right_face} D")

        return cube

    def _solve_middle_layer(self, cube: CubeState) -> CubeState:
        """
        Solve the middle layer edges (second layer).

        Strategy:
        1. Find edges that don't have yellow
        2. Position on D layer
        3. Use algorithm to insert left or right

        Args:
            cube: Current cube state (with white face solved)

        Returns:
            Cube with first two layers solved
        """
        # Solve 4 middle layer edges
        for _ in range(8):  # Iterate multiple times to handle all cases
            if is_middle_layer_solved(cube):
                break

            # Find an edge in D layer that belongs in middle layer
            # (i.e., doesn't have yellow)
            edge_to_solve = None

            # Check D layer edges
            d_edges = [
                ('F', 7, 'D', 1),
                ('R', 7, 'D', 7),
                ('B', 7, 'D', 5),
                ('L', 7, 'D', 3),
            ]

            for edge in d_edges:
                face, pos, adj_face, adj_pos = edge
                c1 = cube.get_sticker(face, pos)
                c2 = cube.get_sticker(adj_face, adj_pos)

                if c1 != 'Y' and c2 != 'Y':
                    edge_to_solve = (c1, c2, face)
                    break

            # If no edge in D layer, extract one from middle layer
            if edge_to_solve is None:
                # Extract an incorrectly placed middle edge
                cube = self._add_moves(cube, "F D F' D' F' D' F D")
                continue

            c1, c2, current_face = edge_to_solve

            # Rotate D to align edge with its center color
            for _ in range(4):
                if cube.get_sticker('F', 7) == 'B' or cube.get_sticker('D', 1) == 'B':
                    if cube.get_sticker('F', 7) == 'B':
                        target_face = 'F'
                        break
                if cube.get_sticker('R', 7) == 'R' or cube.get_sticker('D', 7) == 'R':
                    if cube.get_sticker('R', 7) == 'R':
                        target_face = 'R'
                        break
                if cube.get_sticker('B', 7) == 'G' or cube.get_sticker('D', 5) == 'G':
                    if cube.get_sticker('B', 7) == 'G':
                        target_face = 'B'
                        break
                if cube.get_sticker('L', 7) == 'O' or cube.get_sticker('D', 3) == 'O':
                    if cube.get_sticker('L', 7) == 'O':
                        target_face = 'L'
                        break
                cube = self._add_moves(cube, 'D')

            # Determine direction (left or right)
            # Get the center color of the edge's second color
            target_face = None
            for face in ['F', 'R', 'B', 'L']:
                if cube.get_sticker(face, 7) == cube.get_sticker(face, 4):
                    target_face = face
                    break

            if target_face is None:
                continue

            # Determine which way to insert
            other_color = None
            if cube.get_sticker(target_face, 7) == cube.get_sticker(target_face, 4):
                other_color = cube.get_sticker('D', [1, 7, 5, 3][['F', 'R', 'B', 'L'].index(target_face)])

            # Determine left or right based on color mapping
            face_order = ['F', 'R', 'B', 'L']
            current_idx = face_order.index(target_face)

            # Check which adjacent face the other color belongs to
            if other_color == 'R' and target_face == 'F':
                direction = 'right'
            elif other_color == 'O' and target_face == 'F':
                direction = 'left'
            elif other_color == 'B' and target_face == 'R':
                direction = 'right'
            elif other_color == 'G' and target_face == 'R':
                direction = 'left'
            elif other_color == 'O' and target_face == 'B':
                direction = 'right'
            elif other_color == 'R' and target_face == 'B':
                direction = 'left'
            elif other_color == 'G' and target_face == 'L':
                direction = 'right'
            elif other_color == 'B' and target_face == 'L':
                direction = 'left'
            else:
                cube = self._add_moves(cube, 'D')
                continue

            # Apply algorithm
            if direction == 'right':
                # U R U' R' U' F' U F
                # Translated: D L D' L' D' F' D F (using target face)
                right_face = face_order[(current_idx + 1) % 4]
                cube = self._add_moves(cube, f"D {right_face} D' {right_face}' D' {target_face}' D {target_face}")
            else:
                # U' L' U L U F U' F'
                left_face = face_order[(current_idx - 1) % 4]
                cube = self._add_moves(cube, f"D' {left_face}' D {left_face} D {target_face} D' {target_face}'")

        return cube

    def _solve_yellow_cross(self, cube: CubeState) -> CubeState:
        """
        Create a yellow cross on the D (bottom) face.

        Uses the algorithm: F R U R' U' F'

        Args:
            cube: Current cube state

        Returns:
            Cube with yellow cross on bottom
        """
        # Check yellow cross state and apply algorithm
        for _ in range(3):  # Maximum 3 iterations
            # Count yellow edges on D face
            yellow_edges = sum([
                cube.get_sticker('D', 1) == 'Y',
                cube.get_sticker('D', 3) == 'Y',
                cube.get_sticker('D', 5) == 'Y',
                cube.get_sticker('D', 7) == 'Y',
            ])

            if yellow_edges == 4:
                break

            # Apply algorithm
            cube = self._add_moves(cube, "F R U R' U' F'")

            # Rotate D to try different orientations
            cube = self._add_moves(cube, 'D')

        return cube

    def _position_yellow_edges(self, cube: CubeState) -> CubeState:
        """
        Position yellow edges correctly (swap if needed).

        Args:
            cube: Current cube state

        Returns:
            Cube with yellow edges positioned correctly
        """
        # Simple approach: check and swap edges if needed
        for _ in range(4):
            # Check if edges are positioned correctly
            edges_correct = (
                cube.get_sticker('F', 7) == 'B' and
                cube.get_sticker('R', 7) == 'R' and
                cube.get_sticker('B', 7) == 'G' and
                cube.get_sticker('L', 7) == 'O'
            )

            if edges_correct:
                break

            # Rotate D to check different alignments
            cube = self._add_moves(cube, 'D')

        # If not aligned after rotation, swap edges
        for _ in range(4):
            edges_correct = (
                cube.get_sticker('F', 7) == 'B' and
                cube.get_sticker('R', 7) == 'R' and
                cube.get_sticker('B', 7) == 'G' and
                cube.get_sticker('L', 7) == 'O'
            )

            if edges_correct:
                break

            # Apply edge swap algorithm
            cube = self._add_moves(cube, "R U R' U R U U R' U")
            cube = self._add_moves(cube, 'D')

        return cube

    def _position_yellow_corners(self, cube: CubeState) -> CubeState:
        """
        Position yellow corners in correct locations (not necessarily oriented).

        Args:
            cube: Current cube state

        Returns:
            Cube with yellow corners positioned correctly
        """
        # Use corner swap algorithm
        for _ in range(5):
            # Check if corners are positioned correctly
            # (they have the right colors, even if not oriented)
            corners_correct = True

            # Check each corner position has the right color combination
            # URF corner
            urf_colors = {cube.get_sticker('U', 8), cube.get_sticker('R', 0), cube.get_sticker('F', 2)}
            if urf_colors != {'W', 'B', 'R'}:
                corners_correct = False

            if corners_correct:
                break

            # Apply corner positioning algorithm: U R U' L' U R' U' L
            cube = self._add_moves(cube, "U R U' L' U R' U' L")

        return cube

    def _orient_yellow_corners(self, cube: CubeState) -> CubeState:
        """
        Orient the yellow corners to solve the cube.

        Args:
            cube: Current cube state

        Returns:
            Solved cube
        """
        # Orient each corner using R' D' R D algorithm
        for _ in range(4):
            # Orient the DRF corner
            for _ in range(3):
                if cube.get_sticker('D', 6) == 'Y':
                    break
                cube = self._add_moves(cube, "R' D' R D")

            # Move to next corner
            cube = self._add_moves(cube, 'D')

        # Final adjustments to align layers
        for _ in range(4):
            if cube.is_solved():
                break
            cube = self._add_moves(cube, 'D')

        return cube
