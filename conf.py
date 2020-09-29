# set minimum 24h (quote asset) volume per pair, unfiltered if set to 0
min_volume = 30000000

# quote asset (what you pay to buy an asset)
quote_asset = 'USDT'

# candlestick interval (necessary!)
candle_interval = '30MINUTE'

# how many days to look back?
days = 14

# assets to ignore
ignore_assets = ['USDC', 'PAX', 'BUSD', 'TUSD', 'USDS', 'BNB', 'MTL']

# indicators from csv to add to the chart
# later maybe chart generation just from this dict
add_indicators = {
    'ema_25': {
        'row': 1,
        'color': 'purple',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'wma_50': {
        'row': 1,
        'color': 'orange',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'wma_100': {
        'row': 1,
        'color': 'cyan',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'wma_200': {
        'row': 1,
        'color': 'red',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'macd': {
        'row': 2,
        'color': 'grey',
        'plot_type': 'scatter',
        'add_signal': True
    },
    'macds': {
        'row': 2,
        'color': 'yellow',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'macdh': {
        'row': 2,
        'color': 'red',
        'plot_type': 'bar',
        'add_signal': False
    },
    'mfi': {
        'row': 3,
        'color': 'black',
        'plot_type': 'scatter',
        'add_signal': True
    },
    'adx': {
        'row': 4,
        'color': 'black',
        'plot_type': 'scatter',
        'add_signal': True
    },
    'di_neg': {
        'row': 4,
        'color': 'red',
        'plot_type': 'scatter',
        'add_signal': False
    },
    'di_pos': {
        'row': 4,
        'color': 'green',
        'plot_type': 'scatter',
        'add_signal': False
    }
}
