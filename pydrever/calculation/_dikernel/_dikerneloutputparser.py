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

from pydrever.data import (
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    GrassWaveRunupOutputLocation,
    NaturalStoneOutputLocation,
)
from pydrever.calculation._dikernel._dikernelcreferences import *
import numpy as np


def parse(c_output: CalculationOutput, x_positions: list[float]) -> list[DikernelOutputLocation]:
    """
    Converts C#-typed output to a list of DikernelOutputLocations

    Args:
        c_output (CalculationOutput): The obtained C# output.
        x_positions (list[float]): X-positions of the specfied output locations.

    Returns:
        list[DikernelOutputLocation]: A list of output locations translated
        to a (derived) type of DikernelOutputLocation containing all calculation results.
    """
    output_locations = list[DikernelOutputLocation]()
    i = 0
    for c_output_location in c_output.LocationDependentOutputItems:
        c_output_location = c_output.LocationDependentOutputItems[i]
        output_location = __create_output_location(c_output_location, x_positions[i])
        if output_location is not None:
            output_locations.append(output_location)

        i = i + 1
    return output_locations


def __create_output_location(c_output_location: LocationDependentOutput, x_position: float) -> DikernelOutputLocation | None:
    """
    Converts a single C#-typed output location to an equivalent python class

    Args:
        c_output_location (LocationDependentOutput): The C# output.
        x_position (float): The X-positions of the specfied output location.

    Returns:
        DikernelOutputLocation: The translated output for this location.
    """

    """
    Calculate commonly used output variables
    """
    time_of_failure: float | None = c_output_location.TimeOfFailure
    damage_increment: list[float] = list(item.IncrementDamage for item in c_output_location.TimeDependentOutputItems)
    damage_development: list[float] = list(item for item in c_output_location.CumulativeDamages)

    """
    Switch between the various type of possible output (different types of calculation)
    """
    match c_output_location:
        case AsphaltWaveImpactLocationDependentOutput():
            return __create_asphalt_wave_impact_output_location(
                x_position,
                c_output_location.Z,
                time_of_failure,
                c_output_location.OuterSlope,
                c_output_location.LogFlexuralStrength,
                c_output_location.StiffnessRelation,
                c_output_location.ComputationalThickness,
                c_output_location.EquivalentElasticModulus,
                damage_development,
                damage_increment,
                c_output_location.TimeDependentOutputItems,
            )
        case GrassCumulativeOverloadLocationDependentOutput():
            return __create_grass_overtopping_output_location(
                x_position,
                time_of_failure,
                damage_development,
                damage_increment,
                c_output_location.TimeDependentOutputItems,
            )
        case GrassWaveImpactLocationDependentOutput():
            return __create_grass_wave_impact_output_location(
                x_position,
                c_output_location.Z,
                time_of_failure,
                c_output_location.MinimumWaveHeight,
                c_output_location.MaximumWaveHeight,
                damage_development,
                damage_increment,
                c_output_location.TimeDependentOutputItems,
            )
        # TODO: This needs to change to CumulativeOverload. Also the input.
        # case GrassWaveRunupRayleighLocationDependentOutput():
        #     return __create_grass_wave_runup_output_location(
        #         x_position,
        #         c_output_location.Z,
        #         time_of_failure,
        #         damage_development,
        #         damage_increment,
        #         c_output_location.TimeDependentOutputItems,
        #     )
        case NaturalStoneWaveImpactLocationDependentOutput():
            return __create_natural_stone_output_location(
                x_position,
                c_output_location.Z,
                time_of_failure,
                c_output_location.Resistance,
                damage_development,
                damage_increment,
                c_output_location.TimeDependentOutputItems,
            )


def __create_asphalt_wave_impact_output_location(
    x_position: float,
    z_position: float,
    time_of_failure: float | None,
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
        x_position=x_position,
        time_of_failure=time_of_failure,
        damage_development=damage_development,
        damage_increment=damage_increment,
        z_position=z_position,
        outer_slope=outer_slope,
        log_flexural_strength=log_flexural_strength,
        stiffness_relation=stiffness_relation,
        computational_thickness=computational_thickness,
        equivalent_elastic_modulus=equivalent_elastic_modulus,
        maximum_peak_stress=list(item.MaximumPeakStress for item in time_dependent_output_items),
        average_number_of_waves=list(item.AverageNumberOfWaves for item in time_dependent_output_items),
    )


def __create_grass_overtopping_output_location(
    x_position: float,
    time_of_failure: float | None,
    damage_development: list[float],
    damage_increment: list[float],
    time_dependent_output_items,
) -> GrassOvertoppingOutputLocation:
    return GrassOvertoppingOutputLocation(
        x_position=x_position,
        time_of_failure=time_of_failure,
        damage_development=damage_development,
        damage_increment=damage_increment,
        vertical_distance_water_level_elevation=list(item.VerticalDistanceWaterLevelElevation for item in time_dependent_output_items),
        representative_wave_runup_2p=list(item.RepresentativeWaveRunup2P for item in time_dependent_output_items),
        cumulative_overload=list(item.CumulativeOverload for item in time_dependent_output_items),
        average_number_of_waves=list(item.AverageNumberOfWaves for item in time_dependent_output_items),
    )


