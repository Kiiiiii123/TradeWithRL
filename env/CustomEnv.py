import random
import gym
from gym import spaces
import numpy as np

# 最大账户余额
MAX_ACCOUNT_BALANCE = 2147483647
# 最大持股数
MAX_NUM_SHARES = 2147483647
# 最高股价
MAX_SHARE_PRICE = 5000
# 最大交易量
MAX_VOLUME = 1000e8
MAX_AMOUNT = 3e10
MAX_OPEN_POSITIONS = 5
MAX_STEPS = 20000
MAX_DAY_CHANGE = 1

INITIAL_ACCOUNT_BALANCE = 10000


class StockTradingEnv(gym.Env):
    """基于gym构建简易的股票交易环境"""
    metadata = {'render.modes': ['human']}

    def __init__(self, df):
        super(StockTradingEnv, self).__init__()

        self.df = df
        self.reward_range = (0, MAX_ACCOUNT_BALANCE)
        # 动作空间格式为买入x%，卖出x%以及持有
        self.action_space = spaces.Box(low=[0, 0], high=[3, 1], dtype=np.float16)
        # 观测到的为最近五个价格的OHCL值
        self.observation_space = spaces.Box(
            low=0, high=1, shape=[19, ], dtype=np.float16)

    def _next_observation(self):
        # 注意归一化处理
        obs = np.array([
            self.df.loc[self.current_step, 'open'] / MAX_SHARE_PRICE,
            self.df.loc[self.current_step, 'high'] / MAX_SHARE_PRICE,
            self.df.loc[self.current_step, 'low'] / MAX_SHARE_PRICE,
            self.df.loc[self.current_step, 'close'] / MAX_SHARE_PRICE,
            self.df.loc[self.current_step, 'volume'] / MAX_VOLUME,
            self.df.loc[self.current_step, 'amount'] / MAX_AMOUNT,
            self.df.loc[self.current_step, 'adjustflag'] / 10,
            self.df.loc[self.current_step, 'tradestatus'] / 1,
            self.df.loc[self.current_step, 'pctChg'] / 100,
            self.df.loc[self.current_step, 'peTTM'] / 1e4,
            self.df.loc[self.current_step, 'pbMRQ'] / 100,
            self.df.loc[self.current_step, 'psTTM'] / 100,
            self.df.loc[self.current_step, 'pctChg'] / 1e3,
            self.balance / MAX_ACCOUNT_BALANCE,
            self.max_net_worth / MAX_ACCOUNT_BALANCE,
            self.shares_held / MAX_NUM_SHARES,
            # 买入成本
            self.cost_basis / MAX_SHARE_PRICE,
            self.total_shares_sold / MAX_NUM_SHARES,
            self.total_sales_value / (MAX_NUM_SHARES * MAX_SHARE_PRICE)
        ])

        return obs

    def _take_action(self, action):
        # 将当前股价设置为时间步下的随机价格
        current_price = random.uniform(
            self.df.loc[self.current_step, 'open'], self.df.loc[self.current_step, 'close'])

        action_type = action[0]
        action_amount = action[1]

        if action_type < 1:
            # 用账户余额的x%买入股票
            total_possible = int(self.balance / current_price)
            shares_bought = int(total_possible * action_amount)
            prev_cost = self.cost_basis * self.shares_held
            additional_cost = shares_bought * current_price

            self.balance -= additional_cost
            self.cost_basis = (
                prev_cost + additional_cost) / (self.shares_held + shares_bought)
            self.shares_held += shares_bought

        if action_type < 2:
            # 卖出x%的持有股票
            shares_sold = int(self.shares_held * action_amount)
            self.balance += shares_sold * current_price
            self.shares_held -= shares_sold
            self.total_shares_sold += shares_sold
            self.total_sales_value += shares_sold * current_price

        self.net_worth = self.balance + self.shares_held * current_price
        if self.net_worth > self.max_net_worth:
            self.max_net_worth = self.net_worth

        if self.shares_held == 0:
            self.cost_basis = 0

    def step(self, action):
        self._take_action(action)
        done = False

        self.current_step += 1
        if self.current_step > len(self.df.loc[:, 'open'].values) - 1:
            # 循环训练
            self.current_step = 0
            # done = True

        delay_modifier = (self.current_step / MAX_STEPS)
        reward = self.net_worth - INITIAL_ACCOUNT_BALANCE
        reward = 1 if reward > 0 else -100

        if self.net_worth <= 0:
            done = True

        obs = self._next_observation()

        return obs, reward, done, {}

    def reset(self, new_df=None):
        self.balance = INITIAL_ACCOUNT_BALANCE
        self.net_worth = INITIAL_ACCOUNT_BALANCE
        self.max_net_worth  = INITIAL_ACCOUNT_BALANCE
        self.shares_held = 0
        self.cost_basis = 0
        self.total_shares_sold = 0
        self.total_shares_sold = 0

        # 将测试数据集传递到环境中
        if new_df:
            self.df = new_df

        # self.currebt_step = random.randint(
        #   0, len(self.df.loc[:, 'open'].values) - 6)
        self.current_step = 0

        return self._next_observation()

    def render(self):


