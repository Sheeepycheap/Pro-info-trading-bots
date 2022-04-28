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
import valueobject as val
class outcondition:
    def __init__(self):
        self.condition = False

    def updatecondition(self, comparator : str, value1 : val, indice1 : int, const1, valueisconst1 : bool, value2 : val,  indice2 : int, const2, valueisconst2 : bool):
        value1.updatevalue(indice1 , const1, valueisconst1)
        value2.updatevalue(indice2 , const2, valueisconst2)
        if comparator == '<=':
            self.condition = value1 <= value2
        elif comparator == '<':
            self.conditon = value1 < value2
        elif comparator == '>=':
            self.condition = value1 >= value2
        elif comparator == '>':
            self.condition = value1 > value2

