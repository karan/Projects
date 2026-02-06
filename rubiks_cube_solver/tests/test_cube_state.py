"""
Tests for CubeState class.
"""

import unittest
from src.cube_state import CubeState


class TestCubeState(unittest.TestCase):
    """Test cases for CubeState."""

    def test_solved_cube_creation(self):
        """Test that a new cube is created in solved state."""
        cube = CubeState()

        # Check each face is uniform
        self.assertEqual(cube.get_face('U'), ['W'] * 9)
        self.assertEqual(cube.get_face('R'), ['R'] * 9)
        self.assertEqual(cube.get_face('F'), ['B'] * 9)
        self.assertEqual(cube.get_face('D'), ['Y'] * 9)
        self.assertEqual(cube.get_face('L'), ['O'] * 9)
        self.assertEqual(cube.get_face('B'), ['G'] * 9)

    def test_is_solved(self):
        """Test is_solved method."""
        cube = CubeState()
        self.assertTrue(cube.is_solved())

        # Modify one sticker
        cube.set_sticker('U', 0, 'R')
        self.assertFalse(cube.is_solved())

    def test_get_set_sticker(self):
        """Test getting and setting individual stickers."""
        cube = CubeState()

        # Get initial value
        self.assertEqual(cube.get_sticker('U', 4), 'W')

        # Set new value
        cube.set_sticker('U', 4, 'R')
        self.assertEqual(cube.get_sticker('U', 4), 'R')

    def test_copy(self):
        """Test that copy creates independent cube."""
        cube1 = CubeState()
        cube2 = cube1.copy()

        # Modify cube2
        cube2.set_sticker('U', 0, 'R')

        # cube1 should be unchanged
        self.assertEqual(cube1.get_sticker('U', 0), 'W')
        self.assertEqual(cube2.get_sticker('U', 0), 'R')

    def test_equality(self):
        """Test cube equality comparison."""
        cube1 = CubeState()
        cube2 = CubeState()
        cube3 = CubeState()
        cube3.set_sticker('U', 0, 'R')

        self.assertEqual(cube1, cube2)
        self.assertNotEqual(cube1, cube3)

    def test_str_representation(self):
        """Test string representation doesn't crash."""
        cube = CubeState()
        str_repr = str(cube)
        self.assertIsInstance(str_repr, str)
        self.assertIn('W', str_repr)  # Should contain white stickers


if __name__ == '__main__':
    unittest.main()
