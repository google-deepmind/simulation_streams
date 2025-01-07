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

"""Explicit alternative to evaluate expressions in simulation streams."""

import ast
import builtins
import math
import operator
import random
import statistics

import numpy as np


def evaluator():
  """A function to create a safe evaluator for simple single expression."""
  e = Evaluator()

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
    e.functions[func] = getattr(math, func)

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
      'dict',  # Added 'dict' to support dict() function
  ]
  for func in builtin_functions:
    e.functions[func] = getattr(builtins, func)

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
    e.functions[method] = lambda *args, method=method: getattr(
        str(args[0]), method
    )(*args[1:])

  # Random functions
  e.functions['random'] = random.random
  e.functions['randint'] = random.randint
  e.functions['tile_map'] = get_tile_map
  e.functions['object_map'] = get_object_map
  e.functions['get_maze_obstacles'] = get_maze_obstacles
  e.functions['get_maze_start_x'] = get_maze_start_x
  e.functions['get_maze_start_y'] = get_maze_start_y
  e.functions['get_maze_goal_position'] = get_maze_goal_position
  e.functions['get_maze_goal_position_x'] = get_maze_goal_position_x
  e.functions['get_maze_goal_position_y'] = get_maze_goal_position_y

  # Statistics functions
  statistics_functions = ['mean', 'median', 'mode', 'stdev', 'variance']
  for func in statistics_functions:
    e.functions[func] = getattr(statistics, func)

  return e


def get_tile_map(the_grid_size: int = 5) -> dict[tuple[int, int], str]:
  """Initialize and return the tile map."""
  tile_map = {}
  for x in range(-1, the_grid_size + 1):
    for y in range(-1, the_grid_size + 1):
      if x == -1 or x == the_grid_size or y == -1 or y == the_grid_size:
        tile_map[(x, y)] = 'wall'
      else:
        tile_map[(x, y)] = 'road' if random.random() > 0.2 else 'wall'
  return tile_map


def get_object_map(
    the_grid_size: int = 5, index: int = 0
) -> dict[tuple[int, int], str]:
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


def generate_maze(
    width: int, height: int
) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
  """Generates a maze.

  Args:
    width: The width of the maze.
    height: The height of the maze.

  Returns:
    A tuple containing the maze, the start position, and the goal position.
  """
  # Initialize the maze grid, 0 = empty, 1 = wall
  the_maze = np.ones((height, width), dtype=np.int8)

  # Start position (always in the upper left corner)
  the_start = (1, 1)
  the_maze[the_start] = 0

  # Ensure the adjacent squares are set as desired
  the_maze[1, 2] = 0  # Right of the start
  the_maze[2, 1] = 0  # Below the start
  the_maze[2, 2] = 0  # Diagonally below-right of the start

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

  # Find the goal position (furthest from the start)
  goal_candidates = []
  for x in range(width):
    for y in range(height):
      if the_maze[y][x] == 0 and (x, y) != the_start:
        goal_candidates.append((x, y))

  the_goal = max(
      goal_candidates,
      key=lambda p: abs(p[0] - the_start[0]) + abs(p[1] - the_start[1]),
  )

  return the_maze, the_start, the_goal


def generate_moderately_open_maze(
    width: int, height: int, open_factor: float = 0.1
) -> tuple[np.ndarray, tuple[int, int], tuple[int, int]]:
  """Generates a moderately open maze.

  Args:
    width: The width of the maze.
    height: The height of the maze.
    open_factor: The fraction of cells to open additionally.

  Returns:
    A tuple containing the maze, the start position, and the goal position.
  """
  # Generate a maze
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


def maze_to_obstacles(m: np.ndarray) -> list[tuple[int, int]]:
  """Creates a list of obstacles from a maze.

  Args:
    m: The maze.

  Returns:
    The obstacles including all walls and edges.
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
  inner_obstacles = []
  for x in range(1, width - 1):
    for y in range(1, height - 1):
      if m[y][x] == 1:
        inner_obstacles.append((x, y))

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


def get_maze_obstacles(index: int) -> list[tuple[int, int]]:
  """Get the obstacles for a specific maze."""
  _, _, _, the_obstacles = predefined_mazes[index]
  return the_obstacles


def get_maze_start_position(index: int) -> tuple[int, int]:
  """Get the start position for a specific maze."""
  _, start, _, _ = predefined_mazes[index]
  return start


def get_maze_goal_position(index: int) -> tuple[int, int]:
  """Get the goal position for a specific maze."""
  _, _, goal, _ = predefined_mazes[index]
  return goal


def get_maze_start_x(index: int) -> int:
  """Get the x-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[0]


def get_maze_start_y(index: int) -> int:
  """Get the y-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[1]


def get_maze_goal_position_x(index: int) -> int:
  """Get the x-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[0]


