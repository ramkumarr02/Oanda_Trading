#...............................................................................................
import os
import sys
import yaml
import numpy as np
import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta

import math
from scipy.stats import linregress

import collections
from collections import Counter

from tqdm import tqdm
from IPython import display
import plotly.express as px
import plotly.graph_objects as go
from plotly.graph_objs.layout import YAxis,XAxis,Margin

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

from tqdm import tqdm
tqdm.pandas()

import webbrowser
import requests
from config import keys

import warnings
warnings.filterwarnings('ignore')
#...............................................................................................