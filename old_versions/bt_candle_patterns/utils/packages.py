#...............................................................................................
import os
import sys
import time
import talib
import numpy as np
import pandas as pd
import datetime as dt

import requests
from config import keys

import math
from scipy.stats import linregress

import collections

from tqdm import tqdm
from IPython import display
from tqdm import tqdm
tqdm.pandas()

import warnings
warnings.filterwarnings('ignore')

# -------------------------------------------------------------------------------

import winsound
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs.layout import YAxis,XAxis,Margin
import webbrowser
#...............................................................................................