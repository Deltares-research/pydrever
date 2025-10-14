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
    return settings


@pytest.fixture
def natural_stone_settings() -> NaturalStoneCalculationSettings:
    settings = NaturalStoneCalculationSettings(
        top_layers_settings=[NaturalStoneTopLayerSettings(top_layer_type=TopLayerType.NordicStone)],
    )
    return settings


@pytest.fixture
def grass_wave_impact_settings() -> GrassWaveImpactCalculationSettings:
    settings = GrassWaveImpactCalculationSettings(
        top_layers_settings=[GrassWaveImpactTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return settings


@pytest.fixture
def grass_wave_overtopping_settings() -> GrassWaveOvertoppingCalculationSettings:
    settings = GrassWaveOvertoppingCalculationSettings(
        top_layers_settings=[GrassCumulativeOverloadTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return settings


@pytest.fixture
def grass_wave_runup_settings() -> GrassWaveRunupCalculationSettings:
    settings = GrassWaveRunupCalculationSettings(
        top_layers_settings=[GrassCumulativeOverloadTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return settings


@pytest.fixture
def natural_stone_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=NordicStoneLayerSpecification(top_layer_thickness=1.0, relative_density=1.0),
    )


@pytest.fixture
def natural_stone_location_with_settings() -> OutputLocationSpecification:
    settings = NaturalStoneCalculationSettings(top_layers_settings=[NaturalStoneTopLayerSettings(top_layer_type=TopLayerType.NordicStone)])
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=NordicStoneLayerSpecification(top_layer_thickness=1.0, relative_density=1.0),
        calculation_settings=settings,
    )


@pytest.fixture
def asphalt_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=AsphaltLayerSpecification(
            top_layer_type=TopLayerType.Asphalt,
            flexural_strength=1.0,
            soil_elasticity=1.0,
            upper_layer_thickness=1.0,
            upper_layer_elasticity_modulus=1.0,
        ),
    )


@pytest.fixture
def asphalt_location_with_settings() -> OutputLocationSpecification:
    settings = AsphaltCalculationSettings()
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=AsphaltLayerSpecification(
            top_layer_type=TopLayerType.Asphalt,
            flexural_strength=1.0,
            soil_elasticity=1.0,
            upper_layer_thickness=1.0,
            upper_layer_elasticity_modulus=1.0,
        ),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_impact_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveImpactLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod),
    )


@pytest.fixture
def grass_wave_impact_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveImpactCalculationSettings(
        top_layers_settings=[GrassWaveImpactTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveImpactLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_overtopping_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassOvertoppingLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod),
    )


@pytest.fixture
def grass_wave_overtopping_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveOvertoppingCalculationSettings(
        top_layers_settings=[GrassCumulativeOverloadTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassOvertoppingLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod),
        calculation_settings=settings,
    )


@pytest.fixture
def grass_wave_runup_location_without_settings() -> OutputLocationSpecification:
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassOvertoppingLayerSpecification(top_layer_type=TopLayerType.GrassClosedSod),
    )


@pytest.fixture
def grass_wave_runup_location_with_settings() -> OutputLocationSpecification:
    settings = GrassWaveRunupCalculationSettings(
        top_layers_settings=[GrassCumulativeOverloadTopLayerSettings(top_layer_type=TopLayerType.GrassClosedSod)]
    )
    return OutputLocationSpecification(
        x_position=0.0,
        top_layer_specification=GrassWaveRunupLayerSpecification(outer_slope=0.3, top_layer_type=TopLayerType.GrassClosedSod),
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
    assert return_settings is not None
    assert natural_stone_location_with_settings.calculation_settings is not None
    assert return_settings.top_layers_settings == natural_stone_location_with_settings.calculation_settings.top_layers_settings


def test_get_natural_stone_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(
        natural_stone_location_without_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert return_settings is not None
    assert return_settings.top_layers_settings == natural_stone_settings.top_layers_settings


def test_get_natural_stone_calculation_settings_no_settings_in_general_list(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(natural_stone_location_without_settings, [asphalt_settings])
    assert return_settings is None


def test_get_natural_stone_calculation_settings_nop_general_settings(
    natural_stone_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_natural_stone_calculation_settings(natural_stone_location_without_settings, None)
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
    assert return_settings is not None
    assert asphalt_location_with_settings.calculation_settings is not None
    assert return_settings.top_layers_settings == asphalt_location_with_settings.calculation_settings.top_layers_settings


def test_get_asphalt_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    natural_stone_settings: NaturalStoneCalculationSettings,
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(
        asphalt_location_without_settings,
        [asphalt_settings, natural_stone_settings],
    )
    assert return_settings is not None
    assert return_settings.top_layers_settings == asphalt_settings.top_layers_settings


def test_get_asphalt_calculation_settings_no_settings_in_general_list(
    natural_stone_settings: NaturalStoneCalculationSettings,
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(asphalt_location_without_settings, [natural_stone_settings])
    assert return_settings is None


def test_get_asphalt_calculation_settings_no_general_settings(
    asphalt_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_asphalt_calculation_settings(asphalt_location_without_settings, None)
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
    assert return_settings is not None
    assert grass_wave_impact_location_with_settings.calculation_settings is not None
    assert return_settings.top_layers_settings == grass_wave_impact_location_with_settings.calculation_settings.top_layers_settings


def test_get_grass_wave_impact_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_impact_settings: GrassWaveImpactCalculationSettings,
    grass_wave_impact_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(
        grass_wave_impact_location_without_settings,
        [asphalt_settings, grass_wave_impact_settings],
    )
    assert return_settings is not None
    assert return_settings.top_layers_settings == grass_wave_impact_settings.top_layers_settings


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
    return_settings = _input_parser.__get_grass_wave_impact_calculation_settings(grass_wave_impact_location_without_settings, None)
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
    assert return_settings is not None
    assert grass_wave_overtopping_location_with_settings.calculation_settings is not None
    assert return_settings.top_layers_settings == grass_wave_overtopping_location_with_settings.calculation_settings.top_layers_settings


def test_get_grass_wave_overtopping_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_overtopping_settings: GrassWaveOvertoppingCalculationSettings,
    grass_wave_overtopping_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_overtopping_calculation_settings(
        grass_wave_overtopping_location_without_settings,
        [asphalt_settings, grass_wave_overtopping_settings],
    )
    assert return_settings is not None
    assert return_settings.top_layers_settings == grass_wave_overtopping_settings.top_layers_settings


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
    assert return_settings is not None
    assert grass_wave_runup_location_with_settings.calculation_settings is not None
    assert return_settings.top_layers_settings == grass_wave_runup_location_with_settings.calculation_settings.top_layers_settings


def test_get_grass_wave_runup_calculation_settings_from_general_settings(
    asphalt_settings: AsphaltCalculationSettings,
    grass_wave_runup_settings: GrassWaveOvertoppingCalculationSettings,
    grass_wave_runup_location_without_settings: OutputLocationSpecification,
):
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(
        grass_wave_runup_location_without_settings,
        [asphalt_settings, grass_wave_runup_settings],
    )
    assert return_settings is not None
    assert return_settings.top_layers_settings == grass_wave_runup_settings.top_layers_settings


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
    return_settings = _input_parser.__get_grass_wave_runup_calculation_settings(grass_wave_runup_location_without_settings, None)
    assert return_settings is None


# endregion
