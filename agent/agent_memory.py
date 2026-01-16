import boto3
from datetime import datetime
from decimal import Decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


class AgentMemory:
    def __init__(self, table_name='AgentPerformance'):
        # Boto3 uses the 'default' profile from ~/.aws/config automatically
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def record_prediction(self, ticker: str, mse: float, strategy: str):
        """Stores model performance in DynamoDB for future reflection"""
        timestamp = datetime.now().isoformat()

        # DynamoDB requires Numbers to be stored as Decimals, not Floats
        item = {
            'Ticker': ticker.upper(),
            'Timestamp': timestamp,
            'MSE': Decimal(str(mse)),
            'Strategy': strategy,
            'Status': 'SUCCESS'
        }

        try:
            self.table.put_item(Item=item)
            print(f"Memory logged for {ticker}: MSE {mse:.4f}")
        except ClientError as e:
            print(f"Boto3 Error: {e.response['Error']['Message']}")

    def get_performance_history(self, ticker: str, limit: int = 5):
        """Queries the last X runs to allow the agent to 'reflect'"""
        try:
            response = self.table.query(
                KeyConditionExpression=Key('Ticker').eq(ticker.upper()),
                ScanIndexForward=False,  # Newest first
                Limit=limit
            )
            return response.get('Items', [])
        except Exception as e:
            print(f"Failed to query history: {e}")
            return []