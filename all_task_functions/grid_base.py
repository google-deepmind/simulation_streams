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
"""Engine for grid environments in simulation streams."""

import enum
from typing import Dict, List, Tuple, Optional, Any, Type, TypeVar
import numpy as np

IntEnum = enum.IntEnum

DIRECTION_MAP = {0: "right", 1: "down", 2: "left", 3: "up"}


class WorldObj:
  """Base class for objects in the grid."""

  def __init__(self, object_type: str) -> None:
    self.object_type = object_type
    self.contains = None
    self._init_pos = None
    self._cur_pos = None

  @property
  def cur_pos(self):
    if self._cur_pos is not None:
      return self._cur_pos.copy()
    return None

  @cur_pos.setter
  def cur_pos(self, new_pos: Tuple[int, int]) -> None:
    self._cur_pos = np.array(new_pos)

  @property
  def init_pos(self):
    return self._init_pos.copy() if self._init_pos is not None else None

  @init_pos.setter
  def init_pos(self, new_pos: Tuple[int, int]) -> None:
    self._init_pos = np.array(new_pos)

  def can_overlap(self) -> bool:
    return False

  def can_pickup(self) -> bool:
    return False

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, Any]]:
    # Default behavior for most objects
    del agent
    return 0, False, {}


class Wall(WorldObj):

  def __init__(self) -> None:
    super().__init__("wall")

  def can_overlap(self) -> bool:
    return False

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, Any]]:
    return -0.1, False, {"message": "Bumped into wall"}


class Floor(WorldObj):

  def __init__(self, appearance: int = 0) -> None:
    super().__init__("floor")
    self.appearance = appearance  # 0: default, 1: sand, 2: lawn

  def can_overlap(self) -> bool:
    return True


class Goal(WorldObj):

  def __init__(self, reward_value: float = 1) -> None:
    super().__init__("goal")
    self.reward_value = reward_value

  def can_overlap(self) -> bool:
    return True

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, Any]]:
    return self.reward_value, True, {"message": "Goal reached"}


class Door(WorldObj):
  """A door that can be open or closed."""

  def __init__(self, is_open: bool = False) -> None:
    super().__init__("door")
    self.is_open = is_open

  def can_overlap(self) -> bool:
    return self.is_open

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, Any]]:
    if self.is_open:
      return 0, False, {"message": "Passed through open door"}
    else:
      return -0.1, False, {"message": "Door is closed"}


class AutoDoor(Door):
  """A door that automatically closes after a set number of turns."""

  def __init__(self, is_open: bool = False, auto_close_after: int = 3) -> None:
    super().__init__(is_open)
    self.auto_close_after = auto_close_after
    self.turns_open = 0

  def update_on_turn(self, env: Any) -> None:
    del env
    if self.is_open:
      self.turns_open += 1
      if self.turns_open >= self.auto_close_after:
        self.is_open = False
        self.turns_open = 0


class Key(WorldObj):

  def __init__(self) -> None:
    super().__init__("key")

  def can_overlap(self) -> bool:
    return True

  def can_pickup(self) -> bool:
    return True


class Ball(WorldObj):

  def __init__(self) -> None:
    super().__init__("ball")

  def can_pickup(self) -> bool:
    return True


class Box(WorldObj):

  def __init__(self, contains: Optional[WorldObj] = None) -> None:
    super().__init__("box")
    self.contains = contains

  def can_pickup(self) -> bool:
    return True


class Spikes(WorldObj):
  """Spikes that damage the agent when stepped on."""

  def __init__(self) -> None:
    super().__init__("spikes")

  def can_overlap(self) -> bool:
    return True

  def interact(self, agent: Any) -> Tuple[float, bool, Dict[str, Any]]:
    return -1.0, True, {"message": "Stepped on spikes"}


