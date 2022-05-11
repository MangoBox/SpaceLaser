import serial
import time
import pandas as pd
import datetime
from pathlib import Path

file_path = Path(r'C:\Users\chess\OneDrive\Documents\GK_Clone_Place\SpaceLaser\Horizons\temp.csv')
#file_path = Path('/Users/jacobsolsky/Documents/GitHub/SpaceLaser/Horizons/temp.csv')
df = pd.read_csv(file_path)

# COMMUNICATION
def start_teensy(com_port):
    teensy = serial.Serial(com_port, 9600) # com_port is a string specifying the com port (e.g. "COM4")
    teensy.timeout = 1
    return teensy

def close_teensy(teensy):
    teensy.close()

def new_obs(teensy, temp_filepath):
    file_path = Path(temp_filepath) #Temp is where the values from the calulation or API call are stored
    df = pd.read_csv(file_path)

    while True:
        data_init = "a" + str(5*60*1000) + "," + str(df.loc[0][0]) + "," + str(df.loc[0][1]) + "," + str(df.loc[0][2]) + "\r" # Interval, Azimuth, height, datetime (first datapoint)
        time.sleep(0.5)

        print(teensy.readline().decode('ascii'))

        for i in range(len(df)):
            send_next = datetime.datetime.now() + datetime.timedelta(minutes = 5)
            df2 = df.iloc[i]

            while True:
                if exit == True:
                    break

                if send_next < datetime.datetime.now():
                    data = "b\r" + str(df2.loc[0][0]) + "," + str(df2.loc[0][1]) + "," + str(df.loc[0][2]) +  "\r"
                    teensy.write(data.encode())
                    
                time.sleep(0.5)
                if(teensy.readline().decode('ascii') != ""):
                    print(teensy.readline().decode('ascii'))
            
            if exit == True:
                break
 
        data = "c\r"
        teensy.write(data_init.encode())
        time.sleep(0.5)
        
        break

        # a = initialisation
        # b = send next data points
        # c = exit 

com_port = "COM4" #CHANGE THIS

teensy = start_teensy(com_port)
new_obs(teensy, file_path)
close_teensy(teensy)