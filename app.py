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

"""Flask app for the simulation stream generator."""

import argparse
import json
import os
import pathlib

from editor import ECSEditor
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request


app = Flask(__name__)
ecs_editor = ECSEditor()  # Initialize the Entity-Component-System (ECS) editor


@app.route('/')
def index():
  """Layout of the web interface."""
  return render_template('index.html')


def load_metrics_from_file(file_path):
  """Load metrics from a file."""
  try:
    with open(file_path, 'r') as file:
      return [line.strip() for line in file if line.strip()]
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error loading metrics: {str(e)}')
    return []


def run_simulation_and_extract_metrics(
    steps: int, the_metrics: list[str]
) -> dict[str, list[float]]:
  """Run simulation and extract metrics."""
  ecs_editor.run_simulation(steps)
  the_results = {}
  for a_metric in the_metrics:
    the_results[a_metric] = ecs_editor.extract_values(a_metric)
  return the_results


@app.route('/initialize', methods=['GET'])
def initialize():
  """Initialize the web interface."""
  js_code = ecs_editor.refresh_gui()
  return jsonify({'js_code': js_code})


def load_ecs_from_file(file_path, the_index: int = 0):
  """Load ECS configuration from a file."""
  try:
    with open(file_path, 'r') as file:
      file_content = file.read()
    ecs_editor.load_ecs_from_python(file_content, the_index)
    print(f'Loaded ECS configuration from {file_path} with index {the_index}')
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error loading ECS configuration: {str(e)}')


@app.route('/update_ecs_name', methods=['POST'])
def update_ecs_name():
  """Update the ECS name."""
  data = request.json
  new_name = data['name']
  js_code = ecs_editor.update_ecs_name(new_name)
  return jsonify(js_code=js_code)


@app.route('/add_entity', methods=['POST'])
def add_entity():
  """Add an entity."""
  data = request.get_json()
  entity_name = data.get('entity_name')
  js_code = ecs_editor.add_entity(entity_name)
  return jsonify({'js_code': js_code})


@app.route('/rename_entity', methods=['POST'])
def rename_entity():
  """Rename an entity."""
  data = request.get_json()
  new_name = data.get('new_name')
  js_code = ecs_editor.rename_entity(new_name)
  return jsonify({'js_code': js_code})


@app.route('/remove_entity', methods=['POST'])
def remove_entity():
  """Remove an entity."""
  js_code = ecs_editor.remove_entity()
  return jsonify({'js_code': js_code})


@app.route('/move_entity', methods=['POST'])
def move_entity():
  """Move an entity."""
  data = request.get_json()
  up = data.get('up')
  js_code = ecs_editor.move_entity(up)
  return jsonify({'js_code': js_code})


@app.route('/add_component', methods=['POST'])
def add_component():
  """Add a component."""
  data = request.get_json()
  component_name = data.get('component_name')
  js_code = ecs_editor.add_component(component_name)
  return jsonify({'js_code': js_code})


@app.route('/rename_component', methods=['POST'])
def rename_component():
  """Rename a component."""
  data = request.get_json()
  new_name = data.get('new_name')
  js_code = ecs_editor.rename_component(new_name)
  return jsonify({'js_code': js_code})


@app.route('/remove_component', methods=['POST'])
def remove_component():
  """Remove a component."""
  js_code = ecs_editor.remove_component()
  return jsonify({'js_code': js_code})


@app.route('/move_component', methods=['POST'])
def move_component():
  """Move a component."""
  data = request.get_json()
  up = data.get('up')
  js_code = ecs_editor.move_component(up)
  return jsonify({'js_code': js_code})


@app.route('/add_operator', methods=['POST'])
def add_operator():
  """Add an operator."""
  data = request.get_json()
  new_name = data.get('new_name')
  js_code = ecs_editor.add_operator(new_name)
  return jsonify({'js_code': js_code})


@app.route('/remove_operator', methods=['POST'])
def remove_operator():
  """Remove an operator."""
  js_code = ecs_editor.remove_operator()
  return jsonify({'js_code': js_code})


@app.route('/move_operator', methods=['POST'])
def move_operator():
  """Move an operator."""
  data = request.get_json()
  up = data.get('up')
  js_code = ecs_editor.move_operator(up)
  return jsonify({'js_code': js_code})


@app.route('/run_simulation_step', methods=['POST'])
def run_simulation_step():
  """Run a simulation step."""
  try:
    data = request.get_json()
    time_steps = data.get('time_steps', 1)
    js_code = ecs_editor.run_simulation(time_steps)
    return jsonify({'js_code': js_code})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error in run_simulation_step: {str(e)}')
    return jsonify({'error': str(e)}), 500


@app.route('/reset_simulation', methods=['POST'])
def reset_simulation():
  """Reset the simulation."""
  js_code = ecs_editor.reset_simulation()
  return jsonify({'js_code': js_code})


@app.route('/apply_query', methods=['POST'])
def apply_query():
  """Apply a query to the simulation history."""
  data = request.get_json()
  query = data.get('query')
  js_code = ecs_editor.apply_query(query)
  return jsonify({'js_code': js_code})


