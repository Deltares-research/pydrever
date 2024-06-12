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

import pytest

from pydrever.data import (
    NaturalStoneOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassWaveImpactOutputLocation,
    GrassWaveRunupOutputLocation,
    GrassOvertoppingOutputLocation,
)

from pydantic import ValidationError


def test_naturalstoneoutputlocationthrowsonmissinginput():
    with pytest.raises(ValueError):
        o = NaturalStoneOutputLocation(damage_development=[1.0, 2.0])


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("damage_development", None),
        ("damage_increment", 1.0),
        ("depth_maximum_wave_load", "wrong type"),
        ("distance_maximum_wave_elevation", "[1.0]"),
        ("hydrodynamic_load", False),
        ("loading_revetment", [False, 125.432, "str"]),
        ("lower_limit_loading", [None, 14.543]),
        ("normative_width_of_wave_impact", [1.0, 43, "True"]),
        ("outer_slope", "s;p[e]"),
        ("reference_degradation", None),
        ("reference_time_degradation", [1.0, "earlier"]),
        ("resistance", "False"),
        ("slope_lower_level", [None, 1.0, True]),
        ("slope_lower_position", [1.0, ""]),
        ("slope_upper_level", True),
        ("slope_upper_position", None),
        ("surf_similarity_parameter", 7),
        ("time_of_failure", "a1.5422"),
        ("upper_limit_loading", ["too high"]),
        ("wave_angle", 15),
        ("wave_angle_impact", 16),
        ("wave_steepness_deep_water", 17),
        ("x_position", "False"),
        ("z_position", "34c5.015"),
    ],
)
def test_naturalstoneoutputlocationthrowsonwronginput(field_name, value):
    input = {
        "damage_development": [1.0],
        "damage_increment": [1.0],
        "depth_maximum_wave_load": [1.0],
        "distance_maximum_wave_elevation": [1.0],
        "hydrodynamic_load": [1.0],
        "loading_revetment": [1.0],
        "lower_limit_loading": [1.0],
        "normative_width_of_wave_impact": [1.0],
        "outer_slope": [2.0],
        "reference_degradation": [1.0],
        "reference_time_degradation": [1.0],
        "resistance": 1.0,
        "slope_lower_level": [1.0],
        "slope_lower_position": [1.0],
        "slope_upper_level": [1.0],
        "slope_upper_position": [1.0],
        "surf_similarity_parameter": [1.0],
        "time_of_failure": None,
        "upper_limit_loading": [1.0],
        "wave_angle": [1.0],
        "wave_angle_impact": [1.0],
        "wave_steepness_deep_water": [1.0],
        "x_position": 1.23,
        "z_position": 2.345,
    }

    input[field_name] = value
    with pytest.raises(ValidationError) as v_error:
        o = NaturalStoneOutputLocation(**input)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == field_name


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("x_position", "a3.r2"),
        ("time_of_failure", "tr3"),
        ("damage_development", 1),
        ("damage_increment", "s"),
        ("z_position", "float"),
        ("outer_slope", [1.0, 3.5]),
        ("log_flexural_strength", "float"),
        ("stiffness_relation", "float"),
        ("computational_thickness", "float"),
        ("equivalent_elastic_modulus", "float"),
        ("maximum_peak_stress", ["a", 2.0]),
        ("average_number_of_waves", False),
    ],
)
def test_asphaltoutputlocationthrowsonwronginput(field_name, value):
    input = {
        "x_position": 1.23,
        "time_of_failure": None,
        "damage_development": [1.0],
        "damage_increment": [1.0],
        "z_position": 3.0,
        "outer_slope": 3.0,
        "log_flexural_strength": 3.0,
        "stiffness_relation": 3.0,
        "computational_thickness": 3.0,
        "equivalent_elastic_modulus": 3.0,
        "maximum_peak_stress": [3.0, 3.0],
        "average_number_of_waves": [3.0, 3.0],
    }

    input[field_name] = value
    with pytest.raises(ValidationError) as v_error:
        o = AsphaltWaveImpactOutputLocation(**input)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == field_name


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("x_position", "a3.r2"),
        ("time_of_failure", "tr3"),
        ("damage_development", 1),
        ("damage_increment", "s"),
        ("z_position", "float"),
        ("minimum_wave_height", "not"),
        ("maximum_wave_height", "not"),
        ("loading_revetment", [1.0, None]),
        ("upper_limit_loading", [1.0, 2.0, "a"]),
        ("lower_limit_loading", [1.0, 2.0, "b"]),
        ("wave_angle", [1.0, None, "c"]),
        ("wave_angle_impact", [1.0, "d", None]),
        ("wave_height_impact", [1.0, "e", None]),
    ],
)
def test_grasswaveimpactoutputlocationthrowsonwronginput(field_name, value):
    input = {
        "x_position": 1.23,
        "time_of_failure": None,
        "damage_development": [1.0],
        "damage_increment": [1.0],
        "z_position": 2.132,
        "minimum_wave_height": 12.540,
        "maximum_wave_height": 4.02,
        "loading_revetment": [1.0, 2.0],
        "upper_limit_loading": [1.0, 2.0],
        "lower_limit_loading": [1.0, 2.0],
        "wave_angle": [1.0, 2.0, None],
        "wave_angle_impact": [1.0, 2.0, None],
        "wave_height_impact": [1.0, 2.0, None],
    }

    input[field_name] = value
    with pytest.raises(ValidationError) as v_error:
        o = GrassWaveImpactOutputLocation(**input)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == field_name


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("x_position", "a3.r2"),
        ("time_of_failure", "tr3"),
        ("damage_development", 1),
        ("damage_increment", "s"),
        ("z_position", "float"),
        ("vertical_distance_water_level_elevation", "s"),
        ("representative_wave_runup_2p", ["s"]),
        ("wave_angle", [1.0, "None"]),
        ("wave_angle_impact", False),
        ("cumulative_overload", None),
        ("average_number_of_waves", [1.0, "frnbeu"]),
    ],
)
def test_grasswaverunupoutputlocationthrowsonwronginput(field_name, value):
    input = {
        "x_position": 1.23,
        "time_of_failure": None,
        "damage_development": [1.0],
        "damage_increment": [1.0],
        "z_position": 2.132,
        "vertical_distance_water_level_elevation": [1.0],
        "representative_wave_runup_2p": [1.0],
        "wave_angle": [1.0, None],
        "wave_angle_impact": [1.0, None],
        "cumulative_overload": [1.0],
        "average_number_of_waves": [1.0],
    }

    input[field_name] = value
    with pytest.raises(ValidationError) as v_error:
        o = GrassWaveRunupOutputLocation(**input)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == field_name


@pytest.mark.parametrize(
    "field_name,value",
    [
        ("x_position", "a3.r2"),
        ("time_of_failure", "tr3"),
        ("damage_development", 1),
        ("damage_increment", "s"),
        ("representative_wave_runup_2p", None),
        ("cumulative_overload", 4),
        ("average_number_of_waves", ["test"]),
        ("vertical_distance_water_level_elevation", [None]),
    ],
)
def test_grassovertoppingoutputlocationthrowsonwronginput(field_name, value):
    input = {
        "x_position": 1.23,
        "time_of_failure": None,
        "damage_development": [1.0],
        "damage_increment": [1.0],
        "representative_wave_runup_2p": [2.0],
        "cumulative_overload": [2.0],
        "average_number_of_waves": [2.0],
        "vertical_distance_water_level_elevation": [2.0],
    }

    input[field_name] = value
    with pytest.raises(ValidationError) as v_error:
        o = GrassOvertoppingOutputLocation(**input)

    errors = v_error.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == field_name
