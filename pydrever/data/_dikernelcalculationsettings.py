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

from __future__ import annotations
from pydrever.data._toplayertypes import TopLayerType
from pydantic import BaseModel, ConfigDict


class TopLayerSettings(BaseModel):
    """
    Base class for specification of a top layer.
    """

    model_config = ConfigDict(validate_assignment=True)

    top_layer_type: TopLayerType
    """The type of the top layer - instance variable."""


class GrassCumulativeOverloadTopLayerSettings(TopLayerSettings):
    """
    Specification for a grass cover cumulative overload calculations.
    """

    critical_cumulative_overload: float | None = None
    """The critical cumulative overload - instance variable."""
    critical_front_velocity: float | None = None
    """The critical front velocity - instance variable."""


class GrassWaveImpactTopLayerSettings(TopLayerSettings):
    """
    Specification for a grass cover wave impact calculation.
    """

    stance_time_line_a: float | None = None
    """The stance time line constant a - instance variable."""
    stance_time_line_b: float | None = None
    """The stance time line constant b - instance variable."""
    stance_time_line_c: float | None = None
    """The stance time line constant c - instance variable."""


class NaturalStoneTopLayerSettings(TopLayerSettings):
    """
    Specification for a natural stone cover calculation.
    """

    stability_plunging_a: float | None = None
    """The plunging constant a - instance variable."""
    stability_plunging_b: float | None = None
    """The plunging constant b - instance variable."""
    stability_plunging_c: float | None = None
    """The plunging constant c - instance variable."""
    stability_plunging_n: float | None = None
    """The plunging constant n - instance variable."""
    stability_surging_a: float | None = None
    """The surging constant a - instance variable."""
    stability_surging_b: float | None = None
    """The surging constant b - instance variable."""
    stability_surging_c: float | None = None
    """The surging constant c - instance variable."""
    stability_surging_n: float | None = None
    """The surging constant n - instance variable."""
    xib: float | None = None


class CalculationSettings(BaseModel):
    """
    Base class for specification of calculation settings.
    """

    model_config = ConfigDict(validate_assignment=True)

    failure_number: float | None = None
    """The damage number that is considered to indicate failure of the revetment - instance variable."""
    top_layers_settings: list[TopLayerSettings] | None = None
    """Calculation settings specific for this type of top layer - instance variable."""


class AsphaltCalculationSettings(CalculationSettings):
    """
    Class for specification of asphalt calculation settings.
    """

    density_of_water: float | None = None
    """The density of the water - instance variable."""
    factor_ctm: float | None = None
    """The ctm factor - instance variable."""
    impact_number_c: float | None = None
    """The impact number c - instance variable."""
    width_factors: list[list[float]] | None = None
    """A list of width factors - instance variable."""
    depth_factors: list[list[float]] | None = None
    """A list of depth factors - instance variable."""
    impact_factors: list[list[float]] | None = None
    """A list of impact factors - instance variable."""


class GrassWaveOvertoppingCalculationSettings(CalculationSettings):
    """
    Class for specification of wave overtopping calculation settings.
    """

    acceleration_alpha_a_for_crest: float | None = None
    """The alpha a at the crest of the dike - instance variable."""
    acceleration_alpha_a_for_inner_slope: float | None = None
    """The alpha a at the inner slope of the dike - instance variable."""
    fixed_number_of_waves: int | None = None
    """Fixed number of waves - instance variable."""
    front_velocity_c_wo: float | None = None
    """The front velocity constant c of the overtopping wave - instance variable."""
    average_number_of_waves_factor_ctm: float | None = None
    """The ctm factor - instance variable."""
    dike_height: float | None = None
    """The height of the dike used in the overtopping calculation - instance variable."""


class GrassWaveImpactCalculationSettings(CalculationSettings):
    """
    Class for specification of wave impact calculation settings.
    """

    loading_upper_limit: float | None = None
    """Upper limit of the loading - instance variable."""
    loading_lower_limit: float | None = None
    """Lower limit of the loading - instance variable."""
    wave_angle_impact_n: float | None = None
    """Wave angle impact constant n - instance variable."""
    wave_angle_impact_q: float | None = None
    """Wave angle impact constant q - instance variable."""
    wave_angle_impact_r: float | None = None
    """Wave angle impact constant r - instance variable."""
    te_max: float | None = None
    te_min: float | None = None


class GrassWaveRunupCalculationSettings(CalculationSettings):
    """
    Class for specification of wave runup calculation settings.
    """

    average_number_of_waves_factor_ctm: float = None
    """The ctm factor - instance variable."""
    representative_wave_runup_2p_aru: float | None = None
    representative_wave_runup_2p_bru: float | None = None
    representative_wave_runup_2p_cru: float | None = None
    wave_angle_impact_a_beta: float | None = None
    wave_angle_impact_beta_max: float | None = None
    fixed_number_of_waves: int | None = None
    front_velocity_cu: float | None = None


class NaturalStoneCalculationSettings(CalculationSettings):
    """
    Class for specification of natural stone calculation settings.
    """

    distance_maximum_wave_elevation_a: float | None = None
    distance_maximum_wave_elevation_b: float | None = None
    slope_upper_level: float | None = None
    sLope_lower_level: float | None = None
    normative_width_of_wave_impact_a: float | None = None
    normative_width_of_wave_impact_b: float | None = None
    upper_limit_loading_a: float | None = None
    upper_limit_loading_b: float | None = None
    upper_limit_loading_c: float | None = None
    lower_limit_loading_a: float | None = None
    lower_limit_loading_b: float | None = None
    lower_limit_loading_c: float | None = None
    wave_angle_impact_beta_max: float | None = None
