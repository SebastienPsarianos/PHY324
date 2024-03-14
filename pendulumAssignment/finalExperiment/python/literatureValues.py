import numpy as np
from utilities import sizeInfo, sigFig, sqrtProp

pendulumLength = (30 + sizeInfo["200g"].height/2 + sizeInfo["200g"].hookLength) / 100
pendulumLengthErr = np.sqrt((0.1)**2 + (0.5 * 0.1)**2 + (0.1)**2)/ 100

theoreticalPeriod = sigFig(2 * (np.pi / np.sqrt(9.8)) * np.sqrt(pendulumLength), 4)
periodErr = sigFig(sqrtProp(pendulumLength, pendulumLengthErr), 1)
print(pendulumLength, pendulumLengthErr)

print("Period for decay / angle pendulum:", f"{theoreticalPeriod}+/-{periodErr}")

pendulumLength = (35.5 + sizeInfo["200g"].height/2 + sizeInfo["200g"].hookLength) / 100
pendulumLengthErr = np.sqrt((0.1)**2 + (0.5 * 0.1)**2 + (0.1)**2)/ 100

theoreticalPeriod = sigFig(2 * (np.pi / np.sqrt(9.8)) * np.sqrt(pendulumLength), 4)
periodErr = sigFig(sqrtProp(pendulumLength, pendulumLengthErr), 1)

print("Period for mass pendulum:", f"{theoreticalPeriod}+/-{periodErr}")
