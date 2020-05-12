# -*- coding: utf-8 -*-
"""
Created on Tue May 12 19:15:52 2020

@author: yoann
"""


import tkinter as tk
import time
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread
from selenium import webdriver
from Application import *


nb_plot_counter = 0
update_graph = False
update_scrap = False
run = False
y = []
x = []

    
def my_personal_spyder_scraping():
    PATH = "https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-USD"
    driver = webdriver.Firefox()
    driver.get(PATH)
    global update_scrap
    while update_scrap:
        time.sleep(5)
        price = driver.find_element_by_class_name("price")
        print(price.text)
        y.append(float(price.text))
        current_time = time.localtime()
        x.append(time.strftime('%H:%M:%S', current_time))
    driver.close()
    
def on_click_button_updating_scrap(event):
    global update_scrap
    if update_scrap:
        update_scrap = False
        button_updating_scrap_var.set("Launch scrap")
    else:
        update_scrap = True
        button_updating_scrap_var.set("Stop scrap")
        global thread_1
        thread_1 = Thread(target=scrap_thread)
        thread_1.start()
    print("quelqu'un a cliqué scrap", event.x, event.y)
    
def scrap_thread():
    global update_scrap
    my_personal_spyder_scraping()
    print("je lance mon thread")
    if not update_scrap:
        print("j'ai fini mon thread")
    
def on_click_button_updating_graph(event):
    global update_graph
    if update_graph:
        update_graph = False
        button_updating_graph_var.set("Launch graph")
    else:
        update_graph = True
        button_updating_graph_var.set("Stop graph")
        refresh()

    print("quelqu'un a cliqué", event.x, event.y)

def refresh():
    global update_graph    
    if not update_graph:
        print("je m'arrete")
        return
    global nb_plot_counter
    print("I'm refresh")
    ax.lines.pop(0)  # detruit l'ancienne ligne
    nb_plot_counter += 1
    ax.plot(x[:nb_plot_counter], y[:nb_plot_counter])  # créer une nouvelle ligne
    ax.xticks(range(0,len(x),3),rotation = 60)
    canvas.draw()
    app.after(5000, refresh)  # call la fonction apres 5000 ms