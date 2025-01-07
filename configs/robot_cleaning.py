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

"""Config for robot cleaning task."""

ecs_config = {
    'entities': {
        'world': [
            'heading',
        ],
        'robot': [
            'history_log',
            'planning',
            'move',
            'updates',
            'messages',
        ],
    },
    'variables': {
        'heading': {
            'width': 5,
            'height': 5,
            'obstacles': [
                (2, 2),
                (3, 1),
            ],
            'dirty_spots': [
                (1, 1),
                (3, 3),
                (4, 2),
            ],
            'cleaned_spots': [
            ],
            'time': 0,
        },
        'move': {
            'position_x': 0,
            'position_y': 0,
            'move_x': 0,
            'move_y': 0,
        },
        'updates': {
            'distance': 0,
            'score': 0,
            'average_score': 0,
        },
        'history_log': {
            'history': 'Start. ',
            'message': 'The task has started!',
        },
        'planning': {
            'revision_response': 'No',
        },
        'messages': {

        },
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
        'updates': [
            {
                'formula': (
                    'world_cleaned_spots = world_cleaned_spots +'
                    ' [(robot_position_x, robot_position_y)] if'
                    ' (robot_position_x, robot_position_y) in world_dirty_spots'
                    ' else world_cleaned_spots'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_dirty_spots = [spot for spot in world_dirty_spots if'
                    ' spot != (robot_position_x, robot_position_y)]'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'robot_score_cleaning = len(world_cleaned_spots)',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_obstacle_penalty = 5 if (robot_position_x,'
                    ' robot_position_y) in world_obstacles else 0'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_score = robot_score_cleaning -'
                    ' robot_obstacle_penalty'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_average_score = (robot_average_score * (world_time -'
                    ' 1) + robot_score) / world_time'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'heading': [
            {
                'formula': 'world_time = world_time + 1',
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "world_room_state = 'Room dimensions: ' + str(world_width)"
                    " + 'x' + str(world_height) +'. Obstacles: ' + ',"
                    " '.join(['(' + str(x) + ', ' + str(y) + ')' for x, y in"
                    " world_obstacles]) +'. Dirty spots: ' + ', '.join(['(' +"
                    " str(x) + ', ' + str(y) + ')' for x, y in"
                    " world_dirty_spots]) +'. Cleaned spots: ' +"
                    " str(len(world_cleaned_spots)) + ' spots.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "robot_objective_description = 'Clean all the dirty spots"
                    " without hitting the obstacles.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
        ],
        'planning': [
            {
                'formula': (
                    'planning_instruction = "Consider the robots past'
                    ' developments and in particular the assistants knowledge,'
                    ' make a high-level for how to achieve the objective."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "assistant_high_level_plan = 'The robot should aim to clean"
                    " all dirty spots while avoiding the obstacles.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "robot_revision_response.lower().startswith('y')",
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
                    "assistant_algorithmic_outline = 'First go to the dirt at"
                    ' (1,1), then head to the spot at (3,3) without hitting the'
                    ' obstacles at (2,2) and (3,1) and finally go to the last'
                    " dirty spot at (4,2). Then you are done.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': (
                    'planning_execution_instruction = "Consider the'
                    " assistants high-level and its algorithmic outline and"
                    ' plan concrete next steps from the current state. Consider'
                    ' the previous time steps execution plan and build on it."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "assistant_execution_plan = 'First go right (increase x) to"
                    ' (1,0) and then down (increase y) to the dirty spot at'
                    ' (1,1) before continuing towards the next dirty spot at'
                    " (3,3) starting with (1,2) and then (1,3).'"
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
                    "robot_movement_instruction_x = 'Choose the x-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (d,0) from (x,y) to (x+d,y)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': '{entity}_move_x = 0',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'robot_move_x = max(-1, min(1, robot_move_x))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'robot_position_x = robot_position_x + robot_move_x',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_hit_wall = (robot_position_x + robot_move_x !='
                    ' max(0, min(4, robot_position_x + robot_move_x)) or'
                    ' robot_position_y + robot_move_y != max(0, min(4,'
                    ' robot_position_y + robot_move_y)))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "robot_movement_instruction_y = 'Choose the y-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (0,d) from (x,y) to (x,y+d)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': '{entity}_move_y = 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {
                    'visibility': 'plan',
                },
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'robot_move_y = max(-1, min(1, robot_move_y))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'robot_position_y = robot_position_y + robot_move_y',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_position_x = max(0, min(4, robot_position_x))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'robot_position_y = max(0, min(4, robot_position_y))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'history_log': [
            {
                'formula': 'robot_message = robot_message',
                'visibility': 'plan',
                'for_summary': 'True',
            },
            {
                'formula': 'robot_message = ""',
                'visibility': 'hidden',
                'for_summary': 'False',
            },
            {
                'formula': (
                    "robot_history = robot_history + 'Time ' + str(world_time)"
                    " + ': Position: ' + str(round(robot_position_x, 2)) + ', '"
                    " + str(round(robot_position_y, 2)) + '; Cleaned Spots: ' +"
                    " str(len(world_cleaned_spots)) + '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "robot_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Position: ' +"
                    " str(round(robot_position_x, 2)) + ', ' +"
                    " str(round(robot_position_y, 2)) + '; Cleaned Spots: ' +"
                    " str(len(world_cleaned_spots)) + '.'"
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
                    "assistant_knowledge = 'The robot is at (0,0) in a 5x5"
                    ' gridworld with obstacles at (2,2) and (3,1) with three'
                    ' dirty spots at (1,1), (3,3) and (4,2) and nothing has'
                    " been cleaned yet.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
                'query': {
                    'for_summary': 'Yes',
                },
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
                'formula': 'robot_revision_response = robot_revision_response',
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {
                    'for_summary': 'Yes',
                },
                'use_lm': 'world_time > 1',
            },
        ],
    },
}
