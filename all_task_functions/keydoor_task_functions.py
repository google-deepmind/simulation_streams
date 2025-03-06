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
"""Task functions for the Key-Door environment."""

from typing import Dict, Tuple, Any
import numpy as np

from .grid_base import DIRECTION_MAP
from .grid_base import get_task_functions
from .grid_base import Goal
from .grid_base import grid_from_string
from .grid_base import GridEnv
from .grid_base import Key
from .grid_base import Wall


# Define a custom door class that can be opened with a key.
class KeyDoorObj(Wall):
  """A custom door class that can be opened with a key."""

  def __init__(self, is_open: bool = False) -> None:
    # Start as a door (closed by default); we inherit from Wall so that
    # the agent cannot pass through unless the door is open.
    super().__init__()
    self.object_type = "door"
    self.is_open = is_open

  def can_overlap(self) -> bool:
    if self.is_open:
      return True
    return False

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, str]]:
    if self.is_open:
      return 0, False, {"message": "Passed through open door"}
    elif any(obj.object_type == "key" for obj in agent.inventory):
      # Use the key to open the door.
      self.is_open = True
      # Remove one key from the agent's inventory.
      for idx, obj in enumerate(agent.inventory):
        if obj.object_type == "key":
          del agent.inventory[idx]
          break
      print("Used key to open door")
      return 0, False, {"message": "Used key to open door"}
    else:
      print("Door is closed. A key is needed to open it.")
      return (
          -0.1,
          False,
          {"message": "Door is closed. A key is needed to open it."},
      )


# Define the custom environment.
class KeyDoorEnv(GridEnv):
  """11x11 grid with outer walls and a vertical inner wall along column 5.

  The inner wall is continuous, with one cell replaced by a door.
  A key is located in the right half and the unique goal in the left half.
  Mission: Pick up the key, unlock the door, and reach the goal.
  """

  def __init__(self) -> None:
    # Define a map string that creates outer walls and an inner wall.
    # The vertical wall is in column 5 in rows 1 to 9.
    self.map_str = (
        "W W W W W W W W W W W\n"
        "W F F F F W F F F F W\n"
        "W F S L F W S F L F W\n"
        "W F F F F W F S F F W\n"
        "W F L S F W F F F F W\n"
        "W F F F F W F F L F W\n"
        "W F F L F W F S F F W\n"
        "W F S F F W F F L F W\n"
        "W F F S F W L S F F W\n"
        "W F F F F W F F F F W\n"
        "W W W W W W W W W W W"
    )
    super().__init__(width=11, height=11, max_steps=100)
    # Set the mission after calling super().__init__ so it is not overwritten.
    self.mission = "Pick up the key, unlock the door, and reach the goal."

  def _gen_grid(self, width: int, height: int) -> None:
    # Override grid generation to prevent automatic goal placement.
    self.grid = grid_from_string(self.map_str)
    # Set goal placed flag to True to avoid adding an extra goal.
    self._goal_placed = True

  def reset(self):
    # First, generate the grid and place the agent.
    obs = super().reset()

    # Randomize positions for door, key, goal, and agent.
    # Door: fixed x = 5, y chosen from wall cells (set to row 5 for simplicity)
    door_y = np.random.randint(1, 10)
    # Key: in right half, x in [6, 7, 8, 9] and y in [1, 10)
    key_x = np.random.randint(6, 10)
    key_y = np.random.randint(1, 10)
    # Goal: in left half, x in [1, 2, 3, 4] and y in [1, 10)
    goal_x = np.random.randint(1, 5)
    goal_y = np.random.randint(1, 10)
    # Agent: in right half, x in [6, 7, 8, 9] and y in [1, 10)
    agent_x = np.random.randint(6, 10)
    agent_y = np.random.randint(1, 10)
    self.agent_pos = (agent_x, agent_y)

    # Place the objects.
    self.place_obj_at(Key(), key_x, key_y)
    self.place_obj_at(KeyDoorObj(is_open=False), 5, door_y)
    self.place_obj_at(Goal(), goal_x, goal_y)

    return obs


