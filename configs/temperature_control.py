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

"""Config for Simulation of an agent running a Temperature_control task."""

ecs_config = {
    'entities': {
        'world': ['heading'],
        'control': [
            'history_log',
            'planning',
            'adjustment',
        ],
        'end': ['messages'],
    },
    'variables': {
        'heading': {
            'time': 0,
            'temperature': 22.5,
            'cooling_power': 0,
            'max_cooling_power': 5,
            'max_external_heat': 3,
            'external_heat': 0,
            'average_score': 0,
            'objective': '',
            'score': 0,
        },
        'analysis': {'analysis': ''},
        'planning': {'revision_response': 'No'},
        'history_log': {'history': 'Start. ', 'message': ''},
        'adjustment': {'adjustment': 0},
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
                'formula': 'increment_value = randint(0, 2)-1',
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_external_heat = min(world_max_external_heat, max(1,'
                    ' world_external_heat + increment_value))'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_temperature = world_temperature +'
                    ' world_external_heat - world_cooling_power'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'control_objective = "The goal is to keep temperature near'
                    ' 22.5, which yields the highest score"'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_score = max(0, -abs(world_temperature - 22.5) + 5)'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_average_score = (world_average_score * (world_time -'
                    ' 1) + world_score) / world_time'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
        ],
        'planning': [
            {
                'formula': (
                    'planning_instruction = "Consider the past'
                    " developments and in particular the assistant"
                    ' knowledge, make a high-level plan for how to achieve the'
                    ' objective."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'assistant_high_level_plan = "Increase cooling if the'
                    ' temperature is too high and decrease if too low."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'use_lm': "control_revision_response.lower().startswith('y')",
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
                    'assistant_algorithmic_outline = "Increase cooling by 1 if'
                    ' the temperature is above 24, decrease by 1 if the'
                    ' temperature is below 22. However, do not increase cooling'
                    ' if the temperature is already falling rapidly and do not'
                    ' decrease cooling if the temperature is already rising'
                    ' rapidly. Do not adjust cooling if the temperature is'
                    ' stable near 22.5."'
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
                    'assistant_execution_plan = "As the temperature is near'
                    ' ideal (22.5) and not rapidly changing, do not adjust'
                    ' cooling at this step."'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
        ],
        'adjustment': [
            {
                'formula': (
                    "control_adjustment_instruction = 'Choose the adjustment"
                    ' for the cooling according to your plan for meeting the'
                    " objective.'"
                ),
                'visibility': 'plan',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'control_adjustment = 1 if world_temperature > 24.0'
                    ' else -1 if world_temperature < 21.0 else 0'
                ),
                'visibility': 'plan',
                'for_summary': 'No',
                'query': {'visibility': 'plan'},
                'use_lm': 'world_time > 1',
            },
            {
                'formula': (
                    'control_adjustment = max(-1, min(1, control_adjustment))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_cooling_power = world_cooling_power +'
                    ' control_adjustment'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
            {
                'formula': (
                    'world_cooling_power = max(0, min(5, world_cooling_power))'
                ),
                'visibility': 'x',
                'for_summary': 'No',
            },
        ],
        'history_log': [
            {
                'formula': 'control_message = control_message',
                'visibility': 'plan',
                'for_summary': 'True',
            },
            {
                'formula': 'control_message = ""',
                'visibility': 'hidden',
                'for_summary': 'False',
            },
            {
                'formula': (
                    "control_history = control_history + 'Time ' +"
                    " str(world_time) + ': Temperature: ' +"
                    " str(round(world_temperature, 2)) + ', Cooling Power: ' +"
                    " str(round(world_cooling_power, 2)) + '; External Heat: '"
                    " + str(round(world_external_heat, 2)) + '; '"
                ),
                'visibility': 'hidden',
                'for_summary': 'Yes',
            },
            {
                'formula': (
                    "control_current_status = 'Current Status at Time ' +"
                    " str(world_time) + ': Temperature: ' +"
                    " str(round(world_temperature, 2)) + ', Cooling Power: ' +"
                    " str(round(world_cooling_power, 2)) + ', External Heat: '"
                    " + str(round(world_external_heat, 2)) + '.'"
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
                    "assistant_knowledge = 'The temperature is currently ' +"
                    " str(round(world_temperature, 2)) + ' and stable due to no"
                    " substantial external heat of ' +"
                    " str(round(world_external_heat, 2)) + ' degrees. Cooling"
                    ' power is an appropriate response to maintain temperature'
                    ' stability. The simulation has just started so there is no'
                    " history to analyze.'"
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
                'formula': (
                    'control_revision_response = control_revision_response'
                ),
                'visibility': 'x',
                'for_summary': 'Yes',
                'query': {'for_summary': 'Yes'},
                'use_lm': 'world_time > 1',
            },
        ],
    },
}
