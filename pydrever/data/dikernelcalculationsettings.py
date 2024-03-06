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
from pydrever.data.toplayertypes import TopLayerType
from pydrever.data.calculationmethods import CalculationMethod


class TopLayerSettings:
    """
    Base class for specification of a top layer.
    """

    def __init__(self, type: TopLayerType):
        self.top_layer_type: TopLayerType = type
        """The type of the top layer - instance variable."""


class AsphaltTopLayerSettings(TopLayerSettings):
    """
    Specification for an asphalt toplayer calculation.
    """

    def __init__(self) -> AsphaltTopLayerSettings:
        super().__init__(TopLayerType.WAB)
        self.stiffness_ratio_nu: float = None
        """The stiffness ratio nu of the asphalt top layer - instance variable."""
        self.fatigue_asphalt_alpha: float = None
        """The fatigue constant alpha of the asphalt top layer - instance variable."""
        self.fatigue_asphalt_beta: float = None
        """The fatigue constant beta of the asphalt top layer - instance variable."""


class GrasCoverCumulativeOverloadTopLayerSettings(TopLayerSettings):
    """
    Specification for a grass cover cumulative overload calculations.
    """

    def __init__(
        self, topLayerType: TopLayerType
    ) -> GrasCoverCumulativeOverloadTopLayerSettings:
        super().__init__(topLayerType)
        self.critical_cumulative_overload: float = None
        """The critical cumulative overload - instance variable."""
        self.critical_front_velocity: float = None
        """The critical front velocity - instance variable."""


class GrassCoverWaveImpactTopLayerSettings(TopLayerSettings):
    """
    Specification for a grass cover wave impact calculation.
    """

    def __init__(self, type: TopLayerType):
        super().__init__(type)
        self.stance_time_line_a: float = None
        """The stance time line constant a - instance variable."""
        self.stance_time_line_b: float = None
        """The stance time line constant b - instance variable."""
        self.stance_time_line_c: float = None
        """The stance time line constant c - instance variable."""


class NaturalStoneTopLayerSettings(TopLayerSettings):
    """
    Specification for a natural stone cover calculation.
    """

    def __init__(self):
        super().__init__(TopLayerType.NordicStone)
        self.stability_plunging_a: float = None
        """The plunging constant a - instance variable."""
        self.stability_plunging_b: float = None
        """The plunging constant b - instance variable."""
        self.stability_plunging_c: float = None
        """The plunging constant c - instance variable."""
        self.stability_plunging_n: float = None
        """The plunging constant n - instance variable."""
        self.stability_surging_a: float = None
        """The surging constant a - instance variable."""
        self.stability_surging_b: float = None
        """The surging constant b - instance variable."""
        self.stability_surging_c: float = None
        """The surging constant c - instance variable."""
        self.stability_surging_n: float = None
        """The surging constant n - instance variable."""
        self.xib: float = None


class CalculationSettings:
    """
    Base class for specification of calculation settings.
    """

    def __init__(
        self, calculationMethod: CalculationMethod, topLayers: list[TopLayerSettings]
    ):
        self.CalculationMethod: CalculationMethod = calculationMethod
        """The calculation method this setting is for - instance variable."""
        self.failure_number: float = None
        """The damage number that is considered to indicate failure of the revetment - instance variable."""
        self.top_layers_settings: list[TopLayerSettings] = topLayers
        """Calculation settings specific for this type of top layer - instance variable."""


class AsphaltCalculationSettings(CalculationSettings):
    """
    Class for specification of asphalt calculation settings.
    """

    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.AsphaltWaveImpact, topLayers)
        self.density_of_water: float = None
        """The density of the water - instance variable."""
        self.factor_ctm: float = None
        """The ctm factor - instance variable."""
        self.impact_number_c: float = None
        """The impact number c - instance variable."""
        self.width_factors: list[float, float] = None
        """A list of width factors - instance variable."""
        self.depth_factors: list[float, float] = None
        """A list of depth factors - instance variable."""
        self.impact_factors: list[float, float] = None
        """A list of impact factors - instance variable."""


class GrassWaveOvertoppingCalculationSettings(CalculationSettings):
    """
    Class for specification of wave overtopping calculation settings.
    """

    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveOvertopping, topLayers)
        self.acceleration_alpha_a_for_crest: float = None
        """The alpha a at the crest of the dike - instance variable."""
        self.acceleration_alpha_a_for_inner_slope: float = None
        """The alpha a at the inner slope of the dike - instance variable."""
        self.fixed_number_of_waves: int = None
        """Fixed number of waves - instance variable."""
        self.front_velocity_c_wo: float = None
        """The front velocity constant c of the overtopping wave - instance variable."""
        self.average_number_of_waves_factor_ctm: float = None
        """The ctm factor - instance variable."""
        self.DikeHeight: float = None
        """The height of the dike used in the overtopping calculation - instance variable."""


class GrassWaveImpactCalculationSettings(CalculationSettings):
    """
    Class for specification of wave impact calculation settings.
    """

    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveImpact, topLayers)
        self.loading_upper_limit: float = None
        """Upper limit of the loading - instance variable."""
        self.loading_lower_limit: float = None
        """Lower limit of the loading - instance variable."""
        self.wave_angle_impact_n: float = None
        """Wave angle impact constant n - instance variable."""
        self.wave_angle_impact_q: float = None
        """Wave angle impact constant q - instance variable."""
        self.wave_angle_impact_r: float = None
        """Wave angle impact constant r - instance variable."""
        self.te_max: float = None
        self.te_min: float = None


class GrassWaveRunupCalculationSettings(CalculationSettings):
    """
    Class for specification of wave runup calculation settings.
    """

    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveImpact, topLayers)
        self.average_number_of_waves_factor_ctm: float = None
        """The ctm factor - instance variable."""
        self.representative_wave_runup_2p_aru: float = None
        self.representative_wave_runup_2p_bru: float = None
        self.representative_wave_runup_2p_cru: float = None
        self.wave_angle_impact_a_beta: float = None
        self.wave_angle_impact_beta_max: float = None
        self.fixed_number_of_waves: int = None
        self.front_velocity_cu: float = None


class NaturalStoneCalculationSettings(CalculationSettings):
    """
    Class for specification of natural stone calculation settings.
    """

    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.NaturalStone, topLayers)
        self.distance_maximum_wave_elevation_a: float = None
        self.distance_maximum_wave_elevation_b: float = None
        self.slope_upper_level: float = None
        self.sLope_lower_level: float = None
        self.normative_width_of_wave_impact_a: float = None
        self.normative_width_of_wave_impact_b: float = None
        self.upper_limit_loading_a: float = None
        self.upper_limit_loading_b: float = None
        self.upper_limit_loading_c: float = None
        self.lower_limit_loading_a: float = None
        self.lower_limit_loading_b: float = None
        self.lower_limit_loading_c: float = None
        self.wave_angle_impact_beta_max: float = None