def determine_first_action(
    agent_dir: int,
    pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    surroundings: Dict[str, str]
) -> Tuple[int, str]:
  """Determine the first action considering both x and y distances to target."""
  dx = target_pos[0] - pos[0]
  dy = target_pos[1] - pos[1]
  preferred_x_dir = "right" if dx > 0 else "left" if dx < 0 else None
  preferred_y_dir = "down" if dy > 0 else "up" if dy < 0 else None
  dir_to_num = {"right": 0, "down": 1, "left": 2, "up": 3}

  if abs(dx) > 0:
    primary_dir = preferred_x_dir
    secondary_dir = preferred_y_dir
  else:
    primary_dir = preferred_y_dir
    secondary_dir = None

  if primary_dir:
    primary_num = dir_to_num[primary_dir]
    if agent_dir == primary_num and surroundings["forward"] != "wall":
      return 2, f"Moving forward toward {primary_dir} since no wall ahead"
    turn_diff = (primary_num - agent_dir) % 4
    if turn_diff == 1:
      return 1, f"Turning right to face {primary_dir}"
    elif turn_diff == 3:
      return 0, f"Turning left to face {primary_dir}"
    elif turn_diff == 2:
      return 1, f"Turning right (first of two turns) to face {primary_dir}"

  if secondary_dir and surroundings["forward"] == "wall":
    secondary_num = dir_to_num[secondary_dir]
    turn_diff = (secondary_num - agent_dir) % 4
    if turn_diff == 1:
      return 1, (
          f"Turning right to move in y-direction ({secondary_dir}) due to wall"
          " ahead"
      )
    elif turn_diff == 3:
      return 0, (
          f"Turning left to move in y-direction ({secondary_dir}) due to wall"
          " ahead"
      )
    elif turn_diff == 2:
      return 1, (
          "Turning right (first of two turns) to move in y-direction"
          f" ({secondary_dir})"
      )

  if surroundings["forward"] != "wall":
    return 2, "Moving forward since aligned with target and no wall ahead"
  elif surroundings["left"] != "wall":
    return 0, "Turning left as fallback since wall ahead"
  else:
    return 1, "Turning right as fallback since walls ahead and to the left"


