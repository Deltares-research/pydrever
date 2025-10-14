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

import pydrever.calculation._dikernel._dikernelcreferences as _cs
import numpy as np


def calculate_time_line(
    wave_heights: list[float],
    wave_direction: float,
    dike_orientation: float,
    a: float = 1,
    b: float = -0.035,
    c: float = 0.25,
    n: float = 2.0 / 3,
    q: float = 0.35,
    r: float = 10.0,
    te_min: float = 3.6,
    te_max: float = 360000,
):
    """
    Function that calculates the grass resistance times for given wave heights using DiKErnel.

    Args:
        wave_heights (list[float]): A list of wave heights for which resistance times need to be calculated.
        wave_direction (float): The wave direction.
        dike_orientation (float): The orientation of the dike.
        a (float, optional): Grass resistance timeline parameter a. Defaults to 1 (closed sod).
        b (float, optional): Grass resistance timeline parameter b. Defaults to -0.035.
        c (float, optional): Grass resistance timeline parameter c. Defaults to 0.25.
        n (float, optional): Wave angle correction parameter n. Defaults to 2.0/3.
        q (float, optional): Wave angle correction parameter q. Defaults to 0.35.
        r (float, optional): Wave angle correction parameter r. Defaults to 10.0.
        te_min (float, optional): Minimum resistance time calculated. If wave heights entered result in smaller resistance times, the wave height corresponding to this time wille be added and all larger waves will result in None. Defaults to 3.6.
        te_max (float, optional): Maximum resistance time calculated. If wave heights entered result in larger resistance times, the wave height corresponding to this time wille be added and all smaller waves will result in None. Defaults to 360000.

    Returns:
        _type_: _description_
    """
    wave_angle = _cs.HydraulicLoadFunctions.WaveAngle(wave_direction, dike_orientation)
    wave_angle_impact = _cs.GrassWaveImpactFunctions.WaveAngleImpact(wave_angle, n, q, r)
    minimum_wave_height = _cs.GrassWaveImpactFunctions.MinimumWaveHeight(a, b, c, te_max)
    maximum_wave_height = _cs.GrassWaveImpactFunctions.MaximumWaveHeight(a, b, c, te_min)
    if min(wave_heights) < minimum_wave_height:
        np.append(wave_heights, minimum_wave_height)
    if max(wave_heights) > maximum_wave_height:
        np.append(wave_heights, maximum_wave_height)

    wave_heights = sorted(set(wave_heights))

    times = []
    for wave_height in wave_heights:
        if wave_height < minimum_wave_height or wave_height > maximum_wave_height:
            times.append(None)
        else:
            wave_height_impact = _cs.GrassWaveImpactFunctions.WaveHeightImpact(
                minimum_wave_height,
                maximum_wave_height,
                wave_angle_impact,
                wave_height,
            )

            times.append(_cs.GrassWaveImpactFunctions.TimeLine(wave_height_impact, a, b, c))

    return times
