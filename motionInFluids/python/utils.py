import numpy as np
from os import path
from math import floor, log10

#####################
#### Directories ####
#####################
directory = path.dirname(path.realpath(__file__))
glycerineDir = f"{directory}/data/glycerineData"
waterDir = f"{directory}/data/waterData"

#######################
#### Fit Functions ####
#######################
def squaredFit(x, A):
    return A * x **2

def sqrtFit(x, A):
    return A * np.sqrt(np.abs(x))

################################
#### Posn / Vel Calculation ####
################################
def parsePositionVTime(data):
    posnTime = []

    for i in range(0, len(data)):
        t, x = data[i].split("\t")
        posnTime.append((float(x), float(t)))
    return posnTime

def calculateVelocity(x1, t1, x0, t0):
    velocity = (x1-x0)/(t1-t0)
    return velocity, t0

###########################
#### Error Propagation ####
###########################

def velUncertainty(x1, t1, x0, t0, velocity, frameLength, A=False):
    tUncertainty = sumErrorProp(frameLength/4 , frameLength/4)
    xUncertainty = sumErrorProp(0.05, 0.05)

    return divErrorProp(x1-x0, xUncertainty, t1-t0, tUncertainty, velocity)

def divErrorProp(v1, e1, v2, e2, val):
    if v1 ==0 or v2 ==0:
        return 0
    return val * np.sqrt((e1/v1)**2 + (e2/v2)**2)

def sumErrorProp(e1, e2):
    return np.sqrt(e1**2 + e2**2)

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