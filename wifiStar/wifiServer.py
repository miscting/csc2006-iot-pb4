#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import time
import json
import math
import numpy as np

import paho.mqtt.client as paho
from paho import mqtt
from flask import Flask, jsonify

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Global variables to store x and y values
final_x = None
final_y = None

# Location of the 4 Raspberry Pi units in a square matrix
pi1 = (0, 0) # Bottom left
pi2 = (10, 0) # Bottom right
pi3 = (10, 10) # Top right
pi4 = (0, 10) # Top left

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


izz_dict = {}
jeff_dict = {}
lionel_dict = {}
junwei_dict = {}

# print message, useful for checking if it was successful
def on_message(client, userdata, msg):    
    # Decode the bytes object to a string
    payload_str = (msg.payload).decode()
    
    # Parse the string as a JSON object to get a dictionary
    payload_dict = json.loads(payload_str)
    #print(str(msg.topic) + "  ")
    print(str(msg.topic))
    
    global lionel_dict
    global izz_dict
    global jeff_dict
    global junwei_dict
    
    if(str(msg.topic) == "lionelPi/"):
        lionel_dict = payload_dict
    elif(str(msg.topic) == "izzPi/"):
        izz_dict = payload_dict
    elif(str(msg.topic) == "jeffPi/"):
        jeff_dict = payload_dict
    elif(str(msg.topic) == "junweiPi/"):
        junwei_dict = payload_dict
        
    if(len(lionel_dict) > 0 and len(izz_dict) > 0 and len(jeff_dict) > 0 and len(junwei_dict) > 0):
        keys1 = set(lionel_dict.keys())
        keys2 = set(izz_dict.keys())
        keys3 = set(jeff_dict.keys())
        keys4 = set(junwei_dict.keys())
        common_keys = keys1.intersection(keys2)
        common_keys2 = common_keys.intersection(keys3)
        common_keys3 = common_keys2.intersection(keys4)
        common_dict = {key: lionel_dict[key] for key in common_keys3}
        #print(common_dict)
        for scope in common_dict:
            length_izz = izz_dict.get(scope)
            length_lionel = lionel_dict.get(scope)
            length_jeff = jeff_dict.get(scope)
            length_junwei = junwei_dict.get(scope)
            #print(length_junwei)
            multilaterate(pi1,pi2,pi3,pi4,float(length_jeff), float(length_izz), float(length_junwei),float(length_lionel))

        izz_dict = {}
        jeff_dict = {}
        lionel_dict = {}
        junwei_dict = {}
        
# Calculate the coordinates of the target using Multileration
def multilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4):
    global final_x
    global final_y

    # Distances from the target to each of the Raspberry Pi units
    # d = distanceToIbj * (10 / sizeOfRoom)
    d1 = (d1*100) * (10 / 130) # Bottom lef15
    d2 = (d2*100) * (10 / 130) # Bottom right
    d3 = (d3*100) * (10 / 130) # Top right
    d4 = (d4*100) * (10 / 130) # Top left
    #print(d2)
   #print(d1)
    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi2 and pi1 multiplied by 2
    A = 2 * (pi2[0] - pi1[0])
    # Difference in y-coordinate of pi2 and pi1 multiplied by 2
    B = 2 * (pi2[1] - pi1[1])
    # Difference in distance from M5 to pi2 and pi1 + square of distance between p2
    C = d1**2 - d2**2 - pi1[0]**2 + pi2[0]**2 - pi1[1]**2 + pi2[1]**2

    # System of linear algebra values for pi2, pi3 and M5
    # Difference in x-coordinate of pi3 and pi1 multiplied by 2
    D = 2 * (pi3[0] - pi2[0])
    # Difference in y-coordinate of pi3 and pi1 multiplied by 2
    E = 2 * (pi3[1] - pi2[1])
    # Difference in distance from M5 to pi3 and pi2 + square of distance between p2
    F = d2**2 - d3**2 - pi2[0]**2 + pi3[0]**2 - pi2[1]**2 + pi3[1]**2

    # System of linear algebra values for pi3, pi4 and M5
    # Difference in x-coordinate of pi4 and pi3 multiplied by 2
    G = 2 * (pi4[0] - pi3[0])
    # Difference in y-coordinate of pi4 and pi3 multiplied by 2
    H = 2 * (pi4[1] - pi3[1])
    # Difference in distance from M5 to pi4 and pi3 + square of distance between p2
    I = d3**2 - d4**2 - pi3[0]**2 + pi4[0]**2 - pi3[1]**2 + pi4[1]**2
    
    # System of linear algebra values for pi4, pi1 and M5
    # Difference in x-coordinate of pi1 and pi4 multiplied by 2
    J = 2 * (pi1[0] - pi4[0])
    # Difference in y-coordinate of pi1 and pi4 multiplied by 2
    K = 2 * (pi1[1] - pi4[1])
    # Difference in distance from M5 to pi1 and pi4 + square of distance between p2
    L = d4**2 - d1**2 - pi4[0]**2 + pi1[0]**2 - pi4[1]**2 + pi1[1]**2
    
    # Add an array for each set of system of linear algebra to known points array (4 sets)
    #knownPoints = np.array([[A, B], [D, E], [G, H], [J, K]]) # m x n matrix
    
    knownPoints = np.array([[A, B], [D, E], [G, H]]) # m x n matrix
    unknownPoints = np.array([C, F, I ]) # A vector
    # Add an array for each set of system of linear algebra to unknown points array (4 sets)
    #unknownPoints = np.array([C, F, I, L]) # A vector
    # Return the least-squares solution to a linear matrix equation
    # minimizes the sum of the squares of the differences between the entries KnownPoints * coordinates = UnknownPoints
    coordinates = np.linalg.lstsq(knownPoints, unknownPoints, rcond=None)[0]

    # Round the coordinates to the nearest integer
    x_coordinates = round(coordinates[0])
    y_coordinates = round(coordinates[1])

    final_x = x_coordinates
    final_y = y_coordinates
    print(final_x)
    print(final_y)


@app.route('/data')
@cross_origin() 
def get_data():
    global final_x, final_y
    return jsonify({'x': str(final_x), 'y': str(final_y)})

if __name__ == '__main__':
    # using MQTT version 5 here, for 3.1.1: MQTTv311, 3.1: MQTTv31
    # userdata is user defined data of any type, updated by user_data_set()
    # client_id is the given name of the client
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    # enable TLS for secure connection
    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    # set username and password
    client.username_pw_set("rpiShyamSub", "12345678")
    # connect to HiveMQ Cloud on port 8883 (default for MQTT)
    client.connect("723f23336fd14a93a47aecf629284fb1.s2.eu.hivemq.cloud", 8883)

    # setting callbacks, use separate functions like above for better visibility
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    #client.on_publish = on_publish

    # subscribe to all topics of encyclopedia by using the wildcard "#"
    client.subscribe("izzPi/#", qos=1)
    client.subscribe("lionelPi/#", qos=1)
    client.subscribe("junweiPi/#", qos=1)
    client.subscribe("jeffPi/#", qos=1)

    # a single publish, this can also be done in loops, etc.
    #client.publish("encyclopedia/temperature", payload="hot", qos=1)

    # loop_forever for simplicity, here you need to stop the loop manually
    # you can also use loop_start and loop_stop
    client.loop_start()

    app.run(host='0.0.0.0', port=8015)


