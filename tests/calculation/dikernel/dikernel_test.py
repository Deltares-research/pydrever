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

from dikerosion.calculation import Dikernel
import dikerosion.data as data


def test_perform_basic_calculation():
    x_positions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
    z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
    roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
    dike_schematization = data.DikeSchematization(
        90.0, x_positions, z_positions, roughnesses, 25.0, 45.0
    )
    time_steps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
    water_levels = [1.2, 1.9, 2.8, 2.7, 2.0]
    wave_heights = [0.5, 0.9, 1.2, 1.1, 0.8]
    wave_periods = [6.0, 6.0, 6.0, 6.0, 6.0]
    wave_directions = [60.0, 70.0, 80.0, 90.0, 100.0]

    hydrodynamic_conditions = data.HydrodynamicConditions(
        time_steps, water_levels, wave_heights, wave_periods, wave_directions
    )
    input = data.DikernelInput(hydrodynamic_conditions, dike_schematization)
    input.add_output_location(
        42.0,
        data.GrassWaveImpactLayerSpecification(data.TopLayerType.GrassClosedSod),
    )

    kernel = Dikernel(input)
    validation_result = kernel.validate()
    assert validation_result
    runresult = kernel.run()
    assert runresult
    assert kernel.output is not None
    assert len(kernel.output) == 1
