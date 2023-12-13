from dikernelcreferences import *
from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutputLocation
from dikernelinputparser import DikernelInputParser
from dikerneloutputparser import DikernelOutputParser
import numpy as numpy


class Dikernel:
    def __init__(self, input: DikernelInput):
        self.input: DikernelInput = input
        self.output: list[DikernelOutputLocation] = None
        self.validation_messages: list[str] = list[str]()
        self.__c_input = None
        self.__c_output = None
        self.__c_validation_result = None

    def validate(self) -> bool:
        if not self.__validate_input_data():
            return False

        self.__c_input = DikernelInputParser.parse_dikernel_input(
            self.input.get_run_input()
        )
        if self.__c_input is None:
            self.validation_messages.append("Could not parse input")
            return False

        self.__c_validation_result = Validator.Validate(self.__c_input)
        self.validation_messages.extend(
            list(i.Message for i in self.__c_validation_result.Events)
        )

        return self.__c_validation_result.Successful and int(
            self.__c_validation_result.Data
        ) == int(ValidationResultType.Successful)

    def run(self) -> bool:
        try:
            calculator = Calculator(self.__c_input)
            calculator.WaitForCompletion()

            self.__c_output = calculator.Result

            x_positions = list(
                location.x_position for location in self.input.output_locations
            )
            self.output = DikernelOutputParser.parse_dikernel_output(
                self.__c_output.Data, x_positions
            )

            return (
                self.__c_output is not None
                and self.__c_output.Successful
                and int(calculator.CalculationState)
                == int(CalculationState.FinishedSuccessfully)
            )
        except:
            return False

    def __validate_input_data(self) -> bool:
        if self.input is None:
            self.validation_messages.append("Specify input first")
            return False

        result = True
        if self.input.hydraulic_input is None:
            self.validation_messages.append("Hydraulic input must be specified.")
            result = False
        elif (
            self.input.hydraulic_input.time_steps is None
            or len(self.input.hydraulic_input.time_steps) < 2
        ):
            self.validation_messages.append(
                "At least two time steps need to be specified in the hydraulic input."
            )
            result = False

        if self.input.dike_schematization is None:
            self.validation_messages.append("Dike schematization must be specified")
            result = False
        if (
            self.input.dike_orientation is None
            or self.input.dike_orientation < 0
            or self.input.dike_orientation > 360
        ):
            self.validation_messages.append(
                "Dike orientation must be specified as a number between 0 and 360 degrees."
            )
            result = False
        if self.input.output_locations is None or len(self.input.output_locations) < 1:
            self.validation_messages.append(
                "At least one outputlocation needs to be specified."
            )
            result = False
        if self.input.start_time is not None and self.input.start_time > numpy.max(
            self.input.hydraulic_input.time_steps
        ):
            self.validation_messages.append(
                "Start time should not exceed the specified hydraulic boundary conditions."
            )
            result = False
        if (
            self.input.output_time_steps is not None
            and len(self.input.output_time_steps) > 0
        ):
            minimumOutputTime = numpy.min(self.input.output_time_steps)
            if (
                self.input.start_time is not None
                and minimumOutputTime < self.input.start_time
            ):
                self.validation_messages.append(
                    "Specified output time steps should all be greater than the specified start time."
                )
                result = False
            if (
                self.input.hydraulic_input is not None
                and minimumOutputTime < numpy.min(self.input.hydraulic_input.time_steps)
            ):
                self.validation_messages.append(
                    "Specified output time steps should all be greater than the minimum specified time step of the hydraulic conditions."
                )
                result = False
            maximumOutputTime = numpy.max(self.input.output_time_steps)
            if (
                self.input.hydraulic_input is not None
                and maximumOutputTime > numpy.max(self.input.hydraulic_input.time_steps)
            ):
                self.validation_messages.append(
                    "Specified output time steps should not be greater than the maximum specified time step of the hydraulic conditions."
                )
                result = False
        return result
