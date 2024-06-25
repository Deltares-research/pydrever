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

from pydrever.data import (
    RevetmentZoneSpecification,
    AsphaltLayerSpecification,
    DikeSchematization,
    HorizontalRevetmentZoneDefinition,
    VerticalRevetmentZoneDefinition,
    TopLayerType,
)
import pytest
from pydantic import ValidationError


def test_asphalt_zone():
    flexural_strength = 1.0
    soil_elasticity = 2.0
    upper_layer_thickness = 33.0
    elastic_modulus = 4.0
    x_min = 1.0
    x_max = 6.0
    dx_max = 2.0
    zone_definition = HorizontalRevetmentZoneDefinition(
        x_min=x_min, x_max=x_max, dx_max=dx_max
    )
    top_layer = AsphaltLayerSpecification(
        top_layer_type=TopLayerType.Asphalt,
        flexural_strength=flexural_strength,
        soil_elasticity=soil_elasticity,
        upper_layer_thickness=upper_layer_thickness,
        upper_layer_elasticity_modulus=elastic_modulus,
    )
    zone = RevetmentZoneSpecification(
        zone_definition=zone_definition, top_layer_specification=top_layer
    )
    assert zone.top_layer_specification.flexural_strength == flexural_strength
    assert zone.top_layer_specification.soil_elasticity == soil_elasticity
    assert zone.top_layer_specification.upper_layer_thickness == upper_layer_thickness
    assert (
        zone.top_layer_specification.upper_layer_elasticity_modulus == elastic_modulus
    )
    assert zone.zone_definition.x_min == x_min
    assert zone.zone_definition.x_max == x_max
    assert zone.zone_definition.dx_max == dx_max


def test_asphalt_zone_creates_locations():
    flexural_strength = 1.0
    soil_elasticity = 2.0
    upper_layer_thickness = 33.0
    elastic_modulus = 4.0
    x_min = 1.0
    x_max = 6.0
    nx = 6
    zone_definition = HorizontalRevetmentZoneDefinition(x_min=x_min, x_max=x_max, nx=nx)
    top_layer = AsphaltLayerSpecification(
        top_layer_type=TopLayerType.Asphalt,
        flexural_strength=flexural_strength,
        soil_elasticity=soil_elasticity,
        upper_layer_thickness=upper_layer_thickness,
        upper_layer_elasticity_modulus=elastic_modulus,
    )
    zone = RevetmentZoneSpecification(
        zone_definition=zone_definition, top_layer_specification=top_layer
    )
    locations = zone.get_output_locations(None)
    assert len(locations) == 6
    assert locations[0].top_layer_specification.flexural_strength == flexural_strength
    assert locations[0].top_layer_specification.soil_elasticity == soil_elasticity
    assert (
        locations[0].top_layer_specification.upper_layer_thickness
        == upper_layer_thickness
    )
    assert (
        locations[0].top_layer_specification.upper_layer_elasticity_modulus
        == elastic_modulus
    )


def test_horizontal_zone_definition_creates_coordinates_with_dx():
    zone = HorizontalRevetmentZoneDefinition(x_min=4.0, x_max=10.0, dx_max=2.0)
    x_coordinates = zone.get_x_coordinates(None)
    assert len(x_coordinates) == 4
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 6.0
    assert x_coordinates[2] == 8.0
    assert x_coordinates[3] == 10.0


@pytest.mark.parametrize(("nx"), ((2, 3, 4, 5, 6, 7, 8, 9, 10)))
def test_horizontal_zone_definition_creates_correct_number_of_coordinates_with_nx(nx):
    zone = HorizontalRevetmentZoneDefinition(x_min=4.0, x_max=10.0, nx=nx)
    x_coordinates = zone.get_x_coordinates(None)
    assert len(x_coordinates) == nx


def test_horizontal_zone_definition_creates_coordinates_with_nx():
    zone = HorizontalRevetmentZoneDefinition(x_min=4.0, x_max=10.0, nx=7)
    x_coordinates = zone.get_x_coordinates(None)
    assert len(x_coordinates) == 7
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 6.0
    assert x_coordinates[3] == 7.0
    assert x_coordinates[4] == 8.0
    assert x_coordinates[5] == 9.0
    assert x_coordinates[6] == 10.0


