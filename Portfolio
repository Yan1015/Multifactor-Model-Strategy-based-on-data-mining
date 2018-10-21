# -*- coding: utf-8 -*-
"""
Created on 2016/11/30 20:00 by Yzj

"""

import pandas as pd

from Util import cal_weighted_ret
import datetime



class Portfolio:
    def __init__(self, lst_int_this_port, dtm_first_trading_day, mtx_stk_ret, mtx_stk_cap):
        self.int_trading_times = 0
        self.lst_int_this_port = []
        self.int_trading_times = 0
        self.lst_int_this_port = []

        self.weight = []
        lst_this_port_weight = list(mtx_stk_cap.loc[dtm_first_trading_day, lst_int_this_port])

        # df = mtx_stk_ret.loc[dtm_first_trading_day, lst_int_this_port]             # 如果交易日那一天 把 停牌的股票删去，就用这个  或删除涨跌停
        #
        #
        # for index in range(len(lst_int_this_port)):
        #    if pd.notnull(df[lst_int_this_port[index]]):
        #        self.lst_int_this_port.append(int(lst_int_this_port[index]))
        #        self.weight.append(lst_this_port_weight[index])

        df = mtx_stk_ret.loc[dtm_first_trading_day, lst_int_this_port]           # 如果  删除涨跌停##

        for index in range(len(lst_int_this_port)):
            if abs(df[lst_int_this_port[index]]) <= 0.099:
                self.lst_int_this_port.append(int(lst_int_this_port[index]))
                self.weight.append(lst_this_port_weight[index])#

        self.weight = [1] * len(self.weight)       # equal_weight

        #for index in range(len(lst_int_this_port)):                                 # 如果交易日那一天 不把 停牌的股票删去，就用这个
        #    self.lst_int_this_port.append(int(lst_int_this_port[index]))
        #    self.weight.append(lst_this_port_weight[index])#

        #self.weight = [1] * len(self.weight)  # equal_weight


        self.dtm_first_trading_day = dtm_first_trading_day
        self.mkt_beta = 0.0
        self.mmb_beta = 0.0
        self.dbl_mkt_ret = 0.0
        self.dbl_mmb_ret = 0.0
        self.ret_list = [0] * len(self.lst_int_this_port)
        self.cumulative_ret = 1

    def __str__(self):
        return str(self.lst_int_this_port)

    def __repr__(self):
        return self.__str__()

    def cal_port_ret_1f(self, dtm_trading_day, mtx_stk_ret, mtx_idx_ret):
        if not self.lst_int_this_port:
            self.int_trading_times += 1
            return 'nan'
        else:
            if self.int_trading_times >= 1:
                self.int_trading_times += 1
                ret_list = list(mtx_stk_ret.loc[dtm_trading_day, self.lst_int_this_port].fillna(0))
                for index in range(len(ret_list)):
                    self.ret_list[index] = (1 + self.ret_list[index]) * (1 + ret_list[index]) - 1
                dbl_raw_ret = cal_weighted_ret(self.ret_list, self.weight)
                self.dbl_mkt_ret = (1 + self.dbl_mkt_ret) * (1 + mtx_idx_ret.loc[dtm_trading_day, 'ret_hs300_dty']) -1

                new_ret = (1 + dbl_raw_ret - self.mkt_beta * self.dbl_mkt_ret) / self.cumulative_ret - 1
                self.cumulative_ret = 1 + dbl_raw_ret - self.mkt_beta * self.dbl_mkt_ret
                return new_ret
            else:
                self.int_trading_times += 1
                return 'nan'

    def cal_port_ret_2f(self, dtm_trading_day, mtx_stk_ret, mtx_idx_ret, mtx_mmb_factor_ret, dct_beta_f2):
        if not self.lst_int_this_port:
            self.int_trading_times += 1
            return 'nan'
        else:
            if self.int_trading_times >= 1:
                self.int_trading_times += 1

                ret_list = list(mtx_stk_ret.loc[dtm_trading_day, self.lst_int_this_port].fillna(0))

                # if dtm_trading_day == datetime.datetime(2016, 3, 4, 0, 0, 0):
                #     df = pd.DataFrame({'id': self.lst_int_this_port, 'ret': ret_list, 'weight': self.weight,
                #                        'ret_hs300_dty': [mtx_idx_ret.loc[dtm_trading_day, 'ret_hs300_dty']] * len(ret_list),
                #                        'size_MMB_industryHSI300w_v': mtx_mmb_factor_ret.loc[dtm_trading_day, 'size_MMB_industryHSI300w_v'],
                #                        'beta_s': list(dct_beta_f2['beta_s'].loc[self.dtm_first_trading_day, self.lst_int_this_port].fillna(1)),
                #                        'beta_s_mmb_ind': list(dct_beta_f2['beta_s_mmb_ind'].loc[self.dtm_first_trading_day, self.lst_int_this_port].fillna(0))})
                #     df.to_csv('2016-03-04.csv', index=False)
                #     quit()
                for index in range(len(ret_list)):
                    self.ret_list[index] = (1 + self.ret_list[index]) * (1 + ret_list[index]) - 1
                dbl_raw_ret = cal_weighted_ret(self.ret_list, self.weight)
                self.dbl_mkt_ret = (1 + self.dbl_mkt_ret) * (1 + mtx_idx_ret.loc[dtm_trading_day, 'ret_hs300_dty']) - 1
                self.dbl_mmb_ret = (1 + self.dbl_mmb_ret) * (1 + mtx_mmb_factor_ret.loc[dtm_trading_day, 'size_MMB_industryHSI300w_v']) - 1

                new_ret = (1 + dbl_raw_ret - self.mkt_beta * self.dbl_mkt_ret - self.mmb_beta * self.dbl_mmb_ret) / self.cumulative_ret - 1
                self.cumulative_ret = 1 + dbl_raw_ret - self.mkt_beta * self.dbl_mkt_ret - self.mmb_beta * self.dbl_mmb_ret
                return new_ret
            else:
                self.int_trading_times += 1
                return 'nan'

    def cal_port_ret_raw(self, dtm_trading_day, mtx_stk_ret):
        if not self.lst_int_this_port:
            self.int_trading_times += 1
            return 'nan'
        else:
            if self.int_trading_times >= 1:
                self.int_trading_times += 1
                ret_list = list(mtx_stk_ret.loc[dtm_trading_day, self.lst_int_this_port].fillna(0))
                for index in range(len(ret_list)):
                    self.ret_list[index] = (1 + self.ret_list[index]) * (1 + ret_list[index]) - 1
                dbl_raw_ret = cal_weighted_ret(self.ret_list, self.weight)

                new_ret = (1 + dbl_raw_ret) / self.cumulative_ret - 1
                self.cumulative_ret = 1 + dbl_raw_ret
                return new_ret
            else:
                self.int_trading_times += 1
                return 'nan'

    def update_beta_weight_1f(self, dct_beta_f1):
        # 计算组合的beta
        lst_this_port_weight = self.weight

        lst_this_port_mkt_beta = list(dct_beta_f1['beta_s'].loc[self.dtm_first_trading_day, self.lst_int_this_port].fillna(1))

        self.mkt_beta = cal_weighted_ret(lst_this_port_mkt_beta, lst_this_port_weight)

    def update_beta_weight_2f(self, dct_beta_f2):
        # 计算组合的beta

        lst_this_port_weight = self.weight

        lst_this_port_mkt_beta = list(dct_beta_f2['beta_s'].loc[self.dtm_first_trading_day, self.lst_int_this_port].fillna(1))
        lst_this_port_mmb_beta = list(dct_beta_f2['beta_s_mmb_ind'].loc[self.dtm_first_trading_day, self.lst_int_this_port].fillna(0))

        self.mkt_beta = cal_weighted_ret(lst_this_port_mkt_beta, lst_this_port_weight)
        self.mmb_beta = cal_weighted_ret(lst_this_port_mmb_beta, lst_this_port_weight)
