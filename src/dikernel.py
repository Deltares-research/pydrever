from dikernelcreferences import *
from dikernelinput import DikernelInput, HydraulicInput
from dikerneloutput import DikernelOutputLocation
from dikernelinputparser import DikernelInputParser
from dikerneloutputparser import DikernelOutputParser
import numpy as numpy


class Dikernel:
    def __init__(self, dikernelInput: DikernelInput):
        self.Input: DikernelInput = dikernelInput
        self.Output: list[DikernelOutputLocation] = None
        self.ValidationMessages: list[str] = list[str]()
        self.__cInput = None
        self.__cOutput = None
        self.__cValidationResult = None

    def validate(self) -> bool:
        if not self.__validateinputdata():
            return False

        self.__cInput = DikernelInputParser.parsedikernelinput(self.Input.getruninput())
        if self.__cInput is None:
            self.ValidationMessages.append("Could not parse input")
            return False

        self.__cValidationResult = Validator.Validate(self.__cInput)
        self.ValidationMessages.extend(
            list(i.Message for i in self.__cValidationResult.Events)
        )

        return self.__cValidationResult.Successful and int(
            self.__cValidationResult.Data
        ) == int(ValidationResultType.Successful)

    def run(self) -> bool:
        try:
            calculator = Calculator(self.__cInput)
            calculator.WaitForCompletion()

            self.__cOutput = calculator.Result

            xPositions = list(
                location.XPosition for location in self.Input.OutputLocations
            )
            self.Output = DikernelOutputParser.parsedikerneloutput(
                self.__cOutput.Data, xPositions
            )

            return (
                self.__cOutput is not None
                and self.__cOutput.Successful
                and int(calculator.CalculationState)
                == int(CalculationState.FinishedSuccessfully)
            )
        except:
            return False

    def __validateinputdata(self) -> bool:
        if self.Input is None:
            self.ValidationMessages.append("Specify input first")
            return False

        result = True
        if self.Input.HydraulicInput is None:
            self.ValidationMessages.append("Hydraulic input must be specified.")
            result = False
        elif (
            self.Input.HydraulicInput.TimeSteps is None
            or len(self.Input.HydraulicInput.TimeSteps) < 2
        ):
            self.ValidationMessages.append(
                "At least two time steps need to be specified in the hydraulic input."
            )
            result = False

        if self.Input.DikeSchematization is None:
            self.ValidationMessages.append("Dike schematization must be specified")
            result = False
        if (
            self.Input.DikeOrientation is None
            or self.Input.DikeOrientation < 0
            or self.Input.DikeOrientation > 360
        ):
            self.ValidationMessages.append(
                "Dike orientation must be specified as a number between 0 and 360 degrees."
            )
            result = False
        if self.Input.OutputLocations is None or len(self.Input.OutputLocations) < 1:
            self.ValidationMessages.append(
                "At least one outputlocation needs to be specified."
            )
            result = False
        if self.Input.StartTime is not None and self.Input.StartTime > numpy.max(
            self.Input.HydraulicInput.TimeSteps
        ):
            self.ValidationMessages.append(
                "Start time should not exceed the specified hydraulic boundary conditions."
            )
            result = False
        if (
            self.Input.OutputTimeSteps is not None
            and len(self.Input.OutputTimeSteps) > 0
        ):
            minimumOutputTime = numpy.min(self.Input.OutputTimeSteps)
            if (
                self.Input.StartTime is not None
                and minimumOutputTime < self.Input.StartTime
            ):
                self.ValidationMessages.append(
                    "Specified output time steps should all be greater than the specified start time."
                )
                result = False
            if self.Input.HydraulicInput is not None and minimumOutputTime < numpy.min(
                self.Input.HydraulicInput.TimeSteps
            ):
                self.ValidationMessages.append(
                    "Specified output time steps should all be greater than the minimum specified time step of the hydraulic conditions."
                )
                result = False
            maximumOutputTime = numpy.max(self.Input.OutputTimeSteps)
            if self.Input.HydraulicInput is not None and maximumOutputTime > numpy.max(
                self.Input.HydraulicInput.TimeSteps
            ):
                self.ValidationMessages.append(
                    "Specified output time steps should not be greater than the maximum specified time step of the hydraulic conditions."
                )
                result = False
        return result
