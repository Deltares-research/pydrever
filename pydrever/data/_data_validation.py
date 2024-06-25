"""
 Copyright (C) Stichting Deltares 2024. All rights reserved.
 
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


def validate_one_of_two_should_be_specified(
    values, first_parameter_name: str, second_parameter_name: str
):
    first_parameter_value = (
        values[first_parameter_name] if first_parameter_name in values else None
    )
    second_parameter_value = (
        values[second_parameter_name] if second_parameter_name in values else None
    )
    if first_parameter_value is not None and second_parameter_value is not None:
        raise ValueError(
            "Either {0} or {1} should be specified.".format(
                first_parameter_name, second_parameter_name
            )
        )
    if first_parameter_value is None and second_parameter_value is None:
        raise ValueError(
            "One of {0} or {1} should be specified.".format(
                first_parameter_name, second_parameter_name
            )
        )
    return values


def validate_greater_than(
    values, first_parameter_name: str, second_parameter_name: str
):
    first_parameter_value = (
        values[first_parameter_name] if first_parameter_name in values else None
    )
    second_parameter_value = (
        values[second_parameter_name] if second_parameter_name in values else None
    )
    if not first_parameter_value > second_parameter_value:
        raise ValueError(
            "{0} ({1}) should be greater than {2} ({3})".format(
                first_parameter_name,
                first_parameter_value,
                second_parameter_name,
                second_parameter_value,
            )
        )
    return values


def validate_hydrodynamics_length(values):
    time_steps = __get_value(values, "time_steps")
    wave_heights = __get_value(values, "wave_heights")
    water_levels = __get_value(values, "water_levels")
    wave_periods = __get_value(values, "wave_periods")
    wave_directions = __get_value(values, "wave_directions")
    nr_time_steps = len(time_steps)
    if (
        nr_time_steps - 1 != len(water_levels)
        or nr_time_steps - 1 != len(wave_heights)
        or nr_time_steps - 1 != len(wave_periods)
        or nr_time_steps - 1 != len(wave_directions)
    ):
        raise Exception(
            "Length of the specified series for waterlevels, wave heights, wave periods and wave angles needs to be exactly 1 less than the length of the specified time steps."
        )
    return values


def __get_value(values, name):
    return values[name] if name in values else None
