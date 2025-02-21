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

"""Task functions for the key-chest environment."""

import random


def get_tile_map(the_grid_size: int = 5):
  """Initialize and return the tile map."""
  tile_map = {}
  for x in range(-1, the_grid_size + 1):
    for y in range(-1, the_grid_size + 1):
      if x == -1 or x == the_grid_size or y == -1 or y == the_grid_size:
        tile_map[(x, y)] = 'wall'
      else:
        tile_map[(x, y)] = 'road' if random.random() > 0.2 else 'wall'
  return tile_map


def get_object_map(the_grid_size: int = 5, index: int = 0):
  """Initialize object map, place key and chest, and return the result."""
  object_map = {}
  for x in range(the_grid_size):
    for y in range(the_grid_size):
      object_map[(x, y)] = 'empty'
  keys_x = [4, 1, 4, 0, 4, 3, 3, 1, 3, 2]
  keys_y = [1, 3, 3, 4, 1, 0, 3, 3, 1, 4]
  chest_x, chest_y = 2, 3
  key_x, key_y = keys_x[index], keys_y[index]
  object_map[(key_x, key_y)] = 'key'
  object_map[(chest_x, chest_y)] = 'chest'
  return object_map

key_chest_functions = {
    'tile_map': get_tile_map,
    'object_map': get_object_map,
}
