"""
SimpleSolver: A simple demonstrational Rubik's Cube solver.

This is a simplified solver that demonstrates the basic concepts without
implementing a full layer-by-layer solution. It's designed to be:
- Easy to understand
- Clear in its logic
- A starting point for experimentation

For educational purposes, this solver uses a brute-force search approach
for small scrambles. This is NOT efficient but is easy to understand.
"""

from typing import List, Optional
from collections import deque
from src.cube_state import CubeState
from src.moves import apply_move


class SimpleSolver:
    """
    A simple breadth-first search solver for demonstration purposes.

    This solver finds the shortest solution for small scrambles (up to ~7 moves).
    For larger scrambles, it will timeout or require too much memory.

    This is intentionally simple to be educational - it shows how you could
    solve the cube by systematically exploring all possible move sequences.
    """

    def __init__(self, max_depth: int = 10):
        """
        Initialize the solver.

        Args:
            max_depth: Maximum search depth (number of moves to try)
        """
        self.max_depth = max_depth
        self.moves = ['U', "U'", 'U2', 'R', "R'", 'R2',
                     'F', "F'", 'F2', 'D', "D'", 'D2',
                     'L', "L'", 'L2', 'B', "B'", 'B2']

    def solve(self, cube: CubeState) -> List[str]:
        """
        Solve a cube using breadth-first search.

        Args:
            cube: Scrambled cube state

        Returns:
            List of moves that solve the cube (may be empty if no solution found)
        """
        if cube.is_solved():
            return []

        # BFS queue: (cube_state, move_sequence)
        queue = deque([(cube, [])])
        visited = {cube}

        while queue:
            current_cube, move_seq = queue.popleft()

            # Don't search beyond max depth
            if len(move_seq) >= self.max_depth:
                continue

            # Try each possible move
            for move in self.moves:
                # Optimization: don't do redundant moves
                # (e.g., don't do U after U')
                if move_seq and self._is_redundant(move_seq[-1], move):
                    continue

                new_cube = apply_move(current_cube, move)

                if new_cube.is_solved():
                    return move_seq + [move]

                if new_cube not in visited:
                    visited.add(new_cube)
                    queue.append((new_cube, move_seq + [move]))

        # No solution found within max_depth
        return []

    def _is_redundant(self, last_move: str, next_move: str) -> bool:
        """
        Check if a move is redundant after the last move.

        Args:
            last_move: The previous move
            next_move: The move to check

        Returns:
            True if the move is redundant
        """
        # Get base face (without modifiers)
        last_face = last_move[0]
        next_face = next_move[0]

        # Don't do the same face twice in a row (they should be combined)
        if last_face == next_face:
            return True

        # Don't do opposite faces in certain orders (to reduce search space)
        # This is an optimization: U D is OK, but D U is redundant with U D
        opposite_pairs = [('U', 'D'), ('R', 'L'), ('F', 'B')]
        for face1, face2 in opposite_pairs:
            if last_face == face2 and next_face == face1:
                return True

        return False
