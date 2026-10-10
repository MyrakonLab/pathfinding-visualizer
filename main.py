"""
main.py

The only file that ties grid.py, algorithms.py, and visualizer.py
together. Nothing in the other files knows this file exists — that's
intentional. It's the "wiring," not the logic.
"""

from grid import Grid
from algorithms import bfs, dfs, dijkstra, a_star
from visualizer import render


def build_demo_grid():
    """
    Separated into its own function so swapping in a different maze
    later (or loading one from a file) is a one-function change,
    instead of hunting through main().
    """
    grid = Grid(5, 5)
    grid.set_start(0, 0)
    grid.set_end(4, 4)

    # A small wall cluster so the algorithms actually have to route
    # around something instead of walking in a straight line.
    for wall in [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]:
        grid.add_wall(*wall)

    return grid


def main():
    grid = build_demo_grid()

    print("Grid:")
    render(grid)

    # A list of (label, function) pairs. In Python, a function name
    # with no parentheses after it is just a reference — the same as
    # any other value — so we can store all four algorithms in a list
    # and loop over them instead of writing four near-identical blocks.
    algorithms = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("Dijkstra", dijkstra),
        ("A*", a_star),
    ]

    for name, algorithm in algorithms:
        path = algorithm(grid)

        # Ternary expression: use len(path) if a path was found,
        # otherwise fall back to 0 — avoids crashing on None.
        step_count = len(path) if path else 0

        print(f"\n{name} path ({step_count} steps):")
        render(grid, path)


# This guard means "only run main() if this file is executed directly,
# not if it's imported by something else" — standard Python practice,
# and useful later if we ever import these functions into tests.
if __name__ == "__main__":
    main()
