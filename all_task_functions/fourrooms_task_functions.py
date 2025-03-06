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
"""Task functions for the FourRooms environment."""

from typing import Any, Dict, Tuple, Optional

from .grid_base import DIRECTION_MAP
from .grid_base import get_task_functions
from .grid_base import GridEnv


class FourRoomsEnv(GridEnv):
  """4 rooms gridworld environment."""

  def __init__(
      self,
      agent_pos: Optional[Tuple[int, int]] = None,
      goal_pos: Optional[Tuple[int, int]] = None,
      goal_reward: float = 1,
  ):
    # Also store agent_pos or goal_pos if you wish to override the map.
    self._agent_default_pos = agent_pos
    self._goal_default_pos = goal_pos
    self._goal_reward = goal_reward
    # Set the map string for a FourRooms layout.
    self.map_str = """
    W W W W W W W W W W W
    W S S S S W L L L L W
    W S F S S W L F S L W
    W S S F S W L L F L W
    W S S S S F F F L L W
    W W W W F F F W W W W
    W S S F F F F F L L W
    W F S F S W L F L F W
    W F S F S W L F L F W
    W F S F S W L F L F W
    W W W W W W W W W W W
    """
    super().__init__(width=11, height=11, max_steps=100)
    self.mission = "Reach the goal"


def determine_first_action(
    agent_dir: int,
    pos: Tuple[int, int],
    target_pos: Tuple[int, int],
    surroundings: Dict[str, str]
) -> Tuple[int, str]:
  """Determine the first action considering both x and y distances to target."""
  # Calculate x and y distances to target
  dx = target_pos[0] - pos[0]
  dy = target_pos[1] - pos[1]

  # Determine preferred movement direction
  preferred_x_dir = "right" if dx > 0 else "left" if dx < 0 else None
  preferred_y_dir = "down" if dy > 0 else "up" if dy < 0 else None

  # Convert direction strings to numeric values
  dir_to_num = {"right": 0, "down": 1, "left": 2, "up": 3}

  # Default strategy: Try x-movement first, then y-movement
  if abs(dx) > 0:
    primary_dir = preferred_x_dir
    secondary_dir = preferred_y_dir
  else:
    primary_dir = preferred_y_dir
    secondary_dir = (
        None  # No secondary direction needed if already aligned in x
    )

  # Check if we can move in the primary direction
  if primary_dir:
    primary_num = dir_to_num[primary_dir]

    # If facing the primary direction and no wall ahead
    if agent_dir == primary_num and surroundings["forward"] != "wall":
      return 2, f"Moving forward toward {primary_dir} since no wall ahead"

    # Determine most efficient turn toward primary direction
    turn_diff = (primary_num - agent_dir) % 4
    if turn_diff == 1:
      return 1, f"Turning right to face {primary_dir}"
    elif turn_diff == 3:
      return 0, f"Turning left to face {primary_dir}"
    elif turn_diff == 2:
      return 1, f"Turning right (first of two turns) to face {primary_dir}"

  # If we hit a wall in primary direction or primary complete, try secondary
  if secondary_dir and surroundings["forward"] == "wall":
    secondary_num = dir_to_num[secondary_dir]

    # Determine most efficient turn toward secondary direction
    turn_diff = (secondary_num - agent_dir) % 4
    if turn_diff == 1:
      return (
          1,
          (
              f"Turning right to move in y-direction ({secondary_dir}) due to"
              " wall ahead"
          ),
      )
    elif turn_diff == 3:
      return (
          0,
          (
              f"Turning left to move in y-direction ({secondary_dir}) due to"
              " wall ahead"
          ),
      )
    elif turn_diff == 2:
      return (
          1,
          (
              "Turning right (first of two turns) to move in y-direction"
              f" ({secondary_dir})"
          ),
      )

  # Safety fallbacks
  if surroundings["forward"] != "wall":
    return 2, "Moving forward since aligned with target and no wall ahead"
  elif surroundings["left"] != "wall":
    return 0, "Turning left as fallback since wall ahead"
  else:
    return 1, "Turning right as fallback since walls ahead and to the left"


# Get the task functions for FourRoomsEnv from the base helper.
fourrooms_task_functions = get_task_functions(FourRoomsEnv)

