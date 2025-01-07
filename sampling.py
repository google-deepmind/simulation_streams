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
"""Provides a sampling function to generate text from an LLM."""

import json
import re
import subprocess
import time

MODEL_PROVIDER_MAPPING = {
    'gpt': 'openai',
    'claude': 'anthropic',
    'gemini': 'google',
    'mistral': 'mistral',
    'llama': 'groqcloud',
}

PROVIDER_REGISTRY = {
    'openai': {
        'api_endpoint': 'https://api.openai.com/v1/chat/completions',
        'headers': lambda api_key: {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        'payload_template': lambda prompt, model: {
            'model': model,
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt},
            ],
            'temperature': 0.7,
        },
        'response_key': 'choices',
        'response_field': lambda res: res[0]['message']['content'].strip(),
        'error_key': 'error',
        'error_field': lambda err: err.get('message', 'Unknown error'),
    },
    'anthropic': {
        'api_endpoint': 'https://api.anthropic.com/v1/messages',
        'headers': lambda api_key: {
            'Content-Type': 'application/json',
            'x-api-key': api_key,
            'anthropic-version': '2023-06-01'
        },
        'payload_template': lambda prompt, model: {
            'model': model,
            'max_tokens': 1024,
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        },
        'response_key': 'content',
        'response_field': lambda res: res[0]['text'].strip() if res else '',
        'error_key': 'error',
        'error_field': lambda err: err.get('message', 'Unknown error')
    },
    'google': {
        'api_endpoint_template': (
            'https://generativelanguage.googleapis.com/v1beta/models/'
            '{model}:generateContent?key={api_key}'
        ),
        'headers': lambda _: {'Content-Type': 'application/json'},
        'payload_template': lambda prompt, model: {
            'contents': [{'parts': [{'text': prompt}]}]
        },
        'response_key': (
            'candidates'
        ),
        'response_field': lambda res: res[0]['content']['parts'][0][
            'text'
        ].strip(),
        'error_key': 'error',
        'error_field': lambda err: err.get('message', 'Unknown error'),
    },
    'mistral': {
        'api_endpoint': 'https://api.mistral.ai/v1/chat/completions',
        'headers': lambda api_key: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        'payload_template': lambda prompt, model: {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 512,
            'temperature': 0.7,
        },
        'response_key': 'choices',
        'response_field': lambda res: res[0]['message']['content'].strip(),
        'error_key': 'error',
        'error_field': lambda err: err.get('message', 'Unknown error'),
    },
    'groqcloud': {
        'api_endpoint': 'https://api.groq.com/openai/v1/chat/completions',
        'headers': lambda api_key: {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
        },
        'payload_template': lambda prompt, model: {
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 512,
            'temperature': 0.7,
        },
        'response_key': 'choices',
        'response_field': (
            lambda res: res[0]['message']['content'].strip() if res else ''
        ),
        'error_key': 'error',
        'error_field': lambda err: err.get('message', 'Unknown error'),
    },
}


def get_provider_from_model(model: str):
  """Determine the provider based on model prefix."""
  for prefix, provider in MODEL_PROVIDER_MAPPING.items():
    if model.startswith(prefix):
      return provider
  raise ValueError(f'Model {model} is not supported')


def run_model_command(prompt: str, model: str, api_key: str) -> str:
  """Run a curl command to call any major LLM provider."""

  # Determine provider based on model prefix
  provider = get_provider_from_model(model)
  provider_details = PROVIDER_REGISTRY[provider]

  # Get API endpoint (no longer requiring Google project_id or location)
  if provider == 'google':
    api_endpoint = provider_details['api_endpoint_template'].format(
        model=model, api_key=api_key
    )
  else:
    api_endpoint = provider_details['api_endpoint']

  # Prepare headers and payload
  headers = provider_details['headers'](api_key)
  payload = provider_details['payload_template'](prompt, model)

  # Convert the payload to JSON
  payload_json = json.dumps(payload)

  # Construct the curl command (keep line length reasonable)
  header_str = ' '.join(
      [f'-H "{key}: {value}"' for key, value in headers.items()]
  )
  command = f"curl {api_endpoint} {header_str} -d '{payload_json}'"

  # Run the command and capture the output
  result = subprocess.run(
      command, shell=True, capture_output=True, text=True, check=True
  )
  # print(result)

  if result.returncode != 0:
    raise RuntimeError(f'curl command failed with error: {result.stderr}')

  # Parse the output JSON
  try:
    response_json = json.loads(result.stdout)
  except json.JSONDecodeError as exc:
    raise ValueError('Failed to parse response') from exc

  # Check for errors in the response
  if provider_details['error_key'] in response_json:
    error_message = provider_details['error_field'](
        response_json[provider_details['error_key']]
    )
    raise RuntimeError(f'API Error: {error_message}')

  # Extract the response based on the model's specific response structure
  if provider_details['response_key'] in response_json:
    response_data = response_json[provider_details['response_key']]
    extracted_text = provider_details['response_field'](response_data)
  else:
    raise ValueError('No valid response found in API response')

  return extracted_text


