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

"""Backend for ECS editor app."""

import ast
import base64
import io
import json
import os
import pathlib
import re
from typing import List, Optional

import matplotlib
import matplotlib.pyplot as plt
from simulation_streams import evaluator
from simulation_streams import sampling
from simulation_streams import simulation_utils


sampling = sampling.sampling
generate_operators = simulation_utils.generate_operators
query_history = simulation_utils.query_history
simulation_stream_generator = simulation_utils.simulation_stream_generator
evaluator = evaluator.evaluator

matplotlib.use('Agg')


def get_unique_filename(base_path):
  """Generate a unique filename."""
  path = pathlib.Path(base_path)
  if not path.exists():
    return path

  file_index = 1
  while True:
    new_path = path.with_name(f'{path.stem}_{file_index}{path.suffix}')
    if not new_path.exists():
      return new_path
    file_index += 1


def save_results_to_file(the_results, ecs_file, current_time):
  """Save the simulation results in the 'results' subdirectory."""
  # Get the directory of the current script
  script_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

  # Create 'results' directory if it doesn't exist
  results_dir = script_dir / 'results'
  results_dir.mkdir(exist_ok=True)

  # Generate the base filename for results with step and current time
  ecs_path = pathlib.Path(ecs_file)
  base_filename = f'{ecs_path.stem}_step_{current_time}_results.json'

  # Prepare the output filename in the 'results' directory
  output_path = results_dir / base_filename
  unique_path = get_unique_filename(output_path)

  # Save the results
  with open(unique_path, 'w') as f:
    json.dump(the_results, f, indent=2)
  print(f'Results saved to {unique_path}')
  return unique_path


