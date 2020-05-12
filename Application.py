# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:07:31 2020

@author: thiba
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from My_Data import *
import matplotlib.pyplot as plt
import numpy as np


TITLE = ("OCR A Extended", 14)

class App(tk.Tk):
    """
    Here is the logic behind the app
    The other classes below are the pages
    """
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        tk.Tk.iconbitmap(self, default ="esmeicon3.ico")
        
        tk.Tk.wm_title(self, "COVID 19 Time to bet money!")
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = "True")
        
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        
        for F in (HomePage, PageOne, Graphs, Graph_dynam):

            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=0, column = 0, sticky="nsew")
        
        self.show_frame(HomePage)        
        
    def show_frame(self, page_name):
        # Here we move to the top the frame that is called in argument of the function
        front_frame = self.frames[page_name]
        front_frame.tkraise()
        

class HomePage(tk.Frame):
    """
    The first page displayed
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Home Page", font = TITLE)
        label.pack(pady=10, padx=10)
        
        button_page_one = ttk.Button(self, text = "Go to page One", 
                                     command = lambda: controller.show_frame(PageOne))
        button_page_one.pack()
        
        button_bar_chart = ttk.Button(self, text = "Display bar chart", 
                                     command = lambda: controller.show_frame(Graphs))
        button_bar_chart.pack()

class PageOne(tk.Frame):
    """
    This is page one
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page ONE", font=TITLE)
        label.pack(pady=10, padx=10)
        
        button_home = ttk.Button(self, text = "Home Button", 
                                     command = lambda: controller.show_frame(HomePage))
        button_bar_chart = ttk.Button(self, text = "Display plot chart", 
                                     command = lambda: controller.show_frame(Graph_dynam))
        button_home.pack()
        button_bar_chart.pack()
        

class Graphs(tk.Frame):
    """
    This page has a matplotlib bar chart embedded
    """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)
        data = My_Data()
        data.today_refresh()

        button = ttk.Button(self, text="Home Button", command = lambda:controller.show_frame(HomePage))
        button.pack()
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        X_names, y = data.bar_chart_one_day("05_08")
        
        x = np.arange(len(X_names))
        a.bar(x, height = y)
        
        a.set_xticks(x)
        a.set_xticklabels(X_names, rotation = 90)
        a.set_ylabel("mean CHG% by sector")
        a.set_xlabel("sector of activity")
        a.set_title("Bar chart of sector with most change among Top Gainers")
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
class Graph_dynam(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Kraken Graph")
        label.pack(pady=10, padx=10)
        
            
        x = []   #temps
        y = []   #price_list
        nb_plot_counter = 0
        update_graph = False
        update_scrap = False
            
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
                
        def my_personal_spyder_scraping():
            PATH = "https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-USD"
            driver = webdriver.Firefox()
            driver.get(PATH)
            for i in range(5):
                time.sleep(5)
                price = driver.find_element_by_class_name("price")
                print(price.text)
                y.append(float(price.text))
                current_time = time.localtime()
                x.append(time.strftime('%H:%M:%S', current_time))
            driver.close()
                
        def scrap_thread():
            global update_scrap
            print("je lance mon thread")
            while True:
                if update_scrap:
                    my_personal_spyder_scraping()
                else:
                    break
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
            a.lines.pop(0)  # detruit l'ancienne ligne
            nb_plot_counter += 1
            a.plot(x[:nb_plot_counter], y[:nb_plot_counter])  # créer une nouvelle ligne
            a.set_xticks(x)
            a.set_xticklabels(x, rotation = 60)
            canvas.draw()
            self.after(2000, refresh)  # call la fonction apres 2000 ms
        
                
                
        
        button_updating_graph_var = tk.StringVar()
        button_updating_graph = tk.Button(self, textvariable=button_updating_graph_var) #on déclare le bouton et on le bind au tk.StringVar()
        button_updating_graph.pack(side='top')
        button_updating_graph_var.set("Launch graph")
        
        button_updating_scrap_var = tk.StringVar()
        button_updating_scrap = tk.Button(self, textvariable=button_updating_scrap_var)
        button_updating_scrap.pack(side='top')
        button_updating_scrap_var.set("Launch scrap")
        
        button_home = ttk.Button(self, text = "Home Button", 
                                     command = lambda: controller.show_frame(HomePage))
        
        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        """selenium_btceur_kraken_scraping()"""
        a.plot([], [])
        
        """a.set_xticks(x)
        a.set_yticks(y)
        a.set_xticklabels(x, rotation = 60)"""
        a.set_ylabel("valeur de BTC en €")
        a.set_xlabel("heure")
        a.set_title("Valeur de BTC en € sur Kraken")
        
        canvas = FigureCanvasTkAgg(f, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, expand=True)  # recupere le widget tkinter de la figure canva.tk.get...
        
        button_updating_graph.bind("<ButtonRelease-1>", on_click_button_updating_graph)
        button_updating_scrap.bind("<ButtonRelease-1>", on_click_button_updating_scrap)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        