from os import listdir
from scipy.optimize import curve_fit
import numpy as np

from utils import *

#######################
#### Set up Arrays ####
#######################
terminalVG = np.array([])
terminalVG_Unc = np.array([])
measuredSizeG = np.array([])
reynoldsG = np.array([])

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
        posnTimes = parsePositionVTime(sampleData)
        frameLength = posnTimes[1][1] - posnTimes[0][1]

        posnTimes = posnTimes[start:stop]

        velocities = np.array([])
        times = np.array([])
        uncertainties = np.array([])
        for i in range(len(posnTimes) - 4):
            x0, t0 = posnTimes[i]
            x1, t1 = posnTimes[i + 4]

            velocity, time = calculateVelocity(x1,t1,x0,t0)
            uncertainty = velUncertainty(x1,t1,x0,t0,
                                         velocity,
                                         frameLength)

            velocities = np.append(velocities, velocity)
            times = np.append(times, time)
            uncertainties = np.append(uncertainties, uncertainty)




        #### Calculate the maximum velocity
        terminalVelocityMax = max(range(len(velocities)), key=velocities.__getitem__)

        ###########################
        #### Shaping for plot #####
        ###########################
        terminalVG = np.append(terminalVG, velocities[terminalVelocityMax])
        terminalVG_Unc = np.append(terminalVG_Unc, uncertainties[terminalVelocityMax])
        reynoldsG = np.append(reynoldsG, reynoldsNumber(measuredSize, velocity, 1.26/1000, 9.34 / 10))
        measuredSizeG = np.append(measuredSizeG, measuredSize)

##################
#### Fitting #####
##################
xValuesG = np.linspace(min(measuredSizeG), max(measuredSizeG), 200)
terminalFitG, pcov = curve_fit(squaredFit, measuredSizeG, terminalVG)
terminalFitG_Unc = np.sqrt(pcov[0][0])
chi2G = redChiSquared(terminalVG, squaredFit(measuredSizeG, *terminalFitG), terminalVG_Unc, len(terminalVG) - 1)
