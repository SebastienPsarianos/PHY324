import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

directory = os.path.dirname(os.path.abspath(__file__))

angles = np.array([])
periods = np.array([])
angErr = np.array([])
periodErr = np.array([])

with open(f"{directory}/timeData.csv") as timeData:
    for line in timeData.readlines():
        angle, *periodValues = line.rstrip("\n").split(",")
        for i in range(0, 3):
            angles = np.append(angles, int(angle))
            periods = np.append(periods, float(periodValues[i+1]) - float(periodValues[i]))
            angErr = np.append(angErr, 1)
            periodErr = np.append(periodErr, 0.0333)

def constantFn(x, A):
    return A*x / x

def redChiSquared(y, fit):
    return (1/ (len(y) - 1)) * np.sum( (y- fit)**2 / (periodErr**2) )


Afit, _ = curve_fit(constantFn, angles, periods)

chi = redChiSquared(periods, Afit)

plt.title(f" Pendulum oscillation period vs initial release angle. \n Contains constant function best fit ")
plt.plot(angles, constantFn(angles, constantFn(angles, Afit)), c="b", label=f"Constant Fit $T_{{\\rm fit}} \\approx  {str(Afit[0])[:5]} $s and $\\chi^2_{{\\rm red}} \\approx {str(chi)[:5]}$")
plt.ylim(0, 2)
plt.errorbar(angles, periods, 0.03, 1, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Measured Period Values")
plt.xlabel("Initial angle of release $\\theta_0$ (Degrees)")
plt.ylabel("Period of oscillations (Seconds)")
plt.legend()
plt.savefig(f"{directory}/periodAnglePlot.pdf")