_original_init = fourrooms_task_functions["initialize_default_state"]


def initialize_default_state(state: Dict[str, Any]) -> str:
  """Initializes the simulation stream state."""
  _ = _original_init(state)
  env = state.get("env")

  try:
    # Attempt to get environment description
    if env is not None:
      result = describe_fourrooms_environment(env)

      # Check if result is a tuple of expected length
      if isinstance(result, tuple) and len(result) == 5:
        (
            description,
            high_level_plan,
            algo_outline,
            execution_plan,
            first_action,
        ) = result
      else:
        # Default values if result is not as expected
        description = "Environment description unavailable"
        high_level_plan = "High level plan unavailable"
        algo_outline = "Algorithm outline unavailable"
        execution_plan = "Execution plan unavailable"
        first_action = 2  # Default action
    else:
      # Default values if env is None
      description = "Environment not initialized"
      high_level_plan = "No plan available"
      algo_outline = "No algorithm available"
      execution_plan = "No execution plan available"
      first_action = 2  # Default action
  except Exception as e:  # pylint: disable=broad-exception-caught
    # Fallback if any error occurs
    print(f"Error initializing state: {e}")
    description = f"Error initializing environment: {str(e)}"
    high_level_plan = "Error in planning"
    algo_outline = "Error in algorithm"
    execution_plan = "Error in execution plan"
    first_action = 2  # Default action

  # Set the state values
  state["agent_knowledge"] = description
  state["agent_high_level_plan"] = high_level_plan
  state["agent_algorithmic_outline"] = algo_outline
  state["agent_execution_plan"] = execution_plan
  state["agent_action"] = first_action

  return ""


fourrooms_task_functions["initialize_default_state"] = initialize_default_state


