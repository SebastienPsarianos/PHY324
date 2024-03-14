import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from utilities import sqrt, sigFig, periodErr, lengthErr, sizeInfo, redChiSquared

directory = os.path.dirname(os.path.abspath(__file__))

lengthData = {
    "19": 19.0,
    "31": 31.2,
    "35": 35.5
}

lengths = {
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
with open(f"{directory}/data/length/variedLength.csv") as timeData:
    samples = [([y for y in line.strip('\n').split(':')[0].split(',') ], ([x for x in line.strip('\n').split(':')[1].split('|')[0].split(',') if x != ""], [x for x in line.strip('\n').split(':')[1].split('|')[1].split(',') if x != ""])) for line in timeData.readlines()]
    for (lengthCat, angle), (intervalsOne, intervalsTwo) in samples:
        length = (lengthData[lengthCat] + (sizeInfo["200g"].height / 2 + sizeInfo["200g"].hookLength))/100

        for i in range(len(intervalsOne) - 1):
            periods[angle] = np.append(periods[angle], (int(intervalsOne[i+1]) - int(intervalsOne[i])) / 30)
            lengths[angle] = np.append(lengths[angle], length)


        for i in range(len(intervalsTwo) - 1):
            periods[angle] = np.append(periods[angle], (int(intervalsTwo[i+1]) - int(intervalsTwo[i])) / 30)
            lengths[angle] = np.append(lengths[angle], length)


#################################
#### Uncertainty Propagation ####
#################################
allLengths = np.concatenate((lengths["15"], lengths["30"], lengths["60"]), 0)
allPeriods = np.concatenate((periods["15"], periods["30"], periods["60"]), 0)

#################
#### Fitting ####
#################
a, pcov = curve_fit(sqrt, allLengths, allPeriods)
a1, pcov1 = curve_fit(sqrt, lengths["15"], periods["15"])
a2, pcov2 = curve_fit(sqrt, lengths["30"], periods["30"])
a3, pcov3 = curve_fit(sqrt, lengths["60"], periods["60"])

chi = sigFig(redChiSquared(allPeriods, sqrt(allLengths, a), periodErr, len(allLengths) -  1),4)
chi1 = sigFig(redChiSquared(periods["15"], sqrt(lengths["15"], a1), periodErr, len(lengths["15"]) -  1),4)
chi2 = sigFig(redChiSquared(periods["30"], sqrt(lengths["30"], a2), periodErr, len(lengths["30"]) -  1),4)
chi3 = sigFig(redChiSquared(periods["60"], sqrt(lengths["60"], a3), periodErr, len(lengths["60"]) -  1),4)

fitValue = sigFig(a,4)
fitUnc = sigFig(np.sqrt(pcov[0][0]), 1)

fitValue1 = sigFig(a1,4)
fitUnc1 = sigFig(np.sqrt(pcov1[0][0]), 1)

fitValue2 = sigFig(a2,4)
fitUnc2 = sigFig(np.sqrt(pcov2[0][0]), 1)

fitValue3 = sigFig(a3,4)
fitUnc3 = sigFig(np.sqrt(pcov3[0][0]), 1)

##################
#### Plotting ####
##################
xLabel = "Measured distance between pendulum pivot and approximate center of mass (m)"
yLabel = "Period of oscillation (s)"
yLim = (0.5, 1.5)
xLim = (.2, .5)
xVals = np.linspace(*xLim, 100)


#### 15 DEGREE PLOT
plt.title("")
plt.xlabel(xLabel)
plt.ylabel(yLabel)
#
plt.ylim(yLim)
plt.xlim(xLim)

plt.errorbar(lengths["15"], periods["15"], xerr=lengthErr, yerr=periodErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $15^o$ release")
plt.plot(xVals, sqrt(xVals, a1), c="b", label=f"Square root fit ($15^o$): $\\chi_{{red}}^2 = {chi1}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue1} \\pm {fitUnc1})\\frac{{s}}{{\sqrt{{m}}}}$")

plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableLength/15.pdf")
plt.cla()


#### 30 DEGREE PLOT
plt.title("")
plt.xlabel(xLabel)
plt.ylabel(yLabel)

plt.ylim(yLim)
plt.xlim(xLim)

plt.errorbar(lengths["30"], periods["30"], xerr=lengthErr, yerr=periodErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $30^o$ release")
plt.plot(xVals, sqrt(xVals, a2), c="r", label=f"Square root fit ($30^o$): $\\chi_{{red}}^2 = {chi2}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue2} \\pm {fitUnc2})\\frac{{s}}{{\sqrt{{m}}}}$")

plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableLength/30.pdf")
plt.cla()


#### 60 DEGREE PLOT
plt.title("")
plt.xlabel(xLabel)
plt.ylabel(yLabel)

plt.ylim(yLim)
plt.xlim(xLim)

plt.errorbar(lengths["60"], periods["60"], xerr=lengthErr, yerr=periodErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $60^o$ release")
plt.plot(xVals, sqrt(xVals, a3), c="g", label=f"Square root fit ($60^o$): $\\chi_{{red}}^2 = {chi3}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue3} \\pm {fitUnc3})\\frac{{s}}{{\sqrt{{m}}}}$")

plt.legend(loc='lower left')
plt.savefig(f"{directory}/output/variableLength/60.pdf")
plt.cla()

#### ALL VALUES PLOT
plt.title("")

plt.xlabel(xLabel)
plt.ylabel(yLabel)
plt.ylim(yLim)
plt.xlim(xLim)

plt.errorbar(lengths["15"], periods["15"], xerr=lengthErr, yerr=periodErr, c="b", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $15^o$ release")
plt.errorbar(lengths["30"], periods["30"], xerr=lengthErr, yerr=periodErr, c="r", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $30^o$ release")
plt.errorbar(lengths["60"], periods["60"], xerr=lengthErr, yerr=periodErr, c="g", ls="", marker=".", capsize=3, ecolor="k", label="Pendulum periods for $60^o$ release")

plt.plot(xVals, sqrt(xVals, a), c="k", label=f"Square root fit (all samples): $\\chi_{{red}}^2 = {chi}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue} \\pm {fitUnc})\\frac{{s}}{{\sqrt{{m}}}}$")
plt.plot(xVals, sqrt(xVals, a1), c="b", label=f"Square root fit ($15^o$): $\\chi_{{red}}^2 = {chi1}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue1}\\pm {fitUnc1}) \\frac{{s}}{{\sqrt{{m}}}}$")
plt.plot(xVals, sqrt(xVals, a2), c="r", label=f"Square root fit ($30^o$): $\\chi_{{red}}^2 = {chi2}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue2}  \\pm {fitUnc2})\\frac{{s}}{{\sqrt{{m}}}}$")
plt.plot(xVals, sqrt(xVals, a3), c="g", label=f"Square root fit ($60^o$): $\\chi_{{red}}^2 = {chi3}$, $\\frac{{2\\pi}}{{\sqrt {{g}}}} = ({fitValue3 } \\pm {fitUnc3}) \\frac{{s}}{{\sqrt{{m}}}}$")

plt.legend(loc='lower left', prop={'size': 7})
plt.savefig(f"{directory}/output/variableLength/all.pdf")
plt.cla()
