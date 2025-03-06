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

"""Task functions for the Maze environment."""

import random
import numpy as np


def _generate_maze(width: int, height: int):
  """Generates a maze using a depth-first search approach."""
  # Initialize the maze grid: 0 = free, 1 = wall.
  maze = np.ones((height, width), dtype=np.int8)
  the_start = (1, 1)
  maze[the_start] = 0
  # Set adjacent squares as desired.
  maze[1, 2] = 0  # Right of start.
  maze[2, 1] = 0  # Below start.
  maze[2, 2] = 0  # Diagonally below-right.
  # Stack for cells to visit.
  stack = [the_start, (1, 2), (2, 1), (2, 2)]
  directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
  while stack:
    x, y = stack[-1]
    neighbors = []
    for dx, dy in directions:
      nx, ny = x + dx * 2, y + dy * 2
      if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
        neighbors.append((nx, ny))
    if neighbors:
      nx, ny = random.choice(neighbors)
      maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0  # Remove wall.
      maze[ny][nx] = 0  # Mark cell as free.
      stack.append((nx, ny))
    else:
      stack.pop()
  goal_candidates = [
      (x, y)  # pylint: disable=g-complex-comprehension
      for x in range(width)
      for y in range(height)
      if maze[y][x] == 0 and (x, y) != the_start
  ]
  the_goal = max(
      goal_candidates,
      key=lambda p: abs(p[0] - the_start[0]) + abs(p[1] - the_start[1]),
  )
  return maze, the_start, the_goal


def generate_moderately_open_maze(
    width: int, height: int, open_factor: float = 0.1
):
  """Generates a moderately open maze by opening extra cells."""
  maze, the_start, the_goal = _generate_maze(width, height)
  total_cells = width * height
  open_cells = int(total_cells * open_factor)
  minimal_open = open_cells
  while open_cells > 0:
    x, y = random.randint(1, width - 2), random.randint(1, height - 2)
    if maze[y][x] == 1 and (x, y) != the_start and (x, y) != the_goal:
      maze[y][x] = 0
      open_cells -= 1
  return maze, the_start, the_goal, minimal_open, total_cells


def _maze_to_obstacles(m: np.ndarray):
  """Creates a list of obstacles (walls) from a maze grid."""
  height, width = m.shape
  obstacles = (
      [(x, 0) for x in range(width)]
      + [(x, height - 1) for x in range(width)]
      + [(0, y) for y in range(height)]
      + [(width - 1, y) for y in range(height)]
  )
  obstacles = list(set(obstacles))
  inner_obstacles = [
      (x, y)  # pylint: disable=g-complex-comprehension
      for x in range(1, width - 1)
      for y in range(1, height - 1)
      if m[y][x] == 1
  ]
  obstacles.extend(inner_obstacles)
  return obstacles


# Pre-generate a set of mazes.
_grid_size = 7
random.seed(42)
_predefined_mazes = []
for j in range(10):
  a_maze, start, goal, _, _ = generate_moderately_open_maze(
      _grid_size, _grid_size
  )
  the_obstacles = _maze_to_obstacles(a_maze)
  _predefined_mazes.append((a_maze, start, goal, the_obstacles))


def get_maze_obstacles(index: int):
  """Get the obstacles for a specific maze."""
  _, _, _, obstacles = _predefined_mazes[index]
  return obstacles


def get_maze_start_position(index: int):
  """Get the start position for a specific maze."""
  _, the_start, _, _ = _predefined_mazes[index]
  return the_start


def get_maze_goal_position(index: int):
  """Get the goal position for a specific maze."""
  _, _, the_goal, _ = _predefined_mazes[index]
  return the_goal


def get_maze_start_x(index: int):
  """Get the x-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[0]


def get_maze_start_y(index: int):
  """Get the y-coordinate of the start position for a specific maze."""
  return get_maze_start_position(index)[1]


def get_maze_goal_position_x(index: int):
  """Get the x-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[0]


def get_maze_goal_position_y(index: int):
  """Get the y-coordinate of the goal position for a specific maze."""
  return get_maze_goal_position(index)[1]


