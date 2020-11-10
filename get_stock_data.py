import baostock as bs
import os
# baostock返回的数据类型主要为DataFrame
import pandas as pd


def mkdir(directory):
    """
    创建存放训练和测试数据的文件目录
    """
    if not os.path.exists(directory):
        os.makedirs(directory)


class Downloader(object):
    """
    用于从baostock平台上下载股票证券数据
    """
    def __init__(self,
                 output_dir,
                 date_start='1990-01-01',
                 date_end='2020-03-23'):
        bs.login()
        self.output_dir = output_dir
        self.date_start = date_start
        self.date_end = date_end
        self.fields = "date,code,open,high,low,close,volume,amount," \
                      "adjustflag,turn,tradestatus,pctChg,peTTM," \
                      "pbMRQ,psTTM,pcfNcfTTM,isST"

    def get_codes_by_date(self, date):
        print(date)
        # 获取指定交易日期所有股票交易列表
        stock_rs = bs.query_all_stock(date)
        # 返回当日股票交易DataFrame数据
        stock_df = stock_rs.get_data()
        print(stock_df)
        return stock_df

    def exit(self):
        bs.logout()

    def download(self):
        stock_df = self.get_codes_by_date(self.date_end)
        for index, row in stock_df.iterrows():
            # f表示格式化处理
            print(f'processing{row["code"]} {row["code_name"]}')
            # 获取股票的日K线数据
            df_code = bs.query_history_k_data_plus(row["code"], self.fields,
                                                   self.date_start,
                                                   self.date_end).get_data()
            df_code.to_csv(f'{self.output_dir}/{row["code"]}.{row["code_name"]}.csv', index=False)
        self.exit()


if __name__ == '__main__':
    # 获取全部股票的日K线数据
    mkdir('./stockdata/train')
    downloader = Downloader('./stockdata/train', date_start='1990-01-01', date_end='2019-11-29')
    downloader.download()

    mkdir('./stockdata/test')
    downloader = Downloader('./stockdata/test', date_start='2019-12-01', date_end='2019-12-31')
    downloader.download()



