# Rubik's Cube Solver - Educational Implementation

A beginner-friendly Rubik's Cube solver in Python designed for learning and experimentation.

**Focus**: Clarity, correctness, and educational value over optimal performance.

## Overview

This project implements a Rubik's Cube solver using a 54-sticker representation. It's designed to help beginners understand:

- How to model a Rubik's Cube in code
- How basic cube moves work
- Different solving strategies (BFS vs. layer-by-layer)
- Algorithmic problem-solving

## Features

- ✅ Clean 54-sticker cube representation
- ✅ All basic moves (U, R, F, D, L, B) with inverses and double turns
- ✅ Two solving approaches:
  - **SimpleSolver**: Breadth-first search (optimal for short scrambles)
  - **BeginnerSolver**: Layer-by-layer method (experimental)
- ✅ Comprehensive unit tests
- ✅ CLI demo with scramble and solve
- ✅ Clear, readable, modular code

## Installation

```bash
# Clone the repository
cd rubiks_cube_solver

# No external dependencies required - uses Python standard library only!
```

## Quick Start

```bash
# Solve a simple scramble
python demo.py --scramble "R U"

# Generate a random 5-move scramble and solve
python demo.py --length 5

# Use the experimental layer-by-layer solver
python demo.py --scramble "R U" --solver beginner
```

## How It Works

### Cube Representation

The cube uses a **54-sticker model** where each of the 6 faces has 9 stickers:

```
Face Order: U R F D L B
(Up, Right, Front, Down, Left, Back)

Each face layout:
0 1 2
3 4 5
6 7 8
```

**Standard color scheme:**
- **U (Up)**: White (W)
- **R (Right)**: Red (R)
- **F (Front)**: Blue (B)
- **D (Down)**: Yellow (Y)
- **L (Left)**: Orange (O)
- **B (Back)**: Green (G)

### Move Notation

Standard Rubik's Cube notation:

- `U` - Turn Up face clockwise 90°
- `U'` - Turn Up face counter-clockwise 90°
- `U2` - Turn Up face 180°
- Same for R, F, D, L, B

### Solving Strategies

#### SimpleSolver (Recommended for Learning)

Uses **breadth-first search** to find the shortest solution:

```python
from src.cube_state import CubeState
from src.moves import apply_algorithm
from src.simple_solver import SimpleSolver

# Create and scramble a cube
cube = CubeState()
cube = apply_algorithm(cube, "R U R' U'")

# Solve it
solver = SimpleSolver(max_depth=10)
solution = solver.solve(cube)
print("Solution:", ' '.join(solution))
```

**Pros:**
- Finds optimal (shortest) solution
- Easy to understand algorithm
- Great for learning search techniques

**Cons:**
- Only practical for ~7 move scrambles
- Memory/time grows exponentially

#### BeginnerSolver (Experimental)

Attempts a layer-by-layer solve:

```python
from src.solver import BeginnerSolver

solver = BeginnerSolver()
solution = solver.solve(cube)
```

**Note:** This solver is experimental and may not always produce correct solutions. It's included to demonstrate the layer-by-layer approach conceptually.

## Project Structure

```
rubiks_cube_solver/
├── README.md               # This file
├── demo.py                # CLI demonstration
├── src/
│   ├── __init__.py
│   ├── cube_state.py      # CubeState class (54-sticker model)
│   ├── moves.py           # Move execution (U, R, F, D, L, B, etc.)
│   ├── simple_solver.py   # BFS solver
│   ├── solver.py          # Layer-by-layer solver (experimental)
│   └── utils.py           # Helper functions
└── tests/
    ├── test_cube_state.py # CubeState tests
    └── test_moves.py      # Move tests
```

## Running Tests

```bash
# Run all tests
python -m unittest discover -s tests -v

# Run specific test file
python -m unittest tests.test_moves -v
```

## Code Examples

### Creating and Manipulating a Cube

```python
from src.cube_state import CubeState
from src.moves import apply_move, apply_algorithm

# Create a solved cube
cube = CubeState()
print(cube.is_solved())  # True

# Apply a single move
cube = apply_move(cube, 'R')
print(cube.is_solved())  # False

# Apply a sequence
cube = apply_algorithm(cube, "R' U R U'")

# Display the cube
print(cube)
```

