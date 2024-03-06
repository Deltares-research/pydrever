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


class DikeSchematization:
    def __init__(
        self,
        dike_orientation: float,
        x_positions: list[float],
        z_positions: list[float],
        roughnesses: list[float],
        x_outer_toe: float,
        x_outer_crest: float,
    ):
        """
        Contructor for a schematization of a dike profile.

        Args:
            dikeOrientation (float): orientation of the dike normal
            x_positions (list[float]): list of cross-shore positions
            z_positions (list[float]): list of dike heights in meter correspoinding to the cross-shore positions. zPositions needs to be of the samen length as xPositions
            roughnesses (list[float]): a list of roughness coefficients per dike segment. By definition the length of this list is equal to the length of xPositions - 1
            x_outer_toe (float): The cross-shore location of the toe of the dike at the outer slope
            x_outer_crest (float): The cross-shore location of the (outer) crest of the dike
        """
        self.dike_orientation: float = dike_orientation
        """Orientation of the dike normal relative to North - instance variable."""
        self.x_positions: list[float] = x_positions
        self.z_positions: list[float] = z_positions
        self.roughnesses: list[float] = roughnesses
        self.outer_toe: float = x_outer_toe
        self.outer_crest: float = x_outer_crest
        self.crest_outer_berm: float = None
        self.notch_outer_berm: float = None
        self.inner_crest: float = None
        self.inner_toe: float = None
