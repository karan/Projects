"""
BeginnerSolver Demo and Usage Examples.

This file shows how to use the BeginnerSolver once it's implemented.

Run this file to see the solver in action:
    python3 examples/solver_demo.py

Note: Many examples are commented out because the solver is not
yet fully implemented. Uncomment them as you complete each phase.
"""

from cube import CubeState, apply_sequence
from solver import BeginnerSolver


def demo_basic_usage():
    """Basic solver usage example."""
    print("=" * 60)
    print("DEMO: Basic Solver Usage")
    print("=" * 60)

    # Create a solved cube
    cube = CubeState.solved()
    print("Starting with a solved cube:")
    print(cube)
    print()

    # Apply a simple scramble
    scramble = ['R', 'U', 'F', 'D', 'L']
    print(f"Applying scramble: {' '.join(scramble)}")
    cube = apply_sequence(cube, scramble)
    print(cube)
    print()

    # TODO: Uncomment when solver is implemented
    # print("Solving...")
    # solver = BeginnerSolver(debug=True)
    # solution = solver.solve(cube)
    #
    # print(f"\nSolution found! ({len(solution)} moves)")
    # print(f"Moves: {' '.join(solution)}")
    #
    # # Apply solution
    # cube_solved = apply_sequence(cube, solution)
    # print("\nAfter applying solution:")
    # print(cube_solved)
    # print(f"Is solved: {cube_solved.is_solved()}")


def demo_phase_by_phase():
    """Demo solving each phase independently."""
    print("\n" + "=" * 60)
    print("DEMO: Phase-by-Phase Solving")
    print("=" * 60)

    # Start with scrambled cube
    cube = CubeState.solved()
    scramble = ['R', 'U', 'R', 'U', 'R', 'U', "R'", "U'", 'R2']
    cube = apply_sequence(cube, scramble)

    solver = BeginnerSolver(debug=True)

    # TODO: Uncomment as each phase is implemented

    # print("\n--- Phase 1: White Cross ---")
    # cross_moves = solver.solve_white_cross(cube)
    # print(f"Cross moves: {' '.join(cross_moves)}")
    # cube = apply_sequence(cube, cross_moves)
    # print(f"Cross solved: {solver._is_white_cross_solved(cube)}")

    # print("\n--- Phase 2: White Corners ---")
    # corner_moves = solver.solve_white_corners(cube)
    # print(f"Corner moves: {' '.join(corner_moves)}")
    # cube = apply_sequence(cube, corner_moves)
    # print(f"White face solved: {solver._is_white_face_solved(cube)}")

    # print("\n--- Phase 3: Middle Layer ---")
    # middle_moves = solver.solve_middle_layer(cube)
    # print(f"Middle moves: {' '.join(middle_moves)}")
    # cube = apply_sequence(cube, middle_moves)
    # print(f"Middle layer solved: {solver._is_middle_layer_solved(cube)}")

    # print("\n--- Phase 4: Last Layer ---")
    # last_moves = solver.solve_last_layer(cube)
    # print(f"Last layer moves: {' '.join(last_moves)}")
    # cube = apply_sequence(cube, last_moves)
    # print(f"Cube solved: {cube.is_solved()}")


def demo_debug_mode():
    """Demo using debug mode for learning."""
    print("\n" + "=" * 60)
    print("DEMO: Debug Mode")
    print("=" * 60)

    cube = CubeState.solved()
    scramble = ['R', 'U', 'F']
    cube = apply_sequence(cube, scramble)

    # Enable debug mode for detailed output
    solver = BeginnerSolver(debug=True)

    print("Solving with debug output enabled...")
    print("(You'll see each step the solver takes)")
    print()

    # TODO: Uncomment when solver is implemented
    # solution = solver.solve(cube)
    # print(f"\nTotal moves: {len(solution)}")


def demo_custom_settings():
    """Demo creating solver with custom settings."""
    print("\n" + "=" * 60)
    print("DEMO: Custom Solver Settings")
    print("=" * 60)

    # Create solver with custom iteration limit
    solver = BeginnerSolver(max_iterations=500, debug=False)

    print(f"Solver max iterations: {solver.max_iterations}")
    print(f"Debug mode: {solver.debug}")
    print()

    cube = CubeState.solved()
    # TODO: Uncomment when implemented
    # solution = solver.solve(cube)
    # print(f"Solved in {len(solution)} moves")


def demo_multiple_scrambles():
    """Demo solving multiple different scrambles."""
    print("\n" + "=" * 60)
    print("DEMO: Solving Multiple Scrambles")
    print("=" * 60)

    solver = BeginnerSolver(debug=False)

    scrambles = [
        ['R', 'U', 'F'],
        ['R', 'U', 'R', 'U', 'R', 'U'],
        ['R', 'U', "R'", 'U', 'F', 'D2', 'B'],
        ['R2', 'F2', 'U', 'D', 'L', 'R', 'B2'],
    ]

    # TODO: Uncomment when solver is implemented
    # for i, scramble in enumerate(scrambles, 1):
    #     cube = CubeState.solved()
    #     cube = apply_sequence(cube, scramble)
    #
    #     solution = solver.solve(cube)
    #     cube_solved = apply_sequence(cube, solution)
    #
    #     print(f"Scramble {i}: {' '.join(scramble)}")
    #     print(f"  Scramble length: {len(scramble)} moves")
    #     print(f"  Solution length: {len(solution)} moves")
    #     print(f"  Solved: {cube_solved.is_solved()}")
    #     print()


