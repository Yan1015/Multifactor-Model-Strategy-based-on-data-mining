# -*- coding: gbk -*-

import pandas as pd
import numpy as np
import time
path = u'//SHIMING/accounts/python/YZJ/CSMAR中国上市公司财务报表数据库 20160714_下载'


def find_px_last(id, year):
    global finance_df
    date = str(year + 1) + '-06-30'
    dff = finance_df[finance_df['coid'] == id]
    d = date.replace('-', '')
    d = int(d)
    dff['difference'] = dff['date'].apply(lambda x: d - int(x.replace('-', '')))
    df1 = dff[dff['difference'] >= 0]

    df1 = df1.sort_values(by='difference')
    a = df1.iloc[0, 2]
    return a

def find_eqy_sh_out(id, year):
    global finance_df
    date = str(year + 1) + '-06-30'
    dff = finance_df[finance_df['coid'] == id]
    d = date.replace('-', '')
    d = int(d)
    dff['difference'] = dff['date'].apply(lambda x: d - int(x.replace('-', '')))

    df1 = dff[dff['difference'] >= 0]

    df1 = df1.sort_values(by='difference')
    a = df1.iloc[0, 3]
    return a


table = {}
table[1] = u'利润表'
table[2] = u'现金流量表'
table[3] = u'资产负债表'
dataframe = {}
dataframe[1] = pd.read_csv(ur'{}/{}/{}'.format(path, table[1], 'f_result.csv')).fillna(0)
dataframe[2] = pd.read_csv(ur'{}/{}/{}'.format(path, table[2], 'f_result.csv')).fillna(0)
dataframe[3] = pd.read_csv(ur'{}/{}/{}'.format(path, table[3], 'f_result.csv')).fillna(0)

columns = {}
columns[1] = ['B001100000', 'B001101000', 'B001200000','B001201000','B001207000','B001209000','B001210000','B001211000','B001212000',
            'B001302000', 'B001300000','B001400000','B001500000','B001500101', 'B001000000', 'B002100000', 'B002000000', 'B002000101',
            'B002000201', 'B003000000', 'B004000000', 'B006000000', 'B006000101']
c = {}

c[1] = ['Stkcd', 'Accper', 'Typrep', 'B001100000', 'B001101000', 'B001200000','B001201000','B001207000','B001209000','B001210000','B001211000','B001212000',
            'B001302000', 'B001300000','B001400000','B001500000','B001500101', 'B001000000', 'B002100000', 'B002000000', 'B002000101',
            'B002000201', 'B003000000', 'B004000000', 'B006000000', 'B006000101', 'type','finance_detail']

columns[2] = ['C002003000', 'C003002000', 'C003005000', 'C001014000', 'C003006000', 'C001001000', 'C003000000',
           'C002006000', 'C002000000', 'C005001000', 'C001021000',
           'C001020000', 'C006000000', 'C001013000', 'C001000000', 'C005000000', 'C001022000']

c[2] = ['Stkcd', 'Accper', 'Typrep', 'C002003000', 'C003002000', 'C003005000', 'C001014000', 'C003006000', 'C001001000', 'C003000000',
     'C002006000', 'C002000000', 'C005001000', 'C001021000',
     'C001020000', 'C006000000', 'C001013000', 'C001000000', 'C005000000', 'C001022000', 'type','finance_detail']

columns[3] = ['A001101000', 'A001110000', 'A001111000', 'A001112000', 'A001121000', 'A001123000', 'A001100000',
            'A001205000', 'A001212000', 'A001213000', 'A001218000', 'A001221000', 'A001222000', 'A001200000',
            'A001000000', 'A002101000', 'A002108000', 'A002109000', 'A002112000', 'A002113000', 'A002120000',
            'A002100000', 'A002200000', 'A002000000', 'A003101000', 'A003102000', 'A003103000', 'A003105000',
            'A003100000', 'A003200000', 'A003000000', 'A004000000']

