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

"""Config for Simulation of a village economy."""

ecs_config = {
    'entities': {
        'world': ['time', 'gdp'],
        'government': ['adapt_tax'],
        'market': ['market_system', 'adapt_fee'],
        'common': ['common_resource_system'],
        'farm': ['farm_system', 'dairyfarm_system'],
        'bakery': ['bakery_system'],
        'fishery': ['fishery_system'],
        'consumer': [
            'consumer_bread_system',
            'consumer_milk_system',
            'consumer_fish_system',
        ],
        'consumer2': [
            'consumer2_bread_system',
            'consumer2_milk_system',
            'consumer2_fish_system',
        ],
        'woodshop': ['woodshop_system'],
        'housebuilder': ['housebuilder_system'],
        'housingprovider': ['housingprovider_system'],
        'summary': [
            'leisure_system',
            'utility',
            'average_utility',
            'average_score',
            'blank',
        ],
    },
    'variables': {
        'defaults': {
            'labor': False,
            'bread': False,
            'grain': False,
            'milk': False,
            'fish': False,
            'wood': False,
            'house': False,
            'housing': False,
            'market': False,
        },
        'time': {
            'time': 0,
        },
        'gdp': {
            'gdp': 0,
        },
        'adapt_tax': {
            'capital': 300,
            'tax': 0.2,
        },
        'market_system': {
            'bread_demand': 0,
            'capital': 300,
            'bread_supply': 0,
            'labor_demand': 0,
            'labor_supply': 0,
            'grain_demand': 0,
            'grain_supply': 0,
            'milk_demand': 0,
            'milk_supply': 0,
            'fish_demand': 0,
            'fish_supply': 0,
            'wood_demand': 0,
            'wood_supply': 0,
            'house_demand': 0,
            'house_supply': 0,
            'housing_demand': 0,
            'housing_supply': 0,
            'bread_inventory': 3,
            'labor_inventory': 5,
            'grain_inventory': 3,
            'milk_inventory': 3,
            'fish_inventory': 3,
            'wood_inventory': 3,
            'house_inventory': 2,
            'housing_inventory': 5,
            'bread_price': 1,
            'labor_price': 1,
            'grain_price': 1,
            'milk_price': 1,
            'fish_price': 1,
            'wood_price': 1,
            'house_price': 5,
            'housing_price': 1,
        },
        'common_resource_system': {
            'hay_inventory': 5,
            'hay_production': 0,
            'hay_consumption': 0,
        },
        'bakery_system': {
            'income': 0.025,
            'capital': 10,
            'bread_production': 0,
            'bread_desired_production': 1,
            'labor_consumption': 0,
            'grain_consumption': 0,
            'labor_desired_consumption': 1,
            'grain_desired_consumption': 1,
        },
        'consumer_bread_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'bread_consumption': 0,
            'housing_consumption': 0,
            'bread_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'consumer_milk_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'milk_consumption': 0,
            'housing_consumption': 0,
            'milk_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'consumer_fish_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'fish_consumption': 0,
            'housing_consumption': 0,
            'fish_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'consumer2_bread_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'bread_consumption': 0,
            'housing_consumption': 0,
            'bread_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'consumer2_milk_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'milk_consumption': 0,
            'housing_consumption': 0,
            'milk_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'consumer2_fish_system': {
            'income': 0.025,
            'capital': 10,
            'labor_production': 0,
            'labor_desired_production': 1,
            'fish_consumption': 0,
            'housing_consumption': 0,
            'fish_desired_consumption': 1,
            'housing_desired_consumption': 1,
        },
        'farm_system': {
            'income': 0.025,
            'capital': 10,
            'grain_production': 0,
            'grain_desired_production': 1,
            'hay_contribution': 0,
            'labor_consumption': 0,
            'labor_desired_consumption': 1,
        },
        'dairyfarm_system': {
            'income': 0.025,
            'capital': 10,
            'milk_production': 0,
            'milk_desired_production': 1,
            'hay_extraction': 0,
            'labor_consumption': 0,
            'hay_desired_consumption': 1,
            'labor_desired_consumption': 1,
        },
        'fishery_system': {
            'income': 0.025,
            'capital': 10,
            'fish_production': 0,
            'fish_desired_production': 1,
            'labor_consumption': 0,
            'labor_desired_consumption': 1,
        },
        'woodshop_system': {
            'income': 0.025,
            'capital': 10,
            'wood_production': 0,
            'wood_desired_production': 1,
            'labor_consumption': 0,
            'labor_desired_consumption': 1,
        },
        'housebuilder_system': {
            'income': 0.025,
            'capital': 10,
            'house_production': 0,
            'house_desired_production': 1,
            'wood_consumption': 0,
            'labor_consumption': 0,
            'wood_desired_consumption': 1,
            'labor_desired_consumption': 1,
        },
        'housingprovider_system': {
            'income': 0.025,
            'capital': 10,
            'housing_production': 0,
            'housing_desired_production': 1,
            'house_consumption': 0,
            'house_desired_consumption': 1,
        },
        'average_utility': {'average_utility': 0},
        'average_score': {'average_score': 0},
        'blank': {},
        'utility': {'utility': 0, 'score': 0},
        'leisure_system': {
            'leisure_time': 0,
        },
        'adapt_fee': {'fee_per_unit': 0.25},
    },
    'systems_definitions': {
        'utility': [
            {
                'formula': 'summary_utility = summary_leisure_time',
            },
            {
                'formula': 'summary_score = summary_utility',
            },
        ],
        'average_utility': [
            {
                'formula': (
                    'summary_average_utility = (summary_average_utility *'
                    ' (world_time - 1) + summary_utility) / world_time'
                ),
            },
        ],
        'average_score': [
            {'formula': 'summary_average_score = summary_average_utility'},
        ],
        'time': [
            {
                'formula': '{entity}_time = {entity}_time + 1',
                'labor': True,
                'bread': True,
                'grain': True,
                'milk': True,
                'fish': True,
                'wood': True,
                'house': True,
                'housing': True,
                'market': True,
            },
        ],
        'leisure_system': [
            {
                'formula': (
                    'summary_leisure_time = max(0, 0.2 *'
                    ' (market_labor_inventory - 5))'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = max(0, market_labor_inventory -'
                    ' summary_leisure_time)'
                ),
            },
        ],
        'gdp': [{
            'formula': '{entity}_gdp = 0',
        }],
        'adapt_fee': [{
            'formula': (
                'market_fee_per_unit = min(10.0, max(0.0, market_fee_per_unit +'
                ' 0.01 * (1 if market_capital < 295 else -1 if market_capital >'
                ' 305 else 0)))'
            ),
        }],
        'adapt_tax': [{
            'formula': (
                'government_tax = min(0.5, max(0.0, government_tax + 0.0025 *'
                ' (1 if government_capital < 295 else -1 if government_capital'
                ' > 305 else 0)))'
            ),
        }],
        'blank': [
            {
                'formula': 'blank',
                'labor': True,
                'bread': True,
                'grain': True,
                'milk': True,
                'fish': True,
                'wood': True,
                'house': True,
                'housing': True,
                'market': True,
            },
        ],
        'bakery_system': [
            {
                'formula': (
                    'bakery_profit_per_unit = market_bread_price -'
                    ' market_grain_price - market_labor_price'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_bread_max_production = market_capital / max(0.1,'
                    ' bakery_profit_per_unit-market_fee_per_unit)'
                ),
                'bread': True,
            },
            {
                'formula': (
                    "bakery_bread_objective = 'Maximize profit by optimizing"
                    ' bread production considering its market price and costs'
                    " of grain and labor.'"
                ),
                'bread': True,
            },
            {
                'formula': (
                    "bread_planning = 'Develop a plan to adjust bread"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'bread': True,
            },
            {
                'formula': (
                    "bread_plan_sampling = 'Given the good price and demand for"
                    ' bread, and considering the moderate cost of 1 units of'
                    ' grain, 1 units of labor, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'bread': True},
                'bread': True,
            },
            {
                'formula': (
                    'bakery_bread_production_adjustment = 1 if'
                    ' bakery_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'bread': True},
                'bread': True,
            },
            {
                'formula': (
                    'bakery_bread_desired_production = max(0, min(max(0.1,'
                    ' bakery_bread_production + max(-0.25,'
                    ' min(bakery_bread_production_adjustment, 0.25))),'
                    ' bakery_capital / max(market_grain_price +'
                    ' market_labor_price, 0.01), 5 - market_bread_inventory,'
                    ' (bakery_capital * 0.1) / max(-bakery_profit_per_unit,'
                    ' 0.01)))'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_bread_desired_production = max(0, min(max(0.1,'
                    ' bakery_bread_production + max(-0.25,'
                    ' min(bakery_bread_production_adjustment, 0.25))),'
                    ' bakery_capital / max(market_grain_price +'
                    ' market_labor_price, 0.01),'
                    ' 5 - market_bread_inventory, (bakery_capital * 0.1) /'
                    ' max(-bakery_profit_per_unit, 0.01),'
                    ' (bakery_capital - 1) / max(-bakery_profit_per_unit,'
                    ' 0.01)))'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_bread_production = max(0,'
                    ' min(bakery_bread_desired_production,'
                    ' market_grain_inventory / 1, market_labor_inventory / 1,'
                    ' bakery_bread_max_production))'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'market_bread_supply = market_bread_supply +'
                    ' bakery_bread_production'
                ),
            },
            {
                'formula': (
                    'bakery_grain_consumption = bakery_bread_production * 1'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'market_grain_inventory = market_grain_inventory -'
                    ' bakery_grain_consumption'
                ),
            },
            {
                'formula': (
                    'bakery_labor_consumption = bakery_bread_production * 1'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' bakery_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_bread_inventory = market_bread_inventory +'
                    ' bakery_bread_production'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_grain_desired_consumption = '
                    'bakery_bread_desired_production * 1'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_labor_desired_consumption = '
                    'bakery_bread_desired_production * 1'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'market_grain_demand = market_grain_demand + '
                    'bakery_grain_desired_consumption'
                ),
                # 'grain': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'bakery_labor_desired_consumption'
                ),
                # 'labor': True,
            },
            {
                'formula': (
                    'bakery_profit = bakery_bread_production *'
                    ' (bakery_profit_per_unit - market_fee_per_unit)'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'bakery_tax = max(0, bakery_profit * government_tax)'
                ),
                'bread': True,
            },
            {
                'formula': 'bakery_taxed_profit = bakery_profit - bakery_tax',
                'bread': True,
            },
            {
                'formula': (
                    'bakery_capital = bakery_capital + min(bakery_income,'
                    ' government_capital) + bakery_taxed_profit'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(bakery_income, government_capital) + bakery_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + bakery_bread_production *'
                    ' market_bread_price'
                ),
            },
        ],
        'consumer_bread_system': [
            {
                'formula': (
                    'consumer_profit_per_unit = market_labor_price -'
                    ' (market_bread_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_max_production = market_capital / max(0.1,'
                    ' consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of bread and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' bread, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production_adjustment = 1 if'
                    ' consumer_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer_labor_production + max(-0.25,'
                    ' min(consumer_labor_production_adjustment, 0.25))),'
                    ' consumer_capital / max(market_bread_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer_capital * 0.05) /'
                    ' max(-consumer_profit_per_unit, 0.01),'
                    ' (consumer_capital - 1) / max(-consumer_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production = max(0,'
                    ' min(consumer_labor_desired_production,'
                    ' market_bread_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer_bread_consumption = consumer_labor_production'
                    ' * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_bread_inventory = market_bread_inventory -'
                    ' consumer_bread_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_housing_consumption = consumer_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_bread_desired_consumption = '
                    'consumer_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_housing_desired_consumption = '
                    'consumer_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_bread_demand = market_bread_demand + '
                    'consumer_bread_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer_housing_desired_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_profit = consumer_labor_production *'
                    ' (consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_tax = max(0, consumer_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_taxed_profit = consumer_profit - consumer_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_capital = consumer_capital + min(consumer_income,'
                    ' government_capital) + consumer_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer_income, government_capital) + consumer_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'consumer_milk_system': [
            {
                'formula': (
                    'consumer_profit_per_unit = market_labor_price -'
                    ' (market_milk_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_max_production = market_capital / max(0.1,'
                    ' consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of milk and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' milk, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production_adjustment = 1 if'
                    ' consumer_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer_labor_production + max(-0.25,'
                    ' min(consumer_labor_production_adjustment, 0.25))),'
                    ' consumer_capital / max(market_milk_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer_capital * 0.05) /'
                    ' max(-consumer_profit_per_unit, 0.01),'
                    ' (consumer_capital - 1) / max(-consumer_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production = max(0,'
                    ' min(consumer_labor_desired_production,'
                    ' market_milk_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer_milk_consumption = consumer_labor_production'
                    ' * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_milk_inventory = market_milk_inventory -'
                    ' consumer_milk_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_housing_consumption = consumer_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_milk_desired_consumption = '
                    'consumer_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_housing_desired_consumption = '
                    'consumer_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_milk_demand = market_milk_demand + '
                    'consumer_milk_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer_housing_desired_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_profit = consumer_labor_production *'
                    ' (consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_tax = max(0, consumer_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_taxed_profit = consumer_profit - consumer_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_capital = consumer_capital + min(consumer_income,'
                    ' government_capital) + consumer_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer_income, government_capital) + consumer_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'consumer_fish_system': [
            {
                'formula': (
                    'consumer_profit_per_unit = market_labor_price -'
                    ' (market_fish_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_max_production = market_capital / max(0.1,'
                    ' consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of fish and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' fish, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production_adjustment = 1 if'
                    ' consumer_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer_labor_production + max(-0.25,'
                    ' min(consumer_labor_production_adjustment, 0.25))),'
                    ' consumer_capital / max(market_fish_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer_capital * 0.05) /'
                    ' max(-consumer_profit_per_unit, 0.01),'
                    ' (consumer_capital - 1) / max(-consumer_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_labor_production = max(0,'
                    ' min(consumer_labor_desired_production,'
                    ' market_fish_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer_fish_consumption = consumer_labor_production'
                    ' * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_fish_inventory = market_fish_inventory -'
                    ' consumer_fish_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_housing_consumption = consumer_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_fish_desired_consumption = '
                    'consumer_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_housing_desired_consumption = '
                    'consumer_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_fish_demand = market_fish_demand + '
                    'consumer_fish_desired_consumption'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer_housing_desired_consumption'
                ),
            },
            {
                'formula': (
                    'consumer_profit = consumer_labor_production *'
                    ' (consumer_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_tax = max(0, consumer_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_taxed_profit = consumer_profit - consumer_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer_capital = consumer_capital + min(consumer_income,'
                    ' government_capital) + consumer_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer_income, government_capital) + consumer_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'consumer2_bread_system': [
            {
                'formula': (
                    'consumer2_profit_per_unit = market_labor_price -'
                    ' (market_bread_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_max_production = market_capital / max(0.1,'
                    ' consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer2_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of bread and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' bread, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production_adjustment = 1 if'
                    ' consumer2_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer2_labor_production + max(-0.25,'
                    ' min(consumer2_labor_production_adjustment, 0.25))),'
                    ' consumer2_capital / max(market_bread_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer2_capital * 0.05) /'
                    ' max(-consumer2_profit_per_unit, 0.01),'
                    ' (consumer2_capital - 1) / max(-consumer2_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production = max(0,'
                    ' min(consumer2_labor_desired_production,'
                    ' market_bread_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer2_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer2_bread_consumption = consumer2_labor_production'
                    ' * 0.5'
                ),
                'bread': True,
            },
            {
                'formula': (
                    'market_bread_inventory = market_bread_inventory -'
                    ' consumer2_bread_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_housing_consumption = consumer2_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer2_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_bread_desired_consumption = '
                    'consumer2_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_housing_desired_consumption = '
                    'consumer2_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_bread_demand = market_bread_demand + '
                    'consumer2_bread_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer2_housing_desired_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_profit = consumer2_labor_production *'
                    ' (consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_tax = max(0, consumer2_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_taxed_profit = consumer2_profit - consumer2_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_capital = consumer2_capital +'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer2_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer2_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'consumer2_milk_system': [
            {
                'formula': (
                    'consumer2_profit_per_unit = market_labor_price -'
                    ' (market_milk_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_max_production = market_capital / max(0.1,'
                    ' consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer2_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of milk and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' milk, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production_adjustment = 1 if'
                    ' consumer2_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer2_labor_production + max(-0.25,'
                    ' min(consumer2_labor_production_adjustment, 0.25))),'
                    ' consumer2_capital / max(market_milk_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer2_capital * 0.05) /'
                    ' max(-consumer2_profit_per_unit, 0.01),'
                    ' (consumer2_capital - 1) / max(-consumer2_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production = max(0,'
                    ' min(consumer2_labor_desired_production,'
                    ' market_milk_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer2_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production = max(0, min('
                    ' consumer2_labor_desired_production, market_milk_inventory'
                    ' / 0.5, market_housing_inventory / 0.2,'
                    ' consumer2_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer2_milk_consumption = consumer2_labor_production'
                    ' * 0.5'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'market_milk_inventory = market_milk_inventory -'
                    ' consumer2_milk_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_housing_consumption = consumer2_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer2_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_milk_desired_consumption = '
                    'consumer2_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_housing_desired_consumption = '
                    'consumer2_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_milk_demand = market_milk_demand + '
                    'consumer2_milk_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer2_housing_desired_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_profit = consumer2_labor_production *'
                    ' (consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_tax = max(0, consumer2_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_taxed_profit = consumer2_profit - consumer2_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_capital = consumer2_capital +'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer2_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer2_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'consumer2_fish_system': [
            {
                'formula': (
                    'consumer2_profit_per_unit = market_labor_price -'
                    ' (market_fish_price * 0.5 + market_housing_price * 0.2)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_max_production = market_capital / max(0.1,'
                    ' consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    "consumer2_labor_objective = 'Maximize profit by optimizing"
                    ' labor production considering its market price and costs'
                    " of fish and housing.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_planning = 'Develop a plan to adjust labor"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'labor': True,
            },
            {
                'formula': (
                    "labor_plan_sampling = 'Given the good price and demand for"
                    ' labor, and considering the moderate cost of 0.5 units of'
                    ' fish, 0.2 units of housing, the strategy is to keep up a'
                    ' robust production level to ensure a continuous flow of'
                    ' goods.  If the profit per unit is positive, the current'
                    ' adjustment plan involves increasing production by 1'
                    ' units. If the profit per unit turns negative, we need to'
                    " quickly cut production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production_adjustment = 1 if'
                    ' consumer2_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'labor': True},
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_desired_production = max(0, min(max(1.0,'
                    ' consumer2_labor_production + max(-0.25,'
                    ' min(consumer2_labor_production_adjustment, 0.25))),'
                    ' consumer2_capital / max(market_fish_price * 0.5 +'
                    ' market_housing_price * 0.2, 0.01),'
                    ' 10 - market_labor_inventory, (consumer2_capital * 0.05) /'
                    ' max(-consumer2_profit_per_unit, 0.01),'
                    ' (consumer2_capital - 1) / max(-consumer2_profit_per_unit,'
                    ' 0.01)))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_labor_production = max(0,'
                    ' min(consumer2_labor_desired_production,'
                    ' market_fish_inventory / 0.5, market_housing_inventory /'
                    ' 0.2, consumer2_labor_max_production))'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_labor_supply = market_labor_supply +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory +'
                    ' consumer2_labor_production'
                ),
            },
            {
                'formula': (
                    'consumer2_fish_consumption = consumer2_labor_production'
                    ' * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_fish_inventory = market_fish_inventory -'
                    ' consumer2_fish_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_housing_consumption = consumer2_labor_production'
                    ' * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory -'
                    ' consumer2_housing_consumption'
                ),
            },
            {
                'formula': (
                    'consumer2_fish_desired_consumption = '
                    'consumer2_labor_desired_production * 0.5'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_housing_desired_consumption = '
                    'consumer2_labor_desired_production * 0.2'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'market_fish_demand = market_fish_demand + '
                    'consumer2_fish_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_demand = market_housing_demand + '
                    'consumer2_housing_desired_consumption'
                ),

            },
            {
                'formula': (
                    'consumer2_profit = consumer2_labor_production *'
                    ' (consumer2_profit_per_unit - market_fee_per_unit)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_tax = max(0, consumer2_profit * government_tax)'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_taxed_profit = consumer2_profit - consumer2_tax'
                ),
                'labor': True,
            },
            {
                'formula': (
                    'consumer2_capital = consumer2_capital +'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_taxed_profit'
                ),
                'labor': True,
            },
            {
                'formula': 'market_capital = market_capital - consumer2_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(consumer2_income, government_capital) +'
                    ' consumer2_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + consumer2_labor_production *'
                    ' market_labor_price'
                ),
            },
        ],
        'common_resource_system': [
            {
                'formula': 'common_hay_production = farm_hay_contribution',
            },
            {
                'formula': 'common_hay_consumption = farm_hay_extraction',
            },
            {
                'formula': (
                    'common_hay_inventory = common_hay_inventory +'
                    ' common_hay_production - common_hay_consumption'
                ),
                'initial_value': 0,
            },
        ],
        'market_system': [
            {
                'formula': 'market_labor_price = market_labor_price',
                'market': True
            },
            {
                'formula': 'market_labor_demand = market_labor_demand',
                'market': True
            },
            {
                'formula': 'market_labor_inventory = market_labor_inventory',
                'market': True
            },
            {
                'formula': (
                    "price_setting_objective_labor = 'Set the labor price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=10 units) while aiming to increase traded volumes'
                    ' and produced/consumed labor. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=10 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_labor = 'Based on the current market"
                    ' conditions for labor with moderate inventory levels, we'
                    ' will for now keep the labor price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_labor_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_labor_price = max(0.1, min(10, market_labor_price +'
                    ' max(-0.5, min(market_labor_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_bread_price = market_bread_price',
                'market': True,
            },
            {
                'formula': 'market_bread_demand = market_bread_demand',
                'market': True,
            },
            {
                'formula': 'market_bread_inventory = market_bread_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_bread = 'Set the bread price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=5 units) while aiming to increase traded volumes'
                    ' and produced/consumed bread. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=5 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_bread = 'Based on the current market"
                    ' conditions for bread with moderate inventory levels, we'
                    ' will for now keep the bread price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_bread_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_bread_price = max(0.1, min(10, market_bread_price +'
                    ' max(-0.5, min(market_bread_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_grain_price = market_grain_price',
                'market': True,
            },
            {
                'formula': 'market_grain_demand = market_grain_demand',
                'market': True,
            },
            {
                'formula': 'market_grain_inventory = market_grain_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_grain = 'Set the grain price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=5 units) while aiming to increase traded volumes'
                    ' and produced/consumed grain. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=5 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_grain = 'Based on the current market"
                    ' conditions for grain with moderate inventory levels, we'
                    ' will for now keep the grain price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_grain_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_grain_price = max(0.1, min(10, market_grain_price +'
                    ' max(-0.5, min(market_grain_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_milk_price = market_milk_price',
                'market': True,
            },
            {
                'formula': 'market_milk_demand = market_milk_demand',
                'market': True,
            },
            {
                'formula': 'market_milk_inventory = market_milk_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_milk = 'Set the milk price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=5 units) while aiming to increase traded volumes'
                    ' and produced/consumed milk. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=5 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_milk = 'Based on the current market"
                    ' conditions for milk with moderate inventory levels, we'
                    ' will for now keep the milk price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_milk_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_milk_price = max(0.1, min(10, market_milk_price + '
                    'max(-0.5, min(market_milk_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_fish_price = market_fish_price',
                'market': True,
            },
            {
                'formula': 'market_fish_demand = market_fish_demand',
                'market': True,
            },
            {
                'formula': 'market_fish_inventory = market_fish_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_fish = 'Set the fish price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=5 units) while aiming to increase traded volumes'
                    ' and produced/consumed fish. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=5 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_fish = 'Based on the current market"
                    ' conditions for fish with moderate inventory levels, we'
                    ' will for now keep the fish price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_fish_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_fish_price = max(0.1, min(10, market_fish_price + '
                    'max(-0.5, min(market_fish_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_wood_price = market_wood_price',
                'market': True,
            },
            {
                'formula': 'market_wood_demand = market_wood_demand',
                'market': True,
            },
            {
                'formula': 'market_wood_inventory = market_wood_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_wood = 'Set the wood price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=10 units) while aiming to increase traded volumes'
                    ' and produced/consumed wood. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=10 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_wood = 'Based on the current market"
                    ' conditions for wood with moderate inventory levels, we'
                    ' will for now keep the wood price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_wood_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_wood_price = max(0.1, min(10, market_wood_price + '
                    'max(-0.5, min(market_wood_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_house_price = market_house_price',
                'market': True,
            },
            {
                'formula': 'market_house_demand = market_house_demand',
                'market': True,
            },
            {
                'formula': 'market_house_inventory = market_house_inventory',
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_house = 'Set the house price to"
                    ' ensure a balanced market with limited inventories (full'
                    ' at max=3 units) while aiming to increase traded volumes'
                    ' and produced/consumed houses. If inventory does not cover'
                    ' demand, the price needs to go up to increase production,'
                    ' while if the inventory approaches max=3 units the prices'
                    ' need to be cut to clear it. Always keep the price above 0'
                    " and at most change it by 0.5 per step, but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_house = 'Based on the current market"
                    ' conditions for houses with moderate inventory levels, we'
                    ' will for now keep the house price at 5. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_house_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_house_price = max(0.5, min(50, market_house_price +'
                    ' max(-0.5, min(market_house_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_housing_price = market_housing_price',
                'market': True,
            },
            {
                'formula': 'market_housing_demand = market_housing_demand',
                'market': True,
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory'
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_objective_housing = 'Set the housing price"
                    ' to ensure a balanced market with limited inventories'
                    ' (full at max=10 units) while aiming to increase traded'
                    ' volumes and produced/consumed housing. If inventory does'
                    ' not cover demand, the price needs to go up to increase'
                    ' production, while if the inventory approaches max=10'
                    ' units the prices need to be cut to clear it. Always keep'
                    ' the price above 0 and at most change it by 0.5 per step,'
                    " but be proactive.'"
                ),
                'market': True,
            },
            {
                'formula': (
                    "price_setting_plan_housing = 'Based on the current market"
                    ' conditions for housing with moderate inventory levels, we'
                    ' will for now keep the housing price at 1. If we see the'
                    ' inventories filling up we will cut the price to clear'
                    ' stock, while if they are getting empty such that demand'
                    " is not met, we will increase the price.'"
                ),
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': 'market_housing_price_adjustment = 0',
                'query': {'market': True},
                'use_lm': 'world_time > 1',
                'market': True,
            },
            {
                'formula': (
                    'market_housing_price = max(0.1, min(10,'
                    ' market_housing_price + max(-0.5,'
                    ' min(market_housing_price_adjustment, 0.5))))'
                ),
                'market': True,
            },
            {
                'formula': 'market_labor_demand = 0',
            },
            {
                'formula': 'market_labor_supply = 0',
            },
            {
                'formula': 'market_bread_demand = 0',
            },
            {
                'formula': 'market_bread_supply = 0',
            },
            {
                'formula': 'market_grain_demand = 0',
            },
            {
                'formula': 'market_grain_supply = 0',
            },
            {
                'formula': 'market_milk_demand = 0',
            },
            {
                'formula': 'market_milk_supply = 0',
            },
            {
                'formula': 'market_fish_demand = 0',
            },
            {
                'formula': 'market_fish_supply = 0',
            },
            {
                'formula': 'market_wood_demand = 0',
            },
            {
                'formula': 'market_wood_supply = 0',
            },
            {
                'formula': 'market_house_demand = 0',
            },
            {
                'formula': 'market_house_supply = 0',
            },
            {
                'formula': 'market_housing_demand = 0',
            },
            {
                'formula': 'market_housing_supply = 0',
            },
        ],
        'farm_system': [
            {
                'formula': (
                    'farm_profit_per_unit = market_grain_price -'
                    ' market_labor_price'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'farm_grain_max_production = market_capital / max(0.1,'
                    ' farm_profit_per_unit-market_fee_per_unit)'
                ),
                'grain': True,
            },
            {
                'formula': (
                    "farm_grain_objective = 'Maximize profit by optimizing"
                    ' grain production considering its market price and costs'
                    " of labor.'"
                ),
                'grain': True,
            },
            {
                'formula': (
                    "grain_planning = 'Develop a plan to adjust grain"
                    ' production based on market conditions and capital while'
                    ' remembering the overall need to keep up the flow of goods'
                    ' in the economy. Increase production if profit per unit is'
                    ' high and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'grain': True,
            },
            {
                'formula': (
                    "grain_plan_sampling = 'Given the good price and demand for"
                    ' grain, and considering the moderate cost of 1 units of'
                    ' labor, the strategy is to keep up a robust production'
                    ' level to ensure a continuous flow of goods.  If the'
                    ' profit per unit is positive, the current adjustment plan'
                    ' involves increasing production by 1 units. If the profit'
                    ' per unit turns negative, we need to quickly cut'
                    " production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'grain': True},
                'grain': True,
            },
            {
                'formula': (
                    'farm_grain_production_adjustment = 1 if'
                    ' farm_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'grain': True},
                'grain': True,
            },
            {
                'formula': (
                    'farm_grain_desired_production = max(0, min(max(1.0,'
                    ' farm_grain_production + max(-0.25,'
                    ' min(farm_grain_production_adjustment, 0.25))),'
                    ' farm_capital / max(market_labor_price, 0.01),'
                    ' 5 - market_grain_inventory, (farm_capital * 0.1) /'
                    ' max(-farm_profit_per_unit, 0.01),'
                    ' (farm_capital - 1) / max(-farm_profit_per_unit,'
                    ' 0.01)))'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'farm_grain_production = max(0,'
                    ' min(farm_grain_desired_production, market_labor_inventory'
                    ' / 1, farm_grain_max_production))'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'market_grain_supply = market_grain_supply +'
                    ' farm_grain_production'
                ),
            },
            {
                'formula': 'farm_labor_consumption = farm_grain_production * 1',
                'grain': True,
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' farm_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_grain_inventory = market_grain_inventory +'
                    ' farm_grain_production'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'farm_labor_desired_consumption = '
                    'farm_grain_desired_production * 1'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'farm_labor_desired_consumption'
                ),
                'grain': True,
            },
            {
                'formula': (
                    'farm_profit = farm_grain_production *'
                    ' (farm_profit_per_unit - market_fee_per_unit)'
                ),
                'grain': True,
            },
            {
                'formula': 'farm_tax = max(0, farm_profit * government_tax)',
                'grain': True,
            },
            {
                'formula': 'farm_taxed_profit = farm_profit - farm_tax',
                'grain': True,
            },
            {
                'formula': (
                    'farm_capital = farm_capital + min(farm_income,'
                    ' government_capital) + farm_taxed_profit'
                ),
                'grain': True,
            },
            {
                'formula': 'market_capital = market_capital - farm_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(farm_income, government_capital) + farm_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + farm_grain_production *'
                    ' market_grain_price'
                ),
            },
            {
                'formula': 'farm_hay_contribution = farm_grain_production * 1',
                'common_resource': True,
            },
        ],
        'dairyfarm_system': [
            {
                'formula': (
                    'farm_profit_per_unit = market_milk_price -'
                    ' market_labor_price'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'farm_milk_max_production = market_capital / max(0.1,'
                    ' farm_profit_per_unit-market_fee_per_unit)'
                ),
                'milk': True,
            },
            {
                'formula': (
                    "farm_milk_objective = 'Maximize profit by optimizing milk"
                    ' production considering its market price and costs of'
                    " labor.'"
                ),
                'milk': True,
            },
            {
                'formula': (
                    "milk_planning = 'Develop a plan to adjust milk production"
                    ' based on market conditions and capital while remembering'
                    ' the overall need to keep up the flow of goods in the'
                    ' economy. Increase production if profit per unit is high'
                    ' and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'milk': True,
            },
            {
                'formula': (
                    "milk_plan_sampling = 'Given the good price and demand for"
                    ' milk, and considering the moderate cost of 1 units of'
                    ' labor, the strategy is to keep up a robust production'
                    ' level to ensure a continuous flow of goods.  If the'
                    ' profit per unit is positive, the current adjustment plan'
                    ' involves increasing production by 1 units. If the profit'
                    ' per unit turns negative, we need to quickly cut'
                    " production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'milk': True},
                'milk': True,
            },
            {
                'formula': (
                    'farm_milk_production_adjustment = 1 if'
                    ' farm_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'milk': True},
                'milk': True,
            },
            {
                'formula': (
                    'farm_milk_desired_production = max(0, min(max(1.0,'
                    ' farm_milk_production + max(-0.25,'
                    ' min(farm_milk_production_adjustment, 0.25))),'
                    ' farm_capital / max(market_labor_price, 0.01),'
                    ' 5 - market_milk_inventory, (farm_capital * 0.1) /'
                    ' max(-farm_profit_per_unit, 0.01),'
                    ' (farm_capital - 1) / max(-farm_profit_per_unit,'
                    ' 0.01)))'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'farm_milk_production = max(0,'
                    ' min(farm_milk_desired_production, market_labor_inventory,'
                    ' farm_milk_max_production, common_hay_inventory))'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'market_milk_supply = market_milk_supply +'
                    ' farm_milk_production'
                ),
            },
            {
                'formula': 'farm_labor_consumption = farm_milk_production * 1',
                'milk': True,
            },
            {
                'formula': 'farm_hay_extraction = farm_milk_production * 1',
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' farm_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_milk_inventory = market_milk_inventory +'
                    ' farm_milk_production'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'farm_labor_desired_consumption = '
                    'farm_milk_desired_production * 1'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'farm_hay_desired_consumption = '
                    'farm_milk_desired_production * 1'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'farm_labor_desired_consumption'
                ),
                'milk': True,
            },
            {
                'formula': (
                    'farm_profit = farm_milk_production * (farm_profit_per_unit'
                    ' - market_fee_per_unit)'
                ),
                'milk': True,
            },
            {
                'formula': 'farm_tax = max(0, farm_profit * government_tax)',
                'milk': True,
            },
            {
                'formula': 'farm_taxed_profit = farm_profit - farm_tax',
                'milk': True,
            },
            {
                'formula': (
                    'farm_capital = farm_capital + min(farm_income,'
                    ' government_capital) + farm_taxed_profit'
                ),
                'milk': True,
            },
            {
                'formula': 'market_capital = market_capital - farm_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(farm_income, government_capital) + farm_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + farm_milk_production *'
                    ' market_milk_price'
                ),
            },
        ],
        'fishery_system': [
            {
                'formula': (
                    'fishery_profit_per_unit = market_fish_price -'
                    ' market_labor_price'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_fish_max_production = market_capital / max(0.1,'
                    ' fishery_profit_per_unit-market_fee_per_unit)'
                ),
                'fish': True,
            },
            {
                'formula': (
                    "fishery_fish_objective = 'Maximize profit by optimizing"
                    ' fish production considering its market price and costs of'
                    " labor.'"
                ),
                'fish': True,
            },
            {
                'formula': (
                    "fish_planning = 'Develop a plan to adjust fish production"
                    ' based on market conditions and capital while remembering'
                    ' the overall need to keep up the flow of goods in the'
                    ' economy. Increase production if profit per unit is high'
                    ' and cut if its negative, while make sure to always'
                    ' produce when its positive. The maximal change in'
                    " production for one step is 0.25 units.'"
                ),
                'fish': True,
            },
            {
                'formula': (
                    "fish_plan_sampling = 'Given the good price and demand for"
                    ' fish, and considering the moderate cost of 1 units of'
                    ' labor, the strategy is to keep up a robust production'
                    ' level to ensure a continuous flow of goods.  If the'
                    ' profit per unit is positive, the current adjustment plan'
                    ' involves increasing production by 1 units. If the profit'
                    ' per unit turns negative, we need to quickly cut'
                    " production to minimize losses.'"
                ),
                'use_lm': 'world_time > 1',
                'query': {'fish': True},
                'fish': True,
            },
            {
                'formula': (
                    'fishery_fish_production_adjustment = 1 if'
                    ' fishery_profit_per_unit > 0 else -1'
                ),
                'use_lm': 'world_time > 1',
                'query': {'fish': True},
                'fish': True,
            },
            {
                'formula': (
                    'fishery_fish_desired_production = max(0, min(max(1.0,'
                    ' fishery_fish_production + max(-0.25,'
                    ' min(fishery_fish_production_adjustment, 0.25))),'
                    ' fishery_capital / max(market_labor_price, 0.01),'
                    ' 5 - market_fish_inventory, (fishery_capital * 0.1) /'
                    ' max(-fishery_profit_per_unit, 0.01),'
                    ' (fishery_capital - 1) / max(-fishery_profit_per_unit,'
                    ' 0.01)))'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_fish_production = max(0,'
                    ' min(fishery_fish_desired_production,'
                    ' market_labor_inventory / 1, fishery_fish_max_production))'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'market_fish_supply = market_fish_supply +'
                    ' fishery_fish_production'
                ),
            },
            {
                'formula': (
                    'fishery_labor_consumption = fishery_fish_production * 1'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' fishery_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_fish_inventory = market_fish_inventory +'
                    ' fishery_fish_production'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_labor_desired_consumption = '
                    'fishery_fish_desired_production * 1'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'fishery_labor_desired_consumption'
                ),
            },
            {
                'formula': (
                    'fishery_profit = fishery_fish_production *'
                    ' (fishery_profit_per_unit - market_fee_per_unit)'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_tax = max(0, fishery_profit * government_tax)'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_taxed_profit = fishery_profit - fishery_tax'
                ),
                'fish': True,
            },
            {
                'formula': (
                    'fishery_capital = fishery_capital + min(fishery_income,'
                    ' government_capital) + fishery_taxed_profit'
                ),
                'fish': True,
            },
            {
                'formula': 'market_capital = market_capital - fishery_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(fishery_income, government_capital) + fishery_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + fishery_fish_production *'
                    ' market_fish_price'
                ),
            },
        ],
        'woodshop_system': [
            {
                'formula': (
                    'woodshop_profit_per_unit = market_wood_price -'
                    ' market_labor_price'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_wood_max_production = market_capital / '
                    'max(0.1, woodshop_profit_per_unit - market_fee_per_unit)'
                ),
                'wood': True,
            },
            {
                'formula': (
                    "woodshop_wood_objective = 'Maximize profit by optimizing"
                    ' wood production considering its market price and the cost'
                    " of labor.'"
                ),
                'wood': True,
            },
            {
                'formula': (
                    "wood_planning = 'Develop a plan to adjust wood production"
                    ' based on market conditions and capital. Increase'
                    ' production if profit per unit is high and cut it if'
                    ' negative. The maximal change in production for one step'
                    " is 0.25 units.'"
                ),
                'wood': True,
            },
            {
                'formula': (
                    "wood_plan_sampling = 'Given the good price and demand for"
                    ' wood, the strategy is to keep up a robust production'
                    ' level. If the profit per unit is positive, increase'
                    ' production by 0.25 units. If the profit per unit turns'
                    " negative, cut production to minimize losses.'"
                ),
                'wood': True,
                'use_lm': 'world_time > 1',
                'query': {'wood': True},
            },
            {
                'formula': (
                    'woodshop_wood_production_adjustment = 0.25 if'
                    ' woodshop_profit_per_unit > 0 else -1'
                ),
                'wood': True,
                'use_lm': 'world_time > 1',
                'query': {'wood': True},
            },
            {
                'formula': (
                    'woodshop_wood_desired_production = max(0, min(max(0.1,'
                    ' woodshop_wood_production + max(-0.25,'
                    ' min(woodshop_wood_production_adjustment, 0.25))),'
                    ' woodshop_capital / max(market_labor_price, 0.01),'
                    ' 10 - market_wood_inventory, (woodshop_capital * 0.1) /'
                    ' max(-woodshop_profit_per_unit, 0.01),'
                    ' (woodshop_capital - 1) / max(-woodshop_profit_per_unit,'
                    ' 0.01)))'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_wood_production = max(0,'
                    ' min(woodshop_wood_desired_production,'
                    ' market_labor_inventory / 1,'
                    ' woodshop_wood_max_production))'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'market_wood_supply = market_wood_supply +'
                    ' woodshop_wood_production'
                ),
            },
            {
                'formula': (
                    'woodshop_labor_consumption = woodshop_wood_production * 1'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' woodshop_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_wood_inventory = market_wood_inventory +'
                    ' woodshop_wood_production'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_labor_desired_consumption = '
                    'woodshop_wood_desired_production * 1'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'woodshop_labor_desired_consumption'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_profit = woodshop_wood_production * '
                    '(woodshop_profit_per_unit - market_fee_per_unit)'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_tax = max(0, woodshop_profit * government_tax)'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_taxed_profit = woodshop_profit - woodshop_tax'
                ),
                'wood': True,
            },
            {
                'formula': (
                    'woodshop_capital = woodshop_capital + min(woodshop_income,'
                    ' government_capital) + woodshop_taxed_profit'
                ),
                'wood': True,
            },
            {
                'formula': 'market_capital = market_capital - woodshop_profit',
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(woodshop_income, government_capital) + woodshop_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + woodshop_wood_production *'
                    ' market_wood_price'
                )
            },
        ],
        'housebuilder_system': [
            {
                'formula': (
                    'housebuilder_profit_per_unit = market_house_price - '
                    '(market_wood_price * 3 + market_labor_price * 6)'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_house_max_production = market_capital /'
                    ' max(0.1, housebuilder_profit_per_unit -'
                    ' market_fee_per_unit)'
                ),
                'house': True,
            },
            {
                'formula': (
                    "housebuilder_house_objective = 'Maximize profit by"
                    ' optimizing house production considering its market price'
                    " and the cost of wood and labor.'"
                ),
                'house': True,
            },
            {
                'formula': (
                    "house_planning = 'Develop a plan to adjust house"
                    ' production based on market conditions and capital.'
                    ' Increase production if profit per unit is high and cut it'
                    ' if negative. The maximal change in production for one'
                    " step is 0.25 units.'"
                ),
                'house': True,
            },
            {
                'formula': (
                    "house_plan_sampling = 'Given the good price and demand for"
                    ' houses, the strategy is to keep up a robust production'
                    ' level. If the profit per unit is positive, increase'
                    ' production by 0.25 units. If the profit per unit turns'
                    " negative, cut production to minimize losses.'"
                ),
                'house': True,
                'use_lm': 'world_time > 1',
                'query': {'house': True},
            },
            {
                'formula': (
                    'housebuilder_house_production_adjustment = 0.25 if'
                    ' housebuilder_profit_per_unit > 0 else -1'
                ),
                'house': True,
                'use_lm': 'world_time > 1',
                'query': {'house': True},
            },
            {
                'formula': (
                    'housebuilder_house_desired_production = max(0,'
                    ' min(max(0.025, housebuilder_house_production + max(-0.25,'
                    ' min(housebuilder_house_production_adjustment, 0.25))),'
                    ' housebuilder_capital / max(market_wood_price * 3 +'
                    ' market_labor_price * 6, 0.01), 3 - market_house_inventory,'  # pylint: disable=line-too-long
                    ' (housebuilder_capital * 0.1) / max(-housebuilder_profit_per_unit,'  # pylint: disable=line-too-long
                    ' 0.01), (housebuilder_capital - 1) /'
                    ' max(-housebuilder_profit_per_unit, 0.01)))'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_house_production = max(0,'
                    ' min(housebuilder_house_desired_production,'
                    ' market_wood_inventory / 3, market_labor_inventory / 6,'
                    ' housebuilder_house_max_production))'
                ),
                'house': True,
            },
            {
                'formula': (
                    'market_house_supply = market_house_supply +'
                    ' housebuilder_house_production'
                ),
            },
            {
                'formula': (
                    'housebuilder_wood_consumption ='
                    ' housebuilder_house_production * 3'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_labor_consumption ='
                    ' housebuilder_house_production * 6'
                ),
                'house': True,
            },
            {
                'formula': (
                    'market_wood_inventory = market_wood_inventory -'
                    ' housebuilder_wood_consumption'
                ),
            },
            {
                'formula': (
                    'market_labor_inventory = market_labor_inventory -'
                    ' housebuilder_labor_consumption'
                ),
            },
            {
                'formula': (
                    'market_house_inventory = market_house_inventory +'
                    ' housebuilder_house_production'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_labor_desired_consumption = '
                    'housebuilder_house_desired_production * 6'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_wood_desired_consumption = '
                    'housebuilder_house_desired_production * 3'
                ),
                'house': True,
            },
            {
                'formula': (
                    'market_labor_demand = market_labor_demand + '
                    'housebuilder_labor_desired_consumption'
                ),
            },
            {
                'formula': (
                    'market_wood_demand = market_wood_demand + '
                    'housebuilder_wood_desired_consumption'
                ),
            },
            {
                'formula': (
                    'housebuilder_profit = housebuilder_house_production * '
                    '(housebuilder_profit_per_unit - market_fee_per_unit)'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_tax = max(0, housebuilder_profit *'
                    ' government_tax)'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_taxed_profit = housebuilder_profit -'
                    ' housebuilder_tax'
                ),
                'house': True,
            },
            {
                'formula': (
                    'housebuilder_capital = housebuilder_capital +'
                    ' min(housebuilder_income, government_capital) +'
                    ' housebuilder_taxed_profit'
                ),
                'house': True,
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(housebuilder_income, government_capital) +'
                    ' housebuilder_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + housebuilder_house_production *'
                    ' market_house_price'
                )
            },
        ],
        'housingprovider_system': [
            {
                'formula': (
                    'housingprovider_profit_per_unit = market_housing_price - '
                    'market_house_price * 0.1'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_housing_max_production = market_capital /'
                    ' max(0.1, housingprovider_profit_per_unit -'
                    ' market_fee_per_unit)'
                ),
                'housing': True,
            },
            {
                'formula': (
                    "housingprovider_housing_objective = 'Maximize profit by"
                    ' optimizing housing production considering its market'
                    " price and the cost of houses.'"
                ),
                'housing': True,
            },
            {
                'formula': (
                    "housing_planning = 'Develop a plan to adjust housing"
                    ' production based on market conditions and capital.'
                    ' Increase production if profit per unit is high and cut it'
                    ' if negative. The maximal change in production for one'
                    " step is 0.25 units.'"
                ),
                'housing': True,
            },
            {
                'formula': (
                    "housing_plan_sampling = 'Given the good price and demand"
                    ' for housing, the strategy is to keep up a robust'
                    ' production level. If the profit per unit is positive,'
                    ' increase production by 0.25 units. If the profit per unit'
                    " turns negative, cut production to minimize losses.'"
                ),
                'housing': True,
                'use_lm': 'world_time > 1',
                'query': {'housing': True},
            },
            {
                'formula': (
                    'housingprovider_housing_production_adjustment = 0.25 if'
                    ' housingprovider_profit_per_unit > 0 else -1'
                ),
                'housing': True,
                'use_lm': 'world_time > 1',
                'query': {'housing': True},
            },
            {
                'formula': (
                    'housingprovider_housing_desired_production = max(0,'
                    ' min(max(0.1, housingprovider_housing_production +'
                    ' max(-0.25, min(housingprovider_housing_production_adjustment,'  # pylint: disable=line-too-long
                    ' 0.25))), housingprovider_capital / market_house_price, 10 -'    # pylint: disable=line-too-long
                    ' market_housing_inventory,'
                    ' (housingprovider_capital - 1) /'
                    ' max(-housingprovider_profit_per_unit, 0.01)))'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_housing_production = max(0, min('
                    'housingprovider_housing_desired_production, '
                    'housingprovider_housing_max_production, '
                    'market_house_inventory / 0.1))'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'market_housing_supply = market_housing_supply +'
                    ' housingprovider_housing_production'
                ),
            },
            {
                'formula': (
                    'housingprovider_house_consumption ='
                    ' housingprovider_housing_production * 0.1'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'market_house_inventory = market_house_inventory -'
                    ' housingprovider_house_consumption'
                ),
            },
            {
                'formula': (
                    'market_housing_inventory = market_housing_inventory +'
                    ' housingprovider_housing_production'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_house_desired_consumption = '
                    'housingprovider_housing_desired_production * 0.1'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'market_house_demand = market_house_demand + '
                    'housingprovider_house_desired_consumption'
                ),
            },
            {
                'formula': (
                    'housingprovider_profit ='
                    ' housingprovider_housing_production *'
                    ' (housingprovider_profit_per_unit - market_fee_per_unit)'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_tax = max(0, housingprovider_profit *'
                    ' government_tax)'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_taxed_profit = housingprovider_profit -'
                    ' housingprovider_tax'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'housingprovider_capital = housingprovider_capital +'
                    ' min(housingprovider_income, government_capital) +'
                    ' housingprovider_taxed_profit'
                ),
                'housing': True,
            },
            {
                'formula': (
                    'market_capital = market_capital - housingprovider_profit'
                ),
            },
            {
                'formula': (
                    'government_capital = max(0, government_capital -'
                    ' min(housingprovider_income, government_capital) +'
                    ' housingprovider_tax)'
                ),
                'government': True,
            },
            {
                'formula': (
                    'world_gdp = world_gdp + housingprovider_housing_production'
                    ' * market_housing_price'
                )
            },
        ]
    },
}
