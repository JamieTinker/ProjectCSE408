from tkinter import *
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

class Window(Frame):
    
    #define initialization settings
    def __init__(self, master=None):
        #perameters that you want ot send through the frame class
        Frame.__init__(self, master)
        
        #reference to the master widget, which is tk window
        self.master = master
        
        #with that, run init_window, (doesn't exitst yet)
        self.init_window()
        
    #creation of init_window
    def init_window(self):
        #-------------------INIT-------------------
        #change title
        self.master.title("Non-Invasive Core Body Temperature")
        
        #allow the widget to take the full space of the root window
        self.pack(fill=BOTH, expand=1)
        
        #---------------MENU - Cascade------------------
        
        #create menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        
        #create file object for menu
        file = Menu(menu)
        
        #adds command to the menu option, calling it exit
        file.add_command(label="exit", command=self.client_exit)
        
        #add file to our menu
        menu.add_cascade(label="File", menu=file)
        
        #create file object
        edit = Menu(menu)
        
        #add command to menu option
        edit.add_command(label="Undo")
        
        #add "edit" to menu
        menu.add_cascade(label="Edit", menu=edit)
        
        
        #-------------BUTTONS----------------
        '''
        #creation of button
        quitButton = Button(self, text="Quit", command=self.client_exit)
        
        #place button on window
        quitButton.place(x=5, y=5)
        '''
        
        
        '''       
            #-------------TABS--------------------
        tabControl = ttk.Notebook(self)
        
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text = "Tab 1")
        
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text = "Tab 2")
        
        
        
        #------------TAB1 STUFF--------------
        data1LabelTabOne = tk.Label(tab1, text="Data 1")
        data2LabelTabOne = tk.Label(tab1, text="Data 2")
        
        data1LabelTabOne = tk.Entry(tab1)
        data2LabelTabTwo = tk.Entry(tab1)
        
        #imgLabelTabOne = tk.Label(tab1)
        
        buttonForward = tk.Button(tab1, text="Forward")
        buttonBack = tk.Button(tab1, text="Back")
        
        
            #------------LIVE GRAPH--------------
        #trying to pack matplotlib animate in window
        #canvas = FigureCanvasTkAgg(fig, root)
        #canvas.get_tk_widget().grid(row=5, column=5, padx=15, pady=15)
        
        
        #--------ADD TAB 1 STUFF TO TAB1 GRID---------
        data1LabelTabOne.grid(row=0, column=0, padx=15, pady=15)
        data1EntryTabOne.grid(row=0, column=1, padx=15, pady=15)
        
        data2LabelTabOne.grid(row=1, column=0, padx=15, pady=15)
        data2entryTabOne.grid(row=1, column=1, padx=15, pady=15)

    
        
        tabControl.pack(expand=1, fill="both")
        
        '''
        
        #-------------TXT BOXES---------------
        
        
        
        
        
        
        
        
        
        #------------LIVE GRAPH--------------
        #trying to pack matplotlib animate in window
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.get_tk_widget().pack()
        

    def client_exit(self):
        exit()
        
root = Tk()

#size of window
root.geometry("800x800")

app = Window(root)

ani = animation.FuncAnimation(fig, animate, interval=100)

root.mainloop()