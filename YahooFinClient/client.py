import yfinance as yf
import pandas as pd


class Stock:
    def __init__(self, ticker_symbol: str):
        self.symbol = ticker_symbol.upper()

        try:
            # yfinance handles browser impersonation internally
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

    def get_audit_metrics(self):
        """
        Retrieves the 'Point of Truth' features for the 180-day audit.
        Captures analyst consensus, price targets, and fundamental value.
        """
        info = self.ticker.info

        return {
            "symbol": self.symbol,
            "current_price": info.get("regularMarketPrice") or self.get_live_quote(),
            "target_mean": info.get("targetMeanPrice"),
            "target_high": info.get("targetHighPrice"),
            "target_low": info.get("targetLowPrice"),
            "recommendation": info.get("recommendationKey"),
            "analyst_count": info.get("numberOfAnalystOpinions"),
            "book_value": info.get("bookValue"),
            "dividend_yield": info.get("dividendYield"),
            "earnings_date": info.get("calendar", {}).get("Earnings Date", [None])[0]
        }

    def get_relationship_metrics(self, benchmark_ticker="^TNX"):
        """
        Compares this stock's movement against a feature ticker (like 10Y Yield).
        Useful for identifying divergence/anomalies in AWS Lambda.
        """
        stock_history = self.get_historical_data(days=5)['Close']
        # Use string and suppress progress bar for the benchmark download
        benchmark = yf.download(benchmark_ticker, period="5d", progress=False)['Close']

        # Calculate daily percentage changes
        stock_change = stock_history.pct_change().iloc[-1]
        bench_change = benchmark.pct_change().iloc[-1]

        return {
            "ticker_change": float(stock_change),
            "benchmark_change": float(bench_change),
            "divergence": float(stock_change - bench_change)
        }

    def get_full_day_data(self):
        """
        Fetches the most recent day's data including Pre-market and After-hours.
        Used by the cron job to get the 'final' state of the market.
        """
        print(f"Fetching AH data for {self.symbol}...")
        # Fixed: Using self.symbol and explicitly setting progress=False
        data = yf.download(self.symbol, period="1d", interval="1m", prepost=True, progress=False)

        if data.empty:
            return None

        return data.tail(1)

    def get_training_data(self, period="5y"):
        """
        Fetches the moving 5-year window for model retraining.
        """
        # Fixed: Using self.symbol and explicitly setting progress=False
        return yf.download(self.symbol, period=period, prepost=True, progress=False)['Close']