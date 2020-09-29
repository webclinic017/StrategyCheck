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

        # set up the whole graph
        indicators_total = max(conf.add_indicators[item]['row'] for item in conf.add_indicators.keys())
        self.figure = make_subplots(
            rows=indicators_total,
            cols=1,
            row_width=[1 / indicators_total] * indicators_total
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

        # add every indicator to graph (see conf.py)
        for indicator in conf.add_indicators.keys():
            self.add_indicator_to_graph(indicator)
            if conf.add_indicators[indicator]['add_signal']:
                self.add_signal_to_graph(indicator)

        # generate html file
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

    '''
    This method adds an indicator (see conf.py) to the graph
    plot_type: scatter/bar
    '''
    def add_indicator_to_graph(self, name):
        if conf.add_indicators[name]['plot_type'] == 'scatter':
            self.figure.append_trace(
                go.Scatter(
                    x=self.df['date'],
                    y=self.df[name],
                    name=name,
                    line=dict(color=conf.add_indicators[name]['color'])
                ),
                row=conf.add_indicators[name]['row'],
                col=1
            )
        elif conf.add_indicators[name]['plot_type'] == 'bar':
            self.figure.append_trace(
                go.Bar(
                    x=self.df['date'],
                    y=self.df[name],
                    name=name,
                    marker=dict(color=conf.add_indicators[name]['color'])
                ),
                row=conf.add_indicators[name]['row'],
                col=1
            )

    '''
    This method sets green and red markers within the graph of the associated indicator
    '''
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
            row=conf.add_indicators[name]['row'] if name not in ['high', 'low', 'close', 'open'] else 1,
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
            row=conf.add_indicators[name]['row'] if name not in ['high', 'low', 'close', 'open'] else 1,
            col=1
        )
