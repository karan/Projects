# Beginner Rubik's Cube Solver - Learning Guide

This guide walks you through implementing a beginner-friendly Rubik's Cube solver from scratch.

## 🎯 Learning Objectives

By completing this implementation, you will learn:

- **Layer-by-layer solving strategy** (how humans solve cubes)
- **Algorithm application** (when and how to apply move sequences)
- **State inspection** (finding and tracking pieces on the cube)
- **Iterative problem solving** (breaking complex problems into steps)
- **Test-driven development** (writing tests as you code)

## 📋 Prerequisites

Before starting, ensure you understand:

1. **The cube foundation** (`cube/state.py` and `cube/moves.py`)
   - How to create and inspect cube states
   - How to apply moves
   - How moves compose into sequences

2. **Basic Rubik's Cube concepts**
   - Faces: U (Up), R (Right), F (Front), D (Down), L (Left), B (Back)
   - Pieces: Centers (fixed), Edges (2 colors), Corners (3 colors)
   - Move notation: R (clockwise), R' (counter-clockwise), R2 (180°)

3. **Python fundamentals**
   - Classes and methods
   - Lists and tuples
   - Type hints
   - Basic control flow

## 🏗️ Project Structure

```
solver/
├── __init__.py           # Package exports
└── beginner.py           # BeginnerSolver class (YOU IMPLEMENT THIS)

tests/
└── test_beginner_solver.py  # Test suite for your solver

README_SOLVER.md          # This file
```

## 🎓 Implementation Roadmap

### Phase 0: Understanding (30 minutes)

**Goal:** Understand the layer-by-layer strategy before coding.

**Tasks:**
1. Read `solver/beginner.py` completely
2. Watch a beginner method tutorial video
3. Try solving a physical or virtual cube manually
4. Understand each phase's goal

