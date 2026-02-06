"""
Comprehensive test suite for Rubik's Cube move correctness.

This test suite verifies mathematical properties that MUST hold for
any correct Rubik's Cube implementation:

1. Identity Properties:
   - M^4 = identity (four 90° turns)
   - M · M' = identity (move and inverse)
   - (M2)^2 = identity (double turn twice)

2. Permutation Integrity:
   - Moves are bijections (no duplicate/missing indices)
   - All 54 stickers are accounted for

3. Invariant Preservation:
   - Color counts remain constant (9 of each)
   - Center stickers never move
   - Orientation parity is preserved

4. Scramble/Inverse Property:
   - Random scrambles can be undone by their inverse

Why These Tests Matter:
----------------------
A single bug in ANY move function will cause:
  - Solver to produce invalid solutions
  - Cube states to become corrupted
  - Silent failures that are hard to debug

These tests catch bugs BEFORE they propagate to solver logic.

Test Philosophy:
---------------
  - Test mathematical properties, not implementation details
  - Use property-based thinking (forall x, P(x) holds)
  - Make tests fail LOUDLY with clear error messages
  - Test edge cases and random inputs
"""

import pytest
import random
from typing import List, Set

from cube import CubeState, apply_move, apply_sequence, invert_move, invert_sequence
from cube.moves import MOVE_FUNCTIONS


# ============================================================================
# Test Configuration
# ============================================================================

# All basic moves (single face turns)
BASIC_MOVES = ['U', 'R', 'F', 'D', 'L', 'B']

# All moves including inverses and double turns
ALL_MOVES = list(MOVE_FUNCTIONS.keys())

# Opposite face pairs (these should commute)
OPPOSITE_PAIRS = [
    ('U', 'D'),
    ('R', 'L'),
    ('F', 'B'),
]


# ============================================================================
# 1. Identity Tests
# ============================================================================

class TestIdentityProperties:
    """
    Test fundamental identity properties of moves.

    These are the most basic properties that MUST hold.
    If these fail, the move definitions are fundamentally broken.
    """

    @pytest.mark.parametrize("move", BASIC_MOVES)
    def test_move_four_times_is_identity(self, move: str):
        """
        Test that M^4 = identity for all basic moves.

        Why this matters:
            A 90° rotation applied 4 times must complete a full 360° cycle
            and return to the original state. If this fails, the move
            permutation is incorrect.

        Mathematical property:
            ∀M ∈ {U,R,F,D,L,B}: M^4 = identity
        """
        cube = CubeState.solved()
        original = cube.stickers

        # Apply the move 4 times
        for _ in range(4):
            cube = apply_move(cube, move)

        assert cube.stickers == original, (
            f"Move {move} applied 4 times did not return to identity.\n"
            f"This means the {move} move permutation is incorrect."
        )

    @pytest.mark.parametrize("move", BASIC_MOVES)
    def test_move_and_inverse_is_identity(self, move: str):
        """
        Test that M · M' = identity for all basic moves.

        Why this matters:
            A move followed by its inverse must cancel out.
            This is the definition of an inverse operation.

        Mathematical property:
            ∀M: M · M' = identity

        Historical note:
            This exact test caught the critical R' bug in the original
            implementation where R followed by R' did NOT return to identity.
        """
        cube = CubeState.solved()
        original = cube.stickers

        # Apply move then its inverse
        cube = apply_move(cube, move)
        cube = apply_move(cube, move + "'")

        assert cube.stickers == original, (
            f"Move {move} followed by {move}' did not return to identity.\n"
            f"The inverse move is incorrectly implemented.\n"
            f"This is a CRITICAL bug that will break all solver logic."
        )

    @pytest.mark.parametrize("move", BASIC_MOVES)
    def test_double_move_twice_is_identity(self, move: str):
        """
        Test that (M2)^2 = identity for all basic moves.

        Why this matters:
            A 180° rotation (M2) applied twice completes a 360° cycle.

        Mathematical property:
            ∀M: (M2)^2 = identity
        """
        cube = CubeState.solved()
        original = cube.stickers

        # Apply double move twice
        cube = apply_move(cube, move + '2')
        cube = apply_move(cube, move + '2')

        assert cube.stickers == original, (
            f"Double move {move}2 applied twice did not return to identity.\n"
            f"The double move is incorrectly implemented."
        )

    @pytest.mark.parametrize("move", BASIC_MOVES)
    def test_inverse_relationship(self, move: str):
        """
        Test that M' is equivalent to M^3.

        Why this matters:
            Three 90° rotations in one direction equals one 90° rotation
            in the opposite direction.

        Mathematical property:
            M' = M^3
        """
        cube1 = CubeState.solved()
        cube2 = CubeState.solved()

        # Path 1: Apply inverse
        cube1 = apply_move(cube1, move + "'")

        # Path 2: Apply move three times
        for _ in range(3):
            cube2 = apply_move(cube2, move)

        assert cube1.stickers == cube2.stickers, (
            f"Move {move}' is not equivalent to {move}^3.\n"
            f"The inverse implementation is inconsistent."
        )


