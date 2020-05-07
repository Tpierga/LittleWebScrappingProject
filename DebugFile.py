# -*- coding: utf-8 -*-
"""
Created on Tue May  5 20:14:00 2020

@author: thiba
"""
import os
import re
import datetime
import pandas as pd

def load_top_gainers_from_csv():
    
    top_gainers = {}
    
    for name in os.listdir("DATA"):
        match = re.search('[0-9]*_[0-9]*_top_gainers.csv', name)
        if match:
            path = "DATA" +"\\" + name
            df = pd.read_csv(path, sep = ";", encoding = 'latin1')
            print(path)
            top_gainers[name[3:5]] = df
    return top_gainers
            
now = datetime.datetime.now()

dict_top_lastdays = {}
dict_top_lastdays=load_top_gainers_from_csv()