class GrowingPlant(WorldObj):
  """A plant that grows over time."""

  def __init__(self, growth_stage: int = 0, max_stage: int = 3) -> None:
    super().__init__("plant")
    self.growth_stage = growth_stage
    self.max_stage = max_stage

  def update_on_turn(self, env: Any) -> None:
    del env
    if np.random.random() < 0.1 and self.growth_stage < self.max_stage:
      self.growth_stage += 1

  def can_pickup(self) -> bool:
    return self.growth_stage == self.max_stage

  def can_overlap(self) -> bool:
    return True


class ProximitySensor(WorldObj):
  """A sensor that activates when an agent is nearby."""

  def __init__(
      self, detection_radius: int = 2, is_active: bool = False
  ) -> None:
    super().__init__("sensor")
    self.detection_radius = detection_radius
    self.is_active = is_active

  def on_agent_moved(self, env: Any, event_data: Dict[str, Any]) -> None:
    del event_data
    if self._cur_pos is None:
      return
    agent_x, agent_y = env.agent_pos
    sensor_x, sensor_y = self._cur_pos
    distance = abs(agent_x - sensor_x) + abs(agent_y - sensor_y)
    was_active = self.is_active
    self.is_active = distance <= self.detection_radius
    if not was_active and self.is_active:
      env.events_this_turn["sensor_activated"] = {"position": self._cur_pos}

  def can_overlap(self) -> bool:
    return True


class SpreadingWater(WorldObj):
  """A body of water that spreads over time."""

  def __init__(self, spread_chance: float = 0.2) -> None:
    super().__init__("water")
    self.spread_chance = spread_chance

  def update_on_turn(self, env: Any) -> None:
    """Spread the water to adjacent cells with a given chance."""
    if self._cur_pos is None:
      return
    spread_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    water_x, water_y = self._cur_pos
    for dx, dy in spread_directions:
      if np.random.random() < self.spread_chance:
        new_x, new_y = water_x + dx, water_y + dy
        if 0 <= new_x < env.width and 0 <= new_y < env.height:
          cell = env.grid.get(new_x, new_y)
          if cell is not None and cell.object_type == "floor":
            new_water = SpreadingWater(self.spread_chance)
            env.place_obj_at(new_water, new_x, new_y)

  def can_overlap(self) -> bool:
    return True


class Grid:
  """A simple grid to hold world objects."""

  def __init__(self, width: int, height: int) -> None:
    self.width = width
    self.height = height
    self.grid: List[Optional[WorldObj]] = [None] * (width * height)

  def set(self, i: int, j: int, v: Optional[WorldObj]) -> None:
    assert 0 <= i < self.width and 0 <= j < self.height
    self.grid[j * self.width + i] = v

  def get(self, i: int, j: int) -> Optional[WorldObj]:
    assert 0 <= i < self.width and 0 <= j < self.height
    return self.grid[j * self.width + i]

  def horz_wall(self, x: int, y: int, length: Optional[int] = None) -> None:
    if length is None:
      length = self.width - x
    for i in range(length):
      self.set(x + i, y, Wall())

  def vert_wall(self, x: int, y: int, length: Optional[int] = None) -> None:
    if length is None:
      length = self.height - y
    for j in range(length):
      self.set(x, y + j, Wall())


def grid_from_string(map_string: str) -> Grid:
  """Parse a multi-line string into a Grid object."""
  lines = map_string.strip().splitlines()
  lines = [line.strip() for line in lines]
  height = len(lines)
  rows = [line.split() for line in lines]
  width = max(len(r) for r in rows)
  grid = Grid(width, height)
  for j, tokens in enumerate(rows):
    for i, token in enumerate(tokens):
      if token.upper() == "W":
        grid.set(i, j, Wall())
      elif token.upper() == "F":
        grid.set(i, j, Floor(0))
      elif token.upper() == "S":
        grid.set(i, j, Floor(1))
      elif token.upper() == "L":
        grid.set(i, j, Floor(2))
      elif token.upper() == "G":
        grid.set(i, j, Goal())
      elif token.upper() == "X":
        grid.set(i, j, Spikes())
      else:
        grid.set(i, j, Floor(0))
  return grid


