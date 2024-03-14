import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from utilities import directory

A = 13900
B = 1.689
###################
#### Functions ####
###################
def calcRefractionIndex(theta: float):
    return np.sqrt( ( (2/np.sqrt(3)) * np.sin(theta * np.pi /180) +(1/2))**2 +  3/4   )

def calcWaveLength(n: float):
    return np.sqrt(A/(n-B))

def calcTemperature(roomTemp, voltage, current):
    return roomTemp + (((voltage/current)/R0)-1)/a0

def invFit(x, A):
    return A/x

##############################
#### Constants and Arrays ####
##############################
angleTempArray = [0 for i in range(0,14)]
currVoltTempArray = [0 for i in range(0,14)]
roomTempTempArray = [293 for i in range(0,14)]

#### Shape temp
roomTemps = np.array(roomTempTempArray)


R0 = 1.1
a0 = 0.0045


#######################
#### Data analysis ####
#######################
for fileName in next(os.walk(f"{directory}/rawData/"), (None, None, []))[2]:
    angles = np.array([])
    intensities = np.array([])
    testNum = fileName.lstrip('test').rstrip('.txt')

    if "csv" not in fileName:


        with open(f"{directory}/rawData/{fileName}") as sampleFile:
            data = sampleFile.readlines()[2:]
            for line in data:
                line = line.rstrip('\n')
                angle, intensity = line.split('\t')

                angles = np.append(angles, float(angle))
                intensities = np.append(intensities, float(intensity))

        #### Finding peaks
        peakArray, peakData = find_peaks(intensities, distance=40, prominence=0.01)
        maxIdx= max(range(len(peakData['prominences'])), key=peakData['prominences'].__getitem__)
        withoutMax = [prominence for prominence in peakData['prominences']]
        withoutMax[maxIdx] =-10000000
        secondMaxIdx = max(range(len(withoutMax)), key=withoutMax.__getitem__)

        angleTempArray[int(testNum) - 3] = ((angles[peakArray[secondMaxIdx]], angles[peakArray[maxIdx]]))

        #### Uncomment to show graphs containing peaks
        # plt.axvline(angles[peakArray[maxIdx]], c="k", ymin=0, ymax=5)
        # plt.axvline(angles[peakArray[secondMaxIdx]], c="k", ymin=0, ymax=5)
        # plt.plot(angles, intensities)
        # plt.ylim(min(intensities), max(intensities) + 0.1 *  max(intensities))

        # plt.savefig(f"{directory}/output/{fileName.rstrip('.txt')}.pdf")
        # plt.cla()


with open(f"{directory}/rawData/voltCurr.csv", 'r') as voltageCurrValues:
    for line in voltageCurrValues.readlines():
        voltage, current, test = line.rstrip('\n').split(',')
        currVoltTempArray[int(test) - 3] = (float(voltage), float(current))



#### Shape (theta0: float, thetal: float)
angleTup = np.array(angleTempArray)

#### Shape (voltage: float, current: float)
voltCurr = np.array(currVoltTempArray)

assert len(angleTup) == len(voltCurr) and len(angleTup) == len(roomTemps)

waveLengths = np.array([])
temps = np.array([])

for i in range(len(angleTup)):
    theta0, thetal = angleTup[i]
    voltage, current = voltCurr[i]
    roomTemp = roomTemps[i]

    theta = theta0 - thetal
    n = calcRefractionIndex(theta)
    print(n)

    waveLength = calcWaveLength(n) / 1000000000
    temperature = calcTemperature(roomTemp, voltage, current)

    waveLengths = np.append(waveLengths, waveLength)
    temps = np.append(temps, temperature)

    print(temperature, theta0- thetal, waveLength)


xVals = np.linspace(min(temps),max(temps), 100)
pvars, pcov = curve_fit(invFit, temps, waveLengths)

print("Mean value of temp times wavelength: ",np.mean(temps * waveLengths), *pvars)

plt.plot(xVals, invFit(xVals, *pvars))
plt.scatter(temps, waveLengths)
plt.savefig(f"{directory}/output/lambdaVsTemps.pdf")