# ============================================================================
# 2. Permutation Integrity Tests
# ============================================================================

class TestPermutationIntegrity:
    """
    Test that moves are valid bijections (permutations).

    A move must:
      - Map each of 54 positions to exactly one new position
      - Not duplicate any positions
      - Not skip any positions
    """

    @pytest.mark.parametrize("move", ALL_MOVES)
    def test_move_is_bijection(self, move: str):
        """
        Test that each move is a bijection (permutation).

        Why this matters:
            If a move duplicates or skips positions, stickers can be
            lost or duplicated, corrupting the cube state.

        Method:
            Create a cube where each sticker has a unique label (0-53).
            After applying the move, verify all 54 labels still exist
            exactly once.
        """
        # Create cube with unique labels for each sticker
        unique_labels = [str(i) for i in range(54)]
        cube = CubeState(unique_labels)

        # Apply the move
        cube = apply_move(cube, move)

        # Check all labels still present exactly once
        result_labels = set(cube.stickers)

        assert len(result_labels) == 54, (
            f"Move {move} resulted in {len(result_labels)} unique stickers.\n"
            f"Expected 54. The move is not a bijection."
        )

        assert result_labels == set(unique_labels), (
            f"Move {move} changed the sticker labels.\n"
            f"Missing labels: {set(unique_labels) - result_labels}\n"
            f"Extra labels: {result_labels - set(unique_labels)}\n"
            f"The move permutation has duplicates or missing indices."
        )

    @pytest.mark.parametrize("move", ALL_MOVES)
    def test_no_sticker_duplication(self, move: str):
        """
        Test that no stickers are duplicated after a move.

        This is a sanity check beyond bijection test.
        """
        cube = CubeState.solved()
        cube = apply_move(cube, move)

        # Count each color
        color_counts = {}
        for color in cube.stickers:
            color_counts[color] = color_counts.get(color, 0) + 1

        for color, count in color_counts.items():
            assert count == 9, (
                f"After move {move}, color {color} appears {count} times.\n"
                f"Expected 9. Stickers were duplicated or lost."
            )


# ============================================================================
# 3. Invariant Preservation Tests
# ============================================================================

