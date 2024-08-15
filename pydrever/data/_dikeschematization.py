"""
 Copyright (C) Stichting Deltares 2023-2024. All rights reserved.
 
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

from pydantic import BaseModel, ConfigDict


class DikeSchematization(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    dike_orientation: float
    """Orientation of the dike normal relative to North - instance variable."""
    x_positions: list[float]
    """list of cross-shore positions"""
    z_positions: list[float]
    """list of dike heights in meter correspoinding to the cross-shore positions. zPositions needs to be of the samen length as xPositions"""
    roughnesses: list[float]
    """a list of roughness coefficients per dike segment. By definition the length of this list is equal to the length of xPositions - 1"""
    x_outer_toe: float
    """The cross-shore location of the toe of the dike at the outer slope"""
    x_outer_crest: float
    """The cross-shore location of the (outer) crest of the dike"""
    x_crest_outer_berm: float | None = None
    """The cross-shore location of the notch of the outer berm"""
    x_notch_outer_berm: float | None = None
    """The cross-shore location of the inner crest of the dike"""
    x_inner_crest: float | None = None
    """The cross-shore location of the inner toe of the dike"""
    x_inner_toe: float | None = None