def sample_text(
    prompt,
    model='',
    api_key='',
    max_characters=10000,
    terminators=None,
    max_attempts=10,
    wait_time=10,
):
  """Sample text from the LLM, with multiple attempts."""
  attempts = 0
  text = ''
  while attempts < max_attempts:
    try:
      text = run_model_command(prompt, model, api_key)
      break  # If successful, break out of the loop
    except Exception as e:  # pylint: disable=broad-exception-caught
      attempts += 1
      if attempts == max_attempts:
        raise RuntimeError(
            f'Failed to sample text after {max_attempts} attempts: {e}'
        ) from e
      print(
          f'Attempt {attempts} failed: {e}. Retrying after {wait_time} '
          'seconds...'
      )
      time.sleep(wait_time)  # Wait before the next attempt

  if len(text) > max_characters:
    text = text[:max_characters]

  if terminators:
    for terminator in terminators:
      if terminator in text:
        text = text.split(terminator)[0]
        break

  return text


def clean_context(context):
  """Remove # sampled comments from the context and fix quotes."""
  cleaned_lines = []
  for line in context.split('\n'):
    # Remove # sampled comments
    line = line.split('# sampled')[0].strip()
    # Check for lhs = rhs pattern and ensure rhs is enclosed in double quotes
    if '=' in line:
      lhs, rhs = line.split('=', 1)
      lhs = lhs.strip()
      rhs = rhs.strip()
      # Check if rhs is a string
      if rhs.startswith("'") and rhs.endswith("'"):
        # Remove escape characters for single quotes
        rhs = rhs[1:-1].replace("\\'", "'").replace('\\"', '"')
        # Replace single quotes with double quotes
        rhs = '"' + rhs + '"'
      elif rhs.startswith('"') and rhs.endswith('"'):
        # Remove escape characters for double quotes
        rhs = rhs[1:-1].replace('\\"', '"').replace("\\'", "'")
        rhs = '"' + rhs + '"'
      line = f'{lhs} = {rhs}'
    cleaned_lines.append(line)
  return '\n'.join(cleaned_lines)


def clean_string(input_string):
  """Remove leading and trailing escaped quotes from a string."""
  # Define a regular expression to match leading escaped quotes
  start_pattern = r'^(\\+["\'])'

  # Find the match at the start
  start_match = re.match(start_pattern, input_string)

  if start_match:
    # Count how many characters were removed
    start_length = len(start_match.group(0))

    # Remove these characters from the start
    input_string = input_string[start_length:]

    # Now, remove the exact same number of characters from the end
    input_string = input_string[:-start_length]

  # Additional check: Remove any trailing backslash
  if input_string.endswith('\\'):
    input_string = input_string[:-1]

  return str(input_string)


def sampling(
    prompt: str,
    context: str,
    default_assignment: str,
    value=None,
    mode: str = 'full',
    model: str = '',
    api_key: str = '',
):
  """Sample an assignment from the LLM."""
  print('sampling with ' + model)
  if value is None:
    value = 'Unknown'
  if isinstance(value, str):
    output_value = f'{default_assignment} = "{value}"'
  else:
    output_value = f'{default_assignment} = {value}'
  value_type = type(value).__name__
  hint = (
      f'\nIn the last block, the current line was:\n{output_value}.\nPlease'
      f' update the righ-hand-side (a concrete value of type {value_type}) '
      ' based on recent developments while keep the left-hand-side unchanged'
      f' as {default_assignment}. First think about the choices and their'
      ' format, but only write a python line when you have chosen your'
      ' continuation.'
  )
  query = prompt + hint + '\n\n' + context
  query = clean_context(query)
  text = sample_text(query, model, api_key)
  print(text)

  # Clean up the text by replacing \" with "
  cleaned_text = text.replace('\\\"', '"')
  cleaned_text = cleaned_text.replace("\\\'", '')
  cleaned_text = cleaned_text.replace('\\"', '"')
  cleaned_text = cleaned_text.replace("\\'", '')
  cleaned_text = cleaned_text.replace('\"', '"')
  cleaned_text = cleaned_text.replace("\'", '')

  lines = cleaned_text.split('\n')
  first_line = lines[0]

  # Skip lines that start with unwanted strings
  unwanted_starts = ['```', '```python']
  while first_line.strip() in unwanted_starts and lines:
    lines.pop(0)
    first_line = lines[0] if lines else ''

  if mode == 'full':
    for line in lines:
      # line = line.replace(r"\'", '')
      line = clean_string(line)
      # Check if the line starts with the expected assignment
      if line.strip().startswith(default_assignment):
        r = line.strip()
        print(r)
        return r
    return ''

  # Reduced mode
  return first_line.strip()
