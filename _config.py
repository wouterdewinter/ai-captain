from strategies.default import *
from strategies.my_strategy import *

from user_strategies.martin_strategy.strategy import *
from user_strategies.martin_rule_strategy.strategy import *
from user_strategies.martin_ml_strategy.strategy import *
from user_strategies.martin_deep_strategy.strategy import *

from user_strategies.justin_strategy.strategy import *
from user_strategies.justin_rule_strategy.strategy import JustinRuleStrategy
from user_strategies.justin_deep_strategy.strategy import *
from user_strategies.justin_ml_strategy.strategy import *

from user_strategies.stephan_strategy.strategy import *
from user_strategies.stephan_rule_strategy.strategy import *
from user_strategies.stephan_deep_strategy.strategy import *
from user_strategies.stephan_ml_strategy.strategy import *

from user_strategies.thomasg_strategy.strategy import *
from user_strategies.thomasg_deep_strategy.strategy import *

from user_strategies.thomas_strategy.strategy import *
from user_strategies.thomas_rule_strategy.strategy import *
from user_strategies.thomas_deep_strategy.strategy import *
from user_strategies.thomas_ml_strategy.strategy import *

from user_strategies.bastian_strategy.strategy import *
from user_strategies.bastian_rule_strategy.strategy import *
from user_strategies.bastian_deep_strategy.strategy import *
from user_strategies.bastian_ml_strategy.strategy import *

# setup steering strategies
strategy_list = [
    # Default,
    # MyStrategy,
    # MyRuleStrategy,
    # MyMlStrategy,
    # MyDeepStrategy,
    # TurnSpeed,
    # Proportional,
    # Manual,
    # Binary,

    #MartinStrategy,
    #MartinRuleStrategy,
    #MartinMlStrategy,
    MartinDeepStrategy,

    #JustinStrategy,
    #JustinRuleStrategy,
    #JustinMlStrategy,
    JustinDeepStrategy,

    #StephanStrategy,
    #StephanRuleStrategy,
    #StephanMlStrategy,
    StephanDeepStrategy,

    #ThomasgStrategy,
    ThomasgDeepStrategy,

    #ThomasStrategy,
    ThomasDeepStrategy,
    #ThomasRuleStrategy,
    #ThomasMlStrategy,

    #BastianStrategy,
    #BastianRuleStrategy,
    #BastianMlStrategy,
    BastianDeepStrategy,

]

