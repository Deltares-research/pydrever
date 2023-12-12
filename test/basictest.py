import sys
import os
import numpy
import matplotlib.pyplot as plt

# TODO: remove packages: pandas, plotly, python-kaleido

sys.path.append(os.getcwd() + "\src")
sys.path.append(os.getcwd() + "\src\dikerneldll")

from dikernelinput import (
    DikernelInput,
    DikeSchematization,
    HydraulicInput,
)
from dikerneloutputlocations import (
    GrassWaveImpactOutputLocationSpecification,
)
from toplayertypes import TopLayerType
from dikernel import Dikernel


def interpolatetimeseries(
    timeSteps: list[float], values: list[float], targetTimeSteps: list[float]
) -> list[float]:
    iargs = 1
    itarget = 1
    targetValues = list[float]()
    while itarget < len(targetTimeSteps):
        if targetTimeSteps[itarget] > timeSteps[iargs] and iargs < len(timeSteps) - 1:
            iargs = iargs + 1
            continue
        targetValues.append(values[iargs - 1])
        itarget = itarget + 1

    return targetValues


xLocationPositions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
zPositions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
dikeSchematization = DikeSchematization(
    xLocationPositions, zPositions, roughnesses, 25.0, 45.0
)
timeSteps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
timeSteps = list(numpy.array(timeSteps) * 0.0001)
outputTimeSteps = numpy.arange(0.0, 12.6, 0.1)
outputTimeSteps = numpy.union1d(timeSteps, outputTimeSteps)
waterLevels = [1.5, 2.3, 3.5, 3.2, 2.4]
waterLevels = list(numpy.array(waterLevels) * 0.8)
waveHeights = [3.5, 3.9, 4.2, 4.1, 2.8]
wavePeriods = [8.0, 8.0, 8.0, 8.0, 8.0]
waveDirections = [60.0, 70.0, 80.0, 90.0, 100.0]

waterLevels2 = interpolatetimeseries(timeSteps, waterLevels, outputTimeSteps)
waveHeights2 = interpolatetimeseries(timeSteps, waveHeights, outputTimeSteps)
wavePeriods2 = interpolatetimeseries(timeSteps, wavePeriods, outputTimeSteps)
waveDirections2 = interpolatetimeseries(timeSteps, waveDirections, outputTimeSteps)
hydraulicInput = HydraulicInput(
    timeSteps, waterLevels, waveHeights, wavePeriods, waveDirections
)


input = DikernelInput(90.0, hydraulicInput, dikeSchematization)
input.StartTime = 0.0
input.OutputTimeSteps = outputTimeSteps

input.OutputLocations = [
    GrassWaveImpactOutputLocationSpecification(41.1, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(41.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(44.0, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.5, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.99, 0.0, TopLayerType.GrassClosedSod),
]

kernel = Dikernel(input)
validationResult = kernel.validate()
if validationResult:
    runresult = kernel.run()
    print("Run was: " + "succesfull" if runresult else "unsuccessfull")
    output = kernel.Output
    print("Number of output locations: " + str(len(output)))
    for location in output:
        print(
            "   "
            + ("Failed" if location.Failed else "Not failed")
            + ", X: "
            + str(location.XPosition)
            + ", Damage level = "
            + str(location.DamageDevelopment[-1])
        )

    fig, axs = plt.subplots(ncols=2, nrows=2)
    fig.suptitle("Hydraulic conditions", fontsize=16)
    axs[0, 0].plot(outputTimeSteps, [None] + waterLevels2, "gx", linestyle="dotted")
    axs[0, 0].plot(timeSteps, [None] + waterLevels, "bo")
    axs[0, 0].set(ylabel="Water level [m]")
    axs[0, 0].grid()
    axs[1, 0].plot(outputTimeSteps, [None] + waveHeights2, "gx", linestyle="dotted")
    axs[1, 0].plot(timeSteps, [None] + waveHeights, "bo")
    axs[1, 0].set(xlabel="Time step [s]", ylabel="Wave height [m]")
    axs[1, 0].grid()
    axs[0, 1].plot(outputTimeSteps, [None] + wavePeriods2, "gx", linestyle="dotted")
    axs[0, 1].plot(timeSteps, [None] + wavePeriods, "bo")
    axs[0, 1].set(ylabel="Wave periods [s]")
    axs[0, 1].grid()
    axs[1, 1].plot(outputTimeSteps, [None] + waveDirections2, "gx", linestyle="dotted")
    axs[1, 1].plot(timeSteps, [None] + waveDirections, "bo")
    axs[1, 1].set(xlabel="Time step [s]", ylabel="Wave angles [degrees]")
    axs[1, 1].grid()
    fig.tight_layout()
    # fig.savefig("C:/Test/testimage.png")

    damagelevels = list(loc.Damage for loc in output)
    xLocationPositions = list(loc.XPosition for loc in output)

    fig2, ax = plt.subplots(ncols=1, nrows=1)
    ax.set(xlabel="Cross-shore position [x]", ylabel="Damage (end of storm)")
    ax.tick_params(axis="y", colors="b")
    ax.yaxis.label.set_color("b")
    plt.axhline(1.0, color="red", linewidth=2.0, linestyle="--")
    ax.grid()
    ax.set_facecolor("None")
    ax.plot(xLocationPositions, damagelevels, color="b")

    ax2 = ax.twinx()
    ax2.set(ylabel="Height [m]")
    ax2.plot(
        dikeSchematization.XPositions,
        dikeSchematization.ZPositions,
        linestyle="solid",
        color="lightgray",
        marker="o",
    )
    ax2.set_facecolor("white")
    ax2.tick_params(axis="y", colors="lightgray")
    ax2.yaxis.label.set_color("lightgray")

    ax.set_zorder(1)
    ax2.set_zorder(0)

    fig2.tight_layout()

    plt.show()
else:
    for message in kernel.ValidationMessages:
        print(message)
