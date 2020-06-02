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
from PIL import Image, ImageTk
from tkinter import filedialog

#Experimenting with graph
temp1_list=[] #mask
temp2_list=[] #armpit
temp3_list=[] #bpmtemp
temp4_list=[] #estimated core body temperature
x=[] #used for timestamps

#
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
    temp3_list.append(bpmtemp)
    temp4_list.append(estcoretemp)
    
    sense_data.append(rawmasktemp)
    sense_data.append(armpittemp)
    sense_data.append(bpmtemp)
    sense_data.append(estcoretemp)
    sense_data.append(dt)
    
    time.sleep(.25)
    
    return sense_data

#initialize the lists 
datainit = spoof()

#Used to update and draw live graph + update data labels
def animate(i):
    data = spoof()
    LogData()
    ax1.clear()
    ax1.plot(x, temp1_list)
    ax1.plot(x, temp2_list)
    ax1.plot(x, temp3_list)
    ax1.plot(x, temp4_list)
    ax1.legend(['Breath Temp', 'Axilla Temp', 'Ambient Temp', 'Estimated Core Body Temp'])
    print(data)
    updateDataLabels(coreBodyTempLabel, ambientTempLabel, axillaTempLabel, maskTempLabel)


#auto log data to data.csv
def LogData():
    data = spoof()
    with open('data.csv', 'a', newline = '') as f:
        data_writer = writer(f)
        data_writer.writerow(data)
        
#create nice header at top of data.csv for autologging
with open('data.csv', 'w', newline = '') as f:
    data_writer = writer(f)
    data_writer.writerow(['Breath Temp', 'Axilla Temp', 'Ambient Temp 1', 'Ambient Temp 2', 'Estimated Core Body Temp'])


#------------FUNCTIONS FOR GUI -------------
#Function to update data labels with live data 
def updateDataLabels(label1, label2, label3, label4):
    label1.config(text = str(temp4_list[-1]))
    label2.config(text = str(temp3_list[-1]))
    label3.config(text = str(temp2_list[-1]))
    label4.config(text = str(temp1_list[-1]))

def openUserManual():
    userManual = tk.Toplevel(gui.master)
    userManual.title("User Manual")
    #w, h = gui.winfo_screenwidth(), userManual.winfo_screenheight()
    #userManual.geometry("%dx%d+0+0" % (w, h)) #auto maximize window
    frame1 = tk.Frame(userManual, relief="sunken")
    
    frame1.grid_rowconfigure(0, weight=1)
    frame1.grid_columnconfigure(0, weight=1)
    
    yscrollbar = tk.Scrollbar(frame1, orient="vertical")
    yscrollbar.grid(row=0, column=1, sticky="ns")
    
    manualTextbox = tk.Text(frame1, yscrollcommand=yscrollbar.set)
    #manualTextbox.grid(row=0, column=0, padx=15, pady=15)
    
    with open("UserManual.txt", "r") as f:
        manualTextbox.insert(tk.INSERT, f.read())

    manualTextbox.config(font=("TkDefaultFont", 20))
    
    manualTextbox.grid(row=0, column=0, pady=15)
    yscrollbar.config(command=manualTextbox.yview)

    frame1.pack()
    
#def openInstructions():


def openAboutUs():
    aboutUs = tk.Toplevel(gui.master)
    aboutUs.title("About Us")
    #w, h = gui.winfo_screenwidth(), userManual.winfo_screenheight()
    #userManual.geometry("%dx%d+0+0" % (w, h)) #auto maximize window
    frame2 = tk.Frame(aboutUs, relief="sunken")
    
    frame2.grid_rowconfigure(0, weight=1)
    frame2.grid_columnconfigure(0, weight=1)
    
    yscrollbar = tk.Scrollbar(frame2, orient="vertical")
    yscrollbar.grid(row=0, column=1, sticky="ns")
    
    aboutUs = tk.Text(frame2, yscrollcommand=yscrollbar.set)
    #manualTextbox.grid(row=0, column=0, padx=15, pady=15)
    
    with open("aboutUs.txt", "r") as f:
        aboutUs.insert(tk.INSERT, f.read())

    aboutUs.config(font=("TkDefaultFont", 20))
    
    aboutUs.grid(row=0, column=0, pady=15)
    yscrollbar.config(command=aboutUs.yview)

    frame2.pack()


#---------------------GUI implementation-------------------

gui = tk.Tk() #init
gui.title("Non-Invasive Core Body Temperature") #title of window
#gui.geometry("1200x600") #size of window
#gui.attributes('-fullscreen', True) #auto fullscreen mode window (taskbar dissapears) 
w, h = gui.winfo_screenwidth(), gui.winfo_screenheight()
gui.geometry("%dx%d+0+0" % (w, h)) #auto maximize window


tab_parent = ttk.Notebook(gui)

