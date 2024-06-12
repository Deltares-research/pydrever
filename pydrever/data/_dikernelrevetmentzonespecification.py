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

from pydantic import BaseModel, ConfigDict, root_validator


class RevetmentZoneDefinition(BaseModel, ABC):
    model_config = ConfigDict(validate_assignment=True)

    include_schematization_coordinates: bool = False

    @abstractmethod
    def get_x_coordinates(self, dike_schematization: DikeSchematization) -> list[float]:
        return None


class HorizontalRevetmentZoneDefinition(RevetmentZoneDefinition):
    x_min: float
    x_max: float
    nx: int | None = None
    dx_max: float | None = None

    @root_validator(pre=True)
    def validate_nr_or_dx_max(cls, values):
        nx_value = values["nx"] if "nx" in values else None
        dx_max_value = values["dx_max"] if "dx_max" in values else None
        if nx_value is not None and dx_max_value is not None:
            raise ValueError("Either nx or dx_max should be specified.")
        if nx_value is None and dx_max_value is None:
            raise ValueError("One of nx or dx_max should be specified.")

        return values

    def get_x_coordinates(self, dike_schematizaion: DikeSchematization):
        if self.nx is not None:
            nx = self.nx
        else:
            nx = numpy.ceil((self.x_max - self.x_min) / self.dx_max).astype(int) + 1

        x_coordinates = numpy.linspace(self.x_min, self.x_max, nx)
        if self.include_schematization_coordinates and dike_schematizaion is not None:
            x_coordinates = numpy.union1d(
                x_coordinates,
                [
                    x
                    for x in dike_schematizaion.x_positions
                    if x < self.x_max and x > self.x_min
                ],
            )

        return x_coordinates


class VerticalRevetmentZoneDefinition(RevetmentZoneDefinition):
    z_min: float
    z_max: float
    nz: int | None = None
    dz_max: float | None = None

    @root_validator(pre=True)
    def validate_nr_or_dx_max(cls, values):
        nz_value = values["nz"] if "nz" in values else None
        dz_max_value = values["dz_max"] if "dz_max" in values else None
        if nz_value is not None and dz_max_value is not None:
            raise ValueError("Either nz or dz_max should be specified.")
        if nz_value is None and dz_max_value is None:
            raise ValueError("One of nz or dz_max should be specified.")

        return values

    def get_x_coordinates(
        self, dike_schematizaion: DikeSchematization, inner_slope: bool = False
    ):
        x_coordaintes = numpy.array(dike_schematizaion.x_positions)
        z_coordaintes = numpy.array(dike_schematizaion.z_positions)
        filter_mask = (
            x_coordaintes <= dike_schematizaion.outer_crest
            if not inner_slope
            else x_coordaintes >= dike_schematizaion.outer_crest
        )
        x_dike = numpy.array(x_coordaintes[filter_mask])
        z_dike = numpy.array(z_coordaintes[filter_mask])

        if self.nz is not None:
            nz = self.nz
        else:
            nz = numpy.ceil((self.z_max - self.z_min) / self.dz_max).astype(int) + 1

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
    top_layer_specification: TopLayerSpecification
    zone_definition: RevetmentZoneDefinition
    calculation_settings: CalculationSettings | None = None

    def get_output_locations(
        self, dike_schematization: DikeSchematization
    ) -> list[OutputLocationSpecification]:
        x_output_locations = self.zone_definition.get_x_coordinates(dike_schematization)
        return [
            OutputLocationSpecification(
                x_position=x_location,
                top_layer_specification=self.top_layer_specification,
                calculation_settings=self.calculation_settings,
            )
            for x_location in x_output_locations
        ]
