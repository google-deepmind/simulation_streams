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

"""Simulator and Entity-Component-System (ECS) utilities."""

import copy
import re

import numpy as np
from simulation_streams import evaluator


evaluator = evaluator.evaluator


def read_context(history, query, current_state):
  """A function for putting together the context before sampling.

  Args:
    history:
    query:
    current_state:

  Returns:
    A string with the relevant context.

  """
  max_context_length = current_state.get('max_context_length', 1000000)

  if query is None:
    return ''

  expanded_query = {}
  for k, v in query.items():
    if isinstance(v, str):
      expanded_query[k] = current_state.get(v, v)
    else:
      expanded_query[k] = v

  context = query_history(history, **expanded_query)

  # Check if truncation will occur
  is_truncated = len(context) > max_context_length
  # Apply the cut-off
  truncated_context = context[-max_context_length:]

  # Add truncation notice if needed
  if is_truncated:
    truncation_notice = (
        '[Note: The following history has been truncated due to length'
        ' constraints and can, due to this, start mid-turn.]\n\n'
    )
    return truncation_notice + truncated_context

  return truncated_context


def query_history(history, **kwargs):
  """Quering history for a sub-stream satisfying the kwargs.

  Args:
    history: The history being queried.
    **kwargs: The query

  Returns:
    A string with the relevant sub-stream.

  """
  results = []
  for step in history:
    match = all(
        step['state'].get(k) == v
        if not isinstance(v, list)
        else step['state'].get(k) in v
        for k, v in kwargs.items()
    )
    if match:
      results.extend(step['output'])
  context = '\n'.join(results)
  return context.rstrip('\n') + '\n'


def run_formula(state, formula_data, max_attempts, sampling, history,
                task_name=''):
  """Runs a given formula to update the state."""
  formula = formula_data['formula']
  state['state'] = state
  output = []

  if 'prompt' in formula_data:
    prompt_value = formula_data['prompt']
    prompt = state.get(prompt_value, prompt_value)
  else:
    prompt = state['prompt']

  use_lm_setting = formula_data.get('use_lm', False)
  if isinstance(use_lm_setting, str):
    try:
      s = evaluator(task_name)
      s.names = state
      use_lm_setting = s.eval(use_lm_setting)
    except Exception as e:  # pylint: disable=broad-exception-caught
      print(f'Failed to evaluate use_lm expression: {e}')
      use_lm_setting = False

  if isinstance(use_lm_setting, bool):
    use_default = not use_lm_setting
    use_lm_active = use_lm_setting
  elif callable(use_lm_setting):
    use_default = not use_lm_setting(state)
    use_lm_active = not use_default
  else:
    use_default = True
    use_lm_active = False

  attempts = 0
  default_assignment = ''
  error_occurred = False
  last_generated_text = ''
  error_message = ''

  if not use_default:
    default_assignment = formula.split('=')[0].strip()
    rhs_default = formula.split('=', 1)[1].strip() if '=' in formula else None
    if rhs_default is not None:
      try:
        s = evaluator(task_name)
        s.names = state
        default_value = s.eval(rhs_default)
        if isinstance(default_value, (int, float)):
          expected_type = 'number'
        elif isinstance(default_value, bool):
          expected_type = 'bool'
        else:
          expected_type = type(default_value).__name__
      except Exception as e:  # pylint: disable=broad-exception-caught
        print(
            f'Error evaluating Right-Hand-Side (RHS) in formula: {formula}.'
            f' Reason: {e}'
        )
        expected_type = 'str'
    else:
      expected_type = 'str'

    context = (
        read_context(history, formula_data.get('query', None), state)
        if formula_data.get('query')
        else ''
    )

    while attempts < max_attempts:
      print('attempt' + str(attempts) + ' of ' + str(max_attempts))
      sample_mode = state.get('sample_mode', 'full')

      # Add feedback to the prompt if this is a resampling attempt
      if error_occurred:
        prompt += (
            '\nFeedback: You already tried (generated text:'
            f' {last_generated_text}) and got the following error:'
            f' {error_message}. \nPlease adjust and try again, making sure to'
            ' closely follow the format of the example from the previous'
            ' block, do not use apostrophes within strings but skip them or'
            ' use a * instead, which avoids unterminated string errors in the'
            ' special setting used here.'
        )

      if sample_mode == 'full':
        sampled_formula = sampling(
            prompt,
            context,
            default_assignment,
            state.get(default_assignment, 'Unknown'),
        )
      else:  # rhs_only mode
        context_with_lhs = context + default_assignment + ' = '
        right_hand_side = sampling(
            prompt,
            context_with_lhs,
            default_assignment,
            state.get(default_assignment, 'Unknown'),
            mode='rhs_only',
        )
        sampled_formula = default_assignment + ' = ' + right_hand_side

      last_generated_text = sampled_formula  # Store the last generated text

      if sampled_formula.startswith(default_assignment):
        try:
          s = evaluator(task_name)
          s.names = state
          value = s.eval(sampled_formula.split('=', 1)[1].strip())
          is_number = expected_type in [
              'number', 'int', 'int64', 'float'
          ] and isinstance(value, (int, float, np.number))
          is_bool = expected_type == 'bool' and isinstance(value, bool)
          is_str = expected_type == 'str' and isinstance(value, str)
          is_tuple = expected_type == 'tuple' and isinstance(value, tuple)
          is_list = expected_type == 'list' and isinstance(value, list)
          is_dict = expected_type == 'dict' and isinstance(value, dict)

          if is_number or is_bool or is_str or is_tuple or is_list or is_dict:
            state[default_assignment] = value
            if isinstance(value, (str, tuple, list, dict)):
              output_value = f'{default_assignment} = {repr(value)}'
            else:
              output_value = f'{default_assignment} = {value}'
            output.append(
                output_value + (' # sampled' if use_lm_active else '')
            )
            break
          else:
            error_message = (
                f'Type mismatch: Expected {expected_type}, got '
                f'{type(value).__name__}.'
            )
            print(error_message)
            error_occurred = True
        except Exception as e:  # pylint: disable=broad-exception-caught
          error_message = f'Error evaluating sampled formula. Reason: {e}. '
          print(error_message)
          error_occurred = True
      else:
        error_message = (
            'The response did not follow the expected pattern, which is a'
            ' one-line python assignment formula as in the example from the'
            ' previous block with the same left-hand side'
            f' ({default_assignment}). Do not otherwise communicate, only'
            ' generate a one-line python formula inside single quations (no'
            ' escape characters are required) and if the right-hand side is a'
            ' string then use double quotes for the string and avoid'
            ' apostrophes within it (skip them or use * instead).'
        )
        print(error_message)
        error_occurred = True

      attempts += 1
  else:
    if formula != 'blank':
      try:
        lhs, rhs = formula.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        s = evaluator(task_name)
        s.names = state
        value = s.eval(rhs)

        if "['" in lhs:
          keys = re.findall(r"\['(.*?)'\]", lhs)
          current_dict = state
          for key in keys[:-1]:
            if key not in current_dict:
              current_dict[key] = {}
            current_dict = current_dict[key]
          current_dict[keys[-1]] = value
        else:
          state[lhs] = value

        if isinstance(value, str):
          output_value = f'{lhs} = "{value}"'
        else:
          output_value = f'{lhs} = {value}'

        output.append(output_value + (' # sampled' if use_lm_active else ''))
      except Exception as first:  # pylint: disable=broad-exception-caught
        print(f'Error executing formula: {formula}. Reason: {first}')
    else:
      output.append('# \n')

  if attempts >= max_attempts:
    value = state.get(default_assignment, 'Unknown')
    if isinstance(value, str):
      output_value = f"{default_assignment} = '{value}'"
    else:
      output_value = f'{default_assignment} = {value}'
    output.append(output_value + (' # sampled' if use_lm_active else ''))

  return state, output


