import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utilities import constant, sizeInfo, redChiSquared, sigFig, periodErr, massErr

directory = os.path.dirname(os.path.abspath(__file__))

massData = {
    "20": sizeInfo["20g"].weight,
    "100": sizeInfo["100g"].weight,
    "200": sizeInfo["200g"].weight,
    "500": sizeInfo["500g"].weight,
}

masses = {
    "15": np.array([]),
    "30": np.array([]),
    "60": np.array([])
}
periods = {
    "15": np.array([]),
    "30": np.array([]),
    "60": np.array([])
}

###################################
#### Parse CSV and get periods ####
###################################
with open(f"{directory}/data/mass/variedMass.csv") as timeData:
    samples = [([y for y in line.strip('\n').split(':')[0].split(',') ], ([x for x in line.strip('\n').split(':')[1].split('|')[0].split(',') if x != ""], [x for x in line.strip('\n').split(':')[1].split('|')[1].split(',') if x != ""])) for line in timeData.readlines()]
    for (massCat, angle), (intervalsOne, intervalsTwo) in samples:
        mass = massData[massCat]

        for i in range(len(intervalsOne) - 1):
            periods[angle] = np.append(periods[angle], (int(intervalsOne[i+1]) - int(intervalsOne[i])) / 30)
            masses[angle] = np.append(masses[angle], mass)


        for i in range(len(intervalsTwo) - 1):
            periods[angle] = np.append(periods[angle], (int(intervalsTwo[i+1]) - int(intervalsTwo[i])) / 30)
            masses[angle] = np.append(masses[angle], mass)


#################################
#### Uncertainty Propagation ####
#################################
allMasses = np.concatenate((masses["15"], masses["30"], masses["60"]), 0)
allPeriods = np.concatenate((periods["15"], periods["30"], periods["60"]), 0)

#################
#### Fitting ####
#################
a, pcov = curve_fit(constant, allMasses, allPeriods)
a1, pcov1 = curve_fit(constant, masses["15"], periods["15"])
a2, pcov2 = curve_fit(constant, masses["30"], periods["30"])
a3, pcov3 = curve_fit(constant, masses["60"], periods["60"])

chi1 = sigFig(redChiSquared(periods["15"], constant(masses["15"], a1), periodErr, len(masses["15"]) -  1),4)
chi2 = sigFig(redChiSquared(periods["30"], constant(masses["30"], a2), periodErr, len(masses["30"]) -  1),4)
chi3 = sigFig(redChiSquared(periods["60"], constant(masses["60"], a3), periodErr, len(masses["60"]) -  1),4)
chi = sigFig(redChiSquared(allPeriods, constant(allMasses, a), periodErr, len(allMasses) -  1),4)

period1 = sigFig(a1,4)
uncPeriod1 = sigFig(np.sqrt(pcov1[0][0]), 1)

period2 = sigFig(a2,4)
uncPeriod2 = sigFig(np.sqrt(pcov2[0][0]), 1)

period3 = sigFig(a3,4)
uncPeriod3 = sigFig(np.sqrt(pcov3[0][0]), 1)

period = sigFig(a,4)
uncPeriod = sigFig(np.sqrt(pcov[0][0]), 1)


##################
#### Plotting ####
##################
#### Plot Text
xLabel = "Indicated mass (g)"
yLabel = "Period of oscillation (s)"

yLim = (0.8, 1.6)
xLim = (0, 550)
xVals = np.linspace(*xLim, 100)

#### 15 DEGREE PLOT
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.ylim(yLim)
plt.xlim(xLim)

plt.plot(xVals, constant(xVals, a1), c="b", label=f"Constant fit ($15^o$): $\\chi_{{red}}^2 = {chi1}$, $T=({period1} \\pm {uncPeriod1})s$" )
plt.errorbar(masses["15"], periods["15"], periodErr, massErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $15^o$ release")
plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableMass/15.pdf")
plt.cla()

#### 30 DEGREE PLOT
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.ylim(yLim)
plt.xlim(xLim)

plt.plot(xVals, constant(xVals, a2), c="r", label=f"Constant fit ($30^o$): $\\chi_{{red}}^2 = {chi2}$, $T=({period2} \\pm {uncPeriod2})s$" )
plt.errorbar(masses["30"], periods["30"], periodErr, massErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $30^o$ release")
plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableMass/30.pdf")
plt.cla()

#### 60 DEGREE PLOT
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.ylim(yLim)
plt.xlim(xLim)

plt.plot(xVals, constant(xVals, a3), c="g", label=f"Constant fit ($60^o$):  $\\chi_{{red}}^2 = {chi3}$, $T=({period3}s \\pm {uncPeriod3})s$" )
plt.errorbar(masses["60"], periods["60"], periodErr, massErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $60^o$ release")
plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableMass/60.pdf")
plt.cla()

#### ALL VALUES PLOT
plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.ylim(yLim)
plt.xlim(xLim)

plt.errorbar(masses["15"], periods["15"], periodErr, massErr, c="b", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $15^o$ release")
plt.errorbar(masses["30"], periods["30"], periodErr, massErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $30^o$ release")
plt.errorbar(masses["60"], periods["60"], periodErr, massErr, c="g", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $60^o$ release")

plt.plot(xVals, constant(xVals, a), c="k", label=f"Constant fit for all samples: $\\chi_{{red}}^2 = {chi}$, $T=({period} \\pm {uncPeriod})s$" )
plt.plot(xVals, constant(xVals, a1), c="b", label=f"Constant fit ($15^o$): $\\chi_{{red}}^2 = {chi1}$, $T=({period1} \\pm {uncPeriod1})s$" )
plt.plot(xVals, constant(xVals, a2), c="r", label=f"Constant fit ($30^o$): $\\chi_{{red}}^2 = {chi2}$, $T=({period2} \\pm {uncPeriod2})s$" )
plt.plot(xVals, constant(xVals, a3), c="g", label=f"Constant fit ($60^o$):  $\\chi_{{red}}^2 = {chi3}$, $T=({period3} \\pm {uncPeriod3})s$" )

plt.legend(loc='lower left', prop={'size': 8})
plt.savefig(f"{directory}/output/variableMass/all.pdf")
plt.cla()
