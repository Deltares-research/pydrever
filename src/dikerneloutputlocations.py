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

from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod


class OutputLocationSpecification:
    def __init__(
        self,
        x_position: float,
        initial_damage: float,
        calculation_method: CalculationMethod,
        top_layer_type: TopLayerType,
    ):
        self.x_position = x_position
        self.initial_damage = initial_damage
        self.calculation_method = calculation_method
        self.top_layer_type = top_layer_type


class AsphaltOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        break_strent_asphalt: float,
        spring_constant_soil: float,
        top_layer_thickness: float,
        top_layer_stiffness_modulus: float,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.AsphaltWaveImpact,
            TopLayerType.WAB,
        )
        self.flexural_strent = break_strent_asphalt
        self.soil_elasticity = spring_constant_soil
        self.top_layer_thickness = top_layer_thickness
        self.top_layer_elastic_modulus = top_layer_stiffness_modulus
        self.sub_layer_thickness = None
        self.sub_layer_elastic_modulus = None
        self.fatigue_alpha = None
        self.fatigue_beta = None
        self.top_layer_stiffness_relation_nu = None


class NordicStoneOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        top_layer_thickness: float,
        relative_density: float,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.NaturalStone,
            TopLayerType.NordicStone,
        )
        self.top_layer_thickness = top_layer_thickness
        self.relative_density = relative_density


class GrassWaveImpactOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self, x_position: float, begin_damage: float, top_layer_type: TopLayerType
    ):
        super().__init__(
            x_position, begin_damage, CalculationMethod.GrassWaveImpact, top_layer_type
        )


class GrassOvertoppingOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        top_layer_type: TopLayerType,
        alpha_m: float = 1.0,
        alpha_s: float = 1.0,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.GrassWaveOvertopping,
            top_layer_type,
        )
        self.increased_load_transition_alpha_m = alpha_m
        self.increased_load_transition_alpha_s = alpha_s
