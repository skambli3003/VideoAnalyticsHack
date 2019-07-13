# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 16:35:58 2019

@author: skambli
"""


import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib


data = pd.read_csv("BrandStats.csv")
#data = sns.load_dataset('BrandStats')
data = data.pivot('Brands','Month','Visitors')
data.sort_index(level=1, ascending=False, inplace=True)
display_data = sns.heatmap(data,cmap="BuPu",fmt="d")
