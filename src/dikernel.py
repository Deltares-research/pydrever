from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutputLocation
from dikernelinputparser import DikernelInputParser
from dikerneloutputparser import DikernelOutputParser
from dikernelcreferences import *


class Dikernel:
    def __init__(self, dikernelInput: DikernelInput):
        self.Input: DikernelInput = dikernelInput
        self.__cInput = DikernelInputParser.parsedikernelinput(dikernelInput)
        self.Output: list[DikernelOutputLocation] = None
        self.__cOutput = None

    def validate(self) -> bool:
        # TODO: Validate input with DiKErnel.Core.Validator()
        return True

    def run(self) -> bool:
        try:
            calculator = Calculator(self.__cInput)
            calculator.WaitForCompletion()

            self.__cOutput = calculator.Result

            xPositions = list(location.XPosition for location in self.Input.OutputLocations)
            self.Output = DikernelOutputParser.parsedikerneloutput(self.__cOutput.Data, xPositions)

            return calculator.Result is not None
        except:
            return False