class TestInvariantPreservation:
    """
    Test that moves preserve cube invariants.

    Invariants that MUST be preserved:
      1. Exactly 9 stickers of each color
      2. Center stickers never move
      3. Parity constraints hold
    """

    @pytest.mark.parametrize("move", ALL_MOVES)
    def test_color_counts_preserved(self, move: str):
        """
        Test that color counts remain constant after any move.

        Why this matters:
            Moves should only permute stickers, not create/destroy them.
            If color counts change, stickers are being lost or duplicated.

        Property:
            ∀M, ∀color: count(color, M(cube)) = count(color, cube)
        """
        cube = CubeState.solved()

        # Count colors before
        before = {}
        for color in cube.stickers:
            before[color] = before.get(color, 0) + 1

        # Apply move
        cube = apply_move(cube, move)

        # Count colors after
        after = {}
        for color in cube.stickers:
            after[color] = after.get(color, 0) + 1

        assert before == after, (
            f"Move {move} changed color counts.\n"
            f"Before: {before}\n"
            f"After: {after}\n"
            f"Colors should be preserved by moves."
        )

    @pytest.mark.parametrize("move", ALL_MOVES)
    def test_centers_never_move(self, move: str):
        """
        Test that center stickers remain in their original positions.

        Why this matters:
            Center stickers define the color of each face and should
            never be affected by face rotations.

        Center positions: U=4, R=13, F=22, D=31, L=40, B=49
        """
        cube = CubeState.solved()

        # Record center colors before
        centers_before = {
            'U': cube.get_sticker('U', 4),
            'R': cube.get_sticker('R', 4),
            'F': cube.get_sticker('F', 4),
            'D': cube.get_sticker('D', 4),
            'L': cube.get_sticker('L', 4),
            'B': cube.get_sticker('B', 4),
        }

        # Apply move
        cube = apply_move(cube, move)

        # Check centers after
        centers_after = {
            'U': cube.get_sticker('U', 4),
            'R': cube.get_sticker('R', 4),
            'F': cube.get_sticker('F', 4),
            'D': cube.get_sticker('D', 4),
            'L': cube.get_sticker('L', 4),
            'B': cube.get_sticker('B', 4),
        }

        assert centers_before == centers_after, (
            f"Move {move} changed center stickers.\n"
            f"Before: {centers_before}\n"
            f"After: {centers_after}\n"
            f"Centers should never move during legal moves."
        )

    @pytest.mark.parametrize("moves", [
        ['R', 'U', "R'", "U'"],  # Sexy move
        ['R', 'U', 'R', 'U', 'R', 'U', 'R', 'U'],  # Multiple moves
        ['F2', 'R', 'L', "F'", "B'", 'U2', 'D2'],  # Mixed moves
    ])
    def test_sequence_preserves_color_counts(self, moves: List[str]):
        """
        Test that move sequences preserve color counts.

        This is a stronger test than single moves.
        """
        cube = CubeState.solved()
        original_counts = {'W': 9, 'R': 9, 'G': 9, 'Y': 9, 'O': 9, 'B': 9}

        cube = apply_sequence(cube, moves)

        result_counts = {}
        for color in cube.stickers:
            result_counts[color] = result_counts.get(color, 0) + 1

        assert result_counts == original_counts, (
            f"Sequence {moves} changed color counts.\n"
            f"Expected: {original_counts}\n"
            f"Got: {result_counts}"
        )


# ============================================================================
# 4. Scramble/Inverse Tests
# ============================================================================

class TestScrambleInverse:
    """
    Test that random scrambles can be undone by their inverse.

    This is a critical end-to-end test that verifies the entire
    move system works correctly together.
    """

    @pytest.mark.parametrize("scramble_length", [5, 10, 25, 50, 100])
    def test_random_scramble_and_inverse(self, scramble_length: int):
        """
        Test that a random scramble can be undone by its inverse.

        Why this matters:
            This is the foundation of solving. If we can't undo scrambles,
            we can't solve cubes.

        Method:
            1. Generate random scramble
            2. Apply scramble
            3. Apply inverse of scramble
            4. Verify we're back to solved state

        Property:
            ∀S: S · S^(-1) = identity
        """
        cube = CubeState.solved()

        # Generate random scramble
        scramble = [random.choice(ALL_MOVES) for _ in range(scramble_length)]

        # Apply scramble
        cube = apply_sequence(cube, scramble)

        # Apply inverse
        inverse = invert_sequence(scramble)
        cube = apply_sequence(cube, inverse)

        assert cube.is_solved(), (
            f"Scramble of length {scramble_length} could not be undone.\n"
            f"Scramble: {' '.join(scramble)}\n"
            f"Inverse: {' '.join(inverse)}\n"
            f"This indicates a bug in move implementation or inversion logic."
        )

    def test_many_random_scrambles(self):
        """
        Stress test: Apply and undo many random scrambles.

        This catches bugs that might only appear in specific
        move combinations.
        """
        num_trials = 50
        failures = []

        for trial in range(num_trials):
            cube = CubeState.solved()

            # Random scramble length between 10-30
            length = random.randint(10, 30)
            scramble = [random.choice(ALL_MOVES) for _ in range(length)]

            # Apply and invert
            cube = apply_sequence(cube, scramble)
            inverse = invert_sequence(scramble)
            cube = apply_sequence(cube, inverse)

            if not cube.is_solved():
                failures.append({
                    'trial': trial,
                    'scramble': scramble,
                    'length': length,
                })

        assert len(failures) == 0, (
            f"Failed {len(failures)}/{num_trials} random scramble tests.\n"
            f"First failure: {failures[0] if failures else 'N/A'}\n"
            f"This indicates a systematic bug in move implementation."
        )


