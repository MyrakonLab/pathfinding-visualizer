# PATHMIND — COMPLETE MYRAKON_LAB BUILD SCRIPT
### From empty starter project → finished pathfinding visualizer

---

## PART 1 — PROJECT LEARNING BRIEF

**What we're building:** A terminal-based pathfinding visualizer. A grid with walls, a start point, an end point — and four algorithms (BFS, DFS, Dijkstra, A*) that search it and show their path.

**Why it matters:** This is the exact logic behind GPS routing, game-AI movement, and network packet routing. It's also one of the most common technical-interview topics (graph traversal) — this project doubles as interview prep.

**What you'll learn (new):** Graphs, Queues, Stacks, Priority Queues/Heaps, BFS, DFS, Dijkstra, A*.
**What you already have:** Python, OOP, Big-O, Recursion, Lists.

**DSA connection:** the grid *is* a graph — each cell is a node, each open neighboring cell is an edge. Every algorithm here is really just "how do I choose which node to visit next?"

---

## PART 2 — PROJECT SPEC

| | |
|---|---|
| **Name** | PathMind |
| **Problem** | Finding the best route through obstacles |
| **Solution** | A grid + 4 interchangeable search algorithms |
| **DSA concepts** | Graphs, Queues, Stacks, Heaps, BFS, DFS, Dijkstra, A* |
| **Python concepts** | Classes, sets, tuples, dictionaries, `collections.deque`, `heapq` |
| **Tech** | Pure Python, terminal output (V1) |
| **User flow** | Build a grid → add walls → pick start/end → run an algorithm → see the path and its cost |
| **Future upgrades** | ML-predicted heuristics, web deployment, real map data, LLM routing-explainer agent |

---

## PART 3 — ARCHITECTURE

```
pathmind/
├── main.py         → builds a demo grid, runs algorithms, prints results
├── grid.py         → Grid class: cells, walls, start/end, neighbor lookup
├── algorithms.py   → bfs(), dfs(), dijkstra(), a_star(), reconstruct_path()
├── visualizer.py   → render(): prints the grid + path to the terminal
└── README.md
```

- `grid.py` exists because every algorithm needs the same "what's next to me?" logic — one source of truth.
- `algorithms.py` holds pure search logic — no printing, no I/O. Keeps it testable.
- `visualizer.py` is separate so *how we display things* never tangles with *how we search*.
- `main.py` is the only file that wires everything together.

---

## PART 4 — STARTER PROJECT (what's on screen at 0:00)

```python
# grid.py
class Grid:
    def __init__(self, rows, cols):
        pass
```

```python
# algorithms.py
def bfs(grid):
    pass

def dfs(grid):
    pass

def dijkstra(grid):
    pass

def a_star(grid):
    pass
```

```python
# visualizer.py
def render(grid, path=None):
    pass
```

```python
# main.py
from grid import Grid
from algorithms import bfs, dfs, dijkstra, a_star
from visualizer import render

def main():
    pass

if __name__ == "__main__":
    main()
```

**GitHub:** `starter-code` branch = exactly the above. `main` branch = the finished version we build across this script.

---

## PART 5 — VIDEO OPENING

**0:00 — HOOK**
SCREEN: Finished app running in terminal — path animating from S to E through a maze of `#` walls.
OVERLAY: **"I BUILT A PATHFINDER FROM SCRATCH"**
MOTION: Slow zoom into the terminal.
SOUND: Soft interface hit.

**0:06 — INTRO**
OVERLAY: **"LET'S BUILD PATHMIND"** → **"BFS · DFS · DIJKSTRA · A*"** → **"NO LIBRARIES. JUST LOGIC."**

**0:20 — STARTER PROJECT**
SCREEN: VS Code, folder structure from Part 4.
OVERLAY: **"STARTING FROM HERE"** → **"NO IMPLEMENTATION YET"**

---

## PART 6 — FULL BUILD

### STEP 1 — The Grid (our graph)

