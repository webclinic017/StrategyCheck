import gen_data
import gen_charts
from binance.client import Client
import pandas as pd
import conf


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

    # generate csv data and charts for each pair
    for pair in ticker_df['symbol'].tolist():
        gen_data.gen_ta_candles(pair, conf.days)
        gen_charts.Chart(pair)
