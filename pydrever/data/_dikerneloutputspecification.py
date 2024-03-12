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
from pydrever.data._calculationmethods import CalculationMethod
from pydrever.data._dikernelcalculationsettings import CalculationSettings


class TopLayerSpecification:
    """
    Base class to specify the toplayer characteristics and desired calculations.
    """

    def __init__(
        self,
        calculation_method: CalculationMethod,
        type: TopLayerType,
    ) -> TopLayerSpecification:
        self.calculation_method: CalculationMethod = calculation_method
        """[CalculationMethod] The calculation method - instance variable"""
        self.top_layer_type: TopLayerType = type
        """[TopLayerType] The type of toplayer at this location - instance variable"""
        self.initial_damage: float = None
        """[float] The type of toplayer at this location - instance variable"""


class OutputLocationSpecification:
    """
    Base class to specify the desired calculations and output.
    """

    def __init__(
        self,
        x_position: float,
        top_layer_specification: TopLayerSpecification,
        calculation_settings: CalculationSettings = None,
    ) -> OutputLocationSpecification:
        self.x_position: float = x_position
        """[float] The cross-shore position of the required calculation and output - instance variable"""
        self.top_layer_specification: TopLayerSpecification = top_layer_specification
        """[TopLayerSpecification] The specification of the toplayer and desired calculation"""
        self.calculation_settings: CalculationSettings = calculation_settings
        """[CalculationSettings] The calculation settings that need to be used for this calculation"""


class AsphaltLayerSpecification(TopLayerSpecification):
    def __init__(
        self,
        flexural_strength: float,
        soil_elasticity: float,
        upper_layer_thickness: float,
        upper_layer_stiffness_modulus: float,
    ) -> AsphaltLayerSpecification:
        """
        Creates an instance of the class to specify a calculation for an asphalt revetment.

        Args:
            flexural_strength (float): Break strength of the asphalt.
            soil_elasticity (float): Spring constant of the soil.
            upper_layer_thickness (float): Thickness of the asphalt upper layer.
            upper_layer_stiffness_modulus (float): Stiffness modulus of the upper layer.

        Returns:
            AsphaltLayerSpecification: An instance of the output specification class for asphalt revetments.
        """
        super().__init__(
            CalculationMethod.AsphaltWaveImpact,
            TopLayerType.WAB,
        )
        self.flexural_strength: float = flexural_strength
        self.soil_elasticity: float = soil_elasticity
        self.upper_layer_thickness: float = upper_layer_thickness
        self.upper_layer_elastic_modulus: float = upper_layer_stiffness_modulus
        self.sub_layer_thickness: float = None
        self.sub_layer_elastic_modulus: float = None
        self.fatigue_alpha: float = None
        self.fatigue_beta: float = None
        self.top_layer_stiffness_relation_nu: float = None


class NordicStoneLayerSpecification(TopLayerSpecification):
    def __init__(
        self,
        top_layer_thickness: float,
        relative_density: float,
    ) -> NordicStoneLayerSpecification:
        """
        Creates an instance of the class to specify a calculation for revetment made of nordic stones.

        Args:
            top_layer_thickness (float): Thickness of the stone top layer.
            relative_density (float): Relative density of the stones.

        Returns:
            NordicStoneLayerSpecification: An instance of the output specification class for nordic stones.
        """
        super().__init__(
            CalculationMethod.NaturalStone,
            TopLayerType.NordicStone,
        )
        self.top_layer_thickness: float = top_layer_thickness
        self.relative_density: float = relative_density


class GrassWaveImpactLayerSpecification(TopLayerSpecification):
    def __init__(
        self,
        top_layer_type: TopLayerType,
    ) -> GrassWaveImpactLayerSpecification:
        """
        Creates an instance of the class to specify a calculation for a grass cover revetment wave impact calculation.

        Args:
            top_layer_type (TopLayerType): Type of the toplayer.

        Returns:
            GrassWaveImpactLayerSpecification: An instance of the output specification class for a grass cover wave impact calculation.
        """
        super().__init__(CalculationMethod.GrassWaveImpact, top_layer_type)


class GrassOvertoppingLayerSpecification(TopLayerSpecification):
    def __init__(
        self,
        top_layer_type: TopLayerType,
    ) -> GrassOvertoppingLayerSpecification:
        """
        Creates an instance of the class to specify a calculation for a grass overtopping calculation.

        Args:
            top_layer_type (TopLayerType): Type of the toplayer.

        Returns:
            GrassOvertoppingLayerSpecification: An instance of the output specification class for a grass overtopping calculation.
        """
        super().__init__(
            CalculationMethod.GrassWaveOvertopping,
            top_layer_type,
        )
        self.increased_load_transition_alpha_m: float = None
        self.increased_load_transition_alpha_s: float = None


class GrassWaveRunupLayerSpecification(TopLayerSpecification):
    def __init__(
        self, outer_slope: float, top_layer_type: TopLayerType
    ) -> GrassWaveRunupLayerSpecification:
        """
        Creates an instance of the class to specify a calculation for a grass runup calculation.

        Args:
            outer_slope (float): Outer slope.
            top_layer_type (TopLayerType): Type of the toplayer

        Returns:
            GrassWaveRunupLayerSpecification: An instance of the output specification class for a grass runup calculation.
        """
        super().__init__(CalculationMethod.GrassWaveRunup, top_layer_type)

        self.outer_slope = outer_slope
        self.increased_load_transition_alpha_m: float = None
        self.increased_load_transition_alpha_s: float = None
        self.reduced_strength_transition_2p_gamma_b: float = None
        self.reduced_strength_transition_2p_gamma_f: float = None
