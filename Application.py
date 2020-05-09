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
        
        for F in (HomePage, PageOne, Graphs):

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
        button_home.pack()


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
        data.bar_chart_one_day("05_08", a)
        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        
        
        
        
        
        