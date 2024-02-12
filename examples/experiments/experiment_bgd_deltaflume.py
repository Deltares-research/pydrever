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

from dikerosion.data import (
    CalculationSettings,
    DikeSchematization,
    DikernelInput,
    HydrodynamicConditions,
    OutputLocationSpecification,
    GrassWaveImpactLayerSpecification,
    TopLayerType,
    GrassWaveImpactCalculationSettings,
    GrassCoverWaveImpactTopLayerSettings,
)
from experiment import Experiment
import numpy as numpy


class BgdDeltaFlumeExperiment(Experiment):
    def get_calculation_input() -> DikernelInput:
        input = DikernelInput(
            BgdDeltaFlumeExperiment.generate_hydrodynamics(),
            BgdDeltaFlumeExperiment.generate_dike_schematization(),
        )
        input.output_locations = BgdDeltaFlumeExperiment.generate_output_locations()
        input.settings = BgdDeltaFlumeExperiment.generate_settings()
        return input

    def generate_dike_schematization() -> DikeSchematization:
        x_positions = [154.4, 160.0, 170.48, 191.48]
        z_positions = [0.0, 2.0, 4.325, 8.995]
        roughnesses = [1.0, 1.0, 1.0, 1.0]
        return DikeSchematization(
            90.0, x_positions, z_positions, roughnesses, 160.0, 191.48
        )

    def generate_hydrodynamics() -> HydrodynamicConditions:
        time_steps = (
            numpy.array(
                [
                    0.0,
                    1.00,
                    2.17,
                    3.17,
                    4.17,
                    6.17,
                    8.17,
                    9.13,
                    10.13,
                    10.64,
                    11.39,
                ]
            )
            * 60
            * 60
        )
        water_levels = [6] * (len(time_steps) - 1)
        wave_heights = [
            1.521,
            1.535,
            1.523,
            1.526,
            1.516,
            1.516,
            1.522,
            1.524,
            1.498,
            1.518,
        ]
        wave_directions = [90] * (len(time_steps) - 1)
        wave_periods = [
            4.543,
            4.561,
            4.568,
            4.565,
            4.586,
            4.587,
            4.552,
            4.565,
            4.569,
            4.548,
        ]

        return HydrodynamicConditions(
            time_steps, water_levels, wave_heights, wave_periods, wave_directions
        )

    def generate_settings() -> list[CalculationSettings]:
        closed_sod_top_layer_settings = GrassCoverWaveImpactTopLayerSettings(
            TopLayerType.GrassClosedSod
        )
        closed_sod_top_layer_settings.stance_time_line_a = 1.75
        closed_sod_top_layer_settings.stance_time_line_b = -0.035
        closed_sod_top_layer_settings.stance_time_line_c = 0.25
        wave_impact_settings = GrassWaveImpactCalculationSettings(
            [closed_sod_top_layer_settings]
        )
        wave_impact_settings.te_min = 3.6
        wave_impact_settings.te_max = 3600000
        return [wave_impact_settings]

    def generate_output_locations() -> list[OutputLocationSpecification]:
        x_positions = numpy.linspace(171.0, 190.0, 20)
        return [
            OutputLocationSpecification(
                x_position,
                GrassWaveImpactLayerSpecification(TopLayerType.GrassClosedSod),
            )
            for x_position in x_positions
        ]
