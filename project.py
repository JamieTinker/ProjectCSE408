import Adafruit_BMP.BMP085 as BMP085
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from csv import writer
from datetime import datetime

sensori2c = BMP085.BMP085()

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

#interface with ds18b20 sensors
def read_temp_raw(device_file):
    f = open(device_file, "r")
    lines = f.readlines()
    f.close()
    return lines

#interface with ds18b20 sensors
def read_temp(device_file):
    lines = read_temp_raw(device_file)
    while lines[0].strip()[-3:] != "YES":
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0     #Celcius
        #temp_c = temp_c + float(6)              #Offset based on research paper        
        temp_f = (temp_c*9/5)+32                 #Fahrenheit
        
        return temp_f

#get all data from sensors
def get_sense_data():
    sensorids=["28-011877d5dbff","28-01192d696737","28-01192d63b072"]
        #sensor ID List:
        #28-011877d5dbff  = 'Left' gray tape
        #28-01192d696737  = 'Right' gray tape
        #28-01192d63b072  = 'Middle' gray tape
    
    sense_data = []
    
    #get mask sensor temp
    device_file = "/sys/bus/w1/devices/"+ sensorids[0] +"/w1_slave"
    temperature = (read_temp(device_file))
    dtemp = "%.1f" % temperature
    result = (str(dtemp)) + " F "
    masktemp = result
    rawmasktemp = temperature
    
    #get armpit sensor temp
    device_file = "/sys/bus/w1/devices/"+ sensorids[1] +"/w1_slave"
    temperature = (read_temp(device_file))
    dtemp = "%.1f" % temperature
    result = (str(dtemp)) + " F "
    armpittemp = temperature
    
    #get ambient air temp
    device_file = "/sys/bus/w1/devices/"+ sensorids[2] +"/w1_slave"
    temperature = (read_temp(device_file))
    dtemp = "%.1f" % temperature
    result = (str(dtemp)) + " F "
    ambienttemp = temperature
    
    #get data from bpm180
    bpmalt = sensori2c.read_altitude()
    bpmtemp = ((sensori2c.read_temperature() * (9/5))+32)
    bpmtemp = round(bpmtemp, 2)
    
    #estimate core body temp
    estcoretemp = rawmasktemp + 14 #temp calculation
    
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

