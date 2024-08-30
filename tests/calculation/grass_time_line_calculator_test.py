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

from pydrever.calculation import grassresistancetimescalculator
import matplotlib.pyplot as plt
import pytest


@pytest.mark.parametrize(("wave_height"), ((0, 4)))
def test_calculator_returns_none(wave_height):
    time = grassresistancetimescalculator.calculate_time_line([wave_height], 0, 0)
    assert len(time) == 1
    assert time[0] == None


def test_calculate_right_resistance_time():
    time = grassresistancetimescalculator.calculate_time_line([1], 0, 0)
    assert len(time) == 1
    assert time[0] == pytest.approx(8.22, 0.01)


def test_calculates_multiple_values():
    time = grassresistancetimescalculator.calculate_time_line([1, 1.1, 1.2, 1.3], 0, 0)
    assert len(time) == 4


def test_calculates_with_differend_zones():
    time_none = grassresistancetimescalculator.calculate_time_line(
        [1.2], 0, 0, te_min=3.6
    )
    assert len(time_none) == 1
    assert time_none[0] == None

    time_value = grassresistancetimescalculator.calculate_time_line(
        [1.2], 0, 0, te_min=0
    )
    assert len(time_value) == 1
    assert time_value[0] == pytest.approx(1.47, 0.01)


def test_change_sod_type():
    times = grassresistancetimescalculator.calculate_time_line([0.8], 0, 0, a=1)
    assert len(times) == 1
    assert times[0] == pytest.approx(17.1, 0.1)

    times = grassresistancetimescalculator.calculate_time_line([0.8], 0, 0, a=1.75)
    assert len(times) == 1
    assert times[0] == pytest.approx(33.1, 0.1)
