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


def interpolate_time_series(
    time_steps: list[float], values: list[float], target_time_steps: list[float]
) -> list[float]:
    """
    Private method to interpolate time series and add the target_time_steps to the list.

    Args:
        time_steps (list[float]): Original specification of the time steps of the hydrodynamic forcing.
        values (list[float]): Values for each time step in the original time series.
        target_time_steps (list[float]): Desired output time steps that needs to be added to the time series.

    Returns:
        list[float]: A list of values for the combined list of time steps and target_time_steps.
    """
    iargs = 1
    itarget = 1
    target_values = list[float]()
    while itarget < len(target_time_steps):
        if (
            target_time_steps[itarget] > time_steps[iargs]
            and iargs < len(time_steps) - 1
        ):
            iargs = iargs + 1
            continue
        target_values.append(values[iargs - 1])
        itarget = itarget + 1

    return target_values