# --- Maze Task Functions ---
def initialize_default_state(state):
  """Initializes the default state for the Maze environment."""
  defaults = {
      'grid_size': _grid_size,
      'world_obstacles': get_maze_obstacles(0),
      'mouse_position_x': get_maze_start_x(0),
      'mouse_position_y': get_maze_start_y(0),
      'mouse_move_x': 0,
      'mouse_move_y': 0,
      'agent_action': (0, 0),
      'agent_score': 0,
      'mouse_cheese_found': False,
      'mouse_cheese_x': get_maze_goal_position_x(0),
      'mouse_cheese_y': get_maze_goal_position_y(0),
      'mouse_smell_of_cheese': 0,
      'agent_planning_instruction': (
          'Consider the mouses past developments and in particular the'
          ' agents knowledge, make a high-level plan for how to achieve the'
          ' objective.'
      ),
      'agent_high_level_plan': (
          'The mouse needs to find a way through the maze to find the cheese,'
          ' avoiding walls and trying new open paths that it has not explored'
          ' in the past. It should use a Depth-First-Search strategy.'
      ),
      'agent_planning_algorithmic_instruction': (
          'Provide an algorithmic outline for the plan above.'
      ),
      'agent_algorithmic_outline': (
          'If from where you are, you have not chosen a path to try, start'
          ' going down an available untried direction and only go back if you'
          ' find a dead end. If you are along a path and can continue, do so.'
          ' If you hit a dead end, return to the last place where you had'
          ' another option than the one you tried and then go down that'
          ' unexplored path. At all times, you should have a preference for'
          ' where the smell of cheese is stronger and aim to go in directions'
          ' of increasing smell.'
      ),
      'agent_planning_execution_instruction': (
          'Consider the high-level plan and its algorithmic outline'
          ' and plan concrete next steps from the current state. Consider the'
          ' previous time steps execution plan and build on it.'
      ),
      'agent_execution_plan': (
          'The mouse is at (1,1) and should explore a path to the right'
          ' starting with (1,2) and observe the surroundings and if possible'
          ' continue to new locations that it has not yet visited, always avoid'
          ' hitting the walls. Let your choice among new empty squares be'
          ' guided by the direction in which the smell of cheese increases the'
          ' most. If you at any point see the cheese, go immediately to its'
          ' square.'
      ),
      'agent_summary_instruction': (
          'Make a comprehensive factual summary of the relevant knowledge'
          ' gained at this point. Ensure accuracy and avoid fabrication of'
          ' events that did not occur. Reflect on the current status and any'
          ' changes.'
      ),
      'agent_knowledge': (
          'The mouse is at (1,1) in a maze gridworld (1....5 x 1...5) and is'
          ' very weakly smelling a cheese that it does not know the location'
          ' of. The cheese has not been located (as the current status shows).'
          ' Summary of where the mouse can go and where there are walls: There'
          ' are walls everywhere around the mouse except right (1,2), down'
          ' (2,1) as well as the right-down diagonal (2,2), that are empty. The'
          ' mouse has not visited any other locations yet.'
      ),
      'agent_control_instruction': (
          'Choose the (x,y)-direction to move in according to the plan.'
      ),
      'revision_question': (
          'Given the recent events and developments, should the high-level plan'
          ' and its algorithmic outline be revised (Yes/No)?'
      ),
  }
  for key, value in defaults.items():
    state.setdefault(key, value)
  return ''


def update_state(state):
  """Updates the state of the Maze environment."""
  # initialize_default_state(state)
  if state.get('mouse_position_x') == state.get('mouse_cheese_x') and state.get(
      'mouse_position_y'
  ) == state.get('mouse_cheese_y'):
    state['mouse_cheese_found'] = True

  dx = state.get('mouse_position_x') - state.get('mouse_cheese_x')
  dy = state.get('mouse_position_y') - state.get('mouse_cheese_y')
  dist = np.sqrt(dx**2 + dy**2)
  if dist != 0:
    state['mouse_smell_of_cheese'] = round(1 / dist, 2)
  else:
    state['mouse_smell_of_cheese'] = 0
  if state['mouse_cheese_found']:
    state['agent_score'] = 1
  else:
    state['agent_score'] = (
        -state.get('mouse_hitting_wall_penalty', 0)
        - state.get('mouse_lazy_mouse_penalty', 0)
    )

  return 'State updated'


