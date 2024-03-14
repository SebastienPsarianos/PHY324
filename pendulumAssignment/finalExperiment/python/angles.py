import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utilities import constant, sigFig, periodErr, redChiSquared, angErr

directory = os.path.dirname(os.path.abspath(__file__))

angles = np.array([])
periods = np.array([])

###################################
#### Parse CSV and get periods ####
###################################
with open(f"{directory}/data/angles/variedAngle.csv") as timeData:
    samples = [([y for y in line.strip('\n').split(':')[0].split(',') ], [x for x in line.strip('\n').split(':')[1].split(',') if x != ""]) for line in timeData.readlines()]
    for (angle, _), intervals in samples:
        for i in range(len(intervals) - 1):
            angles = np.append(angles, float(angle))
            periods = np.append(periods, (int(intervals[i+1]) - int(intervals[i])) / 30)

#################
#### Fitting ####
#################
T, pcov = curve_fit(constant, angles, periods)
tRounded = sigFig(T, 4)
rChi = sigFig(redChiSquared(periods, constant(angles, T), periodErr, len(angles) - 1),4)
tErr = sigFig(np.sqrt(pcov[0][0]),1)

##################
#### Plotting ####
##################
xValues = np.linspace(0,2,100)
plt.ylim(0, 2)
plt.errorbar(angles, periods, periodErr, angErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Measured Period Values")
plt.plot(angles, constant(angles, T), c="k", label=f"Constant fit: $\\chi_{{red}}^2={rChi}$, $T = ({tRounded} \\pm {tErr})s$")

plt.xlabel("Initial angle of release $\\theta_0$ (Degrees)")
plt.ylabel("Period of oscillations (Seconds)")
plt.legend(loc="lower left")
plt.savefig(f"{directory}/output/variableAngle/plot.pdf")
plt.cla()

