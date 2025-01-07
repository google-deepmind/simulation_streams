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
"""Config for key-chest gridworld."""

ecs_config = {
    'entities': {
        'world': [
            'heading',
        ],
        'agent': [
            'history_log',
            'planning',
            'move',
            # 'tile_selector',
            # 'road',
            'road_object_selector',
            'chest',
            'return',
            'key',
            'updates',
            'messages',
        ],
    },
    'variables': {
        'heading': {
            'time': 0,
            'grid_size': 5,
        },
        'planning': {
            'revision_response': 'No',
        },
        'history_log': {
            'history': 'Start. ',
            'message': 'The task has started!',
        },
        'move': {
            'position_x': 0,
            'position_y': 0,
            'move_x': 0,
            'move_y': 0,
            'hit_wall': False,
        },
        'updates': {
            'score': 0,
            'average_score': 0,
            'key_found': False,
            'hidden_key_found': False,
            'tiles': 'tile_map(5)',
            'object_map': 'object_map(5, {index})',
            'chest_opened': False,
            'hidden_chest_opened': False,
        },
        'tile_selector': {},
        'road_object_selector': {},
        'road': {},
        'return': {},
        'chest': {},
        'key': {},
        'messages': {},
    },
    'systems_definitions': {
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
                'id': 'operator_1_agent_planning',
            },
            {
                'formula': (
                    'assistant_high_level_plan = "The agent needs to find the'
                    ' key to be able to open the chest at (2,3). The agent'
                    ' should explore the map, searching for the key in places'
                    ' it has not yet seen, while ignoring the chest. The agent'
                    ' should search the map row-by-row to neither repeat nor'
                    ' miss locations."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "agent_revision_response.lower().startswith('y')",
                'query': {
                    'visibility': 'plan',
                },
                'id': 'operator_2_agent_planning',
            },
            {
                'formula': (
                    'planning_algorithmic_instruction = "Provide an algorithmic'
                    ' outline for the plan above."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'id': 'operator_3_agent_planning',
            },
            {
                'formula': (
                    'assistant_algorithmic_outline = "1. Go from (0,0) to (0,4)'
                    ' one step at a time. 2. Step up to (1,4) and then'
                    ' step-by-step to (1,0). 3. Step up to (2,0) and then'
                    ' step-by-step to (2,4), up to (3,4) and step-by-step to'
                    ' (3,0), then up to (4,0) and step-by-step to (4,4) until'
                    ' the key is found, while ignoring the chest until finding'
                    ' the key."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_4_agent_planning',
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
                'id': 'operator_5_agent_planning',
            },
            {
                'formula': (
                    'assistant_execution_plan = "The agent is at (0,0) and'
                    ' should move to (0,1) and down the first row to (0,4) and'
                    ' then turn at (1,4) to search the second row where x is 1,'
                    ' if the key has not been found and then if necessary the'
                    ' third, fourth, and fifth row."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_6_agent_planning',
            },
        ],
        'history_log': [
            {
                'formula': 'agent_message = agent_message',
                'visibility': 'plan',
                'for_summary': 'True',
                'id': 'operator_1_agent_history_log',
            },
            {
                'formula': 'agent_message = ""',
                'visibility': 'hidden',
                'for_summary': 'False',
                'id': 'operator_2_agent_history_log',
            },
            {
                'formula': (
                    "agent_history = agent_history + 'Time ' + str(world_time)"
                    " + ': Position: ' + str(round(agent_position_x, 2)) + ', '"
                    " + str(round(agent_position_y, 2)) + '; Key Found: ' +"
                    " ('Yes' if agent_key_found else 'No') + '; Chest Opened: '"
                    " + ('Yes' if agent_chest_opened else 'No') + '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
                'id': 'operator_3_agent_history_log',
            },
            {
                'formula': (
                    "agent_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Position: ' +"
                    " str(round(agent_position_x, 2)) + ', ' +"
                    " str(round(agent_position_y, 2)) + '; Key Found: ' +"
                    " ('Yes' if agent_key_found else 'No') + '; Chest Opened: '"
                    " + ('Yes' if agent_chest_opened else 'No') + '.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
                'id': 'operator_4_agent_history_log',
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
                'id': 'operator_5_agent_history_log',
            },
            {
                'formula': (
                    "agent_summary = 'The agent is at (0,0) in a 5x5 gridworld"
                    ' (0,...,4x0,...,4) with a chest at (2,3) that can only be'
                    ' opened with a key whose location is unknown to me. The'
                    ' agent does not have the key and the chest is still'
                    ' closed. In the vicinity, I have seen (0,0) and I am at'
                    " (0,1). The key could be anywhere else.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
                'query': {
                    'for_summary': 'Yes',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_6_agent_history_log',
            },
            {
                'formula': (
                    "revision_question = 'Given the recent events and"
                    ' developments, should the high-level plan and its'
                    " algorithmic outline be revised (Yes/No)?'"
                ),
                'visibility': 'x',
                'for_summary': 'Yes',
                'id': 'operator_7_agent_history_log',
            },
            {
                'formula': 'agent_revision_response = agent_revision_response',
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {
                    'for_summary': 'Yes',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_8_agent_history_log',
            },
        ],
        'move': [
            {
                'formula': (
                    "agent_movement_instruction_x = 'Choose the x-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (d,0) from (x,y) to (x+d,y)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'id': 'operator_1_agent_move',
            },
            {
                'formula': 'agent_move_x = 0',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_2_agent_move',
            },
            {
                'formula': 'agent_move_x = max(-1, min(1, agent_move_x))',
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_3_agent_move',
            },
            {
                'formula': 'agent_position_x = agent_position_x + agent_move_x',
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_4_agent_move',
            },
            {
                'formula': (
                    'agent_position_x = max(0, min(4, agent_position_x))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_5_agent_move',
            },
            {
                'formula': (
                    "agent_movement_instruction_y = 'Choose the y-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (0,d) from (x,y) to (x,y+d)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'id': 'operator_6_agent_move',
            },
            {
                'formula': 'agent_move_y = 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
                'id': 'operator_7_agent_move',
            },
            {
                'formula': 'agent_move_y = max(-1, min(1, agent_move_y))',
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_8_agent_move',
            },
            {
                'formula': 'agent_position_y = agent_position_y + agent_move_y',
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_9_agent_move',
            },
            {
                'formula': (
                    'agent_position_y = max(0, min(4, agent_position_y))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_10_agent_move',
            },
        ],
        'heading': [
            {
                'formula': 'world_time = world_time + 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'experience': True,
                'id': 'operator_1_world_heading',
            },
            {
                'formula': '{entity}_grid_size = {entity}_grid_size',
                'visibility': 'plan',
                'for_summary': 'No',
                'id': 'operator_2_world_heading',
            },
            {
                'formula': (
                    "{entity}_objective = 'Objective: Find the key and then use"
                    " it to open the chest at (2,3).'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'id': 'operator_3_world_heading',
            },
        ],
        'updates': [
            {
                'formula': (
                    'agent_score = -1 if agent_hit_wall else 2 if'
                    ' agent_chest_opened else 1 if agent_key_found else 0'
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_1_agent_updates',
            },
            {
                'formula': (
                    'agent_average_score = (agent_average_score * (world_time -'
                    ' 1) + agent_score) / world_time'
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_2_agent_updates',
            },
        ],
        'road': [
            {
                'formula': (
                    "agent_message = 'Observations: ' + "
                    # Current position
                    "('Current: ' + "
                    'agent_tiles.get((agent_position_x, agent_position_y),'
                    " 'empty').capitalize() + "
                    "(' (' + agent_object_map.get((agent_position_x,"
                    " agent_position_y ), 'none').capitalize() + ')' "
                    'if agent_object_map.get((agent_position_x,'
                    " agent_position_y), 'none') != 'none' else '') + '. ') + "
                    # East
                    "('East: ' + "
                    'agent_tiles.get((agent_position_x + 1, agent_position_y),'
                    " 'empty').capitalize() + "
                    "(' (' + agent_object_map.get((agent_position_x + 1,"
                    " agent_position_y), 'none').capitalize() + ')' "
                    'if agent_object_map.get((agent_position_x + 1,'
                    " agent_position_y), 'none') != 'none' else '') + '. ') + "
                    # West
                    "('West: ' + "
                    'agent_tiles.get((agent_position_x - 1, agent_position_y),'
                    " 'empty').capitalize() + "
                    "(' (' + agent_object_map.get((agent_position_x - 1,"
                    " agent_position_y), 'none').capitalize() + ')' "
                    'if agent_object_map.get((agent_position_x - 1,'
                    " agent_position_y), 'none') != 'none' else '') + '. ') + "
                    # North (new)
                    "('North: ' + "
                    'agent_tiles.get((agent_position_x, agent_position_y - 1),'
                    " 'empty').capitalize() + "
                    "(' (' + agent_object_map.get((agent_position_x,"
                    " agent_position_y - 1), 'none').capitalize() + ')' "
                    'if agent_object_map.get((agent_position_x,'
                    " agent_position_y - 1), 'none') != 'none' else '') + '."
                    " ') + "
                    # South (new)
                    "('South: ' + "
                    'agent_tiles.get((agent_position_x, agent_position_y + 1),'
                    " 'empty').capitalize() + "
                    "(' (' + agent_object_map.get((agent_position_x,"
                    " agent_position_y + 1), 'none').capitalize() + ')' "
                    'if agent_object_map.get((agent_position_x,'
                    " agent_position_y + 1), 'none') != 'none' else '') + '.')"
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_1_agent_road',
            },
        ],
        'chest': [
            {
                'formula': (
                    "agent_message = agent_message + (' Chest already opened.'"
                    " if agent_chest_opened else (' Cannot open chest without"
                    " key.' if not agent_key_found else ' Chest opened!'))"
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_1_agent_chest',
            },
            {
                'formula': (
                    'agent_chest_opened = True if agent_key_found and not'
                    ' agent_chest_opened else agent_chest_opened'
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_2_agent_chest',
            },
        ],
        'key': [
            {
                'formula': (
                    "agent_message = agent_message + (' Already picked up the"
                    " key here.' if agent_key_found else ' Key found!')"
                ),
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_1_agent_key',
            },
            {
                'formula': 'agent_key_found = True',
                'visibility': 'x',
                'for_summary': 'No',
                'id': 'operator_2_agent_key',
            },
        ],
        'tile_selector': [
            {
                'formula': 'hidden_op = ""',
                'visibility': 'hidden',
                'for_summary': 'No',
                'id': 'operator_1_agent_tile_selector',
                'next': (
                    "'operator_1_agent_road' if"
                    ' (agent_tiles.get((agent_position_x,'
                    " agent_position_y)) == 'road') else"
                    " 'operator_1_agent_updates'"
                ),
            },
        ],
        'road_object_selector': [
            {
                'formula': 'hidden_op = ""',
                'visibility': 'hidden',
                'for_summary': 'No',
                'id': 'operator_1_agent_road_object_selector',
                'next': (
                    "'operator_1_agent_key' if"
                    ' (agent_object_map.get((agent_position_x,'
                    " agent_position_y)) == 'key') else"
                    " 'operator_1_agent_chest' if"
                    ' (agent_object_map.get((agent_position_x,'
                    " agent_position_y)) == 'chest') else"
                    " 'operator_1_agent_updates'"
                ),
            },
        ],
        'return': [
            {
                'formula': 'hidden_op = ""',
                'visibility': 'hidden',
                'for_summary': 'No',
                'id': 'operator_1_agent_return',
                'next': 'operator_1_agent_updates',
            },
        ],
        'messages': [
            {
                'formula': 'blank',
                'visibility': 'plan',
                'for_summary': 'Yes',
                'experience': True,
                'id': 'operator_1_agent_messages',
            },
        ],
    },
}