**Resources:**
- [J Perm's Beginner Method](https://jperm.net/3x3/moves)
- [Ruwix Beginner Tutorial](https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/)

### Phase 1: White Cross (2-4 hours)

**Goal:** Implement `solve_white_cross()` to solve the bottom white cross.

**What is the white cross?**
```
         W W W        A plus sign (+) of white edges on the
         W W W        bottom face, with each edge matching
         W W W        its adjacent center color.
  O O O  G G G  R R R
  . O .  . G .  . R .
  . . .  . . .  . . .
```

**Implementation Steps:**

1. **Implement `_find_white_edge()`** (30 min)
   ```python
   def _find_white_edge(self, cube: CubeState, target_color: str):
       # Loop through all edge positions
       # Check if edge has white + target_color
       # Return (face, position) if found
   ```

2. **Implement `_is_white_cross_solved()`** (20 min)
   ```python
   def _is_white_cross_solved(self, cube: CubeState):
       # Check D face positions 1, 3, 5, 7 are white
       # Check adjacent colors match F, R, B, L centers
       # Return True/False
   ```

3. **Implement `solve_white_cross()` logic** (2-3 hours)
   ```python
   def solve_white_cross(self, cube: CubeState):
       moves = []
       # For each of 4 edge positions on D face:
       #   1. Find the white edge that belongs there
       #   2. Move it to U face if not there
       #   3. Position above target
       #   4. Insert down with F2 or similar
       #   5. Repeat until edge is correctly placed
       return moves
   ```

**Testing:**
```bash
# Test your implementation
pytest tests/test_beginner_solver.py::TestWhiteCross -v

# Debug with prints
python3 -c "
from cube import CubeState, apply_sequence
from solver import BeginnerSolver

solver = BeginnerSolver(debug=True)
cube = CubeState.solved()
# Apply some moves to scramble cross
cube = apply_sequence(cube, ['R', 'U', 'F'])
moves = solver.solve_white_cross(cube)
print(f'Solution: {moves}')
"
```

**Common Algorithms for White Cross:**
```
Edge on top, insert down:   F2 or R2 or L2 or B2
Edge in middle, move to top: R U or F U or L U or B U
Edge on bottom but wrong:    F2 U F2 (move to top, reposition, insert)
```

**Success Criteria:**
- ✅ Can solve white cross from any scrambled state
- ✅ Cross edges match adjacent center colors
- ✅ Tests pass

---

### Phase 2: White Corners (3-5 hours)

**Goal:** Implement `solve_white_corners()` to complete the white face.

**What are white corners?**
```
         W W W        All 4 corners positioned correctly
         W W W        with white facing down and side
         W W W        colors matching adjacent faces.
  O O O  G G G  R R R
  O O O  G G G  R R R
  . . .  . . .  . . .
```

**Implementation Steps:**

1. **Implement `_find_white_corner()`** (45 min)
   ```python
   def _find_white_corner(self, cube: CubeState, colors: Tuple[str, str]):
       # Loop through all 8 corner positions
       # Check if corner has white + both colors
       # Return (face, position) if found
   ```

2. **Implement `_is_white_face_solved()`** (30 min)
   ```python
   def _is_white_face_solved(self, cube: CubeState):
       # Check all 9 stickers on D face are white
       # Check first layer of adjacent faces matches centers
       # Return True/False
   ```

3. **Implement `solve_white_corners()` logic** (3-4 hours)
   ```python
   def solve_white_corners(self, cube: CubeState):
       moves = []
       # For each of 4 corner positions on D face:
       #   1. Find corner that belongs there
       #   2. Move to U face if on D face
       #   3. Position above target using U moves
       #   4. Apply R U R' U' until correctly oriented
       #   5. Repeat for all corners
       return moves
   ```

**Key Algorithm:**
```
Right Corner Insert: R U R' U'

This algorithm:
- Inserts corner from top-right to bottom-right
- May need 1-5 repetitions to get white facing down
- Does NOT break the white cross (important!)

Example:
- If white faces right: apply once
- If white faces front: apply twice
- If white faces down: apply zero times (done!)
```

**Testing:**
```bash
pytest tests/test_beginner_solver.py::TestWhiteCorners -v
```

**Success Criteria:**
- ✅ Can solve white corners with cross already solved
- ✅ White face is complete (all 9 stickers white)
- ✅ First layer matches on all sides

---

### Phase 3: Middle Layer (4-6 hours)

**Goal:** Implement `solve_middle_layer()` to complete the second layer.

**What is the middle layer?**
```
  . . .  . . .        The 4 edges in the middle that have
  O O O  G G G        no white or yellow. Each edge must
  O O O  G G G        match both adjacent center colors.
```

**Implementation Steps:**

1. **Implement `_find_middle_edge()`** (1 hour)
   ```python
   def _find_middle_edge(self, cube: CubeState):
       # Look for edges on U face without yellow
       # Or edges in middle layer that are wrong
       # Return edge location
   ```

2. **Implement `_is_middle_layer_solved()`** (30 min)
   ```python
   def _is_middle_layer_solved(self, cube: CubeState):
       # Check all 4 middle edges are correct
       # First two layers completely solved
       # Return True/False
   ```

3. **Implement `solve_middle_layer()` logic** (3-4 hours)
   ```python
   def solve_middle_layer(self, cube: CubeState):
       moves = []
       # For each of 4 middle edges:
       #   1. Find an unsolved edge (no yellow)
       #   2. If in middle but wrong, extract to U
       #   3. Position above target
       #   4. Determine left or right insertion
       #   5. Apply appropriate algorithm
       return moves
   ```

**Key Algorithms:**

```
Right Edge Insert:
U R U' R' U' F' U F
(Brings edge from U face into right slot of middle layer)

Left Edge Insert:
U' L' U L U F U' F'
(Brings edge from U face into left slot of middle layer)
```

**Which algorithm to use?**
- Look at the edge on top (U face)
- See which color faces up and which faces front
- If target slot is to the RIGHT of front center: use right algorithm
- If target slot is to the LEFT of front center: use left algorithm

**Edge Case:** If edge is in middle layer but wrong/flipped:
```
# Extract it to top first
Apply right or left algorithm to move it to U face
Then reinsert correctly
```

**Testing:**
```bash
pytest tests/test_beginner_solver.py::TestMiddleLayer -v
```

**Success Criteria:**
- ✅ Can solve middle layer with bottom layer solved
- ✅ All 4 edges correctly positioned
- ✅ First two layers complete

---

### Phase 4: Last Layer (6-10 hours)

**Goal:** Implement `solve_last_layer()` to complete the cube.

This is the most complex phase. Break it into 4 sub-steps.

#### Sub-step 4A: Yellow Cross (2 hours)

**Goal:** Get yellow edges oriented (yellow facing up on U face).

**Implement `_solve_yellow_cross()`:**
```python
def _solve_yellow_cross(self, cube: CubeState):
    # Detect pattern: dot, L, line, or cross
    # Apply F R U R' U' F' as needed
    # Dot: apply 3 times
    # L shape: position and apply once
    # Line: position and apply once
    # Cross: done!
```

**Algorithm:**
```
Yellow Cross Algorithm: F R U R' U' F'
```

#### Sub-step 4B: Yellow Corners Orientation (2-3 hours)

**Goal:** Orient all corners so yellow faces up (not necessarily positioned).

**Implement `_solve_yellow_corners_orientation()`:**
```python
def _solve_yellow_corners_orientation(self, cube: CubeState):
    # Count corners with yellow on top
    # If not all oriented:
    #   Hold with one correct corner at specific position
    #   Apply R U R' U R U2 R'
    #   Rotate cube and repeat
```

**Algorithm:**
```
Sune Algorithm: R U R' U R U2 R'
(Orients 3 corners while keeping 1 fixed)
```

#### Sub-step 4C: Yellow Corners Position (2-3 hours)

**Goal:** Move corners to correct positions (even if rotated).

**Implement `_solve_yellow_corners_position()`:**
```python
def _solve_yellow_corners_position(self, cube: CubeState):
    # Find a corner already in correct position
    # If none, apply algorithm once to create one
    # Hold correct corner at reference position
    # Apply U R U' L' U R' U' L to cycle others
```

**Algorithm:**
```
Corner Swap: U R U' L' U R' U' L
(Cycles 3 corners clockwise)
```

#### Sub-step 4D: Yellow Edges Position (2-3 hours)

**Goal:** Position final edges to complete the cube.

**Implement `_solve_yellow_edges_position()`:**
```python
def _solve_yellow_edges_position(self, cube: CubeState):
    # Check which edges are incorrectly positioned
    # Apply edge cycling algorithm
    # Repeat until all correct
```

**Algorithm:**
```
Edge Cycle: F2 U L R' F2 L' R U F2
(Cycles 3 edges)
```

**Testing Each Sub-step:**
```bash
# Test yellow cross
pytest tests/test_beginner_solver.py::TestLastLayer::test_yellow_cross_subphase -v

# Test full last layer
pytest tests/test_beginner_solver.py::TestLastLayer -v
```

**Success Criteria:**
- ✅ Yellow cross forms correctly
- ✅ All corners oriented with yellow up
- ✅ All corners in correct positions
- ✅ All edges in correct positions
- ✅ **CUBE IS SOLVED!** 🎉

---

### Phase 5: Integration & Testing (2-3 hours)

**Goal:** Ensure all phases work together and handle edge cases.

**Tasks:**

1. **Test full solver** (1 hour)
   ```bash
   # Run all tests
   pytest tests/test_beginner_solver.py -v

   # Test with scrambles
   pytest tests/test_beginner_solver.py::TestFullSolver -v
   ```

2. **Add error handling** (1 hour)
   - Iteration limits in each phase
   - Validation between phases
   - Descriptive error messages

3. **Add debugging support** (30 min)
   - Logging which piece is being worked on
   - Printing intermediate states
   - Move count tracking

4. **Performance testing** (30 min)
   ```python
   # Test with 10 random scrambles
   for i in range(10):
       cube = create_random_scramble()
       solution = solver.solve(cube)
       print(f"Scramble {i}: {len(solution)} moves")
   ```

---

## 🔍 Debugging Tips

### Problem: Solver gets stuck in infinite loop

**Solution:**
```python
# Add iteration counter to each phase
iterations = 0
max_iterations = self.max_iterations

while not phase_complete:
    # ... solving logic ...
    iterations += 1
    if iterations > max_iterations:
        raise RuntimeError(
            f"Phase exceeded {max_iterations} iterations. "
            f"Current state: {cube}"
        )
```

### Problem: Pieces end up in wrong positions

**Solution:**
- Add validation after each piece is placed
- Print cube state before and after algorithm
- Verify algorithm is correctly defined
- Check if you're breaking previously solved pieces

### Problem: Don't know which algorithm to use

**Solution:**
```python
# Add detailed logging
if self.debug:
    print(f"Working on piece at {position}")
    print(f"Current colors: {colors}")
    print(f"Target position: {target}")
    print(f"Applying algorithm: {algorithm}")
```

### Problem: Tests fail with "Cube not solved"

**Solution:**
- Test each phase independently first
- Create test cubes with only later phases scrambled
- Verify preconditions are met
- Check postconditions after each phase

---

## 📚 Learning Resources

### Beginner Method Tutorials
- [J Perm - Beginner Method](https://jperm.net/3x3/moves)
- [CubeSkills - Beginner Solution](https://www.cubeskills.com/tutorials/beginner-solution)
- [Ruwix - How to Solve](https://ruwix.com/the-rubiks-cube/how-to-solve-the-rubiks-cube-beginners-method/)

### Algorithm References
- [Speedsolving Wiki](https://www.speedsolving.com/wiki/index.php/3x3x3_speedsolving_methods)
- [Algorithm Database](https://www.speedsolving.com/wiki/index.php/List_of_Algorithms)

### Understanding Cube Theory
- [Group Theory and Rubik's Cube](https://web.mit.edu/sp.268/www/rubik.pdf)
- [Rubik's Cube Permutations](https://www.math.rwth-aachen.de/~Martin.Schoenert/Cube-Lovers/)

---

## ✅ Success Checklist

Mark these off as you complete each milestone:

### Phase 1: White Cross
- [ ] Implemented `_find_white_edge()`
- [ ] Implemented `_is_white_cross_solved()`
- [ ] Implemented `solve_white_cross()`
- [ ] All white cross tests pass
- [ ] Can solve cross from any scramble

### Phase 2: White Corners
- [ ] Implemented `_find_white_corner()`
- [ ] Implemented `_is_white_face_solved()`
- [ ] Implemented `solve_white_corners()`
- [ ] All white corner tests pass
- [ ] Can complete white face

### Phase 3: Middle Layer
- [ ] Implemented `_find_middle_edge()`
- [ ] Implemented `_is_middle_layer_solved()`
- [ ] Implemented `solve_middle_layer()`
- [ ] All middle layer tests pass
- [ ] First two layers solve correctly

### Phase 4: Last Layer
- [ ] Implemented `_solve_yellow_cross()`
- [ ] Implemented `_solve_yellow_corners_orientation()`
- [ ] Implemented `_solve_yellow_corners_position()`
- [ ] Implemented `_solve_yellow_edges_position()`
- [ ] Implemented `solve_last_layer()`
- [ ] All last layer tests pass

### Phase 5: Integration
- [ ] All tests pass
- [ ] Error handling works
- [ ] Can solve fully scrambled cubes
- [ ] Average solution < 200 moves
- [ ] Code is clean and commented

---

## 🎯 Expected Outcomes

### Move Counts
- **Beginner method average:** 100-150 moves
- **Your implementation:** 100-200 moves is normal
- **Optimal solution:** 20-30 moves (not expected!)

### Performance
- **Time per solve:** 0.1-1 seconds (depends on implementation)
- **Success rate:** 100% (should never fail)

### Code Quality
- Clear, readable code
- Well-commented
- Properly tested
- Error handling in place

---

## 🚀 Next Steps After Completion

Once you've completed the BeginnerSolver:

1. **Optimize move sequences**
   - Remove redundant moves (e.g., R R' = nothing)
   - Combine consecutive moves (e.g., R R = R2)
   - Simplify sequences

2. **Learn advanced methods**
   - CFOP (Fridrich method)
   - Roux method
   - Petrus method

3. **Implement optimal solvers**
   - Kociemba's algorithm (20 moves optimal)
   - IDA* search with pattern databases
   - Two-phase solver

4. **Add features**
   - Solution visualization
   - Move animation
   - Web interface
   - Solver comparison

---

## 💡 Remember

- **Learning is the goal**, not speed
- Test frequently as you build
- It's okay to look up algorithms
- Debugging is part of learning
- Ask for help when stuck
- Celebrate small wins!

**Good luck and have fun solving! 🧩✨**
