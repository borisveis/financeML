Executed by running ML_Stock_Movement.py

Implements Yahoo Finance's yfinance package to fetch live and historical stock daily closing price data a moving 5-year time frame.
Data is retrieved as Pandas data frames
Model is trained using  sklearn linear regression
Plots are generated demonstrating predicted vs. actual visually
# Infrastructure, Terraform, TerraTest
    validation: cd /infra/test
        % go test
# unit and functional test
    cd <repo root>
### % python -m pytest
#  Architecture
# configuration
## target_ticker - Dependent ticker whose predictions will depend on price action of feature_tickers
## feature_tickers - Independent tickers whose price action is used to predict price of target_ticker
## Agents
### memory
Handles data ingestion and model execution.
Responsibility: Generates daily stock movement forecasts.

Key Action: Ingests 5 years of historical data (including After-Hours sessions) to train a Multivariate Regression model.

Output: Saves a serialized .joblib model and creates a "Pending" entry in the local prediction_history.csv.
### reflector("Auditor) 
acts as the project's QA Manager. It provides the essential feedback loop to ensure the model stays grounded in reality.

Responsibility: Grades the accuracy of previous predictions.

Key Action: Retrieves actual closing prices for "Pending" records and compares them to the Predictor’s results.

Output: Updates the historical record with Quality Scores (e.g., Mean Absolute Error) and marks predictions as "Verified".
