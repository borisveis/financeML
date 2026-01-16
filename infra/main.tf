terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_dynamodb_table" "agent_performance" {
  name           = "AgentPerformance"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "Ticker"
  range_key      = "Timestamp"

  attribute {
    name = "Ticker"
    type = "S"
  }

  attribute {
    name = "Timestamp"
    type = "S"
  }

  tags = {
    Project = "financeML"
  }
}

output "table_name" {
  value = aws_dynamodb_table.agent_performance.name
}

