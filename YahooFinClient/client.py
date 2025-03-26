import yfinance as yf


class Stock:
    def __init__(self, ticker_symbol: str):
        self.symbol = ticker_symbol
        try:
            self.ticker = yf.Ticker(ticker_symbol)
            # Attempt to fetch basic info to validate the ticker symbol
            info = self.ticker.info
            if not info or 'longName' not in info:
                raise ValueError(f"Invalid ticker symbol: {ticker_symbol}")
        except Exception as e:
            raise ValueError(f"Invalid ticker symbol: {ticker_symbol}") from e

        self.symbol = ticker_symbol


    def get_live_quote(self) -> float:
        """Get the latest closing price"""
        hist = self.ticker.history(period='1d')
        if hist.empty:
            raise ValueError(f"No data found for {self.symbol}")
        return hist['Close'].iloc[-1]

    def get_historical_data(self, days: int, should_print: bool = False):
        """Get historical data for the specified number of days"""
        period = f"{days}d"
        historical_data = self.ticker.history(period=period)
        if should_print:
            print(historical_data)
        return historical_data
