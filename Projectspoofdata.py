import time
import random
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
    bmptemp = random.randint(76, 78)
    
    
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
    
    sense_data.append(masktemp)
    sense_data.append(armpittemp)
    sense_data.append(ambienttemp)
    sense_data.append(bpmtemp)
    sense_data.append(estcoretemp)
    sense_data.append(dt)
    
    return sense_data


#animate function for matplotlib to update graph
#animate has its own internal loop. Adding additional
#loops will break the program
def animate(i):
    data = get_sense_data()
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
    data = get_sense_data()
    with open('data.csv', 'a', newline = '') as f:
        data_writer = writer(f)
        data_writer.writerow(data)
        
#create nice header at top of data.csv
with open('data.csv', 'w', newline = '') as f:
    data_writer = writer(f)
    data_writer.writerow(['Breath Temp', 'Axilla Temp', 'Ambient Temp 1', 'Ambient Temp 2', 'Estimated Core Body Temp'])

#run animation
ani = animation.FuncAnimation(fig, animate, interval=100)
plt.show()
S