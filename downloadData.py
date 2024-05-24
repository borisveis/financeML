import time

import yfinance as yf
from datetime import datetime, timedelta
import json
configfilepath="config/config.json"
with open(configfilepath, 'r') as f:
    data = json.load(f)
tickers =data["tickers"]
targetdir=data["downloadtargetdir"]

timelength=int(data["timelength"])
# calculate date
current_date = datetime.now()
startdate=current_date-timedelta(days=365*timelength)
for ticker in tickers:
    time.sleep((.1))
    print("downloading "+ticker)
    data=yf.download(tickers, startdate, current_date)
    targetfile = targetdir+"tickersdatefile"+".csv"
data.to_csv(targetfile)

    # data.to_csv(targetfile)
