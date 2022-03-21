from pickle import TRUE
from pandas import *
import pandas as pd
import yfinance as yf
import requests as rq
from binance import *
import asyncio
import json
import requests
import time
from matplotlib import *
import matplotlib.pyplot as plt
import numpy as np
dataframe6mois = pd.read_pickle("./dataframe6mois.pkl")
print(dataframe6mois.iloc[-50:])