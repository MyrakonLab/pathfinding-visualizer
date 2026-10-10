# PathMind

A terminal-based pathfinding visualizer built from scratch — no external
libraries. Implements BFS, DFS, Dijkstra, and A* over a simple grid.

## Files

- `grid.py` — the maze, represented as a graph (cells = nodes, open
  neighbors = edges)
- `algorithms.py` — `bfs`, `dfs`, `dijkstra`, `a_star`, and a shared
  `reconstruct_path` helper
- `visualizer.py` — prints the grid and a found path to the terminal
- `main.py` — builds a demo grid and runs all four algorithms on it

## Run it

```
python main.py
```

## What each algorithm guarantees

| Algorithm | Shortest path? | Time complexity |
|---|---|---|
| DFS | No | O(V + E) |
| BFS | Yes (unweighted) | O(V + E) |
| Dijkstra | Yes (weighted) | O((V + E) log V) |
| A* | Yes (weighted, with a valid heuristic) | O((V + E) log V), typically faster in practice |

## Planned upgrades

- Diagonal movement
- Pygame GUI
- ML-predicted heuristics
- Real map data (OpenStreetMap)
- Web deployment
- LLM agent that explains its routing decisions