class GridEnv:
  """A gridworld environment with reactive objects."""

  class Actions(IntEnum):
    LEFT = 0
    RIGHT = 1
    FORWARD = 2

  def __init__(
      self, width: int = 10, height: int = 10, max_steps: int = 100
  ) -> None:
    self.width = width
    self.height = height
    self.max_steps = max_steps
    self.step_count = 0
    self.turn_count = 0
    self.inventory: List[WorldObj] = []  # Use a list for inventory
    self.grid: Optional[Grid] = None
    self.agent_pos: Optional[Tuple[int, int]] = None  # (x, y)
    self.agent_dir: Optional[int] = None  # 0: right, 1: down, 2: left, 3: up
    self.mission = ""
    self.events_this_turn: Dict[str, Any] = {}
    self.turn_reactive_objects: List[Tuple[int, int]] = []
    self.event_reactive_objects: Dict[str, List[Tuple[int, int]]] = {}
    self.messages: List[str] = []  # For current messages
    self._goal_placed = False

  def reset(self) -> Dict[str, Any]:
    """Reset the environment to its initial state."""
    self.step_count = 0
    self.turn_count = 0
    self.inventory = []  # Clear inventory on reset
    self.messages = []  # Clear messages on reset
    self._gen_grid(self.width, self.height)
    self.place_agent()
    if not self._goal_placed:
      self.place_obj(Goal())
    self.events_this_turn = {}
    self.turn_reactive_objects = []
    self.event_reactive_objects = {}
    self._scan_for_reactive_objects()
    return self.gen_obs()

  def _gen_grid(self, width: int, height: int) -> None:
    """Generate the grid."""
    if hasattr(self, "map_str") and self.map_str:
      self.grid = grid_from_string(self.map_str)
      self._goal_placed = any(
          cell is not None and cell.object_type == "goal"
          for cell in self.grid.grid
      )
      return
    self.grid = Grid(width, height)
    self._goal_placed = False
    self.grid.horz_wall(0, 0, width)
    self.grid.horz_wall(0, height - 1, width)
    self.grid.vert_wall(0, 0, height)
    self.grid.vert_wall(width - 1, 0, height)
    for i in range(1, width - 1):
      for j in range(1, height - 1):
        self.grid.set(i, j, Floor())

  def place_agent(self) -> None:
    """Place the agent at a random floor cell."""
    if self.grid is None:
      return  # Skip if the grid hasn't been initialized yet
    valid_positions = []
    for i in range(1, self.width - 1):
      for j in range(1, self.height - 1):
        cell = self.grid.get(i, j)
        if cell is not None and cell.object_type == "floor":
          valid_positions.append((i, j))
    if valid_positions:
      pos = valid_positions[np.random.randint(len(valid_positions))]
      self.agent_pos = pos
      self.agent_dir = np.random.randint(0, 4)

  def place_obj(self, obj: WorldObj) -> Optional[Tuple[int, int]]:
    """Place an object (e.g., Goal) in a random floor cell."""
    if self.grid is None:
      return None  # Skip if the grid hasn't been initialized yet
    valid_positions = []
    for i in range(1, self.width - 1):
      for j in range(1, self.height - 1):
        cell = self.grid.get(i, j)
        if (
            cell is not None
            and cell.object_type == "floor"
            and (i, j) != self.agent_pos
        ):
          valid_positions.append((i, j))
    pos = None
    if valid_positions:
      pos = valid_positions[np.random.randint(len(valid_positions))]
      self.place_obj_at(obj, pos[0], pos[1])
      if isinstance(obj, Goal):
        self._goal_placed = True
    return pos

  def place_obj_at(self, obj: WorldObj, i: int, j: int) -> Tuple[int, int]:
    """Place an object at a specific position and register it if reactive."""
    if self.grid is None:
      return (i, j)  # Skip if the grid hasn't been initialized yet
    old_obj = self.grid.get(i, j)
    if old_obj is not None:
      self._unregister_reactive_object(i, j)
    self.grid.set(i, j, obj)
    if obj is not None:
      obj._cur_pos = (i, j)  # pylint: disable=protected-access
      self._register_reactive_object(obj, i, j)
    return (i, j)

  def _scan_for_reactive_objects(self) -> None:
    """Scan the grid for objects with reactive behaviors."""
    if self.grid is None:
      return  # Skip if the grid hasn't been initialized yet
    for i in range(self.width):
      for j in range(self.height):
        obj = self.grid.get(i, j)
        if obj is None:
          continue
        self._register_reactive_object(obj, i, j)

  def _register_reactive_object(self, obj: WorldObj, i: int, j: int) -> None:
    """Register an object's reactive behaviors."""
    if hasattr(obj, "update_on_turn"):
      if (i, j) not in self.turn_reactive_objects:
        self.turn_reactive_objects.append((i, j))
    for attr_name in dir(obj):
      if attr_name.startswith("on_") and callable(getattr(obj, attr_name)):
        event_type = attr_name[3:]
        if event_type not in self.event_reactive_objects:
          self.event_reactive_objects[event_type] = []
        if (i, j) not in self.event_reactive_objects[event_type]:
          self.event_reactive_objects[event_type].append((i, j))

  def _unregister_reactive_object(self, i: int, j: int) -> None:
    """Remove an object's reactive behaviors from tracking."""
    if (i, j) in self.turn_reactive_objects:
      self.turn_reactive_objects.remove((i, j))
    for event_type in self.event_reactive_objects:
      if (i, j) in self.event_reactive_objects[event_type]:
        self.event_reactive_objects[event_type].remove((i, j))

  def gen_obs(self) -> Dict[str, Any]:
    """Generate an observation dictionary."""
    obs = {}
    obs["grid"] = self.grid
    obs["direction"] = self.agent_dir
    obs["mission"] = self.mission
    obs["current_message"] = self.messages[-1] if self.messages else ""
    return obs

  def process_turn_updates(self) -> None:
    """Process updates for all turn-based objects."""
    if self.grid is None:
      return  # Skip if the grid hasn't been initialized yet
    for i, j in self.turn_reactive_objects:
      obj = self.grid.get(i, j)
      if obj is not None and hasattr(obj, "update_on_turn"):
        obj.update_on_turn(self)

  def process_event_updates(self) -> None:
    """Process updates for all event-reactive objects."""
    if self.grid is None:
      return  # Skip if the grid hasn't been initialized yet
    current_events = self.events_this_turn.copy()
    for event_type, event_data in current_events.items():
      if event_type in self.event_reactive_objects:
        for i, j in self.event_reactive_objects[event_type]:
          obj = self.grid.get(i, j)
          if obj is not None and hasattr(obj, f"on_{event_type}"):
            handler = getattr(obj, f"on_{event_type}")
            handler(self, event_data)
    for event_type in current_events:
      if event_type in self.events_this_turn:
        del self.events_this_turn[event_type]

  def step(
      self, action: int
  ) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
    """Execute the given action and update the environment."""
    if self.grid is None:
      return (
          self.gen_obs(),
          0.0,
          False,
          {},
      )  # Skip if grid hasn't been initialized
    pre_pos = self.agent_pos
    pre_inventory = ",".join(obj.object_type for obj in self.inventory)
    self.step_count += 1
    self.turn_count += 1
    done = False
    reward = 0
    if not hasattr(self, "agent_score"):
      self.agent_score = 0
    if action == GridEnv.Actions.LEFT:
      self.agent_dir = (self.agent_dir - 1) % 4
    elif action == GridEnv.Actions.RIGHT:
      self.agent_dir = (self.agent_dir + 1) % 4
    elif action == GridEnv.Actions.FORWARD:
      dx, dy = 0, 0
      if self.agent_dir == 0:
        dx = 1
      elif self.agent_dir == 1:
        dy = 1
      elif self.agent_dir == 2:
        dx = -1
      elif self.agent_dir == 3:
        dy = -1
      new_x = self.agent_pos[0] + dx
      new_y = self.agent_pos[1] + dy
      if 0 <= new_x < self.width and 0 <= new_y < self.height:
        cell = self.grid.get(new_x, new_y)
        if cell is not None:
          if cell.can_overlap():
            self.agent_pos = (new_x, new_y)
            if cell.can_pickup():
              self.inventory.append(cell)
              self._unregister_reactive_object(new_x, new_y)
              self.grid.set(new_x, new_y, None)
              self.messages.append("Picked up object: " + cell.object_type)
            else:
              cell_reward, cell_done, cell_info = cell.interact(self)
              reward += cell_reward
              done = done or cell_done
              if "message" in cell_info:
                self.messages.append(cell_info["message"])
          else:
            cell_reward, cell_done, cell_info = cell.interact(self)
            reward += cell_reward
            done = done or cell_done
            if "message" in cell_info:
              self.messages.append(cell_info["message"])
    self.events_this_turn = {}
    if pre_pos != self.agent_pos:
      self.events_this_turn["agent_moved"] = {
          "prev_pos": pre_pos,
          "new_pos": self.agent_pos,
      }
    current_inventory = ",".join(obj.object_type for obj in self.inventory)
    if pre_inventory != current_inventory:
      if not pre_inventory:
        self.events_this_turn["item_pickup"] = {"item_type": current_inventory}
      else:
        self.events_this_turn["item_drop"] = {"item_type": pre_inventory}
    if self.step_count >= self.max_steps:
      done = True
    obs = self.gen_obs()
    info = {}
    return obs, reward, done, info

  def update_state(self, state: Dict[str, Any]) -> str:
    """Update the state based on the current environment."""
    env = state.get("env")
    if env is None:
      return "No environment available."
    if state["done"]:
      _ = env.reset()
      state["done"] = False
    env.process_turn_updates()
    env.process_event_updates()
    agent_x, agent_y = env.agent_pos
    cell = env.grid.get(agent_x, agent_y)
    state["goal_reached"] = cell is not None and cell.object_type == "goal"
    state["agent_pos"] = env.agent_pos
    state["agent_dir"] = env.agent_dir
    state["step_count"] = env.step_count
    state["obs_text"] = render_obs_text(
        env.gen_obs(), env.agent_pos, env.agent_dir
    )
    return "State updated."

  def update_history(self, state: Dict[str, Any]) -> str:
    """Update the agent's history log."""
    env = state.get("env")
    if env is None:
      return "No environment available."
    inv = (
        ",".join(obj.object_type for obj in env.inventory)
        if env.inventory
        else "None"
    )
    log_entry = (
        f"Step: {env.step_count} | "
        f"Position: {env.agent_pos} | "
        f"Direction: {DIRECTION_MAP.get(env.agent_dir, 'unknown')} | "
        f"Mission: {env.mission} | "
        f"Inventory: {inv}\n"
    )
    if env.messages:
      for msg in env.messages:
        log_entry += f"Message: {msg}\n"
      env.messages = []
    state["agent_history"] += log_entry
    return state["agent_history"]

  def update_current_status(self, state: Dict[str, Any]) -> str:
    """Update the current status of the environment."""
    env = state.get("env")
    if env is None:
      return "No environment available."
    inv = (
        ",".join(obj.object_type for obj in env.inventory)
        if env.inventory
        else "None"
    )
    status = (
        f"Step: {env.step_count}\n"
        f"Position: {env.agent_pos}\n"
        f"Direction: {DIRECTION_MAP.get(env.agent_dir, 'unknown')}\n"
        f"Mission: {env.mission}\n"
        f"Goal Reached: {state.get('goal_reached', False)}\n"
        f"Score: {state.get('agent_score', 0)}\n"
        f"Inventory: {inv}\n"
        f"Map:\n{state.get('obs_text', '')}\n"
    )
    return status

  def take_action(self, state: Dict[str, Any]) -> int:
    """Execute the action specified in the state."""
    env = state.get("env")
    if env is None:
      return 0
    action = state.get("agent_action", env.Actions.FORWARD)
    if not isinstance(action, int) or action not in range(3):
      action = env.Actions.FORWARD
    obs, reward, done, _ = env.step(action)
    state["obs"] = obs
    state["reward"] = reward
    state["agent_score"] = state.get("agent_score", 0) + reward
    state["done"] = done
    state["step_count"] = env.step_count
    state["agent_pos"] = env.agent_pos
    state["agent_dir"] = env.agent_dir
    state["obs_text"] = render_obs_text(obs, env.agent_pos, env.agent_dir)
    return action


