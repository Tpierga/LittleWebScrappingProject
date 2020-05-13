# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:07:31 2020

@author: thiba
"""
import tkinter as tk
from tkinter import ttk
import matplotlib
import time
from threading import Thread
matplotlib.use("TkAgg")
from selenium import webdriver
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from My_Data import *

import matplotlib.pyplot as plt
import numpy as np

TITLE = ("OCR A Extended", 14)

update_graph = False
update_scrap = False
nb_plot_counter = 0

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
        frame1 = tk.Frame(self)
        frame2 = tk.Frame(self)
        button_page_one = ttk.Button(frame1, text = "Go to page One",
                                     command = lambda: controller.show_frame(PageOne))
        button_page_one.pack(side ='left')
        button_bar_chart = ttk.Button(frame1, text = "Display bar chart",
                                     command = lambda: controller.show_frame(Graphs))
        button_bar_chart.pack(side ='left')
        button_bar_chart = ttk.Button(frame1, text = "Display plot chart",
                                     command = lambda: controller.show_frame(Graph_dynam))
        button_bar_chart.pack(side ='left')
        frame1.pack(side='top')
        
        signature = tk.Label(frame2,text ="Application de Thibault Pierga et Yoann Randon",font =TITLE)
        signature.pack(side='top')
        frame2.pack(side='bottom')
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
        def display_bar_chart(key):
            f = Figure(figsize=(5,5), dpi=100)
            a = f.add_subplot(111)
            X_names, y = data.bar_chart_one_day(key)
            x = np.arange(len(X_names))
            a.bar(x, height = y)
            a.set_xticks(x)
            a.set_xticklabels(X_names, rotation = -45)
            a.tick_params(axis='both', which='major', labelsize=5)
            a.set_ylabel("mean CHG% by sector")
            a.set_xlabel("sector of activity")
            a.set_title("Bar chart of sector with most change among Top Gainers")
            canvas = FigureCanvasTkAgg(f, self)
            canvas.draw()
            canvas.get_tk_widget().grid(row=4, columnspan = 4,  sticky="nsew")
        def callbackChoice(event):
            print(comboList.get())
            display_bar_chart(comboList.get())
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Who are today top gainers ?", font = TITLE)
        label.grid(column=1, row=0)
        data = My_Data()
        data.today_refresh()
        button = ttk.Button(self, text="Home", command = lambda:controller.show_frame(HomePage))
        button.grid(column = 2, row = 0)
        labelChoice = tk.Label(self, text = "Choose which day you want the data for :")
        labelChoice.grid(column=0, row=1)
        comboList = ttk.Combobox(self, values = [key for key in data.get_dict().keys()])
        comboList.grid(column=0, row=2)
        comboList.current(len(data.get_dict().keys())-1)
        display_bar_chart(comboList.get())
        comboList.bind("<<ComboboxSelected>>", callbackChoice)
        
#class to define the frame where the Selenium scraping will be display
class Graph_dynam(tk.Frame):
    # Constructor of the class
    def __init__(self, parent, controller):
        #Create a Frame called "Kraken Graph" with specific dimension
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Kraken Graph")
        label.pack(pady=10, padx=10)
          
        #initialization of the list which will store data
        x = []   #time
        y = []   #price_list
        
        #method which operate when the user click on the updating scrap button
        def on_click_button_updating_scrap(event):
            #recover the global variable
            global update_scrap
            global run
            #if you click on Stop scrap
            if update_scrap:
                #update the flag
                update_scrap = False
                #update the name of the updating scrap button
                button_updating_scrap_var.set("Launch scrap")
            #if you click on Launch scrap
            else:
                #update the flag
                update_scrap = True
                #update the name of the updating scrap button
                button_updating_scrap_var.set("Stop scrap")
                #Create a thread which will execute scrap_thread
                thread_1 = Thread(target=scrap_thread)
                #launch the thread
                thread_1.start()
               
        #Scrap method
        def my_personal_spyder_scraping():
            #Define the URL of the website u want to scrap
            PATH = "https://trade.kraken.com/fr-fr/charts/KRAKEN:BTC-USD"
            #define the driver
            driver = webdriver.Firefox()
            #open the driver at the URL defined
            driver.get(PATH)
            #recover the global variable
            global update_scrap
            #Until the flag say you are scraping
            while update_scrap:
                #wait 5 second
                time.sleep(5)
                #get the element in the website with the class "price"
                price = driver.find_element_by_class_name("price")
                #print this value
                print(price.text)
                #add this value to the list y
                y.append(float(price.text))
                #get the current time
                current_time = time.localtime()
                #add the time to the list x
                x.append(time.strftime('%H:%M:%S', current_time))
            #when you stop scraping close   the driver 
            driver.close()
              
        #method to controll the scraping method
        def scrap_thread():
            #recover the global variable
            global update_scrap
            #if the flag say you are scraping
            if update_scrap:
                #launch the scrap method
                my_personal_spyder_scraping()
              
        #method which operate when the user click on the updating graph button 
        def on_click_button_updating_graph(event):
            #recover the global variable
            global update_graph
            #if you clic on stop graph
            if update_graph:
                #update the flag
                update_graph = False
                #update the name of the updating graph button
                button_updating_graph_var.set("Launch graph")
            #if you clic on launch graph
            else:
                #update the flag
                update_graph = True
                #update the name of the updating graph button
                button_updating_graph_var.set("Stop graph")
                #launch refresh method
                refresh()
        #method to refresh the display of the graph
        def refresh():
            #recover the global variable
            global update_graph   
            global update_scrap
            global nb_plot_counter
            #if the flag say you are not updating the graph
            if not update_graph:
                #stop refresh
                return
            #detroy the previous line of the graph
            a.lines.pop(0)  
            #increment the variable nb_plot_counter
            nb_plot_counter += 1
            #stop the update of the graph of you display all the data collected
            if (nb_plot_counter  >= len(y) and update_scrap == False) :
                print('dernière valeur avant la fin du tableau')
                #update the flag
                update_graph = False
                #update the name of the updating graph button
                button_updating_graph_var.set("Launch graph")
                
            #if the last value is lower than the previous one 
            if y[nb_plot_counter-1] < y[nb_plot_counter-2]:
                #change the comment value
                texte_etat_var.set("the value of BTC decrease")
                #display the graph in red
                a.plot(x[:nb_plot_counter], y[:nb_plot_counter],marker='*',linestyle = 'dashed', linewidth = 2, color = 'red')  # créer une nouvelle ligne
                #set the x axis and change the orientation of values
                a.set_xticklabels(x[:nb_plot_counter], rotation = 50)
                #draw the graph
                a.tick_params(axis ='both',which='major',labelsize=9)
                canvas.draw()
            #if the last value is equal than the previous one 
            if y[nb_plot_counter-1] == y[nb_plot_counter-2]:
                #same thing as above
                texte_etat_var.set("the value of BTC don't change")
                #color in gray
                a.plot(x[:nb_plot_counter], y[:nb_plot_counter],marker='*',linestyle = 'dashed', linewidth = 2, color = 'gray')  # créer une nouvelle ligne
                a.set_xticklabels(x[:nb_plot_counter], rotation = 50)
                a.tick_params(axis ='both',which='major',labelsize=9)
                canvas.draw()
            #if the last value is greater than the previous one 
            if y[nb_plot_counter-1] > y[nb_plot_counter-2]:
                #same thing as above
                texte_etat_var.set("the value of BTC increase")
                #color in green
                a.plot(x[:nb_plot_counter], y[:nb_plot_counter],marker='*',linestyle = 'dashed', linewidth = 2, color = 'green')  # créer une nouvelle ligne
                a.set_xticklabels(x[:nb_plot_counter], rotation = 50)
                a.tick_params(axis ='both',which='major',labelsize=9)
                canvas.draw()
            #call refresh method in 5 ms
            self.after(5000, refresh)  
        
                
       
        #define a button to update the graph with a variable text and put it at the top of the frame Graph_dynam
        button_updating_graph_var = tk.StringVar()
        button_updating_graph = tk.Button(self, textvariable=button_updating_graph_var) #on déclare le bouton et on le bind au tk.StringVar()
        button_updating_graph.pack(side='top')
        #give a value to the  variable text
        button_updating_graph_var.set("Launch graph")
        
        #define a button to update the graph with a variable text and put it at the top of the frame Graph_dynam
        button_updating_scrap_var = tk.StringVar()
        button_updating_scrap = tk.Button(self, textvariable=button_updating_scrap_var)
        button_updating_scrap.pack(side='top')
        #give a value to the  variable text
        button_updating_scrap_var.set("Launch scrap")
        
        #define a text variable for the comment of the graph
        texte_etat_var = tk.StringVar()
        texte_etat = tk.Label(self, textvariable=texte_etat_var)
        texte_etat.pack(side='bottom')
        #give a value to the  variable text
        texte_etat_var.set("Neutral")
        
        #add a button to go to home page
        button_home = ttk.Button(self, text = "Home Button", 
                                     command = lambda: controller.show_frame(HomePage))
        button_home.pack()
        
        #create a figure
        f = Figure(figsize=(5,5), dpi=100)
        #create 1 subplot in the figure
        a = f.add_subplot(111)
        """selenium_btceur_kraken_scraping()"""
        #define a plot to avoid the error on the command a.pop(0)
        a.plot([], [])
        
        #set label and title of the figure and axis
        a.set_ylabel("valeur de BTC en €")
        a.set_xlabel("heure")
        a.set_title("Valeur de BTC en € sur Kraken")
        
        #define a canvas which will contain the figure
        canvas = FigureCanvasTkAgg(f, self)
        #display the canvas at the bottom of the frame Graph_dynam
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.X, expand=True)  
        
        #bind the button with the appropriate method
        button_updating_graph.bind("<ButtonRelease-1>", on_click_button_updating_graph)
        button_updating_scrap.bind("<ButtonRelease-1>", on_click_button_updating_scrap)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        