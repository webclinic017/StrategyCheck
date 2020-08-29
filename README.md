# StrategyCheck

tool to visualize/check trading strategy so you can use it with your trading bot :]

Currently only for Binance. If you need an account:
[Register on Binance](https://www.binance.com/en/register?ref=23830900)

## Features

- set conditions to filter the data (conf.py)
	- minimum quote asset volume per 24h
	- which quote asset to use (what you pay to buy an asset)
	- candlestick interval and how many days you want to look back
	- which assets should be ignored
- use TA-Lib and custom indicators
	- edit indicators in marked area in gen_candles.py
- save all data as csv

## Used Libraries

[pandas](https://github.com/pandas-dev/pandas)

[python-binance](https://github.com/sammchardy/python-binance)

[TA-Lib](https://github.com/mrjbq7/ta-lib)