c[3] = ['Stkcd', 'Accper', 'Typrep', 'A001101000', 'A001110000', 'A001111000', 'A001112000', 'A001121000', 'A001123000', 'A001100000',
            'A001205000', 'A001212000', 'A001213000', 'A001218000', 'A001221000', 'A001222000', 'A001200000',
            'A001000000', 'A002101000', 'A002108000', 'A002109000', 'A002112000', 'A002113000', 'A002120000',
            'A002100000', 'A002200000', 'A002000000', 'A003101000', 'A003102000', 'A003103000', 'A003105000',
            'A003100000', 'A003200000', 'A003000000', 'A004000000', 'type','finance_detail']

columns_y = ['Stkcd', 'Accper', 'property_plant_equipment', 'market_capitalization']

columns_x = ['C001000000', 'A003000000', 'A001100000', 'A001111000', 'A001123000', 'A001000000', 'B001100000',
             'B001101000', 'B001201000', 'B001400000', 'B001500000', 'B001209000', 'B001210000', 'B001212000',
             'A001123000', 'C002006000', 'B002000000']

finance_df = pd.read_csv(u'{}/{}'.format(path, 'daily.csv')).fillna(0)
finance_df['coid'] = finance_df['id'].apply(lambda x: abs(x))
finance_df = finance_df.loc[:, ['date', 'coid', 'px_last', 'eqy_sh_out']]


m = pd.read_csv(ur'{}/{}'.format(path, 'winsorize_result.csv')).fillna(0)

m = m.loc[:, columns_x]

Y_df = pd.read_csv(ur'{}/{}.csv'.format(path, 'based_variable-Y'))
Y_df = Y_df.loc[:, columns_y]


Y_df['type'] = Y_df['Accper'].apply(lambda x: int(x.split('-')[0]))
Y_df['px_last'] = Y_df.apply(lambda x: find_px_last(int(x['Stkcd']), x['type']), axis=1)
Y_df['eqy_sh_out'] = Y_df.apply(lambda x: find_eqy_sh_out(int(x['Stkcd']), x['type']), axis=1)

Y_df['market_capitalization'] = Y_df.apply(lambda x: x['px_last'] * x['eqy_sh_out'] * 100000, axis=1)

flag = 0
for X in ['C001000000', 'A003000000']:
    df = m.loc[:, ['Stkcd', 'Accper', X]].sort_values(by=['Stkcd', 'Accper'])
    Y = 'eqy_sh_out'
    df[Y] = Y_df[Y]
    signal_name1 = X + '/' + Y
    df[signal_name1] = df.apply(lambda x: float(x[X]) / x[Y] if x[Y] != 0 else 0, axis=1)
    l=[0]
    l.extend(list(df[signal_name1]))
    del l[-1]
    signal_name2 = u'Δ(' + X + '/' + Y + ')'
    df[signal_name2] = l
    df[signal_name2] = df.apply(lambda x: x[signal_name1] - x[signal_name2] + 0.000000000000001 if ((x[signal_name1] != 0) and (x[signal_name2] != 0)) else 0, axis=1)
    if flag == 0:
        nonredundant_df = df
        flag = 1
    else:
        nonredundant_df = pd.merge(nonredundant_df, df)

X_type3 = ['A001000000', 'property, plant and equipment', 'A001100000', 'A001111000', 'A001123000']
Y_type3 = ['B001100000', 'B001100000', 'B001100000', 'B001101000', 'B001201000']
type3_dict = dict(zip(X_type3, Y_type3))
for X in X_type3:
    Y = type3_dict[X]
    l = [0]
    l.extend(list(df[X]))
    del l[-1]
    df['lag_' + X] = l
    signal_name = Y + '/' + '[(' + 'lag_' + X + '+' + X + ')]/2]'
    df['lag_' + X + '+' + X] = df.apply(lambda x: x['lag_' + X] + x[X] + 0.000000000000001 if ((x['lag_' + X] != 0) and (x[X] != 0)) else 0, axis=1)
    df[signal_name] = df.apply(lambda x: 2 * float(x[Y]) / x['lag_' + X + '+' + X] if x['lag_' + X + '+' + X] != 0 else 0, axis=1)










