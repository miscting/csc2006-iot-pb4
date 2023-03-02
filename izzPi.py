from bluepy.btle import Scanner, DefaultDelegate, ScanEntry
import time
import json

import paho.mqtt.client as paho
from paho import mqtt

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
    """
        Prints the result of the connection with a reasoncode to stdout ( used as callback for connect )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param flags: these are response flags sent by the broker
        :param rc: stands for reasonCode, which is a code for the connection result
        :param properties: can be used in MQTTv5, but is optional
    """
    print("CONNACK received with code %s." % rc)


# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    """
        Prints mid to stdout to reassure a successful publish ( used as callback for publish )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param properties: can be used in MQTTv5, but is optional
    """
    print("mid: " + str(mid))


# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    """
        Prints a reassurance for successfully subscribing

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param mid: variable returned from the corresponding publish() call, to allow outgoing messages to be tracked
        :param granted_qos: this is the qos that you declare when subscribing, use the same one for publishing
        :param properties: can be used in MQTTv5, but is optional
    """
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


# print message, useful for checking if it was successful
def on_message(client, userdata, msg):
    """
        Prints a mqtt message to stdout ( used as callback for subscribe )

        :param client: the client itself
        :param userdata: userdata is set when initiating the client, here it is userdata=None
        :param msg: the message with topic and payload
    """
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


# using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
# userdata is user defined data of any type, updated by user_data_set()
# client_id is the given name of the client
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set("rpiLionelPub", "12345678")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect("723f23336fd14a93a47aecf629284fb1.s2.eu.hivemq.cloud", 8883)

# setting callbacks, use separate functions like above for better visibility
#client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# subscribe to all topics of encyclopedia by using the wildcard "#"
#client.subscribe("encyclopedia/#", qos=1)

# client.loop_start()
# # a single publish, this can also be done in loops, etc.
# while True:
#     print("Test")
#     client.publish("izzPi/", payload= "Hi", qos=1)

# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#client.loop_forever()


def add_scope_to_dict(scope_dict, scope_name, scope_distance):
    # Add the new scope name and distance to the dictionary
    scope_dict[scope_name] = scope_distance

    # Return the updated dictionary
    return scope_dict

# Create an empty dictionary to store scope information
scopes = {}

# Function to calculate distance from RSSI value
def calculate_distance_2dp(rssi):
    return round(calculate_distance(rssi),2)

def calculate_distance(rssi):
    measured_power = -62 # RSSI value at one meter
    N = 2.4 # Path loss exponent for indoor environment
    distance = 10 ** ((measured_power - rssi) / (10 * N))
    return distance

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
                print("Discovered device: " + str(dev.addr) + "(" + str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) + ")" + " (" + str(dev.addrType) + "), RSSI=" + str(dev.rssi) + " dB, Distance=" + str(distance_2dp) + " meters")
            elif isNewData:
                add_scope_to_dict(scopes,str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)),str(distance))
                print("Received new data from " + str(dev.addr) + "(" + str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) + ")" + " , RSSI= " + str(dev.rssi) + " dB, Distance=" + str(distance_2dp) + " meters")
            client.loop_start()
            client.publish("izzPi/", payload= json.dumps(scopes), qos=2)
            time.sleep(5)
       
while True:
    # Create a scanner object and start scanning for Bluetooth devices
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(5.0)

# Loop through the discovered devices and print their RSSI values
for dev in devices:
    if dev.addr is not None and str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) != "None" and str(dev.addrType).startswith("endoscope"): 
        distance = calculate_distance(dev.rssi)
        print("Discovered device: " + str(dev.addr) + " (" + str(dev.getValueText(ScanEntry.COMPLETE_LOCAL_NAME)) + ")" + " (" + str(dev.addrType) + "), RSSI=" + str(dev.rssi) + " dB, Distance=" + str(distance_2dp) + " meters")
    





