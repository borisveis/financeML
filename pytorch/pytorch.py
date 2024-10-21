import torch
import torch.nn as nn
import torch.optim as optim
import pandas
from YahooFinClient import client
import _pytest
#1D tensor
onedimtens=torch.tensor([1,2,3,4,56,7,8])
def test_progess():
    # print(onedimtens)
    # print an index
    # print(onedimtens[2])
    # print a slice. "step is optional"
    print(onedimtens[1:4])
    # 2dim tensors
    twodimtens = torch.tensor([[1, 2], [3, 4]])
    GGOG5days=client.get_historical_data("GOOG",5)
    AAPL5days=client.get_historical_data("AAPL",5)
    SPY5days=client.get_historical_data("SPY",5)
