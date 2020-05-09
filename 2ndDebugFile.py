# -*- coding: utf-8 -*-
"""
Created on Thu May  7 17:14:31 2020

@author: thiba
"""

from My_Data import *
import matplotlib.pyplot as plt
import numpy as np

data = My_Data()
data.load_top_gainers_from_csv()
dic = data.get_dict()

df = dic['05_05']

print(len(df['sector'].unique()))

X = df['sector'].unique()

y = []
for sector in X:
    mean_l = []
    for i,value in enumerate(df['sector']):
        if value==sector:
            mean_l.append(float(df['CHG%'][i][:-1]))
    m = sum(mean_l)/max(len(mean_l),1)
    y.append(m)
    
x = np.arange(len(X))

plt.bar(x, height = y)
plt.xticks(x+.2, X, rotation = 90)

plt.ylabel("mean CHG% of top_gainers")
plt.xlabel("sector of activity")