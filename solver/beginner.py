"""
Beginner Layer-by-Layer Rubik's Cube Solver.

This module implements a beginner-friendly solving strategy that mirrors
how humans learn to solve a Rubik's Cube.

Strategy Overview (Layer-by-Layer Method):
==========================================

1. WHITE CROSS (Bottom Layer)
   - Solve 4 white edge pieces on the white (down) face
   - Each edge must match its adjacent center color
   - Creates a plus sign (+) on the bottom

2. WHITE CORNERS (Complete Bottom Layer)
   - Position and orient 4 white corner pieces
   - Completes the entire white face
   - First layer is now fully solved

3. MIDDLE LAYER (Second Layer)
   - Solve 4 edge pieces in the middle layer
   - No white or yellow on these edges
   - Two layers are now complete

4. LAST LAYER (Yellow Face - Top Layer)
   - Solve remaining yellow pieces in multiple sub-steps:
     a) Yellow cross (edges oriented correctly)
     b) Yellow corners positioned
     c) Yellow corners oriented
     d) Final edge positioning

Educational Philosophy:
======================
This code is designed to be READ and UNDERSTOOD, not just executed.
Each method is a skeleton with:
  - Clear explanations of the human strategy
  - TODO comments for implementation
  - Helper method stubs
  - Preconditions and postconditions
  - Sanity checks and debugging support

How to Use This Skeleton:
=========================
1. Read each method's docstring to understand the goal
2. Implement helper methods that find pieces
3. Implement logic to position and orient pieces
4. Use known move sequences (algorithms) for each case
5. Test thoroughly with the cube foundation's test suite

IMPORTANT: This solver prioritizes:
  - Understandability over optimality
  - Educational value over move count
  - Clear logic flow over clever tricks
"""

from typing import List, Optional, Tuple
from cube import CubeState, apply_move, apply_sequence


