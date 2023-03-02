
#  A _______ B
#   |\  |  /|
#   |   5   |
#   |/__|__\|
#  D         C

# Length from pi to pi
lengthAB = 40
lengthBC = 40
lengthCD = 40
lengthDA = 40

# Diagonal Length from pi to pi
lengthAC = 56.56
lengthBD = 56.56

# Length from pi to m5
lengthA5 = 28.28
lengthB5 = 28.28
lengthC5 = 28.28
lengthD5 = 28.28

############################################################
# First Triangle
# Calculate cosines of angles Alpha (ADC), Beta (CAB) & Zeta (ABD)
# cosAlpha = (lengthD5**2 + lengthDA**2 - lengthA5**2) / (2 * lengthD5 * lengthDA)
# cosBeta = (lengthA5**2 + lengthAB**2 - lengthD5**2) / (2 * lengthA5 * lengthAB)
# cosZeta = (lengthB5**2 + lengthBD**2 - lengthD5**2) / (2 * lengthB5 * lengthBD)

cosAlpha = (lengthD5**2 - lengthDA**2 - lengthA5**2) / -(2 * lengthD5 * lengthDA)
cosBeta = (lengthA5**2 - lengthAB**2 - lengthD5**2) / -(2 * lengthA5 * lengthAB)
cosZeta = (lengthB5**2 - lengthBD**2 - lengthD5**2) / -(2 * lengthB5 * lengthBD)

# print(cosAlpha)
# print(cosBeta)
# print(cosZeta)

# Calculate cosine squares of angles Alpha, Beta & Zeta
# cos2Alpha = (lengthD5**2 + lengthDA**2 - lengthA5**2)**2 / (2 * lengthD5 * lengthDA)**2
# cos2Beta = (lengthA5**2 + lengthAB**2 - lengthD5**2)**2 / (2 * lengthA5 * lengthAB)**2
# cos2Zeta = (lengthB5**2 + lengthBD**2 - lengthD5**2)**2 / (2 * lengthB5 * lengthBD)**2

cos2Alpha = cosAlpha**2
cos2Beta = cosBeta**2
cos2Zeta = cosZeta**2

# Calculate sine of angles Alpha, Beta & Zeta from cos squares
sinAlpha = (1 - cos2Alpha)**0.5
sinBeta = (1 - cos2Beta)**0.5
sinZeta = (1 - cos2Zeta)**0.5

# Calculate x & y coordinates of M5 stick
calcx = ((lengthDA * cosZeta) + (lengthAB * cosAlpha) + (lengthBD * cosBeta)) / 3
calcy = ((lengthDA * sinZeta) + (lengthAB * sinAlpha) + (lengthBD * sinBeta)) / 3

x1 = (calcx / lengthAB) * 10
y1 = (calcy / lengthDA) * 10



#  A _______ B
#   |\  |  /|
#   |   5   |
#   |/__|__\|
#  D         C

############################################################
# Second Triangle
# Calculate cosines of angles Alpha (ADC), Beta (CAB) & Zeta (ABD)
# cosAlpha = (lengthA5**2 + lengthAB**2 - lengthB5**2) / (2 * lengthA5 * lengthAB)
# cosBeta = (lengthB5**2 + lengthBC**2 - lengthA5**2) / (2 * lengthB5 * lengthBC)
# cosZeta = (lengthC5**2 + lengthAC**2 - lengthA5**2) / (2 * lengthC5 * lengthAC)

cosAlpha = (lengthB5**2 - lengthAB**2 - lengthA5**2) / (-2 * (lengthAB * lengthA5))
cosBeta = (lengthC5**2 - lengthBC**2 - lengthB5**2) / (-2 * (lengthBC * lengthB5))
cosZeta = (lengthB5**2 - lengthC5**2 - lengthBC**2) / (-2 *(lengthC5 * lengthBC))


# Calculate cosine squares of angles Alpha, Beta & Zeta
# cos2Alpha = (lengthA5**2 + lengthAB**2 - lengthB5**2)**2 / (2 * lengthA5 * lengthAB)**2
# cos2Beta = (lengthB5**2 + lengthBC**2 - lengthA5**2)**2 / (2 * lengthB5 * lengthBC)**2
# cos2Zeta = (lengthC5**2 + lengthAC**2 - lengthA5**2)**2 / (2 * lengthC5 * lengthAC)**2

