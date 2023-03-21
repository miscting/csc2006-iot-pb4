from bluedot.btcomm import BluetoothClient
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry
from datetime import datetime
from time import sleep
from signal import pause

def data_received(data):
    print("recv - {}".format(data))
    

def add_scope_to_dict(scope_dict, scope_name, scope_distance):
    # Add the new scope name and distance to the dictionary
    scope_dict[scope_name] = scope_distance

    # Return the updated dictionary
    return scope_dict

# Create an empty dictionary to store scope information
scopes = {}

#Function to calculate distance from RSSI value
def calculate_distance_2dp(rssi):
    return round(calculate_distance(rssi),2)

def calculate_distance(rssi):
    measured_power = -62 # RSSI value at one meter
    N = 2.6 # Path loss exponent for indoor environment
    distance = 10 ** ((measured_power - rssi) / (10 * N))
    return distance

def bluetoothSendData(data):
        c = BluetoothClient("E4:5F:01:02:BF:9E", data_received)
        print("Connected")
        c.send(data)
        print("Sent")
        c.disconnect()
        print("Disconnected")
        sleep(10)
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        #if str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) != "None" and str(dev.addrType).startswith("endoscope"):
        if str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)).startswith("endoscope"):
            distance = calculate_distance(dev.rssi)
            distance_2dp = calculate_distance_2dp(dev.rssi)
            if isNewDev:
                add_scope_to_dict(scopes,str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)),str(distance))
                data = (str(scopes))
                print("Discovered device: " + str(dev.addr) + "(" + str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) + ")" + " (" + str(dev.addrType) + "), RSSI=" + str(dev.rssi) + " dB, Distance=" + str(distance_2dp) + " meters")
                bluetoothSendData(data)
            elif isNewData:
                add_scope_to_dict(scopes,str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)),str(distance))
                print("Received new data from " + str(dev.addr) + "(" + str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) + ")" + " , RSSI= " + str(dev.rssi) + " dB, Distance=" + str(distance_2dp) + " meters")
                data = (str(scopes))
                bluetoothSendData(data)


try:
    while True:
        # Create a scanner object and start scanning for Bluetooth devices
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(5.0)
finally:
    print("done")
