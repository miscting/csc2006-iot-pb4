#!/usr/bin/env python3


import json
import math
import numpy as np

from bluedot.btcomm import BluetoothServer
from time import sleep
from signal import pause
from flask import Flask, jsonify

from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

# Global variables to store x and y values
final_dict = {}

clients = []
# Location of the 4 Raspberry Pi units in a square matrix
pi1 = (0, 0) # Bottom left
pi2 = (10, 0) # Bottom right
pi3 = (10, 10) # Top right
pi4 = (0, 10) # Top left

izz_dict = {}
jeff_dict = {}
lionel_dict = {}
junwei_dict = {}

def data_received(data):
    typeof = format(data)
    #print("recv - {}".format(data))
    print(typeof)

    global lionel_dict
    global izz_dict
    global jeff_dict
    global junwei_dict
    rasp = str(server.client_address)
    #print("Hello " + rasp)
    if (rasp == "DC:A6:32:BF:22:49"):
        typeof = eval(typeof)
        lionel_dict = typeof
        print("from lionel")
    elif (rasp == "E4:5F:01:02:C2:FF"):
        typeof = eval(typeof)
        izz_dict = typeof
        print("from izzudin")
    elif (rasp == "DC:A6:32:BF:22:61"):
        typeof = eval(typeof)
        jeff_dict = typeof
        print("from jefferson")
    elif (rasp == "E4:5F:01:02:CB:08"):
        typeof = eval(typeof)
        junwei_dict = typeof
        print("from jwjw")

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
            multilaterate(pi1,pi2,pi3,pi4,float(length_jeff), float(length_izz), float(length_junwei),float(length_lionel),scope)

        izz_dict = {}
        jeff_dict = {}
        lionel_dict = {}
        junwei_dict = {}



def client_connected():
    print(server.client_address)

    #print("client connected - {}".format(client["address"]))
    #clients.append(client)

def client_disconnected():
    print(server.client_address)

    #print("client disconnected - {}".format(client["address"]))
    #clients.remove(client)
    
# Calculate the coordinates of the target using Multileration
def multilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4, scopeName):
    global final_dict

    # Distances from the target to each of the Raspberry Pi units
    # d = distanceToIbj * (10 / sizeOfRoom)
    d1 = (d1*100) * (10 / 300) # Bottom lef15
    d2 = (d2*100) * (10 / 300) # Bottom right
    d3 = (d3*100) * (10 / 300) # Top right
    d4 = (d4*100) * (10 / 300) # Top left
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

    if scopeName == "endoscope_junwei":
        final_dict["endo_jw"] = {"x": x_coordinates, "y": y_coordinates}
    elif scopeName == "endoscope_shyam":
        final_dict["endo_shyam"] = {"x": x_coordinates, "y": y_coordinates}
    
    print(x_coordinates)
    print(y_coordinates)

@app.route('/data')
@cross_origin() 
def get_data():
    global final_dict
    return jsonify(final_dict)


    

if __name__ == '__main__':
    print("init")
    server = BluetoothServer(
        data_received,
        auto_start=False,
        when_client_connects=client_connected,
        when_client_disconnects=client_disconnected
    )

    print("starting")
    server.start()
    print(server.server_address)
    print("waiting for connection")
    app.run(host='0.0.0.0', port=8015)

    #try:
    #    pause()
    #except KeyboardInterrupt as e:
    #    print("cancelled by user")
    #finally:
    #    print("stopping")
    #    server.stop()

   #print("stopped")
