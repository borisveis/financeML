import boto3
from datetime import datetime
import os


class AgentMemory:
    def __init__(self, region_name="us-west-1", table_name="AgentPerformance"):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def record_prediction(self, ticker, predicted_price, model_version="v1"):
        """Stores a model prediction with a timestamp."""
        timestamp = datetime.utcnow().isoformat()

        try:
            self.table.put_item(
                Item={
                    'Ticker': ticker,  # Hash Key
                    'Timestamp': timestamp,  # Range Key
                    'PredictedPrice': str(predicted_price),
                    'ModelVersion': model_version,
                    'Status': 'Pending'  # Waiting for market close to verify
                }
            )
            print(f"Successfully recorded prediction for {ticker}")
        except Exception as e:
            print(f"Error writing to DynamoDB: {e}")
            raise e