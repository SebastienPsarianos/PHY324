import numpy as np
from os import path


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

##############################
#### Velocity Calculation ####
##############################
def calculateVelocity(positions, times, size):
    velocities = np.array([])
    startTimes = np.array([])
    uncertainties = np.array([])

    for i in range(0, len(positions) - 1):

        t0, v0 = times[i], positions[i]
        t1, v1 = times[i+1], positions[i+1]

        velocity = (v1-v0)/(t1-t0)

        velocities = np.append(velocities, velocity)
        startTimes = np.append(startTimes, t0)

        uncertainties = np.append(uncertainties, velUncertainty(v1,t1,v0,t0, size, velocity))
    return velocities, startTimes, uncertainties

def parsePositionVTime(data):
    positions = np.array([])
    times = np.array([])

    for i in range(0, len(data)):
        t, x = data[i].split("\t")

        positions = np.append(positions, float(x))
        times = np.append(times, float(t))
    return positions, times


def velUncertainty(v1,t1,v0,t0, size, velocity):
        tUncertainty = sumErrorProp(t1-t0  / 2 , t1-t0  / 2)
        xUncertainty = sumErrorProp(size/2, size/2)
        return divErrorProp(v1-v0, xUncertainty, t1-t0, tUncertainty, velocity)

def divErrorProp(v1, e1, v2, e2, val):
    if v1 ==0 or v2 ==0:
        return 0
    return np.sqrt((e1/v1)**2 + (e2/v2)**2)

def sumErrorProp( e1, e2):
    return np.sqrt(e1**2 + e2**2)







glycSizes = {};
with open(f"{glycerineDir}/sizes.txt") as glycSizeFile:
    sizes = glycSizeFile.readlines()
    for line in sizes:
        sampleType, sampleSize = line.strip('\n').split(': ')
        glycSizes[sampleType] = float(sampleSize)


waterSizes = {};
with open(f"{waterDir}/sizes.txt") as waterSizeFile:
    sizes = waterSizeFile.readlines()
    for line in sizes:
        sampleType, sampleSize = line.strip('\n').split(': ')
        waterSizes[sampleType] = float(sampleSize)
