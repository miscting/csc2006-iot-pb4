
#  A _______ B
#   |\  |  /|
#   |   5   |
#   |/__|__\|
#  D         C

# Length from pi to pi
lengthAB = 0.0
lengthBC = 0.0
lengthCD = 0.0
lengthDA = 0.0

# Diagonal Length from pi to pi
lengthAC = 0.0
lengthBD = 0.0

# Length from pi to m5
lengthA5 = 0.0
lengthB5 = 0.0
lengthC5 = 0.0
lengthD5 = 0.0

# Calculate cosines of angles Alpha (ADC), Beta (CAB) & Zeta (ABD)
cosAlpha = (lengthD5^2 + lengthDA^2 - lengthA5^2) / (2 * lengthD5 * lengthDA)
cosBeta = (lengthA5^2 + lengthAB^2 - lengthD5^2) / (2 * lengthA5 * lengthAB)
cosZeta = (lengthB5^2 + lengthBD^2 - lengthD5^2) / (2 * lengthB5 * lengthBD)

# Calculate cosine squares of angles Alpha, Beta & Zeta
cos2Alpha = (lengthD5^2 + lengthDA^2 - lengthA5^2)^2 / (2 * lengthD5 * lengthDA)^2
cos2Beta = (lengthA5^2 + lengthAB^2 - lengthD5^2)^2 / (2 * lengthA5 * lengthAB)^2
cos2Zeta = (lengthB5^2 + lengthBD^2 - lengthD5^2)^2 / (2 * lengthB5 * lengthBD)^2

# Calculate sine of angles Alpha, Beta & Zeta from cos squares
sinAlpha = (1 - cos2Alpha)^0.5
sinBeta = (1 - cos2Beta)^0.5
sinZeta = (1 - cos2Zeta)^0.5

# Calculate x & y coordinates of M5 stick
calcx = (lengthDA * cosZeta) + (lengthAB * cosAlpha) + (lengthBD * cosBeta) / 3
calcy = (lengthDA * sinZeta) + (lengthAB * sinAlpha) + (lengthBD * cosBeta) / 3

x = (calcx / lengthAB) * 10
y = (calcy / lengthDA) * 10

