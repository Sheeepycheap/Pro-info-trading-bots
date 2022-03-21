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
from datetime import datetime
from math import *
from decimal import *
# from glassnode import GlassnodeClient
import requests

# gn = GlassnodeClient(api_key='24e3Ul4RZRhcgFz4PR9lRhbx60o')

# def btcpercentagesupplyinprofit(asset,freq):
#     return  gn.get(
#     'https://api.glassnode.com/v1/metrics/indicators/sopr',
#     {'a':'BTC',
#     's':'2020-01-01',
#     'i':'24h'}
# )

response = requests.get('https://api.glassnode.com/v1/metrics/supply/profit_relative',{'api_key':'24e3Ul4RZRhcgFz4PR9lRhbx60o',
 'a':'BTC',
 's': int(time.time()),
 'f':'JSON' })
bdd = response.json()
bdd = pd.json_normalize(bdd)
print(bdd.tail(20))