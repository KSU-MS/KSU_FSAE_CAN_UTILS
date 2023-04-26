import cantools
import can
from pprint import pprint
import time
import pyformulas as pf
import matplotlib.pyplot as plt
import numpy as np
import time



db = cantools.database.load_file('dbc_files/ks6e_custom_can.dbc')
can_bus = can.interface.Bus(bustype='slcan', channel='/dev/ttyUSB2', bitrate=500000)
fig = plt.figure()

screen = pf.screen(title='Plot')
max = 30
start = time.time()
accel_list = []
time_list = []
while(1):
    try:
        for msg in can_bus:
            if(msg.arbitration_id == 196):
                t = time.time() - start
                asdf = db.decode_message(msg.arbitration_id, msg.data)
                accel1 = asdf["accel_1"]    
                brake1 = asdf["brake_1"]
                if(len(accel_list)>max):
                    accel_list.pop(0)
                if(len(time_list)>max):
                    time_list.pop(0)
                accel_list.append(accel1)
                time_list.append(t)
                # print(time_list)
                plt.xlim(float(time_list[0]),float(time_list[len(time_list)-1]))
                plt.plot(time_list, accel_list, c='black')
                fig.canvas.draw()
                # If we haven't already shown or saved the plot, then we need to draw the figure first...
                image = np.fromstring(fig.canvas.tostring_rgb(),  dtype=np.uint8, sep='')
                image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

                screen.update(image)
    except:
        print("L")