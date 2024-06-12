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
    NaturalStoneCalculationSettings,
    NordicStoneLayerSpecification,
    OutputLocationSpecification,
    NaturalStoneTopLayerSettings,
    AsphaltCalculationSettings,
    AsphaltLayerSpecification,
    GrassWaveImpactCalculationSettings,
    GrassWaveImpactLayerSpecification,
    GrassWaveImpactTopLayerSettings,
    TopLayerType,
    GrassOvertoppingLayerSpecification,
    GrassCumulativeOverloadTopLayerSettings,
    GrassWaveOvertoppingCalculationSettings,
    GrassWaveRunupCalculationSettings,
    GrassWaveRunupLayerSpecification,
)

import pydrever.calculation._dikernel._dikernelinputparser as _input_parser

import pytest


@pytest.fixture
def asphalt_settings() -> AsphaltCalculationSettings:
    settings = AsphaltCalculationSettings()
    settings.calculation_method = "asphalt_settings"
    # TODO: Move to initializaTion after using pydantic
    return settings


@pytest.fixture
def natural_stone_settings() -> NaturalStoneCalculationSettings:
    settings = NaturalStoneCalculationSettings(
        topLayers=[
            NaturalStoneTopLayerSettings(top_layer_type=TopLayerType.NordicStone)
        ],
    )
    settings.calculation_method = "natural_stone_settings"
    # TODO: Move to initializaTion after using pydantic
    return settings


@pytest.fixture
def grass_wave_impact_settings() -> GrassWaveImpactCalculationSettings:
    settings = GrassWaveImpactCalculationSettings(
        [GrassWaveImpactLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    settings.calculation_method = "grass_wave_impact_settings"
    # TODO: Move to initializaTion after using pydantic
    return settings


@pytest.fixture
def grass_wave_overtopping_settings() -> GrassWaveOvertoppingCalculationSettings:
    settings = GrassWaveOvertoppingCalculationSettings(
        [
            GrassCumulativeOverloadTopLayerSettings(
                top_layer_type=TopLayerType.GrassClosedSod
            )
        ]
    )
    settings.calculation_method = "grass_wave_overtopping_settings"
    # TODO: Move to initializaTion after using pydantic
    return settings


@pytest.fixture
def grass_wave_runup_settings() -> GrassWaveOvertoppingCalculationSettings:
    settings = GrassWaveRunupCalculationSettings(
        topLayers=[
            GrassCumulativeOverloadTopLayerSettings(
                top_layer_type=TopLayerType.GrassClosedSod
            )
        ]
    )
    settings.calculation_method = "grass_wave_runup_settings"
    return settings


@pytest.fixture
def natural_stone_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=NordicStoneLayerSpecification(
            top_layer_thickness=1.0, relative_density=1.0
        ),
    )


@pytest.fixture
def natural_stone_location_with_settings() -> OutputLocationSpecification:
    settings = NaturalStoneCalculationSettings(
        [NaturalStoneTopLayerSettings(top_layer_type=TopLayerType.NordicStone)]
    )
    settings.calculation_method = "location_specific_settings"
    return OutputLocationSpecification(
        0.0,
        NordicStoneLayerSpecification(top_layer_thickness=1.0, relative_density=1.0),
        settings,
    )


@pytest.fixture
def asphalt_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=AsphaltLayerSpecification(
            flexural_strength=1.0,
            soil_elasticity=1.0,
            upper_layer_thickness=1.0,
            upper_layer_stiffness_modulus=1.0,
        ),
    )


@pytest.fixture
def asphalt_location_with_settings() -> OutputLocationSpecification:
    settings = AsphaltCalculationSettings()
    settings.calculation_method = "location_specific_settings"
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=AsphaltLayerSpecification(
            flexural_strength=1.0,
            soil_elasticity=1.0,
            upper_layer_thickness=1.0,
            upper_layer_stiffness_modulus=1.0,
        ),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_impact_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveImpactLayerSpecification(
            top_layer_type=TopLayerType.GrassClosedSod
        ),
    )


@pytest.fixture
def grass_wave_impact_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveImpactCalculationSettings(
        topLayers=[
            GrassWaveImpactTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)
        ]
    )
    settings.calculation_method = "location_specific_settings"
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveImpactLayerSpecification(
            top_layer_type=TopLayerType.GrassClosedSod
        ),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_overtopping_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassOvertoppingLayerSpecification(
            top_layer_type=TopLayerType.GrassClosedSod
        ),
    )


@pytest.fixture
def grass_wave_overtopping_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveOvertoppingCalculationSettings(
        topLayers=[
            GrassCumulativeOverloadTopLayerSettings(
                top_layer_type=TopLayerType.GrassClosedSod
            )
        ]
    )
    settings.calculation_method = "location_specific_settings"
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassOvertoppingLayerSpecification(
            top_layer_type=TopLayerType.GrassClosedSod
        ),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_runup_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassCumulativeOverloadTopLayerSettings(
            top_layer_type=TopLayerType.GrassClosedSod
        ),
    )


