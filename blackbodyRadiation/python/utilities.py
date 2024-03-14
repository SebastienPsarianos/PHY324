import numpy as np
from os import path
from math import floor, log10

###################
#### Directory ####
###################
directory = path.dirname(path.abspath(__file__))

###########################
#### Fitting Functions ####
###########################
def sinFn(t, freq, psi):
    return np.sin(freq * t + psi)

def expDecay(t, A, tau):
    return A * np.exp(-t/tau)

def constant(x, A):
    return np.full(len(x), A)

def sqrt(x, a):
    return a * np.sqrt(x)

###########################
#### Error Propagation ####
###########################
def arctanProp(x, y, xErr, yErr):
    return np.sqrt( (y/(x ** 2 + y ** 2))**2 * xErr**2 + (x/(x ** 2 + y ** 2))**2 * yErr**2)

def sqrtProp(x, xErr):
    """Propagates error for y = sqrt(x)"""
    return xErr/(2*np.sqrt(x))

############################
#### Size Data for Mass ####
############################

class Mass():
    weight = 0
    width = 0
    height = 0
    hookLength = 0

    def __init__(this, weight, width, height, hookLength):
        this.weight = weight
        this.width = width
        this.height = height
        this.hookLength = hookLength



##############################
#### Statistical Analysis ####
##############################
def redChiSquared(meas, fit, unc, dof):
    return (1/ dof) * np.sum((meas- fit) ** 2 / (unc **2) )

def sigFig(x: float, precision: int):
    x = float(x)
    precision = int(precision)
    numDec = max((precision -1) - int(floor(log10(abs(x)))), 0)
    rounded = round(x, -int(floor(log10(abs(x)))) + (precision - 1))
    string = format(rounded, f'.{numDec}f')
    if precision == 1:
        string = string.rstrip('0').rstrip('.')

    return string


############################
#### Global uncertainty ####
############################
periodErr = np.sqrt((1/30) ** 2 * (0.5) )
lengthErr = 0.001
massErr = 1
angErr = 3
