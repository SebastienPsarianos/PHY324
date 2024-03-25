import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid, simpson
from utilities import directory, fourthFit, calcTemperature, redChiSquared, sigFig

def find_closest(array, value):
    return min(range(len(array)), key= lambda i : np.abs(array[i] - value))

def integrateSampleFromBase(x, y, baseline):
    return simpson(x, y) - baseline * (x[-1] - x[0])

################
#### Arrays ####
################
integrationData = [0 for _ in range(0,49)]
currVolts = [0 for _ in range(0,49)]
roomTempArray = [294 for _ in range(0,49)]

#### Shape temp

#######################
#### Data analysis ####
#######################
for fileName in next(os.walk(f"{directory}/rawData/stephanBoltzmann"), (None, None, []))[2]:
    angles = np.array([])
    intensities = np.array([])

    if "csv" not in fileName:
        with open(f"{directory}/rawData/stephanBoltzmann/{fileName}") as sampleFile:
            testNum = int(fileName.lstrip('test').rstrip('.txt'))
            data = sampleFile.readlines()[2:]
            for line in data:
                line = line.rstrip('\n')
                angle, intensity = line.split('\t')

                angles = np.append(angles, float(angle))
                intensities = np.append(intensities, float(intensity))

        #### Finding peaks, integration bounds and background light
        peakArray, peakData = find_peaks(intensities, distance=40, prominence=0.01)
        maxAngleIdx = peakArray[max(range(len(peakData['prominences'])), key=peakData['prominences'].__getitem__)]
        theta0, theta1 = find_closest(angles, angles[maxAngleIdx] - 7.5), find_closest(angles, angles[maxAngleIdx] + 7.5)
        baseline = (np.mean(intensities[:theta0]) + np.mean(intensities[theta1:])) / 2

        integral = 0
        for i in range(theta0, theta1):
            height = np.mean(intensities[i:i+2])
            width = angles[i+1] - angles[i]
            integral += height * width

        integral = integral - baseline

        test = np.mean(intensities[theta0:theta1]) * (angles[theta1]- angles[theta0]) - baseline

        integrationData[testNum-1] = integral

        #### Graphs displaying peak angle and integral bounds
        plt.axvline(angles[maxAngleIdx], c="k", ymin=0, ymax=5)
        plt.axvline(angles[theta0], c="k", ymin=0, ymax=5)
        plt.axvline(angles[theta1], c="k", ymin=0, ymax=5)

        #### Displaying peak value and baseline
        plt.axhline(intensities[maxAngleIdx], c="k")
        plt.axhline(baseline, c="k")

        plt.plot(angles, intensities)
        plt.ylim(min(intensities), max(intensities) + 0.1 *  max(intensities))

        plt.savefig(f"{directory}/output/stephanBoltzmann/peaks/{fileName.rstrip('.txt')}.pdf")
        plt.cla()


voltageGroups = {}
with open(f"{directory}/rawData/stephanBoltzmann/voltCurr.csv", 'r') as voltageCurrValues:
    for line in voltageCurrValues.readlines():
        test, voltage, current  = line.rstrip('\n').split(',')
        voltage, current = float(voltage), float(current)
        if voltage not in voltageGroups:
            voltageGroups[voltage] = [], []

        voltageGroups[voltage][0].append(integrationData[int(test)-1])
        voltageGroups[voltage][1].append(calcTemperature(293, voltage,current))

        currVolts[int(test) - 1] = calcTemperature(293, voltage, current)

plotX = np.array([])
xUnc = np.array([])
plotY = np.array([])
yUnc = np.array([])
for key in voltageGroups:
    integrals, temperatures = voltageGroups[key]
    plotX = np.append(plotX, np.mean(temperatures))
    xUnc = np.append(xUnc, np.std(temperatures))
    plotY = np.append(plotY, np.mean(integrals))
    yUnc = np.append(yUnc, np.std(integrals))


integrationData = np.array(integrationData)
temperatureData = np.array(currVolts)

pvars, pcov = curve_fit(fourthFit, plotX, plotY)
xVals = np.linspace(min(plotX), max(plotX), 100)

chi2 = redChiSquared(plotY, fourthFit(plotX, *pvars), yUnc, len(plotX) - 1)

plt.plot(xVals, fourthFit(xVals, *pvars), label=f"Line of best fit for fourth power function. \n $\\chi_{{\\rm red}} = {sigFig(chi2, 3)}$,\n $A=4.6 \\times 10^{{-14}} \\pm , 2\\times 10^{{-15}}$", c="k")
plt.errorbar(plotX, plotY, xerr=xUnc, yerr=yUnc, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Intensity approximation")
plt.xlabel("Inferred Temperature (K)")
plt.ylabel("Approximated proportional total intensity ($V\cdot rad$)")
plt.legend()

plt.savefig(f"{directory}/output/stephanBoltzmann/intensityVsTemps.pdf")
plt.cla()

plt.axhline(0, ls="dashed", c="k")
plt.scatter(plotX, fourthFit(plotX, *pvars) - plotY, c="r", label="Residuals")
plt.xlabel("Inferred blackbody temperature (K)")
plt.ylabel("Residuals for proportional total intensity ($V\cdot rad$)")
plt.legend()
plt.savefig(f"{directory}/output/stephanBoltzmann/intensityVsTempsRes.pdf")
