import clr
import os

clr.AddReference(os.getcwd() + "/src/dikerneldll/" + "DiKErnel.Integration.dll")
from DiKErnel.Integration import CalculationInputBuilder


class DiKernelInput:
    def __init__(self, dikeOrientation):
        self.inputBuilder = CalculationInputBuilder(dikeOrientation)

    def AddProfile(self, profileCoordinates):
        pass

    def AddHydraulicConditions(self, timeSteps, waterLevels, waveHeights, wavePeriods, waveAngles):
        pass

    def AddOutputPoints(self, outputLocations):
        pass