def simulation_stream_generator(
    initial_state, operators, first_operator, max_attempts=3, sampling=None,
    task_name=''):
  """Generates a sequence of states by applying operators from a given list.

  Args:
      initial_state: The initial values
      operators: The list of operators that transforms the state
      first_operator: The operator to start with
      max_attempts: The number of attempts to reach a compliant sample .
      sampling: The sampling function used.
      task_name: The name of the task to load task functions for.

  Yields:
      New states
  """
  state = initial_state.copy()
  state['np'] = np  # If you need numpy
  state['sampling'] = sampling

  history = []  # Maintain the running history within this generator

  current_operator_id = first_operator  # Start with the first formula

  while True:
    formula_data = next(
        item for item in operators if item['id'] == current_operator_id
    )

    # Update state with formula data's properties
    for key, value in formula_data.items():
      if key not in ['id', 'formula', 'next']:
        state[key] = value

    state, output = run_formula(
        state, formula_data, max_attempts, sampling, history, task_name
    )

    # Append to the history and then yield the current step's data
    current_step_data = {
        'state': state.copy(),
        'output': output,
        'operator_id': current_operator_id,
    }
    history.append(current_step_data)

    yield current_step_data

    if ' if ' in f' {formula_data["next"]} ':
      # Contains a proper if statement with spaces
      expression = formula_data['next'].strip()
      s = evaluator()
      s.names = state
      current_operator_id = s.eval(expression)
    else:
      # No conditional logic, use the string value directly
      current_operator_id = formula_data['next']


