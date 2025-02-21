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

"""Functions to evaluate expressions in simulation streams."""

import builtins
import math
import random
import statistics

from simpleeval import EvalWithCompoundTypes
import task_functions

task_functions = task_functions.task_functions


def evaluator(task_name=None):
  """A function to create a safe evaluator for simple single expression."""
  s = EvalWithCompoundTypes()
  if task_name in task_functions:
    task_funcs = task_functions[task_name]
    s.functions.update(task_funcs)

  # Math functions
  math_functions = [
      'ceil',
      'floor',
      'sqrt',
      'exp',
      'log',
      'log10',
      'sin',
      'cos',
      'tan',
      'asin',
      'acos',
      'atan',
      'degrees',
      'radians',
      'pi',
      'e',
  ]
  for func in math_functions:
    s.functions[func] = getattr(math, func)

  # Built-in functions
  builtin_functions = [
      'abs',
      'round',
      'min',
      'max',
      'sum',
      'len',
      'sorted',
      'enumerate',
      'zip',
      'any',
      'all',
      'filter',
      'map',
      'str',
      'int',
      'float',
      'bool',
  ]
  for func in builtin_functions:
    s.functions[func] = getattr(builtins, func)

  # String methods as functions
  string_methods = [
      'lower',
      'upper',
      'title',
      'capitalize',
      'strip',
      'lstrip',
      'rstrip',
      'replace',
      'split',
      'join',
      'startswith',
      'endswith',
      'find',
      'count',
  ]
  for method in string_methods:
    s.functions[method] = lambda *args, method=method: getattr(
        str(args[0]), method
    )(*args[1:])

  # Random functions
  s.functions['random'] = random.random
  s.functions['randint'] = random.randint

  # Statistics functions
  statistics_functions = ['mean', 'median', 'mode', 'stdev', 'variance']
  for func in statistics_functions:
    s.functions[func] = getattr(statistics, func)

  return s
