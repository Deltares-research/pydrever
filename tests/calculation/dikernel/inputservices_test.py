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

from pydrever.calculation.dikernel import inputservices as input_service
from pydrever.data import (
    DikernelInput,
    RevetmentZoneSpecification,
    HorizontalRevetmentZoneDefinition,
    VerticalRevetmentZoneDefinition,
    OutputLocationSpecification,
    DikeSchematization,
)


def test_get_output_locations_returns_output_locations():
    input = DikernelInput(None, None)
    input.output_locations = [
        OutputLocationSpecification(0.0, None),
        OutputLocationSpecification(1.0, "test"),
    ]

    locations = input_service.get_output_locations_from_input(input)
    assert len(locations) == 2
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[0].top_layer_specification is None
    assert locations[1].top_layer_specification == "test"


def test_get_output_locations_returns_output_locations_from_zone():
    input = DikernelInput(None, None)
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(0.0, 5.0, dx_max=1.0), None
        )
    ]

    locations = input_service.get_output_locations_from_input(input)
    assert len(locations) == 6
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[2].x_position == 2.0
    assert locations[3].x_position == 3.0
    assert locations[4].x_position == 4.0
    assert locations[5].x_position == 5.0


def test_get_output_locations_returns_output_locations_from_zones():
    input = DikernelInput(None, None)
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(0.0, 2.0, dx_max=1.0), None
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(3.0, 5.0, dx_max=1.0), None
        ),
    ]

    locations = input_service.get_output_locations_from_input(input)
    assert len(locations) == 6
    assert locations[0].x_position == 0.0
    assert locations[1].x_position == 1.0
    assert locations[2].x_position == 2.0
    assert locations[3].x_position == 3.0
    assert locations[4].x_position == 4.0
    assert locations[5].x_position == 5.0


def test_get_output_locations_returns_combined_output_locations():
    schematization = DikeSchematization(0.0, [0.0, 10.0], [0.0, 5.0], [1.0], 0.0, 10.0)
    input = DikernelInput(None, schematization)
    input.output_locations = [
        OutputLocationSpecification(0.0, top_layer_specification=None),
        OutputLocationSpecification(1.0, top_layer_specification="test"),
    ]
    input.output_revetment_zones = [
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(4.0, 6.0, dx_max=1.0),
            top_layer_specification="test horizontal",
        ),
        RevetmentZoneSpecification(
            VerticalRevetmentZoneDefinition(4.0, 5.0, dz_max=0.5),
            top_layer_specification="test vertical",
        ),
    ]

    locations = input_service.get_output_locations_from_input(input)

    assert len(locations) == 8
    assert locations[0].x_position == 0.0
    assert locations[0].top_layer_specification == None
    assert locations[1].x_position == 1.0
    assert locations[1].top_layer_specification == "test"
    assert locations[2].x_position == 4.0
    assert locations[2].top_layer_specification == "test horizontal"
    assert locations[3].x_position == 5.0
    assert locations[3].top_layer_specification == "test horizontal"
    assert locations[4].x_position == 6.0
    assert locations[4].top_layer_specification == "test horizontal"
    assert locations[5].x_position == 8.0
    assert locations[5].top_layer_specification == "test vertical"
    assert locations[6].x_position == 9.0
    assert locations[6].top_layer_specification == "test vertical"
    assert locations[7].x_position == 10.0
    assert locations[7].top_layer_specification == "test vertical"