class BeginnerSolver:
    """
    Layer-by-layer Rubik's Cube solver for beginners.

    This solver implements the classic beginner method taught in tutorials.
    It solves the cube in distinct phases, each building on the previous.

    Attributes:
        max_iterations: Safety limit to prevent infinite loops
        debug: Enable detailed logging for learning/debugging

    Example:
        >>> solver = BeginnerSolver(debug=True)
        >>> cube = scrambled_cube  # Some scrambled state
        >>> solution = solver.solve(cube)
        >>> # solution is a list of moves like ['R', 'U', "R'", ...]
    """

    def __init__(self, max_iterations: int = 1000, debug: bool = False):
        """
        Initialize the BeginnerSolver.

        Args:
            max_iterations: Maximum iterations per phase to prevent infinite loops
            debug: If True, print detailed solving progress
        """
        self.max_iterations = max_iterations
        self.debug = debug

    def solve(self, cube: CubeState) -> List[str]:
        """
        Solve a Rubik's Cube using the beginner layer-by-layer method.

        This is the main entry point. It orchestrates the entire solving process
        by calling each phase in sequence.

        Args:
            cube: The scrambled cube state to solve

        Returns:
            List of moves that solve the cube (e.g., ['R', 'U', "R'", ...])

        Raises:
            ValueError: If cube is invalid or unsolvable
            RuntimeError: If solver gets stuck (exceeds iteration limits)

        Strategy:
            1. Solve white cross (bottom layer edges)
            2. Solve white corners (complete bottom layer)
            3. Solve middle layer edges
            4. Solve last layer (yellow)

        Note:
            The returned move sequence can be quite long (100-200 moves).
            That's normal for the beginner method!
        """
        if self.debug:
            print("Starting BeginnerSolver...")
            print(f"Initial state: {cube}")

        # Accumulate all moves in solution
        solution = []

        # Phase 1: White Cross
        if self.debug:
            print("\n=== Phase 1: White Cross ===")
        cross_moves = self.solve_white_cross(cube)
        solution.extend(cross_moves)
        cube = apply_sequence(cube, cross_moves)

        # TODO: Add validation that white cross is actually solved
        # assert self._is_white_cross_solved(cube), "White cross not solved!"

        # Phase 2: White Corners
        if self.debug:
            print("\n=== Phase 2: White Corners ===")
        corner_moves = self.solve_white_corners(cube)
        solution.extend(corner_moves)
        cube = apply_sequence(cube, corner_moves)

        # TODO: Add validation that white face is complete
        # assert self._is_white_face_solved(cube), "White face not solved!"

        # Phase 3: Middle Layer
        if self.debug:
            print("\n=== Phase 3: Middle Layer ===")
        middle_moves = self.solve_middle_layer(cube)
        solution.extend(middle_moves)
        cube = apply_sequence(cube, middle_moves)

        # TODO: Add validation that middle layer is solved
        # assert self._is_middle_layer_solved(cube), "Middle layer not solved!"

        # Phase 4: Last Layer (Yellow)
        if self.debug:
            print("\n=== Phase 4: Last Layer ===")
        last_moves = self.solve_last_layer(cube)
        solution.extend(last_moves)
        cube = apply_sequence(cube, last_moves)

        # Final validation
        if not cube.is_solved():
            raise RuntimeError(
                f"Solver completed all phases but cube is not solved! "
                f"This indicates a bug in the solver logic. "
                f"Solution length: {len(solution)} moves"
            )

        if self.debug:
            print(f"\n=== SOLVED! ===")
            print(f"Total moves: {len(solution)}")

        return solution

    # ========================================================================
    # Phase 1: White Cross
    # ========================================================================

    def solve_white_cross(self, cube: CubeState) -> List[str]:
        """
        Solve the white cross on the bottom (D) face.

        GOAL:
        ====
        Create a plus sign (+) of white edges on the bottom face, where each
        edge also matches the color of its adjacent center.

        Example of solved white cross (viewing from bottom):
                    W W W
                    W W W
                    W W W
            O O O   G G G   R R R   B B B
            . O .   . G .   . R .   . B .
            . . .   . . .   . . .   . . .

        The white edges at D[1], D[3], D[5], D[7] are correctly positioned
        and the adjacent colors (O, G, R, B) match the center colors.

        PRECONDITIONS:
        =============
        - None (this is the first step)

        POSTCONDITIONS:
        ==============
        - Four white edge pieces on D face
        - Each edge correctly oriented (white on bottom)
        - Each edge in correct position (matches adjacent center)

        STRATEGY:
        ========
        For beginners, the white cross is solved intuitively:

        1. Find a white edge piece (anywhere on the cube)
        2. Determine where it belongs (which position on D face)
        3. Move it to that position using simple moves
        4. Repeat for all 4 edges

        Common techniques:
        - If edge is on U face: move it above target, then insert down
        - If edge is on middle layer: move it up first
        - If edge is on D face but wrong: move it up and reinsert

        IMPLEMENTATION HINTS:
        ====================
        - Use helper methods to find unsolved edges
        - Break into cases based on current edge position
        - Use simple move sequences, not optimal algorithms
        - Check after each edge to avoid breaking previous work

        Args:
            cube: Current cube state

        Returns:
            List of moves to solve the white cross
        """
        moves = []

        # TODO: Implement white cross solving logic
        #
        # Suggested approach:
        # 1. Loop through 4 edge positions on D face
        # 2. For each position:
        #    a) Find the white edge that belongs there
        #    b) Move it to the top layer if not already there
        #    c) Position it above the target location
        #    d) Insert it into place
        # 3. Add iteration limit to prevent infinite loops
        #
        # Example pseudocode:
        #   for target_position in [D_north, D_east, D_south, D_west]:
        #       while not edge_solved_at(target_position):
        #           edge = find_white_edge_for(target_position)
        #           moves += move_edge_to_top(edge)
        #           moves += position_above_target(edge, target_position)
        #           moves += insert_edge_down()
        #           iterations += 1
        #           if iterations > max: raise error

        # For now, return empty list (no implementation)
        # Learners will implement this logic
        return moves

    def _find_white_edge(self, cube: CubeState, target_color: str) -> Optional[Tuple[str, int]]:
        """
        Find a white edge piece that should pair with the given color.

        This is a helper method for solve_white_cross().

        Args:
            cube: Current cube state
            target_color: The non-white color of the edge we're looking for
                         (e.g., 'R' for the white-red edge)

        Returns:
            (face, position) where the edge is located, or None if not found

        Example:
            If looking for white-red edge, might return ('U', 1) meaning
            the edge is at the top face, position 1.

        TODO: Implement edge finding logic
        - Check all edge positions on the cube
        - Look for a piece with white and target_color
        - Return its location
        """
        # TODO: Implement
        return None

    def _is_white_cross_solved(self, cube: CubeState) -> bool:
        """
        Check if the white cross is correctly solved.

        A solved white cross means:
        1. D face has white at positions 1, 3, 5, 7 (the edges)
        2. Each edge's other color matches the adjacent center

        Args:
            cube: Current cube state

        Returns:
            True if white cross is solved, False otherwise

        TODO: Implement validation logic
        """
        # TODO: Implement
        # Check D[1], D[3], D[5], D[7] are white
        # Check adjacent colors match F, R, B, L centers
        return False

    # ========================================================================
    # Phase 2: White Corners
    # ========================================================================

    def solve_white_corners(self, cube: CubeState) -> List[str]:
        """
        Solve the four white corner pieces to complete the white face.

        GOAL:
        ====
        Position and orient all four white corners so the entire white (D) face
        is complete, and the first layer of adjacent colors also matches.

        Example of solved white face (viewing from bottom):
                    W W W
                    W W W
                    W W W
            O O O   G G G   R R R   B B B
            O O O   G G G   R R R   B B B
            . . .   . . .   . . .   . . .

        PRECONDITIONS:
        =============
        - White cross is solved (from Phase 1)

        POSTCONDITIONS:
        ==============
        - All 9 stickers on D face are white
        - First layer of F, R, B, L faces match their centers

        STRATEGY:
        ========
        The beginner method for corners:

        1. Find a white corner piece (must have white + 2 other colors)
        2. Determine where it belongs (which D face corner)
        3. Move it to the top layer (U face) if not already there
        4. Position it above its target location
        5. Use a simple algorithm to insert it correctly oriented

        Common Algorithm (Right Corner Insert):
            R U R' U'   (repeated 1-5 times depending on orientation)

        This moves a corner from top-right position into bottom-right,
        potentially rotating it to get white facing down.

        KEY INSIGHT:
        ===========
        - Corners can be in 3 orientations (white on D, white on side, white on front)
        - You may need to repeat the algorithm multiple times
        - Don't worry about breaking the cross - it stays solved!

        IMPLEMENTATION HINTS:
        ====================
        - Work on one corner at a time
        - Always move corner to U layer first (if not already there)
        - Position above target using U moves
        - Apply algorithm until corner is correctly oriented
        - Move to next corner

        Args:
            cube: Current cube state (with white cross solved)

        Returns:
            List of moves to solve white corners
        """
        moves = []

        # TODO: Implement white corners solving logic
        #
        # Suggested approach:
        # 1. Loop through 4 corner positions on D face
        # 2. For each corner:
        #    a) Find the corner piece that belongs there
        #    b) Move it to U layer if on D layer
        #    c) Position above target using U moves
        #    d) Apply insertion algorithm (R U R' U') repeatedly
        #    e) Check orientation and repeat if needed
        # 3. Add iteration limit
        #
        # Example algorithm:
        #   RIGHT_CORNER_INSERT = ['R', 'U', "R'", "U'"]
        #
        #   for corner_position in [DRF, DRB, DLB, DLF]:
        #       corner = find_white_corner_for(corner_position)
        #       moves += bring_to_top(corner)
        #       moves += position_above_target(corner, corner_position)
        #
        #       # Insert and orient
        #       for _ in range(5):  # Max 5 iterations to orient
        #           if corner_correctly_oriented():
        #               break
        #           moves += RIGHT_CORNER_INSERT
        #           cube = apply_sequence(cube, RIGHT_CORNER_INSERT)

        return moves

    def _find_white_corner(self, cube: CubeState, colors: Tuple[str, str]) -> Optional[Tuple[str, int]]:
        """
        Find a white corner piece with the given two other colors.

        This is a helper method for solve_white_corners().

        Args:
            cube: Current cube state
            colors: The two non-white colors of the corner
                   (e.g., ('R', 'G') for white-red-green corner)

        Returns:
            (face, position) where the corner is located, or None if not found

        TODO: Implement corner finding logic
        - Check all 8 corner positions
        - Look for piece with white + the two given colors
        - Return its location
        """
        # TODO: Implement
        return None

    def _is_white_face_solved(self, cube: CubeState) -> bool:
        """
        Check if the entire white face is correctly solved.

        A solved white face means:
        1. All 9 stickers on D face are white
        2. First layer of adjacent faces match their centers

        Args:
            cube: Current cube state

        Returns:
            True if white face is complete, False otherwise

        TODO: Implement validation logic
        """
        # TODO: Implement
        return False

    # ========================================================================
    # Phase 3: Middle Layer
    # ========================================================================

    def solve_middle_layer(self, cube: CubeState) -> List[str]:
        """
        Solve the four edge pieces in the middle layer.

        GOAL:
        ====
        Position the four middle-layer edges correctly, completing the first
        two layers of the cube.

        These are the edges WITHOUT white or yellow (the center layer).

        Example: After this phase, looking at front and right:
            . . .   . . .
            G G G   R R R
            G G G   R R R

        PRECONDITIONS:
        =============
        - White face completely solved (from Phase 2)
        - First layer complete

        POSTCONDITIONS:
        ==============
        - Four middle layer edges correctly positioned
        - First two layers completely solved
        - Only the yellow (U) layer remains unsolved

        STRATEGY:
        ========
        The beginner method for middle layer:

        1. Find an edge on the U (top) layer that has no yellow
        2. Determine where it belongs in the middle layer
        3. Position it above its target location (using U moves)
        4. Use one of two algorithms to insert it:
           - Left algorithm: inserts edge to the left
           - Right algorithm: inserts edge to the right

        Common Algorithms:

        Right Algorithm (inserts edge to right side):
            U R U' R' U' F' U F

        Left Algorithm (inserts edge to left side):
            U' L' U L U F U' F'

        WHICH ALGORITHM TO USE:
        ======================
        Look at the edge on U face:
        - If target position is to the RIGHT: use right algorithm
        - If target position is to the LEFT: use left algorithm

        EDGE CASES:
        ==========
        - If edge is in middle layer but WRONG: move it to U layer first
        - If edge is in middle layer but FLIPPED: move it to U, then reinsert
        - If no valid edges on U layer: move a wrong edge up to make space

        IMPLEMENTATION HINTS:
        ====================
        - Work on one edge at a time
        - Only edges without yellow can go in middle layer
        - May need to extract wrong edges before inserting correct ones
        - Add iteration limit (should solve in 4-8 edge insertions)

        Args:
            cube: Current cube state (with white face solved)

        Returns:
            List of moves to solve middle layer
        """
        moves = []

        # TODO: Implement middle layer solving logic
        #
        # Suggested approach:
        # 1. Find 4 middle-layer edge pieces (no white/yellow)
        # 2. For each edge:
        #    a) If in middle layer but wrong, move to U layer
        #    b) Position above target location using U moves
        #    c) Determine if target is to left or right
        #    d) Apply appropriate algorithm (left or right)
        #    e) Verify edge is correctly placed
        # 3. Repeat until all 4 edges solved
        #
        # Example algorithms:
        #   RIGHT_ALGO = ['U', 'R', "U'", "R'", "U'", "F'", 'U', 'F']
        #   LEFT_ALGO = ["U'", "L'", 'U', 'L', 'U', 'F', "U'", "F'"]
        #
        # Example loop:
        #   for _ in range(4):  # 4 edges to solve
        #       edge = find_unsolved_middle_edge()
        #       if edge_in_middle_but_wrong():
        #           moves += extract_to_top(edge)
        #       moves += position_above_target(edge)
        #       if target_is_right():
        #           moves += RIGHT_ALGO
        #       else:
        #           moves += LEFT_ALGO

        return moves

    def _find_middle_edge(self, cube: CubeState) -> Optional[Tuple[str, int]]:
        """
        Find an edge piece that belongs in the middle layer.

        Middle layer edges have no white or yellow.

        Args:
            cube: Current cube state

        Returns:
            (face, position) where a middle edge is located, or None

        TODO: Implement
        - Look for edges on U face without yellow
        - Or edges in middle layer that are incorrectly placed
        """
        # TODO: Implement
        return None

    def _is_middle_layer_solved(self, cube: CubeState) -> bool:
        """
        Check if the middle layer is correctly solved.

        A solved middle layer means:
        1. All 4 middle edges are correctly positioned
        2. First two layers are completely solved

        Args:
            cube: Current cube state

        Returns:
            True if middle layer is solved, False otherwise

        TODO: Implement validation logic
        """
        # TODO: Implement
        return False

    # ========================================================================
    # Phase 4: Last Layer (Yellow)
    # ========================================================================

    def solve_last_layer(self, cube: CubeState) -> List[str]:
        """
        Solve the last layer (yellow face on top).

        GOAL:
        ====
        Complete the entire cube by solving all yellow pieces on the U (top) face.

        This is the most complex phase and typically involves multiple sub-steps:
        1. Yellow cross (orient edges)
        2. Yellow face (orient corners)
        3. Position corners
        4. Position edges

        PRECONDITIONS:
        =============
        - White face solved
        - Middle layer solved
        - First two layers complete

        POSTCONDITIONS:
        ==============
        - Entire cube is solved!

        STRATEGY:
        ========
        The beginner method breaks last layer into sub-steps:

        STEP 4A: Yellow Cross
        ---------------------
        Get a yellow plus sign (+) on top, using the F R U R' U' F' algorithm.
        May need to repeat from different starting positions (dot, L, line, cross).

        STEP 4B: Yellow Corners Orientation
        ---------------------
        Orient all yellow corners so yellow faces up (not necessarily in correct positions).
        Uses repeated R U R' U R U2 R' algorithm.

        STEP 4C: Position Yellow Corners
        ---------------------
        Move corners to their correct positions (even if rotated wrong).
        Uses corner-swapping algorithm.

        STEP 4D: Position Yellow Edges
        ---------------------
        Final step - position the 4 yellow edges correctly.
        Uses edge-cycling algorithm.

        IMPLEMENTATION HINTS:
        ====================
        This phase is the longest and most algorithm-heavy.
        Break it into clear sub-methods for each step.
        Each algorithm may need to be repeated multiple times.
        Add validation between steps.

        Args:
            cube: Current cube state (with 2 layers solved)

        Returns:
            List of moves to solve the last layer
        """
        moves = []

        # Sub-step 4A: Yellow Cross
        # TODO: Implement yellow cross logic
        # Algorithm: F R U R' U' F' (may need 1-3 applications)
        moves_4a = self._solve_yellow_cross(cube)
        moves.extend(moves_4a)
        cube = apply_sequence(cube, moves_4a)

        # Sub-step 4B: Yellow Corners Orientation
        # TODO: Implement corner orientation logic
        # Algorithm: R U R' U R U2 R' (repeated for each corner)
        moves_4b = self._solve_yellow_corners_orientation(cube)
        moves.extend(moves_4b)
        cube = apply_sequence(cube, moves_4b)

        # Sub-step 4C: Position Yellow Corners
        # TODO: Implement corner positioning logic
        moves_4c = self._solve_yellow_corners_position(cube)
        moves.extend(moves_4c)
        cube = apply_sequence(cube, moves_4c)

        # Sub-step 4D: Position Yellow Edges
        # TODO: Implement edge positioning logic
        moves_4d = self._solve_yellow_edges_position(cube)
        moves.extend(moves_4d)
        cube = apply_sequence(cube, moves_4d)

        return moves

    def _solve_yellow_cross(self, cube: CubeState) -> List[str]:
        """
        Create a yellow cross on the top (U) face.

        GOAL: Get yellow at U[1], U[3], U[5], U[7] (edge positions).

        Cases:
        - Dot (no yellow edges): apply algorithm 3 times
        - L shape (2 yellow edges forming L): position and apply once
        - Line (2 opposite yellow edges): position and apply once
        - Cross (all 4 yellow edges): done!

        Algorithm: F R U R' U' F'

        Args:
            cube: Current cube state

        Returns:
            Moves to create yellow cross

        TODO: Implement
        - Detect current pattern (dot, L, line, cross)
        - Apply algorithm appropriate number of times
        - Verify yellow cross is formed
        """
        moves = []
        # TODO: Implement
        return moves

    def _solve_yellow_corners_orientation(self, cube: CubeState) -> List[str]:
        """
        Orient all yellow corners so yellow faces upward.

        GOAL: All 4 corners have yellow on U face (may not be in correct positions yet).

        Algorithm: R U R' U R U2 R' (called "Sune" or similar)

        Strategy:
        - Hold cube with one correctly oriented corner at a specific position
        - Apply algorithm to orient other corners
        - May need to repeat algorithm and rotate cube

        Args:
            cube: Current cube state (with yellow cross)

        Returns:
            Moves to orient yellow corners

        TODO: Implement
        - Count how many corners are correctly oriented
        - Apply algorithm until all oriented correctly
        """
        moves = []
        # TODO: Implement
        return moves

    def _solve_yellow_corners_position(self, cube: CubeState) -> List[str]:
        """
        Position yellow corners in their correct locations.

        GOAL: Each corner is in its correct position (even if rotated).

        Algorithm: U R U' L' U R' U' L (corner swap)

        Strategy:
        - Find a corner that's already in correct position (if any)
        - Hold it at a reference position
        - Apply algorithm to cycle other 3 corners
        - Repeat if needed

        Args:
            cube: Current cube state (with yellow corners oriented)

        Returns:
            Moves to position yellow corners

        TODO: Implement
        - Detect which corners are in correct positions
        - Apply swapping algorithm as needed
        """
        moves = []
        # TODO: Implement
        return moves

    def _solve_yellow_edges_position(self, cube: CubeState) -> List[str]:
        """
        Position yellow edges to complete the cube.

        GOAL: Each edge is in its final correct position.

        Algorithm: F2 U L R' F2 L' R U F2 (or similar edge-cycling algorithm)

        Strategy:
        - Find edges that are incorrectly positioned
        - Apply algorithm to cycle 3 edges
        - Repeat until all edges correct

        Args:
            cube: Current cube state (with corners solved)

        Returns:
            Moves to position yellow edges

        TODO: Implement
        - Detect which edges need to be moved
        - Apply edge-cycling algorithm
        - Verify cube is fully solved
        """
        moves = []
        # TODO: Implement
        return moves


