import lib.gen_data as gen_data
import lib.gen_charts as gen_charts
from binance.client import Client
import pandas as pd
import json


with open("lib/settings.json", "r") as settings_json:
    settings = json.load(settings_json)
    filter_settings = settings["FilterSettings"]
    exchange_settings = settings["ExchangeSettings"]


if __name__ == '__main__':
    client = Client()
    ticker_df = pd.DataFrame(client.get_ticker())

    # only pairs with desired quote asset
    filter_ticker_df = ticker_df['symbol'].str[-len(filter_settings["Quote_Asset"]):] == filter_settings["Quote_Asset"]
    ticker_df = ticker_df[filter_ticker_df]

    # only pairs with volume > minimal volume of interest to trade
    filter_ticker_df = ticker_df['quoteVolume'].astype(float) > filter_settings["Min_Volume"]
    ticker_df = ticker_df[filter_ticker_df]

    # only pairs not containing any of the assets to ignore
    for asset in exchange_settings["Ignore_Assets"]:
        filter_ticker_df = ticker_df['symbol'].str.contains(asset)
        ticker_df = ticker_df[~filter_ticker_df]

    # generate csv data and charts for each pair
    for pair in ticker_df['symbol'].tolist():
        gen_data.gen_ta_candles(pair, exchange_settings["Days_to_look_back"])
        gen_charts.Chart(pair)
