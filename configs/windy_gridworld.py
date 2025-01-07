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

"""Config for Simulation of an agent running a windy gridworld task."""

ecs_config = {
    'entities': {
        'world': ['heading'],
        'agent': [
            'history_log',
            'planning',
            'move',
            'updates',
        ],
        'end': ['messages'],
    },
    'variables': {
        'heading': {
            'time': 0,
            'wind_x': 0,
            'wind_y': 0,
            'grid_size': 10,
            'target_x': 4,
            'target_y': 8,
        },
        'move': {
            'position_x': 0,
            'position_y': 0,
            'move_x': 0,
            'move_y': 0,
        },
        'planning': {'revision_response': 'No'},
        'history_log': {
            'history': 'Start. ',
            'message': 'The task has started!',
        },
        'updates': {
            'distance_to_target': 0,
            'score': 0,
            'average_score': 0,
        },
        'messages': {},
    },
    'systems_definitions': {
        'messages': [
            {
                'formula': 'blank',
                'visibility': 'plan',
                'for_summary': 'Yes',
                'experience': True,
            },
        ],
        'heading': [
            {
                'formula': 'world_time = world_time + 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'experience': True,
            },
            {
                'formula': (
                    "world_objective = 'Objective: Move towards the target at"
                    " (' + str(world_target_x) + ', ' + str(world_target_y)"
                    " + ')'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'world_wind_x = np.random.choice([-1, 0, 1])',
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'world_wind_y = np.random.choice([-1, 0, 1])',
                'visibility': 'plan',
                'for_summary': 'No',
            },
        ],
        'updates': [
            {
                'formula': (
                    'agent_distance_to_target = np.sqrt((agent_position_x -'
                    ' world_target_x)**2 + (agent_position_y -'
                    ' world_target_y)**2)'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'agent_score = 5 - agent_distance_to_target',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'agent_average_score = (agent_average_score * (world_time -'
                    ' 1) + agent_score) / world_time'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'planning': [
            {
                'formula': (
                    'planning_instruction = "Consider the agents past'
                    " developments and in particular the assistants"
                    ' knowledge, make a high-level plan for how to achieve the'
                    ' objective."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_high_level_plan = "The agent should aim to move'
                    ' towards the target at (4,8)."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "agent_revision_response.lower().startswith('y')",
                'query': {'visibility': 'plan'},
            },
            {
                'formula': (
                    'planning_algorithmic_instruction = "Provide an algorithmic'
                    ' outline for the plan above."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_algorithmic_outline = "Always take a step in the'
                    ' direction that decreases the distance to the target the'
                    ' most when taking the wind into account."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': (
                    'planning_execution_instruction = "Consider the'
                    " assistants high-level plan and its algorithmic outline"
                    ' and plan concrete next steps from the current state.'
                    " Consider the previous time steps execution plan and"
                    ' build on it."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_execution_plan = "As the agent is at (0,0) and'
                    ' the target is at (4,8), the agent should move in the'
                    ' direction of the target by moving by 1 in both the x and'
                    ' y directions, even if the wind will move it away again."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
        ],
        'move': [
            {
                'formula': (
                    "agent_movement_instruction_x = 'Choose the x-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    ' (d,0) from (x,y) to (x+d+v,y) for wind v in the'
                    " x-direction.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'agent_move_x = 0',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'agent_move_x = max(-1, min(1, agent_move_x))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'agent_position_x = agent_position_x + agent_move_x +'
                    ' world_wind_x'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'agent_position_x = max(0, min(4, agent_position_x))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "agent_movement_instruction_y = 'Choose the y-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    ' (0,d) from (x,y) to (x,y+d+w) for wind w in the'
                    " y-direction.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'agent_move_y = 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'agent_move_y = max(-1, min(1, agent_move_y))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'agent_position_y = agent_position_y + agent_move_y +'
                    ' world_wind_y'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'agent_position_y = max(0, min(4, agent_position_y))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'history_log': [
            {
                'formula': 'agent_message = agent_message',
                'visibility': 'plan',
                'for_summary': 'True',
            },
            {
                'formula': 'agent_message = ""',
                'visibility': 'hidden',
                'for_summary': 'False',
            },
            {
                'formula': (
                    "agent_history = agent_history + 'Time ' + str(world_time)"
                    " + ': Position: ' + str(round(agent_position_x, 2)) + ', '"
                    " + str(round(agent_position_y, 2)) + '; Distance to"
                    " Target: ' + str(round(agent_distance_to_target, 2)) +"
                    " '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "agent_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Position: ' +"
                    " str(round(agent_position_x, 2)) + ', ' +"
                    " str(round(agent_position_y, 2)) + '; Distance to Target:"
                    " ' + str(round(agent_distance_to_target, 2)) + '.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "summary_instruction = 'Make a comprehensive factual"
                    ' summary of the relevant knowledge gained at this point.'
                    ' Ensure accuracy and avoid fabrication of events that did'
                    ' not occur. Reflect on the current status and any'
                    " changes.'"
                ),
                'visibility': 'x',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "assistant_knowledge = 'The agent is at (0,0) in a windy"
                    ' 10x10 gridworld with a target at (4,8). The wind is'
                    ' changing randomly. The agent is just starting out so'
                    " there is no history to analyze.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': (
                    "revision_question = 'Given the recent events and"
                    ' developments, should the high-level plan and its'
                    " algorithmic outline be revised (Yes/No)?'"
                ),
                'visibility': 'x',
                'for_summary': 'Yes',
            },
            {
                'formula': 'agent_revision_response = agent_revision_response',
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
        ],
    },
}
