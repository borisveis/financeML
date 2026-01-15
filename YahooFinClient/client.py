import yfinance as yf


class Stock:
    def __init__(self, ticker_symbol: str):
        self.symbol = ticker_symbol.upper()

        try:
            # FIX: Removed the manual session. yfinance now handles
            # browser impersonation internally via curl_cffi.
            self.ticker = yf.Ticker(self.symbol)

            # Using fast_info to validate without heavy scraping
            if not self.ticker.fast_info['currency']:
                raise ValueError(f"Invalid ticker symbol: {self.symbol}")
        except Exception as e:
            raise ValueError(f"Invalid ticker symbol: {self.symbol}") from e

    def get_live_quote(self) -> float:
        """Get the latest price using fast_info"""
        return self.ticker.fast_info['last_price']

    def get_historical_data(self, days: int, should_print: bool = False):
        """Get historical data for the specified number of days"""
        period = f"{days}d"
        historical_data = self.ticker.history(period=period)
        if should_print:
            print(historical_data)
        return historical_data