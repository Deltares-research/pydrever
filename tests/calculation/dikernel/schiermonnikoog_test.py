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

import numpy
from pydrever.data import (
    DikeSchematization,
    HydrodynamicConditions,
    DikernelInput,
    RevetmentZoneSpecification,
    HorizontalRevetmentZoneDefinition,
    NordicStoneLayerSpecification,
    AsphaltLayerSpecification,
    GrassWaveImpactLayerSpecification,
    TopLayerType,
    GrassWaveRunupLayerSpecification,
)

from pydrever.calculation import Dikernel
import pytest


# @pytest.mark.skip("Not functioning yet")
def test_schiermonnikoog():

    xcoordinates_unsorted = [60.0, 50, 22, 15, 0.8, -90]
    zcoordinates_unsorted = [7, 7, 2.8, 2.5, 0.7, -1.5]

    """
    xcoordinates = sorted(xcoordinates_unsorted)
    zcoordinates = [
        z for _, z in sorted(zip(xcoordinates_unsorted, zcoordinates_unsorted))
    ]
    """

    xcoordinates = xcoordinates_unsorted
    zcoordinates = zcoordinates_unsorted

    roughnesses = [1, 1, 1, 0.6, 1]
    dike_schematization = DikeSchematization(
        dike_orientation=180.0,
        x_positions=xcoordinates,
        z_positions=zcoordinates,
        roughnesses=roughnesses,
        x_outer_toe=0.8,
        x_outer_crest=50.0,
    )

    mean_water_level = 0.0
    tidal_emplitude_moon = 1.4
    tidal_emplitude_sun = 0.4
    time_steps_per_hour = 1
    signal_length = 36
    time_steps = (
        numpy.linspace(0, signal_length, signal_length * time_steps_per_hour + 1) * 3600
    )
    tidal_signal = (
        numpy.add(
            (
                numpy.sin(time_steps[:-1] * (2 * numpy.pi) / ((12 * 60 + 25) * 60))
                * tidal_emplitude_moon
            ),
            (
                numpy.sin(time_steps[:-1] * (2 * numpy.pi) / ((24 * 60 + 50) * 60))
                * tidal_emplitude_sun
                * -1.0
            ),
        )
        + mean_water_level
    )

    water_level_setup = numpy.interp(
        time_steps[:-1], numpy.array([0, 18, 36]) * 3600, [0, 5.6, 0]
    )
    water_levels = numpy.add(tidal_signal, water_level_setup)

    wave_heights = numpy.interp(
        time_steps[:-1], numpy.array([0, 16.5, 36]) * 3600, [0.5, 2.8, 1.2]
    )

    wave_periods = numpy.ones(tidal_signal.size) * 7.0
    wave_directions = numpy.ones(tidal_signal.size) * 210.0

    hydrodynamic_conditions = HydrodynamicConditions(
        time_steps=time_steps,
        water_levels=water_levels,
        wave_heights=wave_heights,
        wave_periods=wave_periods,
        wave_directions=wave_directions,
    )

    input = DikernelInput(
        hydrodynamic_input=hydrodynamic_conditions,
        dike_schematization=dike_schematization,
    )

    input.start_time = 0.0
    output_time_steps = numpy.arange(0.0, 126000, 1000)
    output_time_steps = numpy.union1d(time_steps, output_time_steps)
    input.output_time_steps = output_time_steps

    input.output_revetment_zones = []
    input.output_revetment_zones.append(
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=0.9, x_max=14.9, dx_max=1.0
            ),
            top_layer_specification=NordicStoneLayerSpecification(
                top_layer_thickness=0.4, relative_density=2.45
            ),
        )
    )

    input.output_revetment_zones.append(
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=15.0, x_max=21.9, dx_max=1.0
            ),
            top_layer_specification=AsphaltLayerSpecification(
                flexural_strength=0.9,
                soil_elasticity=64.0,
                upper_layer_thickness=0.16,
                upper_layer_elasticity_modulus=5712.0,
                stiffness_ratio_nu=0.35,
                fatigue_asphalt_alpha=0.5,
                fatigue_asphalt_beta=5.4,
            ),
        )
    )

    input.output_revetment_zones.append(
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=22.0, x_max=49.9, dx_max=1.0
            ),
            top_layer_specification=GrassWaveImpactLayerSpecification(
                top_layer_type=TopLayerType.GrassClosedSod
            ),
        )
    )
    input.output_revetment_zones.append(
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=22.0, x_max=49.9, dx_max=1.0
            ),
            top_layer_specification=GrassWaveRunupLayerSpecification(
                outer_slope=0.16, top_layer_type=TopLayerType.GrassClosedSod
            ),
        )
    )

    calculation = Dikernel(input=input)
    result = calculation.run()

    assert result is not False
