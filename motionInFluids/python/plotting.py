import matplotlib.pyplot as plt

from newUtils import redChiSquared
from waterData import *
from glycerineData import *

plt.errorbar(measuredSizeG,
             secantVG,
             xerr=0.01,
             yerr=secantVG_Unc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(xValuesG, squaredFit(xValuesG, *terminalFitG), label="Theoretical model fit")
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.title("", wrap=True)
plt.savefig(f"{directory}/output/glycMaxFit.pdf")
plt.cla()

plt.errorbar(measuredSizeG,
             secantVG,
             xerr=0.01,
             yerr=secantVG_Unc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(xValuesG, squaredFit(xValuesG, *secantFitG), label="Theoretical model fit")
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/glycSecFit.pdf")
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

plt.plot(xValuesW, sqrtFit(xValuesW, *terminalFitW), label="Theoretical model fit")
plt.legend()
plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/waterMaxGraph.pdf")
plt.cla()
plt.errorbar(measuredSizeW,
             secantVW,
             xerr=0.01,
             yerr=secantVW_Unc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(xValuesW, sqrtFit(xValuesW, *secantFitW), label="Theoretical model fit")
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/waterSecGraph.pdf")
plt.cla()


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