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

"""A collection of task functions for various environments."""

from all_task_functions import key_chest_functions
from all_task_functions import maze_functions
from all_task_functions import mountain_car_functions

key_chest_functions = key_chest_functions.key_chest_functions
maze_functions = maze_functions.maze_functions
mountain_car_functions = mountain_car_functions.mountain_car_functions


task_functions = {
    'key_chest': key_chest_functions,
    'mountain_car': mountain_car_functions,
    'maze': maze_functions,
}
