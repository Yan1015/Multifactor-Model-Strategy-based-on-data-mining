# -*- coding: gbk -*-
"""
Created on 2015/12/29 8:44

@author: yanzijian
"""

import datetime

from Account import Account
import Util
import os
import pandas as pd
import numpy as np
import time
import datetime


def find_type(a):
    x1 = a.count(u'/')
    x2 = a.count(u'%')
    x3 = a.count(u'lag')
    x4 = a.count(u'Δ')
    if x3 != 0:
        return 4
    if (x1 == 1) and (x2 == 0) and (x3 == 0) and (x4 == 0):
        return 0
    if (x1 == 1) and (x2 == 0) and (x3 == 0) and (x4 == 1):
        return 1
    if (x1 == 1) and (x2 == 1) and (x3 == 0) and (x4 == 1):
        return 2
    if (x1 == 0) and (x2 == 2) and (x3 == 0) and (x4 == 2):
        return 3


def find_y(a, type):
    if type == 0:
        return a.split('/')[1]
    if type == 1:
        return a.split('/')[1].split(')')[0]
    if type == 2:
        return a.split('/')[1].split(')')[0]
    if type == 3:
        return a.split(u'Δ')[-1]
    if type == 4:
        return a.split('lag')[1].split(')')[0].replace('(', '')


