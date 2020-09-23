from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import conf
import strategy
import os


class Chart:
    def __init__(self, name):
        self.name = name
        self.df = pd.read_csv(f'candle_data/{name}_{conf.days}days_{conf.candle_interval}_ta.csv')
        self.long_index = strategy.go_long(self.df)
        self.short_index = strategy.go_short(self.df)
        self.figure = make_subplots(
            rows=len(set(conf.add_indicators.values())),
            cols=1,
            row_width=[1 / len(set(conf.add_indicators.values()))] * len(set(conf.add_indicators.values()))
        )

        # candlestick graph of asset
        self.figure.append_trace(
            go.Candlestick(
                x=self.df['date'],
                name='price',
                open=self.df['open'],
                high=self.df['high'],
                low=self.df['low'],
                close=self.df['close']
            ),
            row=1,
            col=1
        )

        date_long = [self.df['date'][i] for i in self.long_index]
        date_short = [self.df['date'][i] for i in self.short_index]

        close_long_filter = [self.df['close'].tolist()[i] for i in self.long_index]
        close_short_filter = [self.df['close'].tolist()[i] for i in self.short_index]

        # Long Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_long,
                y=close_long_filter,
                name="Buy Signals",
                marker=dict(color="lime", size=12, opacity=0.5),
                mode="markers"
            ),
            row=1,
            col=1
        )

        # Short Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_short,
                y=close_short_filter,
                name="Sell Signals",
                marker=dict(color="rgb(255, 36, 0)", size=12, opacity=0.5),
                mode="markers"
            ),
            row=1,
            col=1
        )

        ##############################
        #### add indicators below ####
        ##############################

        # Row 1

        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['ema_25'],
                name='EMA_25'
            ),
            row=1,
            col=1
        )

        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['wma_50'],
                name='WMA_50'
            ),
            row=1,
            col=1
        )

        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['wma_100'],
                name='WMA_100'
            ),
            row=1,
            col=1
        )

        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['wma_200'],
                name='WMA_200'
            ),
            row=1,
            col=1
        )

        # Row 2

        # MACD Scatterplot
        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['macd'],
                name='MACD',
                line=dict(color='grey')
            ),
            row=2,
            col=1
        )

        # MACD Signal Scatterplot
        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['macds'],
                name='MACD Signal',
                line=dict(color='yellow')
            ),
            row=2,
            col=1
        )

        # MACD Histogram
        self.figure.append_trace(
            go.Bar(
                x=self.df['date'],
                y=self.df['macdh'],
                name='MACDH'
            ),
            row=2,
            col=1
        )

        macd_long_filter = [self.df['macd'].tolist()[i] for i in self.long_index]
        macd_short_filter = [self.df['macd'].tolist()[i] for i in self.short_index]

        # Long Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_long,
                y=macd_long_filter,
                name="Buy Signals",
                marker=dict(color="lime", size=12, opacity=0.5),
                mode="markers"
            ),
            row=2,
            col=1
        )

        # Short Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_short,
                y=macd_short_filter,
                name="Sell Signals",
                marker=dict(color="rgb(255, 36, 0)", size=12, opacity=0.5),
                mode="markers"
            ),
            row=2,
            col=1
        )

        # Row 3

        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['mfi'],
                name='MFI'
            ),
            row=3,
            col=1
        )

        mfi_long_filter = [self.df['mfi'].tolist()[i] for i in self.long_index]
        mfi_short_filter = [self.df['mfi'].tolist()[i] for i in self.short_index]

        # Long Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_long,
                y=mfi_long_filter,
                name="Buy Signals",
                marker=dict(color="lime", size=12, opacity=0.5),
                mode="markers"
            ),
            row=3,
            col=1
        )

        # Short Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_short,
                y=mfi_short_filter,
                name="Sell Signals",
                marker=dict(color="rgb(255, 36, 0)", size=12, opacity=0.5),
                mode="markers"
            ),
            row=3,
            col=1
        )

        # Row 4

        # ADX Scatterplot
        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['adx'],
                name='ADX',
                line=dict(color='black')
            ),
            row=4,
            col=1
        )

        # NDI Scatterplot
        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['di_neg'],
                name='-DI',
                line=dict(color='red')
            ),
            row=4,
            col=1
        )

        # PDI Scatterplot
        self.figure.append_trace(
            go.Scatter(
                x=self.df['date'],
                y=self.df['di_pos'],
                name='+DI',
                line=dict(color='green')
            ),
            row=4,
            col=1
        )

        adx_long_filter = [self.df['adx'].tolist()[i] for i in self.long_index]
        adx_short_filter = [self.df['adx'].tolist()[i] for i in self.short_index]

        # Long Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_long,
                y=adx_long_filter,
                name="Buy Signals",
                marker=dict(color="lime", size=12, opacity=0.5),
                mode="markers"
            ),
            row=4,
            col=1
        )

        # Short Signals
        self.figure.append_trace(
            go.Scatter(
                x=date_short,
                y=adx_short_filter,
                name="Sell Signals",
                marker=dict(color="rgb(255, 36, 0)", size=12, opacity=0.5),
                mode="markers"
            ),
            row=4,
            col=1
        )

        ##############################
        #### add indicators above ####
        ##############################

        size = 1500
        self.figure.update_layout(
            title=self.name,
            xaxis_rangeslider_visible=False,
            autosize=False,
            width=size * 1.5,
            height=size
        )

        if not os.path.exists('charts'):
            os.makedirs('charts')
        self.figure.write_html(f'charts/{self.name}.html')
        print(f'generated chart for {name}')


if __name__ == '__main__':
    c = Chart('BTCUSDT')
