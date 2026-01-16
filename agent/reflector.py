from YahooFinClient import client
from agent.agent_memory import AgentMemory  # We will create this next


class Reflector:
    def __init__(self):
        self.memory = AgentMemory()

    def decide_strategy(self, ticker):
        """
        Reflects on past performance to choose the best data features.
        """
        history = self.memory.get_last_performance(ticker)

        if not history:
            print("No memory found. Defaulting to 'Price + Volume' strategy.")
            return "price_volume"

        # Simple logic: Compare the latest MSE to a threshold
        latest_mse = float(history[0]['MSE'])
        if latest_mse > 0.05:
            print(f"Latest MSE ({latest_mse}) is high. Switching to high-complexity features.")
            return "price_volume_sentiment"
        else:
            print(f"Performance is stable (MSE: {latest_mse}). Staying with current strategy.")
            return "price_volume"