**A. What we're building:** A `Grid` class storing size, walls, start, and end.
**B. Why:** Every algorithm needs something to search. This is that something.
**C. Concept — what's a graph?** A graph is things (**nodes**) connected to other things (**edges**) — like subway stations connected by tracks. Our grid is a graph in disguise: each cell is a node, each adjacent open cell is an edge.
**D. DSA connection:** every algorithm below walks node → neighbor → neighbor, along edges. That's *all* graph traversal ever is.
**E. File:** `grid.py`

**G. Code to type:**
```python
class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.walls = set()
        self.start = None
        self.end = None

    def add_wall(self, row, col):
        self.walls.add((row, col))

    def is_wall(self, row, col):
        return (row, col) in self.walls

    def set_start(self, row, col):
        self.start = (row, col)

    def set_end(self, row, col):
        self.end = (row, col)

    def in_bounds(self, row, col):
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, row, col):
        candidates = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        result = []
        for r, c in candidates:
            if self.in_bounds(r, c) and not self.is_wall(r, c):
                result.append((r, c))
        return result
```

**H. Line-by-line:**
- `self.walls = set()` — a **set**, not a list. Sets give O(1) average "is this in here?" checks, vs O(n) for a list. We'll check "is this a wall?" constantly, so this matters.
- `self.start = None` / `self.end = None` — placeholders until set.
- `add_wall` / `is_wall` — store and check `(row, col)` tuples. Tuples are used (not lists) because they're **hashable** — required for anything going into a `set` or used as a `dict` key.
- `in_bounds` — guards against walking off the grid edge. Skip this and you'll get index errors or infinite wraparound bugs.
- `neighbors` — the heart of the graph. For any cell, look up, down, left, right; keep only the ones inside the grid and not walled off. **This one method is what every algorithm below calls.**

**I. Prediction:** For a 5×5 grid, what does `grid.neighbors(0, 0)` (top-left corner) return — 2, 3, or 4 cells?

**J. Run:**
```python
g = Grid(5, 5)
print(g.neighbors(0, 0))
```
**K. Expected result:** `[(1, 0), (0, 1)]` — only 2, because the corner has no up or left neighbor.

**M. Common mistake:** using lists `[row, col]` instead of tuples `(row, col)` for positions — lists aren't hashable, so they can't go in a `set` or be a `dict` key. This will crash the moment we build `came_from` dictionaries in Step 2.

**O. Overlay:** "THE GRID IS A GRAPH" · "NEIGHBORS = EDGES"
**P. Focus:** zoom on the `neighbors` method as it runs.
**Q. Audio:** soft click on successful print.
**R. Learning check:** Why can't we use a list `[2, 3]` as a dictionary key?
**S. Next:** now that we can find neighbors, we teach the first search algorithm — BFS.

---

### STEP 2 — BFS (Breadth-First Search)

**A. What:** A function that explores the grid layer by layer, guaranteeing the shortest path on an unweighted grid.
**B. Why:** It's the simplest correct shortest-path algorithm — the foundation everything else builds on.
**C. Concept — the Queue:** A queue is **FIFO** (first in, first out) — like a checkout line. The first cell we discover is the first one we explore. This "layer by layer" order is exactly why BFS finds the *shortest* path first.
**D. DSA connection:** BFS explores in expanding rings around the start. Because it visits closer cells before farther ones, the first time it reaches the end, that path is guaranteed shortest — O(V + E) time.
**E. File:** `algorithms.py`

**G. Code to type:**
```python
from collections import deque

def bfs(grid):
    start = grid.start
    end = grid.end
    frontier = deque([start])
    came_from = {start: None}

    while frontier:
        current = frontier.popleft()
        if current == end:
            break
        for neighbor in grid.neighbors(*current):
            if neighbor not in came_from:
                frontier.append(neighbor)
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)


def reconstruct_path(came_from, start, end):
    if end not in came_from:
        return None
    path = []
    current = end
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path
```