# =============================================================================
# Learning Path for Students
# =============================================================================
"""
HOW TO IMPLEMENT THIS SOLVER:
=============================

Step 1: Start with White Cross (Easiest)
-----------------------------------------
Implement solve_white_cross() first. This is the most intuitive phase.

Tasks:
1. Implement _find_white_edge() to locate white edge pieces
2. Implement _is_white_cross_solved() to verify your work
3. Write simple logic to move edges to the top, then insert down
4. Test with a cube that only has white cross scrambled

Step 2: White Corners (Moderate)
---------------------------------
Implement solve_white_corners() next.

Tasks:
1. Implement _find_white_corner() to locate corner pieces
2. Learn the "R U R' U'" algorithm and when to apply it
3. Implement logic to repeat algorithm until corner is oriented
4. Test with a cube that has white cross solved but corners scrambled

Step 3: Middle Layer (Moderate-Hard)
-------------------------------------
Implement solve_middle_layer().

Tasks:
1. Implement _find_middle_edge() to find edges without yellow/white
2. Learn the left and right insertion algorithms
3. Implement logic to determine which algorithm to use
4. Handle edge case: extracting wrongly placed edges
5. Test with a cube that has bottom layer solved

Step 4: Last Layer (Most Complex)
----------------------------------
Implement solve_last_layer() and its sub-methods.

Tasks:
1. Break into 4 sub-steps (cross, orient corners, position corners, position edges)
2. Learn the algorithm for each sub-step
3. Implement detection logic for each pattern/case
4. Test each sub-step independently
5. Integrate all sub-steps

Step 5: Integration and Testing
--------------------------------
1. Test with fully scrambled cubes
2. Add error handling and iteration limits
3. Optimize move sequences (optional)
4. Add detailed logging for debugging


DEBUGGING TIPS:
===============

1. Test Each Phase Independently
   - Create cubes with only later phases scrambled
   - Verify each phase works before moving to next

2. Use Assertions Liberally
   - Check preconditions at start of each method
   - Check postconditions at end
   - Add intermediate checks during solving

3. Add Logging
   - Print which piece you're working on
   - Print moves being applied
   - Print cube state after each major operation

4. Visualize
   - Use the cube's __str__ method to print state
   - Manually verify pieces are moving as expected
   - Use a physical cube alongside the code

5. Iteration Limits
   - Add max iteration counters to prevent infinite loops
   - If limit reached, print current state for debugging
   - Gradually increase limit as you gain confidence


COMMON BEGINNER ALGORITHMS TO RESEARCH:
=======================================

White Cross:
- Intuitive (no fixed algorithm needed)

White Corners:
- R U R' U' (right corner insert)
- L' U' L U (left corner insert)

Middle Layer:
- U R U' R' U' F' U F (right edge insert)
- U' L' U L U F U' F' (left edge insert)

Last Layer - Yellow Cross:
- F R U R' U' F' (cross formation)

Last Layer - Corner Orientation:
- R U R' U R U2 R' (Sune)
- U R U' L' U R' U' L (adjacent corner swap)

Last Layer - Corner Position:
- R' F R' B2 R F' R' B2 R2 (corner 3-cycle)

Last Layer - Edge Position:
- F2 U L R' F2 L' R U F2 (edge 3-cycle)


REMEMBER:
=========
- This solver is for LEARNING, not for speed
- Focus on understanding WHY each step works
- It's okay if your solution is 200+ moves
- Test thoroughly at each phase
- Read beginner tutorials to understand algorithms
- Use the cube foundation's test suite to verify correctness
"""
