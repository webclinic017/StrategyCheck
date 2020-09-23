import pandas as pd

'''
In the go_long/go_short methods "index i"
is always the index for the respective buy/sell signal
'''


def go_long(df):
    long_index = []
    for i in range(1, len(df)):
        if df['macd'][i - 1] < df['macd'][i] < 0:
            if df['mfi'][i - 1] < df['mfi'][i] < 40:
                long_index.append(i)
    return long_index


def go_short(df):
    short_index = []
    for i in range(1, len(df)):
        if 40 < df['mfi'][i] < df['mfi'][i - 1]:
            if df['macd'][i - 1] > df['macd'][i]:
                short_index.append(i)
    return short_index