@app.route('/add_variable_field', methods=['POST'])
def add_variable_field():
  """Add a variable field."""
  try:
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')
    js_code = ecs_editor.add_variable_field(key, value)
    return jsonify({'js_code': js_code})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error in add_variable_field: {str(e)}')
    return jsonify({'error': str(e)}), 500


@app.route('/rename_variable_field', methods=['POST'])
def rename_variable_field():
  """Rename a variable field."""
  data = request.json
  new_key = data['new_key']
  new_value = data['new_value']
  js_code = ecs_editor.rename_variable_field(new_key, new_value)
  return jsonify(js_code=js_code)


@app.route('/remove_variable_field', methods=['POST'])
def remove_variable_field():
  """Remove a variable field."""
  data = request.json
  field_name = data['field_name']
  js_code = ecs_editor.remove_variable_field(field_name)
  return jsonify(js_code=js_code)


@app.route('/save_ecs_configuration_py', methods=['POST'])
def save_ecs_to_python_file():
  """Save the ECS configuration to a Python file."""
  print('in route')
  js_code = ecs_editor.save_ecs_configuration_py()
  return jsonify({'js_code': js_code})


@app.route('/load_ecs_from_python', methods=['POST'])
def load_ecs_from_python():
  """Load the ECS configuration from a Python file."""
  file_content = request.get_data().decode('utf-8')
  try:
    js_code = ecs_editor.load_ecs_from_python(file_content)
    return jsonify({'js_code': js_code})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print('Error:', str(e))
    return jsonify({'error': str(e)}), 500


@app.route('/save_component', methods=['POST'])
def save_component():
  """Save the component."""
  js_code = ecs_editor.save_component()
  return jsonify({'js_code': js_code})


@app.route('/upload_component', methods=['POST'])
def upload_component():
  """Upload a component."""
  file_content = request.get_data().decode('utf-8')  # Decode to string
  try:
    js_code = ecs_editor.upload_component(file_content)
    return jsonify({'js_code': js_code})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print('Error:', str(e))  # Log the error
    return jsonify({'error': str(e)}), 500


@app.route('/analyze_simulation', methods=['POST'])
def analyze_simulation():
  """Analyze the simulation stream with chosen metrics."""
  data = request.json
  field = data['field']
  js_code = ecs_editor.analyze_simulation(field)
  return jsonify(js_code=js_code)


@app.route('/remove_metric', methods=['POST'])
def remove_metric():
  """Remove a metric."""
  data = request.get_json()
  a_metric = data.get('metric')
  js_code = ecs_editor.remove_metric(a_metric)
  return jsonify({'js_code': js_code})


@app.route('/extract_metric', methods=['POST'])
def extract_metric():
  """Extract values for a metric."""
  data = request.get_json()
  a_metric = data.get('metric')
  js_code = ecs_editor.extract_metric(a_metric)
  return jsonify({'js_code': js_code})


@app.route('/plot_analysis', methods=['POST'])
def plot_analysis():
  """Plot the selected metrics."""
  data = request.get_json()
  list_of_metrics = data.get('metrics', [])
  visualization_type = data.get('visualization_type', 'line_plot')
  js_code = ecs_editor.plot_analysis(list_of_metrics, visualization_type)
  return jsonify({'js_code': js_code})


@app.route('/add_operator_field', methods=['POST'])
def add_operator_field():
  """Add an operator field."""
  data = request.get_json()
  key = data.get('key')
  value = data.get('value')
  js_code = ecs_editor.add_operator_field(key, value)
  return jsonify({'js_code': js_code})


@app.route('/rename_operator_field', methods=['POST'])
def rename_operator_field():
  """Rename an operator field."""
  try:
    data = request.get_json()
    new_key = data.get('new_key')
    new_value = data.get('new_value')
    js_code = ecs_editor.rename_operator_field(new_key, new_value)
    return jsonify({'js_code': js_code})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error in rename_operator_field: {str(e)}')
    return jsonify({'error': str(e)}), 500


@app.route('/rename_operator', methods=['POST'])
def rename_operator():
  """Rename an operator."""
  data = request.get_json()
  new_name = data.get('new_name')
  js_code = ecs_editor.rename_operator(new_name)
  return jsonify({'js_code': js_code})


@app.route('/remove_operator_field', methods=['POST'])
def remove_operator_field():
  """Remove an operator field."""
  data = request.get_json()
  field_name = data.get('field_name')
  js_code = ecs_editor.remove_operator_field(field_name)
  return jsonify({'js_code': js_code})


@app.route('/on_entity_select', methods=['POST'])
def on_entity_select():
  """Handle entity selection in the GUI."""
  data = request.get_json()
  entities = data.get('entities')
  js_code = ecs_editor.on_entity_select(entities)
  return jsonify({'js_code': js_code})