def describe_fourrooms_environment(
    env: FourRoomsEnv
):
  """Generates environment description and plans for the initial turn."""
  if env.grid is None:
    return  # Skip if the grid hasn't been initialized yet
  pos = env.agent_pos
  agent_dir = env.agent_dir

  # Define relative directions based on agent's current direction
  # The mapping is:
  # 0: right, 1: down, 2: left, 3: up
  relative_dirs = {}

  # Forward position based on current direction
  if agent_dir == 0:  # Facing right
    relative_dirs["forward"] = (pos[0] + 1, pos[1])
    relative_dirs["left"] = (pos[0], pos[1] - 1)
    relative_dirs["right"] = (pos[0], pos[1] + 1)
    relative_dirs["behind"] = (pos[0] - 1, pos[1])
  elif agent_dir == 1:  # Facing down
    relative_dirs["forward"] = (pos[0], pos[1] + 1)
    relative_dirs["left"] = (pos[0] + 1, pos[1])
    relative_dirs["right"] = (pos[0] - 1, pos[1])
    relative_dirs["behind"] = (pos[0], pos[1] - 1)
  elif agent_dir == 2:  # Facing left
    relative_dirs["forward"] = (pos[0] - 1, pos[1])
    relative_dirs["left"] = (pos[0], pos[1] + 1)
    relative_dirs["right"] = (pos[0], pos[1] - 1)
    relative_dirs["behind"] = (pos[0] + 1, pos[1])
  elif agent_dir == 3:  # Facing up
    relative_dirs["forward"] = (pos[0], pos[1] - 1)
    relative_dirs["left"] = (pos[0] - 1, pos[1])
    relative_dirs["right"] = (pos[0] + 1, pos[1])
    relative_dirs["behind"] = (pos[0], pos[1] + 1)

  # Get information about surrounding cells
  neighbor_info = []
  surroundings = {}
  for d, npos in relative_dirs.items():
    if 0 <= npos[0] < env.width and 0 <= npos[1] < env.height:
      cell = env.grid.get(*npos)
      if cell is not None:
        if cell.object_type == "floor":
          # Check the appearance attribute for different floor types
          if hasattr(cell, "appearance"):
            if cell.appearance == 1:  # Sand
              cell_type = "sand"
            elif cell.appearance == 2:  # Lawn
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
      # For cells outside the grid, we'll mark them as wall without coordinates
      neighbor_info.append(f"{d}: wall")
      surroundings[d] = "wall"

  # Find the goal position by scanning the grid.
  goal_pos = None
  for j in range(env.height):
    for i in range(env.width):
      cell = env.grid.get(i, j)
      if cell is not None and cell.object_type == "goal":
        goal_pos = (i, j)
        break
    if goal_pos is not None:
      break

  # Determine the room for the agent and the goal.
  # For an 11x11 grid, interior cells are indices 1 to 9.
  def get_room(p, width, height):
    mid_x = (width - 2) // 2 + 1  # center of interior
    mid_y = (height - 2) // 2 + 1
    hor = "left" if p[0] < mid_x else "right"
    ver = "top" if p[1] < mid_y else "bottom"
    return f"{ver} {hor}"

  agent_room = get_room(pos, env.width, env.height)
  goal_room = (
      get_room(goal_pos, env.width, env.height)
      if goal_pos is not None
      else "unknown"
  )

  direction_str = DIRECTION_MAP.get(agent_dir, "unknown")

  # Create directional mapping explanation based on agent's current direction
  if agent_dir == 0:  # Facing right
    orientation_explanation = (
        "Agent is facing right on the map: moving forward means increasing x,"
        " agents left is maps up (decreasing y), agents right is maps down"
        " (increasing y)"
    )
  elif agent_dir == 1:  # Facing down
    orientation_explanation = (
        "Agent is facing down on the map: moving forward means increasing y,"
        " agents left is maps right (increasing x), agents right is maps left"
        " (decreasing x)"
    )
  elif agent_dir == 2:  # Facing left
    orientation_explanation = (
        "Agent is facing left on the map: moving forward means decreasing x,"
        " agents left is maps down (increasing y), agents right is maps up"
        " (decreasing y)"
    )
  elif agent_dir == 3:  # Facing up
    orientation_explanation = (
        "Agent is facing up on the map: moving forward means decreasing y,"
        " agents left is maps left (decreasing x), agents right is maps right"
        " (increasing x)"
    )

  description = (
      "FourRooms gridworld: avoid walls (-0.1 penalty), reach goal (+1 reward,"
      " triggers reset). As we see in the map marked by an arrow (<,v,...) the"
      f" agent is at {pos} facing {direction_str}. {orientation_explanation}."
      " The agents perspective is always relative to its facing direction -"
      " all turns and movements are from the agents perspective. Actions:"
      " 0=turn left, 1=turn right, 2=move forward (all from agents"
      f" perspective). The map also shows the Goal (as G) at {goal_pos}."
      " Inspecting cells, cell-by-cell, adjacent to the agent arrow in the"
      " map, and expressing it from the agents perspective, we see:"
      f" {', '.join(neighbor_info)}. The agent is in the {agent_room} room and"
      f" the goal is in the {goal_room} room. We are just starting the task so"
      " there is not yet a history, but we will always here comprehensively"
      " reflect on the whole history of actions and outcomes, identify"
      " problems and adapt intelligently. After a reset (triggered when"
      " reaching the goal), we only keep general learning from previous"
      " episodes but not the detailed history in the knowledge. There is not"
      " need to revise the high-level plan during the episode."
  )

  # Generate plans based on agent's and goal's positions
  if agent_room == goal_room:
    high_level_plan = (
        f"The agent and the goal are both in the {agent_room} room. "
        f"The agent should move directly to the goal at {goal_pos}."
    )
    algorithmic_outline = (
        "1. Figure out how far away the goal is left/right and up/down.\n2."
        " Plan to reach the goal by first moving in x-direction (left/right),"
        " then in y-direction (up/down).\n3. Turn in the right direction before"
        " moving forward.\n4. If you hit a wall, try going in y-direction"
        " instead and then again in x-direction.\n5. Always check what is in"
        " front before moving forward."
    )

    # Calculate first action using the enhanced function
    first_action, action_explanation = determine_first_action(
        agent_dir, pos, goal_pos, surroundings
    )

    execution_plan = (
        f"From position {pos} to goal at {goal_pos}, the steps needed in the"
        f" x-direction is ({goal_pos[0] - pos[0]}) and then we need to move"
        f" ({goal_pos[1] - pos[1]}) in the y-direction. First move in"
        " x-direction by turning to face"
        f" {'right' if goal_pos[0] > pos[0] else 'left'}. Always turn"
        " efficiently - use a single left or right turn when possible. For"
        " 180-degree turns (e.g., from facing up to facing down), turn twice"
        " in the same direction. After facing the correct direction, move"
        f" forward {abs(goal_pos[0] - pos[0])} steps. If a wall is encountered,"
        " switch to move in the y-direction first by turning until facing"
        f" {'down' if goal_pos[1] > pos[1] else 'up'}, then return to complete"
        " the x-direction movement after bypassing the wall. Always check the"
        " surroundings before moving. Currently, the agents surroundings as"
        " seen in the agents knowledge (derived from the map) are:"
        f" {', '.join(neighbor_info)}. Only"
        " move forward if there is no wall in that direction. Based on this"
        f" plan, our first action will be: {action_explanation} (action code:"
        f" {first_action})."
    )
  else:
    # Define central region coordinates
    center_x = env.width // 2
    center_y = env.height // 2
    center_region = {
        "x_min": center_x - 1,
        "x_max": center_x + 1,
        "y_min": center_y - 1,
        "y_max": center_y + 1,
    }

    # For an 11x11 grid, this would be the region (4-6,4-6)
    center_region_str = f"({center_region['x_min']}-{center_region['x_max']},{center_region['y_min']}-{center_region['y_max']})"

    # Define function to get the doorway for a room
    def get_room_doorway(position, room_name):
      # Calculate middle points
      mid_x = center_x  # 5 for an 11x11 grid
      mid_y = center_y  # 5 for an 11x11 grid

      # Determine which doorway to use based on room name
      if "top left" in room_name:
        return (mid_x - 1, center_region["y_min"])  # (4,4) for 11x11 grid
      elif "top right" in room_name:
        return (mid_x + 1, center_region["y_min"])  # (6,4) for 11x11 grid
      elif "bottom left" in room_name:
        return (mid_x - 1, center_region["y_max"])  # (4,6) for 11x11 grid
      elif "bottom right" in room_name:
        return (mid_x + 1, center_region["y_max"])  # (6,6) for 11x11 grid

      # Fallback if room name doesn't contain the expected pattern
      if "top" in room_name:
        if position[0] < mid_x:
          return (mid_x - 1, center_region["y_min"])  # top left doorway
        else:
          return (mid_x + 1, center_region["y_min"])  # top right doorway
      elif "bottom" in room_name:
        if position[0] < mid_x:
          return (mid_x - 1, center_region["y_max"])  # bottom left doorway
        else:
          return (mid_x + 1, center_region["y_max"])  # bottom right doorway

      # If still not found, use the nearest doorway based on position
      if position[1] < mid_y and position[0] < mid_x:
        return (mid_x - 1, center_region["y_min"])  # top left
      elif position[1] < mid_y and position[0] >= mid_x:
        return (mid_x + 1, center_region["y_min"])  # top right
      elif position[1] >= mid_y and position[0] < mid_x:
        return (mid_x - 1, center_region["y_max"])  # bottom left
      else:
        return (mid_x + 1, center_region["y_max"])  # bottom right

    # Get doorways for both agent and goal rooms using the same method
    agent_doorway = get_room_doorway(pos, agent_room)
    goal_doorway = get_room_doorway(goal_pos, goal_room)

    # For the first action, target the doorway of the agent's room
    target_center_pos = agent_doorway

    high_level_plan = (
        f"The agent is in the {agent_room} room and the goal is in the"
        f" {goal_room} room. The agent should navigate from the current room"
        f" through the central region {center_region_str} to reach the"
        f" {goal_room} room, and then move to the goal."
    )
    algorithmic_outline = (
        "Three-phase navigation algorithm:\n\nPhase 1: Navigate to own room"
        " doorway\n1. Identify the doorway connecting the agents current room"
        " to the central region.\n2. Calculate steps needed in x and y"
        " directions to reach this doorway.\n3. Navigate to this doorway point"
        " using the most efficient path.\n\nPhase 2: Cross central region to"
        " goal room doorway\n4. From the current room doorway, identify the"
        " doorway to the goal room.\n5. Navigate through the central region to"
        " the goal room doorway.\n\nPhase 3: Navigate from goal room doorway to"
        " goal\n6. From the goal room doorway, calculate steps to the goal"
        " position.\n7. Navigate from the doorway to the goal using the most"
        " efficient path.\n\nGeneral movement principles:\n- At each step, turn"
        " in the right direction before moving forward.\n- Try moving in"
        " x-direction first, then y-direction (adapt if needed).\n- If a wall"
        " is encountered, try the other coordinate direction first.\n- Always"
        " check what is in front before moving forward."
    )

    # Calculate first action using the enhanced function
    first_action, action_explanation = determine_first_action(
        agent_dir, pos, target_center_pos, surroundings
    )

    execution_plan = (
        "Three-phase navigation plan:\n\nPhase 1: Navigate to own room"
        f" doorway\nStarting at position {pos}, navigate to the doorway of our"
        f" current room at {agent_doorway}.\nDistance:"
        f" {abs(agent_doorway[0] - pos[0])} steps in x-direction and"
        f" {abs(agent_doorway[1] - pos[1])} steps in y-direction.\n1a. Turn to"
        " face"
        f" {'right' if agent_doorway[0] > pos[0] else 'left' if agent_doorway[0] < pos[0] else 'current direction (already aligned in x)'}.\n1b."
        " Move to align with the doorway x-coordinate"
        f" ({agent_doorway[0]}).\n1c. Turn to face"
        f" {'down' if agent_doorway[1] > pos[1] else 'up' if agent_doorway[1] < pos[1] else 'current direction (already aligned in y)'}.\n1d."
        f" Move to the doorway y-coordinate ({agent_doorway[1]}).\n\nPhase 2:"
        " Cross central region to goal room doorway\nFrom our room doorway at"
        f" {agent_doorway}, navigate to the goal room doorway at"
        f" {goal_doorway}.\nDistance:"
        f" {abs(goal_doorway[0] - agent_doorway[0])} steps in x-direction and"
        f" {abs(goal_doorway[1] - agent_doorway[1])} steps in y-direction.\n2a."
        " Turn to face"
        f" {'right' if goal_doorway[0] > agent_doorway[0] else 'left' if goal_doorway[0] < agent_doorway[0] else 'current direction (already aligned in x)'}.\n2b."
        " Move to align with the goal doorway x-coordinate"
        f" ({goal_doorway[0]}).\n2c. Turn to face"
        f" {'down' if goal_doorway[1] > agent_doorway[1] else 'up' if goal_doorway[1] < agent_doorway[1] else 'current direction (already aligned in y)'}.\n2d."
        f" Move to the goal doorway y-coordinate ({goal_doorway[1]}).\n\nPhase"
        " 3: Navigate from goal room doorway to goal\nFrom the goal room"
        f" doorway at {goal_doorway}, navigate to the goal at"
        f" {goal_pos}.\nDistance: {abs(goal_pos[0] - goal_doorway[0])} steps in"
        f" x-direction and {abs(goal_pos[1] - goal_doorway[1])} steps in"
        " y-direction.\n3a. Turn to face"
        f" {'right' if goal_pos[0] > goal_doorway[0] else 'left' if goal_pos[0] < goal_doorway[0] else 'current direction (already aligned in x)'}.\n3b."
        f" Move to align with the goal x-coordinate ({goal_pos[0]}).\n3c. Turn"
        " to face"
        f" {'down' if goal_pos[1] > goal_doorway[1] else 'up' if goal_pos[1] < goal_doorway[1] else 'current direction (already aligned in y)'}.\n3d."
        f" Move to the goal y-coordinate ({goal_pos[1]}).\n\nGeneral navigation"
        " principles:\n- Always turn efficiently (single left/right turn when"
        " possible, two turns in same direction for 180-degree turns).\n-"
        f" Check surroundings before moving: {', '.join(neighbor_info)}.\n-"
        " Only move forward if there is no wall in that direction.\n- If a"
        " wall is encountered, try the other coordinate direction first, then"
        " return to original plan.\n- Adapt dynamically if unexpected"
        " obstacles are encountered.\n\nCurrent status: We are in Phase"
        f" 1\nFirst action: {action_explanation} (action code: {first_action})."
    )

  return (
      description,
      high_level_plan,
      algorithmic_outline,
      execution_plan,
      first_action,  # Return the first action to be set in state
  )
