import tkinter as tk
from tkinter import ttk
import time
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from csv import writer
from datetime import datetime

plt.style.use('fivethirtyeight')


fig1, ax1 = plt.subplots()

line1, = ax1.plot(0, 0)


fig2, ax2 = plt.subplots()

line2, = ax2.plot(0, 0)


data1 = []
data2 = []

timedata = []

def dataset():
    timedata.append(datetime.now())
    data1.append(random.randint(1, 20))
    data2.append(random.randint(25, 88))
    

def animate(i):
    dataset()
    
    line1.set_xdata(
    
    