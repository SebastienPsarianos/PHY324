import numpy as np
from math import floor, log10
import os
from scipy.optimize import curve_fit

directory = os.path.dirname(os.path.realpath(__file__))

def sigFig(x: float, precision: int):
    x = float(x)
    precision = int(precision)

    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))


def myGauss(x, A, mean, width, base):
    return A*np.exp(-(x-mean)**2/(2*width**2)) + base
# This is my fitting function, a Guassian with a uniform background.

def pulse_shape(t_rise, t_fall):
    xx=np.linspace(0, 4095, 4096)
    yy = -(np.exp(-(xx-1000)/t_rise)-np.exp(-(xx-1000)/t_fall))
    yy[:1000]=0
    yy /= np.max(yy)
    return yy

def fit_pulse(x, A):
    _pulse_template = pulse_shape(20,80)
    xx=np.linspace(0, 4095, 4096)
    return A*np.interp(x, xx, _pulse_template)

def getXLimits(binRange):
    marginWidth = (binRange[1] - binRange[0]) / 20
    return (binRange[0]- marginWidth, binRange[1] + marginWidth)


def testFn(x, A1,mean1,width1,base, A2, mean2, width2):
    return myGauss(x, A1**2,mean1,width1,0) + myGauss(x, A2**2,mean2,width2,0) + base



def amp1Estimator(sample):
    """Implements the first amplitude estimator and converts to mV"""
    return (np.max(sample)  - np.min(sample)) * 1000

def amp2Estimator(sample):
    """Implements the second amplitude estimator and converts to mV"""
    baseline = np.average(sample[:1001])
    return (np.max(sample)  - np.min(sample) - baseline) * 1000


def area1Estimator(sample):
    """Implements the first integral estimator and converts to mV"""
    return (np.mean(sample)) * 1000

def area2Estimator(sample):
    """Implements the second integral estimator and converts to mV"""
    baseline = np.average(sample[:1001])
    return (np.mean(sample) - baseline ) * 1000

def area3Estimator(sample):
    """Implements the third integral estimator and converts to mV"""
    baseline = np.average(sample[:1001])
    return (np.mean(sample[1001:1101]) - baseline ) * 1000

def pulseFitEstimator(sample):
    """Implements the pulse fit estimator and converts to mV"""
    return curve_fit(fit_pulse, np.linspace(0, 4095, 4096), sample )[0] * 1000

def myExp(x, A, dec, base):
    return A * np.exp(-dec * x) + base
