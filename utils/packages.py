# Normal Packages
import sys
import pytz
import yaml
import time
import json
import warnings
import datetime
import winsound
import statistics
import numpy as np
import collections
import pandas as pd
from tqdm import tqdm
from IPython import display
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Oanda Packages
from oandapyV20 import API
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.transactions as trans
import oandapyV20.endpoints.positions as positions
import oandapyV20.definitions.pricing as defpricing
import oandapyV20.endpoints.instruments as instruments
from oandapyV20.contrib.requests import StopLossDetails
from oandapyV20.contrib.requests import MarketOrderRequest