### Checking Move Properties

```python
from src.cube_state import CubeState
from src.moves import apply_move

cube = CubeState()

# A move applied 4 times returns to original state
for _ in range(4):
    cube = apply_move(cube, 'U')
print(cube.is_solved())  # True

# A move and its inverse cancel out
cube = apply_move(cube, 'R')
cube = apply_move(cube, "R'")
print(cube.is_solved())  # True
```

## CLI Demo Options

```bash
# Basic usage
python demo.py

# Custom scramble
python demo.py --scramble "R U F D L B"

# Random scramble with specific length
python demo.py --length 7

# Choose solver
python demo.py --solver simple    # BFS (default)
python demo.py --solver beginner  # Layer-by-layer

# Adjust search depth
python demo.py --max-depth 12

# Hide cube visualizations
python demo.py --no-display
```

## Educational Focus

This project prioritizes **learning** over **performance**:

### What This Project Teaches

1. **State Representation**
   - How to model a complex 3D object in code
   - Trade-offs between different representations

2. **Move Mechanics**
   - How Rubik's Cube moves work mathematically
   - Implementing rotations and transformations

3. **Search Algorithms**
   - Breadth-first search
   - State space exploration
   - Pruning redundant paths

4. **Algorithm Design**
   - Breaking complex problems into steps
   - Layer-by-layer problem solving

5. **Testing and Verification**
   - Property-based testing (e.g., move × 4 = identity)
   - Invariant checking

### What This Project Does NOT Do

- ❌ Use optimal algorithms (IDA*, Kociemba, etc.)
- ❌ Optimize for speed or move count
- ❌ Use lookup tables or databases
- ❌ Employ advanced group theory

## Extending the Project

Here are some ideas for experimentation:

### Beginner Projects

1. **Add visualization**: Create a graphical display of the cube
2. **Improve move notation**: Support `x`, `y`, `z` rotations
3. **Add scramble validation**: Ensure scrambles are valid cube states
4. **Pattern detection**: Identify common patterns (checkerboard, etc.)

### Intermediate Projects

1. **Fix BeginnerSolver**: Complete the layer-by-layer implementation
2. **Implement IDA***: Add a more efficient search algorithm
3. **Add heuristics**: Estimate distance to solved state
4. **Two-phase solver**: Implement a simplified Kociemba algorithm

### Advanced Projects

1. **Optimal solver**: Implement full Kociemba or IDA* with pattern databases
2. **Machine learning**: Train a neural network to solve cubes
3. **Multiple cube sizes**: Extend to 2×2×2, 4×4×4, etc.
4. **Interactive web app**: Build a web-based cube simulator

## Common Pitfalls

1. **Off-by-one errors**: Sticker indices are 0-based
2. **Face orientation**: Make sure you understand which way each face rotates
3. **Move sequences**: Remember that moves are applied right-to-left in math notation
4. **State copying**: Always use `.copy()` to avoid mutating the original cube

## Performance Notes

### SimpleSolver

| Scramble Length | Typical Time | States Explored |
|----------------|--------------|-----------------|
| 1-2 moves      | < 0.1s       | ~100            |
| 3-4 moves      | < 1s         | ~10,000         |
| 5-6 moves      | < 10s        | ~1,000,000      |
| 7+ moves       | > 60s        | > 10,000,000    |

**Note**: The SimpleSolver is intentionally simple and unoptimized. A production solver would use pruning tables, IDA*, and other optimizations.

## Contributing

This is an educational project! Feel free to:

- Fix bugs in the BeginnerSolver
- Add better documentation
- Create additional test cases
- Implement new solving strategies
- Improve code clarity

**Priority**: Readability > Performance

## License

This project is provided as-is for educational purposes.

## Resources

To learn more about Rubik's Cube algorithms:

- [Speedsolving.com Wiki](https://www.speedsolving.com/wiki/)
- [Ruwix - Beginner's Method](https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/)
- [Cube Explorer](http://kociemba.org/cube.htm) - Optimal solver

## Acknowledgments

Created as an educational resource for learning:
- Python programming
- Algorithm design
- State space search
- Problem decomposition

---

**Remember**: The goal is to learn, not to build the fastest solver!
