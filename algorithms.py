"""
algorithms.py

All four search algorithms live here. None of them print anything or
know about the terminal — they take a Grid in and return a path (a
list of (row, col) tuples) or None if no path exists. Keeping search
logic separate from display logic means we can test/reuse it anywhere.

All four functions share the same skeleton:
    1. Start with a "frontier" (cells we still need to explore).
    2. Pop one cell off the frontier.
    3. If it's the goal, stop.
    4. Otherwise, look at its neighbors and add the new ones to the
       frontier, remembering which cell led to each ("came_from").
    5. When done, walk backward through came_from to build the path.

What changes between them is HOW the frontier picks which cell to
explore next. That single difference is the entire personality of
each algorithm.
"""

from collections import deque
import heapq


def reconstruct_path(came_from, start, end):
    """
    Shared by every algorithm below. came_from is a dictionary mapping
    each visited cell to "the cell that led me here". Starting at the
    end and following that trail backward rebuilds the full path.
    """
    # If the end was never reached, there's no path to reconstruct.
    if end not in came_from:
        return None

    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)

    # We built this from end -> start, so flip it to read start -> end.
    path.reverse()
    return path


# ---------------------------------------------------------------------
# BFS — Breadth-First Search
# ---------------------------------------------------------------------
def bfs(grid):
    """
    Explores the grid layer by layer, like ripples spreading from a
    stone dropped in water. Because it always explores the CLOSEST
    unvisited cells first, the first time it reaches the goal, that
    path is guaranteed to be the shortest possible (on an unweighted
    grid). Time complexity: O(V + E).
    """
    start = grid.start
    end = grid.end

    # deque (double-ended queue) gives O(1) removal from the front.
    # A plain list's pop(0) is O(n) — a common beginner performance
    # trap on larger grids.
    frontier = deque([start])

    # came_from doubles as our "visited" tracker AND our breadcrumb
    # trail for rebuilding the path afterward.
    came_from = {start: None}

    while frontier:
        # popleft() takes the OLDEST discovered cell — this FIFO
        # (first in, first out) order is what makes this breadth-first
        # instead of depth-first.
        current = frontier.popleft()

        if current == end:
            break  # Found it — no need to keep exploring.

        for neighbor in grid.neighbors(*current):
            # The * unpacks the (row, col) tuple into two arguments,
            # since neighbors() expects row, col separately.
            if neighbor not in came_from:
                # First time seeing this cell — queue it up and
                # remember how we got here.
                frontier.append(neighbor)
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)


# ---------------------------------------------------------------------
# DFS — Depth-First Search
# ---------------------------------------------------------------------
def dfs(grid):
    """
    Identical structure to bfs() above, with ONE change: the frontier
    is a plain list used as a STACK (LIFO — last in, first out)
    instead of a queue. That single change — removing from the END
    instead of the FRONT — is the entire difference between depth-
    first and breadth-first search.

    DFS dives down one direction until it hits a dead end, then
    backtracks. It does NOT guarantee the shortest path — only that
    a path will be found if one exists.
    """
    start = grid.start
    end = grid.end

    frontier = [start]           # plain list, used as a stack
    came_from = {start: None}

    while frontier:
        current = frontier.pop()  # removes from the END, not the front

        if current == end:
            break

        for neighbor in grid.neighbors(*current):
            if neighbor not in came_from:
                frontier.append(neighbor)
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)


# ---------------------------------------------------------------------
# Dijkstra — Weighted Shortest Path
# ---------------------------------------------------------------------
def dijkstra(grid, weight_fn=None):
    """
    Like BFS, but built for grids where not all cells cost the same to
    cross (e.g. "mud" cells that slow you down). Instead of a plain
    queue, the frontier is a PRIORITY QUEUE (a min-heap) ordered by
    total cost so far — always explore the cheapest known option next.

    Time complexity: O((V + E) log V) — the log V comes from heap
    push/pop operations.
    """
    start = grid.start
    end = grid.end

    # If the caller doesn't supply a custom cost function, every cell
    # costs 1 to enter (this makes Dijkstra behave like BFS when all
    # weights are equal — a nice sanity check).
    weight_fn = weight_fn or (lambda cell: 1)

    # heapq keeps a list ordered by the FIRST element of each tuple,
    # so (cost, cell) tuples naturally sort by cost, cheapest first.
    frontier = [(0, start)]

    came_from = {start: None}

    # Unlike BFS's simple "visited" set, we track the CHEAPEST cost
    # found so far to reach each cell — because with weights, a cell
    # might later be reachable more cheaply via a different route.
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)  # cheapest first

        if current == end:
            break

        for neighbor in grid.neighbors(*current):
            new_cost = current_cost + weight_fn(neighbor)

            # Only update if we've never reached this neighbor before,
            # OR we just found a cheaper way to reach it.
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)


# ---------------------------------------------------------------------
# A* — Heuristic-Guided Search
# ---------------------------------------------------------------------
def heuristic(a, b):
    """
    Manhattan distance: the number of grid steps between two cells if
    you could ignore walls entirely. It's an ESTIMATE, not the real
    distance — which is exactly the point of a heuristic. It never
    overestimates the true cost on a grid with no diagonal movement,
    which is what keeps A* correct (still finds the shortest path).
    """
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)


def a_star(grid, weight_fn=None):
    """
    Dijkstra, plus an educated guess about which direction the goal
    is in. The frontier is ordered by:

        cost_so_far (real cost so far) + heuristic (estimated cost left)

    instead of just cost_so_far. This biases exploration toward the
    goal, usually visiting far fewer cells than Dijkstra while still
    finding the same shortest path.
    """
    start = grid.start
    end = grid.end
    weight_fn = weight_fn or (lambda cell: 1)

    frontier = [(0, start)]
    came_from = {start: None}

    # cost_so_far tracks the REAL cost — used both for correctness
    # and for computing each neighbor's total priority below.
    cost_so_far = {start: 0}

    while frontier:
        # The underscore _ means "I'm receiving this value but
        # deliberately ignoring it" — we only need the cell itself,
        # not the priority number that got it popped.
        _, current = heapq.heappop(frontier)

        if current == end:
            break

        for neighbor in grid.neighbors(*current):
            new_cost = cost_so_far[current] + weight_fn(neighbor)

            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost

                # priority = real cost + estimated remaining cost.
                # This is the ONLY real difference from dijkstra().
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)
