# Copyright 2024 DeepMind Technologies Limited.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Functions to evaluate expressions in simulation streams."""

import builtins
import math
import random
import statistics

import numpy as np
from simpleeval import EvalWithCompoundTypes


def evaluator():
  """A function to create a safe evaluator for simple single expression."""
  s = EvalWithCompoundTypes()

  # Math functions
  math_functions = [
      'ceil',
      'floor',
      'sqrt',
      'exp',
      'log',
      'log10',
      'sin',
      'cos',
      'tan',
      'asin',
      'acos',
      'atan',
      'degrees',
      'radians',
      'pi',
      'e',
  ]
  for func in math_functions:
    s.functions[func] = getattr(math, func)

  # Built-in functions
  builtin_functions = [
      'abs',
      'round',
      'min',
      'max',
      'sum',
      'len',
      'sorted',
      'enumerate',
      'zip',
      'any',
      'all',
      'filter',
      'map',
      'str',
      'int',
      'float',
      'bool',
  ]
  for func in builtin_functions:
    s.functions[func] = getattr(builtins, func)

  # String methods as functions
  string_methods = [
      'lower',
      'upper',
      'title',
      'capitalize',
      'strip',
      'lstrip',
      'rstrip',
      'replace',
      'split',
      'join',
      'startswith',
      'endswith',
      'find',
      'count',
  ]
  for method in string_methods:
    s.functions[method] = lambda *args, method=method: getattr(
        str(args[0]), method
    )(*args[1:])

  # Random functions
  s.functions['random'] = random.random
  s.functions['randint'] = random.randint
  s.functions['tile_map'] = get_tile_map
  s.functions['object_map'] = get_object_map
  s.functions['get_maze_obstacles'] = get_maze_obstacles
  s.functions['get_maze_start_x'] = get_maze_start_x
  s.functions['get_maze_start_y'] = get_maze_start_y
  s.functions['get_maze_goal_position'] = get_maze_goal_position
  s.functions['get_maze_goal_position_x'] = get_maze_goal_position_x
  s.functions['get_maze_goal_position_y'] = get_maze_goal_position_y

  # Statistics functions
  statistics_functions = ['mean', 'median', 'mode', 'stdev', 'variance']
  for func in statistics_functions:
    s.functions[func] = getattr(statistics, func)

  return s


def get_tile_map(the_grid_size: int = 5):
  """Initialize and return the tile map."""
  tile_map = {}
  for x in range(-1, the_grid_size + 1):
    for y in range(-1, the_grid_size + 1):
      if x == -1 or x == the_grid_size or y == -1 or y == the_grid_size:
        tile_map[(x, y)] = 'wall'
      else:
        tile_map[(x, y)] = 'road' if random.random() > 0.2 else 'wall'
  return tile_map


def get_object_map(the_grid_size: int = 5, index: int = 0):
  """Initialize object map, place key and chest, and return the result."""
  object_map = {}
  for x in range(the_grid_size):
    for y in range(the_grid_size):
      object_map[(x, y)] = 'empty'

  keys_x = [4, 1, 4, 0, 4, 3, 3, 1, 3, 2]
  keys_y = [1, 3, 3, 4, 1, 0, 3, 3, 1, 4]
  chest_x, chest_y = 2, 3

  key_x, key_y = keys_x[index], keys_y[index]
  object_map[(key_x, key_y)] = 'key'
  object_map[(chest_x, chest_y)] = 'chest'

  return object_map


