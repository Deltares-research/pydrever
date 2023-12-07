import sys
import os
import numpy

sys.path.append(os.getcwd() + "\src")
sys.path.append(os.getcwd() + "\src\dikerneldll")

from dikernelinput import (
    DikernelInput,
    DikeSchematization,
    HydraulicInput,
)
from dikerneloutputlocations import (
    GrassWaveImpactOutputLocation,
)
from toplayertypes import TopLayerType
from dikernel import Dikernel

xPositions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
zPositions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
dikeSchematization = DikeSchematization(xPositions, zPositions, roughnesses, 25.0, 45.0)
timeSteps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
# timeSteps = list(numpy.array(timeSteps) * 100.0)
waterLevels = [1.5, 2.3, 3.5, 3.2, 2.4]
waveHeights = [3.5, 3.9, 4.2, 4.1, 2.8]
wavePeriods = [8.0, 8.0, 8.0, 8.0, 8.0]
waveAngles = [60.0, 70.0, 80.0, 90.0, 100.0]
hydraulicInput = HydraulicInput(timeSteps, waterLevels, waveHeights, wavePeriods, waveAngles)

input = DikernelInput(90.0, hydraulicInput, dikeSchematization)

input.OutputLocations = [
    GrassWaveImpactOutputLocation(41.1, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(41.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(42.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(42.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(43.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(43.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocation(44.0, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocation(44.5, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocation(44.99, 0.0, TopLayerType.GrassClosedSod),
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
else:
    for message in kernel.ValidationMessages:
        print(message)
