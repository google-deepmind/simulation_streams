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
"""Config for Simulation of a mouse seeking cheese in a maze."""

ecs_config = {
    'entities': {
        'world': ['heading'],
        'mouse': [
            'observation',
            'history_log',
            'planning',
            'movement',
            'updates',
            'messages',
        ],
    },
    'variables': {
        'heading': {
            'time': 0,
            'grid_size': 7,
            'obstacles': 'get_maze_obstacles({index})',
        },
        'history_log': {
            'history': 'Start. ',
            'message': '',
            'smell_of_cheese': 0,
        },
        'planning': {'revision_response': 'No'},
        'movement': {
            'position_x': 'get_maze_start_x({index})',
            'position_y': 'get_maze_start_y({index})',
            'move_x': 0,
            'move_y': 0,
        },
        'updates': {
            'score': 0,
            'average_score': 0,
            'cheese_found': False,
            'cheese_x': 'get_maze_goal_position_x({index})',
            'cheese_y': 'get_maze_goal_position_y({index})',
        },
        'observation': {'observation': {}},
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
        ],
        'updates': [
            {
                'formula': (
                    'mouse_cheese_found = True if mouse_cheese_found or'
                    ' (mouse_position_x == mouse_cheese_x and mouse_position_y'
                    ' == mouse_cheese_y) else False'
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    'mouse_smell_of_cheese = round(1/np.sqrt((mouse_position_x'
                    ' - mouse_cheese_x)**2 + (mouse_position_y -'
                    ' mouse_cheese_y)**2), 2)'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'mouse_score = 1 if mouse_cheese_found else'
                    ' -mouse_hitting_wall_penalty - mouse_lazy_mouse_penalty'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'mouse_average_score = (mouse_average_score * (world_time -'
                    ' 1) + mouse_score) / world_time'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'observation': [
            {
                'formula': (
                    "current_observation = 'Observations: ' + "
                    # Current
                    "('Current (' + str(mouse_position_x) + ',' +"
                    " str(mouse_position_y) + '): Mouse. ') + "
                    # North
                    "('North (' + str(mouse_position_x) + ',' +"
                    " str(mouse_position_y - 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x, mouse_position_y - 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x,"
                    ' mouse_position_y - 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # South
                    "('South (' + str(mouse_position_x) + ',' +"
                    " str(mouse_position_y + 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x, mouse_position_y + 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x,"
                    ' mouse_position_y + 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # East
                    "('East (' + str(mouse_position_x + 1) + ',' +"
                    " str(mouse_position_y) + '): ' + ('Wall' if"
                    ' (mouse_position_x + 1, mouse_position_y) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x + 1,"
                    ' mouse_position_y) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # West
                    "('West (' + str(mouse_position_x - 1) + ',' +"
                    " str(mouse_position_y) + '): ' + ('Wall' if"
                    ' (mouse_position_x - 1, mouse_position_y) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x - 1,"
                    ' mouse_position_y) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # Northeast
                    "('Northeast (' + str(mouse_position_x + 1) + ',' +"
                    " str(mouse_position_y - 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x + 1, mouse_position_y - 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x + 1,"
                    ' mouse_position_y - 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # Northwest
                    "('Northwest (' + str(mouse_position_x - 1) + ',' +"
                    " str(mouse_position_y - 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x - 1, mouse_position_y - 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x - 1,"
                    ' mouse_position_y - 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # Southeast
                    "('Southeast (' + str(mouse_position_x + 1) + ',' +"
                    " str(mouse_position_y + 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x + 1, mouse_position_y + 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x + 1,"
                    ' mouse_position_y + 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '. ') + "
                    # Southwest
                    "('Southwest (' + str(mouse_position_x - 1) + ',' +"
                    " str(mouse_position_y + 1) + '): ' + ('Wall' if"
                    ' (mouse_position_x - 1, mouse_position_y + 1) in'
                    " world_obstacles else 'Cheese' if (mouse_position_x - 1,"
                    ' mouse_position_y + 1) == (mouse_cheese_x, mouse_cheese_y)'
                    " else 'Empty') + '.')"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
            },
        ],
        'planning': [
            {
                'formula': (
                    'planning_instruction = "Consider the mouses past'
                    " developments and in particular the assistants"
                    ' knowledge, make a high-level plan for how to achieve the'
                    ' objective."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_high_level_plan = "The mouse needs to find its'
                    ' way through the maze to find the cheese, avoiding walls'
                    ' and trying new open paths that it has not explored in the'
                    ' past. It should use a Depth-First-Search strategy."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "mouse_revision_response.lower().startswith('y')",
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
                    'assistant_algorithmic_outline = "If from where you are,'
                    ' you have not chosen a path to try, start going down an'
                    ' available untried direction and only go back if you find'
                    ' a dead end. If you are along a path and can continue, do'
                    ' so. If you hit a dead end, return to the last place where'
                    ' you had another option than the one you tried and then go'
                    ' down that unexplored path. At all times, you should have'
                    ' a preference for where the smell of cheese is stronger'
                    ' and aim to go in directions of increasing smell."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time>1',
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
                    'assistant_execution_plan = "The mouse is at (1,1) and'
                    ' should explore a path to the right starting with (1,2)'
                    ' and observe the surroundings and if possible continue to'
                    ' new locations that it has not yet visited, always avoid'
                    ' hitting the walls. Let your choice among new empty'
                    ' squares be guided by the direction in which the smell of'
                    ' cheese increases the most. If you at any point see the'
                    ' cheese, go immediately to its square."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
        ],
        'movement': [
            {
                'formula': (
                    "mouse_movement_instruction_x = 'Choose the x-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (d,0) from (x,y) to (x+d,y)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'mouse_move_x = 0',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'mouse_move_x = max(-1, min(1, mouse_move_x))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'mouse_position_x = mouse_position_x + mouse_move_x',
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'mouse_hit_wall = (mouse_position_x + mouse_move_x !='
                    ' max(0, min(world_grid_size-1, mouse_position_x +'
                    ' mouse_move_x)) or mouse_position_y + mouse_move_y !='
                    ' max(0, min(world_grid_size-1, mouse_position_y +'
                    ' mouse_move_y)))'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'mouse_hitting_wall_penalty = 0.1 if ((mouse_position_x +'
                    ' mouse_move_x, mouse_position_y + mouse_move_y) in'
                    ' world_obstacles) else 0'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    "mouse_movement_instruction_y = 'Choose the y-direction"
                    ' movement d (from -1,0 or 1) based on the plan, to move by'
                    " (0,d) from (x,y) to (x,y+d)'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'mouse_move_y = 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'mouse_move_y = max(-1, min(1, mouse_move_y))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'mouse_position_y = mouse_position_y + mouse_move_y',
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'mouse_lazy_mouse_penalty = 0.1 if (mouse_move_x,'
                    ' mouse_move_y) == (0, 0) else 0'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
        ],
        'history_log': [
            {
                'formula': (
                    "mouse_history = mouse_history + 'Time ' + str(world_time)"
                    " + ': Position: ' + str(round(mouse_position_x, 2)) + ', '"
                    " + str(round(mouse_position_y, 2)) + '; Smell of Cheese: '"
                    " + str(round(mouse_smell_of_cheese, 2)) + '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "mouse_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Position: ' +"
                    " str(round(mouse_position_x, 2)) + ', ' +"
                    " str(round(mouse_position_y, 2)) + '; Smell of Cheese: ' +"
                    " str(round(mouse_smell_of_cheese, 2)) + '; Cheese Found: '"
                    " + str(mouse_cheese_found) + '.'"
                ),
                'visibility': 'hidden',
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
                    "assistant_knowledge = 'The mouse is at (1,1) in a maze"
                    ' gridworld (1....5 x 1...5) and is very weakly smelling a'
                    ' cheese that it does not know the location of. The cheese'
                    ' has not been located (as the current status shows).'
                    ' Summary of where the mouse can go and where there are'
                    ' walls: There are walls everywhere around the mouse except'
                    ' right (1,2), down (2,1) as well as the right-down'
                    ' diagonal (2,2), that are empty. The mouse has not visited'
                    " any other locations yet.'"
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
                'formula': 'mouse_revision_response = mouse_revision_response',
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
        ],
    },
}
