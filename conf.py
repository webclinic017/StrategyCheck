# set minimum 24h (quote asset) volume per pair, unfiltered if set to 0
min_volume = 30000000

# quote asset (what you pay to buy an asset)
quote_asset = 'USDT'

# candlestick interval (necessary!)
candle_interval = '15MINUTE'

# how many days to look back?
days = 14

# assets to ignore
ignore_assets = ['USDC', 'PAX', 'BUSD', 'TUSD', 'USDS', 'BNB', 'MTL']

# indicators from csv to add to the chart
# later maybe chart generation just from this dict
add_indicators = {
    'ema_25': 1,
    'wma_50': 1,
    'wma_100': 1,
    'wma_200': 1,
    'macd': 2,
    'macds': 2,
    'macdh': 2,
    'mfi': 3
}