**H. Line-by-line:**
- `deque([start])` — `deque` (double-ended queue) gives O(1) `popleft()`. A plain list's `pop(0)` is O(n) — slow for large grids. This is a classic beginner performance trap.
- `came_from = {start: None}` — a dictionary doing double duty: it tracks "have I visited this?" *and* "which cell led me here?" (for rebuilding the path afterward). `None` for start means "nothing led here, this is the beginning."
- `frontier.popleft()` — take the *oldest* discovered cell. This FIFO order is what makes BFS breadth-first instead of depth-first.
- `if current == end: break` — stop as soon as we reach the goal; no need to keep exploring.
- `grid.neighbors(*current)` — the `*` unpacks the tuple `(row, col)` into two separate arguments, since `neighbors` expects `row, col` not one tuple.
- `if neighbor not in came_from` — this is our "visited" check. Skipping it would cause infinite loops (revisiting cells forever).
- `reconstruct_path` — walks backward from `end` to `start` using the breadcrumbs in `came_from`, then reverses the list so it reads start → end.

**I. Prediction:** If `end` was never reached (blocked off by walls), what will `reconstruct_path` return?

**J. Run:** call `bfs(grid)` on a small grid with no walls.
**K. Expected:** a list of tuples tracing the shortest route.
**L. Verify:** the returned path's length should equal the Manhattan distance between start and end when there are no walls.

**M. Common mistakes:**
- Checking `if current == end` *after* popping instead of when first discovering it — still correct, but wastes one extra loop iteration. Fine for learning, worth knowing for optimization later.
- Forgetting the "visited" check → infinite loop, program hangs.

**N. Debugging:** if `bfs` never terminates, print `len(frontier)` inside the loop — if it keeps growing without bound, you're re-adding visited cells.

**O. Overlay:** "🚨 BUG ALERT" → "CAN YOU SPOT IT?" (pause 3s on a version missing the `came_from` check) → "MISSING VISITED CHECK"
**P. Focus:** zoom on `if neighbor not in came_from`.
**Q. Audio:** low synth drop on bug reveal, soft chime on fix confirmed.
**R. Learning check:** Why does popping from the *front* (not the back) guarantee shortest path?

**🏁 MILESTONE 1 — "PATHMIND CAN NOW FIND THE SHORTEST PATH"**

**S. Next:** wire this into `main.py` and *see* it, via the visualizer.

---

### STEP 3 — The Visualizer

**A. What:** A `render()` function that prints the grid with walls, start, end, and (optionally) the path.
**B. Why:** Right now the algorithm returns a list of tuples — meaningless to look at. We need to *see* the maze.
**E. File:** `visualizer.py`

**G. Code to type:**
```python
def render(grid, path=None):
    path = path or []
    for row in range(grid.rows):
        line = ""
        for col in range(grid.cols):
            cell = (row, col)
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
```

**H. Line-by-line:**
- `path = path or []` — if no path was passed in (`None`), default to an empty list, so `cell in path` never crashes.
- Nested `for row` / `for col` loops — walks the grid top-to-bottom, left-to-right, building one printable string per row.
- The `if/elif` chain — priority order matters: we check `start`/`end` before `wall` before `path`, so a path is never drawn *over* the start or end marker.
- `cell in path` — this is O(n) on a list; fine for small demo grids, worth noting as a spot to optimize later (turn `path` into a `set` if grids get large).

**J. Run:**
```python
render(grid, bfs(grid))
```
**K. Expected:** an ASCII grid — `S` at start, `E` at end, `#` for walls, `*` tracing the path.

**M. Common mistake:** checking `is_wall` *before* `start`/`end` — if you ever place a wall on the start cell by accident, you'd silently draw `#` instead of `S` and hide the bug. Order of checks matters.

**🏁 MILESTONE 2 — "WE CAN SEE THE PATH"**

**S. Next:** contrast BFS with DFS — same grid, very different behavior.

---

### STEP 4 — DFS (Depth-First Search)

**A. What:** Same shape as BFS, but explores as *deep* as possible before backing up.
**C. Concept — the Stack:** A stack is **LIFO** (last in, first out) — like a stack of plates; you take from the top. Swap BFS's queue for a stack and you get depth-first behavior for free.
**D. DSA connection:** DFS does **not** guarantee shortest path — it just dives down one direction until it hits a dead end, then backtracks. Great for "does a path exist at all," bad for "shortest path."

**G. Code to type:**
```python
def dfs(grid):
    start = grid.start
    end = grid.end
    frontier = [start]
    came_from = {start: None}

    while frontier:
        current = frontier.pop()
        if current == end:
            break
        for neighbor in grid.neighbors(*current):
            if neighbor not in came_from:
                frontier.append(neighbor)
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)
```

