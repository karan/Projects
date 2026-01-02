#!/usr/bin/env python3
"""
Demo: Rubik's Cube Solver CLI

This demo shows how to use the beginner solver:
1. Create a solved cube
2. Scramble it with random moves
3. Solve it using the BeginnerSolver
4. Display the solution moves

Usage:
    python demo.py
    python demo.py --scramble "R U R' U'"
"""

import argparse
import random
from src.cube_state import CubeState
from src.moves import apply_algorithm, apply_move_sequence
from src.solver import BeginnerSolver
from src.simple_solver import SimpleSolver


def generate_scramble(length: int = 20) -> str:
    """
    Generate a random scramble sequence.

    Args:
        length: Number of moves in scramble

    Returns:
        Space-separated move sequence
    """
    moves = ['U', 'R', 'F', 'D', 'L', 'B']
    modifiers = ['', "'", '2']

    scramble = []
    last_move = None

    for _ in range(length):
        # Avoid consecutive moves on same face
        available_moves = [m for m in moves if m != last_move]
        move = random.choice(available_moves)
        modifier = random.choice(modifiers)
        scramble.append(move + modifier)
        last_move = move

    return ' '.join(scramble)


def format_solution(moves: list, moves_per_line: int = 10) -> str:
    """
    Format solution moves for display.

    Args:
        moves: List of move strings
        moves_per_line: Number of moves per line

    Returns:
        Formatted string with moves
    """
    lines = []
    for i in range(0, len(moves), moves_per_line):
        line = ' '.join(moves[i:i + moves_per_line])
        lines.append(line)
    return '\n'.join(lines)


def main():
    """Run the demo."""
    parser = argparse.ArgumentParser(description='Rubik\'s Cube Solver Demo')
    parser.add_argument(
        '--scramble',
        type=str,
        help='Custom scramble sequence (space-separated moves)'
    )
    parser.add_argument(
        '--length',
        type=int,
        default=5,
        help='Scramble length for random scramble (default: 5)'
    )
    parser.add_argument(
        '--solver',
        type=str,
        choices=['simple', 'beginner'],
        default='simple',
        help='Solver to use: simple (BFS, works for short scrambles) or beginner (layer-by-layer, experimental)'
    )
    parser.add_argument(
        '--max-depth',
        type=int,
        default=10,
        help='Maximum search depth for simple solver (default: 10)'
    )
    parser.add_argument(
        '--no-display',
        action='store_true',
        help='Don\'t display cube states (only show moves)'
    )

    args = parser.parse_args()

    print("=" * 60)
    print("RUBIK'S CUBE SOLVER - BEGINNER'S METHOD")
    print("=" * 60)
    print()

    # Create a solved cube
    cube = CubeState()

    if not args.no_display:
        print("SOLVED CUBE:")
        print(cube)
        print()

    # Generate or use provided scramble
    if args.scramble:
        scramble = args.scramble
        print(f"CUSTOM SCRAMBLE: {scramble}")
    else:
        scramble = generate_scramble(args.length)
        print(f"RANDOM SCRAMBLE ({args.length} moves):")
        print(scramble)

    print()

    # Apply scramble
    scrambled_cube = apply_algorithm(cube, scramble)

    if not args.no_display:
        print("SCRAMBLED CUBE:")
        print(scrambled_cube)
        print()

    # Solve the cube
    print(f"SOLVING (using {args.solver} solver)...")
    print()

    if args.solver == 'simple':
        solver = SimpleSolver(max_depth=args.max_depth)
        solution = solver.solve(scrambled_cube)
        if not solution and not scrambled_cube.is_solved():
            print(f"No solution found within {args.max_depth} moves.")
            print("Try increasing --max-depth or using a shorter scramble.")
            print()
            return
    else:  # beginner
        solver = BeginnerSolver()
        solution = solver.solve(scrambled_cube)

    # Apply solution to verify
    solved_cube = apply_move_sequence(scrambled_cube, solution)

    # Display results
    print("=" * 60)
    print("SOLUTION")
    print("=" * 60)
    print()
    print(f"Number of moves: {len(solution)}")
    print()
    print("Moves:")
    print(format_solution(solution))
    print()

    if not args.no_display:
        print("SOLVED CUBE:")
        print(solved_cube)
        print()

    # Verify solution
    if solved_cube.is_solved():
        print("✓ VERIFICATION: Cube is solved!")
    else:
        print("✗ VERIFICATION FAILED: Cube is not solved")
        print("This is a bug - please report it!")

    print()
    print("=" * 60)
    print()

    # Educational notes
    print("EDUCATIONAL NOTES:")
    print()
    if args.solver == 'simple':
        print("The SimpleSolver uses breadth-first search (BFS):")
        print("  - Tries all possible move combinations systematically")
        print("  - Finds the SHORTEST solution (optimal)")
        print("  - Only practical for short scrambles (~7 moves)")
        print("  - Great for understanding search algorithms!")
        print()
        print("This solver demonstrates:")
        print("  - How to explore a problem space systematically")
        print("  - The importance of pruning redundant paths")
        print("  - Trade-offs between optimality and scalability")
    else:
        print("The BeginnerSolver uses a layer-by-layer approach:")
        print("  1. White cross (4 edges)")
        print("  2. White corners (complete first layer)")
        print("  3. Middle layer edges (complete second layer)")
        print("  4. Yellow cross")
        print("  5. Position yellow edges")
        print("  6. Position yellow corners")
        print("  7. Orient yellow corners (solve!)")
        print()
        print("Note: This solver is experimental and may not always work.")
        print("It demonstrates the concepts but needs further development.")
    print()


if __name__ == '__main__':
    main()
