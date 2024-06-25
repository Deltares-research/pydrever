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
from pydantic import BaseModel, ConfigDict, root_validator

import numpy as numpy
from pydrever.data._dikerneloutputspecification import (
    OutputLocationSpecification,
    TopLayerSpecification,
)
from pydrever.data._dikeschematization import DikeSchematization
from pydrever.data._dikernelrevetmentzonespecification import (
    RevetmentZoneSpecification,
)
from pydrever.data._dikernelcalculationsettings import CalculationSettings
from pydrever.data import _data_validation as data_validation


class HydrodynamicConditions(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    time_steps: list[float]
    """list of timesteps."""
    water_levels: list[float]
    """list of waterlevels"""
    wave_heights: list[float]
    """list of significant wave heights (Hs)"""
    wave_periods: list[float]
    """list of wave periods"""
    wave_directions: list[float]
    """list of wave directions"""
    # TODO: Maybe automatically correct the wave directions?

    @root_validator(pre=True)
    def validate_nr_or_dx_max(cls, values):
        data_validation.validate_hydrodynamics_length(values=values)
        return values


class DikernelInput:
    def __init__(
        self,
        hydrodynamic_input: HydrodynamicConditions,
        dike_schematization: DikeSchematization,
    ):
        """
        Constructor for the DikernelInput class.

        Args:
            hydrodynamicInput (HydrodynamicInput): object containing the hydrodynamic input
            dikeSchematization (DikeSchematization): object containing the dike schematization
        """
        self.hydrodynamic_input: HydrodynamicConditions = hydrodynamic_input
        """Hydrodynamic input specification - instance variable."""
        self.dike_schematization: DikeSchematization = dike_schematization
        """Schematization of the dike cross-shore profile and characteristic points - instance variable."""
        self.output_locations: list[OutputLocationSpecification] = None
        """Specification of the desired calculation and output locations - instance variable."""
        self.output_revetment_zones: list[RevetmentZoneSpecification] = None
        """Specification of the desired calculation and output locations by zone - instance variable."""
        self.settings: list[CalculationSettings] = None
        """List of calculation settings that are used for the various types of revetments - instance variable."""
        self.start_time: float = None
        """Optional start time of the calculation - instance variable."""
        self.stop_time: float = None
        """Optional stop time of the calculation - instance variable."""
        self.output_time_steps: list[float] = None
        """Optional list of desired output time steps. This will add output times to the calculation - instance variable."""
        # Results are not filtered based on this list (cumulative values such as the damage increment in the results would not make sense anymore).

    def add_output_location(
        self, x_location: float, top_layer_specification: TopLayerSpecification
    ):
        """
        Adds the specified output location to the list of output locations.

        Args:
            x_location (float): Cross-shore coordinate of the desired output location.
            top_layer_specification (TopLayerSpecification): Specification of the top layer.
        """
        new_output_location = OutputLocationSpecification(
            x_position=x_location, top_layer_specification=top_layer_specification
        )
        if self.output_locations is None:
            self.output_locations = [new_output_location]
        else:
            self.output_locations.append(new_output_location)