@app.route('/on_component_select', methods=['POST'])
def on_component_select():
  """Handle component selection in the GUI."""
  data = request.get_json()
  components = data.get('components')
  js_code = ecs_editor.on_component_select(components)
  return jsonify({'js_code': js_code})


@app.route('/on_select_variable', methods=['POST'])
def on_select_variable():
  """Handle variable selection in the GUI."""
  data = request.get_json()
  key = data.get('key')
  js_code = ecs_editor.on_select_variable(key)
  return jsonify({'js_code': js_code})


@app.route('/on_operator_select', methods=['POST'])
def on_operator_select():
  """Handle operator selection in the GUI."""
  data = request.get_json()
  operator_indices = data.get('operator_indices')
  js_code = ecs_editor.on_operator_select(operator_indices)
  return jsonify({'js_code': js_code})


@app.route('/on_operator_field_select', methods=['POST'])
def on_operator_field_select():
  """Handle operator field selection in the GUI."""
  data = request.get_json()
  field_name = data.get('field_name')
  js_code = ecs_editor.on_operator_field_select(field_name)
  return jsonify({'js_code': js_code})


@app.route('/on_metric_select', methods=['POST'])
def on_metric_select():
  """Handle metric selection in the GUI."""
  data = request.get_json()
  a_metric = data.get('metric')
  js_code = ecs_editor.on_metric_select(a_metric)
  return jsonify({'js_code': js_code})


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


def save_results_to_file(the_results, ecs_file):
  """Save the simulation results in the 'results' subdirectory."""
  # Get the directory of the current script
  script_dir = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

  # Create 'results' directory if it doesn't exist
  results_dir = script_dir / 'results'
  results_dir.mkdir(exist_ok=True)

  # Generate the base filename for results
  ecs_path = pathlib.Path(ecs_file)
  base_filename = f'{ecs_path.stem}_results.json'

  # Prepare the output filename in the 'results' directory
  output_path = results_dir / base_filename
  unique_path = get_unique_filename(output_path)

  # Save the results
  with open(unique_path, 'w') as f:
    json.dump(the_results, f, indent=2)
  print(f'Results saved to {unique_path}')


@app.route('/save_current_values', methods=['POST'])
def save_current_values():
  """Save the current values of the metrics to a file."""
  try:
    # Use the ECS name for the base of the results filename
    ecs_name = ecs_editor.ecs_name or 'ecs_config'
    # Extract the metric values to be saved
    extracted_values = {
        metric: ecs_editor.metrics[metric]
        for metric in ecs_editor.metrics.keys()
    }

    # Generate a unique filename in the 'results/' directory and save results
    save_results_to_file(extracted_values, ecs_name)

    return jsonify({'message': 'Values saved successfully!'})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error in save_current_values: {str(e)}')
    return jsonify({'error': str(e)}), 500


@app.route('/extract_all_metrics', methods=['POST'])
def extract_all_metrics():
  """Extract the current values for all metrics."""
  try:
    # Extract values for all metrics
    for a_metric in ecs_editor.metrics.keys():
      ecs_editor.extract_metric(a_metric)

    return jsonify({'message': 'All metrics extracted successfully!'})
  except Exception as e:  # pylint: disable=broad-exception-caught
    print(f'Error in extract_all_metrics: {str(e)}')
    return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='ECS Editor and Simulator')
  parser.add_argument(
      'ecs_file', nargs='?', help='Path to the ECS configuration file'
  )
  parser.add_argument(
      '--web', action='store_true', help='Launch the web interface'
  )
  parser.add_argument(
      '--steps', type=int, default=10, help='Number of simulation steps to run'
  )
  parser.add_argument(
      '--metrics', help='Path to file containing metrics to track'
  )
  parser.add_argument(
      '--index', type=int, default=0, help='Index initializing variables'
  )
  parser.add_argument(
      '--model', type=str, default='gemini-1.5-pro', help='LLM model'
  )
  parser.add_argument('--api_key', type=str, default='', help='API key')
  parser.add_argument(
      '--output_file', type=str, default='', help='File to save query results'
  )

  parser.add_argument(
      '--task_name', type=str, default='', help='Task name'
  )

  args = parser.parse_args()
  ecs_editor.set_model(args.model)
  ecs_editor.set_api_key(args.api_key)
  if args.output_file:
    ecs_editor.output_file_name = args.output_file

  if args.ecs_file:
    load_ecs_from_file(args.ecs_file, args.index)
  if args.task_name:
    ecs_editor.task_name = args.task_name

  if args.web:
    if args.metrics:
      metrics = load_metrics_from_file(args.metrics)
      for metric in metrics:
        ecs_editor.extract_metric(metric)
    app.run(debug=False)
  elif args.ecs_file:
    metrics = load_metrics_from_file(args.metrics) if args.metrics else []
    results = run_simulation_and_extract_metrics(args.steps, metrics)
    print(json.dumps(results, indent=2))
    save_results_to_file(results, args.ecs_file)
  else:
    print(
        'Please specify an ECS file to load or use --web to launch the web'
        ' interface.'
    )
