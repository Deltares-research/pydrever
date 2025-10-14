"""
Copyright (C) Stichting Deltares 2024. All rights reserved.

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
from pydrever.data._dikernelinput import DikeSchematization
from pydrever.data._dikerneloutputspecification import (
    OutputLocationSpecification,
    TopLayerSpecification,
)
from pydrever.data._dikernelcalculationsettings import CalculationSettings
from abc import ABC, abstractmethod
import numpy as numpy
import pydrever.data._data_validation as data_validation
from pydantic import BaseModel, ConfigDict, root_validator, Field


class RevetmentZoneDefinition(BaseModel, ABC):
    """
    This class acts as a base class for defining revetment zones. Each derived class
    should define a ethod that returns a list of output locations (x-positions).
    """

    model_config = ConfigDict(validate_assignment=True)

    include_schematization_coordinates: bool = False
    """ Determines whether the profile coordinates of the DikeSchematization are also returned when calling get_x_coordinates"""

    @abstractmethod
    def get_x_coordinates(self, dike_schematization: DikeSchematization) -> list[float]:
        """
        This method returns the x-locations where calculations should be performed.

        Args:
            dike_schematization (DikeSchematization): The dike schematization.

        Returns:
            list[float]: A list of x-locations
        """
        return []


class HorizontalRevetmentZoneDefinition(RevetmentZoneDefinition):
    """
    This class defines a revetment zone in a horizontal way, meaning that it can be used to
    define output locations based on a minimum and maximum x-location cross-shore to the dike.

    When creating this class, either the number of output points between this minimum and maximum
    should be provided, or a maximum cross-shore distance between the output points. This class
    will then automatically generate all x-locations for the output points.
    """

    x_min: float
    """The minimum x cross-shore coordinate of this revetment zone."""
    x_max: float
    """The maximum x cross-shore coordinate of this revetment zone."""
    nx: int | None = Field(gt=1, default=None)
    """The number of desired output locations."""
    dx_max: float | None = Field(gt=0.0, default=None)
    """The maximum distance between output locations."""

    @root_validator(pre=True)
    def validate_nr_or_dx_max(cls, values):
        data_validation.validate_greater_than(values=values, first_parameter_name="x_max", second_parameter_name="x_min")
        data_validation.validate_one_of_two_should_be_specified(values=values, first_parameter_name="nx", second_parameter_name="dx_max")
        return values

    def get_x_coordinates(self, dike_schematizaion: DikeSchematization):
        if self.nx is not None:
            nx = self.nx
        elif self.dx_max is not None:
            nx = numpy.ceil((self.x_max - self.x_min) / self.dx_max).astype(int) + 1
        else:
            # TODO: Throw? input is not specified correctly
            nx = 1

        x_coordinates = numpy.linspace(self.x_min, self.x_max, nx)
        if self.include_schematization_coordinates and dike_schematizaion is not None:
            x_coordinates = numpy.union1d(
                x_coordinates,
                [x for x in dike_schematizaion.x_positions if x < self.x_max and x > self.x_min],
            )

        return x_coordinates


class VerticalRevetmentZoneDefinition(RevetmentZoneDefinition):
    """
    This class defines a revetment zone in a vertical way, meaning that it can be used to
    define output locations based on a minimum and maximum elevation.

    When creating this class, either the number of output points between this minimum and maximum
    should be provided, or a maximum (vertical) distance between the output points should be provided.
    This class will then automatically generate all x-locations for the output points.
    """

    z_min: float
    """The minimum elevation of this revetment zone."""
    z_max: float
    """The maximum elevation of this revetment zone."""
    nz: int | None = Field(gt=1, default=None)
    """The number of (vertical) levels at which output is required."""
    dz_max: float | None = Field(gt=0.0, default=None)
    """The maximum (vertical) distance between output points."""

    @root_validator(pre=True)
    def validate_nr_or_dx_max(cls, values):
        data_validation.validate_greater_than(values=values, first_parameter_name="z_max", second_parameter_name="z_min")
        data_validation.validate_one_of_two_should_be_specified(values=values, first_parameter_name="nz", second_parameter_name="dz_max")
        return values

    def get_x_coordinates(self, dike_schematizaion: DikeSchematization, inner_slope: bool = False):
        x_coordaintes = numpy.array(dike_schematizaion.x_positions)
        z_coordaintes = numpy.array(dike_schematizaion.z_positions)
        filter_mask = (
            x_coordaintes <= dike_schematizaion.x_outer_crest if not inner_slope else x_coordaintes >= dike_schematizaion.x_outer_crest
        )
        x_dike = numpy.array(x_coordaintes[filter_mask])
        z_dike = numpy.array(z_coordaintes[filter_mask])

        if self.nz is not None:
            nz = self.nz
        elif self.dz_max is not None:
            nz = numpy.ceil((self.z_max - self.z_min) / self.dz_max).astype(int) + 1
        else:
            nz = 1
            # TODO: Throw an error? Input is not specified correctly.

        z_output_coordinates = numpy.linspace(self.z_min, self.z_max, nz)
        x_output_coordinates = numpy.interp(
            z_output_coordinates,
            z_dike,
            x_dike,
        )

        if self.include_schematization_coordinates and dike_schematizaion is not None:
            z_filter = numpy.logical_and(z_dike <= self.z_max, z_dike >= self.z_min)
            x_output_coordinates = numpy.union1d(
                x_output_coordinates,
                x_dike[z_filter],
            )
        return x_output_coordinates


class RevetmentZoneSpecification(BaseModel):
    """
    Specifies a revetment zone. This class holds a top layer specification
    and a revetment zone definition. Optionally also calculation settings specific
    for this revetment zone can be specified.

    The class offers also a method get_output_locations to generate desired output-/
    calculation locations, all with the same top layer specification and optional
    settings.
    """

    top_layer_specification: TopLayerSpecification
    """Specification of the top layer of this revetment zone."""
    zone_definition: RevetmentZoneDefinition
    """Specification of the geometry of the revetment zone (either vertical or horizontal)."""
    calculation_settings: CalculationSettings | None = None
    """Optionl settings that should be used when calculating along this revetment zone."""

    def get_output_locations(self, dike_schematization: DikeSchematization) -> list[OutputLocationSpecification]:
        """
        Automatically generates the desired output locations based on the specified zone_definition
        and top_layer_specification.

        Args:
            dike_schematization (DikeSchematization): The schematization of the dike, needed in order to generate locations based on the revetment zone definition.

        Returns:
            list[OutputLocationSpecification]: A list of output location specifications to be used by Dikernel.
        """
        x_output_locations = self.zone_definition.get_x_coordinates(dike_schematization)
        return [
            OutputLocationSpecification(
                x_position=x_location,
                top_layer_specification=self.top_layer_specification,
                calculation_settings=self.calculation_settings,
            )
            for x_location in x_output_locations
        ]
