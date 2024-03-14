from os import listdir
from scipy.optimize import curve_fit
import numpy as np

from utils import *

glycSizeValues = np.array([])

#######################
#### Set up Arrays ####
#######################
glycMaxVel = np.array([])
glycMaxVelUnc = np.array([])
glycSecVel = np.array([])
glycSecVelUnc = np.array([])


############################################
#### Populate arrays with velocity data ####
############################################
for glycerineFileName in listdir(f"{glycerineDir}/txt"):
    with open(f"{glycerineDir}/txtTrimmed/{glycerineFileName}", 'r') as glycerineFile:

        sampleType, trialNumber = glycerineFileName.strip('.txt').split('--')

        _, sizeCategory = sampleType.split('-')

        sampleData = glycerineFile.read().splitlines()[2:]

        #### Parse the positions and times for the last 80% of the measurements
        start, stop = round(len(sampleData) * 0.2), round(len(sampleData))
        positions, posnTimes = parsePositionVTime(sampleData[start:stop])

        # calculate the speeds and times of each interval
        speeds, times, uncertainties = calculateVelocity(positions, posnTimes, glycSizes[f"{sizeCategory}-{trialNumber}"])

        # Calculate overall velocity based on initial and final t, x
        secantVelocity = (positions[-1]-positions[0])/(posnTimes[-1]-posnTimes[0])

        # Calculate the maximum velocity
        terminalVelocityMax = max(range(len(speeds)), key=speeds.__getitem__)

        # Add them all to list
        glycMaxVel = np.append(glycMaxVel, speeds[terminalVelocityMax])
        glycMaxVelUnc = np.append(glycMaxVelUnc, uncertainties[terminalVelocityMax])

        glycSecVel = np.append(glycSecVel, secantVelocity)
        glycSecVelUnc = np.append(glycSecVelUnc, velUncertainty(positions[-1],posnTimes[-1],positions[0],posnTimes[0], glycSizes[f"{sizeCategory}-{trialNumber}"], secantVelocity))

        # Put in the measured size values
        glycSizeValues = np.append(glycSizeValues, glycSizes[f"{sizeCategory}-{trialNumber}"])


waterMeanVel = np.array([])
waterMaxVel = np.array([])
waterMaxVelUnc = np.array([])

waterSecVel = np.array([])
waterSecVelUnc = np.array([])

waterVelocityPlots = []
waterSizeValues = np.array([])

for waterFileName in listdir(f"{waterDir}/txt"):

    with open(f"{waterDir}/txtTrimmed/{waterFileName}", 'r') as waterFile:
        sampleType, trialNumber = waterFileName.strip('.txt').split('--')
        _, sizeCategory = sampleType.split('-')

        sampleData = waterFile.read().splitlines()[2:]

        # Parse the positions and times for the last 80% of the measurements
        positions, posnTimes = parsePositionVTime(sampleData)

        toKeep = positions != 0
        positions = positions[toKeep]
        posnTimes = posnTimes[toKeep]

        start, stop = round(len(sampleData) * 0.2), round(len(sampleData))

        # calculate the speeds and times of each interval
        speeds, times, uncertainties = calculateVelocity(positions, posnTimes, waterSizes[f"{sizeCategory}-{trialNumber}"])

        # Calculate overall velocity based on initial and final t, x
        secantVelocity = (positions[-1]-positions[0])/(posnTimes[-1]-posnTimes[0])

        toKeep = np.abs(speeds) < 2.5 * secantVelocity
        speeds = speeds[toKeep]
        times = times[toKeep]
        uncertainties = uncertainties[toKeep]

        # Calculate the maximum velocity
        terminalVelocityMax = max(range(len(speeds)), key=speeds.__getitem__)

        # Add them all to list
        waterMaxVel = np.append(waterMaxVel, speeds[terminalVelocityMax])
        waterMaxVelUnc = np.append(waterMaxVelUnc, uncertainties[terminalVelocityMax])

        waterSecVel = np.append(waterSecVel, secantVelocity)
        waterSecVelUnc = np.append(waterSecVelUnc, velUncertainty(positions[-1],posnTimes[-1],positions[0],posnTimes[0], waterSizes[f"{sizeCategory}-{trialNumber}"], secantVelocity))

        # Put in the measured size values
        waterSizeValues = np.append(waterSizeValues, waterSizes[f"{sizeCategory}-{trialNumber}"])
        waterVelocityPlots.append((speeds, times, f"{sizeCategory}-{trialNumber}"))


############################
#### Glycerine Fitting #####
############################
glycFitXValues = np.linspace(min(glycSizeValues), max(glycSizeValues), 200)
glycMaxFit, _ = curve_fit(squaredFit, glycSizeValues, glycMaxVel)
glycSecFit, _ = curve_fit(squaredFit, glycSizeValues, glycSecVel)


########################
#### Water Fitting #####
########################
waterFitXValues = np.linspace(min(waterSizeValues), max(waterSizeValues), 200)
waterMaxFit, _ = curve_fit(sqrtFit, waterSizeValues, waterMaxVel)
waterSecFit, _ = curve_fit(sqrtFit, waterSizeValues, waterSecVel, (53))
