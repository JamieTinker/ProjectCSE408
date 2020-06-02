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

#Experimenting with graph
temp1_list=[] #mask
temp2_list=[] #armpit
temp3_list=[] #ambient
temp4_list=[] #bpmtemp
temp5_list=[] #estimated core body temperature
time_list=[] #used for timestamps

style.use('fivethirtyeight')

fig1, ax11 = plt.subplots()
'''
ax11.set_ylim(ymin=0, ymax=100)
ax11.set_title("")
ax11.set_xlabel("")
ax11.set_ylabel("")
ax11.grid = true
'''

fig2, ax12 = plt.subplots()
'''
ax11.set_ylim(ymin=0, ymax=100)
ax11.set_title("")
ax11.set_xlabel("")
ax11.set_ylabel("")
ax11.grid = true
'''

tempx = [[0]]
tempy = [[0]]
rhx = []
rhy = []


def spoofRawMaskTemp():
    #spoof mask sensor temp
    rawmasktemp = random.randint(88, 92)
    
    temp1_list.append(rawmasktemp)
    
    return rawmasktemp


def spoofArmpitTemp():
    #spoof armpit sensor temp
    armpittemp = random.randint(96, 98)
    
    temp2_list.append(armpittemp)

    return armpittemp


lines_temp1 = []
lines_temp2 = []
lines_temp1.append(ax11.plot(time_list,temp1_list)[0])
lines_temp2.append(ax12.plot([],[])[0])





#fig = plt.figure(num='Non-Invasive Core Body Temperature', figsize=[13, 3])
#ax1 = fig.add_subplot(1, 1, 1)


def spoof():
    
    sense_data = []
    
    #spoof mask sensor temp
    rawmasktemp = random.randint(88, 92)
    
    #spoof armpit sensor temp
    armpittemp = random.randint(96, 98)
    
    #spoof ambient air temp
    ambienttemp = random.randint(75, 77)
    
    #spoof data from bpm180
    bpmtemp = random.randint(76, 78)
    
    
    #estimate core body temp
    estcoretemp = rawmasktemp + 10 #temp calculation
    
    #get timestamp
    dt=datetime.now()
    #save timestamp
    time_list.append(dt)
    
    #save temp data
    temp1_list.append(rawmasktemp)
    temp2_list.append(armpittemp)
    temp3_list.append(ambienttemp)
    temp4_list.append(bpmtemp)
    temp5_list.append(estcoretemp)
    
    sense_data.append(rawmasktemp)
    sense_data.append(armpittemp)
    sense_data.append(ambienttemp)
    sense_data.append(bpmtemp)
    sense_data.append(estcoretemp)
    sense_data.append(dt)
    
    time.sleep(.25)
    
    return sense_data

'''
def animate1(i):
    data = spoof()
    ax1.clear()
    ax1.plot(x, temp1_list)
    ax1.legend(['data 1'])
    print(data)


def animate2(i):
    data = spoof()
    ax1.clear()
    ax1.plot(x, temp2_list)
    ax1.legend(['data 1'])
    print(data)
'''


def animate(t, x, y, lines, ax):
    time_list.append(datetime.now())
 
    x[0].append(x[0][-1] + 1)
    y[0].append(random.randrange(1, 100, 1))
        
   
    lines[0].set_data(x[0], y[0])
    ax.relim()
    ax.autoscale_view()
        
        
   
   
   
#run animation
ani1 = animation.FuncAnimation(fig1, animate, interval=1000, fargs=(tempx, tempy, lines_temp1, ax11))
ani2 = animation.FuncAnimation(fig2, animate, interval=1000, fargs=(tempx, tempy, lines_temp2, ax12))

plt.show()