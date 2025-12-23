"""
Tests for moves module.

These tests verify that:
1. Moves execute without errors
2. Inverse moves undo the original move
3. Applying a move 4 times returns to original state
4. Move sequences work correctly
"""

import unittest
from src.cube_state import CubeState
from src.moves import apply_move, apply_algorithm, apply_move_sequence


class TestMoves(unittest.TestCase):
    """Test cases for cube moves."""

    def test_move_and_inverse(self):
        """Test that X followed by X' returns to original state."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            cube = CubeState()
            original = cube.copy()

            # Apply move then inverse
            cube = apply_move(cube, move)
            cube = apply_move(cube, move + "'")

            self.assertEqual(cube, original,
                           f"{move} followed by {move}' should return to original")

    def test_move_four_times(self):
        """Test that applying a move 4 times returns to original state."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            cube = CubeState()
            original = cube.copy()

            # Apply move 4 times
            for _ in range(4):
                cube = apply_move(cube, move)

            self.assertEqual(cube, original,
                           f"{move} applied 4 times should return to original")

    def test_double_move(self):
        """Test that X2 equals X applied twice."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            cube1 = CubeState()
            cube2 = CubeState()

            # Apply X2
            cube1 = apply_move(cube1, move + '2')

            # Apply X twice
            cube2 = apply_move(cube2, move)
            cube2 = apply_move(cube2, move)

            self.assertEqual(cube1, cube2,
                           f"{move}2 should equal {move} applied twice")

    def test_algorithm_parsing(self):
        """Test that algorithms are parsed and applied correctly."""
        cube1 = CubeState()
        cube2 = CubeState()

        # Apply as algorithm string
        cube1 = apply_algorithm(cube1, "R U R' U'")

        # Apply as individual moves
        for move in ['R', 'U', "R'", "U'"]:
            cube2 = apply_move(cube2, move)

        self.assertEqual(cube1, cube2)

    def test_move_sequence(self):
        """Test applying a list of moves."""
        cube1 = CubeState()
        cube2 = CubeState()

        moves = ['R', 'U', "R'", "U'"]

        # Apply as sequence
        cube1 = apply_move_sequence(cube1, moves)

        # Apply individually
        for move in moves:
            cube2 = apply_move(cube2, move)

        self.assertEqual(cube1, cube2)

    def test_moves_change_state(self):
        """Test that moves actually change the cube state."""
        cube = CubeState()
        original = cube.copy()

        # Each move should change the state
        for move in ['U', 'R', 'F', 'D', 'L', 'B']:
            cube_after = apply_move(cube.copy(), move)
            self.assertNotEqual(cube_after, original,
                              f"{move} should change the cube state")

    def test_invalid_move(self):
        """Test that invalid moves raise ValueError."""
        cube = CubeState()

        with self.assertRaises(ValueError):
            apply_move(cube, 'X')

        with self.assertRaises(ValueError):
            apply_move(cube, 'u')  # Lowercase not supported


if __name__ == '__main__':
    unittest.main()
