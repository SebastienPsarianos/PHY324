import pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2
import textwrap

from utilities import *


font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 22}
rc('font', **font)
# This changes the fonts for all graphs to make them bigger.

with open(f"{directory}/rawData/calibration_p3.pkl","rb") as file:
    calibration_data=pickle.load(file)

with open(f"{directory}/rawData/signal_p3.pkl","rb") as file:
    signal_data=pickle.load(file)

pulse_template = pulse_shape(20,80)
for itrace in range(10):
    plt.plot(calibration_data['evt_%i'%itrace], alpha=0.3)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel('Time ($\\mu s$)')
plt.ylabel('Readout (V)')
plt.savefig(f"{directory}/figures/pulses_cal.png", bbox_inches='tight')
plt.savefig(f"{directory}/../latex/figures/pulses_cal.png", bbox_inches='tight')
plt.cla()

pulse_template = pulse_shape(20,80)
for itrace in range(10):
    plt.plot(signal_data['evt_%i'%itrace], alpha=0.3)

plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
plt.xlabel('Time ($\\mu s$)')
plt.ylabel('Readout (V)')
plt.savefig(f"{directory}/figures/pulses_signal.png", bbox_inches='tight')
plt.savefig(f"{directory}/../latex/figures/pulses_signal.png", bbox_inches='tight')
plt.cla()

pulse_template = pulse_shape(20,80)
plt.plot(pulse_template, label='Pulse Template', color='r')
plt.xlabel('Time ($\\mu s$)')
plt.ylabel('Readout (V)')
plt.savefig(f"{directory}/figures/pulses_sim.png", bbox_inches='tight')
plt.savefig(f"{directory}/../latex/figures/pulses_sim.png", bbox_inches='tight')
plt.cla()

amp1=np.zeros(1000)
amp2=np.zeros(1000)
area1=np.zeros(1000)
area2=np.zeros(1000)
area3=np.zeros(1000)
pulse_fit=np.zeros(1000)

plotData = []
for ievt in range(1000):
    sample = calibration_data['evt_%i'%ievt]

    amp1[ievt] = amp1Estimator(sample)
    amp2[ievt] = amp2Estimator(sample)

    area1[ievt] = area1Estimator(sample)
    area2[ievt] = area2Estimator(sample)
    area3[ievt] = area3Estimator(sample)

    pulse_fit[ievt] = pulseFitEstimator(sample)


energyEstimators = [
    ("1", "Maximum - Minimum signal", "amp1", 20, (.2,.4), amp1),
    ("2", "Maximum - Minimum signal with mean signal in pre pulse region subtracted", "amp2",  20, (.2,.4), amp2),
    ("3", "Mean signal measured in entire sample", "area1", 20, (-.05, .05), area1),
    ("4", "Mean signal measured in entire sample with mean signal in pre pulse region subtracted", "area2", 30, (-.01, .025), area2),
    ("5", "Mean signal during 100$\mu s$ following trigger with mean signal in pre pulse region subtracted", "area3", 32, (.125, .225), area3),
    ("6", "Amplitude of theoretical pulse model fit", "pulseFit",  35, (.1, .3), pulse_fit),
]


plotValues = open(f"{directory}/../latex/plotValues.tex", "w")
plotValues.write("\\begin{center}\n\\begin{tabular}[pos]{|l|c|c|c|c|c|}\n		\hline\n		\\textbf{Method}&\\textbf{Energy Resolution}&\\textbf{Bins}&\\textbf{Calibration Factor}&\\textbf{$\chi^2$ Prob}\\\\\n		\hline\n")

convFactors = {}

