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

from calculationmethods import CalculationMethod


class DikernelOutputLocation:
    def __init__(
        self,
        calculation_type: CalculationMethod,
        x_position: float,
        time_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
    ):
        self.__x_position = x_position
        self.__time_of_failure = time_of_failure
        self.__damage_development = damage_development
        self.__damage_increment = damage_increment
        self.__calculation_type = calculation_type

    @property
    def calculation_method(self) -> CalculationMethod:
        """
        Returns:
            CalculationMethod: The calculation method that was used at this output location.
        """
        return self.__calculation_type

    @property
    def x_position(self) -> float:
        """
        Returns:
            float: The cross-shore position of the calculated location.
        """
        return self.__x_position

    @property
    def failed(self) -> bool:
        """
        Returns:
            bool: Whether the revetment has failed at this position.
        """
        return self.__time_of_failure is not None

    @property
    def time_of_failure(self) -> float:
        """
        Returns:
            float: The moment (time step) this location failed. None if it did not fail.
        """
        return self.__time_of_failure

    @property
    def damage_development(self) -> list[float]:
        """
        Returns:
            list[float]: The damage level at the end of each time step.
        """
        return self.__damage_development

    @property
    def final_damage(self) -> float:
        return (
            self.__damage_development[-1]
            if self.__damage_development is not None
            else 0.0
        )

    @property
    def damage_increment(self) -> list[float]:
        """
        Returns:
            list[float]: The increment of the damage level during each time step.
        """
        return self.__damage_increment


class AsphaltWaveImpactOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        x_position: float,
        time_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
        z: float,
        outer_slope: float,
        log_flexural_strength: float,
        stiffness_relation: float,
        computational_thickness: float,
        equivalent_elastic_modulus: float,
        maximum_peak_stress: list[float],
        average_number_of_waves: list[float],
    ):
        super().__init__(
            CalculationMethod.AsphaltWaveImpact,
            x_position,
            time_of_failure,
            damage_development,
            damage_increment,
        )
        self.__zPosition = z
        self.__outer_slope = outer_slope
        self.__log_flexural_strength = log_flexural_strength
        self.__stiffness_relation = stiffness_relation
        self.__computational_thickness = computational_thickness
        self.__equivalent_elastic_modulus = equivalent_elastic_modulus
        self.__maximum_peak_stress = maximum_peak_stress
        self.__average_number_of_waves = average_number_of_waves

    @property
    def z_position(self) -> float:
        return self.__zPosition

    @property
    def outer_slope(self) -> float:
        return self.__outer_slope

    @property
    def log_flexural_strength(self) -> float:
        return self.__log_flexural_strength

    @property
    def stiffness_relation(self) -> float:
        return self.__stiffness_relation

    @property
    def computational_thickness(self) -> float:
        return self.__computational_thickness

    @property
    def equivalent_elastic_modulus(self) -> float:
        return self.__equivalent_elastic_modulus

    @property
    def maximum_peak_stress(self) -> list[float]:
        return self.__maximum_peak_stress

    @property
    def average_number_of_waves(self) -> list[float]:
        return self.__average_number_of_waves


class GrassOvertoppingOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        x_position: float,
        time_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
        vertical_distance_water_level_elevation: list[float],
        representative_wave_runup_2p: list[float],
        cumulative_overload: list[float],
        average_number_of_waves: list[float],
    ):
        super().__init__(
            CalculationMethod.GrassWaveOvertopping,
            x_position,
            time_of_failure,
            damage_development,
            damage_increment,
        )
        self.__vertical_distance_water_level_elevation = (
            vertical_distance_water_level_elevation
        )
        self.__representative_wave_runup_2p = representative_wave_runup_2p
        self.__cumulative_overload = cumulative_overload
        self.__average_number_of_waves = average_number_of_waves

    @property
    def vertical_distance_water_level_elevation(self) -> list[float]:
        return self.__vertical_distance_water_level_elevation

    @property
    def representative_wave_runup_2p(self) -> list[float]:
        return self.__representative_wave_runup_2p

    @property
    def cumulative_overload(self) -> list[float]:
        return self.__cumulative_overload

    @property
    def average_number_of_waves(self) -> list[float]:
        return self.__average_number_of_waves


class GrassWaveImpactOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        x_position: float,
        time_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
        z: float,
        minimum_wave_height: float,
        maximum_wave_height: float,
        loading_revetment: list[float],
        upper_limit_loading: list[float],
        lower_limit_loading: list[float],
        wave_angle: list[float],
        wave_angle_impact: list[float],
        wave_height_impactt: list[float],
    ):
        super().__init__(
            CalculationMethod.GrassWaveImpact,
            x_position,
            time_of_failure,
            damage_development,
            damage_increment,
        )
        self.__z_position = z
        self.__minimum_wave_height = minimum_wave_height
        self.__maximum_wave_height = maximum_wave_height
        self.__loading_revetment = loading_revetment
        self.__upper_limit_loading = upper_limit_loading
        self.__lower_limit_loading = lower_limit_loading
        self.__wave_angle = wave_angle
        self.__wave_angle_impact = wave_angle_impact
        self.__wave_height_impactt = wave_height_impactt

    @property
    def z_position(self) -> float:
        return self.__z_position

    @property
    def minimum_wave_height(self) -> float:
        return self.__minimum_wave_height

    @property
    def maximum_wave_height(self) -> float:
        return self.__maximum_wave_height

    @property
    def loading_revetment(self) -> list[float]:
        return self.__loading_revetment

    @property
    def upper_limit_loading(self) -> list[float]:
        return self.__upper_limit_loading

    @property
    def lower_limit_loading(self) -> list[float]:
        return self.__lower_limit_loading

    @property
    def wave_angle(self) -> list[float]:
        return self.__wave_angle

    @property
    def wave_angle_impact(self) -> list[float]:
        return self.__wave_angle_impact

    @property
    def wave_height_impactt(self) -> list[float]:
        return self.__wave_height_impactt


class NaturalStoneOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        x_position: float,
        time_of_failure: float,
        damage_development: list[float],
        damage_increment: list[float],
        z: float,
        resistance: float,
        outer_slope: list[float],
        slope_upper_level: list[float],
        slope_upper_position: list[float],
        slope_lower_level: list[float],
        slope_lower_position: list[float],
        loading_revetment: list[float],
        surf_similarity_parameter: list[float],
        wave_steepness_deep_water: list[float],
        upper_limit_loading: list[float],
        lower_limit_loading: list[float],
        depth_maximum_wave_load: list[float],
        distance_maximum_wave_elevation: list[float],
        normative_width_of_wave_impact: list[float],
        hydrodynamic_load: list[float],
        wave_angle: list[float],
        wave_angle_impact: list[float],
        reference_time_degradation: list[float],
        reference_degradation: list[float],
    ):
        super().__init__(
            CalculationMethod.NaturalStone,
            x_position,
            time_of_failure,
            damage_development,
            damage_increment,
        )
        self.__z_position = z
        self.__resistance = resistance
        self.__outer_slope = outer_slope
        self.__slope_upper_level = slope_upper_level
        self.__slope_upper_position = slope_upper_position
        self.__slope_lower_level = slope_lower_level
        self.__slope_lower_position = slope_lower_position
        self.__loading_revetment = loading_revetment
        self.__surf_similarity_parameter = surf_similarity_parameter
        self.__wave_steepness_deep_water = wave_steepness_deep_water
        self.__upper_limit_loading = upper_limit_loading
        self.__lower_limit_loading = lower_limit_loading
        self.__depth_maximum_wave_load = depth_maximum_wave_load
        self.__distance_maximum_wave_elevation = distance_maximum_wave_elevation
        self.__normative_width_of_wave_impact = normative_width_of_wave_impact
        self.__hydrodynamic_load = hydrodynamic_load
        self.__wave_angle = wave_angle
        self.__wave_angle_impact = wave_angle_impact
        self.__reference_time_degradation = reference_time_degradation
        self.__reference_degradation = reference_degradation

    @property
    def z_position(self) -> float:
        return self.__z_position

    @property
    def resistance(self) -> float:
        return self.__resistance

    @property
    def outer_slope(self) -> list[float]:
        return self.__outer_slope

    @property
    def slope_upper_level(self) -> list[float]:
        return self.__slope_upper_level

    @property
    def slope_upper_position(self) -> list[float]:
        return self.__slope_upper_position

    @property
    def slope_lower_level(self) -> list[float]:
        return self.__slope_lower_level

    @property
    def slope_lower_position(self) -> list[float]:
        return self.__slope_lower_position

    @property
    def loading_revetment(self) -> list[float]:
        return self.__loading_revetment

    @property
    def surf_similarity_parameter(self) -> list[float]:
        return self.__surf_similarity_parameter

    @property
    def wave_steepness_deep_water(self) -> list[float]:
        return self.__wave_steepness_deep_water

    @property
    def upper_limit_loading(self) -> list[float]:
        return self.__upper_limit_loading

    @property
    def lower_limit_loading(self) -> list[float]:
        return self.__lower_limit_loading

    @property
    def depth_maximum_wave_load(self) -> list[float]:
        return self.__depth_maximum_wave_load

    @property
    def distance_maximum_wave_elevation(self) -> list[float]:
        return self.__distance_maximum_wave_elevation

    @property
    def normative_width_of_wave_impact(self) -> list[float]:
        return self.__normative_width_of_wave_impact

    @property
    def hydrodynamic_load(self) -> list[float]:
        return self.__hydrodynamic_load

    @property
    def wave_angle(self) -> list[float]:
        return self.__wave_angle

    @property
    def wave_angle_impact(self) -> list[float]:
        return self.__wave_angle_impact

    @property
    def reference_time_degradation(self) -> list[float]:
        return self.__reference_time_degradation

    @property
    def reference_degradation(self) -> list[float]:
        return self.__reference_degradation
