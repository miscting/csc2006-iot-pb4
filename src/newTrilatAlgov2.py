import math
import numpy as np

# https://math.libretexts.org/Bookshelves/Linear_Algebra/Interactive_Linear_Algebra_(Margalit_and_Rabinoff)/06%3A_Orthogonality/6.5%3A_The_Method_of_Least_Squares

# pi4 _______ pi3        \  /
#    |\  |  /|         d4 \/ d3
#    |   5   |            M5 
#    |/__|__\|        d1 /  \ d2
# pi1         pi2       /    \

# Location of the 4 Raspberry Pi units in a square matrix
pi1 = (0, 0) # Bottom left
pi2 = (10, 0) # Bottom right
pi3 = (10, 10) # Top right
pi4 = (0, 10) # Top left

# Distances from the target to each of the Raspberry Pi units
# d = distanceToIbj * (10 / sizeOfRoom)
d1 = 18.87 * (10 / 20) # Bottom left
d2 = 18.87 * (10 / 20) # Bottom right
d3 = 10.77 * (10 / 20) # Top right
d4 = 10.77 * (10 / 20) # Top left

# Calculate the coordinates of the target using Multileration
def multilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4):
    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi2 and pi1 multiplied by 2
    A = 2 * (pi2[0] - pi1[0])
    # Difference in y-coordinate of pi2 and pi1 multiplied by 2
    B = 2 * (pi2[1] - pi1[1])
    # Difference in distance from M5 to pi2 and pi1 + square of distance between p2
    C = d1**2 - d2**2 - pi1[0]**2 + pi2[0]**2 - pi1[1]**2 + pi2[1]**2

    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi3 and pi1 multiplied by 2
    D = 2 * (pi3[0] - pi2[0])
    # Difference in y-coordinate of pi3 and pi1 multiplied by 2
    E = 2 * (pi3[1] - pi2[1])
    # Difference in distance from M5 to pi3 and pi2 + square of distance between p2
    F = d2**2 - d3**2 - pi2[0]**2 + pi3[0]**2 - pi2[1]**2 + pi3[1]**2

    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi4 and pi3 multiplied by 2
    G = 2 * (pi4[0] - pi3[0])
    # Difference in y-coordinate of pi4 and pi3 multiplied by 2
    H = 2 * (pi4[1] - pi3[1])
    # Difference in distance from M5 to pi4 and pi3 + square of distance between p2
    I = d3**2 - d4**2 - pi3[0]**2 + pi4[0]**2 - pi3[1]**2 + pi4[1]**2
    
    # System of linear algebra values for pi1, pi2 and M5
    # Difference in x-coordinate of pi1 and pi4 multiplied by 2
    J = 2 * (pi1[0] - pi4[0])
    # Difference in y-coordinate of pi1 and pi4 multiplied by 2
    K = 2 * (pi1[1] - pi4[1])
    # Difference in distance from M5 to pi1 and pi4 + square of distance between p2
    L = d4**2 - d1**2 - pi4[0]**2 + pi1[0]**2 - pi4[1]**2 + pi1[1]**2
    
    # Add an array for each set of system of linear algebra to known points array (4 sets)
    knownPoints = np.array([[A, B], [D, E], [G, H], [J, K]]) # m x n matrix
    # Add an array for each set of system of linear algebra to unknown points array (4 sets)
    unknownPoints = np.array([C, F, I, L]) # A vector
    # Return the least-squares solution to a linear matrix equation
    # minimizes the sum of the squares of the differences between the entries KnownPoints * coordinates = UnknownPoints
    coordinates = np.linalg.lstsq(knownPoints, unknownPoints, rcond=None)[0]

    # Round the coordinates to the nearest integer
    x_coordinates = round(coordinates[0])
    y_coordinates = round(coordinates[1])

    return x_coordinates, y_coordinates


x, y = multilaterate(pi1, pi2, pi3, pi4, d1, d2, d3, d4)
print(f"The Endoscope is located at ({x}, {y}) in the room.")