for methodName, title, fileName, numBins, binRange, energyValues in energyEstimators:
    with open(f"{directory}/energyEstimators/{fileName}Data.csv", "w") as estimatorValues:
        for i in range(len(energyValues)):
            estimatorValues.write(f"{i},{energyValues[i]};\n")

    xlimits = getXLimits(binRange)

    #### Histogram Binning
    bins, binEdges, _ = plt.hist(energyValues, bins=numBins, range=binRange, color='k', histtype='bar', label='Data')
    binCenters = 0.5*(binEdges[1:]+binEdges[:-1])

    largestBin = max(range(len(bins)), key=bins.__getitem__)

    #### Labels / Ranges
    plt.xlabel(textwrap.fill(f"{title} (mV)", 30))
    plt.ylabel('Events / %2.2f mV'%((binRange[-1]-binRange[0])/numBins));
    plt.xlim(*xlimits)

    #### Error Bars
    sig = np.sqrt(bins)
    sig=np.where(sig==0, 1, sig)
    plt.errorbar(binCenters, bins, yerr=sig, fmt='none', c='r', capsize=3, label="uncertainty")
    #### Gaussian Fit
    fitVars, pcov = curve_fit(myGauss, binCenters,  bins, sigma = sig, p0=(bins[largestBin], binCenters[largestBin], 0.1 * (binRange[1] - binRange[0]), 0), absolute_sigma=True)

    bins_fit = myGauss(binCenters, *fitVars)

    #### Calculating Chi Squared
    chiSquared = np.sum( ((bins - bins_fit)/sig )**2)

    dof = numBins - len(fitVars)

    #### Smooth Best Fit Line
    xBestFit = np.linspace(binEdges[0], binEdges[-1], 1000)
    yBestFit = myGauss(xBestFit, *fitVars)

    #### Plotting
    fontsize=18
    plt.plot(xBestFit, yBestFit, label='Fit')

    plt.legend(loc=1, fontsize="15")
    plt.savefig(f"{directory}/figures/{fileName}.png", bbox_inches='tight')
    plt.savefig(f"{directory}/../latex/figures/{fileName}.png", bbox_inches='tight')

    plt.cla()


    ##########################
    #### Post Calibration ####
    ##########################

    conversionFactor = 10 / fitVars[1]
    convFactors[methodName] = conversionFactor

    energyValues_cal = energyValues * conversionFactor
    binRange_cal=(binRange[0] * conversionFactor, binRange[1] * conversionFactor)

    xlimits_cal = getXLimits(binRange_cal)

    #### Histogram Binning
    bins_cal, binEdges_cal, _ = plt.hist(energyValues_cal, bins=numBins, range=binRange_cal, color='k', histtype='bar', label='Data')
    binCenters_cal = 0.5*(binEdges_cal[1:]+binEdges_cal[:-1])
    largestBin_cal = max(range(len(bins_cal)), key=bins_cal.__getitem__)

    #### Labels / Ranges
    plt.xlabel(textwrap.fill(f"{title} (mV)", 30))
    plt.ylabel('Events / %2.2f mV'%((binRange_cal[-1]-binRange_cal[0])/numBins));
    plt.xlim(*xlimits_cal)

    #### Error Bars
    sig_cal = np.sqrt(bins_cal)
    sig_cal=np.where(sig_cal==0, 1, sig_cal)
    plt.errorbar(binCenters_cal, bins_cal, yerr=sig_cal, fmt='none', c='r', capsize=3, label="uncertainty")

    #### Gaussian Fit
    fitVars_cal, pcov_cal = curve_fit(myGauss, binCenters_cal,  bins_cal, sigma = sig_cal, p0=(bins_cal[largestBin_cal], binCenters_cal[largestBin_cal], 0.1 * (binRange_cal[1] - binRange_cal[0]), 0), absolute_sigma=True)
    binsFit_cal = myGauss(binCenters_cal, *fitVars_cal)

    #### Calculating Chi Squared
    chiSquared_cal = np.sum( ((bins_cal - binsFit_cal)/sig_cal )**2)
    dof_cal = numBins - len(fitVars_cal)

    #### Smooth Best Fit Line
    xBestFit_cal = np.linspace(binEdges_cal[0], binEdges_cal[-1], 1000)
    yBestFit_cal = myGauss(xBestFit_cal, *fitVars_cal)

    #### Labels / Ranges
    plt.xlabel(textwrap.fill(f"{title} (Calibrated Energy Estimate) (KeV)", 35))
    plt.ylabel('Events / %2.2f KeV'%((binRange_cal[-1]-binRange_cal[0])/numBins));
    plt.xlim(xlimits_cal[0], xlimits_cal[1])

    #### Plotting
    fontsize=18
    plt.plot(xBestFit_cal, yBestFit_cal, label='Fit')
    plt.legend(loc=1, fontsize="15")
    plt.savefig(f"{directory}/figures/{fileName}--calibrated.png", bbox_inches='tight')
    plt.savefig(f"{directory}/../latex/figures/{fileName}--calibrated.png", bbox_inches='tight')
    plt.cla()
    plotValues.write(f"		\\textbf{{{methodName}}}&${sigFig(fitVars_cal[2], 3)}\\unit{{KeV}}$&${numBins}$&${sigFig(conversionFactor, 3)}\\unit{{ {{KeV}} \\per{{mV}} }}$&{sigFig((1-chi2.pdf(chiSquared_cal, dof_cal)) * 100, 3)}\\%\\\\\n")



