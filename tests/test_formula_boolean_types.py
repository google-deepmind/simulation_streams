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

"""Exercise sampled formula type checking with the real expression evaluator."""

from contextlib import redirect_stdout
import io
from unittest import mock
import unittest

import numpy as np
from simulation_streams import simulation_utils


class FormulaBooleanTypeTest(unittest.TestCase):

  def run_sample(self, default, values, mode='full', max_attempts=3):
    state = {'prompt': 'Update result.', 'result': default, 'sample_mode': mode}
    responses = [
        repr(value) if mode == 'rhs_only' else f'result = {value!r}'
        for value in values
    ]
    sampler = mock.Mock(side_effect=responses)
    formula = {'formula': f'result = {default!r}', 'use_lm': True}
    with redirect_stdout(io.StringIO()) as log:
      actual_state, output = simulation_utils.run_formula(
          state, formula, max_attempts, sampler, []
      )
    self.assertIs(actual_state, state)
    self.assertIs(state['state'], state)
    return state, output, sampler, log.getvalue()

  def test_boolean_defaults_reject_numbers_and_retry_with_feedback(self):
    for default in (False, True):
      for invalid in (0, 1, 2.5):
        with self.subTest(default=default, invalid=invalid):
          expected = not default
          state, output, sampler, log = self.run_sample(
              default, [invalid, expected]
          )
          self.assertIs(state['result'], expected)
          self.assertEqual(sampler.call_count, 2)
          self.assertEqual(output, [f'result = {expected} # sampled'])
          self.assertIn('Type mismatch: Expected bool', log)
          retry_prompt = sampler.call_args_list[1].args[0]
          self.assertIn('Type mismatch: Expected bool', retry_prompt)
          self.assertIn(f'result = {invalid!r}', retry_prompt)

  def test_numeric_defaults_reject_booleans_and_retry(self):
    for default in (2, 2.5):
      for invalid in (False, True):
        with self.subTest(default=default, invalid=invalid):
          state, output, sampler, log = self.run_sample(
              default, [invalid, 3.25]
          )
          self.assertEqual(state['result'], 3.25)
          self.assertIs(type(state['result']), float)
          self.assertEqual(sampler.call_count, 2)
          self.assertEqual(output, ['result = 3.25 # sampled'])
          self.assertIn('Type mismatch: Expected number, got bool', log)

  def test_exhausted_type_mismatches_leave_the_existing_value_unchanged(self):
    for mode in ('full', 'rhs_only'):
      for default, invalid in ((False, 1), (4, True)):
        with self.subTest(mode=mode, default=default):
          state, output, sampler, _ = self.run_sample(
              default, [invalid] * 3, mode=mode
          )
          self.assertEqual(state['result'], default)
          self.assertIs(type(state['result']), type(default))
          self.assertEqual(sampler.call_count, 3)
          self.assertEqual(output, [f'result = {default} # sampled'])
          if mode == 'rhs_only':
            self.assertEqual(sampler.call_args.kwargs, {'mode': 'rhs_only'})

  def test_valid_boolean_and_numeric_samples_are_accepted_immediately(self):
    for default, value in ((False, True), (True, False), (0, 2.5), (0.5, 2)):
      for mode in ('full', 'rhs_only'):
        with self.subTest(default=default, value=value, mode=mode):
          state, output, sampler, log = self.run_sample(default, [value], mode)
          self.assertEqual(state['result'], value)
          self.assertIs(type(state['result']), type(value))
          self.assertEqual(sampler.call_count, 1)
          self.assertEqual(output, [f'result = {value!r} # sampled'])
          self.assertNotIn('Type mismatch', log)

  def test_other_supported_types_keep_their_existing_behavior(self):
    for default, value in (
        ('old', 'new'),
        ((1,), (2, 3)),
        ([1], [2, 3]),
        ({'a': 1}, {'b': 2}),
    ):
      with self.subTest(default=default):
        state, _, sampler, log = self.run_sample(default, [value])
        self.assertEqual(state['result'], value)
        self.assertIs(type(state['result']), type(default))
        self.assertEqual(sampler.call_count, 1)
        self.assertNotIn('Type mismatch', log)

  def test_numeric_numpy_values_remain_accepted(self):
    for value in (np.int64(7), np.float32(3.5)):
      with self.subTest(dtype=value.dtype):
        state = {'prompt': 'Update result.', 'result': 1, 'candidate': value}
        sampler = mock.Mock(return_value='result = candidate')
        with redirect_stdout(io.StringIO()):
          simulation_utils.run_formula(
              state, {'formula': 'result = 1', 'use_lm': True}, 3, sampler, []
          )
        self.assertIs(state['result'], value)
        sampler.assert_called_once()

  def test_boolean_expressions_infer_boolean_type(self):
    for expression in ('1 < 2', 'not True', 'bool(0)'):
      with self.subTest(expression=expression):
        state = {'prompt': 'Update result.', 'result': False}
        sampler = mock.Mock(side_effect=['result = 7', 'result = True'])
        with redirect_stdout(io.StringIO()):
          simulation_utils.run_formula(
              state,
              {'formula': f'result = {expression}', 'use_lm': True},
              3,
              sampler,
              [],
          )
        self.assertIs(state['result'], True)
        self.assertEqual(sampler.call_count, 2)

  def test_non_sampled_formulas_do_not_call_the_sampler(self):
    for default in (True, False, 1, 1.5):
      with self.subTest(default=default):
        state = {'prompt': 'unused'}
        sampler = mock.Mock(side_effect=AssertionError('unexpected sample'))
        actual, output = simulation_utils.run_formula(
            state,
            {'formula': f'result = {default!r}', 'use_lm': False},
            3,
            sampler,
            [],
        )
        self.assertIs(type(actual['result']), type(default))
        self.assertEqual(actual['result'], default)
        self.assertEqual(output, [f'result = {default!r}'])
        sampler.assert_not_called()

  def test_stream_branch_uses_the_valid_boolean_after_a_rejected_number(self):
    state = {'prompt': 'Choose gate.', 'gate': False, 'world_time': 0}
    operators = [
        {
            'id': 'choose',
            'formula': 'gate = False',
            'use_lm': True,
            'next': "'accept' if gate else 'reject'",
        },
        {
            'id': 'accept',
            'formula': 'world_time = 1',
            'use_lm': False,
            'next': 'choose',
        },
        {
            'id': 'reject',
            'formula': 'world_time = 2',
            'use_lm': False,
            'next': 'choose',
        },
    ]
    sampler = mock.Mock(side_effect=['gate = 1', 'gate = False'])
    with redirect_stdout(io.StringIO()):
      stream = simulation_utils.generate_simulation_stream(
          state, operators, 'choose', sampling=sampler, end_time=1
      )
    self.assertEqual(
        [step['operator_id'] for step in stream], ['choose', 'reject']
    )
    self.assertIs(stream[0]['state']['gate'], False)
    self.assertEqual(stream[1]['state']['world_time'], 2)
    self.assertEqual(sampler.call_count, 2)
    self.assertEqual(
        state, {'prompt': 'Choose gate.', 'gate': False, 'world_time': 0}
    )


if __name__ == '__main__':
  unittest.main()
