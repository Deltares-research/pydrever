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

from pydrever.calculation._dikernel import _inputservices as _input_service
from pydrever.data import (
    DikernelInput,
    RevetmentZoneSpecification,
    HorizontalRevetmentZoneDefinition,
    VerticalRevetmentZoneDefinition,
    OutputLocationSpecification,
    DikeSchematization,
    TopLayerSpecification,
    TopLayerType,
)

import pytest


class TestTopLayerSpecification(TopLayerSpecification):
    test_field: str | None = None


@pytest.fixture
def top_layer_specification() -> TopLayerSpecification:
    return TestTopLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod)


@pytest.fixture
def valid_output_location_specification(
    top_layer_specification,
) -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=top_layer_specification,
    )


def test_get_output_locations_returns_output_locations(top_layer_specification):
    input = DikernelInput(None, None)
    spec1 = top_layer_specification.copy()
    spec1.test_field = "a"
    spec2 = top_layer_specification.copy()
    spec2.test_field = "b"
    input.output_locations = [
        OutputLocationSpecification(x_position=0.0, top_layer_specification=spec1),
        OutputLocationSpecification(x_position=1.0, top_layer_specification=spec2),
    ]

    locations = _input_service.get_output_locations_from_input(input)
    assert len(locations) == 2
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[0].top_layer_specification == spec1
    assert locations[1].top_layer_specification == spec2


def test_get_output_locations_returns_output_locations_from_zone(
    top_layer_specification,
):
    input = DikernelInput(None, None)
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=0.0, x_max=5.0, dx_max=1.0
            ),
            top_layer_specification=top_layer_specification,
        )
    ]

    locations = _input_service.get_output_locations_from_input(input)
    assert len(locations) == 6
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[2].x_position == 2.0
    assert locations[3].x_position == 3.0
    assert locations[4].x_position == 4.0
    assert locations[5].x_position == 5.0


def test_get_output_locations_returns_output_locations_from_zones(
    top_layer_specification,
):
    input = DikernelInput(None, None)
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=0.0, x_max=2.0, dx_max=1.0
            ),
            top_layer_specification=top_layer_specification,
        ),
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=3.0, x_max=5.0, dx_max=1.0
            ),
            top_layer_specification=top_layer_specification,
        ),
    ]

    locations = _input_service.get_output_locations_from_input(input)
    assert len(locations) == 6
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[2].x_position == 2.0
    assert locations[3].x_position == 3.0
    assert locations[4].x_position == 4.0
    assert locations[5].x_position == 5.0


def test_get_output_locations_returns_combined_output_locations(
    top_layer_specification,
):
    schematization = DikeSchematization(0.0, [0.0, 10.0], [0.0, 5.0], [1.0], 0.0, 10.0)
    input = DikernelInput(None, schematization)
    input.output_locations = [
        OutputLocationSpecification(
            x_position=0.0, top_layer_specification=top_layer_specification
        ),
        OutputLocationSpecification(
            x_position=1.0, top_layer_specification=top_layer_specification
        ),
    ]
    spec_horizontal = top_layer_specification.copy()
    spec_horizontal.test_field = "horizontal"
    spec_vertical = top_layer_specification.copy()
    spec_vertical.test_field = "vertical"
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            zone_definition=HorizontalRevetmentZoneDefinition(
                x_min=4.0, x_max=6.0, dx_max=1.0
            ),
            top_layer_specification=spec_horizontal,
        ),
        RevetmentZoneSpecification(
            zone_definition=VerticalRevetmentZoneDefinition(
                z_min=4.0, z_max=5.0, dz_max=0.5
            ),
            top_layer_specification=spec_vertical,
        ),
    ]

    locations = _input_service.get_output_locations_from_input(input)

    assert len(locations) == 8
    assert locations[0].x_position == 0.0
    assert locations[0].top_layer_specification == top_layer_specification
    assert locations[1].x_position == 1.0
    assert locations[1].top_layer_specification == top_layer_specification
    assert locations[2].x_position == 4.0
    assert locations[2].top_layer_specification == spec_horizontal
    assert locations[3].x_position == 5.0
    assert locations[3].top_layer_specification == spec_horizontal
    assert locations[4].x_position == 6.0
    assert locations[4].top_layer_specification == spec_horizontal
    assert locations[5].x_position == 8.0
    assert locations[5].top_layer_specification == spec_vertical
    assert locations[6].x_position == 9.0
    assert locations[6].top_layer_specification == spec_vertical
    assert locations[7].x_position == 10.0
    assert locations[7].top_layer_specification == spec_vertical
