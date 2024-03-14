import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utilities import expDecay, directory, arctanProp, sizeInfo, redChiSquared, sigFig

##################################
#### Parse CSV and get angles ####
##################################
times = np.array([])
xPosns = np.array([])
yPosns = np.array([])

with open(f"{directory}/data/decay/15degDecay.csv") as decayData:
    data = decayData.readlines()
    for point in data:
        t, x, y = point.split(',')
        times = np.append(times, float(t))
        xPosns = np.append(xPosns, float(x))
        yPosns = np.append(yPosns, float(y))

avgY = np.mean(yPosns)
angles = np.arctan(xPosns / avgY)

#####################################
#### Calculate / Propogate Error ####
#####################################
# Weight, Width, Length, Hook Length
xyUnc = 0.5 * np.sqrt(sizeInfo["200g"].width ** 2 + sizeInfo["200g"].height ** 2)\

print(xyUnc)
angleUncertainties = arctanProp(xPosns, yPosns, xyUnc, xyUnc)
timeUncertainty = (times[1] - times[0])/2

########################
#### Get Avg Values ####
########################
maxVals = np.array([])
maxValTimes = np.array([])
maxValUnc = np.array([])

n=100
length = int(np.floor(len(times) / n))
for i in range(n):
    start = i * length
    end = (i+1) * length
    center = int(np.floor((i + 0.5) * length))

    maxVals = np.append(maxVals, np.max(angles[start:end]))
    maxValTimes = np.append(maxValTimes, times[center])
    maxValUnc = np.append(maxValUnc, angleUncertainties[center])

###############################
#### Fit Exponential Decay ####
###############################
(A, gamma), pcov = curve_fit(expDecay, maxValTimes, maxVals)

##################
#### Plotting ####
##################
rChi = sigFig(redChiSquared(maxVals, expDecay(maxValTimes, A, gamma), maxValUnc, len(maxVals)-2),4)
amplitude = sigFig(A,4)
amplitudeErr = sigFig(np.sqrt(pcov[0][0]), 1)
gammaRounded = sigFig(gamma, 3)
gammaErr = sigFig(np.sqrt(pcov[1][1]), 1)


plt.xlim(0, max(times))
plt.ylabel(f"Pendulum angle (radians)")
plt.xlabel(f"Time (s)")
plt.errorbar(times, angles, xerr=timeUncertainty, yerr=angleUncertainties, c="r", ls="", marker=".", capsize=1, ecolor="k", label="Measured Period Values", markersize=1)
plt.savefig(f"{directory}/output/decay/plot.pdf")
plt.cla()


plt.ylabel(f"Maximum angle in {sigFig(maxValTimes[1]-maxValTimes[0], 3)}s region surrounding time (radians)")
plt.xlabel(f"Center of sample interval (s)")
plt.ylim(0,0.35)
plt.plot(times, expDecay(times, A, gamma), c='b', label=f"Exponential decay fit: $\\chi_{{red}}^2 = {rChi}$, $A = ({amplitude} \\pm {amplitudeErr})$rad, $\\tau = ({gammaRounded}\\pm {gammaErr})s$")
plt.errorbar(maxValTimes, maxVals, xerr=timeUncertainty, yerr=maxValUnc, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Measured Period Values")
plt.legend(loc="lower left", prop={'size': 8})
plt.savefig(f"{directory}/output/decay/envelope.pdf")
plt.cla()