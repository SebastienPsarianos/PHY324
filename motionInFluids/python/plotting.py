import matplotlib.pyplot as plt

from data import *

plt.errorbar(glycSizeValues,
             glycSecVel,
             xerr=0.01,
             yerr=glycSecVelUnc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(glycFitXValues, squaredFit(glycFitXValues, *glycMaxFit), label="Theoretical model fit")
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.title("", wrap=True)
plt.savefig(f"{directory}/output/glycMaxFit.pdf")
plt.cla()

plt.errorbar(glycSizeValues,
             glycSecVel,
             xerr=0.01,
             yerr=glycSecVelUnc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(glycFitXValues, squaredFit(glycFitXValues, *glycSecFit), label="Theoretical model fit")
plt.legend()

plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/glycSecFit.pdf")
plt.cla()




###############
#### WATER ####
###############
plt.errorbar(waterSizeValues,
             waterMaxVel,
             xerr=0.01,
             yerr=waterMaxVelUnc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(waterFitXValues, sqrtFit(waterFitXValues,*waterMaxFit), label="Theoretical model fit")
plt.legend()
plt.xlabel("Sphere diameter (mm)")
plt.ylabel("Terminal Velocity (mm/s)")
plt.savefig(f"{directory}/output/waterMaxGraph.pdf")
plt.cla()
plt.errorbar(waterSizeValues,
             waterSecVel,
             xerr=0.01,
             yerr=waterSecVelUnc,
             linestyle='None',
             marker = 'o',
             c='k',
             ecolor='r',
             capsize=3,
             label="Inferred terminal velocity"
            )

plt.plot(waterFitXValues, sqrtFit(waterFitXValues, *waterSecFit), label="Theoretical model fit")
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