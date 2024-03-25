import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from utilities import directory, calcRefractionIndex, calcWaveLength, calcTemperature, invFit, redChiSquared, sigFig

################
#### Arrays ####
################
angleTempArray = [0 for _ in range(0,35)]
currVoltTempArray = [0 for _ in range(0,35)]
roomTemp = 293
#### Shape temp

#######################
#### Data analysis ####
#######################
for fileName in next(os.walk(f"{directory}/rawData/wein"), (None, None, []))[2]:
    angles = np.array([])
    intensities = np.array([])
    testNum = fileName.lstrip('test').rstrip('.txt')

    if "csv" not in fileName:
        with open(f"{directory}/rawData/wein/{fileName}") as sampleFile:
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

        angleTempArray[int(testNum) - 1] = ((angles[peakArray[secondMaxIdx]], angles[peakArray[maxIdx]]))

        #### Graphs displaying peaks
        # plt.axvline(angles[peakArray[maxIdx]], c="k", ymin=0, ymax=5)
        # plt.axvline(angles[peakArray[secondMaxIdx]], c="k", ymin=0, ymax=5)
        # plt.plot(angles, intensities)
        # plt.ylim(min(intensities), max(intensities) + 0.1 *  max(intensities))

        # plt.savefig(f"{directory}/output/wein/peaks/{fileName.rstrip('.txt')}.pdf")
        # plt.cla()


voltageGroups = {}
with open(f"{directory}/rawData/wein/voltCurr.csv", 'r') as voltageCurrValues:
    for line in voltageCurrValues.readlines():

        test, voltage, current  = line.rstrip('\n').split(',')
        voltage, current = float(voltage), float(current)

        if voltage not in voltageGroups:
            voltageGroups[voltage] = [], []

        theta0, thetal = angleTempArray[int(test)-1]

        theta = theta0 - thetal
        n = calcRefractionIndex(theta)
        waveLength = calcWaveLength(n) / 1000000000
        temperature = calcTemperature(roomTemp, voltage, current)

        voltageGroups[voltage][0].append(waveLength)
        voltageGroups[voltage][1].append(temperature)


plotX = np.array([])
xUnc = np.array([])
plotY = np.array([])
yUnc = np.array([])
for key in voltageGroups:
    waveLengths, temperatures = voltageGroups[key]
    plotX = np.append(plotX, np.mean(temperatures))
    xUnc = np.append(xUnc, np.std(temperatures))
    plotY = np.append(plotY, np.mean(waveLengths))
    yUnc = np.append(yUnc, np.std(waveLengths))


xVals = np.linspace(min(plotX),max(plotX), 100)
pvars, pcov = curve_fit(invFit, plotX, plotY)
chi2 = redChiSquared(plotY, invFit(plotX, *pvars), yUnc, len(plotX) - 1)
print("Mean value of temp times wavelength: ", np.mean(plotX * plotY), *pvars)
print("Reduced chi squared", chi2)

plt.ylim(0, max(plotY) * 1.1)
plt.plot(xVals, invFit(xVals, *pvars), label=f"Line of best fit for inverse function. \n $\\chi_{{\\rm red}} = {sigFig(chi2, 3)}$,\n $A={sigFig(pvars[0], 3)} \\pm {sigFig(np.sqrt(pcov[0][0]), 1)}$", c="k")
plt.errorbar(plotX, plotY, yerr=yUnc, xerr=xUnc, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Inferred $\lambda_{\\rm max}$")
plt.xlabel("Inferred blackbody temperature (K)")
plt.ylabel("Inferred spectrum peak wavelength (nm)")

plt.legend()
plt.savefig(f"{directory}/output/wein/lambdaVsTemps.pdf")
plt.cla()


plt.axhline(0, ls="dashed", c="k")
plt.scatter(plotX, invFit(plotX, *pvars) - plotY, c="r", label="Residuals")
plt.xlabel("Inferred blackbody temperature (K)")
plt.ylabel("Residuals for inferred spectrum peak wavelength (nm)")
plt.legend()
plt.savefig(f"{directory}/output/wein/lambdaVsTempsResidual.pdf")