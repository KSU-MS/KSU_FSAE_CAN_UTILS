import cantools
from pprint import pprint

db = cantools.database.load_file('dbc_files/20200701_RMS_PM_CAN_DB.dbc')
# pprint(db.messages)
example_message = db.get_message_by_name('M192_Command_Message')
# pprint(example_message.signals)
data = example_message.encode({'Torque_Command': -10.0, 'Speed_Command': 0.0, 'Direction_Command': 1, 'Inverter_Enable': 1, 'Inverter_Discharge': 0, 'Speed_Mode_Enable':0, 'Torque_Limit_Command': 0})
print(data)