def update_history(state):
  """Appends the current state to the history log."""
  new_entry = (
      f"Time: {state['world_time']}, "
      f"Position: ({state['mouse_position_x']}, "
      f"{state['mouse_position_y']}), "
      f"Smell: {state['mouse_smell_of_cheese']}, "
      f"Hitting Wall Penalty: {state.get('mouse_hitting_wall_penalty', 0)}, "
      f"Lazy Mouse Penalty: {state.get('mouse_lazy_mouse_penalty', 0)}, "
      f"Cheese Found: {state['mouse_cheese_found']}, "
      f"Reward: {state.get('agent_score', 0)}\n"
  )
  state['agent_history'] += new_entry
  return state['agent_history']


def update_current_status(state):
  """Returns a summary of the current state, including an Observation of immediate surroundings."""
  # Build observation for four cardinal directions.
  x = state.get('mouse_position_x', 0)
  y = state.get('mouse_position_y', 0)
  obstacles = state.get('world_obstacles', [])
  cheese = (state.get('mouse_cheese_x'), state.get('mouse_cheese_y'))
  directions = {
      'North': (x, y - 1),
      'South': (x, y + 1),
      'East': (x + 1, y),
      'West': (x - 1, y),
  }
  obs_list = []
  for d, (nx, ny) in directions.items():
    if (nx, ny) in obstacles:
      cell = 'Wall'
    elif (nx, ny) == cheese:
      cell = 'Cheese'
    else:
      cell = 'Empty'
    obs_list.append(f'{d} ({nx},{ny}): {cell}')
  observation = '; '.join(obs_list)
  return (
      f"Time: {state['world_time']} | "
      f"Position: ({state['mouse_position_x']}, {state['mouse_position_y']}) | "
      f"Smell: {state['mouse_smell_of_cheese']} | "
      f"Cheese Found: {state['mouse_cheese_found']} | "
      f'Observation: {observation}'
  )


def take_action(state):
  """Reads agent_action (a tuple) and apply it to the mouse."""
  action = state.get('agent_action', (0, 0))
  try:
    dx, dy = action
  except Exception:  # pylint: disable=broad-exception-caught
    dx, dy = 0, 0
  dx = max(-1, min(1, dx))
  dy = max(-1, min(1, dy))
  state['mouse_move_x'] = dx
  state['mouse_move_y'] = dy
  # Compute tentative new position.
  new_x = state.get('mouse_position_x', 0) + dx
  new_y = state.get('mouse_position_y', 0) + dy
  grid = state.get('grid_size', 7)
  # Clip to grid boundaries.
  new_x = max(0, min(grid - 1, new_x))
  new_y = max(0, min(grid - 1, new_y))
  obstacles = state.get('world_obstacles', [])
  print(obstacles)
  print((new_x, new_y))
  # Check for wall collision.
  if (new_x, new_y) in obstacles:
    state['mouse_hitting_wall_penalty'] = 0.1
    # Do not update position.
  else:
    state['mouse_hitting_wall_penalty'] = 0
    state['mouse_position_x'] = new_x
    state['mouse_position_y'] = new_y
  # Lazy penalty if no movement.
  if (dx, dy) == (0, 0):
    state['mouse_lazy_mouse_penalty'] = 0.1
  else:
    state['mouse_lazy_mouse_penalty'] = 0
  return (state['mouse_move_x'], state['mouse_move_y'])


# --- Exported Dictionary ---
maze_functions = {
    'initialize_default_state': initialize_default_state,
    'update_state': update_state,
    'update_history': update_history,
    'update_current_status': update_current_status,
    'take_action': take_action,
    'generate_moderately_open_maze': generate_moderately_open_maze,
    'get_maze_obstacles': get_maze_obstacles,
    'get_maze_start_position': get_maze_start_position,
    'get_maze_goal_position': get_maze_goal_position,
    'get_maze_start_x': get_maze_start_x,
    'get_maze_start_y': get_maze_start_y,
    'get_maze_goal_position_x': get_maze_goal_position_x,
    'get_maze_goal_position_y': get_maze_goal_position_y,
}