for X in columns_x:
    print X
    name = {}

    df = m.loc[:, ['Stkcd', 'Accper', X]].sort_values(by=['Stkcd', 'Accper'])

    name[6] = u'Δ' + X
    name[8] = u'%Δ' + X

    l = [0]
    l.extend(list(df[X]))
    del l[-1]
    df[name[6]] = l

    df[name[6]] = df.apply(lambda x: x[X] - x[name[6]] + 0.000000000000001 if ((x[X] != 0) and (x[name[6]] != 0)) else 0, axis=1)

    coid_l = list(m['Stkcd'])
    coid_l = list(set(coid_l))
    for i in coid_l:
        index_l = df[df['Stkcd'] == i].index
        df.loc[index_l[0], name[6]] = 0


    l = [0]
    l.extend(list(df[X]))
    del l[-1]
    df['1'] = l

    df[name[8]] = df.apply(lambda x: float(x[name[6]]) / abs(x['1']) if x['1'] != 0 else 0, axis=1)
    for index in range(2, 15):
        Y = columns_y[index]
        df[Y] = Y_df[Y]

        name[1] = X + '/' + Y
        name[2] = u'Δ(' + X + '/' + Y + ')'
        name[3] = u'%Δ(' + X + '/' + Y + ')'
        name[4] = u'%Δ' + X + '-' + u'%Δ' + Y
        name[5] = u'Δ' + X + '/' + 'lag(' + Y + ')'
        name[7] = u'Δ' + Y
        name[9] = u'%Δ' + Y
        df[name[1]] = df.apply(lambda x: float(x[X]) / x[Y] if x[Y] != 0 else 0, axis=1)
        l=[0]
        l.extend(list(df[name[1]]))
        del l[-1]
        df[name[2]] = l
        df[name[2]] = df.apply(lambda x: x[name[1]] - x[name[2]] + 0.000000000000001 if ((x[name[1]] != 0) and (x[name[2]] != 0)) else 0, axis=1)

        for i in coid_l:
            index_l = df[df['Stkcd'] == i].index
            df.loc[index_l[0], name[2]] = 0

        l = [0]
        l.extend(list(df[name[1]]))
        del l[-1]
        df['1'] = l
        df[name[3]] = df.apply(lambda x: float(x[name[2]]) / abs(x['1']) if x['1'] != 0 else 0, axis=1)

        l = [0]
        l.extend(list(df[Y]))
        del l[-1]
        df['1'] = l
        df[name[5]] = df.apply(lambda x: float(x[name[6]]) / x['1'] if x['1'] != 0 else 0, axis=1)

        l = [0]
        l.extend(list(df[Y]))
        del l[-1]
        df[name[7]] = l
        df[name[7]] = df.apply(lambda x: x[Y] - x[name[7]] + 0.000000000000001 if ((x[Y] != 0) and (x[name[7]] != 0)) else 0, axis=1)

        for i in coid_l:
            index_l = df[df['Stkcd'] == i].index
            df.loc[index_l[0], name[7]] = 0

        l = [0]
        l.extend(list(df[Y]))
        del l[-1]
        df['1'] = l
        df[name[9]] = df.apply(lambda x: float(x[name[7]]) / abs(x['1']) if x['1'] != 0 else 0, axis=1)

        df[name[4]] = df.apply(lambda x: x[name[8]] - x[name[9]] if ((x[name[8]] != 0) and (x[name[9]] != 0)) else 0, axis=1)

        if (Y != 'market_capitalization'):
            df = df.drop([name[7], name[9], Y], axis=1)
        else:
            df = df.drop([name[7], name[9]], axis=1)


    df = df.drop(['1', name[6]], axis=1)




    df.to_csv(ur'{}/{}/{}.csv'.format(path, 'signals', X + '_signals'), encoding='gbk', index =False)
    end = time.clock()