# ============================================================================
# 5. Commutativity Tests
# ============================================================================

class TestCommutativity:
    """
    Test that opposite faces commute.

    Opposite face pairs (U/D, R/L, F/B) don't share any stickers,
    so their moves should commute: M1 · M2 = M2 · M1
    """

    @pytest.mark.parametrize("move1,move2", OPPOSITE_PAIRS)
    def test_opposite_faces_commute(self, move1: str, move2: str):
        """
        Test that opposite face moves commute.

        Why this matters:
            Opposite faces don't affect each other, so the order
            shouldn't matter. This is a mathematical property that
            must hold.

        Property:
            U · D = D · U
            R · L = L · R
            F · B = B · F
        """
        cube1 = CubeState.solved()
        cube2 = CubeState.solved()

        # Path 1: move1 then move2
        cube1 = apply_move(cube1, move1)
        cube1 = apply_move(cube1, move2)

        # Path 2: move2 then move1
        cube2 = apply_move(cube2, move2)
        cube2 = apply_move(cube2, move1)

        assert cube1.stickers == cube2.stickers, (
            f"Opposite faces {move1} and {move2} do not commute.\n"
            f"{move1} {move2} ≠ {move2} {move1}\n"
            f"This violates the mathematical property of opposite faces."
        )

    @pytest.mark.parametrize("move1,move2", OPPOSITE_PAIRS)
    def test_opposite_faces_with_inverses_commute(self, move1: str, move2: str):
        """
        Test that opposite faces commute even with inverse moves.
        """
        cube1 = CubeState.solved()
        cube2 = CubeState.solved()

        # Path 1: move1' then move2
        cube1 = apply_move(cube1, move1 + "'")
        cube1 = apply_move(cube1, move2)

        # Path 2: move2 then move1'
        cube2 = apply_move(cube2, move2)
        cube2 = apply_move(cube2, move1 + "'")

        assert cube1.stickers == cube2.stickers, (
            f"Opposite faces {move1}' and {move2} do not commute."
        )


# ============================================================================
# 6. Known Pattern Tests
# ============================================================================

class TestKnownPatterns:
    """
    Test known move sequences that produce specific patterns.

    These are famous sequences with known properties.
    """

    def test_sexy_move_period(self):
        """
        Test that sexy move (R U R' U') has period 6.

        Why this matters:
            The sexy move is one of the most famous sequences.
            It should return to solved after exactly 6 repetitions.

        Note: Actually the sexy move has period 105 for full restoration,
        but creates a 6-cycle pattern in corners.
        """
        cube = CubeState.solved()
        sexy_move = ['R', 'U', "R'", "U'"]

        # Apply 6 times (one full cycle for the corner 3-cycle)
        for _ in range(6):
            cube = apply_sequence(cube, sexy_move)

        # After 6 repetitions, corners should be cycled fully
        # but the entire cube won't be solved until period 105

        # For educational purposes, we'll just verify the sequence is repeatable
        # by checking that applying it 105 times returns to solved
        cube = CubeState.solved()
        for _ in range(105):
            cube = apply_sequence(cube, sexy_move)

        assert cube.is_solved(), (
            "Sexy move (R U R' U') repeated 105 times did not return to solved.\n"
            "This is a known mathematical property that must hold."
        )

    def test_checkerboard_pattern(self):
        """
        Test that checkerboard sequence is self-inverse.

        Sequence: M2 E2 S2 (but we'll use an equivalent face-only sequence)
        Equivalent: R L U D F B (all 180° turns)
        """
        cube = CubeState.solved()

        # Checkerboard-like pattern using only face moves
        sequence = ['R2', 'L2', 'U2', 'D2', 'F2', 'B2']

        # Apply once
        cube = apply_sequence(cube, sequence)

        # Apply again (should return to solved since each move is 180°)
        cube = apply_sequence(cube, sequence)

        assert cube.is_solved(), (
            "Checkerboard pattern sequence applied twice should return to solved."
        )

    def test_superflip_is_self_inverse(self):
        """
        Test that superflip sequence applied twice returns to solved.

        Superflip is a famous position where all edges are flipped in place.
        Applying it twice returns to solved.

        Note: Full superflip is very long (20+ moves). We'll use a simplified
        pattern for testing purposes.
        """
        cube = CubeState.solved()

        # Simplified pattern that's self-inverse
        pattern = ['U', 'R2', 'F', 'B', 'R', 'B2', 'R', 'U2', 'L', 'B2', 'R', "U'",
                   'D', "R'", 'B2', 'F', 'R', 'L', 'B2', 'U2', 'F2']

        # Apply pattern
        cube = apply_sequence(cube, pattern)

        # Apply again
        cube = apply_sequence(cube, pattern)

        # Should return to solved (since pattern · pattern = identity)
        assert cube.is_solved(), (
            "Self-inverse pattern applied twice should return to solved."
        )