def render_obs_text(
    obs: Dict[str, Any], agent_pos: Tuple[int, int], agent_dir: int
) -> str:
  """Render the grid as text, now working directly with Grid object."""
  grid = obs.get("grid")
  if grid is None:
    return "No observation grid available."
  arrow_map = {0: ">", 1: "v", 2: "<", 3: "^"}
  floor_map = {0: "F", 1: "S", 2: "L"}
  text_lines = []
  for j in range(grid.height):
    row_cells = []
    for i in range(grid.width):
      if (i, j) == agent_pos:
        token = arrow_map.get(agent_dir, "A")
      else:
        cell = grid.get(i, j)
        if cell is None:
          token = " "
        elif cell.object_type == "floor":
          appearance = getattr(cell, "appearance", 0)
          token = floor_map.get(appearance, "F")
        elif cell.object_type == "spikes":
          token = "X"
        elif cell.object_type == "door":
          if hasattr(cell, "is_open") and cell.is_open:
            token = "O"
          else:
            token = "D"
        else:
          token = f"{cell.object_type[0].upper()}"
      row_cells.append(token)
    text_lines.append(" ".join(row_cells))
  legend = (
      "Legend: W=Wall (solid barrier), F=Floor (can move here), S=Sand (floor"
      " with different appearance), L=Lawn (floor with different appearance),"
      " K=Key (pickable item), D=Door (closed), O=Door (open), G=Goal"
      " (destination), X=Spikes (dangerous, -1 penalty), >,v,<,^=Agent"
      " (facing right,down,left,up)\nMap coordinates use (x,y) where x"
      " increases rightward and y increases downward"
  )
  rendered_map = "\n".join(text_lines)
  current_message = obs.get("current_message", "")
  if current_message:
    rendered_map += "\n\nMessage: " + current_message
  else:
    rendered_map += "\n\nMessage: No message available"
  rendered_map += "\n\n" + legend
  return rendered_map


