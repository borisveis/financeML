Executed by running ML_Stock_Movement.py

Implements Yahoo Finance's yfinance package to fetch live and historical stock daily closing price data a moving 5-year time frame.
Data is retrieved as Pandas data frames
Model is trained using  sklearn linear regression
Plots are generated demonstrating predicted vs. actual visually
# Infrastructure, Terraform, TerraTest
    validation: cd /infra/test
### % go test
