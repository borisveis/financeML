import os
import requests
from dotenv import load_dotenv

load_dotenv()


class SeekingAlphaClient:
    def __init__(self):
        self.api_key = os.getenv("RAPIDAPI_KEY")
        self.host = "seeking-alpha-api.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": self.host,
            "Content-Type": "application/json"
        }

    def get_metrics(self, tickers: list):
        """
        Retrieves price returns and metric data for a list of tickers.
        """
        url = f"https://{self.host}/metrics"
        params = {"slugs": ",".join([t.lower() for t in tickers])}

        try:
            res = requests.get(url, headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json()
                return data.get('metrics', [])
            return []
        except Exception as e:
            print(f"[ERROR] Metrics fetch failed: {e}")
            return []

    def get_analyst_summary(self, ticker: str):
        """
        Retrieves the aggregate analyst counts and recommendation volume.
        """
        url = f"https://{self.host}/analyst-recommendation"
        params = {"symbol": ticker.lower()}

        try:
            res = requests.get(url, headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json()
                metrics = data.get('metrics', [])
                if metrics:
                    return metrics[0]
            return None
        except Exception as e:
            print(f"[ERROR] Analyst summary fetch failed: {e}")
            return None

    def get_real_time_quote(self, ticker: str):
        """
        Retrieves real-time quote data (last price, volume, etc.).
        """
        url = f"https://{self.host}/recommendation"
        params = {"symbol": ticker.lower()}

        try:
            res = requests.get(url, headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json()
                quotes = data.get('real_time_quotes', [])
                if quotes:
                    return quotes[0]
            return None
        except Exception as e:
            print(f"[ERROR] Real-time quote fetch failed: {e}")
            return None