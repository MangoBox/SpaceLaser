import serial
import time
import pandas as pd
from pathlib import Path

file_path = Path(r'C:\Users\chess\OneDrive\Documents\GK_Clone_Place\SpaceLaser\Horizons\temp.csv')
df = pd.read_csv(file_path)
print(df)

# COMMUNICATION
teensy = serial.Serial('COM4', 9600) # HUGH
teensy.timeout = 1

while True:
    #data_init = str(df.loc[0][2]) + "," + str(5*60*1000) +"\r" # Start datetime, Incremenet in minutes
    #teensy.write(data_init.encode())
    data = str(df.loc[0][0]) + "," + str(df.loc[0][1]) + "\r" # A, h
    teensy.write(data.encode())
    time.sleep(0.5)
    print(teensy.readline().decode('ascii'))
    time.sleep(0.5)
    print(teensy.readline().decode('ascii'))
    break

teensy.close()


# send_next = datetime.datetime.now() + datetime.timedelta(minutes = 5)


"""x = True
while x == True:
    if send_next < datetime.datetime.now():
        dtLCL = datetime.datetime.now() + last_index * datetime.timedelta(minutes = 5)
        A, h = findCoords(planet_selected, earth, dtLCL, tzdiff, latitude, longlitude)
        df2 = pd.DataFrame({
            "A": [A],
            "H": [h],
            "time": [dtLCL.time()]
        },
        index = [last_index + 1])
        df = pd.concat([df, df2])
        last_index = last_index + 1
        print(df2)
        send_next = datetime.datetime.now() + datetime.timedelta(minutes = 5)

        df2.to_csv(filepath_results, mode='a', index=True, header=False)
        x = False
"""