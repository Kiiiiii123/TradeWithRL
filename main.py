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
# pylot使用rc配置文件来自定义图形的各种默认属性
plt.rcParams['axes.unicode_minus'] = False


def train_stock_trading(stock_file):
    day_profits = []
    df_train = pd.read_csv(stock_file)
    df_train = df_train.sort_values('date')

    env = DummyVecEnv([lambda: StockTradingEnv(df_train)])
    model = PPO2(MlpPolicy, env, verbose=0, tensorboard_log='./log')
    model.learn(total_timesteps=int(1e4))

    df_test = pd.read_csv(stock_file.replace('train', 'test'))

    env = DummyVecEnv([lambda: StockTradingEnv(df_test)])
    obs = env.reset()
    for i in range(len(df_test) - 1):
        action, _status = model.predict(obs)
        obs, reward, done, info = env.step(action)
        profit = env.render()
        day_profits.append(profit)
        if done:
            break

    return day_profits


def find_file(path, name):
    # print(path, name)
    # os.walk() 方法是简单易用的文件、目录遍历器
    for root, dirs, files in os.walk(path):
        for file_name in files:
            if name in file_name:
                return os.path.join(root, file_name)


def test_stock_trading(stock_code):
    stock_file = find_file('./stockdata/train', str(stock_code))

    daily_profits = train_stock_trading(stock_file)
    fig, ax = plt.subplots()
    ax.plot(daily_profits, '-o', label=stock_code, marker='o', ms=10, alpha=0.7, mfc='orange')
    ax.grid()
    plt.xlabel('step')
    plt.ylabel('profit')
    ax.legend(prop=font)
    # plt.show()
    plt.savefig(f'./img/{stock_code}.png')


def batch_test():
    start_code = 600000
    max_num = 3000
    group_results = []

    for stock_code in range(start_code, start_code + max_num):
        stock_file = find_file('./stockdata/train', str(stock_code))
        if stock_file:
            try:
                profits = train_stock_trading(stock_file)
                group_results.append(profits)
            except Exception as error:
                print(error)

    with open(f'code-{start_code}-{start_code + max_num}.pkl', 'wb') as f:
        pickle.dump(group_results, f)


if __name__ == '__main__':
    # test_stock_trading('sh.600036')
    # test_stock_trading('sz.002714')
    batch_test()