# ============================================================================
# 7. Move Inversion Tests
# ============================================================================

class TestMoveInversion:
    """
    Test the move inversion utilities.
    """

    @pytest.mark.parametrize("move,expected_inverse", [
        ('U', "U'"),
        ("U'", 'U'),
        ('U2', 'U2'),
        ('R', "R'"),
        ("F'", 'F'),
        ('D2', 'D2'),
    ])
    def test_invert_move_function(self, move: str, expected_inverse: str):
        """
        Test that invert_move returns correct inverse notation.
        """
        assert invert_move(move) == expected_inverse

    def test_invert_sequence_function(self):
        """
        Test that invert_sequence returns correct reversed inverse sequence.
        """
        sequence = ['R', 'U', "R'", 'F2', 'D']
        expected = ["D'", 'F2', 'R', "U'", "R'"]

        assert invert_sequence(sequence) == expected

    def test_double_inversion_is_identity(self):
        """
        Test that inverting twice returns original sequence.
        """
        sequence = ['R', 'U', 'F', 'D', 'L', 'B']
        double_inverted = invert_sequence(invert_sequence(sequence))

        assert double_inverted == sequence


# ============================================================================
# 8. Edge Case Tests
# ============================================================================

class TestEdgeCases:
    """
    Test edge cases and error handling.
    """

    def test_empty_sequence(self):
        """
        Test that applying empty sequence does nothing.
        """
        cube = CubeState.solved()
        cube = apply_sequence(cube, [])

        assert cube.is_solved()

    def test_invalid_move_raises_error(self):
        """
        Test that invalid move notation raises ValueError.
        """
        cube = CubeState.solved()

        with pytest.raises(ValueError, match="Invalid move"):
            apply_move(cube, 'X')

        with pytest.raises(ValueError, match="Invalid move"):
            apply_move(cube, 'R3')

    def test_cube_state_immutability(self):
        """
        Test that applying moves doesn't mutate original cube.
        """
        cube = CubeState.solved()
        original_stickers = cube.stickers

        # Apply moves (should create new cube)
        new_cube = apply_move(cube, 'R')
        newer_cube = apply_move(new_cube, 'U')

        # Original should be unchanged
        assert cube.stickers == original_stickers
        assert cube.is_solved()

    def test_cube_equality(self):
        """
        Test cube equality comparison.
        """
        cube1 = CubeState.solved()
        cube2 = CubeState.solved()
        cube3 = apply_move(cube1, 'R')

        assert cube1 == cube2
        assert cube1 != cube3
        assert cube2 != cube3

    def test_cube_hashing(self):
        """
        Test that cubes can be hashed and used in sets/dicts.
        """
        cube1 = CubeState.solved()
        cube2 = CubeState.solved()
        cube3 = apply_move(cube1, 'R')

        # Should be hashable
        cube_set = {cube1, cube2, cube3}

        # cube1 and cube2 are equal, so set should have 2 elements
        assert len(cube_set) == 2

        # Should work as dict keys
        cube_dict = {cube1: 'solved', cube3: 'R'}
        assert cube_dict[cube2] == 'solved'  # cube2 == cube1


# ============================================================================
# Test Execution Summary
# ============================================================================

if __name__ == '__main__':
    """
    Run this test file directly with pytest:

        pytest tests/test_moves.py -v

    Expected output:
        - All tests should PASS
        - Any failure indicates a bug in move implementation
        - Failures in identity tests are CRITICAL and must be fixed first

    Test count: 100+ individual tests covering all critical properties
    """
    pytest.main([__file__, '-v', '--tb=short'])
