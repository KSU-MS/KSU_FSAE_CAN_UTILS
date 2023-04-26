import cantools

import cantools


# 0xC4 pedal readings
accel_pedal1 = cantools.database.can.Signal("accel_1", 0, 16)
accel_pedal2 = cantools.database.can.Signal("accel_2", 16, 16)
brake1 = cantools.database.can.Signal("brake_1", 32, 16)
brake2 = cantools.database.can.Signal("brake_2", 48, 16)

pedal_readings = cantools.database.can.Message(
    0xC4, "pedals", 8, [accel_pedal1, accel_pedal2, brake1, brake2]
)

db = cantools.database.can.Database(
    [
       pedal_readings
    ]
)

cantools.database.dump_file(db, "ks6e_custom_can.dbc")
db = cantools.database.load_file("ks6e_custom_can.dbc")
print(db)
