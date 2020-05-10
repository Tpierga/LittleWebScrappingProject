# -*- coding: utf-8 -*-
"""
Created on Thu May  7 11:18:16 2020

@author: thiba
"""

import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import os.path
import re


class My_Data():
    """
    All the methods for manipulating the data are embedded into this class
    """
    def __init__(self):
        self.dict_lastdays_top = {}
        
    def get_df_top_gainers(self, key_today):
        # called to scrapp website and constitute dataframe with data of today
        top_gainers = requests.get("https://www.tradingview.com/markets/stocks-france/market-movers-gainers/")
        
        soup = BeautifulSoup(top_gainers.text, 'lxml')
        
        table = soup.find("table", attrs = {"class":"tv-data-table tv-screener-table"}).find_all("tr", attrs = {"class":"tv-data-table__row tv-data-table__stroke tv-screener-table__result-row"})
        
        # Is recollecting all the labels name of the stocks and store it in indexes list
        indexes = []
        for elem in table:
            valeur = elem.find("a", attrs = {"class":"tv-screener__symbol" })
            indexes.append(valeur.text)
        
        self.dict_lastdays_top[key_today] = pd.DataFrame(columns = ["TICKER", "LAST", "CHG%", "CHG", "RATING", "VOL", "MKT CAP", "P/E", "EPS (TTM)", "EMPLOYEES", "sector"])
        
        rows = soup.find("table", attrs = {"class":"tv-data-table tv-screener-table"}).find_all("tr", attrs = {"class":"tv-data-table__row tv-data-table__stroke tv-screener-table__result-row"})
        
        for i,row in enumerate(rows):
            ligne = []
            row = row.find_all("td")
            for r in row:
                ligne.append(r.text)
                
            self.dict_lastdays_top[key_today].loc[i] = [indexes[i]] + ligne[1:]
    
    def get_today_key(self):
        # the key in dictionary
        now = datetime.datetime.now()
        if now.month<10:
            month = "0"+str(now.month)
        else:
            month = str(now.month)
            
        if now.day<10:
            day = "0"+str(now.day)
        else:
            day = str(now.day)
    
        return month+"_"+day
    
    def save_dict_to_csv(self,today_top_gainers :pd.DataFrame):
        # called to create a new csv file with data
        today_key = self.get_today_key()
    
        today_top_gainers.to_csv("DATA\\"+ today_key + "_top_gainers.csv", sep = ";", index = False)
    
    
    def load_top_gainers_from_csv(self):
        # We are getting values for today and store it in dict object on the model{day:dataframe}  
        for name in os.listdir("DATA"):
            match = re.search(r'[0-9]*_[0-9]*_top_gainers.csv', name)
            if match:
                self.dict_lastdays_top[str(name[:5])] = pd.read_csv("DATA\\"+name, sep = ";", encoding = "latin1")

    def today_refresh(self):
        # function that call get_df_top_gainers if not already called and if called after markets closing hour
        now = datetime.datetime.now()
        self.load_top_gainers_from_csv()
        key_today = self.get_today_key()

        if (key_today not in self.dict_lastdays_top.keys() and (now.hour >= 18)):
            print("get top gainers of today\n")
            self.get_df_top_gainers(key_today)
            print(self.dict_lastdays_top[key_today].head())
            self.save_dict_to_csv(self.dict_lastdays_top[key_today])
            return True
        
        elif (key_today in self.dict_lastdays_top.keys()):
            print("** :) **already in database ***\n\n")
            print(self.dict_lastdays_top[key_today].head())
            return True
            
        elif (key_today not in self.dict_lastdays_top.keys() and (now.hour< 18)):
            print(" wait until 18:00 PM")
            return False
            
        else:
            print("unknown error")
            return False
        
    def bar_chart_one_day(self, day_key):
        # Displays a bar chart corresponding to average
        # of columns CHG% for each sector of activity
        # called to display graph inside application
        
        try : 
            df = self.dict_lastdays_top[day_key]
        except:
            print("Wrong Key entered, can't display chart")
            
        X_names = df['sector'].unique()

        y = []
        for sector in X_names:
            mean_l = []
            for i,value in enumerate(df['sector']):
                if value==sector:
                    mean_l.append(float(df['CHG%'][i][:-1]))
            m = sum(mean_l)/max(len(mean_l),1)
            y.append(m)
        
        return X_names, y

            
    def get_dict(self):
        return self.dict_lastdays_top
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    