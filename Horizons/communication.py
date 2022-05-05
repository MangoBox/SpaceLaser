import serial
import datetime

# COMMUNICATION
teensy = serial.Serial('com1', 115200) # HUGH
data_init = str(df.loc[0][2]) + "," + str(5*60*1000) +"\r" # Start datetime, Incremenet in minutes
teensy.write(data_init.encode())

# WAIT FOR ERROR CHECK
data = str(df.loc[0][0]) + "," + str(df.loc[0][1]) + "\r" # A, h
teensy.write(data.encode())




send_next = datetime.datetime.now() + datetime.timedelta(minutes = 5)

x = True
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