def demo_comparing_solutions():
    """Demo comparing solution efficiency."""
    print("\n" + "=" * 60)
    print("DEMO: Comparing Solution Lengths")
    print("=" * 60)

    solver = BeginnerSolver(debug=False)

    # TODO: Uncomment when solver is implemented
    # # Solve same cube multiple times (should be deterministic)
    # cube = CubeState.solved()
    # scramble = ['R', 'U', 'F', 'D', 'L', 'B']
    # cube = apply_sequence(cube, scramble)
    #
    # solution1 = solver.solve(cube)
    # solution2 = solver.solve(cube)  # Should be identical
    #
    # print(f"Solution 1: {len(solution1)} moves")
    # print(f"Solution 2: {len(solution2)} moves")
    # print(f"Solutions identical: {solution1 == solution2}")
    # print()
    #
    # # Note: Beginner method should be deterministic!
    # if solution1 != solution2:
    #     print("WARNING: Solutions differ! Solver may have randomness.")
    # else:
    #     print("✓ Solver is deterministic (same input = same output)")


def demo_error_handling():
    """Demo how solver handles errors."""
    print("\n" + "=" * 60)
    print("DEMO: Error Handling")
    print("=" * 60)

    # TODO: Uncomment when error handling is implemented

    # # Test iteration limit
    # print("Testing iteration limit...")
    # solver = BeginnerSolver(max_iterations=10, debug=False)
    # cube = CubeState.solved()
    # scramble = ['R', 'U', 'F'] * 20  # Very scrambled
    # cube = apply_sequence(cube, scramble)
    #
    # try:
    #     solution = solver.solve(cube)
    #     print("  Solved successfully!")
    # except RuntimeError as e:
    #     print(f"  Caught error: {e}")
    #     print("  (This is expected with low iteration limit)")


def create_interesting_pattern():
    """Create an interesting cube pattern to solve."""
    print("\n" + "=" * 60)
    print("DEMO: Solving a Pattern")
    print("=" * 60)

    # Checkerboard pattern (solved in two F2 moves)
    cube = CubeState.solved()
    pattern = ['R2', 'L2', 'U2', 'D2', 'F2', 'B2']
    cube = apply_sequence(cube, pattern)

    print("Created checkerboard pattern:")
    print(cube)
    print()

    # TODO: Uncomment when solver is implemented
    # print("Solving checkerboard pattern...")
    # solver = BeginnerSolver(debug=False)
    # solution = solver.solve(cube)
    #
    # print(f"Solution: {len(solution)} moves")
    # print(f"Moves: {' '.join(solution)}")
    # print()
    # print("Note: Optimal solution is just reversing the pattern (6 moves),")
    # print("but beginner method doesn't optimize for patterns.")


def demo_validating_solution():
    """Demo validating that solution actually solves the cube."""
    print("\n" + "=" * 60)
    print("DEMO: Solution Validation")
    print("=" * 60)

    cube = CubeState.solved()
    scramble = ['R', 'U', 'F', 'D']
    cube_scrambled = apply_sequence(cube, scramble)

    print(f"Scramble: {' '.join(scramble)}")
    print(f"Scrambled cube is solved: {cube_scrambled.is_solved()}")
    print()

    # TODO: Uncomment when solver is implemented
    # solver = BeginnerSolver(debug=False)
    # solution = solver.solve(cube_scrambled)
    #
    # print(f"Solution: {' '.join(solution)}")
    # print()
    #
    # # Apply solution
    # cube_final = apply_sequence(cube_scrambled, solution)
    #
    # print("Validation:")
    # print(f"  Final cube is solved: {cube_final.is_solved()}")
    # print(f"  Solution length: {len(solution)} moves")
    # print()
    #
    # # Double-check by comparing to solved state
    # if cube_final == CubeState.solved():
    #     print("✓ Solution verified! Cube matches solved state.")
    # else:
    #     print("✗ Solution failed! Cube does not match solved state.")


# =============================================================================
# Main Demo Runner
# =============================================================================

def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("BEGINNER SOLVER DEMONSTRATIONS")
    print("=" * 60)
    print()
    print("This file demonstrates various uses of the BeginnerSolver.")
    print("Many demos are commented out because the solver is not yet implemented.")
    print()
    print("As you implement the solver, uncomment the demos to see it in action!")
    print()

    # Run basic demo (works even without full implementation)
    demo_basic_usage()

    # Uncomment other demos as you implement the solver
    # demo_phase_by_phase()
    # demo_debug_mode()
    # demo_custom_settings()
    # demo_multiple_scrambles()
    # demo_comparing_solutions()
    # demo_error_handling()
    # create_interesting_pattern()
    # demo_validating_solution()

    print("\n" + "=" * 60)
    print("DEMOS COMPLETE")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Implement the solver methods in solver/beginner.py")
    print("2. Uncomment the demos above to test your implementation")
    print("3. Run: python3 examples/solver_demo.py")
    print()


if __name__ == '__main__':
    main()