class ECSEditor:
  """Entity-component-system (ECS) editor class."""

  def __init__(self, simulation_data=None):
    """Initialize the ECS editor.

    Args:
      simulation_data:
    """
    self.ecs = (
        simulation_data
        if simulation_data
        else {'entities': {}, 'variables': {}, 'systems_definitions': {}}
    )
    self.simulation_data = simulation_data or {}
    self.current_filename = None  # To store the current filename
    self.last_auto_save_time = 0  # Initialize last auto-save time
    self.auto_save_interval = 10  # Time between auto-saves
    self.function_sources = {}  # To store function source code
    self.current_system_index = 0  # track the current operator
    self.new_field_name = None
    self.new_field_value = None
    self.query_option = 'all=True'  # Default query option
    self.component_library = {}  # Default is an empty component library
    self.last_clicked = None
    self.ecs_name = 'ecs_config'  # Default ECS name
    self.task_name = ''  # Default task name
    self.model = ''
    self.api_key = ''  # No default api_key
    self.sampling = sampling
    self.output_file_name = None  # To store the output file name for queries
    self.selected_variable_field = None
    self.current_entity = None
    self.current_component = None
    self.current_variable = None
    self.current_variable_field = None
    self.current_operator_index = None
    self.current_operator_field = None
    self.time_steps = 10  # Default time steps for simulation
    self.current_metric = None  # Track the currently selected metric
    self.metrics = {}  # Store metrics and their values
    self.validate_ecs_structure()
    self.initialize_current_selections()

  def validate_ecs_structure(self):
    """Ensure 'systems_definitions' is a dictionary."""
    if not isinstance(self.ecs.get('systems_definitions'), dict):
      print(
          "Invalid type for 'systems_definitions', reset with empty dictionary."
      )
      self.ecs['systems_definitions'] = {}

  def set_model(self, model: str):
    """Set the model to be used."""
    self.model = model

  def set_api_key(self, api_key: str):
    """Set the api_key to be used."""
    self.api_key = api_key

  def initialize_current_selections(self):
    """Initialize current selections for entities, components, and variables."""
    if self.ecs['entities']:
      self.current_entity = next(iter(self.ecs['entities']))
      if self.ecs['entities'][self.current_entity]:
        self.current_component = self.ecs['entities'][self.current_entity][0]
        if self.ecs['variables'][self.current_component]:
          self.current_variable = next(iter(self.ecs['variables'][
              self.current_component]))
          if self.ecs['systems_definitions'][self.current_component]:
            self.current_operator_index = 0
            self.current_operator_field = next(
                iter(self.ecs['systems_definitions'][
                    self.current_component][self.current_operator_index]), None
            )
            self.current_variable_field = next(
                iter(self.ecs['variables'][self.current_component]), None
            )

  def update_ecs_name(self, name: str):
    """Update the name of the ECS configuration."""
    self.ecs_name = name
    return self.refresh_gui()

  def add_entity(self, entity_name=None):
    """Add a new entity to the ECS configuration."""
    if not entity_name:
      entity_name = f"Entity{len(self.ecs['entities']) + 1}"
    while entity_name in self.ecs['entities']:
      entity_name = f'{entity_name}_copy'
    self.ecs['entities'][entity_name] = []
    self.current_entity = entity_name
    self.last_clicked = ('entity', entity_name)
    return self.refresh_gui()

  def rename_entity(self, new_name=None):
    """Rename the selected entity."""
    if self.last_clicked and self.last_clicked[0] == 'entity':
      old_name = self.last_clicked[1]
      if (
          new_name
          and new_name != old_name
          and new_name not in self.ecs['entities']
      ):
        self.ecs['entities'][new_name] = self.ecs['entities'].pop(old_name)
        self.last_clicked = ('entity', new_name)
        self.current_entity = new_name
        return self.refresh_gui()
    return ''

  def remove_entity(self):
    """Remove the selected entity."""
    if self.current_entity:
      entity = self.current_entity
      del self.ecs['entities'][entity]
      self.current_entity = next(iter(self.ecs['entities']), None)
      if self.current_entity:
        self.on_entity_select([self.current_entity])
      else:
        self.current_component = None
        self.current_variable = None
        self.current_operator_index = None
        self.current_operator_field = None
      return self.refresh_gui()
    return ''

  def move_entity(self, up: bool):
    """Move the selected entity up or down in the list."""
    if self.last_clicked and self.last_clicked[0] == 'entity':
      entity = self.last_clicked[1]
      entities = list(self.ecs['entities'].keys())
      index = entities.index(entity)
      if up and index > 0:
        entities[index], entities[index - 1] = (
            entities[index - 1],
            entities[index],
        )
      elif not up and index < len(entities) - 1:
        entities[index], entities[index + 1] = (
            entities[index + 1],
            entities[index],
        )
      self.ecs['entities'] = {
          name: self.ecs['entities'][name] for name in entities
      }
      self.last_clicked = ('entity', entities[index])
      self.current_entity = entities[index]
      return self.refresh_gui()
    return ''

  def add_component(self, component_name=None):
    """Add a new component to the selected entity."""
    if self.current_entity:
      entity = self.current_entity
      if not component_name:
        component_name = f"Component{len(self.ecs['entities'][entity]) + 1}"
      while component_name in self.ecs['entities'][entity]:
        component_name = f'{component_name}_copy'
      self.ecs['entities'][entity].append(component_name)
      self.ecs['variables'][component_name] = {}
      self.ecs['systems_definitions'][component_name] = []
      self.last_clicked = ('component', component_name)
      self.current_component = component_name
      self.current_variable = None  # Reset current variable
      return self.on_entity_select([self.current_entity])  # self.refresh_gui()
    return ''

  def rename_component(self, new_name):
    """Rename the selected component."""
    if self.current_component:
      old_name = self.current_component
      entity = self.current_entity  # Use current_entity
      if (
          new_name
          and new_name != old_name
          and new_name not in self.ecs['variables']
      ):
        index = self.ecs['entities'][entity].index(old_name)
        self.ecs['entities'][entity][index] = new_name
        self.ecs['variables'][new_name] = self.ecs['variables'].pop(old_name)
        self.ecs['systems_definitions'][new_name] = self.ecs[
            'systems_definitions'
        ].pop(old_name)
        self.last_clicked = ('component', new_name)
        self.current_component = new_name
        self.current_variable = None
        return self.refresh_gui()
    return ''

  def remove_component(self):
    """Remove the selected component from the current entity."""
    if self.current_component:
      component = self.current_component
      entity = self.current_entity
      self.ecs['entities'][entity].remove(component)
      if component in self.ecs['variables']:
        del self.ecs['variables'][component]
      if component in self.ecs['systems_definitions']:
        del self.ecs['systems_definitions'][component]
      # Set current_component to the first remaining component or None
      remaining_components = self.ecs['entities'][entity]
      self.current_component = (
          remaining_components[0] if remaining_components else None
      )
      return self.refresh_gui()
    return ''

  def move_component(self, up: bool):
    """Move the selected component up or down in the list."""
    if self.current_component:
      component = self.current_component
      entity = self.current_entity
      components = self.ecs['entities'][entity]
      index = components.index(component)
      if up and index > 0:
        components[index], components[index - 1] = (
            components[index - 1],
            components[index],
        )
      elif not up and index < len(components) - 1:
        components[index], components[index + 1] = (
            components[index + 1],
            components[index],
        )
      self.ecs['entities'][entity] = components
      self.last_clicked = ('component', components[index])
      self.current_component = components[index]
      self.current_variable = None
      return self.refresh_gui()
    return ''

  def rename_operator_field(self, new_key, new_value):
    """Rename the field of the selected operator."""
    if (
        self.current_component
        and self.current_operator_index is not None
        and self.current_operator_field
    ):
      component = self.current_component
      operator_index = self.current_operator_index
      old_key = self.current_operator_field

      # Update the operator field
      self.ecs['systems_definitions'][component][operator_index][
          new_key
      ] = new_value

      # Remove the old key if it's different
      if new_key != old_key:
        del self.ecs['systems_definitions'][component][operator_index][old_key]

      # Update the current operator field
      self.current_operator_field = new_key

      # Refresh the GUI
      return self.refresh_gui()
    return ''

  def add_operator(self, new_name=None):
    """Add a new operator to the current component."""
    if self.current_component:
      # Use the provided name or generate a default one
      if not new_name:
        new_name = f"operator_{len(self.ecs['systems_definitions'][self.current_component]) + 1}"  # pylint: disable=line-too-long

      # Find the current entity for this component
      entity_name = next((
          entity
          for entity, components in self.ecs.get('entities', {}).items()
          if self.current_component in components
      ), None)

      if entity_name:
        # Create the new ID
        new_op_id = f'{new_name}_{entity_name}_{self.current_component}'

        used_op_ids = set()
        for operators in self.ecs['systems_definitions'].values():
          for op in operators:
            if 'id' in op:
              used_op_ids.add(op['id'])

        if new_op_id in used_op_ids:
          suffix = 1
          while f'{new_op_id}_{suffix}' in used_op_ids:
            suffix += 1
          new_op_id = f'{new_op_id}_{suffix}'

        # Add the new operator with the generated ID and an empty formula field
        self.ecs['systems_definitions'][
            self.current_component].append({'id': new_op_id, 'formula': ''})

        # Update the current operator index to point to the new operator
        self.current_operator_index = len(self.ecs['systems_definitions'][
            self.current_component]) - 1

        # Update GUI
        return self.refresh_gui()
      else:
        print('Error: Could not find entity for component')
    return ''

  def remove_operator(self):
    """Remove the selected operator."""
    if self.current_component and self.current_operator_index is not None:
      operators = self.ecs['systems_definitions'].get(self.current_component,
                                                      [])
      if isinstance(self.current_operator_index, int):
        if 0 <= self.current_operator_index < len(operators):  # type: ignore
          self.ecs['systems_definitions'][self.current_component].pop(
              self.current_operator_index
          )
          if not operators:
            self.add_operator()
          self.current_operator_index = 0
          return self.refresh_gui()
    return ''

  def move_operator(self, up: bool):
    """Move the selected operator up or down in the list."""
    if self.current_component and self.current_operator_index is not None:
      operators = self.ecs['systems_definitions'][self.current_component]
      index = self.current_operator_index
      if up and index > 0:  # type: ignore
        (
            self.ecs['systems_definitions'][self.current_component][index],
            self.ecs['systems_definitions'][self.current_component][index - 1],
        ) = (
            self.ecs['systems_definitions'][self.current_component][index - 1],
            self.ecs['systems_definitions'][self.current_component][index],
        )
        self.current_operator_index = index - 1
      elif not up and index < len(operators) - 1:
        (
            self.ecs['systems_definitions'][self.current_component][index],
            self.ecs['systems_definitions'][self.current_component][index + 1],
        ) = (
            self.ecs['systems_definitions'][self.current_component][index + 1],
            self.ecs['systems_definitions'][self.current_component][index],
        )
        self.current_operator_index = index + 1
      return self.refresh_gui()
    return ''

  def run_simulation(self, time_steps: Optional[int] = None):
    """Run the simulation for the given number of time steps."""
    if time_steps is None:
      time_steps = self.time_steps  # Use the default time steps
    print('Running simulation...')
    if 'initial_state' not in self.simulation_data:
      defaults = {}
      if 'defaults' in self.ecs['variables']:
        defaults = self.ecs['variables']['defaults']
      operators, initial_state = generate_operators(
          self.ecs['entities'],
          self.ecs['variables'],
          self.ecs['systems_definitions'],
          task_name=self.task_name,
          default_values=defaults,
      )
      prompt = (
          'Write one line of valid python to continue the simulation'
          ' consistently including following the format used for every line,'
          ' achieve the stated objectives and, thereby, achieve high scores.\n'
      )
      initial_state['prompt'] = prompt
      initial_state['grid_size'] = 10

      first_entity = next(iter(self.ecs['entities'].keys()), None)
      first_component = (
          self.ecs['entities'][first_entity][0] if first_entity else None
      )
      if first_component and self.ecs['systems_definitions'][first_component]:
        first_operator_id = self.ecs['systems_definitions'][first_component][0][
            'id'
        ]
      else:
        first_operator_id = 'operator_world_heading_1'  # Fallback to default

      sampler = (
          lambda prompt, context, default_assignment, value=None, mode='full': self.sampling(  # pylint: disable=line-too-long
              prompt,
              context,
              default_assignment,
              value,
              mode,
              model=self.model,
              api_key=self.api_key,
          )  # pylint: disable=line-too-long
      )

      self.simulation_data = {
          'initial_state': initial_state,
          'operators': operators,
          'stream': [],
          'gen': simulation_stream_generator(
              initial_state,
              operators,
              first_operator_id,
              max_attempts=10,
              sampling=sampler,
              task_name=self.task_name),
      }

    end_time = (
        self.simulation_data['stream'][-1]['state']['world_time'] + time_steps
        if self.simulation_data['stream']
        else time_steps
    )

    while True:
      try:
        current_step_data = next(self.simulation_data['gen'])
        self.simulation_data['stream'].append(current_step_data)
        # Check if it's time to auto-save metrics
        current_time = current_step_data['state']['world_time']
        if current_time - self.last_auto_save_time >= self.auto_save_interval:
          extracted_values = {
              metric: self.extract_values(metric)
              for metric in self.metrics.keys()
          }
          ecs_name = self.ecs_name or 'ecs_config'
          save_results_to_file(extracted_values, ecs_name, current_time)
          print('********Saved*********')
          self.last_auto_save_time = current_time
        if current_time >= end_time:
          break
      except StopIteration:
        break
    return self.apply_query(self.query_option)

  def reset_simulation(self):
    """Reset the simulation data."""
    self.simulation_data = {}
    return """
      var simOutput = document.getElementById('simulation-output');
      simOutput.innerHTML = '';
      """

  def apply_query(self, query):
    """Apply a query to the simulation history."""
    try:
      s = evaluator(self.task_name)  # Initialize the SimpleEval evaluator
      query_dict = s.eval(f'dict({query})')  # Safely evaluate the query string
      query_result = query_history(
          self.simulation_data['stream'], **query_dict
      )
      # Save the query result to a file if output_file_name is set
      if self.output_file_name is not None:
        # Sanitize the query to create a safe filename
        sanitized_query = re.sub(r'[^a-zA-Z0-9_\-]', '_', query)
        base, ext = os.path.splitext(self.output_file_name)
        if not ext:
          ext = '.txt'  # Default to .txt if no extension provided
        output_filename = f'{base}_{sanitized_query}{ext}'

        # Ensure the directory exists
        dir_name = os.path.dirname(output_filename)
        if dir_name:
          os.makedirs(dir_name, exist_ok=True)

        # Save the query result to the file, replacing existing content
        with open(output_filename, 'w') as f:
          f.write(query_result)
        print(f'Query result saved to {output_filename}')

      formatted_result = self.format_simulation_output(query_result)

      js_code = f"""
      var simOutput = document.getElementById('simulation-output');
      simOutput.innerHTML = `{formatted_result}`;
      """
      return js_code
    except Exception as e:  # pylint: disable=broad-exception-caught
      print(f'Error applying query: {str(e)}')
    return ''

  def format_simulation_output(self, query_result):
    """Format the simulation output for display."""
    lines = query_result.split('\n')
    formatted_lines = []

    for line in lines:
      if '=' in line:
        sampled = ' # sampled' in line
        line = line.replace(' # sampled', '')

        lhs, rhs = line.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        lhs_color = '#ff6347' if sampled else '#66d9ef'
        lhs = f"<span style='color: {lhs_color};'>{lhs}</span>"

        if rhs.startswith('"') and rhs.endswith('"'):
          rhs = f"<span style='color: #e6db74;'>{rhs}</span>"
        elif rhs.startswith("'") and rhs.endswith("'"):
          rhs = f"<span style='color: #e6db74;'>{rhs}</span>"
        elif rhs.isdigit():
          rhs = f"<span style='color: #ae81ff;'>{rhs}</span>"
        else:
          rhs = f"<span style='color: #a6e22e;'>{rhs}</span>"

        formatted_line = f"{lhs} <span style='color: #f8f8f2;'>=</span> {rhs}"
      else:
        formatted_line = f"<span style='color: #f8f8f2;'>{line}</span>"

      formatted_lines.append(formatted_line)

    formatted_result = (
        "<pre style='white-space: pre-wrap; background-color: #2b2b2b; padding:"
        " 10px; border: 1px solid black; color: #f8f8f2;'>"
        + '<br>'.join(formatted_lines)
        + '</pre>'
    )

    return formatted_result

  def save_ecs_configuration_py(self):
    """Save the ECS configuration to a Python file."""
    try:
      py_file = f'{self.ecs_name}.py'
      ecs_dict = {
          'entities': self.ecs['entities'],
          'variables': self.ecs['variables'],
          'systems_definitions': self.ecs['systems_definitions'],
      }

      def dict_to_str(d, indent: int = 0):
        """Convert dictionary to a string with proper formatting."""
        result = []
        ind = ' ' * indent
        for key, value in d.items():
          if isinstance(value, dict):
            result.append(f"{ind}'{key}': " + '{')
            result.append(dict_to_str(value, indent + 4))
            result.append(f'{ind}' + '},')
          elif isinstance(value, list):
            result.append(f"{ind}'{key}': [")
            for item in value:
              if isinstance(item, dict):
                result.append(ind + '    {')
                result.append(dict_to_str(item, indent + 8))
                result.append(ind + '    },')
              else:
                result.append(f'{ind}    {repr(item)},')
            result.append(ind + '],')
          else:
            result.append(f"{ind}'{key}': {repr(value)},")
        return '\n'.join(result)

      config_str = dict_to_str(ecs_dict, 4)
      with open(py_file, 'w') as f:
        f.write('# Generated Python file from ECS configuration\n\n')
        f.write('ecs_config = {\n')
        f.write(config_str)
        f.write('\n}\n')
      print(f'Saved ECS configuration to {py_file}')
      return self.create_download_link(py_file)
    except Exception as e:  # pylint: disable=broad-exception-caught
      print(f'Error saving ECS configuration to Python file: {str(e)}')
      return ''

  def assign_default_op_ids(self):
    """Assign default op_ids to operators without one, ensuring uniqueness."""
    used_op_ids = set()
    for entity, components in self.ecs.get('entities', {}).items():
      for component in components:
        operators = self.ecs['systems_definitions'].get(component, [])
        for i, operator in enumerate(operators):
          if 'id' not in operator:
            # Generate default op_id in the format name_entity_component
            op_id = f'operator_{i + 1}_{entity}_{component}'
            while op_id in used_op_ids:
              i += 1
              op_id = f'operator_{i + 1}_{entity}_{component}'
            operator['id'] = op_id
          used_op_ids.add(operator['id'])

  def load_ecs_from_python(self, file_content, index=0):
    """Load the ECS configuration from a Python file."""
    try:
      # Remove the first line (comment) if it exists
      lines = file_content.split('\n')
      if lines and lines[0].startswith('#'):
        lines = lines[1:]

      # Join the lines back together
      file_content = '\n'.join(lines)

      # Find the start of the ecs_config dictionary
      start_index = file_content.find('ecs_config = {')
      if start_index == -1:
        raise ValueError(
            "No 'ecs_config' dictionary found in the Python file"
        )

      # Extract the dictionary content
      dict_content = file_content[start_index + 13:]  # from 'ecs_config = '

      # Parse the dictionary content
      self.ecs = ast.literal_eval(dict_content)

      # Replace {index} in callable expressions within variables
      self.replace_index_in_variables(index)

      # Assign default op_ids to operators without one
      self.assign_default_op_ids()

      self.initialize_current_selections()
      return self.refresh_gui()
    except Exception as e:
      raise ValueError(  # pylint: disable=raise-missing-from
          f'Error loading ECS configuration from Python file: {str(e)}'
      )

  def replace_index_in_variables(self, index: int):
    """Replace {index} in callable expressions within variables."""
    for variable_name, variable_data in self.ecs['variables'].items():
      for key, value in variable_data.items():
        if isinstance(value, str) and self.is_callable_expression(value):
          self.ecs['variables'][variable_name][key] = value.replace(
              '{index}', str(index))

  def is_callable_expression(self, value):
    """Check if a string looks like a callable expression."""
    return isinstance(value, str) and re.match(
        r'^[a-zA-Z_][a-zA-Z0-9_]*\s*\(.*\)$', value.strip())

  def create_download_link(self, file_name):
    """Create a download link for the saved file."""
    with open(file_name, 'rb') as f:
      data = f.read()
      b64 = base64.b64encode(data).decode()
      payload = f'data:application/octet-stream;base64,{b64}'
      download_link = (
          f'<a download="{file_name}" href="{payload}" target="_blank"'
          f' style="color: #ff00ff;">Click to download {file_name}</a>'
      )

    return f"""
      var downloadLink = `{download_link}`;
      var simOutput = document.getElementById('simulation-output');
      simOutput.innerHTML = downloadLink;
      """

  def save_component(self):
    """Save the current component to a Python file."""
    if self.current_component:
      component_name = self.current_component
      component_data = {
          'component': component_name,
          'variables': self.ecs['variables'][component_name],
          'systems_definitions': self.ecs['systems_definitions'][
              component_name
          ],
      }
      try:
        py_file = f'{component_name}.py'
        def dict_to_str(d, indent=0):
          """Convert dictionary to a string with proper formatting."""
          result = []
          ind = ' ' * indent
          for key, value in d.items():
            if isinstance(value, dict):
              result.append(f"{ind}'{key}': " + '{')
              result.append(dict_to_str(value, indent + 4))
              result.append(f'{ind}' + '},')
            elif isinstance(value, list):
              result.append(f"{ind}'{key}': [")
              for item in value:
                if isinstance(item, dict):
                  result.append(ind + '    {')
                  result.append(dict_to_str(item, indent + 8))
                  result.append(ind + '    },')
                else:
                  result.append(f'{ind}    {repr(item)},')
              result.append(ind + '],')
            else:
              result.append(f"{ind}'{key}': {repr(value)},")
          return '\n'.join(result)

        config_str = dict_to_str(component_data, 4)
        with open(py_file, 'w') as f:
          f.write('# Generated Python file from Component configuration\n\n')
          f.write(f'{component_name}_config = {{\n')
          f.write(config_str)
          f.write('\n}\n')
        print(f'Saved Component configuration to {py_file}')
        return self.create_download_link(py_file)
      except Exception as e:  # pylint: disable=broad-exception-caught
        print(f'Error saving Component configuration to Python file: {str(e)}')
      return ''

  def upload_component(self, file_content):
    """Upload a component from a Python file."""
    try:
      # Remove the first line (comment) if it exists
      lines = file_content.split('\n')
      if lines and lines[0].startswith('#'):
        lines = lines[1:]

      # Join the lines back together
      file_content = '\n'.join(lines)

      # Find the start of the component dictionary
      start_index = file_content.find('_config = {')
      if start_index == -1:
        raise ValueError(
            'No component configuration dictionary found in the Python file'
        )

      # Extract the dictionary content
      dict_content = file_content[
          start_index + 10 :
      ]  # 10 is the length of '_config = '

      # Parse the dictionary content
      component_data = ast.literal_eval(dict_content)

      original_component_name = component_data['component']
      component_name = original_component_name

      # Ensure the component name is unique
      suffix = 1
      while component_name in self.ecs['entities'][self.current_entity]:
        component_name = f'{original_component_name}_{suffix}'
        suffix += 1

      # Add the component to the current entity
      self.ecs['entities'][self.current_entity].append(component_name)
      self.ecs['variables'][component_name] = component_data['variables']
      self.ecs['systems_definitions'][component_name] = component_data[
          'systems_definitions'
      ]

      return self.refresh_gui()
    except Exception as e:
      raise ValueError(  # pylint: disable=raise-missing-from
          f'Error loading component configuration from Python file: {str(e)}'
      )

  def refresh_gui(self):
    """Refresh the GUI to reflect the current state."""
    entities = list(self.ecs['entities'].keys())
    components = (
        self.ecs['entities'][self.current_entity] if self.current_entity else []
    )
    variable_fields = (
        list(self.ecs['variables'][self.current_component].keys())
        if self.current_component
        else []
    )
    operators = (
        self.ecs['systems_definitions'][self.current_component]
        if self.current_component
        else []
    )
    operator_fields = (
        list(operators[self.current_operator_index].keys())
        if operators and self.current_operator_index is not None
        else []
    )
    metrics = list(self.metrics.keys())  # Get the list of metrics

    current_entity_value = self.current_entity if self.current_entity else ''
    current_component_value = (
        self.current_component if self.current_component else ''
    )
    current_variable_field_key = (
        self.current_variable if self.current_variable else ''
    )
    if self.current_component and self.current_variable:
      current_variable_field_value = self.ecs['variables'][
          self.current_component
      ].get(self.current_variable, '')
    else:
      current_variable_field_value = ''
    current_variable_field_value = self.format_variable_value(
        current_variable_field_value
    )
    current_operator_field_key = (
        self.current_operator_field if self.current_operator_field else ''
    )
    current_operator_field_value = (
        self.ecs['systems_definitions'][self.current_component][  # pylint: disable=g-long-ternary
            self.current_operator_index
        ].get(self.current_operator_field, '')
        if self.current_operator_field
        and self.current_operator_index is not None
        else ''
    )

    formatted_operator_field_value = self.format_operator_data(
        current_operator_field_value
    )

    if (
        self.current_operator_index is not None
        and 'id' in operators[self.current_operator_index]
    ):
      current_operator_id = operators[self.current_operator_index]['id']
      trimmed_operator_name = '_'.join(current_operator_id.split('_')[:-2])
    else:
      trimmed_operator_name = ''

    operator_names = (
        [op['id'] for op in operators if 'id' in op] if operators else []
    )

    js_code = f"""
      var entityList = document.getElementById('entity-list');
      entityList.innerHTML = '';
      var entities = {entities};
      entities.forEach(function(entity) {{
        var option = document.createElement('option');
        option.value = entity;
        option.text = entity;
        entityList.appendChild(option);
      }});
      document.getElementById('entity-name-input').value = "{current_entity_value}";

      var componentList = document.getElementById('component-list');
      componentList.innerHTML = '';
      var components = {components};
      components.forEach(function(component) {{
        var option = document.createElement('option');
        option.value = component;
        option.text = component;
        componentList.appendChild(option);
      }});
      document.getElementById('component-name-input').value = "{current_component_value}";

      var variableFieldList = document.getElementById('variable-field-list');
      variableFieldList.innerHTML = '';
      var variableFields = {variable_fields};
      variableFields.forEach(function(field) {{
        var option = document.createElement('option');
        option.value = field;
        option.text = field;
        variableFieldList.appendChild(option);
      }});
      document.getElementById('variable-field-key-input').value = "{current_variable_field_key}";
      document.getElementById('variable-field-value-input').value = "{current_variable_field_value}";

      var operatorList = document.getElementById('operator-list');
      operatorList.innerHTML = '';
      var operators = {operator_names};
      operators.forEach(function(operator) {{
        var option = document.createElement('option');
        option.value = operator;
        option.text = operator;
        operatorList.appendChild(option);
      }});
      document.getElementById('operator-name-input').value = "{trimmed_operator_name}";

      var operatorFieldList = document.getElementById('operator-field-list');
      operatorFieldList.innerHTML = '';
      var operatorFields = {operator_fields};
      operatorFields.forEach(function(field) {{
        var option = document.createElement('option');
        option.value = field;
        option.text = field;
        operatorFieldList.appendChild(option);
      }});
      document.getElementById('operator-field-key-input').value = "{current_operator_field_key}";
      document.getElementById('operator-field-value-input').innerHTML = "{formatted_operator_field_value}";

      var metricList = document.getElementById('metric-list');
      metricList.innerHTML = '';
      var metrics = {metrics};
      metrics.forEach(function(metric) {{
        var option = document.createElement('option');
        option.value = metric;
        option.text = metric;
        metricList.appendChild(option);
      }});
      """
    return js_code

  def format_variable_value(self, value):
    """Format a variable value, handling multiline and escaping issues."""
    if not isinstance(value, str):
      return str(value)

    # Join lines and normalize whitespace
    lines = [line.strip() for line in value.split('\n')]
    value = ' '.join(filter(None, lines))

    # Escape quotes and backslashes for JavaScript
    value = value.replace('\\', '\\\\')
    value = value.replace('"', '\\"')
    value = value.replace("'", "\\'")

    return value

  def format_operator_data(self, value):
    """Format the operator data for display."""
    def clean_multiline(text):
      """Clean multiline string into single line while preserving quotes."""
      if not isinstance(text, str):
        return text
      lines = [line.strip() for line in text.split('\n')]
      return ' '.join(filter(None, lines))

    def escape_for_js(text):
      """Escape string for JavaScript without losing HTML formatting."""
      if not isinstance(text, str):
        return text
      text = text.replace('"', '\\"')
      text = text.replace("'", "\\'")
      text = text.replace('\n', ' ')
      return text

    # First clean up any multiline strings
    value = clean_multiline(value)

    if isinstance(value, str):
      if (
          value.strip().startswith('lambda')
          or value.strip().startswith('def ')
      ):
        formatted_line = f"<span style='color: #a6e22e;'>{value}</span>"
      elif '=' in value:
        lhs, rhs = value.split('=', 1)
        lhs = lhs.strip()
        rhs = rhs.strip()

        lhs = f"<span style='color: #a6e22e;'>{lhs}</span>"

        if rhs.startswith('"') or rhs.startswith("'"):
          rhs = f"<span style='color: #e6db74;'>{rhs}</span>"
        elif rhs.isdigit():
          rhs = f"<span style='color: #ae81ff;'>{rhs}</span>"
        else:
          rhs = f"<span style='color: #a6e22e;'>{rhs}</span>"

        formatted_line = f"{lhs} <span style='color: #f8f8f2;'>=</span> {rhs}"
      else:
        keywords = ['if', 'else', 'for', 'while', 'in', 'append']
        words = value.split()
        formatted_words = []
        for word in words:
          if word in keywords:
            formatted_words.append(
                f"<span style='color: #f92672;'>{word}</span>")
          else:
            formatted_words.append(
                f"<span style='color: #a6e22e;'>{word}</span>")
        formatted_line = ' '.join(formatted_words)
    elif isinstance(value, dict):
      formatted_lines = []
      for k, v in value.items():
        formatted_key = f"<span style='color: #66d9ef;'>{k}</span>"
        if isinstance(v, str):
          if v.startswith('"') or v.startswith("'"):
            formatted_value = f"<span style='color: #e6db74;'>{v}</span>"
          else:
            formatted_value = f"<span style='color: #e6db74;'>'{v}'</span>"
        elif isinstance(v, bool):
          formatted_value = f"<span style='color: #ae81ff;'>{v}</span>"
        elif isinstance(v, (int, float)):
          formatted_value = f"<span style='color: #a6e22e;'>{v}</span>"
        else:
          formatted_value = f"<span style='color: #f8f8f2;'>{v}</span>"

        formatted_line = (
            f"{formatted_key}<span style='color: #f8f8f2;'>:</span> "
            f"{formatted_value}")
        formatted_lines.append(formatted_line)

      formatted_line = (
          "<span style='color: #f8f8f2;'>{" + ', '.join(formatted_lines) +
          '}</span>')
    else:
      formatted_line = f"<span style='color: #f8f8f2;'>{value}</span>"

    # Finally, escape the formatted HTML for JavaScript
    return escape_for_js(formatted_line)

  def on_entity_select(self, entities):
    """Handle entity selection in the GUI."""
    if entities:
      entity = entities[0]
      self.current_entity = entity
      self.last_clicked = ('entity', entity)
      if (
          self.ecs['entities'].get(self.current_entity)
          and len(self.ecs['entities'][self.current_entity]) >= 1
      ):
        self.current_component = self.ecs['entities'][self.current_entity][0]
        return self.on_component_select([self.current_component])
      else:
        self.current_component = None
        self.current_operator_index = None
        self.current_operator_field = None
        self.current_variable = None
      return self.refresh_gui()
    return ''

  def on_component_select(self, components: List[str]):
    """Handle component selection in the GUI."""
    if components:
      component = components[0]
      self.current_component = component
      self.last_clicked = ('component', component)

      if (self.ecs['systems_definitions'].get(self.current_component) and
          'id' in self.ecs['systems_definitions'][self.current_component][0]):
        first_operator_id = self.ecs['systems_definitions'][
            self.current_component][0]['id']
        self.on_operator_select([first_operator_id])
      else:
        self.current_operator_index = None
        self.current_operator_field = None

      if self.ecs['variables'][self.current_component]:
        self.current_variable = next(
            iter(self.ecs['variables'][self.current_component])
        )
      else:
        self.current_variable = None
      return self.refresh_gui()
    return ''

  def on_select_variable(self, key):
    """Handle variable field selection in the GUI."""
    if self.current_component:
      component = self.current_component
      self.selected_variable_field = key
      self.current_variable = key
      value = self.ecs['variables'][component].get(key, '')
      value = self.format_variable_value(value)
      js_code = f"""
      document.getElementById('variable-field-key-input').value = "{key}";
      document.getElementById('variable-field-value-input').value = "{value}";
      """
      return js_code
    return ''

  def on_operator_select(self, operator_ids: List[str]):
    """Handle operator field selection in the GUI using operator IDs."""
    if operator_ids:
      selected_operator_id = operator_ids[0]
      self.last_clicked = ('operator', selected_operator_id)

      # Find the operator index based on the selected operator_id
      operators = self.ecs['systems_definitions'][self.current_component]
      self.current_operator_index = next(
          (
              index
              for index, op in enumerate(operators)
              if op['id'] == selected_operator_id
          ),
          None,
      )

      if self.current_operator_index is not None:
        operator_fields = list(
            operators[self.current_operator_index].keys()
        )
        if operator_fields:
          self.current_operator_field = operator_fields[0]
        else:
          self.current_operator_field = None

        # Trim the entity and component tags from the operator ID
        trimmed_name = '_'.join(
            selected_operator_id.split('_')[:-2]
        )

        # Update the operator name input field
        js_code = f"""
        document.getElementById('operator-name-input').value = "{trimmed_name}";
        """
        js_code += self.refresh_gui()
        return js_code

    return {'js_code': ''}

  def on_operator_field_select(self, field_name):
    """Handle operator field selection in the GUI."""
    if self.current_component and self.current_operator_index is not None:
      self.current_operator_field = field_name
      if (
          field_name
          in self.ecs['systems_definitions'][self.current_component][
              self.current_operator_index
          ]
      ):
        field_value = self.ecs['systems_definitions'][self.current_component][
            self.current_operator_index
        ][field_name]
        print(
            f'Field value for {field_name}: {field_value} (type:'
            f' {type(field_value)})'
        )
        formatted_value = self.format_operator_data(field_value)
        js_code = f"""
        document.getElementById('operator-field-key-input').value = "{field_name}";
        document.getElementById('operator-field-value-input').innerHTML = "{formatted_value}";
        """
        return js_code
      else:
        return ''
    return ''

  def on_metric_select(self, metric):
    """Handle metric selection in the GUI."""
    if metric:
      self.current_metric = metric
      values = self.metrics.get(metric, [])
      js_code = self.update_metric_values(metric, values)
      js_code += f"""
      document.getElementById('metric-field').value = "{metric}";
      """
      return js_code
    else:
      self.current_metric = None
    return ''

  def update_metric_values(self, metric, values):
    """Update metric values in the GUI."""
    output_text = f'{metric}: {values}' if values else ''
    js_code = f"""
    var metricValues = document.getElementById('metric-values');
    metricValues.innerHTML = `{output_text}`;
    """
    return js_code

  def analyze_simulation(self, field):
    """Analyze the simulation output for a specific field."""
    values = self.extract_values(field)
    self.metrics[field] = values
    return self.refresh_gui()

  def remove_metric(self, metric):
    """Remove a metric from the analysis."""
    if metric in self.metrics:
      del self.metrics[metric]
    return self.refresh_gui()

  def extract_metric(self, metric):
    """Extract values for a specific metric."""
    if ('stream' not in self.simulation_data or
        not self.simulation_data['stream']):
      # If there's no stream, store an empty list for the metric
      self.metrics[metric] = []
    else:
      values = self.extract_values(metric)
      self.metrics[metric] = values
      return (self.update_metric_values(metric, values) +
              self.refresh_gui())

    # Return just a refresh of the GUI with empty values
    return self.refresh_gui()

  def plot_analysis(self, metrics, visualization_type='line_plot'):
    """Plot the analysis of the selected metrics."""
    if metrics:
      plt.figure(figsize=(10, 4))

      if visualization_type == 'line_plot':
        for metric in metrics:
          if metric in self.metrics:
            values = self.metrics[metric]
            plt.plot(values, marker='o', label=metric)
        plt.xlabel('Time Steps')
        plt.ylabel('Values')
        plt.title('Plot of Selected Metrics')
        plt.legend()
        plt.grid(True)

      elif visualization_type == '2d_map':
        if len(metrics) >= 2:
          x_metric, y_metric = metrics[:2]
          if x_metric in self.metrics and y_metric in self.metrics:
            x_values = self.metrics[x_metric]
            y_values = self.metrics[y_metric]
            plt.scatter(x_values, y_values, marker='o')
            plt.xlabel(x_metric)
            plt.ylabel(y_metric)
            plt.title('2D Map of Selected Metrics')
            plt.grid(True)

      # Save plot to a PNG in base64 format
      buffer = io.BytesIO()
      plt.savefig(buffer, format='png')
      plt.close()
      buffer.seek(0)
      image_png = buffer.getvalue()
      buffer.close()
      image_base64 = base64.b64encode(image_png).decode('utf-8')

      # JavaScript code to update the plot area
      js_code = f"""
      var plotOutput = document.getElementById('plot-output');
      plotOutput.innerHTML = '<img src="data:image/png;base64,{image_base64}" style="width:100%; height:100%;">';
      """
      return js_code
    return ''

  def extract_values(self, field):
    """Extract values from the simulation output stream at each new time step."""
    values = []

    if ('stream' not in self.simulation_data or
        not self.simulation_data['stream']):
      # If there's no stream, return an empty list
      return values

    previous_time = None

    for step in self.simulation_data['stream']:
      current_time = step['state'].get('world_time', None)
      if current_time != previous_time:
        value = step['state'].get(field, None)
        if value is not None:
          values.append(value)
        previous_time = current_time

    return values

  def rename_operator(self, new_name):
    """Rename the selected operator and update its ID."""
    if self.current_component and self.current_operator_index is not None:
      operators = self.ecs['systems_definitions'][self.current_component]
      operator = operators[self.current_operator_index]

      if 'id' in operator:
        entity_name = next((
            entity
            for entity, components in self.ecs.get('entities', {}).items()
            if self.current_component in components
        ), None)

        # Create the new ID
        new_op_id = f'{new_name}_{entity_name}_{self.current_component}'

        used_op_ids = {  # pylint: disable=g-complex-comprehension
            op['id']
            for ops in self.ecs['systems_definitions'].values()
            for op in ops
        }

        if new_op_id in used_op_ids:
          suffix = 1
          while f'{new_op_id}_{suffix}' in used_op_ids:
            suffix += 1
          new_op_id = f'{new_op_id}_{suffix}'

        # Rename the operator
        operator['id'] = new_op_id

        # Update GUI
        return self.refresh_gui()
    return ''

  def add_operator_field(self, key, value):
    """Add a new field to the current operator."""
    if self.current_component and self.current_operator_index is not None:
      operator = self.ecs['systems_definitions'][self.current_component][
          self.current_operator_index
      ]
      operator[key] = value
      return self.refresh_gui()
    return ''

  def remove_operator_field(self, field_name):
    """Remove an operator field from the current component's operator."""
    if (
        self.current_component
        and self.current_operator_index is not None
        and field_name
    ):
      # operators = self.ecs['systems_definitions'][self.current_component]
      operators = self.ecs['systems_definitions'].get(self.current_component,
                                                      [])
      if isinstance(self.current_operator_index, int):
        if 0 <= self.current_operator_index < len(operators):  # type: ignore
          operator = operators[self.current_operator_index]
          if field_name in operator:
            del operator[field_name]
            self.current_operator_field = None
            return self.refresh_gui()
    return ''

  def add_variable_field(self, key=None, value=None):
    """Add a new field to the current variable."""
    if self.current_component:
      component = self.current_component
      if not key or key in self.ecs['variables'][component]:
        key = f"Field{len(self.ecs['variables'][component]) + 1}"
      if not value:
        value = 'default_value'
      self.ecs['variables'][component][key] = value
      return self.refresh_gui()
    return ''

  def rename_variable_field(self, new_key, new_value):
    """Rename a field in the current variable."""
    if self.current_component and self.selected_variable_field:
      component = self.current_component
      old_key = self.selected_variable_field

      # Rename the key in the variables dictionary
      if old_key in self.ecs['variables'][component]:
        self.ecs['variables'][component][new_key] = self.ecs['variables'][
            component].pop(old_key)
        self.ecs['variables'][component][new_key] = new_value
        self.selected_variable_field = new_key
        return self.refresh_gui()
    return ''

  def remove_variable_field(self, field_name):
    """Remove a field from the current variable."""
    if self.current_component and field_name:
      component = self.current_component

      # Remove the key from the variables dictionary
      if field_name in self.ecs['variables'][component]:
        del self.ecs['variables'][component][field_name]
        self.selected_variable_field = None
        return self.refresh_gui()
    return ''
