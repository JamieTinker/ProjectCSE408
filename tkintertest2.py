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
x=[] #used for timestamps

style.use('fivethirtyeight')
fig = plt.figure(num='Non-Invasive Core Body Temperature', figsize=[13, 3])
ax1 = fig.add_subplot(1, 1, 1)


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
    x.append(dt)
    
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
    
    time.sleep(1)
    
    return sense_data


#animate function for matplotlib to update graph
#animate has its own internal loop. Adding additional
#loops will break the program
def animate(i):
    data = spoof()
    LogData()
    ax1.clear()
    ax1.plot(x, temp1_list)
    ax1.plot(x, temp2_list)
    ax1.plot(x, temp3_list)
    ax1.plot(x, temp4_list)
    ax1.plot(x, temp5_list)
    ax1.legend(['Breath Temp', 'Axilla Temp', 'Ambient Temp 1', 'Ambient Temp 2', 'Estimated Core Body Temp'])
    print(data)

#log data to data.csv
def LogData():
    data = spoof()
    with open('data.csv', 'a', newline = '') as f:
        data_writer = writer(f)
        data_writer.writerow(data)
        
#create nice header at top of data.csv
with open('data.csv', 'w', newline = '') as f:
    data_writer = writer(f)
    data_writer.writerow(['Breath Temp', 'Axilla Temp', 'Ambient Temp 1', 'Ambient Temp 2', 'Estimated Core Body Temp'])

#run animation
#ani = animation.FuncAnimation(fig, animate, interval=100)
#plt.show()



#-----------------------------GUI------------------------

gui = tk.Tk() #init
gui.title("Testing...") #title of window
gui.geometry("1200x600") #size of window

tab_parent = ttk.Notebook(gui)

#init frames for tabs 1 and 2
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)

#add frames to parent with titles
tab_parent.add(tab1, text="Data")
tab_parent.add(tab2, text="More")
tab_parent.add(tab3, text="Graph")


# === WIDGETS FOR TAB ONE
data1LabelTabOne = tk.Label(tab1, text="Core Body Temp: ")
data2LabelTabOne = tk.Label(tab1, text="Ambient Air Temp: ")
data3LabelTabOne = tk.Label(tab1, text="Something Else: ")


#imgLabelTabOne = tk.Label(tab1)

buttonForward = tk.Button(tab1, text="Forward")
buttonBack = tk.Button(tab1, text="Back")



# === ADD WIDGETS TO GRID ON TAB ONE
data1LabelTabOne.grid(row=0, column=0, padx=15, pady=15)
data2LabelTabOne.grid(row=1, column=0, padx=15, pady=15)
data3LabelTabOne.grid(row=2, column=0, padx=15, pady=15)

#imgLabelTabOne.grid(row=0, column=2, rowspan=3, padx=15, pady=15)



# === WIDGETS FOR TAB TWO
firstLabelTabTwo = tk.Label(tab2, text="First Name:")
familyLabelTabTwo = tk.Label(tab2, text="Family Name:")
jobLabelTabTwo = tk.Label(tab2, text="Job Title:")

firstEntryTabTwo = tk.Entry(tab2)
familyEntryTabTwo = tk.Entry(tab2)
jobEntryTabTwo = tk.Entry(tab2)

#imgLabelTabTwo = tk.Label(tab2)

buttonCommit = tk.Button(tab2, text="Add Record to Database")
buttonAddImage = tk.Button(tab2, text="Add Image")



# === ADD WIDGETS TO GRID ON TAB TWO
firstLabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
firstEntryTabTwo.grid(row=0, column=1, padx=15, pady=15)
#imgLabelTabTwo.grid(row=0, column=2, rowspan=3, padx=15, pady=15)

familyLabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
familyEntryTabTwo.grid(row=1, column=1, padx=15, pady=15)

jobLabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
jobEntryTabTwo.grid(row=2, column=1, padx=15, pady=15)

buttonCommit.grid(row=4, column=1, padx=15, pady=15)
buttonAddImage.grid(row=4, column=2, padx=15, pady=15)


# === WIDGETS FOR TAB 3
canvas = FigureCanvasTkAgg(fig, master=tab3)


# === ADD WIDGETS TO TAB 3
canvas.get_tk_widget().grid(row=1, column=1, padx=15, pady=15)


tab_parent.pack(expand=1, fill="both")

ani = animation.FuncAnimation(fig, animate, interval=100)

gui.mainloop()