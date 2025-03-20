# multiple_classes.py

import yfinance
class Stock:
    ticker="default"

    def __init__(self, symbol):
        self.symbol = symbol
        ticker=yfinance.Ticker(symbol)

    def getlast(self):
        self.ticker.info





class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def info(self):
        return f"This car is a {self.year} {self.make} {self.model}."