@pytest.fixture
def grass_wave_runup_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveRunupCalculationSettings(
        topLayers=[
            GrassCumulativeOverloadTopLayerSettings(
                top_layer_type=TopLayerType.GrassClosedSod
            )
        ]
    )
    settings.calculation_method = "location_specific_settings"
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveRunupLayerSpecification(
            outer_slope=0.3, top_layer_type=TopLayerType.GrassClosedSod
        ),
        calculation_settings=settings,
    )


# region test get_natural_stone_calculation_settings
def test_get_natural_stone_calculation_settings_from_location(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    natural_stone_location_with_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(
        natural_stone_location_with_settings, [asphalt_settings, natural_stone_settings]
    )
    assert (
        return_settings.calculation_method
        == natural_stone_location_with_settings.calculation_settings.calculation_method
    )


def test_get_natural_stone_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(
        natural_stone_location_without_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert (
        return_settings.calculation_method == natural_stone_settings.calculation_method
    )


def test_get_natural_stone_calculation_settings_no_settings_in_general_list(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(
        natural_stone_location_without_settings, [asphalt_settings]
    )
    assert return_settings is None


def test_get_natural_stone_calculation_settings_nop_general_settings(
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(
        natural_stone_location_without_settings, None
    )
    assert return_settings is None


# endregion


# region test get_asphalt_calculation_settings
def test_get_asphalt_calculation_settings_from_location(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    asphalt_location_with_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(
        asphalt_location_with_settings, [asphalt_settings, natural_stone_settings]
    )
    assert (
        return_settings.calculation_method
        == asphalt_location_with_settings.calculation_settings.calculation_method
    )


def test_get_asphalt_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(
        asphalt_location_without_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert return_settings.calculation_method == asphalt_settings.calculation_method


def test_get_asphalt_calculation_settings_no_settings_in_general_list(
    natural_stone_settings: NaturalStoneCalculationSettings,
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(
        asphalt_location_without_settings, [natural_stone_settings]
    )
    assert return_settings is None


def test_get_asphalt_calculation_settings_no_general_settings(
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(
        asphalt_location_without_settings, None
    )
    assert return_settings is None


# endregion


# region test get_grass_wave_impact_calculation_settings
def test_get_grass_wave_impact_calculation_settings_from_location(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_impact_location_with_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(
        grass_wave_impact_location_with_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_impact_location_with_settings.calculation_settings.calculation_method
    )


def test_get_grass_wave_impact_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_impact_settings: GrassWaveImpactCalculationSettings,
    grass_wave_impact_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(
        grass_wave_impact_location_without_settings,
        [asphalt_settings, grass_wave_impact_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_impact_settings.calculation_method
    )


def test_get_grass_wave_impact_calculation_settings_no_settings_in_general_list(
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_impact_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(
        grass_wave_impact_location_without_settings, [natural_stone_settings]
    )
    assert return_settings is None


def test_get_grass_wave_impact_calculation_settings_no_general_settings(
    grass_wave_impact_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(
        grass_wave_impact_location_without_settings, None
    )
    assert return_settings is None


# endregion


# region test get_grass_wave_overtopping_calculation_settings
def test_get_grass_wave_overtopping_calculation_settings_from_location(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_overtopping_location_with_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_overtopping_calculation_settings(
        grass_wave_overtopping_location_with_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_overtopping_location_with_settings.calculation_settings.calculation_method
    )


def test_get_grass_wave_overtopping_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_overtopping_settings: GrassWaveOvertoppingCalculationSettings,
    grass_wave_overtopping_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_overtopping_calculation_settings(
        grass_wave_overtopping_location_without_settings,
        [asphalt_settings, grass_wave_overtopping_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_overtopping_settings.calculation_method
    )


def test_get_grass_wave_overtopping_calculation_settings_no_settings_in_general_list(
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_overtopping_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_overtopping_calculation_settings(
        grass_wave_overtopping_location_without_settings, [natural_stone_settings]
    )
    assert return_settings is None


def test_get_grass_wave_overtopping_calculation_settings_no_general_settings(
    grass_wave_overtopping_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_overtopping_calculation_settings(
        grass_wave_overtopping_location_without_settings, None
    )
    assert return_settings is None


# endregion


# region test get_grass_wave_runup_calculation_settings
def test_get_grass_wave_runup_calculation_settings_from_location(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_runup_location_with_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(
        grass_wave_runup_location_with_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_runup_location_with_settings.calculation_settings.calculation_method
    )


def test_get_grass_wave_runup_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_runup_settings: GrassWaveOvertoppingCalculationSettings,
    grass_wave_runup_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(
        grass_wave_runup_location_without_settings,
        [asphalt_settings, grass_wave_runup_settings],
    )
    assert (
        return_settings.calculation_method
        == grass_wave_runup_settings.calculation_method
    )


def test_get_grass_wave_runup_calculation_settings_no_settings_in_general_list(
    natural_stone_settings: NaturalStoneCalculationSettings,
    grass_wave_runup_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(
        grass_wave_runup_location_without_settings, [natural_stone_settings]
    )
    assert return_settings is None


def test_get_grass_wave_runup_calculation_settings_no_general_settings(
    grass_wave_runup_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(
        grass_wave_runup_location_without_settings, None
    )
    assert return_settings is None


# endregion
