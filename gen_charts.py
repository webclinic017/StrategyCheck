from plotly.subplots import make_subplots
import plotly.graph_objs as go
import pandas as pd
import conf
import strategy
import os


class Chart:
    def __init__(self, name):
        self.name = name
        try:
            self.df = pd.read_csv(f'candle_data/{name}_{conf.days}days_{conf.candle_interval}_ta.csv')
        except FileNotFoundError:
            return
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

        # set date as index for graphs
        self.date_long = [self.df['date'][i] for i in self.long_index]
        self.date_short = [self.df['date'][i] for i in self.short_index]


        ##############################
        #### add indicators below ####
        ##############################

        # Row 1
        self.add_indicator_to_graph('ema_25', 'scatter', 'purple')
        self.add_indicator_to_graph('wma_50', 'scatter', 'orange')
        self.add_indicator_to_graph('wma_100', 'scatter', 'cyan')
        self.add_indicator_to_graph('wma_200', 'scatter', 'red')
        self.add_signal_to_graph('close')

        # Row 2
        self.add_indicator_to_graph('macd', 'scatter', 'grey')
        self.add_indicator_to_graph('macds', 'scatter', 'yellow')
        self.add_indicator_to_graph('macdh', 'bar', 'red')
        self.add_signal_to_graph('macd')

        # Row 3
        self.add_indicator_to_graph('mfi', 'scatter', 'black')
        self.add_signal_to_graph('mfi')

        # Row 4
        self.add_indicator_to_graph('adx', 'scatter', 'black')
        self.add_indicator_to_graph('di_neg', 'scatter', 'red')
        self.add_indicator_to_graph('di_pos', 'scatter', 'green')
        self.add_signal_to_graph('adx')

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

    def add_indicator_to_graph(self, name, plot_type, color):
        if plot_type == 'scatter':
            self.figure.append_trace(
                go.Scatter(
                    x=self.df['date'],
                    y=self.df[name],
                    name=name,
                    line=dict(color=color)
                ),
                row=conf.add_indicators[name],
                col=1
            )
        elif plot_type == 'bar':
            self.figure.append_trace(
                go.Bar(
                    x=self.df['date'],
                    y=self.df[name],
                    name=name,
                    marker=dict(color=color)
                ),
                row=2,
                col=1
            )

    def add_signal_to_graph(self, name):
        indicator_long_filter = [self.df[name].tolist()[i] for i in self.long_index]
        indicator_short_filter = [self.df[name].tolist()[i] for i in self.short_index]

        # Long Signals
        self.figure.append_trace(
            go.Scatter(
                x=self.date_long,
                y=indicator_long_filter,
                name="Buy Signals",
                marker=dict(color="lime", size=12, opacity=0.5),
                mode="markers"
            ),
            row=conf.add_indicators[name] if name not in ['high', 'low', 'close', 'open'] else 1,
            col=1
        )

        # Short Signals
        self.figure.append_trace(
            go.Scatter(
                x=self.date_short,
                y=indicator_short_filter,
                name="Sell Signals",
                marker=dict(color="rgb(255, 36, 0)", size=12, opacity=0.5),
                mode="markers"
            ),
            row=conf.add_indicators[name] if name not in ['high', 'low', 'close', 'open'] else 1,
            col=1
        )
