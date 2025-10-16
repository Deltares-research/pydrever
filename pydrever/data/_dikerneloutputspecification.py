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
from pydrever.data._dikernelcalculationsettings import CalculationSettings
from pydrever.data._grassovertoppingcalculationtypes import GrassOvertoppingCalculationType
from pydrever.data._grasswaverunupcalculationtypes import GrassWaveRunupCalculationType
from pydantic import BaseModel, ConfigDict


class TopLayerSpecification(BaseModel):
    """
    Base class to specify the toplayer characteristics and desired calculations.
    """

    model_config = ConfigDict(validate_assignment=True)

    top_layer_type: TopLayerType | None = None
    """[TopLayerType] The type of toplayer at this location - instance variable"""
    initial_damage: float | None = None
    """[float] The type of toplayer at this location - instance variable"""


class OutputLocationSpecification(BaseModel):
    """
    class to specify the desired calculations and output.
    """

    model_config = ConfigDict(validate_assignment=True)

    x_position: float
    """[float] The cross-shore position of the required calculation and output - instance variable"""
    top_layer_specification: TopLayerSpecification
    """[TopLayerSpecification] The specification of the toplayer and desired calculation"""
    calculation_settings: CalculationSettings | None = None
    """[CalculationSettings] The calculation settings that need to be used for this calculation"""


class AsphaltLayerSpecification(TopLayerSpecification):
    flexural_strength: float
    soil_elasticity: float
    upper_layer_thickness: float
    upper_layer_elasticity_modulus: float
    sub_layer_thickness: float | None = None
    sub_layer_elastic_modulus: float | None = None
    fatigue_asphalt_alpha: float | None = None
    """The fatigue constant alpha of the asphalt top layer - instance variable."""
    fatigue_asphalt_beta: float | None = None
    """The fatigue constant beta of the asphalt top layer - instance variable."""
    stiffness_ratio_nu: float | None = None
    """The stiffness ratio nu of the asphalt top layer - instance variable."""


class NordicStoneLayerSpecification(TopLayerSpecification):
    """
    Specification of a nordic stone top layer.
    """

    top_layer_thickness: float
    """Thickness of the top layer in meters."""
    relative_density: float
    """Relative density of the stone material."""


class GrassWaveImpactLayerSpecification(TopLayerSpecification):
    """
    Specification of a grass top layer for wave impact calculations.
    """

    pass


class GrassOvertoppingLayerSpecification(TopLayerSpecification):
    """
    Specification of a grass top layer for wave overtopping calculations.
    """

    calculation_type: GrassOvertoppingCalculationType = GrassOvertoppingCalculationType.Analytical
    increased_load_transition_alpha_m: float | None = None
    increased_load_transition_alpha_s: float | None = None


class GrassWaveRunupLayerSpecification(TopLayerSpecification):
    """
    Specification of a grass top layer for wave runup calculations.
    """

    calculation_type: GrassWaveRunupCalculationType = GrassWaveRunupCalculationType.AnalyticalBattjesGroenendijk
    outer_slope: float
    increased_load_transition_alpha_m: float | None = None
    increased_load_transition_alpha_s: float | None = None
