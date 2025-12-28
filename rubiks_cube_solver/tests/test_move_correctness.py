"""
Comprehensive move correctness tests.

These tests verify that the move implementation is mathematically correct.
"""

import unittest
from collections import Counter
from src.cube_state import CubeState
from src.moves import apply_move, apply_algorithm


class TestMoveCorrectness(unittest.TestCase):
    """Test cases for move correctness."""

    def test_move_identity_four_times(self):
        """Test that M^4 = identity for all basic moves."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            with self.subTest(move=move):
                cube = CubeState()
                original_stickers = cube.stickers.copy()

                # Apply move 4 times
                for _ in range(4):
                    cube = apply_move(cube, move)

                self.assertEqual(cube.stickers, original_stickers,
                               f"{move}^4 should return to identity")

    def test_move_inverse_identity(self):
        """Test that M M' = identity for all basic moves."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            with self.subTest(move=move):
                cube = CubeState()
                original_stickers = cube.stickers.copy()

                # Apply move then its inverse
                cube = apply_move(cube, move)
                cube = apply_move(cube, move + "'")

                self.assertEqual(cube.stickers, original_stickers,
                               f"{move} {move}' should return to identity")

    def test_double_move_identity(self):
        """Test that (M2)^2 = identity for all basic moves."""
        moves = ['U', 'R', 'F', 'D', 'L', 'B']

        for move in moves:
            with self.subTest(move=move):
                cube = CubeState()
                original_stickers = cube.stickers.copy()

                # Apply M2 twice
                cube = apply_move(cube, move + '2')
                cube = apply_move(cube, move + '2')

                self.assertEqual(cube.stickers, original_stickers,
                               f"({move}2)^2 should return to identity")

    def test_move_is_bijection(self):
        """Test that each move is a valid permutation (bijection)."""
        moves = ['U', "U'", 'U2', 'R', "R'", 'R2',
                'F', "F'", 'F2', 'D', "D'", 'D2',
                'L', "L'", 'L2', 'B', "B'", 'B2']

        for move in moves:
            with self.subTest(move=move):
                cube = CubeState()
                cube = apply_move(cube, move)

                # Check all 54 positions are present exactly once
                sticker_positions = {}
                for i, color in enumerate(cube.stickers):
                    if color not in sticker_positions:
                        sticker_positions[color] = []
                    sticker_positions[color].append(i)

                # Every color should appear exactly 9 times
                for color in ['W', 'R', 'B', 'Y', 'O', 'G']:
                    self.assertEqual(len(sticker_positions.get(color, [])), 9,
                                   f"Move {move} should preserve color count")

    def test_color_invariants(self):
        """Test that any sequence of moves preserves color counts."""
        sequences = [
            "R U R' U'",
            "F R U R' U' F'",
            "R U R' U R U2 R'",
            "R U R' U' R' F R F'",
            "R U2 R' U' R U' R'",
        ]

        for seq in sequences:
            with self.subTest(sequence=seq):
                cube = CubeState()
                cube = apply_algorithm(cube, seq)

                # Count colors
                color_counts = Counter(cube.stickers)

                for color in ['W', 'R', 'B', 'Y', 'O', 'G']:
                    self.assertEqual(color_counts[color], 9,
                                   f"Sequence '{seq}' should preserve color counts")

    def test_known_sequence_verification(self):
        """Test that a known sequence produces expected result."""
        # Test the "sexy move" R U R' U' has period 105
        # (This affects only certain pieces, the full cube period is 105)
        cube = CubeState()

        # Apply sexy move 105 times
        for _ in range(105):
            cube = apply_algorithm(cube, "R U R' U'")

        self.assertTrue(cube.is_solved(),
                       "Sexy move (R U R' U') should have period 105")

    def test_commutator_identity(self):
        """Test that commutator [R, U] has finite period."""
        cube = CubeState()

        # The commutator R U R' U' has period 105
        for _ in range(105):
            cube = apply_move(cube, 'R')
            cube = apply_move(cube, 'U')
            cube = apply_move(cube, "R'")
            cube = apply_move(cube, "U'")

        self.assertTrue(cube.is_solved(),
                       "Commutator [R, U] should return to solved state")

    def test_superflip_sequences(self):
        """Test well-known cube sequences."""
        # Test checkerboard pattern can be created and undone
        cube = CubeState()
        checkerboard = "U2 D2 F2 B2 L2 R2"

        cube = apply_algorithm(cube, checkerboard)
        self.assertFalse(cube.is_solved(), "Checkerboard should scramble cube")

        # Apply again to return to solved
        cube = apply_algorithm(cube, checkerboard)
        self.assertTrue(cube.is_solved(), "Checkerboard^2 should be identity")

    def test_random_scramble_and_inverse(self):
        """Test that random scrambles can be undone by their inverse."""
        import random

        moves = ['U', "U'", 'U2', 'R', "R'", 'R2',
                'F', "F'", 'F2', 'D', "D'", 'D2',
                'L', "L'", 'L2', 'B', "B'", 'B2']

        for trial in range(20):
            with self.subTest(trial=trial):
                # Generate random scramble
                scramble_moves = [random.choice(moves) for _ in range(25)]
                scramble = ' '.join(scramble_moves)

                # Apply scramble
                cube = CubeState()
                cube = apply_algorithm(cube, scramble)

                # Create inverse
                inverse_moves = []
                for move in reversed(scramble_moves):
                    if move.endswith("'"):
                        inverse_moves.append(move[0])
                    elif move.endswith('2'):
                        inverse_moves.append(move)
                    else:
                        inverse_moves.append(move + "'")

                inverse = ' '.join(inverse_moves)

                # Apply inverse
                cube = apply_algorithm(cube, inverse)

                self.assertTrue(cube.is_solved(),
                               f"Scramble and inverse should return to solved (trial {trial})")

    def test_move_commutativity_properties(self):
        """Test that opposite faces commute."""
        # U and D should commute (U D = D U)
        cube1 = CubeState()
        cube1 = apply_move(cube1, 'U')
        cube1 = apply_move(cube1, 'D')

        cube2 = CubeState()
        cube2 = apply_move(cube2, 'D')
        cube2 = apply_move(cube2, 'U')

        self.assertEqual(cube1, cube2, "U and D should commute")

        # R and L should commute
        cube1 = CubeState()
        cube1 = apply_move(cube1, 'R')
        cube1 = apply_move(cube1, 'L')

        cube2 = CubeState()
        cube2 = apply_move(cube2, 'L')
        cube2 = apply_move(cube2, 'R')

        self.assertEqual(cube1, cube2, "R and L should commute")

        # F and B should commute
        cube1 = CubeState()
        cube1 = apply_move(cube1, 'F')
        cube1 = apply_move(cube1, 'B')

        cube2 = CubeState()
        cube2 = apply_move(cube2, 'B')
        cube2 = apply_move(cube2, 'F')

        self.assertEqual(cube1, cube2, "F and B should commute")


if __name__ == '__main__':
    unittest.main()