def generate_maze(width: int, height: int):
  """Generates a maze.

  Args:
    width:
    height:

  Returns:

  """
  # Initialize the maze grid, 0 = empty, 1 = wall
  the_maze = np.ones((height, width), dtype=np.int8)

  # Start position (always in the upper left corner)
  the_start = (1, 1)
  the_maze[the_start] = 0

  # Ensure the adjacent squares are set as desired
  the_maze[1, 2] = 0  # Right of the start
  the_maze[2, 1] = 0  # Below the start
  the_maze[2, 2] = 0  # Diagonally below-right of the start, ensure it's a wall

  # Stack to hold the cells to visit, starting from the adjusted initial cells
  stack = [the_start, (1, 2), (2, 1), (2, 2)]

  # Directions to move: up, right, down, left
  directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

  while stack:
    x, y = stack[-1]

    # Find unvisited neighbors
    neighbors = []
    for dx, dy in directions:
      nx, ny = x + dx * 2, y + dy * 2
      if 1 <= nx < width - 1 and 1 <= ny < height - 1 and the_maze[ny][nx] == 1:
        neighbors.append((nx, ny))

    if neighbors:
      # Choose a random neighboring cell
      nx, ny = random.choice(neighbors)

      # Remove wall between current cell and chosen cell
      the_maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0

      # Mark chosen cell as free and add to stack
      the_maze[ny][nx] = 0
      stack.append((nx, ny))
    else:
      # Backtrack
      stack.pop()
  # pylint: disable=g-complex-comprehension
  goal_candidates = [
      (x, y)
      for x in range(width)
      for y in range(height)
      if the_maze[y][x] == 0 and (x, y) != the_start
  ]

  the_goal = max(
      goal_candidates,
      key=lambda p: abs(p[0] - the_start[0]) + abs(p[1] - the_start[1]),
  )

  return the_maze, the_start, the_goal


def generate_moderately_open_maze(
    width: int, height: int, open_factor: float = 0.1
):
  """Generates a moderately open maze.

  Args:
    width:
    height:
    open_factor:

  Returns:

  """

  # Generate a maze with DFS and then open additional cells
  the_maze, the_start, the_goal = generate_maze(width, height)

  # Number of additional cells to open
  total_cells = width * height
  open_cells = int(total_cells * open_factor)

  # Randomly open cells that are not the start or the goal
  while open_cells > 0:
    x, y = random.randint(1, width - 2), random.randint(1, height - 2)
    if the_maze[y][x] == 1 and (x, y) != the_start and (x, y) != the_goal:
      the_maze[y][x] = 0
      open_cells -= 1

  return the_maze, the_start, the_goal


def maze_to_obstacles(m: np.ndarray):
  """Creates a list of obstacles from a maze.

  Args:
    m: The maze

  Returns:
    the_obstacles: All walls including edges

  """
  height, width = m.shape

  # Initialize the obstacles list with the boundaries of the maze
  the_obstacles = (
      [(x, 0) for x in range(width)]
      + [(x, height - 1) for x in range(width)]
      + [(0, y) for y in range(height)]
      + [(width - 1, y) for y in range(height)]
  )

  # Remove duplicates that might occur at the corners
  the_obstacles = list(set(the_obstacles))

  # Add inner walls to the obstacles list
  # pylint: disable=g-complex-comprehension
  inner_obstacles = [
      (x, y)
      for x in range(1, width - 1)
      for y in range(1, height - 1)
      if m[y][x] == 1
  ]

  the_obstacles.extend(inner_obstacles)

  return the_obstacles

# Global variables
grid_size = 7
random.seed(42)
predefined_mazes = []

# Generate predefined mazes
for j in range(10):
  _maze, _start, _goal = generate_moderately_open_maze(grid_size, grid_size)
  obstacles = maze_to_obstacles(_maze)
  predefined_mazes.append((_maze, _start, _goal, obstacles))


def get_maze_obstacles(index: int):
  """Get the obstacles for a specific maze."""
  _, _, _, the_obstacles = predefined_mazes[index]
  return the_obstacles


def get_maze_start_position(index: int):
  """Get the start position for a specific maze."""
  _, start, _, _ = predefined_mazes[index]
  return start


def get_maze_goal_position(index: int) -> tuple[int, int]:
  """Get the goal position for a specific maze."""
  _, _, goal, _ = predefined_mazes[index]
  return goal


def get_maze_start_x(index: int):
  """Get the x-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[0]


def get_maze_start_y(index: int):
  """Get the y-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[1]


def get_maze_goal_position_x(index: int) -> int:
  """Get the x-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[0]


def get_maze_goal_position_y(index: int) -> int:
  """Get the y-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[1]
