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


def is_continuously_increasing(lst: list[float]) -> bool:
    """
    Function to check whether a list has continuously increasing numbers.

    Args:
        lst (list[float]): The list that needs to increase continuously

    Returns:
        bool: False of one or more of the numbers is decreasing
    """
    return all(i < j for i, j in zip(lst, lst[1:]))


def is_valid_orientation(orientation: float) -> bool:
    """
    Function to check whether the provided number is a valid orientation (wind direction within the range [0, 360] degrees).

    Args:
        orientation (float): The orientation (in degrees)

    Returns:
        bool: False in case the orientation is empty (None), less than 0 degrees or greater than 360 degrees.
    """
    return orientation is not None and orientation >= 0 and orientation <= 360