**H. Line-by-line:** Only one meaningful change from `bfs`: `frontier = [start]` (a plain list) and `frontier.pop()` (removes from the **end**, not the front). That single change — front-removal vs end-removal — is the entire difference between breadth-first and depth-first. Everything else is identical.

**I. Prediction:** On the same grid, will BFS and DFS return the *same* path?

**J/K.** Run both back-to-back and print both paths — they'll usually differ, and DFS's will often be longer.

**O. Overlay:** "SAME CODE. ONE LINE CHANGED." → "QUEUE → STACK"
**R. Learning check:** Why might DFS return a *longer* path than BFS on the same grid?

**🏁 MILESTONE 3 — "TWO ALGORITHMS, ONE SHARED SKELETON"**

**S. Next:** clean up before adding weighted pathfinding.

---

### STEP 5 — Refactor Pass

**"THE APP WORKS."** → **"LET'S CLEAN IT UP."**

At this point `bfs` and `dfs` share almost everything except the frontier type and pop direction. We leave them separate here (merging them into one generic "graph search" function is a great *future* exercise once you've covered more DSA — flagging it, not doing it yet, so the algorithms stay easy to read individually).

What we do clean up:
- Confirm every function has a clear, single job (grid = data, algorithms = logic, visualizer = display).
- Add short docstrings to `bfs`, `dfs`, and `reconstruct_path`.
- Add type hints where they help readability: `def bfs(grid: Grid) -> list[tuple[int, int]] | None:`

**Why this matters professionally:** readable code is a feature. Interviewers and teammates read your code far more often than they run it.

---

### STEP 6 — Dijkstra (Weighted Shortest Path)

**A. What:** Shortest path when not all cells cost the same to cross (e.g. "mud" cells cost more than open ground).
**B. Why:** Real maps aren't uniform — a highway and a dirt road aren't equally "costly." BFS can't handle this; Dijkstra can.
**C. Concept — the Priority Queue / Heap:** Instead of "first discovered, first explored" (queue) we now need "**cheapest so far**, first explored." A **min-heap** keeps the smallest item accessible in O(log n) time — much faster than sorting a list every time. Python's `heapq` module gives us this for free.
**D. DSA connection:** Dijkstra is BFS's weighted cousin — same frontier/visited pattern, but the frontier is now a priority queue ordered by *cost*, not discovery order.
**E. File:** `algorithms.py`

**G. Code to type:**
```python
import heapq

def dijkstra(grid, weight_fn=None):
    start = grid.start
    end = grid.end
    weight_fn = weight_fn or (lambda cell: 1)

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        if current == end:
            break
        for neighbor in grid.neighbors(*current):
            new_cost = current_cost + weight_fn(neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)
```

**H. Line-by-line:**
- `weight_fn = weight_fn or (lambda cell: 1)` — a default: every cell costs 1 unless the caller supplies a custom cost function (e.g. "mud costs 5"). A **lambda** is just a tiny unnamed function — `lambda cell: 1` means "given a cell, return 1."
- `frontier = [(0, start)]` — a list used as a heap; `heapq` keeps tuples ordered by their **first** element, so `(cost, cell)` naturally sorts by cost.
- `heapq.heappop(frontier)` — always returns the *lowest-cost* entry — O(log n).
- `cost_so_far` — tracks the cheapest known cost to reach each cell so far. This replaces the simple "visited" check from BFS/DFS, because with weights, a cell might be reached more cheaply later via a different route.
- `if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]` — the key difference from BFS: we don't just check "have I seen this?" — we check "have I seen a *cheaper* way to it?" This is what makes Dijkstra correct with weights.

**M. Common mistake:** reusing BFS's simple `if neighbor not in came_from` visited check here — it silently breaks Dijkstra, because a cell might legitimately need to be reprocessed if a cheaper path to it is found later.

**N. Debugging:** if paths look wrong with weighted cells, print `cost_so_far` after the run — a cell with a suspiciously high cost usually means the cheaper route was skipped.

**O. Overlay:** "NOT ALL CELLS ARE EQUAL" → "PRIORITY QUEUE = CHEAPEST FIRST"
**R. Learning check:** Why isn't a plain "visited" set enough once cells have different costs?

**🏁 MILESTONE 4 — "PATHMIND HANDLES WEIGHTED TERRAIN"**

**S. Next:** make it *smart* — add a heuristic and get A*.

---

### STEP 7 — A* (Heuristic Search)

**A. What:** Dijkstra, plus an educated guess about which direction the goal is in.
**B. Why:** Dijkstra explores equally in all directions — wasteful when we already know roughly where the goal is. A* uses that hint to search far fewer cells.
**C. Concept — the Heuristic:** A heuristic is an *estimate*, not the exact answer — like "as the crow flies" distance. For grids, we use **Manhattan distance**: `|row1 - row2| + |col1 - col2|` — the number of grid steps ignoring walls.
**D. DSA connection:** A* ranks the frontier by `cost_so_far + heuristic` instead of just `cost_so_far`. This biases the search toward the goal without sacrificing correctness (as long as the heuristic never *overestimates* the true distance — Manhattan distance never does, on a grid with no diagonal movement).
**E. File:** `algorithms.py`

**G. Code to type:**
```python
def heuristic(a, b):
    (r1, c1), (r2, c2) = a, b
    return abs(r1 - r2) + abs(c1 - c2)


def a_star(grid, weight_fn=None):
    start = grid.start
    end = grid.end
    weight_fn = weight_fn or (lambda cell: 1)

    frontier = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == end:
            break
        for neighbor in grid.neighbors(*current):
            new_cost = cost_so_far[current] + weight_fn(neighbor)
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, end)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current

    return reconstruct_path(came_from, start, end)
```

**H. Line-by-line:**
- `heuristic(a, b)` — tuple unpacking `(r1, c1), (r2, c2) = a, b` pulls both coordinates out in one line. Returns the Manhattan distance.
- `_, current = heapq.heappop(frontier)` — the underscore `_` is Python convention for "I'm receiving this value but deliberately ignoring it" — here, we don't need the raw priority number itself, just the cell.
- `priority = new_cost + heuristic(neighbor, end)` — the only real difference from Dijkstra: we push based on *real cost so far* **plus** *estimated remaining cost*, not real cost alone. This is what steers the search toward the goal.
- `cost_so_far` still tracks *actual* cost (for correctness); `priority` is only used for ordering the heap.

**I. Prediction:** On an open grid with no walls, will A* explore more or fewer cells than Dijkstra to find the same path?

**M. Common mistake:** pushing `heuristic(neighbor, end)` alone (without adding it to `new_cost`) — this turns A* into "Greedy Best-First Search," which is faster but no longer guarantees the shortest path. Worth knowing the difference exists.

**O. Overlay:** "DIJKSTRA + A GUESS = A*" → "SAME SHORTEST PATH. LESS WORK."
**R. Learning check:** Why does Manhattan distance work as a heuristic here, but wouldn't if diagonal movement were allowed?

**🏁 MILESTONE 5 — "ALL FOUR ALGORITHMS ARE LIVE"**

---

### STEP 8 — Wiring It Together (`main.py`)

```python
from grid import Grid
from algorithms import bfs, dfs, dijkstra, a_star
from visualizer import render


def build_demo_grid():
    grid = Grid(5, 5)
    grid.set_start(0, 0)
    grid.set_end(4, 4)
    for wall in [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]:
        grid.add_wall(*wall)
    return grid


def main():
    grid = build_demo_grid()
    print("Grid:")
    render(grid)

    for name, algorithm in [("BFS", bfs), ("DFS", dfs), ("Dijkstra", dijkstra), ("A*", a_star)]:
        path = algorithm(grid)
        print(f"\n{name} path ({len(path) if path else 0} steps):")
        render(grid, path)


if __name__ == "__main__":
    main()
```

**H. Line-by-line:**
- `build_demo_grid()` — separates *building test data* from *running the program*, so swapping in a different maze later is a one-function change.
- `for name, algorithm in [...]` — a list of `(label, function)` pairs. This is **functions as values** — in Python, a function name with no parentheses is just a reference you can store and pass around, same as any other variable.
- `f"\n{name} path ({len(path) if path else 0} steps):"` — an f-string with an inline conditional (a **ternary expression**): "use `len(path)` if a path exists, otherwise `0`" — guards against crashing when `path` is `None`.

**J/K. Run:** `python main.py` — expect the grid printed once, then four labeled runs showing each algorithm's path and step count.

---

## PART 7 — FINAL TESTING

Before the reveal, test:
- **Normal case:** open grid, clear path exists.
- **No path exists:** walls fully seal off the end → all four functions should return `None` gracefully, not crash.
- **Start equals end:** should return a single-cell path immediately.
- **Edge cells:** start/end in corners — confirms `in_bounds` works correctly.

Fix anything that crashes instead of returning `None` or an empty result — a pathfinder should never throw an unhandled exception just because a path doesn't exist.

---

## PART 8 — FINAL REVEAL

Overlays: **"CREATE"** → **"EXPLORE"** → **"FIND"** → **"BUILT FROM SCRATCH"**
Show all four algorithms running back-to-back on the same maze, side by side if possible.

---

## PART 9 — DSA COMPLEXITY BREAKDOWN

| Operation | Algorithm | Time Complexity | Why |
|---|---|---|---|
| Find any path | DFS | O(V + E) | Visits each node/edge once, no shortest-path guarantee |
| Shortest path (unweighted) | BFS | O(V + E) | Layer-by-layer guarantees shortest first |
| Shortest path (weighted) | Dijkstra | O((V + E) log V) | Heap push/pop is O(log V), done up to E times |
| Shortest path (weighted + guided) | A* | O((V + E) log V) worst case, typically much faster in practice | Heuristic prunes exploration toward the goal |

*V = number of cells, E = number of edges (neighbor connections).*

---

## PART 10 — FUTURE UPGRADES

- **V2:** Diagonal movement + a proper heuristic adjustment (Euclidean/Chebyshev distance)
- **V3:** Pygame GUI — click to place walls/start/end, animate the search live
- **V4:** ML-predicted heuristics — train a model to *guess* good heuristics instead of hand-coding Manhattan distance
- **V5:** Real map data (OpenStreetMap) — swap the grid for real road networks
- **V6:** Web deployment (Flask/FastAPI) — run PathMind in the browser
- **V7:** LLM agent that narrates *why* it chose each step ("I skipped this cell because it looked farther from the goal")

---

## PART 11 — VIDEO TIMELINE

```
00:00 — Hook (finished project)
00:06 — What we're building
00:20 — Starter project tour
00:45 — Step 1: The Grid
02:30 — Step 2: BFS
05:00 — Milestone 1
05:10 — Step 3: Visualizer
06:30 — Milestone 2
06:40 — Step 4: DFS
08:30 — Milestone 3
08:40 — Step 5: Refactor
09:30 — Step 6: Dijkstra
12:30 — Milestone 4
12:40 — Step 7: A*
15:30 — Milestone 5
15:40 — Step 8: Wiring main.py
17:00 — Final testing
18:00 — Final reveal
19:00 — DSA complexity breakdown
20:00 — Future upgrades
```

---

## PART 12 — SHORT-FORM SCRIPT

1. Show finished maze with path animating (2s)
2. Overlay: **"4 ALGORITHMS. 1 MAZE."**
3. Quick-cut: BFS path → DFS path (longer, wandering) → A* path (fast, direct)
4. Overlay: **"CAN YOU GUESS WHICH IS FASTEST?"**
5. Overlay: **"FULL BUILD →"** with arrow to long-form video.
Pinned comment: full tutorial link + GitHub repo link.

---

## PART 13 — PRODUCTION CHECKLIST

- [ ] Every concept explained before its code (Graphs, Queue, Stack, Heap, Heuristic)
- [ ] All 4 algorithms typed manually, one step at a time
- [ ] Bugs used as teaching moments (missing visited-check, stale cost check)
- [ ] Edge cases tested (no path, start=end)
- [ ] `starter-code` and `main` branches match Parts 4 and this document
- [ ] Overlays ≤ 6 words per line, 1.5× reading time on screen
- [ ] Milestones visible after each algorithm
- [ ] DSA breakdown table shown at the end
