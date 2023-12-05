import clr

clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Integration.dll")
clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Core.dll")

from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutputLocation
from dikernelinputparser import DikernelInputParser


from DiKErnel.Core import Calculator
from DiKErnel.Core.Data import LocationDependentOutput


class Dikernel:
    @staticmethod
    def run(dikernelInput: DikernelInput) -> list[DikernelOutputLocation]:
        cInput = DikernelInputParser.ConvertToCInput(dikernelInput)
        calculator = Calculator(cInput)
        calculator.WaitForCompletion()
        return Dikernel.ConvertToDikernelOutput(calculator.Result.Data)

    @staticmethod
    def ConvertToDikernelOutput(cOutput) -> list[DikernelOutputLocation]:
        outputLocations = []
        for cOutputLocation in cOutput.LocationDependentOutputItems:
            outputLocations.append(Dikernel.__createOutputLocation(cOutputLocation))
        return outputLocations

    @staticmethod
    def __createOutputLocation(cOutputLocation: LocationDependentOutput):
        momentOfFailureItem = next(
            (item for item in cOutputLocation.TimeDependentOutputItems if item is not None), None
        )
        momentOfFailure = momentOfFailureItem.TimeOfFailure if not None else None
        damageDevelopment = list[float]()
        for cItem in cOutputLocation.TimeDependentOutputItems:
            damageDevelopment.append(cItem.Damage)

        output = DikernelOutputLocation(momentOfFailure, damageDevelopment)

        return output
