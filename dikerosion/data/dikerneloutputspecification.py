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
from dikerosion.data.toplayertypes import TopLayerType
from dikerosion.data.calculationmethods import CalculationMethod


class OutputLocationSpecification:
    """
    Base class to specify the desired calculations and output.
    """

    def __init__(
        self,
        x_position: float,
        calculation_method: CalculationMethod,
        top_layer_type: TopLayerType,
    ) -> OutputLocationSpecification:
        self.x_position: float = x_position
        """[float] The cross-shore position of the required calculation and output - instance variable"""
        self.calculation_method: CalculationMethod = calculation_method
        """[CalculationMethod] The calculation method - instance variable"""
        self.top_layer_type: TopLayerType = top_layer_type
        """[TopLayerType] The type of toplayer at this location - instance variable"""
        self.initial_damage: float = None
        """[float] The type of toplayer at this location - instance variable"""


class AsphaltOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        flexural_strength: float,
        soil_elasticity: float,
        upper_layer_thickness: float,
        upper_layer_stiffness_modulus: float,
    ) -> AsphaltOutputLocationSpecification:
        """
        Creates an instance of the class to specify a calculation for an asphalt revetment.

        Args:
            x_position (float): Cross-shore position of the location.
            flexural_strength (float): Break strength of the asphalt.
            soil_elasticity (float): Spring constant of the soil.
            upper_layer_thickness (float): Thickness of the asphalt upper layer.
            upper_layer_stiffness_modulus (float): Stiffness modulus of the upper layer.

        Returns:
            AsphaltOutputLocationSpecification: An instance of the output specification class for asphalt revetments.
        """
        super().__init__(
            x_position,
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


class NordicStoneOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        top_layer_thickness: float,
        relative_density: float,
    ) -> NordicStoneOutputLocationSpecification:
        """
        Creates an instance of the class to specify a calculation for revetment made of nordic stones.

        Args:
            x_position (float): Cross-shore position of the location.
            top_layer_thickness (float): Thickness of the stone top layer.
            relative_density (float): Relative density of the stones.

        Returns:
            NordicStoneOutputLocationSpecification: An instance of the output specification class for nordic stones.
        """
        super().__init__(
            x_position,
            CalculationMethod.NaturalStone,
            TopLayerType.NordicStone,
        )
        self.top_layer_thickness: float = top_layer_thickness
        self.relative_density: float = relative_density


class GrassWaveImpactOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self, x_position: float, top_layer_type: TopLayerType
    ) -> GrassWaveImpactOutputLocationSpecification:
        """
        Creates an instance of the class to specify a calculation for a grass cover revetment wave impact calculation.

        Args:
            x_position (float): Cross-shore position of the location.
            top_layer_type (TopLayerType): Type of the toplayer.

        Returns:
            GrassWaveImpactOutputLocationSpecification: An instance of the output specification class for a grass cover wave impact calculation.
        """
        super().__init__(x_position, CalculationMethod.GrassWaveImpact, top_layer_type)


class GrassOvertoppingOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        top_layer_type: TopLayerType,
    ) -> GrassOvertoppingOutputLocationSpecification:
        """
        Creates an instance of the class to specify a calculation for a grass overtopping calculation.

        Args:
            x_position (float): Cross-shore position of the location.
            top_layer_type (TopLayerType): Type of the toplayer.

        Returns:
            GrassOvertoppingOutputLocationSpecification: An instance of the output specification class for a grass overtopping calculation.
        """
        super().__init__(
            x_position,
            CalculationMethod.GrassWaveOvertopping,
            top_layer_type,
        )
        self.increased_load_transition_alpha_m: float = None
        self.increased_load_transition_alpha_s: float = None


class GrassWaveRunupOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self, x_position: float, outer_slope: float, top_layer_type: TopLayerType
    ) -> OutputLocationSpecification:
        super().__init__(x_position, CalculationMethod.GrassWaveRunup, top_layer_type)

        self.outer_slope = outer_slope
        self.increased_load_transition_alpha_m: float = None
        self.increased_load_transition_alpha_s: float = None
        self.reduced_strength_transition_2p_gamma_b: float = None
        self.reduced_strength_transition_2p_gamma_f: float = None
