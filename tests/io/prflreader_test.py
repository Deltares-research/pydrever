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

import os
from pydrever.io import prflreader
import pytest


@pytest.mark.parametrize(
    "file_name",
    (
        "profiel001.prfl",
        "profiel002.prfl",
        "profiel003.prfl",
        "profiel004.prfl",
        "profiel005.prfl",
    ),
)
def test_read_correct_file(test_data_dir, file_name):
    filename = os.path.join(test_data_dir, file_name)
    schematization = prflreader.read(filename)
    assert schematization is not None
    if file_name == "profiel001.prfl":
        assert len(schematization.x_positions) == 2
        assert schematization.x_positions[0] == 0.0
        assert schematization.x_positions[1] == 18.0
        assert len(schematization.z_positions) == 2
        assert schematization.z_positions[0] == 0.0
        assert schematization.z_positions[1] == 6.0
        assert len(schematization.roughnesses) == 1
        assert schematization.roughnesses[0] == 1.0
    else:
        assert len(schematization.x_positions) == 4
        assert schematization.x_positions[0] == -18.0
        assert schematization.x_positions[1] == -2.0
        assert schematization.x_positions[2] == 2.0
        assert schematization.x_positions[3] == 18.0
        assert len(schematization.z_positions) == 4
        assert schematization.z_positions[0] == -6.0
        assert schematization.z_positions[1] == -0.1
        assert schematization.z_positions[2] == 0.1
        assert schematization.z_positions[3] == 6.0
        assert len(schematization.roughnesses) == 3
        assert schematization.roughnesses[1] == 0.5
