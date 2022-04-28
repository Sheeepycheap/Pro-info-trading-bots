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

class value:
    def __init__(self, dataframe, indice, column, const, valueisconst : bool):
        self.data = dataframe
        self.column = column
        self.value1 = dataframe.loc[int(indice), str(column)]
        if valueisconst:
            self.value1 = const

    def updatevalue(self, indice, const, valueisconst : bool):
        self.value1 = self.data.loc[int(indice), str(self.column)]
        if valueisconst:
            self.value1 = const