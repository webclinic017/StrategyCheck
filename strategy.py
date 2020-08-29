import pandas as pd

'''
In the go_long/go_short methods "index i"
is always the index for the respective buy/sell signal
'''


def go_long(df):
    long_index = []
    for i in range(len(df)):
        if df['ema_25'][i] > df['wma_50'][i] > df['wma_200'][i]:
            if df['mfi'][i] < 40:
                long_index.append(i)
    return long_index


def go_short(df):
    short_index = []
    for i in range(len(df)):
        if df['ema_25'][i] < df['wma_50'][i]:
            short_index.append(i)
    return short_index
