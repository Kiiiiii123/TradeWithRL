import os
# 实现python对象的持久化存储
import pickle
import pandas as pd
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import PPO2
from env.CustomEnv import StockTradingEnv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

font = fm.FontProperties(fname='font/wqy-microhei.ttc')
# plt.rc('font', family='Source Han Sans CN')
plt.rcParams['axes.unicode_minus'] = False

def train_stock_trading(stock_file):
    day_profits = []
    df_train = pd.read_csv(stock_file)
    df_train = df_train.sort_values('date')

    env =DummyVecEnv([lambda: StockTradingEnv(df_train)])
    model = PPO2(MlpPolicy, env, verbose=0, tensorboard_log='./log')
    model.learn(total_timesteps=int(1e4))

    df_test =



def test_stock_trading()

if __name__ == '__main__':
