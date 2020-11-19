import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pickle

font = fm.FontProperties(fname='./font/wqy-microhei.ttc')


def pie(profit_data):
    # 饼图显示盈亏占比
    # 每一块饼图外侧显示的说明文字
    labels = 'Profit', 'Loss', '0'
    sizes = [0, 0, 0]
    for p in profit_data:
        if p > 0:
            sizes[0] += 1
        if p < 0:
            sizes[1] += 1
        else:
            sizes[2] += 1
    # 每一块饼图离开中心距离
    explode = [0.1, 0.05, 0.05]
    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    # 使每一块饼图长宽相等
    ax.axis('equal')
    plt.legend(prop=font)
    plt.savefig('./img/pie.png')
    # plt.show()


def hist(profit_data):
    # 柱状图显示盈亏量
    n_bins = 150
    fig, ax = plt.subplots()
    ax.hist(profit_data, bins=n_bins, density=True)
    plt.savefig('./img/hist.png')
    # plt.show()


if __name__ == '__main__':
    with open('./code-600000-603000.pkl', 'rb') as f:
        results = pickle.load(f)

    is_profit = [p[-1] for p in results]
    print(len(is_profit))

    pie(is_profit)
    hist(is_profit)



