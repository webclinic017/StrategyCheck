import conf
from binance.client import Client
import pandas as pd
from talib.abstract import *


# convert date to seconds and set every relevant non-float column to float
def only_numlist(candle_elem):
    return [candle_elem[0] // 1000] + [float(val) if type(val) is str else val for val in candle_elem[1:6]]


# generate the classic candles data
def gen_candles(symbol='BTCUSDT', days=14):
    c = Client()
    candles = c.get_historical_klines(
        symbol,
        eval(f'c.KLINE_INTERVAL_{conf.candle_interval}'),
        f'{days} days ago UTC'
    )
    candle_data = [only_numlist(candle) for candle in candles]
    df = pd.DataFrame(candle_data)
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['date'] = df['date'] / 1000
    return df


def gen_ta_candles(symbol='BTCUSDT', days=14):
    data = gen_candles(symbol, days)
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
    data['mfi'] = MFI(inputs, timeperiod=14)

    # set indicators above
    #################################################################################
    data = data.dropna()
    data.to_csv(f'candle_data/{symbol}_{days}days_{conf.candle_interval}_ta.csv', index=False)
    print(f'generated {symbol} ta-data')


if __name__ == '__main__':
    client = Client()
    ticker_df = pd.DataFrame(client.get_ticker())

    # only pairs with desired quote asset
    filter_ticker_df = ticker_df['symbol'].str[-len(conf.quote_asset):] == conf.quote_asset
    ticker_df = ticker_df[filter_ticker_df]

    # only pairs with volume > minimal volume of interest to trade
    filter_ticker_df = ticker_df['quoteVolume'].astype(float) > conf.min_volume
    ticker_df = ticker_df[filter_ticker_df]

    # only pairs not containing any of the assets to ignore
    for asset in conf.ignore_assets:
        filter_ticker_df = ticker_df['symbol'].str.contains(asset)
        ticker_df = ticker_df[~filter_ticker_df]

    # generate csv data for each pair
    for pair in ticker_df['symbol'].tolist():
        gen_ta_candles(pair, conf.days)
