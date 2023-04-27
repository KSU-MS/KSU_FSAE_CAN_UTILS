import cantools
import can
from pprint import pprint
import time
import pyformulas as pf
import matplotlib.pyplot as plt
import numpy as np
import time

db = cantools.database.load_file('dbc_files/ks6e_custom_can.dbc')
db2 = cantools.database.load_file('dbc_files/Orion_CANBUS.dbc')
can_bus = can.interface.Bus(bustype='slcan', channel='COM15', bitrate=500000)
fig_1 = plt.figure(1)
fig_2 = plt.figure(2)

screen = pf.screen(title='Plot')
screen2 = pf.screen(title='Plot2')
max = 30
start = time.time()

pedal_accel_list = []
pedal_time_list = []

accum_curr_list = []
accum_time_list = []
while(1):
    try:
        for msg in can_bus:
            t = time.time()
            if(msg.arbitration_id == 196):
                pedal_data = db.decode_message(msg.arbitration_id, msg.data)
                accel1 = pedal_data["accel_1"]    
                brake1 = pedal_data["brake_1"]
                if(len(pedal_accel_list)>max):
                    pedal_accel_list.pop(0)
                if(len(pedal_time_list)>max):
                    pedal_time_list.pop(0)
                pedal_accel_list.append(accel1)
                pedal_time_list.append(t)
                # print(pedal_time_list)
                plt.figure(1)
                plt.xlim(float(pedal_time_list[0]),float(pedal_time_list[len(pedal_time_list)-1]))
                plt.plot(pedal_time_list, pedal_accel_list, c='black')
                fig_1.canvas.draw()
                # If we haven't already shown or saved the plot, then we need to draw the figure first...
                image = np.fromstring(fig_1.canvas.tostring_rgb(),  dtype=np.uint8, sep='')
                image = image.reshape(fig_1.canvas.get_width_height()[::-1] + (3,))
                screen.update(image)
            if(msg.arbitration_id == 1714):
                accum_0x6b2 = db2.decode_message(msg.arbitration_id, msg.data)
                current = accum_0x6b2["Pack_Current"]
                if(len(accum_curr_list)>max):
                    accum_curr_list.pop(0)
                if(len(accum_time_list)>max):
                    accum_time_list.pop(0)
                accum_curr_list.append(current)
                accum_time_list.append(t)
                plt.figure(1)
                plt.xlim(float(accum_time_list[0]),float(accum_time_list[len(accum_time_list)-1]))
                plt.plot(accum_time_list, pedal_accel_list, c='black')
                fig_2.canvas.draw()
                # If we haven't already shown or saved the plot, then we need to draw the figure first...
                image = np.fromstring(fig_2.canvas.tostring_rgb(),  dtype=np.uint8, sep='')
                image = image.reshape(fig_2.canvas.get_width_height()[::-1] + (3,))

                screen2.update(image)
    except:
        print("L")