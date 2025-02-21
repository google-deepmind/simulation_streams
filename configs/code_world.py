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

"""Configuration for the Code World environment."""

ecs_config = {
    "entities": {
        "world": ["header"],
        "agent": [
            "history_log",
            "planning",
            "action",
            "updates",
            "messages",
        ],
    },
    "variables": {
        "header": {
            "init": "initialize_default_state(state)",
            "time": 0,
        },
        "action": {},
        "updates": {},
        "history_log": {
            "history": "Start. ",
            "message": "",
            "current_status": "",
        },
        "planning": {
            "revision_response": "No",
        },
        "messages": {},
        "state": {},
    },
    "systems_definitions": {
        "updates": [
            {
                "formula": "update = update_state(state)",
                "visibility": "x",
                "for_summary": "No",
            },
            {
                "formula": "agent_score = agent_score",
                "visibility": "x",
                "for_summary": "Yes",
            },
        ],
        "header": [
            {
                "formula": "world_time = world_time + 1",
                "visibility": "plan",
                "for_summary": "Yes",
            },
        ],
        "planning": [
            {
                "formula": (
                    "agent_planning_instruction = agent_planning_instruction"
                ),
                "visibility": "plan",
                "for_summary": "No",
            },
            {
                "formula": "agent_high_level_plan = agent_high_level_plan",
                "visibility": "plan",
                "for_summary": "No",
                "use_lm": "agent_revision_response.lower().startswith('y')",
            },
            {
                "formula": (
                    "agent_planning_algorithmic_instruction ="
                    " agent_planning_algorithmic_instruction"
                ),
                "visibility": "plan",
                "for_summary": "No",
            },
            {
                "formula": (
                    "agent_algorithmic_outline = agent_algorithmic_outline"
                ),
                "use_lm": "world_time > 1",
            },
            {
                "formula": (
                    "agent_planning_execution_instruction ="
                    " agent_planning_execution_instruction"
                ),
                "visibility": "plan",
                "for_summary": "No",
            },
            {
                "formula": "agent_execution_plan = agent_execution_plan",
                "visibility": "plan",
                "for_summary": "No",
                "query": {"visibility": "plan"},
                "use_lm": "world_time > 1",
            },
        ],
        "history_log": [
            {
                "formula": "agent_history = update_history(state)",
                "visibility": "hidden",
                "for_summary": "Yes",
            },
            {
                "formula": (
                    "agent_current_status = update_current_status(state)"
                ),
                "visibility": "plan",
                "for_summary": "Yes",
            },
            {
                "formula": (
                    "agent_summary_instruction = agent_summary_instruction"
                ),
                "visibility": "x",
                "for_summary": "Yes",
            },
            {
                "formula": "agent_knowledge = agent_knowledge",
                "visibility": "plan",
                "for_summary": "Yes",
                "query": {"for_summary": "Yes"},
                "use_lm": "world_time > 1",
            },
            {
                "formula": (
                    "revision_question = 'Based on recent events, should the"
                    " high-level plan and its algorithmic outline be revised"
                    " (Yes/No)?'"
                ),
                "visibility": "x",
                "for_summary": "Yes",
            },
            {
                "formula": "agent_revision_response = agent_revision_response",
                "visibility": "x",
                "for_summary": "Yes",
                "query": {"for_summary": "Yes"},
                "use_lm": "world_time > 1",
            },
        ],
        "action": [
            {
                "formula": (
                    "agent_control_instruction = agent_control_instruction"
                ),
                "visibility": "plan",
                "for_summary": "No",
            },
            {
                "formula": "agent_action = agent_action",
                "visibility": "plan",
                "for_summary": "No",
                "query": {"visibility": "plan"},
                "use_lm": "world_time > 1",
            },
            {
                "formula": "agent_action = take_action(state)",
                "visibility": "x",
                "for_summary": "No",
            },
        ],
        "messages": [
            {
                "formula": "blank",
                "visibility": "plan",
                "for_summary": "Yes",
                "experience": True,
            },
        ],
    },
}
