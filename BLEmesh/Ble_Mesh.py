import json
import math
import numpy as np

from time import sleep
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flask import request

app = Flask(__name__)
CORS(app)

# Global variables to store x and y values
final_dict = {}


# Location of the 4 Raspberry Pi units in a square matrix
pi1 = (0, 0) # Bottom left
pi2 = (10, 0) # Bottom right
pi3 = (10, 10) # Top right
pi4 = (0, 10) # Top left

shyam_dict = {}
junwei_dict = {}
    
# Calculate the coordinates of the target using Multileration
def multilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4, scopeName):
    global final_dict
    
    # Distances from the target to each of the Raspberry Pi units
    # d = distanceToIbj * (10 / sizeOfRoom)
    d1 = (d1*100) * (10 / 280) # Bottom lef15 (Jeff)
    d2 = (d2*100) * (10 / 280) # Bottom right (Izz)
    d3 = (d3*100) * (10 / 280) # Top right (Junwei)
    d4 = (d4*100) * (10 / 280) # Top left (lionel)

    # d1 = 18.87 * (10 / 20)
    # d2 = 18.87 * (10 / 20)
    # d3 = 10.77 * (10 / 20)
    # d4 = 10.77 * (10 / 20)

    #print(d2)
    #print(d1)
    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi2 and pi1 multiplied by 2
    A = 2.0 * (pi2[0] - pi1[0])
    # Difference in y-coordinate of pi2 and pi1 multiplied by 2
    B = 2.0 * (pi2[1] - pi1[1])
    # Difference in distance from M5 to pi2 and pi1 + square of distance between p2
    C = d1**2.0 - d2**2.0 - pi1[0]**2.0 + pi2[0]**2.0 - pi1[1]**2.0 + pi2[1]**2.0

    # System of linear algebra values for pi2, pi3 and M5
    # Difference in x-coordinate of pi3 and pi1 multiplied by 2
    D = 2.0 * (pi3[0] - pi2[0])
    # Difference in y-coordinate of pi3 and pi1 multiplied by 2
    E = 2.0 * (pi3[1] - pi2[1])
    # Difference in distance from M5 to pi3 and pi2 + square of distance between p2
    F = d2**2.0 - d3**2.0 - pi2[0]**2.0 + pi3[0]**2.0 - pi2[1]**2.0 + pi3[1]**2.0

    # System of linear algebra values for pi3, pi4 and M5
    # Difference in x-coordinate of pi4 and pi3 multiplied by 2
    G = 2.0 * (pi4[0] - pi3[0])
    # Difference in y-coordinate of pi4 and pi3 multiplied by 2
    H = 2.0 * (pi4[1] - pi3[1])
    # Difference in distance from M5 to pi4 and pi3 + square of distance between p2
    I = d3**2.0 - d4**2.0 - pi3[0]**2.0 + pi4[0]**2.0 - pi3[1]**2.0 + pi4[1]**2.0
    
    # System of linear algebra values for pi4, pi1 and M5
    # Difference in x-coordinate of pi1 and pi4 multiplied by 2
    J = 2.0 * (pi1[0] - pi4[0])
    # Difference in y-coordinate of pi1 and pi4 multiplied by 2
    K = 2.0 * (pi1[1] - pi4[1])
    # Difference in distance from M5 to pi1 and pi4 + square of distance between p2
    L = d4**2.0 - d1**2.0 - pi4[0]**2.0 + pi1[0]**2.0 - pi4[1]**2.0 + pi1[1]**2.0
    
    # Add an array for each set of system of linear algebra to known points array (4 sets)
    #knownPoints = np.array([[A, B], [D, E], [G, H], [J, K]]) # m x n matrix
    
    knownPoints = np.array([[A, B], [D, E], [G, H], [J ,K]]) # m x n matrix
    unknownPoints = np.array([C, F, I, L]) # A vector
    # Add an array for each set of system of linear algebra to unknown points array (4 sets)
    #unknownPoints = np.array([C, F, I, L]) # A vector
    # Return the least-squares solution to a linear matrix equation
    # minimizes the sum of the squares of the differences between the entries KnownPoints * coordinates = UnknownPoints
    coordinates = np.linalg.lstsq(knownPoints, unknownPoints, rcond=None)[0]

    # Round the coordinates to the nearest integer
    x_coordinates = round(coordinates[0])
    y_coordinates = round(coordinates[1])

    if scopeName == "endo_jw":
        final_dict[scopeName] = {"x": x_coordinates, "y": y_coordinates}
    elif scopeName == "endo_shyam":
        final_dict[scopeName] = {"x": x_coordinates, "y": y_coordinates}
        
    print(x_coordinates)
    print(y_coordinates)

# Function to calculate distance from RSSI value
def calculate_distance_2dp(rssi):
    return round(calculate_distance(rssi),2)

def calculate_distance(rssi):
    measured_power = -62 # RSSI value at one meter
    N = 2.4 # Path loss exponent for indoor environment
    distance = 10 ** ((measured_power - rssi) / (10 * N))
    return distance

@app.route('/data')
@cross_origin() 
def get_data():
    global final_dict
    return jsonify(final_dict)

@app.route('/updateValues', methods = ['POST'])
@cross_origin()
def updateValues():
    global shyam_dict, junwei_dict
    data = list(request.form.to_dict().keys())[0]
    piName = data.split(',')[0]
    scopeName = data.split(',')[1].split(':')[0]
    rssi = data.split(',')[1].split(':')[1]

    if scopeName == "endo_jw":
        junwei_dict[piName] = rssi
        
        if len(junwei_dict) == 4:
            jeffPi = None
            izzPi = None
            jwPi = None
            lionelPi = None
            
            for pi in junwei_dict:
                if pi == "Jeff_Pi":
                    jeffPi = junwei_dict.get(pi)
                elif pi == "Izz_Pi":
                    izzPi = junwei_dict.get(pi)
                elif pi == "JunweiPi":
                    jwPi = junwei_dict.get(pi)
                elif pi == "LionelPi":
                    lionelPi = junwei_dict.get(pi)
                    
            d1 = calculate_distance_2dp(float(jeffPi))
            d2 = calculate_distance_2dp(float(izzPi))
            d3 = calculate_distance_2dp(float(jwPi))
            d4 = calculate_distance_2dp(float(lionelPi))
            
            multilaterate(pi1,pi2,pi3,pi4,d1,d2,d3,d4,scopeName)
            print(junwei_dict)
            junwei_dict = {}
    elif scopeName == "endo_shyam":
        shyam_dict[piName] = rssi

        if len(shyam_dict) == 4:
            jeffPi = None
            izzPi = None
            jwPi = None
            lionelPi = None
            
            for pi in shyam_dict:
                if pi == "Jeff_Pi":
                    jeffPi = shyam_dict.get(pi)
                elif pi == "Izz_Pi":
                    izzPi = shyam_dict.get(pi)
                elif pi == "JunweiPi":
                    jwPi = shyam_dict.get(pi)
                elif pi == "LionelPi":
                    lionelPi = shyam_dict.get(pi)
                    
            d1 = calculate_distance_2dp(float(jeffPi))
            d2 = calculate_distance_2dp(float(izzPi))
            d3 = calculate_distance_2dp(float(jwPi))
            d4 = calculate_distance_2dp(float(lionelPi))
            
            multilaterate(pi1,pi2,pi3,pi4,d1,d2,d3,d4,scopeName)
            print(shyam_dict)
            shyam_dict = {}

    return ""
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8015, debug=True)