cos2Alpha = cosAlpha**2
cos2Beta = cosBeta**2
cos2Zeta = cosZeta**2

# Calculate sine of angles Alpha, Beta & Zeta from cos squares
sinAlpha = (1 - cos2Alpha)**0.5
sinBeta = (1 - cos2Beta)**0.5
sinZeta = (1 - cos2Zeta)**0.5

# Calculate x & y coordinates of M5 stick
calcx = ((lengthAB * cosZeta) + (lengthBC * cosAlpha) + (lengthAC * cosBeta)) / 4.8
calcy = ((lengthAB * sinZeta) + (lengthBC * sinAlpha) + (lengthAC * sinBeta)) / 4.8

x2 = (calcx / lengthAB) * 10
y2 = (calcy / lengthDA) * 10


print(calcx)
print(calcy)


print(round(x2))
print(round(y2))

############################################################
# Third Triangle
# Calculate cosines of angles Alpha (ADC), Beta (CAB) & Zeta (ABD)
cosAlpha = (lengthB5**2 + lengthBC**2 - lengthC5**2) / (2 * lengthB5 * lengthBC)
cosBeta = (lengthC5**2 + lengthCD**2 - lengthB5**2) / (2 * lengthC5 * lengthCD)
cosZeta = (lengthD5**2 + lengthBD**2 - lengthB5**2) / (2 * lengthD5 * lengthBD)

# Calculate cosine squares of angles Alpha, Beta & Zeta
cos2Alpha = (lengthB5**2 + lengthBC**2 - lengthC5**2)**2 / (2 * lengthB5 * lengthBC)**2
cos2Beta = (lengthC5**2 + lengthCD**2 - lengthB5**2)**2 / (2 * lengthC5 * lengthCD)**2
cos2Zeta = (lengthD5**2 + lengthBD**2 - lengthB5**2)**2 / (2 * lengthD5 * lengthBD)**2

# Calculate sine of angles Alpha, Beta & Zeta from cos squares
sinAlpha = (1 - cos2Alpha)**0.5
sinBeta = (1 - cos2Beta)**0.5
sinZeta = (1 - cos2Zeta)**0.5

# Calculate x & y coordinates of M5 stick
calcx = ((lengthAB * cosZeta) + (lengthBC * cosAlpha) + (lengthAC * cosBeta)) / 3
calcy = ((lengthAB * sinZeta) + (lengthBC * sinAlpha) + (lengthAC * sinBeta)) / 3

x3 = (calcx / lengthAB) * 10
y3 = (calcy / lengthDA) * 10

############################################################
# Fourth Triangle
# Calculate cosines of angles Alpha (ADC), Beta (CAB) & Zeta (ABD)
cosAlpha = (lengthC5**2 + lengthCD**2 - lengthD5**2) / (2 * lengthC5 * lengthCD)
cosBeta = (lengthD5**2 + lengthDA**2 - lengthC5**2) / (2 * lengthD5 * lengthDA)
cosZeta = (lengthA5**2 + lengthAC**2 - lengthC5**2) / (2 * lengthA5 * lengthAC)

# Calculate cosine squares of angles Alpha, Beta & Zeta
cos2Alpha = (lengthC5**2 + lengthCD**2 - lengthD5**2)**2 / (2 * lengthC5 * lengthCD)**2
cos2Beta = (lengthD5**2 + lengthDA**2 - lengthC5**2)**2 / (2 * lengthD5 * lengthDA)**2
cos2Zeta = (lengthA5**2 + lengthAC**2 - lengthC5**2)**2 / (2 * lengthA5 * lengthAC)**2

# Calculate sine of angles Alpha, Beta & Zeta from cos squares
sinAlpha = (1 - cos2Alpha)**0.5
sinBeta = (1 - cos2Beta)**0.5
sinZeta = (1 - cos2Zeta)**0.5

# Calculate x & y coordinates of M5 stick
calcx = ((lengthAB * cosZeta) + (lengthBC * cosAlpha) + (lengthAC * cosBeta)) / 3
calcy = ((lengthAB * sinZeta) + (lengthBC * sinAlpha) + (lengthAC * sinBeta)) / 3

x4 = (calcx / lengthAB) * 10
y4 = (calcy / lengthDA) * 10

############################################################
# Final Aggregation of location
finalx = (x1 + x2 + x3 + x4) / 4
finaly = (y1 + y2 + y3 + y4) / 4


# print(finalx)
# print(finaly)
