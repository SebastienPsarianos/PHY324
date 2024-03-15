import matplotlib.pyplot as plt

from utils import redChiSquared, sigFig
from waterData import *
from glycerineData import *


chi2W = redChiSquared(terminalVW, sqrtFit(measuredSizeW, *terminalFitW), terminalVW_Unc, len(terminalVW) - 1)



labelG = f"Best fit for Equation 3 (High $R_e$):\n\
$\\chi_{{red}}^2={sigFig(chi2G,4)}$\n\
$2\\rho_s g /\\  9 \\eta={sigFig(terminalFitG[0],3)}\\pm {sigFig(terminalFitG_Unc,1)}$"
print(labelG)

labelW = f"Best fit for Equation 3 (High $R_e$):\n\
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
             label="Inferred terminal velocity",
             markersize=3
            )



plt.plot(xValuesG, squaredFit(xValuesG, *terminalFitG), label=labelG)
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.title("", wrap=True)
plt.savefig(f"{directory}/output/glycMaxFit.pdf")
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
             label="Inferred terminal velocity"
            )

plt.plot(xValuesW,
         sqrtFit(xValuesW, *terminalFitW),
         label=labelW)
plt.legend()
plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/waterMaxGraph.pdf")
plt.cla()
# plt.errorbar(measuredSizeW,
#              secantVW,
#              xerr=0.01,
#              yerr=secantVW_Unc,
#              linestyle='None',
#              marker = 'o',
#              c='k',
#              ecolor='r',
#              capsize=3,
#              label="Inferred terminal velocity"
#             )

# plt.plot(xValuesW, sqrtFit(xValuesW, *secantFitW), label="Theoretical model fit")
# plt.legend()

# plt.xlabel("Sphere diameter (mm)")
# plt.ylabel("Terminal Velocity (mm/s)")
# plt.savefig(f"{directory}/output/waterSecGraph.pdf")
# plt.cla()


# plt.errorbar(measuredSizeG,
#              secantVG,
#              xerr=0.01,
#              yerr=secantVG_Unc,
#              linestyle='None',
#              marker = 'o',
#              c='k',
#              ecolor='r',
#              capsize=3,
#              label="Inferred terminal velocity"
#             )

# plt.plot(xValuesG, squaredFit(xValuesG, *secantFitG), label="Theoretical model fit")
# plt.legend()

# plt.xlabel("Sphere diameter (mm)")
# plt.ylabel("Terminal Velocity (mm/s)")
# plt.savefig(f"{directory}/output/glycSecFit.pdf")
# plt.cla()

# for speeds, times, name in waterVelocityPlots:
#     plt.errorbar(times,
#              speeds,
#              xerr=0.01,
#             #  yerr=waterSecVelUnc,
#              linestyle='None',
#              marker = 'o',
#              c='k',
#              ecolor='r',
#              capsize=3,
#              label="Inferred terminal velocity"
#             )


#     plt.xlabel("Time (s)")
#     plt.ylabel("Velocity (mm/s)")
#     plt.savefig(f"{directory}/output/test/{name}.pdf")
#     plt.cla()