# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:57:01 2020

@author: thiba
"""
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import os.path
import re


def get_df_top_gainers():
    
    top_gainers = requests.get("https://www.tradingview.com/markets/stocks-france/market-movers-gainers/")
    
    
    soup = BeautifulSoup(top_gainers.text, 'lxml')
    
    
    
    table = soup.find("table", attrs = {"class":"tv-data-table tv-screener-table"}).find_all("tr", attrs = {"class":"tv-data-table__row tv-data-table__stroke tv-screener-table__result-row"})
    
    
    # Is recollecting all the labels name of the stocks and store it in indexes list
    indexes = []
    for elem in table:
        valeur = elem.find("a", attrs = {"class":"tv-screener__symbol" })
        indexes.append(valeur.text)
    
    
    df_top_gainers = pd.DataFrame(columns = ["TICKER", "LAST", "CHG%", "CHG", "RATING", "VOL", "MKT CAP", "P/E", "EPS (TTM)", "EMPLOYEES", "sector"])
    
    rows = soup.find("table", attrs = {"class":"tv-data-table tv-screener-table"}).find_all("tr", attrs = {"class":"tv-data-table__row tv-data-table__stroke tv-screener-table__result-row"})
    
    for i,row in enumerate(rows):
        ligne = []
        row = row.find_all("td")
        for r in row:
            ligne.append(r.text)
            
        df_top_gainers.loc[i] = [indexes[i]] + ligne[1:]  
    
    return df_top_gainers
    

def save_dict_to_csv(today_top_gainers :pd.DataFrame):

    if now.month<10:
        month = "0"+str(now.month)
    else:
        month = str(now.month)
        
    if now.day<10:
        day = "0"+str(now.day)
    else:
        day = str(now.day)

    today_top_gainers.to_csv("DATA\\"+ month +"_"+ day + "_top_gainers.csv", sep = ";")
    

# We are getting values for today and store it in dict object on the model{day:dataframe}

def load_top_gainers_from_csv():
    
    top_gainers = {}
    
    for name in os.listdir("DATA"):
        match = re.search(r'[0-9]*_[0-9]*_top_gainers.csv', name)
        if match:
            top_gainers[str(name[:5])] = pd.read_csv("DATA\\"+name, sep = ";", encoding = "latin1")
    
    return top_gainers


def get_today_key():
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
            
now = datetime.datetime.now()
dict_lastdays_top = {}
dict_lastdays_top = load_top_gainers_from_csv()

key_today = get_today_key()

if (key_today not in dict_lastdays_top.keys() and (now.hour >= 18)):
    
    print("get top gainers of today\n")
    dict_lastdays_top[key_today] = get_df_top_gainers()
    print(dict_lastdays_top[key_today].head())
    save_dict_to_csv(dict_lastdays_top[key_today])

    
elif (key_today in dict_lastdays_top.keys()):
    print("** :) **already in database ***\n\n")
    print(dict_lastdays_top[key_today].head())
    
elif (key_today not in dict_lastdays_top.keys() and (now.hour< 18)):
    print(" wait until 18:00 PM")
    
else:
    print("unknown error")
    


    
app = App()
app.mainloop()
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    














 

    
    
    


# getting to real time data collecting





