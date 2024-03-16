import matplotlib.pyplot as plt

from utils import sigFig
from waterData import *
from glycerineData import *

labelG = f"Best fit for Equation 3 (Low $R_e$ approximation):\n\
$\\chi_{{red}}^2={sigFig(chi2G,4)}$\n\
$2\\rho_s g /\\  9 \\eta={sigFig(terminalFitG[0],3)}\\pm {sigFig(terminalFitG_Unc,1)}$"

labelW = f"Best fit for Equation 3 (High $R_e$ approximation):\n\
$\\chi_{{red}}^2={sigFig(chi2W,4)}$\n\
$\sqrt{{8 \\rho_sg/3\\rho C_d }}={sigFig(terminalFitW[0],4)}\\pm {sigFig(terminalFitW_Unc,1)}$"


plt.errorbar(measuredSizeG,
             terminalVG,
             xerr=0.001,
             yerr=terminalVG_Unc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Calculated terminal velocity",
             markersize=3
            )

plt.plot(xValuesG, squaredFit(xValuesG, *terminalFitG), label=labelG)
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.title("", wrap=True)
plt.savefig(f"{directory}/output/terminalPlotG.pdf")
plt.cla()

plt.scatter(measuredSizeG, terminalVG - squaredFit(measuredSizeG, *terminalFitG), s=10, c="r")
plt.axhline(y = 0, color = 'k', linestyle = 'dashed')
plt.savefig(f"{directory}/output/terminalPlotGRes.pdf")
plt.ylabel("Resdiuals")
plt.xlabel("Terminal Velocity (mm/s)")
plt.cla()
###############
#### WATER ####
###############


plt.errorbar(measuredSizeW,
             terminalVW,
             xerr=0.01,
             yerr=terminalVW_Unc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Calculated terminal velocity"
            )

plt.plot(xValuesW,
         sqrtFit(xValuesW, *terminalFitW),
         label=labelW)
plt.legend()
plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/waterMaxGraph.pdf")
plt.cla()

plt.scatter(measuredSizeW, terminalVW - sqrtFit(measuredSizeW, *terminalFitW), s=10, c="r")
plt.axhline(y = 0, color = 'k', linestyle = 'dashed')
plt.savefig(f"{directory}/output/terminalPlotWRes.pdf")
plt.ylabel("Resdiuals")
plt.xlabel("Terminal Velocity (mm/s)")
plt.cla()


for speeds, times, name in waterVelocityPlots:
    plt.errorbar(times,
             speeds,
             xerr=0.01,
            #  yerr=waterSecVelUnc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )


    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (mm/s)")
    plt.savefig(f"{directory}/output/test/{name}.pdf")
    plt.cla()