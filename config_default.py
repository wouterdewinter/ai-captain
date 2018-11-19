from strategies import default
from strategies import my_strategy
#from user_strategies import my_strategy

# setup steering strategies
strategy_list = [
    default.Default,
    my_strategy.MyStrategy,
    my_strategy.MyRuleStrategy,
    my_strategy.MyMlStrategy,
    my_strategy.MyDeepStrategy,
    # default.TurnSpeed,
    # default.Proportional,
    # default.Manual,
    # default.Binary,
]