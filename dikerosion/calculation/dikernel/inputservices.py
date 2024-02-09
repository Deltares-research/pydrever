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

import copy, numpy
from dikerosion.data import DikernelInput, HydrodynamicConditions
import dikerosion.calculation.hydrodynamicsinterpolation as interpolation


def get_run_input(dikernel_input: DikernelInput) -> DikernelInput:
    """
    Returns manipulated input that incorporates the desired output time steps and start time of the calculation in the hydrodynamic input.

    Returns:
        DikernelInput: A manipulated input object that can be used to calculate.
    """
    time_steps = dikernel_input.hydrodynamic_input.time_steps
    run_time_steps = get_run_time_steps(dikernel_input)
    run_hydrodynamics = HydrodynamicConditions(
        run_time_steps,
        interpolation.interpolate_time_series(
            time_steps, dikernel_input.hydrodynamic_input.water_levels, run_time_steps
        ),
        interpolation.interpolate_time_series(
            time_steps, dikernel_input.hydrodynamic_input.wave_heights, run_time_steps
        ),
        interpolation.interpolate_time_series(
            time_steps, dikernel_input.hydrodynamic_input.wave_periods, run_time_steps
        ),
        interpolation.interpolate_time_series(
            time_steps,
            dikernel_input.hydrodynamic_input.wave_directions,
            run_time_steps,
        ),
    )
    run_input = DikernelInput(run_hydrodynamics, dikernel_input.dike_schematization)
    run_input.output_locations = copy.deepcopy(dikernel_input.output_locations)
    run_input.settings = copy.deepcopy(dikernel_input.settings)
    return run_input


def get_run_time_steps(input: DikernelInput) -> list[float]:
    """
    This method combines all time steps and required output time steps to for
    a list of time steps that needs to be used during calculation.

    It combines the specified time steps for hydrodynamic conditions and the
    specified output time steps and then takes all time steps between the
    optional start and stop times (including the start and stop times).
    """
    run_time_steps = input.hydrodynamic_input.time_steps
    if input.output_time_steps is not None:
        run_time_steps = numpy.union1d(run_time_steps, input.output_time_steps).tolist()

    if input.start_time is not None:
        run_time_steps = list(
            time_step
            for time_step in numpy.union1d(run_time_steps, [input.start_time])
            if time_step >= input.start_time
        )

    if input.stop_time is not None:
        run_time_steps = list(
            time_step
            for time_step in numpy.union1d(run_time_steps, [input.stop_time])
            if time_step <= input.start_time
        )
    return run_time_steps