plotValues.write("		\\hline\n\\end{tabular}\n\\end{center}")
plotValues.close()


print("#####################")
print("Signal Analysis")
print("#####################")



area3Sig=np.zeros(1000)
for ievt in range(1000):
    area3Sig[ievt] = area3Estimator(signal_data['evt_%i'%ievt])

energyEstimators = [
        ("Integral 3", "Calibrated energy estimations for sample data (KeV)", "area3", 32, (.125, .225), area3Sig),
]

for methodName, title, fileName, numBins, binRange, energyValues in energyEstimators:

    conversionFactor = convFactors["5"]

    energyValues_cal = energyValues * conversionFactor
    binRange_cal = (0,20)
    xlimits_cal = getXLimits(binRange_cal)

    numBins=31

    #### Histogram Binning
    bins_cal, binEdges_cal, _ = plt.hist(energyValues_cal, bins=numBins, range=binRange_cal, color='k', histtype='bar', label='Data')
    binCenters_cal = 0.5*(binEdges_cal[1:]+binEdges_cal[:-1])
    largestBin_cal = max(range(len(bins_cal)), key=bins_cal.__getitem__)

    #### Labels / Ranges
    plt.xlabel(textwrap.fill(f"{title} (mV)", 30))
    plt.ylabel('Events / %2.2f mV'%((binRange_cal[-1]-binRange_cal[0])/numBins));
    plt.xlim(*xlimits_cal)

    #### Error Bars
    sig_cal = np.sqrt(bins_cal)
    sig_cal=np.where(sig_cal==0, 1, sig_cal)
    plt.errorbar(binCenters_cal, bins_cal, yerr=sig_cal, fmt='none', c='r', capsize=3, label="uncertainty")

    ### Gaussian Fit
    fitVars_cal, pcov_cal = curve_fit(myExp,
                                    binCenters_cal,
                                    bins_cal,
                                    sigma = sig_cal,
                                    p0=((bins_cal[largestBin_cal]),
                                        5,
                                        0),
                                    absolute_sigma=True)

    binsFit_cal = myExp(binCenters_cal, *fitVars_cal)

    #### Calculating Chi Squared
    chiSquared_cal = np.sum( ((bins_cal - binsFit_cal)/sig_cal )**2)
    dof_cal = numBins - len(fitVars_cal)

    #### Smooth Best Fit Line
    xBestFit_cal = np.linspace(binEdges_cal[0], binEdges_cal[-1], 1000)
    yBestFit_cal = myExp(xBestFit_cal, *fitVars_cal)


    #### Labels / Ranges
    plt.xlabel(textwrap.fill(f"{title}", 35))
    plt.ylabel('Events / %2.2f KeV'%((binRange_cal[-1]-binRange_cal[0])/numBins));
    plt.xlim(xlimits_cal[0], xlimits_cal[1])

    ### Plotting
    fontsize=18

    plt.plot(xBestFit_cal, yBestFit_cal, label='Fit')
    plt.legend(loc=1, fontsize="15")
    plt.savefig(f"{directory}/sampleTest/{fileName}.png", bbox_inches='tight')
    plt.savefig(f"{directory}/../latex/figures/signalAnalysis--calibrated.png", bbox_inches='tight')


    plt.cla()
    print(sigFig(fitVars_cal[0], 3))
    print(sigFig(fitVars_cal[1], 3))
    print(sigFig(fitVars_cal[2], 3))
    print(sigFig(chiSquared_cal/dof_cal, 3))
    print("chiSqared Probability",sigFig( (1-chi2.pdf(chiSquared_cal, dof_cal)) * 100, 3) )
