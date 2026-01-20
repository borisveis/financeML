import boto3
import yfinance as yf
from datetime import datetime
from agent.agent_memory import AgentMemory


class Reflector:
    def __init__(self, table_name="AgentPerformance"):
        self.memory = AgentMemory(table_name=table_name)
        self.table = self.memory.table

    def run_reflection(self):
        """Processes all pending predictions and grades them."""
        # 1. Fetch pending items
        response = self.table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr('Status').eq('Pending')
        )
        pending_items = response.get('Items', [])

        for item in pending_items:
            ticker = item['Ticker']
            predicted = float(item['PredictedPrice'])

            # 2. Get actual price (simplifying for 'now' vs historical)
            # In production, we'd use the stored Timestamp to get historical close
            stock = yf.Ticker(ticker)
            actual_price = stock.history(period="1d")['Close'].iloc[-1]

            # 3. Calculate Accuracy
            error = abs(predicted - actual_price)
            accuracy_score = (1 - (error / actual_price)) * 100

            # 4. Update the record
            self.table.update_item(
                Key={'Ticker': ticker, 'Timestamp': item['Timestamp']},
                UpdateExpression="SET #s = :val, ActualPrice = :ap, Accuracy = :acc",
                ExpressionAttributeNames={'#s': 'Status'},
                ExpressionAttributeValues={
                    ':val': 'Verified',
                    ':ap': str(actual_price),
                    ':acc': str(accuracy_score)
                }
            )
            print(
                f"Reflected on {ticker}: Predicted {predicted}, Actual {actual_price:.2f}. Accuracy: {accuracy_score:.2f}%")


if __name__ == "__main__":
    Reflector().run_reflection()