if __name__ == '__main__':
    path = u'E:\CSMAR中国上市公司财务报表数据库 20160714_下载'

    financial_columns = [1, 3, 4, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36,37]

    trade_day_list = list(pd.read_csv(r'{}/{}'.format(path, 'trade_day - 副本.csv'), names=None).iloc[:, 0])
    print(trade_day_list)

    start_date = '2009-01-05'
    end_date = '2016-07-01'
    s_index = trade_day_list.index(start_date)
    e_index = trade_day_list.index(end_date)
    friday_list = []
    for trade_date in trade_day_list[s_index:e_index:]:
        y, m, d = trade_date.split('-')[0:3]
        y = int(y)
        m = int(m)
        d = int(d)
        weekday = datetime.date(y, m, d).weekday()
        if weekday == 4:
            friday_list.append(trade_date)
    print(friday_list)

    name1 = [u'7-66.%Δ管理费用-%Δmarket_capitalization', u'65-66.%Δ实收资本(或股本)-%Δmarket_capitalization', u'65-63.Δ(实收资本(或股本)/market_capitalization)',
             u'29-64.%Δ(销售商品、提供劳务收到的现金/market_capitalization)',
             u'54-66.%Δ非流动资产合计-%Δmarket_capitalization', u'35-66.%Δ支付给职工以及为职工支付的现金-%Δmarket_capitalization', u'67-66.%Δ盈余公积-%Δmarket_capitalization',
             u'67-64.%Δ(盈余公积/market_capitalization)',
             u'65-64.%Δ(实收资本(或股本)/market_capitalization)', u'62-66.%Δ流动负债合计-%Δmarket_capitalization', u'3-66.%Δ营业总成本-%Δmarket_capitalization',
             u'4-66.%Δ营业成本-%Δmarket_capitalization',
             u'5-66.%Δ营业税金及附加-%Δmarket_capitalization', u'50-66.%Δ在建工程净额-%Δmarket_capitalization', u'7-64.%Δ(管理费用/market_capitalization)']
    name2 = [u'8-37.财务费用/total_common_equity', u'8-2.财务费用/total_assets', u'7-30.Δ管理费用/lag(total_current_liabilities)',
             u'8-57.财务费用/number_of_emplogees', u'7-25.Δ管理费用/lag(total liabilities)',
             u'49-57.固定资产净额/number_of_emplogees',
             u'54-52.非流动资产合计/selling_general_adminstrative_cost', u'71-17.所有者权益合计/property_plant_equipment',
             u'34-17.支付的各项税费/property_plant_equipment', u'35-22.支付给职工以及为职工支付的现金/total liabilities',
             u'8-52.财务费用/selling_general_adminstrative_cost', u'59-50.Δ应付职工薪酬/lag(cost_of_goods_sold)',
             u'40-22.支付其他与经营活动有关的现金/total liabilities', u'11-17.营业利润/property_plant_equipment',
             u'8-7.财务费用/total_current_assets', u'7-22.管理费用/total liabilities',
             u'49-52.固定资产净额/selling_general_adminstrative_cost', u'11-32.营业利润/long_term_debt',
             u'69-17.归属于母公司所有者权益合计/property_plant_equipment',
             u'68-17.未分配利润/property_plant_equipment']
    name3 = [u'7-25.Δ管理费用/lag(total liabilities)', u'11-17.营业利润/property_plant_equipment',
             u'36-17.期末现金及现金等价物余额/property_plant_equipment', u'17-17.净利润/property_plant_equipment',
             u'59-30.Δ应付职工薪酬/lag(total_current_liabilities)', u'11-22.营业利润/total liabilities',
             u'18-17.归属于母公司所有者的净利润/property_plant_equipment', u'15-32.利润总额/long_term_debt', u'11-2.营业利润/total_assets',
             u'60-32.应交税费/long_term_debt', u'40-27.支付其他与经营活动有关的现金/total_current_liabilities',
             u'40-20.Δ支付其他与经营活动有关的现金/lag(property_plant_equipment)', u'1-22.营业总收入/total liabilities',
             u'55-17.资产总计/property_plant_equipment', u'72-17.负债与所有者权益总计/property_plant_equipment',
             u'2-22.营业收入/total liabilities', u'40-25.Δ支付其他与经营活动有关的现金/lag(total liabilities)',
             u'59-40.Δ应付职工薪酬/lag(total_common_equity)', u'7-35.Δ管理费用/lag(long_term_debt)',
             u'40-30.Δ支付其他与经营活动有关的现金/lag(total_current_liabilities)']

    name4 = [u'8-37.财务费用/total_common_equity', u'8-57.财务费用/number_of_emplogees',
             u'8-52.财务费用/selling_general_adminstrative_cost', u'7-22.管理费用/total liabilities',
             u'63-52.非流动负债合计/selling_general_adminstrative_cost',
             u'25-57.取得借款收到的现金/number_of_emplogees', u'16-31.%Δ所得税费用-%Δtotal_current_liabilities',
             u'50-59.%Δ(在建工程净额/number_of_emplogees)', u'61-37.其他应付款/total_common_equity']

    columns = {}
    columns[1] = ['B001100000', 'B001101000', 'B001200000', 'B001201000', 'B001207000', 'B001209000', 'B001210000',
                  'B001211000', 'B001212000',
                  'B001302000', 'B001300000', 'B001400000', 'B001500000', 'B001500101', 'B001000000', 'B002100000',
                  'B002000000', 'B002000101',
                  'B002000201', 'B003000000', 'B004000000', 'B006000000', 'B006000101']
    c = {}

    c[1] = ['Stkcd', 'Accper', 'Typrep', 'B001100000', 'B001101000', 'B001200000', 'B001201000', 'B001207000',
            'B001209000', 'B001210000', 'B001211000', 'B001212000',
            'B001302000', 'B001300000', 'B001400000', 'B001500000', 'B001500101', 'B001000000', 'B002100000',
            'B002000000', 'B002000101',
            'B002000201', 'B003000000', 'B004000000', 'B006000000', 'B006000101', 'type', 'finance_detail']

    columns[2] = ['C002003000', 'C003002000', 'C003005000', 'C001014000', 'C003006000', 'C001001000', 'C003000000',
                  'C002006000', 'C002000000', 'C005001000', 'C001021000',
                  'C001020000', 'C006000000', 'C001013000', 'C001000000', 'C005000000', 'C001022000']

    c[2] = ['Stkcd', 'Accper', 'Typrep', 'C002003000', 'C003002000', 'C003005000', 'C001014000', 'C003006000',
            'C001001000', 'C003000000',
            'C002006000', 'C002000000', 'C005001000', 'C001021000',
            'C001020000', 'C006000000', 'C001013000', 'C001000000', 'C005000000', 'C001022000', 'type',
            'finance_detail']

    columns[3] = ['A001101000', 'A001110000', 'A001111000', 'A001112000', 'A001121000', 'A001123000', 'A001100000',
                  'A001205000', 'A001212000', 'A001213000', 'A001218000', 'A001221000', 'A001222000', 'A001200000',
                  'A001000000', 'A002101000', 'A002108000', 'A002109000', 'A002112000', 'A002113000', 'A002120000',
                  'A002100000', 'A002200000', 'A002000000', 'A003101000', 'A003102000', 'A003103000', 'A003105000',
                  'A003100000', 'A003200000', 'A003000000', 'A004000000']

    c[3] = ['Stkcd', 'Accper', 'Typrep', 'A001101000', 'A001110000', 'A001111000', 'A001112000', 'A001121000',
            'A001123000', 'A001100000',
            'A001205000', 'A001212000', 'A001213000', 'A001218000', 'A001221000', 'A001222000', 'A001200000',
            'A001000000', 'A002101000', 'A002108000', 'A002109000', 'A002112000', 'A002113000', 'A002120000',
            'A002100000', 'A002200000', 'A002000000', 'A003101000', 'A003102000', 'A003103000', 'A003105000',
            'A003100000', 'A003200000', 'A003000000', 'A004000000', 'type', 'finance_detail']

    columns_x = columns[1] + columns[2] + columns[3]

    num_list = columns_x
    name_list = ['营业总收入', '营业收入', '营业总成本', '营业成本', '营业税金及附加', '销售费用', '管理费用', '财务费用', '资产减值损失', '投资收益',
                 '营业利润', '营业外收入', '营业外支出', '其中：非流动资产处置净损益', '利润总额', '所得税费用', '净利润', '归属于母公司所有者的净利润',
                 '少数股东损益', '基本每股收益', '稀释每股收益', '综合收益总额', '归属于母公司所有者的综合收益', '处置固定资产、无形资产和其他长期资产收回的现金净额', '取得借款收到的现金',
                 '偿还债务支付的现金', '购买商品、接受劳务支付的现金',
                 '分配股利、利润或偿付利息支付的现金', '销售商品、提供劳务收到的现金', '筹资活动产生的现金流量净额', '购建固定资产、无形资产和其他长期资产支付的现金', '投资活动产生的现金流量净额',
                 '期初现金及现金等价物余额', '支付的各项税费',
                 '支付给职工以及为职工支付的现金', '期末现金及现金等价物余额', '收到的其他与经营活动有关的现金', '经营活动产生的现金流量净额', '现金及现金等价物净增加额',
                 '支付其他与经营活动有关的现金', '货币资金', '应收票据净额', '应收账款净额',
                 '预付款项净额', '其他应收款净额', '存货净额', '流动资产合计', '长期股权投资净额', '固定资产净额', '在建工程净额', '无形资产净额', '长期待摊费用', '递延所得税资产',
                 '非流动资产合计', '资产总计', '短期借款', '应付账款', '预收款项',
                 '应付职工薪酬', '应交税费', '其他应付款', '流动负债合计', '非流动负债合计', '负债合计', '实收资本(或股本)', '资本公积', '盈余公积', '未分配利润',
                 '归属于母公司所有者权益合计', '少数股东权益', '所有者权益合计', '负债与所有者权益总计']

    signals_columns = [u'Δ(C001000000/eqy_sh_out)', u'Δ(A003000000/eqy_sh_out)',
                       'B001100000/[(lag_A001000000+A001000000)]/2]',
                       'B001100000/[(lag_property_plant_equipment+property_plant_equipment)]/2]',
                       'B001100000/[(lag_A001100000+A001100000)]/2]', 'B001101000/[(lag_A001111000+A001111000)]/2]',
                       'B001201000/[(lag_A001123000+A001123000)]/2]',
                       'B001209000', 'B001210000', 'B001212000', u'非经常性利润', 'A001123000', 'C002006000', u'现金收益率']

    variable_dict = dict(zip(num_list, name_list))
    reverse_dict = dict(zip(name_list, num_list))

    find_origin_dict = {}

    financial_columns = [1, 3, 4, 9, 10, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 25, 26, 27, 28, 29, 31, 32, 33, 34, 36,37]




    trade_date_list = trade_day_list[trade_day_list.index('2009-01-05'):trade_day_list.index('2016-07-01') + 2:]


    trading_date_list = []

    for variable_num in ['equal_weight']:
        print(variable_num)


        for k in range(1):
            holding = [[], [], [], [], [], [], [], [], [], []]
            holding_w = [[], [], [], [], [], [], [], [], [], []]

            dct_dct_my_port = {}
            dct_dct_my_port_weight = {}
            for trade_date in trade_date_list:

                to_path = u'{}/{}/{}.csv'.format('F://', u'copula\\output\\ret_liquidity_4_utd_monthly_port', trade_date_list[trade_date_list.index(trade_date) - 1])
                print(trade_date)
                if not os.path.exists(to_path):
                    continue
                print(trade_date)

                df = pd.read_csv(u'{}/{}/{}.csv'.format('F://', u'copula\\output\\ret_liquidity_4_utd_monthly_port', trade_date_list[trade_date_list.index(trade_date) - 1]), encoding='gbk')
                port = []
                coid_list = []
                for i in range(10):
                    df1 = df[df['port_type'] == i]
                    stkcd_list = list(df1['Stkcd'])
                    coid_list = []
                    for item in stkcd_list:
                        coid_list.append(abs(item))
                    port.append(coid_list)
                year = int(trade_date.split('-')[0])
                month = int(trade_date.split('-')[1])
                day = int(trade_date.split('-')[2])
                dt_obj = datetime.datetime(year, month, day, 0, 0, 0)

                trading_date_list.append(dt_obj)
                # date_str = dt_obj.strftime("%Y-%m-%d %H:%M:%S")
                dct_dct_my_port[dt_obj] = port

                # str_port_path = 'FactorData\\portfolio_record_vol_factor_pkl.pkl'  # pandas or csv, factor_file is a N*2 array: time*[group, code]
                # # str_port_path = 'E:\\MyPy\\OrderFlowProject\OrderFlowOutput\\factor\\buy_minus_sell_2vwxy_count201512291733.csv'  # pandas or csv, factor_file is a N*2 array: time*[group, code]
                # # str_port_path = 'E:\\MyPy\\OrderFlowProject\OrderFlowOutput\\factor\\buy_minus_sell_2vwxy_value201512291748.csv'  # pandas or csv, factor_file is a N*2 array: time*[group, code]
                # # str_port_path = 'E:\\MyPy\\OrderFlowProject\OrderFlowOutput\\factor\\buy_2vwxy_count20151230093434.csv'
                # # str_port_path = 'E:\\MyPy\\OrderFlowProject\OrderFlowOutput\\factor\\sell_2vwxy_count20151230093448.csv'
                # # str_port_path = 'E:\\MyPy\\OrderFlowProject\OrderFlowOutput\\factor\\new_limit_buy_count_5_minus_new_limit_sell_count_5_sum20151230100326.csv'
                #
                # str_description = 'vol'
                # # str_description = 'buy_minus_sell_2vwxy_count'
                # # str_description = 'buy_minus_sell_2vwxy_value'
                # # str_description = 'sell_2vwxy_count'
                # # str_description = 'buy_2vwxy_count'
                # # str_description = 'new_limit_buy_count_5_minus_new_limit_sell_count_5_sum'
                #
                # str_output_path = 'Output\\'
                # # str_output_path = 'E:\\MyPy\\OrderFlowProject\\OrderFlowOutput\\FactorOutput\\'
                #
                # int_group_num = 10
                #
                # dct_dct_my_port = Util.get_port_every_day(str_port_path, int_group_num)  # a dict of dict of list int, date of group number of codes list


            str_output_path = 'Output\\Output\\ret_liquidity_4_utd_monthly_delete_zdt_5_ew\\'
            int_group_num = 10
            str_description = 'value_weight_2fresult'



            outputpath = str_output_path + str_description
            # if os.path.exists(outputpath):
            #     continue

            dtm_begin_date = datetime.datetime(2011, 4, 21)
            dtm_end_date = datetime.datetime(2015, 11, 29)
            # dtm_begin_date = datetime.datetime(2008, 1, 1)
            # dtm_end_date = datetime.datetime(2014, 12, 31)
            # dtm_end_date = datetime.datetime(2008, 3, 31)

            int_holding_day = 5

            int_or_str_change_day = 'Friday'  # 或者任何int，代表在哪一天调仓
            # int_or_str_change_day = 1

            my_account = Account(dct_dct_my_port, str_output_path, int_holding_day, int_or_str_change_day, dtm_begin_date, dtm_end_date, int_group_num, str_description, trading_date_list, dct_dct_my_port_weight)

            my_account.start_trading()

            my_account.report()
