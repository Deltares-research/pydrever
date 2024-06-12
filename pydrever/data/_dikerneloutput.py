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

from pydantic import BaseModel, ConfigDict


class DikernelOutputLocation(BaseModel):
    model_config = ConfigDict(frozen=True)

    x_position: float
    """The cross-shore position of the calculated location."""
    time_of_failure: float | None
    """The moment (time step) this location failed. None if it did not fail."""
    damage_development: list[float]
    """The damage level at the end of each time step."""
    damage_increment: list[float]
    """The increment of the damage level during each time step."""

    @property
    def failed(self) -> bool:
        """
        Returns:
            bool: Whether the revetment has failed at this position.
        """
        return self.time_of_failure is not None

    @property
    def final_damage(self) -> float:
        return (
            self.damage_development[-1] if self.damage_development is not None else 0.0
        )


class AsphaltWaveImpactOutputLocation(DikernelOutputLocation):
    z_position: float
    outer_slope: float
    log_flexural_strength: float
    stiffness_relation: float
    computational_thickness: float
    equivalent_elastic_modulus: float
    maximum_peak_stress: list[float]
    average_number_of_waves: list[float]


class GrassOvertoppingOutputLocation(DikernelOutputLocation):
    representative_wave_runup_2p: list[float]
    cumulative_overload: list[float]
    average_number_of_waves: list[float]
    vertical_distance_water_level_elevation: list[float]


class GrassWaveRunupOutputLocation(DikernelOutputLocation):
    z_position: float
    vertical_distance_water_level_elevation: list[float]
    representative_wave_runup_2p: list[float]
    wave_angle: list[float | None]
    wave_angle_impact: list[float | None]
    cumulative_overload: list[float]
    average_number_of_waves: list[float]


class GrassWaveImpactOutputLocation(DikernelOutputLocation):
    z_position: float
    minimum_wave_height: float
    maximum_wave_height: float
    loading_revetment: list[float]
    upper_limit_loading: list[float]
    lower_limit_loading: list[float]
    wave_angle: list[float | None]
    wave_angle_impact: list[float | None]
    wave_height_impact: list[float | None]


class NaturalStoneOutputLocation(DikernelOutputLocation):
    z_position: float
    resistance: float
    outer_slope: list[float]
    slope_upper_level: list[float]
    slope_upper_position: list[float]
    slope_lower_level: list[float]
    slope_lower_position: list[float]
    loading_revetment: list[float]
    surf_similarity_parameter: list[float]
    wave_steepness_deep_water: list[float]
    upper_limit_loading: list[float]
    lower_limit_loading: list[float]
    depth_maximum_wave_load: list[float]
    distance_maximum_wave_elevation: list[float]
    normative_width_of_wave_impact: list[float]
    hydrodynamic_load: list[float | None]
    wave_angle: list[float | None]
    wave_angle_impact: list[float | None]
    reference_time_degradation: list[float | None]
    reference_degradation: list[float | None]