def __create_grass_wave_runup_output_location(
    x_position: float,
    z_position: float,
    time_of_failure: float | None,
    damage_development: list[float],
    damage_increment: list[float],
    time_dependent_output_items,
) -> GrassWaveRunupOutputLocation:
    return GrassWaveRunupOutputLocation(
        x_position=x_position,
        z_position=z_position,
        time_of_failure=time_of_failure,
        damage_development=damage_development,
        damage_increment=damage_increment,
        vertical_distance_water_level_elevation=list(item.VerticalDistanceWaterLevelElevation for item in time_dependent_output_items),
        wave_angle=list(item.WaveAngle for item in time_dependent_output_items),
        wave_angle_impact=list(item.WaveAngleImpact for item in time_dependent_output_items),
        representative_wave_runup_2p=list(item.RepresentativeWaveRunup2P for item in time_dependent_output_items),
        cumulative_overload=list(item.CumulativeOverload for item in time_dependent_output_items),
        average_number_of_waves=list(item.AverageNumberOfWaves for item in time_dependent_output_items),
    )


def __create_grass_wave_impact_output_location(
    x_position: float,
    z_position: float,
    time_of_failure: float | None,
    minimum_wave_height: float,
    maximum_wave_height: float,
    damage_development: list[float],
    damage_increment: list[float],
    time_dependent_output_items,
) -> GrassWaveImpactOutputLocation:
    return GrassWaveImpactOutputLocation(
        x_position=x_position,
        time_of_failure=time_of_failure,
        damage_development=damage_development,
        damage_increment=damage_increment,
        z_position=z_position,
        minimum_wave_height=minimum_wave_height,
        maximum_wave_height=maximum_wave_height,
        loading_revetment=list(item.LoadingRevetment for item in time_dependent_output_items),
        upper_limit_loading=list(item.UpperLimitLoading for item in time_dependent_output_items),
        lower_limit_loading=list(item.LowerLimitLoading for item in time_dependent_output_items),
        wave_angle=list(item.WaveAngle for item in time_dependent_output_items),
        wave_angle_impact=list(item.WaveAngleImpact for item in time_dependent_output_items),
        wave_height_impact=list(item.WaveHeightImpact for item in time_dependent_output_items),
    )


def __create_natural_stone_output_location(
    x_position: float,
    z_position: float,
    time_of_failure: float | None,
    resistance: float,
    damage_development: list[float],
    damage_increment: list[float],
    time_dependent_output_items,
) -> NaturalStoneOutputLocation:
    return NaturalStoneOutputLocation(
        x_position=x_position,
        time_of_failure=time_of_failure,
        damage_development=damage_development,
        damage_increment=damage_increment,
        z_position=z_position,
        resistance=resistance,
        outer_slope=list(item.OuterSlope for item in time_dependent_output_items),
        slope_upper_level=list(item.SlopeUpperLevel for item in time_dependent_output_items),
        slope_upper_position=list(item.SlopeUpperPosition for item in time_dependent_output_items),
        slope_lower_level=list(item.SlopeLowerLevel for item in time_dependent_output_items),
        slope_lower_position=list(item.SlopeLowerPosition for item in time_dependent_output_items),
        loading_revetment=list(item.LoadingRevetment for item in time_dependent_output_items),
        surf_similarity_parameter=list(item.SurfSimilarityParameter for item in time_dependent_output_items),
        wave_steepness_deep_water=list(item.WaveSteepnessDeepWater for item in time_dependent_output_items),
        upper_limit_loading=list(item.UpperLimitLoading for item in time_dependent_output_items),
        lower_limit_loading=list(item.LowerLimitLoading for item in time_dependent_output_items),
        depth_maximum_wave_load=list(item.DepthMaximumWaveLoad for item in time_dependent_output_items),
        distance_maximum_wave_elevation=list(item.DistanceMaximumWaveElevation for item in time_dependent_output_items),
        normative_width_of_wave_impact=list(item.NormativeWidthOfWaveImpact for item in time_dependent_output_items),
        hydrodynamic_load=list(item.HydraulicLoad for item in time_dependent_output_items),
        wave_angle=list(item.WaveAngle for item in time_dependent_output_items),
        wave_angle_impact=list(item.WaveAngleImpact for item in time_dependent_output_items),
        reference_time_degradation=list(item.ReferenceTimeDegradation for item in time_dependent_output_items),
        reference_degradation=list(item.ReferenceDegradation for item in time_dependent_output_items),
    )
