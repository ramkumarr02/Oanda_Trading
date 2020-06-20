# Normal Packages

import numpy as np
import pandas as pd

import yaml
import json

import sys
import time
import pytz
import datetime
import winsound
import collections

from tqdm import tqdm

import warnings
warnings.filterwarnings('ignore')

# Oanda Packages

from oandapyV20 import API
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.pricing as pricing
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.transactions as trans
import oandapyV20.endpoints.positions as positions

import oandapyV20.definitions.pricing as defpricing

import oandapyV20.endpoints.instruments as instruments

from oandapyV20.contrib.requests import (MarketOrderRequest, StopLossDetails)