def describe_keydoor_environment(env):
  """Generates environment description and plans for the initial turn."""
  pos = env.agent_pos
  agent_dir = env.agent_dir
  direction_str = DIRECTION_MAP.get(agent_dir, "unknown")

  if agent_dir == 0:
    orientation_explanation = (
        "Agent is facing right on the map: moving forward means increasing x,"
        " agents left is maps up (decreasing y), agents right is maps down"
        " (increasing y)."
    )
  elif agent_dir == 1:
    orientation_explanation = (
        "Agent is facing down on the map: moving forward means increasing y,"
        " agents left is maps right (increasing x), agents right is maps left"
        " (decreasing x)."
    )
  elif agent_dir == 2:
    orientation_explanation = (
        "Agent is facing left on the map: moving forward means decreasing x,"
        " agents left is maps down (increasing y), agents right is maps up"
        " (decreasing y)."
    )
  elif agent_dir == 3:
    orientation_explanation = (
        "Agent is facing up on the map: moving forward means decreasing y,"
        " agents left is maps left (decreasing x), agents right is maps right"
        " (increasing x)."
    )

  neighbor_info = []
  surroundings = {}
  for d, npos in {
      "forward": (
          pos[0] + (1 if agent_dir == 0 else -1 if agent_dir == 2 else 0),
          pos[1] + (1 if agent_dir == 1 else -1 if agent_dir == 3 else 0),
      ),
      "left": (
          pos[0]
          + (0 if agent_dir in [0, 2] else (1 if agent_dir == 1 else -1)),
          pos[1] + (1 if agent_dir == 0 else -1 if agent_dir == 2 else 0),
      ),
      "right": (
          pos[0]
          + (0 if agent_dir in [0, 2] else (-1 if agent_dir == 1 else 1)),
          pos[1] + ((-1) if agent_dir == 0 else (1) if agent_dir == 2 else 0),
      ),
      "behind": (
          pos[0] - (1 if agent_dir == 0 else -1 if agent_dir == 2 else 0),
          pos[1] - (1 if agent_dir == 1 else -1 if agent_dir == 3 else 0),
      ),
  }.items():
    if 0 <= npos[0] < env.width and 0 <= npos[1] < env.height:
      cell = env.grid.get(*npos)
      if cell is not None:
        if cell.object_type == "floor":
          if hasattr(cell, "appearance"):
            if cell.appearance == 1:
              cell_type = "sand"
            elif cell.appearance == 2:
              cell_type = "lawn"
            else:
              cell_type = "floor"
          else:
            cell_type = "floor"
        else:
          cell_type = cell.object_type
      else:
        cell_type = "floor"
      neighbor_info.append(f"{d} ({npos[0]},{npos[1]}): {cell_type}")
      surroundings[d] = cell_type
    else:
      neighbor_info.append(f"{d}: wall")
      surroundings[d] = "wall"

  key_pos = None
  door_pos = None
  goal_pos = None
  for j in range(env.height):
    for i in range(env.width):
      cell = env.grid.get(i, j)
      if cell is not None:
        if cell.object_type == "key" and key_pos is None:
          key_pos = (i, j)
        elif cell.object_type == "door" and door_pos is None:
          door_pos = (i, j)
        elif cell.object_type == "goal" and goal_pos is None:
          goal_pos = (i, j)

  description = (
      "Key-Door gridworld: avoid walls (-0.1 penalty) and unlock the door to"
      " reach the goal (+1 reward, triggers reset). As we see in the map"
      f" marked by an arrow (> or v or < or ^), the agent is at {pos} facing"
      f" {direction_str}. {orientation_explanation} The agents perspective is"
      " always relative to its facing direction - all turns and movements are"
      " from the agents perspective. Actions: 0=turn left, 1=turn right,"
      " 2=move forward (all from agent perspective). The map also shows the"
      f" Key (as K) at {key_pos}, the Door (as D) at {door_pos}, and the Goal"
      f" (as G) at {goal_pos}. Inspecting cells, cell-by-cell, adjacent to the"
      f" agent arrow in the map, we see: {', '.join(neighbor_info)}. The grid"
      " is divided by a vertical wall, with the key in the right half and the"
      " goal in the left half. We are just starting the task so there is not"
      " yet a history nor any messages, but we will always comprehensively"
      " reflect on the whole history of actions and outcomes, identify"
      " problems, and adapt intelligently. After a reset (triggered when"
      " reaching the goal), we only keep general learning from previous"
      " episodes but not the detailed history. There is no need to revise the"
      " high-level plan during the episode."
  )

  high_level_plan = (
      f"Plan: The agent should first navigate to the key at {key_pos}, then"
      f" move to the door at {door_pos} to unlock it, and finally proceed to"
      f" the goal at {goal_pos}."
  )
  algorithmic_outline = (
      "Outline:\n1. Compute the relative position of the key from the current"
      " location.\n2. Navigate to the key and pick it up (the agent can overlap"
      " the key cell).\n3. Reorient toward the door and unlock it using the"
      " key.\n4. After the door is open, compute a path to the goal and"
      " navigate there.\n5. Adjust movement based on obstacles encountered."
  )

  first_action, action_explanation = determine_first_action(
      agent_dir, pos, key_pos, surroundings
  )

  execution_plan = (
      "Three-phase navigation plan:\n\nPhase 1: Navigate to the key\nFrom"
      f" position {pos} to key at {key_pos}, the x-distance is"
      f" {key_pos[0] - pos[0]} and the y-distance is"
      f" {key_pos[1] - pos[1]}.\nFirst, turn to face"
      f" {'right' if key_pos[0] > pos[0] else 'left'} and move forward"
      f" {abs(key_pos[0] - pos[0])} steps.\nThen, turn to face"
      f" {'down' if key_pos[1] > pos[1] else 'up'} and move forward"
      f" {abs(key_pos[1] - pos[1])} steps.\n\nPhase 2: Navigate from the key to"
      f" the door\nFrom key at {key_pos} to door at {door_pos}, the x-distance"
      f" is {door_pos[0] - key_pos[0]} and the y-distance is"
      f" {door_pos[1] - key_pos[1]}.\nTurn to face"
      f" {'right' if door_pos[0] > key_pos[0] else 'left'} and move"
      f" forward{abs(door_pos[0] - key_pos[0])} steps.\nThen, turn to face"
      f" {'down' if door_pos[1] > key_pos[1] else 'up'} and move forward"
      f" {abs(door_pos[1] - key_pos[1])} steps.\n\nPhase 3: Navigate from the"
      f" door to the goal\nFrom door at {door_pos} to goal at {goal_pos}, the"
      f" x-distance is {goal_pos[0] - door_pos[0]} and the y-distance is"
      f" {goal_pos[1] - door_pos[1]}.\nTurn to face"
      f" {'right' if goal_pos[0] > door_pos[0] else 'left'} and move"
      f" forward{abs(goal_pos[0] - door_pos[0])} steps.\nThen, turn to face"
      f" {'down' if goal_pos[1] > door_pos[1] else 'up'} and move forward"
      f" {abs(goal_pos[1] - door_pos[1])} steps.\n\nBased on this plan, our"
      f" first action will be: {action_explanation} (action code:"
      f" {determine_first_action(agent_dir, pos, key_pos, surroundings)[0]})."
  )

  return (
      description,
      high_level_plan,
      algorithmic_outline,
      execution_plan,
      first_action,
  )


def initialize_default_state(state: Dict[str, Any]) -> str:
  """Initializes the simulation stream state."""
  _ = original_init(state)
  env = state.get("env")
  if env is None:
    # Provide default values if env is None
    description = ""
    high_level_plan = ""
    algo_outline = ""
    execution_plan = ""
    first_action = 2
  else:
    description, high_level_plan, algo_outline, execution_plan, first_action = (
        describe_keydoor_environment(env)
    )
  state["agent_knowledge"] = description
  state["agent_high_level_plan"] = high_level_plan
  state["agent_algorithmic_outline"] = algo_outline
  state["agent_execution_plan"] = execution_plan
  state["agent_action"] = first_action
  return ""


# Retrieve the default task functions from the base helper.
keydoor_task_functions = get_task_functions(KeyDoorEnv)
original_init = keydoor_task_functions["initialize_default_state"]
keydoor_task_functions["initialize_default_state"] = initialize_default_state
