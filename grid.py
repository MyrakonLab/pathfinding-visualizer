"""
grid.py

Represents the maze as a graph.

Why this matters: every pathfinding algorithm needs something to search
through. That "something" is this Grid — a set of cells (nodes) where
each open cell is connected to the open cells directly above, below,
left, and right of it (edges). This file is the ONLY place that knows
about rows/cols/walls — every algorithm just asks it "what's next to
me?" and never touches the raw data itself.
"""


class Grid:
    def __init__(self, rows, cols):
        # How big the grid is. Used for bounds-checking later.
        self.rows = rows
        self.cols = cols

        # Walls are stored as a SET of (row, col) tuples, not a list.
        # Why a set? Checking "is this cell a wall?" happens constantly
        # while searching — a set does that check in O(1) average time,
        # a list would take O(n). Tuples (not lists) are used for the
        # positions because tuples are hashable, which is required for
        # anything stored inside a set or used as a dict key.
        self.walls = set()

        # These start out empty (None) until the caller sets them.
        # None here means "not configured yet" — a deliberate signal,
        # not a bug.
        self.start = None
        self.end = None

    def add_wall(self, row, col):
        """Mark a single cell as blocked."""
        self.walls.add((row, col))

    def is_wall(self, row, col):
        """O(1) average lookup — is this cell blocked?"""
        return (row, col) in self.walls

    def set_start(self, row, col):
        self.start = (row, col)

    def set_end(self, row, col):
        self.end = (row, col)

    def in_bounds(self, row, col):
        """
        Guards against walking off the edge of the grid.
        Without this check, neighbors() could return cells with
        negative indexes or indexes past the grid size — a classic
        source of crashes or silent wraparound bugs.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, row, col):
        """
        THE core graph method. Every algorithm in algorithms.py calls
        this and only this to figure out where it can move next.

        A cell has up to 4 neighbors: up, down, left, right.
        (No diagonals in this version — see future upgrades.)
        """
        candidates = [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right
        ]

        result = []
        for r, c in candidates:
            # Only keep a neighbor if it's actually on the grid
            # AND it isn't a wall. Both checks matter — skip either
            # one and the search can walk through walls or crash.
            if self.in_bounds(r, c) and not self.is_wall(r, c):
                result.append((r, c))

        return result
