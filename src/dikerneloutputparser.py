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
 
 This is a license template.
"""

from dikerneloutput import (
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    NaturalStoneOutputLocation,
)
from dikernelcreferences import *


class DikernelOutputParser:
    @staticmethod
    def parse_dikernel_output(
        c_output: CalculationOutput, x_positions: list[float]
    ) -> list[DikernelOutputLocation]:
        output_locations = list[float]()
        i = 0
        for c_output_location in c_output.LocationDependentOutputItems:
            c_output_location = c_output.LocationDependentOutputItems[i]
            output_locations.append(
                DikernelOutputParser.__create_output_location(
                    c_output_location, x_positions[i]
                )
            )
            i = i + 1
        return output_locations

    @staticmethod
    def __create_output_location(
        c_output_location: LocationDependentOutput, x_position: float
    ):
        moment_of_failure = (
            next(
                (
                    item.TimeOfFailure
                    for item in c_output_location.TimeDependentOutputItems
                    if item is not None and item.TimeOfFailure is not None
                ),
                None,
            )
            if not None
            else None
        )
        time_dependent_output_items = c_output_location.TimeDependentOutputItems
        damage_development = list(item.Damage for item in time_dependent_output_items)
        damage_increment = list(
            item.IncrementDamage for item in time_dependent_output_items
        )

        match c_output_location:
            case AsphaltRevetmentWaveImpactLocationDependentOutput():
                return (
                    DikernelOutputParser.__create_asphalt_wave_impact_output_location(
                        x_position,
                        c_output_location.Z,
                        moment_of_failure,
                        c_output_location.OuterSlope,
                        c_output_location.LogFlexuralStrength,
                        c_output_location.StiffnessRelation,
                        c_output_location.ComputationalThickness,
                        c_output_location.EquivalentElasticModulus,
                        damage_development,
                        damage_increment,
                        time_dependent_output_items,
                    )
                )
            case GrassRevetmentOvertoppingLocationDependentOutput():
                return DikernelOutputParser.__create_grass_overtopping_output_location(
                    x_position,
                    moment_of_failure,
                    damage_development,
                    damage_increment,
                    time_dependent_output_items,
                )
            case GrassRevetmentWaveImpactLocationDependentOutput():
                return DikernelOutputParser.__create_grass_wave_impact_output_location(
                    x_position,
                    c_output_location.Z,
                    moment_of_failure,
                    c_output_location.MinimumWaveHeight,
                    c_output_location.MaximumWaveHeight,
                    damage_development,
                    damage_increment,
                    time_dependent_output_items,
                )
            case GrassRevetmentWaveRunupRayleighLocationDependentOutput():
                return None
                """
                    TODO: Implement wave runup calculations
                    grassRevetmentWaveRunupRayleightime_dependent_output_items = cOutputLocation.time_dependent_output_items

                    return GrassWaveRunupOutputLocation(
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.IncrementDamage).ToList(),
                        grassRevetmentWaveRunupRayleighLocationDependentOutput.Z,
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.VerticalDistanceWaterLevelElevation).ToList(),
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.WaveAngle).ToList(),
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.WaveAngleImpact).ToList(),
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.RepresentativeWaveRunup2P).ToList(),
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.CumulativeOverload).ToList(),
                        grassRevetmentWaveRunupRayleightime_dependent_output_items
                            .Select(tdo => tdo.AverageNumberOfWaves).ToList()) """
            case NaturalStoneRevetmentLocationDependentOutput():
                return DikernelOutputParser.__create_natural_stone_output_location(
                    x_position,
                    c_output_location.Z,
                    moment_of_failure,
                    c_output_location.Resistance,
                    damage_development,
                    damage_increment,
                    time_dependent_output_items,
                )

    @staticmethod
    def __create_asphalt_wave_impact_output_location(
        x_position: float,
        z_position: float,
        moment_of_failure: float,
        outer_slope: float,
        log_flexural_strength: float,
        stiffness_relation: float,
        computational_thickness: float,
        equivalent_elastic_modulus: float,
        damage_development: list[float],
        damage_increment: list[float],
        time_dependent_output_items,
    ) -> AsphaltWaveImpactOutputLocation:
        return AsphaltWaveImpactOutputLocation(
            x_position,
            moment_of_failure,
            damage_development,
            damage_increment,
            z_position,
            outer_slope,
            log_flexural_strength,
            stiffness_relation,
            computational_thickness,
            equivalent_elastic_modulus,
            list(item.MaximumPeakStress for item in time_dependent_output_items),
            list(item.AverageNumberOfWaves for item in time_dependent_output_items),
        )

    @staticmethod
    def __create_grass_overtopping_output_location(
        x_position: float,
        moment_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
        time_dependent_output_items,
    ) -> GrassOvertoppingOutputLocation:
        return GrassOvertoppingOutputLocation(
            x_position,
            moment_of_failure,
            damage_development,
            damage_increment,
            list(
                item.VerticalDistanceWaterLevelElevation
                for item in time_dependent_output_items
            ),
            list(
                item.RepresentativeWaveRunup2P for item in time_dependent_output_items
            ),
            list(item.CumulativeOverload for item in time_dependent_output_items),
            list(item.AverageNumberOfWaves for item in time_dependent_output_items),
        )

    @staticmethod
    def __create_grass_wave_impact_output_location(
        x_position: float,
        z_position: float,
        moment_of_failure: float,
        minimum_wave_height: float,
        maximum_wave_height: float,
        damage_development: list[float],
        damage_increment: list[float],
        time_dependent_output_items,
    ) -> GrassWaveImpactOutputLocation:
        return GrassWaveImpactOutputLocation(
            x_position,
            moment_of_failure,
            damage_development,
            damage_increment,
            z_position,
            minimum_wave_height,
            maximum_wave_height,
            list(item.LoadingRevetment for item in time_dependent_output_items),
            list(item.UpperLimitLoading for item in time_dependent_output_items),
            list(item.LowerLimitLoading for item in time_dependent_output_items),
            list(item.WaveAngle for item in time_dependent_output_items),
            list(item.WaveAngleImpact for item in time_dependent_output_items),
            list(item.WaveHeightImpact for item in time_dependent_output_items),
        )

    @staticmethod
    def __create_natural_stone_output_location(
        x_position: float,
        z_position: float,
        moment_of_failure: float,
        resistance: float,
        damage_development: list[float],
        damage_increment: list[float],
        time_dependent_output_items,
    ) -> NaturalStoneOutputLocation:
        return NaturalStoneOutputLocation(
            x_position,
            moment_of_failure,
            damage_development,
            damage_increment,
            z_position,
            resistance,
            list(item.outer_slope for item in time_dependent_output_items),
            list(item.SlopeUpperLevel for item in time_dependent_output_items),
            list(item.SlopeUpperPosition for item in time_dependent_output_items),
            list(item.SlopeLowerLevel for item in time_dependent_output_items),
            list(item.SlopeLowerPosition for item in time_dependent_output_items),
            list(item.LoadingRevetment for item in time_dependent_output_items),
            list(item.SurfSimilarityParameter for item in time_dependent_output_items),
            list(item.WaveSteepnessDeepWater for item in time_dependent_output_items),
            list(item.UpperLimitLoading for item in time_dependent_output_items),
            list(item.LowerLimitLoading for item in time_dependent_output_items),
            list(item.DepthMaximumWaveLoad for item in time_dependent_output_items),
            list(
                item.DistanceMaximumWaveElevation
                for item in time_dependent_output_items
            ),
            list(
                item.NormativeWidthOfWaveImpact for item in time_dependent_output_items
            ),
            list(item.HydraulicLoad for item in time_dependent_output_items),
            list(item.WaveAngle for item in time_dependent_output_items),
            list(item.WaveAngleImpact for item in time_dependent_output_items),
            list(item.ReferenceTimeDegradation for item in time_dependent_output_items),
            list(item.ReferenceDegradation for item in time_dependent_output_items),
        )
