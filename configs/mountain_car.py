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

"""Config for Simulation of an agent running a mountain car task."""

ecs_config = {
    'entities': {
        'world': ['heading'],
        'car': [
            'history_log',
            'planning',
            'movement',
            'updates',
            'messages',
        ],
    },
    'variables': {
        'movement': {
            'position': -0.5,
            'velocity': 0.0,
            'acceleration': 0.0,
            'force': 0.0,
        },
        'heading': {
            'time': 0,
        },
        'updates': {
            'goal_position': 0.5,  # The position the car needs to reach
            'score': 0.0,
            'average_score': 0.0,
        },
        'planning': {'revision_response': 'No'},
        'history_log': {'history': 'Start. ', 'message': ''},
        'distance_to_target': {},
        'analysis': {},
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
        'updates': [
            {
                'formula': 'car_distance_to_target = abs(car_position - 0.5)',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'car_score = 1 if car_position >= car_goal_position else'
                    ' car_score'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'car_score = car_score',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'car_average_score = (car_average_score * (world_time - 1)'
                    ' + car_score) / world_time'
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
                'experience': True,
            },
        ],
        'planning': [
            {
                'formula': (
                    'planning_instruction = "Consider the cars past'
                    " developments and in particular the assistants"
                    ' knowledge, make a high-level plan for how to achieve the'
                    ' objective."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_high_level_plan = "The car should try'
                    ' accelerating towards the goals, but if the hill makes the'
                    ' car reverse down before reaching the goal, accelerate in'
                    ' the other direction and up the other hill in the same way'
                    ' gathering momentum and then reverse back forward and use'
                    ' it to reach up to the goal."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "car_revision_response.lower().startswith('y')",
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
                    'assistant_algorithmic_outline = "First use Force 1 forward'
                    ' until velocity decreases towards turning negative due to'
                    ' the uphill, then reverse the Force to -1 to head up the'
                    ' other side and gather momentum until the hill makes the'
                    ' velocity increase towards turning positive again, and'
                    ' then back to +1 to head up to the goal."'
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
                    'assistant_execution_plan = "The car should use Force 1'
                    ' forward until velocity decreases towards turning negative'
                    ' due to the uphill."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
        ],
        'history_log': [
            {
                'formula': 'car_message = car_message',
                'visibility': 'plan',
                'for_summary': 'True',
            },
            {
                'formula': 'car_message = ""',
                'visibility': 'hidden',
                'for_summary': 'False',
            },
            {
                'formula': (
                    "car_history = car_history + 'Time ' + str(world_time) + ':"
                    " Position: ' + str(round(car_position, 2)) + ', Velocity:"
                    " ' + str(round(car_velocity, 2)) + '; Acceleration: ' +"
                    " str(round(car_acceleration, 2)) + '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "car_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Position: ' +"
                    " str(round(car_position, 2)) + ', Velocity: ' +"
                    " str(round(car_velocity, 2)) + ', Acceleration: ' +"
                    " str(round(car_acceleration, 2)) + '.'"
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
                    "assistant_knowledge = 'The car is at position ' +"
                    " str(round(car_position, 2)) + ' in a task where an"
                    ' underpowered car is trying to get up a hill in front of'
                    ' the car. There is also a hill behind the car. The car is'
                    ' aiming to get to position +0.5 and has not yet reached'
                    " this goal. Its velocity is ' + str(round(car_velocity,"
                    " 2)) +  ' and acceleration is ' +"
                    " str(round(car_acceleration, 2)) + ', and it is unlikely"
                    " to have the power to go straight up to the goal.'"
                ),
                'visibility': 'plan',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': (
                    'revision_question = "Given the recent events and '
                    'developments, should the high-level plan and its '
                    'algorithmic outline be revised (Yes/No)?"'
                ),
                'visibility': 'x',
                'for_summary': 'Yes',
            },
            {
                'formula': 'car_revision_response = car_revision_response',
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
        ],
        'movement': [
            {
                'formula': (
                    "control_instruction = 'Choose the force, according to the"
                    ' plan to accelerate the car with so as to get to the goal'
                    " at position=+0.5 (height 1.0).'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': 'car_force = 1',
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': 'car_force = max(-1, min(1, car_force))',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'car_acceleration = car_force * 0.1 - 0.25 * np.cos(3 *'
                    ' car_position)'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'car_velocity = car_velocity + car_acceleration',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'car_position = car_position + car_velocity',
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': 'car_height_in_hill = np.sin(3 * car_position)',
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
    },
}
