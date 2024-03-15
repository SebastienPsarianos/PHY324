from os import listdir
from scipy.optimize import curve_fit
import numpy as np

from newUtils import *

#######################
#### Set up Arrays ####
#######################
terminalVG = np.array([])
terminalVG_Unc = np.array([])
secantVG = np.array([])
secantVG_Unc = np.array([])
measuredSizeG = np.array([])

#####################
#### Parse Sizes ####
#####################
measuredSizes = {};
with open(f"{glycerineDir}/sizes.txt") as glycSizeFile:
    sizes = glycSizeFile.readlines()
    for line in sizes:
        sampleType, sampleSize = line.strip('\n').split(': ')
        measuredSizes[sampleType] = float(sampleSize)


############################################
#### Populate arrays with velocity data ####
############################################
for glycerineFileName in listdir(f"{glycerineDir}/txt"):
    with open(f"{glycerineDir}/txtTrimmed/{glycerineFileName}", 'r') as glycerineFile:

        #### Parse file
        sampleType, trialNumber = glycerineFileName.strip('.txt').split('--')
        _, sizeCategory = sampleType.split('-')
        sampleData = glycerineFile.read().splitlines()[2:]

        #### Grab the measured size
        measuredSize = measuredSizes[f"{sizeCategory}-{trialNumber}"]

        #### Get position time tuples for the last 80% of measurements
        start, stop = round(len(sampleData) * 0.2), round(len(sampleData))
        posnTimes = parsePositionVTime(sampleData[start:stop])

        velocities = np.array([])
        times = np.array([])
        uncertainties = np.array([])
        for i in range(len(posnTimes) - 1):
            x0, t0 = posnTimes[i]
            x1, t1 = posnTimes[i + 1]

            velocity, time = calculateVelocity(x1, t1, x0, t0)
            uncertainty = velUncertainty(x1, t1, x0, t0, measuredSize, velocity)

            velocities = np.append(velocities, velocity)
            times = np.append(times, time)
            uncertainties = np.append(uncertainties, uncertainty)

        #### Secant velocity calculation
        secantVelocity = (posnTimes[-1][0]-posnTimes[0][0])/(posnTimes[-1][1]-posnTimes[0][1])
        #### Calculate the maximum velocity
        terminalVelocityMax = max(range(len(velocities)), key=velocities.__getitem__)

        ###########################
        #### Shaping for plot #####
        ###########################
        terminalVG = np.append(terminalVG,
                               velocities[terminalVelocityMax])
        terminalVG_Unc = np.append(terminalVG_Unc,
                                  uncertainties[terminalVelocityMax])

        secantVG = np.append(secantVG, secantVelocity)
        secantVG_Unc = np.append(secantVG_Unc,
                                  velUncertainty(*posnTimes[-1],
                                                 *posnTimes[0],
                                                 measuredSize,
                                                 secantVelocity))
        # Put in the measured size values
        measuredSizeG = np.append(measuredSizeG,
                                   measuredSize)


############################
#### Gerine Fitting #####
############################
xValuesG = np.linspace(min(measuredSizeG), max(measuredSizeG), 200)
terminalFitG, _ = curve_fit(squaredFit, measuredSizeG, terminalVG)
secantFitG, _ = curve_fit(squaredFit, measuredSizeG, secantVG)


