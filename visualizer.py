"""
visualizer.py

Turns a Grid (and optionally a path) into something you can actually
look at in the terminal. This file knows nothing about HOW a path was
found — it only knows how to draw one. That separation means we can
swap this out for a GUI later (see future upgrades) without touching
grid.py or algorithms.py at all.
"""


def render(grid, path=None):
    """
    Prints the grid using:
        S = start
        E = end
        # = wall
        * = part of the found path
        . = open, unused cell
    """
    # Default to an empty list if no path was given, so "cell in path"
    # below never crashes on None.
    path = path or []

    for row in range(grid.rows):
        line = ""
        for col in range(grid.cols):
            cell = (row, col)

            # Order matters here: we check start/end BEFORE wall,
            # so if a wall ever accidentally overlaps the start or
            # end cell, we still see S/E instead of silently hiding
            # that bug behind a #.
            if cell == grid.start:
                line += "S "
            elif cell == grid.end:
                line += "E "
            elif grid.is_wall(row, col):
                line += "# "
            elif cell in path:
                line += "* "
            else:
                line += ". "

        print(line)
