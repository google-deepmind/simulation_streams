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

"""A Simulation of a game of catch between three players."""

ecs_config = {
    'entities': {
        'world': ['time', 'world_story'],
        'ball': ['ball1_story'],
        'alice': ['alice_world_view', 'alice_story'],
        'ball2': ['ball2_story'],
        'bob': ['bob_world_view', 'bob_story'],
        'ball3': ['ball3_story'],
        'charlie': ['charlie_world_view', 'charlie_story'],
        'ball4': ['ball4_story', 'blank'],
    },
    'variables': {
        'defaults': {
            'alice': False,
            'bob': False,
            'charlie': False,
            'ball': False,
            'world': False,
        },
        'world_story': {
            'contribution': '',
            'inconsistency_counter': 0,
            'prompt': '''
    You are the world entity in a collaborative storytelling simulation of a ball-throwing game in a park, but your role is not to determine how the ball game itself is proceeding and leave that to the player entities, that all determine player actions with their contributions.
    The world contribution should not determine any player actions, but instead focus on things surrounding the game.

    Background:
    Three friends, Alice, Bob, and Charlie, are playing a game of catch in a park. The rules are simple: whoever has the ball can throw it to one of the other two players. Players without the ball can chat or remain silent.

    The park is bustling with activity on a sunny afternoon. Theres a gentle breeze, and the sounds of laughter and conversation fill the air. Various objects and people around the park might influence the game or provide topics for conversation.

    Alice, Bob, and Charlie stand in a triangle formation, ready to begin their game. Alice holds the ball, preparing to make the first throw.

    Rules for the world entity:
    1. Never include that a player throws the ball.
    1. Add world developments between player turns, 1-3 novel sentences.
    2. Do not repeat previous content but keep moving the story forward with new information.
    3. Introduce elements of the environment and setting, keeping to add new elements.
    4. Ensure all objects are introduced before players interact with them.
    5. Do not make decisions for the players (e.g. to throw the ball), nor introduce developments that imply such player decisions.
    6. The contribution of the player with the ball is the only one who can decide who to throw it to.

    The task proceeds turn by turn, with you acting between each player turn. Add novel, non-generic content to the developing story when called upon, following your rules. Keep the ball in play with throws and catches, but only describe the balls movement when a player has thrown it. Make sure the players always send the ball on promptly to the next person after catching it.

    All contributions should be fully in line with the latest development and never lag in time.
    '''
        },
        'ball1_story': {
            'contribution': 'The ball is with Alice.',
            'previous_state': '',
            'prompt': '''
    You are the ball in a game of catch between Alice, Bob, and Charlie in a park.
    Your sole responsibility is to provide a simple, factual summary of your current location or movement based EXCLUSIVELY on the MOST RECENT contributions from the world and players, including the most recent player action.
    However, if they do not clearly state a change in your state, you remain in the previous state.

    CRITICAL RULES:
    1. ONLY use one of the following predefined statements to describe your current state:
       - "The ball is with Alice."
       - "The ball is with Bob."
       - "The ball is with Charlie."
       - "The ball is flying from Alice towards Bob."
       - "The ball is flying from Bob towards Charlie."
       - "The ball is flying from Charlie towards Bob."
    2. NEVER infer, predict, or move the story forward on your own.

    Remember:
    - You are ONLY summarizing your understanind of the CURRENT state based on the LATEST information.
    - NEVER influence or predict future actions, but make sure to be fully up to date and accurately reflect the absolutely latest contributions.
    - Your report must be based SOLELY on information about your last known position or movement from the most recent world or player contributions.
    '''
        },
        'ball2_story': {},
        'ball3_story': {},
        'ball4_story': {},
        'alice_story': {
            'contribution': '',
            'inconsistency_counter': 0,
            'prompt': '''
    You are Alice, an enthusiastic and competitive player in a game of catch with your friends Bob and Charlie in a park.
    You can see the most current state of the ball in the most recent ball contribution,
    always make sure to be up-to-date and logically coherent based on that state.
    If the action taken by the player in their contribution is found to be invalid,
    one chance to revise the contribution will be given to assure the result in a valid
    logically coherent action that aligns with the current state of the ball.
    If the first attempt at writitng the contribution is found to be invalid,
    you must revise the contribution to make it valid in the second attempt.
    Never just repeat the first attempt, unless it is valid.

    Your background:
    You enjoy the game but also like to challenge your friends with tricky throws.

    Your goals:
    1. Have fun and keep the game interesting.
    2. Show off your throwing skills when you have the ball.
    3. Try to catch any balls thrown your way, no matter how difficult.

    Rules for players:
    1. Add 1-2 sentences to the story during your turn.
    2. Do not write anything that implies decisions for other players.
    3. Only describe independent actions for your own character.
    4. You can interact and talk (use * instead of quotes) but cannot introduce new information about others or the world.
    5. You can only use or mention items already introduced by the world.
    6. Do not repeat content from previous turns.
    7. If you do not have the ball, you can speak but cannot determine what happens to the ball.
    8. If the ball is not in your possession, you cannot throw it.

    Remember, you can only control your own actions. When you have the ball, you decide who to throw it to, but you cant determine if they catch it. Make sure that your contribution is fully in line with the latest developments (seen in the latest ball contribution and your world view) and never lags in time.
    ''',
            'action_prompt': '''
    Based on the players latest contribution, determine their action from the following set:
    - CATCH: The player successfully catches the ball, only possible (valid) if the ball is flying towards them.
    - THROW_TO_ALICE: The player throws the ball to Alice, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_BOB: The player throws the ball to Bob, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_CHARLIE: The player throws the ball to Charlie, only possible (valid) if the ball is with them or flying towards them.
    - NO_ACTION: The player does not interact with the ball, this is always allowed.

    Rules for determining the action:
    1. If the contribution mentions catching or receiving the ball, choose CATCH.
    2. If the contribution describes throwing or sending the ball to a specific player, choose the appropriate THROW_TO_X action.
    3. If the contribution does not mention any direct interaction with the ball, choose NO_ACTION.
    4. Only choose an action that is explicitly described in the contribution.

    Your task is to output ONLY the action name, nothing else. For example: THROW_TO_BOB.
    '''
        },
        'alice_world_view': {
            'world_view': '',
            'world_view_prompt': '''
    You are describing the world from Alices perspective in a game of catch. Your role is to provide a simple, factual summary of the current state of the park and the game based EXCLUSIVELY on the MOST RECENT world description, the latest actions of Bob and Charlie and the current ball position stated in its contribution.

    CRITICAL RULES:
    1. ONLY summarize what has EXPLICITLY been stated in the latest world description and player actions.
    2. NEVER infer, predict, or move the story forward on your own, , but make sure to not repeat the previous world view but focus on what is new.
    3. Do not add any new information not present in the given descriptions.
    4. Focus on details that would be most relevant to Alice.

    Guidelines for Alices world view:
    1. Use 2-3 sentences to describe the current state.
    2. Do not make any assumptions or decisions about future actions.
    3. Only mention objects or events that have been explicitly introduced.

    Remember:
    - You are ONLY summarizing the CURRENT state based on the LATEST information.
    - NEVER influence or predict future actions.
    - Your description must be based SOLELY on EXPLICIT information from the most recent world and player contributions.
    '''
        },
        'bob_story': {
            'contribution': '',
            'inconsistency_counter': 0,
            'prompt': '''
    You are Bob, a laid-back and observant player in a game of catch with your friends Alice and Charlie in a park.
    You can see the most current state of the ball in the most recent ball contribution,
    always make sure to be up-to-date and logically coherent based on that state.
    If the action taken by the player in their contribution is found to be invalid,
    one chance to revise the contribution will be given to assure the result in a valid
    logically coherent action that aligns with the current state of the ball.
    If the first attempt at writitng the contribution is found to be invalid,
    you must revise the contribution to make it valid in the second attempt.
    Never just repeat the first attempt, unless it is valid.

    Your background:
    You enjoy the social aspect of the game more than the competitive side.

    Your goals:
    1. Keep the conversation flowing, whether you have the ball or not.
    2. Make easygoing throws when you have the ball.
    3. Comment on interesting things happening in the park.

    Rules for players:
    1. Add 1-2 sentences to the story during your turn.
    2. Do not write anything that implies decisions for other players.
    3. Only describe independent actions for your own character.
    4. You can interact and talk (use * instead of quotes) but cannot introduce new information about others or the world.
    5. You can only use or mention items already introduced by the world.
    6. Do not repeat content from previous turns.
    7. If you do not have the ball, you can speak but cannot determine what happens to the ball.
    8. If the ball is not in your possession, you cannot throw it.

    Remember, you can only control your own actions. When you have the ball, you decide who to throw it to, but you cant determine if they catch it. Make sure that your contribution is fully in line with the latest developments (seen in the latest ball contribution and your world view) and never lags in time.
    ''',
            'action_prompt': '''
    Based on the players latest contribution, determine their action from the following set:
    - CATCH: The player successfully catches the ball, only possible (valid) if the ball is flying towards them.
    - THROW_TO_ALICE: The player throws the ball to Alice, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_BOB: The player throws the ball to Bob, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_CHARLIE: The player throws the ball to Charlie, only possible (valid) if the ball is with them or flying towards them.
    - NO_ACTION: The player does not interact with the ball, this is always allowed.

    Rules for determining the action:
    1. If the contribution mentions catching or receiving the ball, choose CATCH.
    2. If the contribution describes throwing or sending the ball to a specific player, choose the appropriate THROW_TO_X action.
    3. If the contribution does not mention any direct interaction with the ball, choose NO_ACTION.
    4. Only choose an action that is explicitly described in the contribution.

    Your task is to output ONLY the action name, nothing else. For example: THROW_TO_BOB.
    '''
        },
        'bob_world_view': {
            'world_view': '',
            'world_view_prompt': '''
    You are describing the world from Bobs perspective in a game of catch. Your role is to provide a simple, factual summary of the current state of the park and the game based EXCLUSIVELY on the MOST RECENT world description, the latest actions of Alice and Charlie and the current ball position stated in its contribution.

    CRITICAL RULES:
    1. ONLY summarize what has EXPLICITLY been stated in the latest world description and player actions.
    2. NEVER infer, predict, or move the story forward on your own, but make sure to not repeat the previous world view but focus on what is new.
    3. Do not add any new information not present in the given descriptions.
    4. Focus on details that would be most relevant to Bob.

    Guidelines for Bobs world view:
    1. Use 2-3 sentences to describe the current state.
    2. Do not make any assumptions or decisions about future actions.
    3. Only mention objects or events that have been explicitly introduced.

    Remember:
    - You are ONLY summarizing the CURRENT state based on the LATEST information.
    - NEVER influence or predict future actions.
    - Your description must be based SOLELY on EXPLICIT information from the most recent world and player contributions.
    '''
        },
        'charlie_story': {
            'contribution': '',
            'inconsistency_counter': 0,
            'prompt': '''
    You are Charlie, a strategic and analytical player in a game of catch with your friends Alice and Bob in a park.
    You can see the most current state of the ball in the most recent ball contribution,
    always make sure to be up-to-date and logically coherent based on that state.
    If the action taken by the player in their contribution is found to be invalid,
    one chance to revise the contribution will be given to assure the result in a valid
    logically coherent action that aligns with the current state of the ball.
    If the first attempt at writitng the contribution is found to be invalid,
    you must revise the contribution to make it valid in the second attempt.
    Never just repeat the first attempt, unless it is valid.

    Your background:
    You like to predict where the ball will go and position yourself accordingly.

    Your goals:
    1. Try to anticipate who will receive the next throw.
    2. Make calculated throws when you have the ball.
    3. Observe patterns in how Alice and Bob play.

    Rules for players:
    1. Add 1-2 sentences to the story during your turn.
    2. Do not write anything that implies decisions for other players.
    3. Only describe independent actions for your own character.
    4. You can interact and talk (use * instead of quotes) but cannot introduce new information about others or the world.
    5. You can only use or mention items already introduced by the world.
    6. Do not repeat content from previous turns.
    7. If you do not have the ball, you can speak but cannot determine what happens to the ball.
    8. If the ball is not in your possession, you cannot throw it.

    Remember, you can only control your own actions. When you have the ball, you decide who to throw it to, but you cant determine if they catch it. Make sure that your contribution is fully in line with the latest developments (seen in the latest ball contribution and your world view) and never lags in time.
    ''',
            'action_prompt': '''
    Based on the players latest contribution, determine their action from the following set:
    - CATCH: The player successfully catches the ball, only possible (valid) if the ball is flying towards them.
    - THROW_TO_ALICE: The player throws the ball to Alice, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_BOB: The player throws the ball to Bob, only possible (valid) if the ball is with them or flying towards them.
    - THROW_TO_CHARLIE: The player throws the ball to Charlie, only possible (valid) if the ball is with them or flying towards them.
    - NO_ACTION: The player does not interact with the ball, this is always allowed.

    Rules for determining the action:
    1. If the contribution mentions catching or receiving the ball, choose CATCH.
    2. If the contribution describes throwing or sending the ball to a specific player, choose the appropriate THROW_TO_X action.
    3. If the contribution does not mention any direct interaction with the ball, choose NO_ACTION.
    4. Only choose an action that is explicitly described in the contribution.

    Your task is to output ONLY the action name, nothing else. For example: THROW_TO_BOB.
    '''
        },
        'charlie_world_view': {
            'world_view': '',
            'world_view_prompt': '''
    You are describing the world from Charlies perspective in a game of catch. Your role is to provide a simple, factual summary of the current state of the park and the game based EXCLUSIVELY on the MOST RECENT world description, the latest actions of Alice and Bob and the current ball position stated in its contribution.

    CRITICAL RULES:
    1. ONLY summarize what has EXPLICITLY been stated in the latest world description and player contributions.
    2. NEVER infer, predict, or move the story forward on your own, , but make sure to not repeat the previous world view but focus on what is new.
    3. Do not add any new information not present in the given descriptions.
    4. Focus on details that would be most relevant to Charlie.

    Guidelines for Charlies world view:
    1. Use 2-3 sentences to describe the current state.
    2. Do not make any assumptions or decisions about future actions.
    3. Only mention objects or events that have been explicitly introduced.

    Remember:
    - You are ONLY summarizing the CURRENT state based on the LATEST information.
    - NEVER influence or predict future actions.
    - Your description must be based SOLELY on EXPLICIT information from the most recent world and player contributions.
    '''
        },
        'time': {
            'time': 0,
        },
        'blank': {},
    },
    'systems_definitions': {
        'time': [
            {
                'formula': 'world_time = world_time + 1',
                'alice': True,
                'bob': True,
                'charlie': True,
                'ball': True,
                'world': True,
            },
        ],
        'world_story': [
            {
                'formula': '''world_contribution = (
                    "The park basks in warm sunlight on this pleasant afternoon. A gentle breeze "
                    "rustles through the trees, carrying the scent of freshly cut grass. The red "
                    "rubber ball gleams brightly, its surface smooth and inviting. Around the "
                    "three friends, the park bustles with activity: joggers pass by on a nearby "
                    "path, a group of picnickers spread out a checkered blanket, and a playful "
                    "dog chases a frisbee in the distance. The cheerful atmosphere sets the "
                    "perfect stage for their game of catch."
                )''',
                'query': {'world': True},
                'use_lm': 'world_time > 1',
                'prompt': 'world_prompt',
                'ball': True,
                'world': True,
            },
        ],
        'ball1_story': [
            {
                'formula': 'ball_contribution = ball_contribution',
                'ball': True,
            },
        ],
        'ball2_story': [
            {'formula': 'ball_previous_state = ball_contribution'},
            {
                'formula': (
                    'ball_contribution = ('
                    '    "The ball is with Alice." if alice_action == "CATCH"'
                    '    else "The ball is flying from Alice towards Bob."'
                    '    if alice_action == "THROW_TO_BOB"'
                    '    else "The ball is flying from Alice towards Charlie."'
                    '    if alice_action == "THROW_TO_CHARLIE"'
                    '    else ball_previous_state'
                    ')'
                ),
                'ball': True,
                'alice': True,
            },
        ],
        'ball3_story': [
            {
                'formula': 'ball_previous_state = ball_contribution',
                'ball': True,
            },
            {
                'formula': (
                    'ball_contribution = (    "The ball is with Bob." if'
                    ' bob_action == "CATCH" else    "The ball is flying from'
                    ' Bob towards Alice." if bob_action == "THROW_TO_ALICE"'
                    ' else    "The ball is flying from Bob towards Charlie." if'
                    ' bob_action == "THROW_TO_CHARLIE" else   '
                    ' ball_previous_state)'
                ),
                'ball': True,
                'bob': True,
            },
        ],
        'ball4_story': [
            {'formula': 'ball_previous_state = ball_contribution'},
            {
                'formula': (
                    'ball_contribution = (    "The ball is with Charlie." if'
                    ' charlie_action == "CATCH" else    "The ball is flying '
                    'from Charlie towards Alice." if charlie_action == '
                    '"THROW_TO_ALICE" else    "The ball is flying from Charlie '
                    'towards Bob." if charlie_action == "THROW_TO_BOB" else '
                    ' ball_previous_state)'
                ),
                'ball': True,
                'charlie': True,
            },
        ],
        'alice_story': [
            {
                'formula': """alice_contribution = (
                    "Alice grins mischievously, winding up for her first throw. "
                    "She sends the ball flying towards Bob with a "
                    "tricky spin."
                )""",
                'query': {'alice': True},
                'use_lm': 'world_time > 1',
                'prompt': 'alice_prompt',
                'alice': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'alice_action = "THROW_TO_BOB"',
                'query': {'alice': True},
                'use_lm': 'world_time > 1',
                'prompt': 'alice_action_prompt',
                'alice': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'action_validity = ('
                    'alice_action == "NO_ACTION" or '
                    '(ball_contribution == "The ball is with Alice." and '
                    'alice_action.startswith("THROW_TO_")) or '
                    '(ball_contribution.startswith("The ball is flying") and '
                    'ball_contribution.endswith("Alice.") and '
                    '(alice_action == "CATCH" or '
                    'alice_action.startswith("THROW_TO_")))'
                    ')'
                ),
                'query': {'alice': True},
                'alice': True,
            },
            {
                'formula': 'alice_contribution = alice_contribution',
                'query': {'alice': True},
                'use_lm': 'not action_validity',
                'prompt': 'alice_prompt',
                'alice': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'alice_action = alice_action',
                'query': {'alice': True},
                'use_lm': 'not action_validity',
                'prompt': 'alice_action_prompt',
                'alice': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'action_validity = ('
                    'alice_action == "NO_ACTION" or '
                    '(ball_contribution == "The ball is with Alice." and '
                    'alice_action.startswith("THROW_TO_")) or '
                    '(ball_contribution.startswith("The ball is flying") and '
                    'ball_contribution.endswith("Alice.") and '
                    '(alice_action == "CATCH" or '
                    'alice_action.startswith("THROW_TO_")))'
                    ')'
                ),
                'alice': True,
            },
            {
                'formula': (
                    'alice_inconsistency_counter = alice_inconsistency_counter'
                    ' + 1 if not action_validity else'
                    ' alice_inconsistency_counter'
                ),
                'alice': True,
            },
            {
                'formula': (
                    'alice_action = "NO_ACTION" if not action_validity else'
                    ' alice_action'
                ),
                'alice': True,
            },
        ],
        'bob_story': [
            {
                'formula': (
                    'bob_contribution = "Bob reaches out and catches the ball'
                    ' with a smooth motion. *Nice throw* he calls out'
                    ' cheerfully. With a relaxed stance, he turns to Charlie'
                    ' and makes an easy, arcing throw in his direction."'
                ),
                'query': {'bob': True},
                'use_lm': 'world_time > 1',
                'prompt': 'bob_prompt',
                'bob': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'bob_action = "THROW_TO_CHARLIE"',
                'query': {'bob': True},
                'use_lm': 'world_time > 1',
                'prompt': 'bob_action_prompt',
                'bob': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'action_validity = ('
                    'bob_action == "NO_ACTION" or '
                    '(ball_contribution == "The ball is with Bob." and '
                    'bob_action.startswith("THROW_TO_")) or '
                    '(ball_contribution.startswith("The ball is flying") and '
                    'ball_contribution.endswith("Bob.") and '
                    '(bob_action == "CATCH" or '
                    'bob_action.startswith("THROW_TO_")))'
                    ')'
                ),
                'bob': True,
            },
            {
                'formula': 'bob_contribution = bob_contribution',
                'query': {'bob': True},
                'use_lm': 'not action_validity',
                'prompt': 'bob_prompt',
                'bob': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'bob_action = bob_action',
                'query': {'bob': True},
                'use_lm': 'not action_validity',
                'prompt': 'bob_action_prompt',
                'bob': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'action_validity = ('
                    'bob_action == "NO_ACTION" or '
                    '(ball_contribution == "The ball is with Bob." and '
                    'bob_action.startswith("THROW_TO_")) or '
                    '(ball_contribution.startswith("The ball is flying") and '
                    'ball_contribution.endswith("Bob.") and '
                    '(bob_action == "CATCH" or '
                    'bob_action.startswith("THROW_TO_")))'
                    ')'
                ),
                'bob': True,
            },
            {
                'formula': (
                    'bob_inconsistency_counter = bob_inconsistency_counter + 1'
                    ' if not action_validity else bob_inconsistency_counter'
                ),
                'bob': True,
            },
            {
                'formula': (
                    'bob_action = "NO_ACTION" if not action_validity else'
                    ' bob_action'
                ),
                'bob': True,
            },
        ],
        'charlie_story': [
            {
                'formula': '''charlie_contribution = (
                    "Charlie tracks the balls trajectory and catches it deftly. He takes a "
                    "moment to consider his options, then makes a calculated throw back towards Bob, "
                    "aiming for a spot just slightly to Bobs left."
                )''',
                'query': {'charlie': True},
                'use_lm': 'world_time > 1',
                'prompt': 'charlie_prompt',
                'charlie': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'charlie_action = "THROW_TO_BOB"',
                'query': {'charlie': True},
                'use_lm': 'world_time > 1',
                'prompt': 'charlie_action_prompt',
                'charlie': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'action_validity = ('
                    'charlie_action == "NO_ACTION" or '
                    '(ball_contribution == "The ball is with Charlie." and '
                    'charlie_action.startswith("THROW_TO_")) or '
                    '(ball_contribution.startswith("The ball is flying") and '
                    'ball_contribution.endswith("Charlie.") and '
                    '(charlie_action == "CATCH" or '
                    'charlie_action.startswith("THROW_TO_")))'
                    ')'
                ),
                'charlie': True,
            },
            {
                'formula': 'charlie_contribution = charlie_contribution',
                'query': {'charlie': True},
                'use_lm': 'not action_validity',
                'prompt': 'charlie_prompt',
                'charlie': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': 'charlie_action = charlie_action',
                'query': {'charlie': True},
                'use_lm': 'not action_validity',
                'prompt': 'charlie_action_prompt',
                'charlie': True,
                'world': True,
                'ball': True,
            },
            {
                'formula': (
                    'charlie_inconsistency_counter ='
                    ' charlie_inconsistency_counter + 1 if not action_validity'
                    ' else charlie_inconsistency_counter'
                ),
                'charlie': True,
            },
            {
                'formula': (
                    'charlie_action = "NO_ACTION" if not action_validity else'
                    ' charlie_action'
                ),
                'charlie': True,
                'ball': True,
            },
        ],
        'alice_world_view': [
            {
                'formula': '''alice_world_view = (
                    "Alice sees the sun-drenched park, feeling the competitive energy in the air. "
                    "She notes Bobs relaxed catch and Charlies calculated throw, seeing opportunities "
                    "to show off her skills in this perfect setting for their game. The ball is with Alice."
                )''',
                'query': {'all': True},
                'use_lm': 'world_time > 1',
                'prompt': 'alice_world_view_prompt',
                'alice': True,
            },
        ],
        'bob_world_view': [
            {
                'formula': '''bob_world_view = (
                    "Bob takes in the pleasant park atmosphere, enjoying the gentle breeze. "
                    "He observes Alices enthusiastic throw and Charlies strategic movements, "
                    "appreciating the relaxed game among friends amidst the parks activities. The ball is flying towards Bob from Alice."
                )''',
                'query': {'all': True},
                'use_lm': 'world_time > 1',
                'prompt': 'bob_world_view_prompt',
                'bob': True,
            },
        ],
        'charlie_world_view': [
            {
                'formula': '''charlie_world_view = (
                    "Charlie analyzes the park layout, noting potential variables like the breeze. "
                    "He assesses Alices tricky throw and Bobs casual catch. Bob shouted *Nice throw* to Alice and then Bob threw the ball towards Charlie. "
                    "The ball is flying towards Charlie from Bob."
                )''',
                'query': {'all': True},
                'use_lm': 'world_time > 1',
                'prompt': 'charlie_world_view_prompt',
                'charlie': True,
            },
        ],
        'blank': [
            {
                'formula': 'blank',
                'alice': True,
                'bob': True,
                'charlie': True,
                'ball': True,
                'world': True,
            },
        ],
    },
}
