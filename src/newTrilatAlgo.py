import math
import numpy as np
# Location of the 4 Raspberry Pi units in a square matrix
pi1 = (0, 0)
pi2 = (10, 0)
pi3 = (10, 10)
pi4 = (0, 10)

# Distances from the target to each of the Raspberry Pi units
# d = distanceToIbj * (10 / sizeOfRoom)
d1 = 18.87 * (10 / 20) # Bottom left
d2 = 18.87 * (10 / 20) # Bottom right
d3 = 10.77 * (10 / 20) # Top right
d4 = 10.77 * (10 / 20) # Top left

def trilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4):
    # Calculate the coordinates of the target using trilateration
    A = 2 * (pi2[0] - pi1[0])
    B = 2 * (pi2[1] - pi1[1])
    C = d1**2 - d2**2 - pi1[0]**2 + pi2[0]**2 - pi1[1]**2 + pi2[1]**2
    D = 2 * (pi3[0] - pi2[0])
    E = 2 * (pi3[1] - pi2[1])
    F = d2**2 - d3**2 - pi2[0]**2 + pi3[0]**2 - pi2[1]**2 + pi3[1]**2
    G = 2 * (pi4[0] - pi3[0])
    H = 2 * (pi4[1] - pi3[1])
    I = d3**2 - d4**2 - pi3[0]**2 + pi4[0]**2 - pi3[1]**2 + pi4[1]**2
    # Add an extra row to a for the fourth Pi unit
    a = np.array([[A, B], [D, E], [G, H]])
    b = np.array([C, F, I])
    # print('a:', a.shape)
    # print('b:', b.shape)
    x = np.linalg.lstsq(a, b, rcond=None)[0]
    # print('x:', x.shape)

    # Round the coordinates to the nearest integer
    x_coord = round(x[0])
    y_coord = round(x[1])

    return x_coord, y_coord


x, y = trilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4)
print(f"The Endoscope is located at ({x}, {y}) in the room.")