import pandas as pd
import matplotlib.pyplot as plt
from os import walk, path
from math import floor, log10

def sigFig(x: float, precision: int):
    x = float(x)
    precision = int(precision)

    return round(x, -int(floor(log10(abs(x)))) + (precision - 1))


def formatValue(inputString):
    if "mV" in inputString:
        return '{:.0f}'.format(round(float(inputString.split("mV")[0]), -1))  + "\\pm 10\\unit{mV}"
    elif "V" in inputString:
        return '{:.2f}'.format(round(float(inputString.split("V")[0]), 2))  + "\\pm 0.01\\unit{V}"
    elif "No edges" in inputString:
        return "No Edges"
    else:
        return inputString

directory = path.dirname(path.realpath(__file__))

experiments = {}

# for fileName in next(walk(f"{directory}/oscilloscopeData/csv"), (None, None, []))[2]:
#     fileName = fileName.strip(".csv")
#     num, experiment, *varNames = fileName.split('-')

#     if experiment in experiments:
#         experiments[experiment] += 1
#     else:
#         experiments[experiment] = 0

#     filePath = f"{directory}/oscilloscopeData/csv/{fileName}.csv"
#     data = pd.read_csv(filePath)

#     ch1Active = "1" in data.columns
#     ch2Active = "2" in data.columns

#     x_axis = pd.to_numeric(data['x-axis'][1:], errors='coerce')

#     if ch1Active:
#         plt.xlabel('Time (seconds)')
#         plt.ylabel('Voltage (Volts)')
#         plt.grid(True)
#         plt.tight_layout()

#         label = varNames[0]
#         plt.title(f'Voltage Measurements Over Time Channel 1 ({label})')

#         ch1 = pd.to_numeric(data['1'][1:], errors='coerce')
#         plt.plot(x_axis, ch1, label="Channel 1")

#         plt.savefig(f"{directory}/output/{experiment}/{num}--ch1.png")
#         plt.savefig(f"{directory}/../latex/figures/{experiment}/{num}--ch1.png")

#         plt.cla()


#     if ch2Active:
#         plt.xlabel('Time (seconds)')
#         plt.ylabel('Voltage (Volts)')
#         plt.grid(True)
#         plt.tight_layout()

#         label = (ch1Active and ch2Active and varNames[1]) or varNames[0]
#         plt.title(f'Voltage Measurements Over Time Channel 2 ({label})')

#         ch2 = pd.to_numeric(data['2'][1:], errors='coerce')
#         plt.plot(x_axis, ch2, label="Channel 2")

#         plt.savefig(f"{directory}/output/{experiment}/{num}--ch2.png")
#         plt.savefig(f"{directory}/../latex/figures/{experiment}/{num}--ch2.png")
#         plt.cla()



for dirName in next(walk(f"{directory}/oscilloscopeData/txt"), (None, None, []))[1]:
    minVal = 1000
    for fileName in next(walk(f"{directory}/oscilloscopeData/txt/{dirName}"), (None, None, []))[2]:
        if ".txt" in fileName:
            num = int(fileName.strip(".txt").split("_")[1])

            if minVal > num:
                minVal = num

    tableRows=[]
    for fileName in next(walk(f"{directory}/oscilloscopeData/txt/{dirName}"), (None, None, []))[2]:
        if ".txt" not in fileName:
            break

        print(dirName, fileName)

        num = int(fileName.strip(".txt").split("_")[1]) - minVal + 1

        with open(f"{directory}/oscilloscopeData/txt/{dirName}/{fileName}", "r") as file:
            ch1Dc = ""
            ch1Ac = ""
            ch2Dc = ""
            ch2Ac = ""

            key, data = file.read().split("MEASUREMENTS")

            ch1Name=None
            ch2Name=None
            key = key.strip("\n").split("\n")

            for line in key:
                if "CH1" in line:
                    ch1Name=line.lstrip("CH1: ")
                if "CH2" in line:
                    ch2Name=line.lstrip("CH2: ")

            for line in data.strip("\n").split("\n"):

                if "AC(2)" in line:
                    ch2Ac = line.split(", Cur ")[1]

                elif "(2)" in line:
                    ch2Dc = line.split(", Cur ")[1]

                elif "AC(1)" in line:
                    ch1Ac = line.split(", Cur ")[1]

                elif "(1)" in line:
                    ch1Dc = line.split(", Cur ")[1]
            if ch1Dc == "No edges" or ch2Dc == "No edges":
                print(ch1Dc, ch2Dc)

            if ch1Name:
                tableRows.append(f"        ${ch1Name}$ & ${formatValue(ch1Ac)}$ & ${formatValue(ch1Dc)}$ \\\\\n")
            if ch2Name:
                tableRows.append(f"        ${ch2Name}$ & ${formatValue(ch2Ac)}$ & ${formatValue(ch2Dc)}$ \\\\\n")

        tableRows.sort()

        with open(f"{directory}/../latex/data/{dirName}.tex", "w") as writeFile:
            writeFile.write("\\begin{figure}[H]")
            writeFile.write("    \\centering")
            writeFile.write("    \\begin{tabular}{|l|c|c|}\n")
            writeFile.write("        \\hline\n")
            writeFile.write("        Measured Value & AC RMS & DC RMS \\\\\n")
            writeFile.write("        \\hline\n")
            writeFile.writelines(tableRows)
            writeFile.write("        \\hline\n")
            writeFile.write("    \\end{tabular}")
            writeFile.write(f"    \\caption{{Oscilloscope measured voltages for experiment {dirName}}}")
            writeFile.write("\\end{figure}")