T = TypeVar("T", bound=GridEnv)


def get_task_functions(env_class: Type[T]) -> Dict[str, Any]:
  """Generate a dictionary of task functions."""

  def initialize_default_state(state: Dict[str, Any]) -> str:
    env = env_class()
    obs = env.reset()
    defaults = {
        "env": env,
        "obs": obs,
        "done": False,
        "mission": env.mission,
        "agent_pos": env.agent_pos,
        "agent_dir": env.agent_dir,
        "step_count": env.step_count,
        "agent_history": "",
        "goal_reached": False,
        "obs_text": render_obs_text(obs, env.agent_pos, env.agent_dir),
        "grid_size": env.width,
        "agent_action": 2,
        "agent_score": 0,
        "agent_planning_instruction": (
            "Consider the agents current environment and mission, and plan a "
            "high-level strategy for achieving the objective."
        ),
        "agent_high_level_plan": (
            "The agent should navigate the grid efficiently, avoiding obstacles"
            " and moving toward the goal while exploring unknown areas."
        ),
        "agent_planning_algorithmic_instruction": (
            "Provide an algorithmic outline for executing the high-level plan."
        ),
        "agent_algorithmic_outline": (
            "Begin by scanning the immediate surroundings. If the goal is "
            "visible, move directly toward it; otherwise, select an "
            "unexplored direction."
        ),
        "agent_planning_execution_instruction": (
            "Based on the high-level plan and its algorithmic outline, provide "
            "a detailed execution plan for the agent to follow including "
            "immediate steps."
        ),
        "agent_execution_plan": (
            "Move forward if clear; otherwise, turn left and try another"
            " direction."
        ),
        "agent_summary_instruction": (
            "Summarize and reflect on the current knowledge about the task "
            "and how the agent is progressing. This includes tracking the "
            "agent state and all the relevant available information for it. "
            "Think silently step-by-step through all complex elements like "
            "maps, translations between third-person and first-person "
            "perspectives (think cell-by-cell), interactons with objects, "
            "and any unexpected outcomes or difficulties that has taken place."
        ),
        "agent_knowledge": (
            "The agent starts in an unknown grid environment with a specified"
            " mission. The grid may have obstacles and a hidden goal. No"
            " additional knowledge is available at the start."
        ),
        "agent_control_instruction": (
            "Choose an action by picking only a number from the following"
            " available actions: 0: (rotate left), 1: (rotate right), 2: (move"
            " ahead). The action is only the number, not the action name."
        ),
        "revision_question": (
            "Based on recent events, should the high-level plan be revised"
            " (Yes/No)?"
        ),
    }
    for key, value in defaults.items():
      state.setdefault(key, value)
    return ""

  def update_state(state: Dict[str, Any]) -> str:
    env = state.get("env")
    if env is None:
      return "No environment available."
    if state["done"]:
      _ = env.reset()
      state["done"] = False
    env.process_turn_updates()
    env.process_event_updates()
    agent_x, agent_y = env.agent_pos
    cell = env.grid.get(agent_x, agent_y)
    state["goal_reached"] = cell is not None and cell.object_type == "goal"
    state["agent_pos"] = env.agent_pos
    state["agent_dir"] = env.agent_dir
    state["step_count"] = env.step_count
    state["obs_text"] = render_obs_text(
        env.gen_obs(), env.agent_pos, env.agent_dir
    )
    return "State updated."

  def update_history(state: Dict[str, Any]) -> str:
    env = state.get("env")
    if env is None:
      return "No environment available."
    inv = (
        ",".join(obj.object_type for obj in env.inventory)
        if env.inventory
        else "None"
    )
    log_entry = (
        f"Step: {env.step_count} | "
        f"Position: {env.agent_pos} | "
        f"Direction: {DIRECTION_MAP.get(env.agent_dir, 'unknown')} | "
        # f"Mission: {env.mission} | "
        f"Inventory: {inv}\n"
    )
    if env.messages:
      for msg in env.messages:
        log_entry += f"Message: {msg}\n"
      env.messages = []
    state["agent_history"] += log_entry
    return state["agent_history"]

  def update_current_status(state: Dict[str, Any]) -> str:
    env = state.get("env")
    if env is None:
      return "No environment available."
    inv = (
        ",".join(obj.object_type for obj in env.inventory)
        if env.inventory
        else "None"
    )
    status = (
        f"Step: {env.step_count}\n"
        f"Position: {env.agent_pos}\n"
        f"Direction: {DIRECTION_MAP.get(env.agent_dir, 'unknown')}\n"
        f"Mission: {env.mission}\n"
        f"Goal Reached: {state.get('goal_reached', False)}\n"
        f"Inventory: {inv}\n"
        f"Map:\n{state.get('obs_text', '')}\n"
    )
    return status

  def take_action(state: Dict[str, Any]) -> int:
    """Execute the action specified in the state."""
    env = state.get("env")
    if env is None:
      return 0
    action = state.get("agent_action", env.Actions.FORWARD)
    if not isinstance(action, int) or action not in range(3):
      action = env.Actions.FORWARD
    obs, reward, done, _ = env.step(action)
    state["obs"] = obs
    state["reward"] = reward
    state["agent_score"] = state.get("agent_score", 0) + reward
    state["done"] = done
    state["step_count"] = env.step_count
    state["agent_pos"] = env.agent_pos
    state["agent_dir"] = env.agent_dir
    state["obs_text"] = render_obs_text(obs, env.agent_pos, env.agent_dir)
    return action

  return {
      "initialize_default_state": initialize_default_state,
      "update_state": update_state,
      "update_history": update_history,
      "update_current_status": update_current_status,
      "take_action": take_action,
  }
