from strategies.default.strategy import *
from strategies.my_strategy.strategy import *
from strategies.my_rule_strategy.strategy import *
from strategies.proportional.strategy import *
from strategies.turnspeed.strategy import *
from strategies.manual.strategy import *
from strategies.my_deep_strategy.strategy import *
from strategies.my_ml_strategy.strategy import *
from strategies.binary.strategy import *

# setup steering strategies
strategy_list = [
    Default,
    MyStrategy,
    # MyRuleStrategy,
    # MyMlStrategy,
    # MyDeepStrategy,
    # TurnSpeed,
    # Proportional,
    # Manual,
    # Binary,
]