def get_maze_goal_position_y(index: int) -> int:
  """Get the y-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[1]


class Evaluator(ast.NodeVisitor):
  """A safe evaluator for simple expressions."""

  def __init__(self, functions=None, names=None):
    self.functions = functions or {}
    self.names = names or {}
    self.operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.LShift: operator.lshift,
        ast.RShift: operator.rshift,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.BitAnd: operator.and_,
    }
    self.unary_operators = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
        ast.Invert: operator.invert,
        ast.Not: operator.not_,  # Added 'ast.Not' to support 'not' operator
    }
    self.compare_operators = {
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
        ast.In: lambda x, y: x in y,
        ast.NotIn: lambda x, y: x not in y,
    }

  def eval(self, expr):
    self.expr = expr
    self.node = ast.parse(expr, mode='eval')
    return self.visit(self.node.body)

  def visit_BinOp(self, node):  # pylint: disable=invalid-name
    left = self.visit(node.left)
    right = self.visit(node.right)
    op_type = type(node.op)
    if op_type in self.operators:
      return self.operators[op_type](left, right)
    else:
      raise ValueError(f'Unsupported operator: {op_type}')

  def visit_UnaryOp(self, node):  # pylint: disable=invalid-name
    operand = self.visit(node.operand)
    op_type = type(node.op)
    if op_type in self.unary_operators:
      return self.unary_operators[op_type](operand)
    else:
      raise ValueError(f'Unsupported unary operator: {op_type}')

  def visit_Compare(self, node):  # pylint: disable=invalid-name
    left = self.visit(node.left)
    for op, comparator in zip(node.ops, node.comparators):
      right = self.visit(comparator)
      op_type = type(op)
      if op_type in self.compare_operators:
        if not self.compare_operators[op_type](left, right):
          return False
        left = right  # For chained comparisons
      else:
        raise ValueError(f'Unsupported comparison operator: {op_type}')
    return True

  def visit_Call(self, node):  # pylint: disable=invalid-name
    func = self.visit(node.func)
    if callable(func):
      args = [self.visit(arg) for arg in node.args]
      keywords = {kw.arg: self.visit(kw.value) for kw in node.keywords}
      return func(*args, **keywords)  # pylint: disable=exec-used
    else:
      raise ValueError(f'Attempt to call non-function {func}')

  def visit_Name(self, node):  # pylint: disable=invalid-name
    if isinstance(node.ctx, ast.Load):
      if node.id in self.names:
        return self.names[node.id]
      elif node.id in self.functions:
        return self.functions[node.id]
      else:
        raise NameError(f"Name '{node.id}' is not defined")
    else:
      raise ValueError(f'Unsupported context {node.ctx}')

  def visit_Constant(self, node):
    return node.value

  def visit_Num(self, node):  # pylint: disable=invalid-name
    return node.n

  def visit_Str(self, node):  # pylint: disable=invalid-name
    return node.s

  def visit_List(self, node):  # pylint: disable=invalid-name
    return [self.visit(elem) for elem in node.elts]

  def visit_Tuple(self, node):  # pylint: disable=invalid-name
    return tuple(self.visit(elem) for elem in node.elts)

  def visit_Dict(self, node):  # pylint: disable=invalid-name
    return {
        self.visit(k): self.visit(v) for k, v in zip(node.keys, node.values)
    }

  def visit_Subscript(self, node):  # pylint: disable=invalid-name
    value = self.visit(node.value)
    slice_ = self.visit(node.slice)
    return value[slice_]

  def visit_Index(self, node):  # pylint: disable=invalid-name
    return self.visit(node.value)

  def visit_Slice(self, node):  # pylint: disable=invalid-name
    lower = self.visit(node.lower) if node.lower else None
    upper = self.visit(node.upper) if node.upper else None
    step = self.visit(node.step) if node.step else None
    return slice(lower, upper, step)

  def visit_IfExp(self, node):  # pylint: disable=invalid-name
    condition = self.visit(node.test)
    if condition:
      return self.visit(node.body)
    else:
      return self.visit(node.orelse)

  def visit_BoolOp(self, node):  # pylint: disable=invalid-name
    """Visit a boolean operator."""
    if isinstance(node.op, ast.And):
      for value in node.values:
        result = self.visit(value)
        if not result:
          return False
      return True
    elif isinstance(node.op, ast.Or):
      for value in node.values:
        result = self.visit(value)
        if result:
          return True
      return False
    else:
      raise ValueError(f'Unsupported boolean operator {node.op}')

  def visit_Attribute(self, node):  # pylint: disable=invalid-name
    value = self.visit(node.value)
    attr = node.attr
    if hasattr(value, attr):
      return getattr(value, attr)
    else:
      raise AttributeError(
          f"'{type(value).__name__}' object has no attribute '{attr}'"
      )

  def visit_ListComp(self, node):  # pylint: disable=invalid-name
    # Evaluate a list comprehension
    return self._evaluate_comprehension(node, {})

  def _evaluate_comprehension(self, node, local_vars):
    # Save the original names to restore after evaluation
    original_names = self.names.copy()
    self.names.update(local_vars)
    try:
      return self._eval_comprehension(node)
    finally:
      # Restore the original names
      self.names = original_names

  def _eval_comprehension(self, node):
    """Evaluate a comprehension."""
    if len(node.generators) != 1:
      raise ValueError('Only single generator comprehensions are supported')
    generator = node.generators[0]
    iter_values = self.visit(generator.iter)
    result = []
    for item in iter_values:
      # Assign the target variable(s)
      self._assign_target(generator.target, item)
      # Evaluate ifs
      if all(self.visit(iff) for iff in generator.ifs):
        result.append(self.visit(node.elt))
    return result

  def _assign_target(self, target, value):
    if isinstance(target, ast.Name):
      self.names[target.id] = value
    elif isinstance(target, ast.Tuple):
      if not isinstance(value, (list, tuple)):
        raise ValueError('Expected a list or tuple to unpack')
      if len(target.elts) != len(value):
        raise ValueError('Mismatched number of elements for unpacking')
      for t_elem, v_elem in zip(target.elts, value):
        self._assign_target(t_elem, v_elem)
    else:
      raise ValueError(f'Unsupported comprehension target: {type(target)}')

  def generic_visit(self, node):
    raise ValueError(f'Unsupported syntax {type(node).__name__}')