#init frames for tabs 1 and 2
tab1 = ttk.Frame(tab_parent)
tab2 = ttk.Frame(tab_parent)
tab3 = ttk.Frame(tab_parent)
tab4 = ttk.Frame(tab_parent)


#add frames to parent with titles - 4 tabs
tab_parent.add(tab1, text="Graph")
tab_parent.add(tab2, text="Data")
tab_parent.add(tab3, text="About")
tab_parent.add(tab4, text="Temp")


# === WIDGETS FOR TAB TWO
data1LabelTabTwo = tk.Label(tab2, text="Core Body Temperature: ", bg="Grey", font=("TkDefaultFont", 30), width = 30, height = 3)
coreBodyTempLabel = tk.Label(tab2, bg="white", relief="sunken", font=("TkDefaultFont", 30), width = 15, height = 3)
data2LabelTabTwo = tk.Label(tab2, text="Ambient Air Temperature: ", bg="Grey", font=("TkDefaultFont", 30), width = 30, height = 3)
ambientTempLabel = tk.Label(tab2, bg="white", relief="sunken", font=("TkDefaultFont", 30), width = 15, height = 3)
data3LabelTabTwo = tk.Label(tab2, text="Mask Temperature: ", bg="Grey", font=("TkDefaultFont", 30), width = 30, height = 3)
maskTempLabel = tk.Label(tab2, bg="white", relief="sunken", font=("TkDefaultFont", 30), width = 15, height = 3)
data4LabelTabTwo = tk.Label(tab2, text="Auxilla Temperature: ", bg="Grey", font=("TkDefaultFont", 30), width = 30, height = 3)
axillaTempLabel = tk.Label(tab2, bg="white", relief="sunken", font=("TkDefaultFont", 30), width = 15, height = 3)
#imgLabelTabOne = tk.Label(tab1)

buttonForward = tk.Button(tab1, text="Forward")
buttonBack = tk.Button(tab1, text="Back")


# === ADD WIDGETS TO GRID ON TAB TWO
data1LabelTabTwo.grid(row=0, column=0, padx=15, pady=15)
coreBodyTempLabel.grid(row=0, column=2, padx=15, pady=15)
data2LabelTabTwo.grid(row=1, column=0, padx=15, pady=15)
ambientTempLabel.grid(row=1, column=2, padx=15, pady=15)
data3LabelTabTwo.grid(row=2, column=0, padx=15, pady=15)
maskTempLabel.grid(row=2, column=2, padx=15, pady=15)
data4LabelTabTwo.grid(row=3, column=0, padx=15, pady=15)
axillaTempLabel.grid(row=3, column=2)

#imgLabelTabOne.grid(row=0, column=2, rowspan=3, padx=15, pady=15)


# === WIDGETS FOR TAB THREE
buttonInstructions = tk.Button(tab3, text="Instructions", font=("TkDefaultFont", 30), width = 10, height = 3)
buttonUsermanual = tk.Button(tab3, text="User Manual", font=("TkDefaultFont", 30), width = 10, height = 3, command=openUserManual)
buttonAboutus = tk.Button(tab3, text="About Us", font=("TkDefaultFont", 30), width = 10, height = 3, command=openAboutUs)
classNameLabel = tk.Label(tab3, text="California State University San Bernardino \n CSE 408 - Spring 2020", font=("TkDefaultFont", 30), width = 45, height = 4, bg="White")
groupNameLabel = tk.Label(tab3, text="Team: The High And Mighty", font=("TkDefaultFont", 30), width = 30, height = 4, bg="White")

logoImage = Image.open("CSUSBLogo.gif")
photoTK = ImageTk.PhotoImage(logoImage, master=tab3)
logoLabel = tk.Label(tab3, image=photoTK)
logoLabel.image = photoTK

# === ADD WIDGETS TO GRID ON TAB THREE
buttonInstructions.grid(row=0, column=0, padx=15, pady=15)
buttonUsermanual.grid(row=1, column=0, padx=15, pady=15)
buttonAboutus.grid(row=2, column=0, padx=15, pady=15)
classNameLabel.grid(row=0, column=2, padx=15, pady=15)
groupNameLabel.grid(row=1, column=2, padx = 15, pady=15)
logoLabel.grid(row=2, column=2, padx = 15, pady=15)

#------------GRAPH------------
# === WIDGETS FOR TAB 1
graphTitleLabel = tk.Label(tab1, text="Live Graph", font=("TkDefaultFont", 20), bg="white", relief="sunken", width =30)
canvas = FigureCanvasTkAgg(fig, master=tab1)

# === ADD WIDGETS TO TAB1
graphTitleLabel.pack()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



tab_parent.pack(expand=1, fill="both")

#Run animation and begin recording data
ani = animation.FuncAnimation(fig, animate, interval=100)

#Tkinter main loop 
gui.mainloop()