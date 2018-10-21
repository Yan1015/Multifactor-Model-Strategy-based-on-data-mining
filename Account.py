# -*- coding: utf-8 -*-
"""
Created on 2016/11/30 20:00 by Yzj
"""


import pickle as pkl
import pandas as pd
import datetime
import os
import numpy as np
import copy
import math

from Portfolio import Portfolio


class Account:

    def __init__(self, dct_dct_my_port, str_output_path, int_holding_day, int_or_str_change_day, dtm_begin_date, dtm_end_date, int_group_num, str_description, trading_date_list, dct_dct_my_port_weight):

        self.this_program_start_time = datetime.datetime.now()
        self.str_prog_beg_time = self.this_program_start_time.strftime('%Y%m%d%H%M%S')
        print('begin: '+self.str_prog_beg_time)

        self.str_description = str_description

        self.raw_return_path = 'update_raw_data\\' # 这是那存储基本数据的文件夹
        self.dct_dct_my_port = dct_dct_my_port
        self.dct_dct_my_port_weight = dct_dct_my_port_weight
        self.str_output_path = str_output_path
        self.int_holding_day = int_holding_day
        self.int_or_str_change_day = int_or_str_change_day
        self.dtm_begin_date = dtm_begin_date
        self.dtm_end_date = dtm_end_date
        self.int_group_num = int_group_num

        all_data_clean = self.load_market_data_from_pkl() # 从已经处理过的pkl文件里面读取基本数据

        self.mtx_stk_ret = all_data_clean['stk_ret_matrix']   # 这是股票每天return的记录
        self.mtx_stk_cap = all_data_clean['stk_mkt_cap_matrix'] # 这是股票每天mkt_cap的记录
        self.mtx_stk_cap_fillna = self.mtx_stk_cap.fillna(0)
        self.mtx_stk_cap_shift1 = self.mtx_stk_cap.shift(1).fillna(0) # 这是将每天股票mkt_cap的记录存储上一天mkt_cap的结果，使用在新交易portfolio的那一天，用的是前一天的mkt_cap作为weight(这里初始文件会给到weight所以不会用到)
        self.mtx_idx_ret = all_data_clean['idx_ret_matrix']     # 这是股票每天index_ret的记录
        self.mtx_mmb_factor_ret = all_data_clean['mmb_factor_matrix'] # 这是股票每天mmb_factor的记录
        self.dct_beta_f2 = all_data_clean['beta_f2_dict']        # 这是股票每天2f_beta的记录
        self.dct_beta_f1 = all_data_clean['beta_f1_matrix']      # 这是股票每天1f_beta的记录

        self.dct_beta_f1_shift1 = dict()                               # 这是将每天股票1f_beta的记录存储上一天1f_beta的结果，使用在新交易portfolio的那一天，用的是前一天的1f_beta作为beta
        self.dct_beta_f1_shift1['beta_s'] = self.dct_beta_f1.shift(1)




        self.dct_beta_f2_shift1 = dict()                               # 这是将每天股票2f_beta的记录存储上一天2f_beta的结果，使用在新交易portfolio的那一天，用的是前一天的2f_beta作为beta
        for key, value in self.dct_beta_f2.items():
            self.dct_beta_f2_shift1[key] = value.shift(1)
        self.dct_beta_f2_shift1['beta_s'].fillna(1, inplace=True)
        self.dct_beta_f2_fillna = dict()
        for key, value in self.dct_beta_f2.items():
            self.dct_beta_f2_fillna[key] = value
        self.dct_beta_f2_fillna['beta_s'].fillna(1, inplace=True)

        self.lst_holding_days = self.get_holding_days(self.mtx_idx_ret.index)
        # self.lst_trading_days = self.get_trading_days(self.lst_holding_days)
        self.lst_trading_days = trading_date_list

        self.lst_my_portfolios = []  # list of list of portfolios
        for idx in range(self.int_group_num):
            self.lst_my_portfolios.append([])

        self.mtx_return_record = pd.DataFrame([[0]*self.int_group_num]*len(self.lst_holding_days), index=self.lst_holding_days, columns=list(range(self.int_group_num)))  # 这是记录每天portfolio_return的结果

    def get_holding_days(self, idx_timestamp):
        lst_timestamp = list(idx_timestamp[(idx_timestamp>=self.dtm_begin_date) & (idx_timestamp<=self.dtm_end_date)])
        return [datetime.datetime(x.year, x.month, x.day) for x in lst_timestamp]

    def get_trading_days(self, lst_dtm_holding_days):
        if isinstance(self.int_or_str_change_day, str):
            if self.int_or_str_change_day == 'Friday':
                return [l_h_d for l_h_d in lst_dtm_holding_days if l_h_d.weekday() == 4]
                # return [l_h_d for l_h_d in lst_dtm_holding_days]
        elif isinstance(self.int_or_str_change_day, int):
            return [lst_dtm_holding_days[idx] for idx in range(0, len(lst_dtm_holding_days), self.int_or_str_change_day)]
        else:
            return []

    def load_market_data_from_csv(self):
        pass

    def load_market_data_from_pkl(self):
        f = open(self.raw_return_path+'clean_data_pickle.pkl', 'rb')
        all_data_clean = pkl.load(f)
        f.close()

        return all_data_clean

    def start_trading(self):
        print(self.str_description)
        for this_holding_day in self.lst_holding_days:
            print(this_holding_day)
            self.update_portfolio(this_holding_day)
            self.mtx_return_record.loc[this_holding_day, :] = self.calculate_return(this_holding_day)  # return of 1-10 groups

    def update_portfolio(self, dtm_this_holding_day):
        new_port_rcd = []  # list of list of portfolios
        for idx in range(self.int_group_num):
            new_port_rcd.append([])
        # 用复制的方法删除portfolio
        for idx in range(self.int_group_num):
            for this_port in self.lst_my_portfolios[idx]:
                assert isinstance(this_port, Portfolio)
                if this_port.int_trading_times >= self.int_holding_day + 1:
                    pass
                else:
                    new_port_rcd[idx].append(this_port)
        self.lst_my_portfolios = new_port_rcd
        # 增加portfolio
        if dtm_this_holding_day in self.lst_trading_days:
            if dtm_this_holding_day in self.dct_dct_my_port.keys():
                for idx in range(self.int_group_num):
                    new_port = Portfolio(self.dct_dct_my_port[dtm_this_holding_day][idx], dtm_this_holding_day, self.mtx_stk_ret, self.mtx_stk_cap_shift1)
                    if self.str_description == 'value_weight_1fresult':
                        new_port.update_beta_weight_1f(self.dct_beta_f1_shift1)
                    if 'value_weight_2fresult' in self.str_description:
                        new_port.update_beta_weight_2f(self.dct_beta_f2_shift1)

                    # print('add'+str(len(new_port.lst_int_this_port)))
                    self.lst_my_portfolios[idx].append(new_port)

    def calculate_return(self, this_holding_day):
        lst_dbl_ret = [0.0] * self.int_group_num

        for idx in range(self.int_group_num):
            this_group_ret = []

            for this_port in self.lst_my_portfolios[idx]:
                assert isinstance(this_port, Portfolio)
                if self.str_description == 'value_weight_1fresult':
                    this_port_ret_tmp = this_port.cal_port_ret_1f(this_holding_day, self.mtx_stk_ret, self.mtx_idx_ret)
                this_port_ret_tmp = this_port.cal_port_ret_2f(this_holding_day, self.mtx_stk_ret, self.mtx_idx_ret, self.mtx_mmb_factor_ret, self.dct_beta_f2_shift1)
                if self.str_description == 'value_weight_rawresult':
                    this_port_ret_tmp = this_port.cal_port_ret_raw(this_holding_day, self.mtx_stk_ret)
                if isinstance(this_port_ret_tmp, float):
                    this_group_ret.append(this_port_ret_tmp)


            print(this_group_ret)
            print(0)

            lst_dbl_ret[idx] = sum(this_group_ret)/len(this_group_ret) if len(this_group_ret)!=0 else 0.0

        return lst_dbl_ret

    def report(self):
        print('report')
        outputpath = self.str_output_path+self.str_description
        if not os.path.exists(self.str_output_path):
            os.mkdir(self.str_output_path)
        if not os.path.exists(outputpath):
            os.mkdir(outputpath)
            print(outputpath+'\\'+'port_daily_return_record.csv')
            self.mtx_return_record.to_csv(outputpath+'\\'+'port_daily_return_record.csv')

            self.mtx_return_record['winner_loser'] = self.mtx_return_record[self.mtx_return_record.columns[0]] - self.mtx_return_record[self.mtx_return_record.columns[-1]]

            group_ret_mean_daily = (np.exp(np.log(self.mtx_return_record + 1).resample('1D', how='sum')) - 1).mean() * 245
            group_ret_std_daily = (np.exp(np.log(self.mtx_return_record + 1).resample('1D', how='sum')) - 1).std() * math.sqrt(245)
            pd_daily = pd.concat([group_ret_mean_daily, group_ret_std_daily], axis=1, keys=['mean', 'std'])
            pd_daily['sharpe'] = pd_daily['mean'] / pd_daily['std']
            print(outputpath + '\\' + 'port_daily_stat.csv')
            pd_daily.to_csv(outputpath + '\\' + 'port_daily.csv')
            print(pd_daily['sharpe'])



            group_ret_mean_Weekly = (np.exp(np.log(self.mtx_return_record+1).resample('1W', how='sum'))-1).mean() * 52
            group_ret_std_Weekly = (np.exp(np.log(self.mtx_return_record+1).resample('1W', how='sum'))-1).std() * math.sqrt(52)
            pd_weekly = pd.concat([group_ret_mean_Weekly, group_ret_std_Weekly], axis=1, keys=['mean', 'std'])
            pd_weekly['sharpe'] = pd_weekly['mean']/pd_weekly['std']
            print(outputpath+'\\'+'port_weekly_stat.csv')
            pd_weekly.to_csv(outputpath+'\\'+'port_weekly.csv')
            print(pd_weekly['sharpe'])

            group_ret_mean_weekly = (np.exp(np.log(self.mtx_return_record + 1).resample('1W', how='mean')) - 1)
            group_ret_std_weekly = self.mtx_return_record.resample('1W', how='std')
            group_ret_sharpe_weekly = group_ret_mean_weekly / group_ret_std_weekly * math.sqrt(252)
            pd_weekly = pd.concat([group_ret_mean_weekly, group_ret_std_weekly, group_ret_sharpe_weekly], axis=1, keys=['mean', 'std', 'sharpe'])
            print(outputpath + '\\' + 'port_weekly_record.csv')
            pd_weekly.to_csv(outputpath + '\\' + 'port_weekly_record.csv')



            group_ret_mean_Monthly = (np.exp(np.log(self.mtx_return_record + 1).resample('1M', how='sum')) - 1).mean() * 12
            group_ret_std_Monthly = (np.exp(np.log(self.mtx_return_record + 1).resample('1M', how='sum')) - 1).std() * math.sqrt(12)
            pd_monthly = pd.concat([group_ret_mean_Monthly, group_ret_std_Monthly], axis=1, keys=['mean', 'std'])
            pd_monthly['sharpe'] = pd_monthly['mean'] / pd_monthly['std']
            print(outputpath + '\\' + 'port_monthly_stat.csv')
            pd_monthly.to_csv(outputpath + '\\' + 'port_monthly.csv')
            print(pd_monthly['sharpe'])


            group_ret_mean_monthly = (np.exp(np.log(self.mtx_return_record+1).resample('1M', how='mean'))-1)
            group_ret_std_monthly = self.mtx_return_record.resample('1M', how='std')
            group_ret_sharpe_monthly = group_ret_mean_monthly / group_ret_std_monthly * math.sqrt(252)
            pd_monthly = pd.concat([group_ret_mean_monthly, group_ret_std_monthly, group_ret_sharpe_monthly], axis=1, keys=['mean', 'std', 'sharpe'])
            print(outputpath+'\\'+'port_monthly_record.csv')
            pd_monthly.to_csv(outputpath+'\\'+'port_monthly_record.csv')

            group_ret_mean_Yearly = (np.exp(np.log(self.mtx_return_record + 1).resample('12M', how='sum')) - 1).mean()
            group_ret_std_Yearly = (np.exp(np.log(self.mtx_return_record + 1).resample('12M', how='sum')) - 1).std()
            pd_yearly = pd.concat([group_ret_mean_Yearly, group_ret_std_Yearly], axis=1, keys=['mean', 'std'])
            pd_yearly['sharpe'] = pd_yearly['mean'] / pd_yearly['std']
            print(outputpath + '\\' + 'port_yearly_stat.csv')
            pd_yearly.to_csv(outputpath + '\\' + 'port_yearly.csv')
            print(pd_yearly['sharpe'])



            group_ret_mean_yearly = (np.exp(np.log(self.mtx_return_record+1).resample('12M', how='sum', closed='left', label='right'))-1)
            group_ret_std_yearly = self.mtx_return_record.resample('12M', how='std', closed='left', label='right') * math.sqrt(252)
            group_ret_sharpe_yearly = group_ret_mean_yearly / group_ret_std_yearly
            pd_yearly = pd.concat([group_ret_mean_yearly, group_ret_std_yearly, group_ret_sharpe_yearly], axis=1, keys=['mean', 'std', 'sharpe'])
            print(outputpath+'\\'+'port_yearly_record.csv')
            pd_yearly.to_csv(outputpath+'\\'+'port_yearly_record.csv')

            # group_ret_cumsum_monthly = self.mtx_return_record.resample('1M', how='sum').cumsum() * 12
            # # group_ret_std_monthly = self.mtx_return_record.resample('M', how='std') * math.sqrt(252)
            # # pd_monthly = pd.concat([group_ret_mean_monthly, group_ret_std_monthly], axis=1, keys=['mean', 'std'])
            # group_ret_cumsum_monthly.to_csv(outputpath+'\\'+'port_monthly_cumsum.csv')


            my_str = 'start time: %s, end time: %s\ndescription: %s\nholding_day: %d\nchange_day: %s\ngroup num:%d\n'\
                  % (self.dtm_begin_date.strftime('%Y%m%d'), self.dtm_end_date.strftime('%Y%m%d'), self.str_description, self.int_holding_day,
                     str(self.int_or_str_change_day), self.int_group_num)
            my_str += 'program start time: %s, program end time: %s'%(self.this_program_start_time.strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            f = open(outputpath+'\\'+'ReadMe.txt', 'w')
            f.write(my_str)
            f.close()


