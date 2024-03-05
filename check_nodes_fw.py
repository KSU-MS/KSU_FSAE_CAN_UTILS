import cantools
import can
import json
import importlib  
from decode_can import decode_can_message

def load_wanted_signals_from_json(inputjson = "scrape_targets.json",db = cantools.db.Database):
    with open(inputjson) as file:
        json_input = json.load(file)
    msg_list= []
    signal_dict = {}
    for message in json_input:
        print(message)
        print(json_input[message])
        if json_input[message][0] == "all":
            msg  = (db.get_message_by_name(message))
            print(msg)
            print(msg.signals)
            for signal in msg.signals:
                signal_dict[signal.name]="SNA"
        else:
            for signal_name in json_input[message]:
                signal_dict[signal_name]="SNA"
    print(json.dumps(signal_dict,indent=3))
    return signal_dict

def open_pcan_bus():
    try:
        bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000)
    except:
        print("pcan failed to open")
        exit(1)
    return bus

def main():
    # Load the DBC file
    db = cantools.db.load_file("KS5e-Data-Logging\dbc-files\ksu_ev_can.dbc")
    signal_dict = load_wanted_signals_from_json(db=db)
    # Initialize the CAN interface
    bus = open_pcan_bus()
    # Main loop to receive and decode CAN messages
    while True:
        try:
            # Receive a CAN message with a timeout of 1 second
            msg = bus.recv(timeout=1.0)
            if msg is not None:
                try:
                    # print(decode_can_message(msg, db))
                    decoded_msg = decode_can_message(msg,db)
                    for signal in decoded_msg:
                        if signal in signal_dict.keys():
                            signal_dict[signal]=decoded_msg[signal]
                    json.dumps(signal_dict,indent=3)
                    
                except:
                    pass
        except KeyboardInterrupt:
            break

    # Cleanup
    bus.shutdown()

if __name__ == "__main__":
    main()