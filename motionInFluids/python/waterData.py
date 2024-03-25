from os import listdir
from scipy.optimize import curve_fit
import numpy as np

from utils import *

#######################
#### Set up Arrays ####
#######################
terminalVW = np.array([])
terminalVW_Unc = np.array([])
reynoldsW = np.array([])

waterVelocityPlots = []
measuredSizeW = np.array([])

#####################
#### Parse Sizes ####
#####################
measuredSizes = {};
with open(f"{waterDir}/sizes.txt") as waterSizeFile:
    sizes = waterSizeFile.readlines()
    for line in sizes:
        sampleType, sampleSize = line.strip('\n').split(': ')
        measuredSizes[sampleType] = float(sampleSize)

############################################
#### Populate arrays with velocity data ####
############################################
for waterFileName in listdir(f"{waterDir}/txt"):

    with open(f"{waterDir}/txtTrimmed/{waterFileName}", 'r') as waterFile:

        #### Parse file
        sampleType, trialNumber = waterFileName.strip('.txt').split('--')
        _, sizeCategory = sampleType.split('-')
        sampleData = waterFile.read().splitlines()[2:]

        #### Grab measured size
        measuredSize = measuredSizes[f"{sizeCategory}-{trialNumber}"]

        start, stop = round(len(sampleData) * 0.2), round(len(sampleData))
        posnTimes = parsePositionVTime(sampleData)
        frameLength = posnTimes[1][1] - posnTimes[0][1]
        posnTimes = posnTimes[start:stop]


        # #### Remove 0 position points
        posnTimes = [(position, time) for position, time in posnTimes if position != 0 ]

        velocities = np.array([])
        times = np.array([])
        uncertainties = np.array([])
        for i in range(len(posnTimes) - 4):
            x0, t0 = posnTimes[i]
            x1, t1 = posnTimes[i+4]

            velocity, time = calculateVelocity(x1, t1, x0, t0)
            uncertainty = velUncertainty(x1, t1, x0, t0,
                                         velocity,
                                         frameLength)

            velocities = np.append(velocities, velocity)
            times = np.append(times, time)
            uncertainties = np.append(uncertainties, uncertainty )




        #### Calculate overall velocity based on initial and final t, x
        secantVelocity = (posnTimes[-1][0]-posnTimes[0][0])/(posnTimes[-1][1]-posnTimes[0][1])


        #### Filter out data points greater than 2.5 times the avg velocity
        toKeep = np.abs(velocities) < 1.5 * secantVelocity
        velocities = velocities[toKeep]
        times = times[toKeep]
        uncertainties = uncertainties[toKeep]

        # Calculate the maximum velocity
        terminalVIndex = max(range(len(velocities)), key=velocities.__getitem__)

        ###########################
        #### Shaping for plot #####
        ###########################
        terminalVW = np.append(terminalVW, velocities[terminalVIndex])
        terminalVW_Unc = np.append(terminalVW_Unc, uncertainties[terminalVIndex])
        reynoldsW = np.append(reynoldsW, reynoldsNumber(measuredSize, velocity, 1/1000, .01 / 10))

        measuredSizeW = np.append(measuredSizeW, measuredSize)
        waterVelocityPlots.append((velocities, times, f"{sizeCategory}-{trialNumber}"))


########################
#### Water Fitting #####
########################
xValuesW = np.linspace(min(measuredSizeW), max(measuredSizeW), 200)
terminalFitW, pcov = curve_fit(sqrtFit, measuredSizeW, terminalVW)
terminalFitW_Unc = np.sqrt(pcov[0][0])
chi2W = redChiSquared(terminalVW, sqrtFit(measuredSizeW, *terminalFitW), terminalVW_Unc, len(terminalVW) - 1)