def test_horizontal_zone_includes_profile_points():
    zone = HorizontalRevetmentZoneDefinition(x_min=4.0, x_max=7.0, nx=4)
    zone.include_schematization_coordinates = True
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 5.5, 10.0],
        z_positions=[-5.0, 0.0, 5.0],
        roughnesses=[1.0, 1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 5
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 5.5
    assert x_coordinates[3] == 6.0
    assert x_coordinates[4] == 7.0


def test_horizontal_zone_excludes_profile_points():
    zone = HorizontalRevetmentZoneDefinition(x_min=4.0, x_max=7.0, nx=4)
    zone.include_schematization_coordinates = False
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 5.5, 10.0],
        z_positions=[-5.0, 0.0, 5.0],
        roughnesses=[1.0, 1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 4
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 6.0
    assert x_coordinates[3] == 7.0


def test_horizontal_zone_definition_throws_on_wrong_nz():
    with pytest.raises(ValidationError) as v_error:
        o = HorizontalRevetmentZoneDefinition(x_min=0.2, x_max=5.0, nx=-1)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "nx"


def test_horizontal_zone_wrong_z_values_throws():
    with pytest.raises(ValueError) as v_error:
        o = HorizontalRevetmentZoneDefinition(x_min=3.0, x_max=1.0, dx_max=0.5)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert (
        errors[0]["msg"]
        == "Value error, x_max (1.0) should be greater than x_min (3.0)"
    )


def test_vertical_zone_definition_creates_coordinates_with_dz():
    zone = VerticalRevetmentZoneDefinition(z_min=-2.0, z_max=2.0, dz_max=2.0)
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 10.0],
        z_positions=[-5.0, 5.0],
        roughnesses=[1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 3
    assert x_coordinates[0] == 3.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 7.0


def test_vertical_zone_definition_creates_coordinates_with_nz():
    zone = VerticalRevetmentZoneDefinition(z_min=-2.0, z_max=2.0, nz=3)
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 10.0],
        z_positions=[-5.0, 5.0],
        roughnesses=[1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 3
    assert x_coordinates[0] == 3.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 7.0


@pytest.mark.parametrize(("nz"), ((2, 3, 4, 5, 6, 7, 8, 9, 10)))
def test_vertical_zone_definition_creates_correct_number_of_coordinates_with_nz(nz):
    zone = VerticalRevetmentZoneDefinition(z_min=-2.0, z_max=2.0, nz=nz)
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 10.0],
        z_positions=[-5.0, 5.0],
        roughnesses=[1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == nz


def test_vertical_zone_definition_creates_coordinates_with_dz_inner_slope():
    zone = VerticalRevetmentZoneDefinition(z_min=-2.0, z_max=2.0, dz_max=2.0)
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 10.0, 15.0],
        z_positions=[-5.0, 5.0, -3.0],
        roughnesses=[1.0, 1.0],
        x_outer_toe=0.0,
        x_outer_crest=10.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 3
    assert x_coordinates[0] == 3.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 7.0


def test_vertical_zone_includes_profile_points():
    zone = VerticalRevetmentZoneDefinition(z_min=4.0, z_max=7.0, nz=4)
    zone.include_schematization_coordinates = True
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 5.5, 10.0],
        z_positions=[0.0, 5.5, 10.0],
        roughnesses=[1.0, 1.0],
        x_outer_toe=0.0,
        x_outer_crest=15.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 5
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 5.5
    assert x_coordinates[3] == 6.0
    assert x_coordinates[4] == 7.0


def test_vertical_zone_excludes_profile_points():
    zone = VerticalRevetmentZoneDefinition(z_min=4.0, z_max=7.0, nz=4)
    zone.include_schematization_coordinates = False
    dike_schem = DikeSchematization(
        dike_orientation=0.0,
        x_positions=[0.0, 5.5, 10.0],
        z_positions=[0.0, 5.5, 10.0],
        roughnesses=[1.0, 1.0],
        x_outer_toe=0.0,
        x_outer_crest=15.0,
    )
    x_coordinates = zone.get_x_coordinates(dike_schem)
    assert len(x_coordinates) == 4
    assert x_coordinates[0] == 4.0
    assert x_coordinates[1] == 5.0
    assert x_coordinates[2] == 6.0
    assert x_coordinates[3] == 7.0


def test_vertical_zone_definition_throws_on_wrong_nz():
    with pytest.raises(ValidationError) as v_error:
        o = VerticalRevetmentZoneDefinition(z_min=0.2, z_max=5.0, nz=-1)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == "nz"


def test_vertical_zone_wrong_z_values_throws():
    with pytest.raises(ValueError) as v_error:
        o = VerticalRevetmentZoneDefinition(z_min=3.0, z_max=1.0, dz_max=0.5)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert (
        errors[0]["msg"]
        == "Value error, z_max (1.0) should be greater than z_min (3.0)"
    )
