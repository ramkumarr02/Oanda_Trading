#...............................................................................................
import os
import time
import yaml
import logging
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta

import math
from scipy.stats import linregress

import collections
from IPython import display

# from tqdm import tqdm
# from IPython import display
# import matplotlib.pyplot as plt
# from matplotlib.pyplot import figure

import warnings
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
from oandapyV20.contrib.requests import TakeProfitDetails
from oandapyV20.contrib.requests import MarketOrderRequest
from oandapyV20.contrib.requests import TrailingStopLossDetails
from oandapyV20.contrib.requests import TrailingStopLossOrderRequest
#...............................................................................................


import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs.layout import YAxis,XAxis,Margin