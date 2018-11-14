from strategies.default.strategy import *
from strategies.my_strategy.strategy import *
from strategies.proportional.strategy import *
from strategies.turnspeed.strategy import *
from strategies.manual.strategy import *
from strategies.my_deep_strategy.strategy import *
from strategies.my_ml_strategy.strategy import *

# setup steering strategies
strategy_list = [
    Default,
    MyStrategy,
    #MyMlStrategy,
    #MyDeepStrategy,
    #TurnSpeed,
    #Proportional,
    #Manual,
]