def generate_simulation_stream(
    initial_state,
    operators,
    first_operator,
    max_attempts=3,
    sampling=None,
    end_time=25,):
  """Runs the simulation_stream_generator.

  Args:
      initial_state: The initial values.
      operators: The operators that transform the state.
      first_operator: The operator to start with.
      max_attempts: The number of attempts at sampling a compliant formula.
      sampling: The sampling function used.
      end_time: The `world_time` value at which the simulation should end.

  Returns:
      A list of states generated by the simulation.
  """
  initial_state = copy.deepcopy(initial_state)
  gen = simulation_stream_generator(
      initial_state, operators, first_operator, max_attempts, sampling
  )

  stream = []
  while True:
    current_step_data = next(gen)
    stream.append(current_step_data)

    if current_step_data['state']['world_time'] >= end_time:
      break

  return stream


def preprocess_systems_definitions(systems_definitions):
  """Preprocess systems_definitions to ensure it has the required structure.

  Args:
      systems_definitions: Incomplete systems definitions

  Returns:
      processed_systems_definitions: Completed systems using defaults
  """
  processed_systems_definitions = {}

  for system, components in systems_definitions.items():
    processed_components = []

    for component in components:
      formula = component.get('formula', '')
      query = component.get('query', None)
      use_lm = component.get('use_lm', False)
      processed_component = {
          'formula': formula,
          'query': query,
          'use_lm': use_lm,
      }
      # Add any other fields from component into processed_component
      for key, value in component.items():
        if key not in ['formula', 'query', 'use_lm']:
          processed_component[key] = value
      processed_components.append(processed_component)

    processed_systems_definitions[system] = processed_components

  return processed_systems_definitions


def is_callable_expression(value):
  """Check if a string looks like a callable expression."""
  return isinstance(value, str) and re.match(
      r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)$', value.strip()
  )


def generate_operators(
    entities,
    variables,
    systems_definitions,
    world_entity_name='world',
    task_name='',
    default_values=None,
):
  """Generates operators and initial_state for the history generator."""
  if default_values is None:
    default_values = {}

  systems_definitions = preprocess_systems_definitions(systems_definitions)
  s = evaluator(task_name)

  # Initialize state dictionary and make it self-referential
  state = {}
  state['state'] = state  # Make state a member of itself
  s.names = state  # Add state to evaluator's namespace

  # Components
  components = {}
  for entity, entity_variables in entities.items():
    for variable in entity_variables:
      for component_name, initial_value in variables[variable].items():
        full_component_name = f'{entity}_{component_name}'
        if is_callable_expression(initial_value):
          print('initial_value from function: ' + initial_value)
          try:
            evaluated_value = s.eval(initial_value)
            components[full_component_name] = evaluated_value
          except Exception as e:  # pylint: disable=broad-exception-caught
            print(f'Error evaluating {full_component_name}: {str(e)}')
            components[full_component_name] = initial_value
        else:
          # If it's not a callable expression, use the value as is
          components[full_component_name] = initial_value

  # Update state with components
  state.update(components)

  # Systems
  world_entity = world_entity_name

  # Iterate over the entities and their associated variables (systems)
  all_systems = []
  for entity, entity_variables in entities.items():
    entity_systems = []
    for variable in entity_variables:
      formulas = None
      if variable in systems_definitions:
        print(f'Systems_definitions applied for {variable}!')
        formulas = systems_definitions[variable]
        print(formulas)
      elif variable in s.functions:
        print('Programatic systems_definitions applied for {variable}!')
        try:
          system_generator = s.functions[variable]
          generated_systems = system_generator()
          if isinstance(generated_systems, (list, tuple)):
            formulas = generated_systems
          else:
            formulas = [generated_systems]
        except Exception as e:  # pylint: disable=broad-exception-caught
          print(f'Error generating systems for {variable}: {str(e)}')

      if formulas:
        for i, formula_dict in enumerate(formulas):
          if i == 0:
            op_id = f'operator_1_{entity}_{variable}'
          else:
            op_id = formula_dict.get(
                'id', f'operator_{i+1}_{entity}_{variable}'
            )

          formula = formula_dict['formula'].replace('{entity}', entity)
          formula = formula.replace('{world_entity}', world_entity)
          operator = {
              'id': op_id,
              'formula': formula,
              'query': formula_dict.get('query'),
              'use_lm': formula_dict.get('use_lm', False),
          }
          # Add any other fields from formula_dict into operator
          for key, value in formula_dict.items():
            if key not in ['formula', 'query', 'use_lm']:
              operator[key] = value
          for default_key, default_value in default_values.items():
            if default_key not in operator:
              operator[default_key] = default_value
          entity_systems.append(operator)
    all_systems.extend(entity_systems)

  # Determine the 'next' operators
  for i, operator in enumerate(all_systems):
    if 'next' not in operator:
      if i < len(all_systems) - 1:
        operator['next'] = all_systems[i + 1]['id']
      else:
        operator['next'] = all_systems[0]['id']

  # Update state with default values
  state.update({
      'agent_index': 0,
      'prompt': '',
      'max_context_length': 1000000,
      'sample_mode': 'full',
      'all': True,
  })
  return all_systems, state
