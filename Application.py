# -*- coding: utf-8 -*-
"""
Created on Wed May  6 20:07:31 2020

@author: thiba
"""
import tkinter as tk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class App(tk.Tk, top_gainers_dict):
    
    def __init__(self):
        
        tk.Tk.__init__(self)
        
        tk.Tk.wm_title(self, "tkinter app displaying graphs")
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = "True")
        self.frames = {}
        frame = Graphs(container, self)
        self.frames[Graphs] = frame
        
        self.show_frame(Graphs)
        
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()


class Graphs(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!")
        label.pack(pady=10, padx=10)
        
        #button = ttk.Button(self, text="Afficher Graphs", command = lambda:controller.show_frame(StartPage))
        #button.pack
        
        f = Figure(figsize=(5,5), dpi=100)
        colors = ["blue", "red", "green", "orange", "yellow", "brown", "black"]

        X = df['Date']
        for i,k in enumerate(sorted_e_dict.keys()):
            Y = df[k]
            plt.plot(X,Y, c = colors[i], label = k)


        #Y = df['Total (MW)']
        #plt.plot(X,Y, c = 'pink', label = 'Total (MW)')
        plt.xticks(range(0,len(df), 20), rotation = 90)
        plt.title('The amount of energy produced during the day')
        plt.xlabel('time')
        plt.ylabel('Energie Produced (MW)')
        plt.legend( loc = "upper left")
        plt.show()

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        
        
        
        
        