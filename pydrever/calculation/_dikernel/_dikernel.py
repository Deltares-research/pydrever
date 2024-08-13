"""
 Copyright (C) Stichting Deltares 2023-2024. All rights reserved.
 
 This file is part of the dikernel-python toolbox.
 
 This program is free software; you can redistribute it and/or modify it under the terms of
 the GNU Lesser General Public License as published by the Free Software Foundation; either
 version 3 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public License along with this
 program; if not, see <https://www.gnu.org/licenses/>.
 
 All names, logos, and references to "Deltares" are registered trademarks of Stichting
 Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

from pydrever.data import DikernelInput, DikernelOutputLocation
from pydrever.calculation._dikernel._dikernelcreferences import *
import pydrever.calculation._dikernel._dikernelinputparser as _input_parser
import pydrever.calculation._dikernel._dikerneloutputparser as _output_parser
import pydrever.calculation._dikernel._inputservices as _input_services
import pydrever.calculation._dikernel._messagehelper as _message_helper
import numpy as numpy


class Dikernel:
    """
    Class to facilitate calculations with the (C#-typed) Dikernel.
    """

    def __init__(self, input: DikernelInput):
        """
        Initiates an instance of the Dikernel class that can be used to perform a calculation.

        Args:
            input (DikernelInput): The specified input for the calculation.
        """
        self.input: DikernelInput = input
        self.output: list[DikernelOutputLocation] = None
        self.warnings: list[str] = list[str]()
        self.errors: list[str] = list[str]()
        self.__c_input = None
        self.__c_output = None
        self.__c_validation_result = None

    def run(self) -> bool:
        """
        Method to run a calculation.

        Returns:
            bool: Indicating whether the calculation was seccessfull or not.
        """
        if not self.__validate():
            return False

        try:
            calculator = Calculator(self.__c_input)
            calculator.WaitForCompletion()

            self.__c_output = calculator.Result

            warnings, errors = _message_helper.parse_messages(self.__c_output)
            self.warnings.extend(warnings)
            self.errors.extend(errors)

            if (
                not self.__c_output.Successful
                or self.__c_output.Data is None
                or len(self.errors) > 0
            ):
                return False

            x_positions = [
                l.x_position
                for l in _input_services.get_output_locations_from_input(self.input)
            ]
            self.output = _output_parser.parse(self.__c_output.Data, x_positions)

            return (
                self.__c_output is not None
                and self.__c_output.Successful
                and int(calculator.CalculationState)
                == int(CalculationState.FinishedSuccessfully)
            )
        except:
            return False

    def __validate(self) -> bool:
        """
        Calls the validation method of Dikernel to validate the specified input. First this
        method validates part of the specified input in order to convert the input to
        C#-typed input. The C#-typed input is then used to validate with Dikernel.

        Returns:
            bool: The result of validation. In case it is false, validation messages are added to the instance variable "validation_messages" of this class.
        """
        if not self.__validate_input_data():
            return False

        if not self.__convert_input_to_c():
            return False

        return self.__run_kernel_validation()

    def __convert_input_to_c(self) -> bool:
        self.__c_input, warnings, errors = _input_parser.parse(
            _input_services.get_run_input(self.input)
        )

        self.warnings.extend(warnings)
        self.errors.extend(errors)
        if self.__c_input is None or len(self.errors) > 0:
            return False

        return True

    def __run_kernel_validation(self) -> bool:
        self.__c_validation_result = Validator.Validate(self.__c_input)
        warnings, errors = _message_helper.parse_messages(self.__c_validation_result)
        self.warnings.extend(warnings)
        self.errors.extend(errors)

        return self.__c_validation_result.Successful and int(
            self.__c_validation_result.Data
        ) == int(ValidationResultType.Successful)

    def __validate_input_data(self) -> bool:
        """
        Internal method to validate the specified input to avoid problems when converting it to C#.

        Returns:
            bool: True if the specified input meets criteria to be able to convert to C#. In case it is false, the instanve variable "validation_messages" contains information on why validation was not successfull.
        """
        if self.input is None:
            self.errors.append("Specify input first")
            return False

        result = True
        if self.input.hydrodynamic_input is None:
            self.errors.append("Hydrodynamic input must be specified.")
            result = False
        elif (
            self.input.hydrodynamic_input.time_steps is None
            or len(self.input.hydrodynamic_input.time_steps) < 2
        ):
            self.errors.append(
                "At least two time steps need to be specified in the hydrodynamic input."
            )
            result = False

        if self.input.dike_schematization is None:
            self.errors.append("Dike schematization must be specified")
            result = False
        if (
            self.input.dike_schematization.dike_orientation is None
            or self.input.dike_schematization.dike_orientation < 0
            or self.input.dike_schematization.dike_orientation > 360
        ):
            self.errors.append(
                "Dike orientation must be specified as a number between 0 and 360 degrees."
            )
            result = False
        if (
            self.input.output_locations is None or len(self.input.output_locations) < 1
        ) and (
            self.input.output_revetment_zones is None
            or len(self.input.output_revetment_zones) < 1
        ):
            self.errors.append("At least one outputlocation needs to be specified.")
            result = False
        if self.input.start_time is not None and self.input.start_time > numpy.max(
            self.input.hydrodynamic_input.time_steps
        ):
            self.errors.append(
                "Start time should not exceed the specified hydrodynamic boundary conditions."
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
                self.errors.append(
                    "Specified output time steps should all be greater than the specified start time."
                )
                result = False
            if (
                self.input.hydrodynamic_input is not None
                and minimumOutputTime
                < numpy.min(self.input.hydrodynamic_input.time_steps)
            ):
                self.errors.append(
                    "Specified output time steps should all be greater than the minimum specified time step of the hydrodynamic conditions."
                )
                result = False
            maximumOutputTime = numpy.max(self.input.output_time_steps)
            if (
                self.input.hydrodynamic_input is not None
                and maximumOutputTime
                > numpy.max(self.input.hydrodynamic_input.time_steps)
            ):
                self.errors.append(
                    "Specified output time steps should not be greater than the maximum specified time step of the hydrodynamic conditions."
                )
                result = False
        return result
