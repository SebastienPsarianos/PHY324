import pickle
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chi2, poisson
from scipy.special import gamma
import textwrap

from utilities import *


font = {'family' : 'DejaVu Sans',
        'weight' : 'normal',
        'size'   : 22}
rc('font', **font)
# This changes the fonts for all graphs to make them bigger.

with open(f"{directory}/rawData/signal_p3.pkl","rb") as file:
    signal_data=pickle.load(file)

def myPoisson(x, A, lmda):
    return A * poisson.pmf(x, lmda)

def myExp(x, A, d, pos):
    return A * np.exp(-(x-pos)*d)

dist=np.zeros(1000)
for ievt in range(1000):
    currentData = signal_data['evt_%i'%ievt]
    dist[ievt] = (np.max(currentData)  - np.min(currentData)) * 1000 * 32.818073822782644

numBins=25

print(max(dist))
bins, binEdges, _ = plt.hist(dist, bins=numBins, range=(3.4,8), color='k', histtype='bar', label='Data')
binCenters = 0.5*(binEdges[1:]+binEdges[:-1])
largestBin = max(range(len(bins)), key=bins.__getitem__)

sig = np.sqrt(bins)
sig=np.where(sig==0, 1, sig)
# plt.errorbar(binCenters, bins, yerr=sig, fmt='none', c='r', capsize=3, label="uncertainty")

lambdaEst = np.sum(bins) / numBins
fitVars, pcov = curve_fit(myExp, binCenters,  bins, (320, 5, 4.5))

xBestFit = np.linspace=(3.4, 11, 1000)
# yBestFit = myExp(xBestFit, 320,1, 4.5)

fontsize=18
# plt.plot(xBestFit, yBestFit, label='Fit')

plt.legend(loc=1, fontsize="15")
plt.savefig(f"{directory}/figures/test.png", bbox_inches='tight')
# plt.savefig(f"{directory}/../latex/figures/test.png", bbox_inches='tight')

plt.cla()

