from dikernelcreferences import *
from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutputLocation
from dikernelinputparser import DikernelInputParser
from dikerneloutputparser import DikernelOutputParser


class Dikernel:
    def __init__(self, dikernelInput: DikernelInput):
        self.Input: DikernelInput = dikernelInput
        self.Output: list[DikernelOutputLocation] = None
        self.__cInput = DikernelInputParser.parsedikernelinput(dikernelInput)
        self.__cOutput = None
        self.__cValidationResult = None

    def validate(self) -> bool:
        if self.__cInput is None:
            return False

        self.__cValidationResult = Validator.Validate(self.__cInput)

        return self.__cValidationResult.Successful and int(self.__cValidationResult.Data) == int(
            ValidationResultType.Successful
        )

    def run(self) -> bool:
        try:
            calculator = Calculator(self.__cInput)
            calculator.WaitForCompletion()

            self.__cOutput = calculator.Result

            xPositions = list(location.XPosition for location in self.Input.OutputLocations)
            self.Output = DikernelOutputParser.parsedikerneloutput(self.__cOutput.Data, xPositions)

            return (
                self.__cOutput is not None
                and self.__cOutput.Successful
                and int(calculator.CalculationState) == int(CalculationState.FinishedSuccessfully)
            )
        except:
            return False
