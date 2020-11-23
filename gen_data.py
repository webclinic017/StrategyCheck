from binance.client import Client
import pandas as pd
from talib.abstract import *
import os
import json


with open("settings.json", "r") as settings_json:
    settings = json.load(settings_json)
    exchange_settings = settings["ExchangeSettings"]


# convert date to seconds and set every relevant non-float column to float
def only_numlist(candle_elem):
    return [candle_elem[0] // 1000] + [float(val) if type(val) is str else val for val in candle_elem[1:6]]


# generate the classic candles data
def gen_candles(symbol='BTCUSDT', days=14):
    c = Client()
    candles = c.get_historical_klines(
        symbol,
        eval(f'c.KLINE_INTERVAL_{exchange_settings["Candle_Interval"]}'),
        f'{days} days ago UTC'
    )
    candle_data = [only_numlist(candle) for candle in candles]
    df = pd.DataFrame(candle_data)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['date'] = df['date'] / 1000
    return df


def gen_ta_candles(symbol='BTCUSDT', days=14):
    data = gen_candles(symbol, days)

    # abort if not enough data
    if len(data) < 200:
        return

    inputs = {
        'open': data['open'].astype(float),
        'high': data['high'].astype(float),
        'low': data['low'].astype(float),
        'close': data['close'].astype(float),
        'volume': data['volume'].astype(float),
    }
    #################################################################################
    # set indicators below

    data['close_weight'] = WCLPRICE(inputs)
    data['middle'] = (data['high'] + data['low'] + data['close'] + data['open']) / 4
    data['ema_25'] = EMA(inputs, timeperiod=25)
    data['wma_50'] = WMA(inputs, timeperiod=50)
    data['wma_100'] = WMA(inputs, timeperiod=100)
    data['wma_200'] = WMA(inputs, timeperiod=200)
    data['macd'], data['macds'], data['macdh'] = MACD(inputs)
    data['macd'] = EMA(data["macd"], 3)
    data['macds'] = EMA(data["macds"], 3)
    data['macdh'] = data["macd"] - data["macds"]
    data['mfi'] = EMA(MFI(inputs, timeperiod=14), 5)
    data['adx'] = EMA(ADX(inputs, timeperiod=14), 5)
    data['di_neg'] = EMA(MINUS_DI(inputs, timeperiod=14), 5)
    data['di_pos'] = EMA(PLUS_DI(inputs, timeperiod=14), 5)

    # set indicators above
    #################################################################################
    data = data.dropna()
    if not os.path.exists('candle_data'):
        os.makedirs('candle_data')

    data.to_csv(f'candle_data/{symbol}_{days}days_{exchange_settings["Candle_Interval"]}_ta.csv', index=False)
    print(f'generated {symbol} ta-data')
