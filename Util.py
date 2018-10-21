# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import datetime


def get_port_every_day_from_pkl(str_port_path):
    f = open(str_port_path, 'rb')
    dct_dct_my_port = pickle.load(f)


    f.close()
    assert isinstance(dct_dct_my_port, dict)
    return dct_dct_my_port


def cal_weighted_ret(lst_value, lst_weight):
    # if value == null, replace it by average
    assert len(lst_value) == len(lst_weight)

    sum_tmp = 0.0
    weight_tmp = 0.0

    for int_idx in range(len(lst_value)):
        if pd.notnull(lst_value[int_idx]) and pd.notnull(lst_weight[int_idx]):
            sum_tmp += lst_value[int_idx] * lst_weight[int_idx]
            weight_tmp += lst_weight[int_idx]

    return sum_tmp/weight_tmp if weight_tmp != 0 else 0.0


def get_port_every_day_from_csv(str_path, int_group_num, pd_stk_capital):
    dct_portfolio_record = {}
    pd_factor_data = pd.read_csv(str_path, index_col=[0], parse_dates=True, date_parser=str2date)
    assert isinstance(pd_factor_data, pd.DataFrame)

    for date, factor_this_day in pd_factor_data.iterrows():
        print(date)
        if date in pd_stk_capital.index:
            list_stk_cap_this_day = pd_stk_capital.loc[date, :].dropna()
        else:
            continue
        # choose those in the largest 70%
        # idx_larger = sorted(list_stk_cap_this_day.dropna().index, key=lambda x: list_stk_cap_this_day[x])[int(len(list_stk_cap_this_day.dropna())*0.3):]
        idx_larger = sorted(list_stk_cap_this_day.index, key=lambda x: list_stk_cap_this_day[x])[int(len(list_stk_cap_this_day)*0.3):]
        lst_str_sorted_stk = filter(lambda x: x in idx_larger, sorted(factor_this_day.dropna().index, key=lambda x: factor_this_day[x]))
        lst_int_sorted_stk = [int(str_stk) for str_stk in lst_str_sorted_stk]
        int_stk_num_in_each_group = int(len(lst_int_sorted_stk)/int_group_num)
        group_num_tmp = len(lst_int_sorted_stk) - int_stk_num_in_each_group * int_group_num
        group_num_lst = [int_stk_num_in_each_group+1] * group_num_tmp + [int_stk_num_in_each_group] * (int_group_num-group_num_tmp)

        stk_idx_start = 0
        stk_in_each_group = []
        for group_num_tmp2 in group_num_lst:
            stk_in_each_group.append(lst_int_sorted_stk[stk_idx_start:stk_idx_start+group_num_tmp2])
            stk_idx_start += group_num_tmp2

        dct_portfolio_record[date] = stk_in_each_group

    return dct_portfolio_record


def get_port_every_day(str_path, int_group_num):

    # group by factor
    if str_path.split('.')[-1] == 'csv':
        # get stk capital
        pd_stk_capital = pd.read_csv('\\\\SHIMING\\Desktop\\qiding\\DailyMarketData\\dailyretme.csv', index_col=[0], parse_dates='date', date_parser=str2date)
        return get_port_every_day_from_csv(str_path, int_group_num, pd_stk_capital)
    elif str_path.split('.')[-1] == 'pkl':
        return get_port_every_day_from_pkl(str_path)
    else:
        pass


def str2date(s):
    f = lambda x:datetime.datetime.strptime(str(x).replace('-', ''), '%Y%m%d')

    return f(s)
