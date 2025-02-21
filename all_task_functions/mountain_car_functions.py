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

"""Task functions for the Mountain Car environment."""

import numpy as np


def initialize_default_state(state):
  """Initializes the default state for the Mountain Car environment."""
  defaults = {
      'car_position': -0.5,
      'car_velocity': 0.0,
      'car_acceleration': 0.0,
      'car_force': 1.0,  # The main control variable
      'car_goal_position': 0.5,
      'agent_score': 0.0,
      'agent_history': 'Start. ',
      'agent_message': '',
      'agent_current_status': '',
      'agent_action': 1.0,
      'agent_planning_instruction': (
          'Consider the agents past developments and the knowledge string to'
          ' form a high-level plan to achieve the task objective.'
      ),
      'agent_high_level_plan': (
          'The vehicle should try accelerating towards the goal, but if the'
          ' hill makes the vehicle reverse down before reaching the goal,'
          ' accelerate in the opposite direction to gather momentum.'
      ),
      'agent_planning_algorithmic_instruction': (
          'Provide an algorithmic outline for the above plan.'
      ),
      'agent_algorithmic_outline': (
          'First, use Force 1 forward until velocity decreases, then reverse'
          ' the force to -1 until momentum is built, and finally use Force 1'
          ' again to reach the goal.'
      ),
      'agent_planning_execution_instruction': (
          'Based on the plan and its outline, determine the next concrete steps'
          ' from the current state.'
      ),
      'agent_execution_plan': (
          'The vehicle should use Force 1 forward until velocity decreases'
          ' towards negative, then switch to -1, and finally revert to Force 1'
          ' to reach the goal.'
      ),
      'agent_summary_instruction': (
          'Make a comprehensive factual summary of the current state. Reflect'
          ' on the cars position, velocity, and overall progress.'
      ),
      'agent_control_instruction': (
          'Choose the force, according to the plan, to accelerate the car so as'
          ' to reach the goal at position=+0.5 (height 1.0).'
      ),
      'agent_knowledge': (
          'The vehicle is at position -0.5 with velocity 0.0 and acceleration'
          ' 0.0. The task involves an underpowered vehicle trying to get up a'
          ' hill. There is also a hill behind the vehicle. The goal is to reach'
          ' position +0.5, and it is unlikely to have enough power to go'
          ' straight up to the goal.'
      ),
  }
  for key, value in defaults.items():
    state.setdefault(key, value)
  return ''


def _update_acceleration(state):
  """Updates the car's acceleration."""
  state['car_acceleration'] = state['car_force'] * 0.1 - 0.25 * np.cos(
      3 * state['car_position']
  )
  return state


def _update_velocity(state):
  """Updates the car's velocity based on the current acceleration."""
  state['car_velocity'] = state['car_velocity'] + state['car_acceleration']
  return state


def _update_position(state):
  """Updates the car's position based on the current velocity."""
  state['car_position'] = state['car_position'] + state['car_velocity']
  return state


def _compute_reward(state):
  """Computes the reward based on the car's position relative to the goal."""
  return 1 if state['car_position'] >= state['car_goal_position'] else 0


def update_state(state):
  """Updates the entire state of the Mountain Car environment."""
  _update_acceleration(state)
  _update_velocity(state)
  _update_position(state)
  state['agent_score'] = _compute_reward(state)
  return 'State updated'


def update_history(state):
  """Updates the agent's history with the current state."""
  new_entry = (
      f"Time {state['world_time']}: "
      f"Position {state['car_position']:.2f}, "
      f"Velocity {state['car_velocity']:.2f}, "
      f"Acceleration {state['car_acceleration']:.2f}, "
      f"Force: {state['car_force']:.2f}\n"
  )
  state['agent_history'] += new_entry
  return state['agent_history']


def update_current_status(state):
  """Updates the current status of the agent."""
  status = (
      f"Time {state['world_time']}: "
      f"Position {state['car_position']:.2f}, "
      f"Velocity {state['car_velocity']:.2f}, "
      f"Acceleration {state['car_acceleration']:.2f}, "
      f"Force: {state['car_force']:.2f}"
  )
  return status


def take_action(state):
  """Takes an action and updates the car's force."""
  action = state.get('agent_action', 0)
  normalized_action = max(-1, min(1, action))
  state['car_force'] = normalized_action
  return normalized_action


mountain_car_functions = {
    'initialize_default_state': initialize_default_state,
    'update_state': update_state,
    'update_history': update_history,
    'update_current_status': update_current_status,
    'take_action': take_action,
}
