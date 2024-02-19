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

from dikerosion.data import DikeSchematization
import os.path
from enum import Enum


class PrflReaderExceptionType(Enum):
    """
    This enum provides the type of error raised by the prflreader in case a file could not be read.
    """

    FileNotFound = "File could not be found."
    FileShouldNotBeEmpty = "The file should not be empty."
    WrongVersion = "The version should be 4.0."
    NoDikeProfile = "No dike profile was found."
    NoValidVersion = "No valid version was found."
    NoValidOrientation = "No valid orientation was found."
    IncorrectCoordinates = "Something went wrong reading coordinates or roughnesses."


class PrflFileReaderException(Exception):
    """
    Custom exception used by the prfl reader in case a file could not be read. The PrflExceptionType (type)
    provides information on what went wrong.

    Args:
        type (PrflReaderExceptiuonType): The type of exception that occurred.
    """

    def __init__(self, type: PrflReaderExceptionType):
        self.type = type
        super().__init__(str(self.type.value))


def read(file_name: str) -> DikeSchematization:
    """
    This method reads the content of a *.prfl file into a dike schematization object.

    Args:
        file_name (str): The full path to the prfl file.

    Raises:
        PrflFileReaderException: Raised case the file could not be read.

    Returns:
        DikeSchematization: The dike schematization contained by the prfl file.
    """
    if not os.path.isfile(file_name):
        raise PrflFileReaderException(PrflReaderExceptionType.FileNotFound)

    lines = None
    with open(file_name) as file:
        lines = [line.rstrip().split() for line in file]

    if lines is None or len(lines) < 1:
        raise PrflReaderExceptionType(PrflReaderExceptionType.FileShouldNotBeEmpty)

    version = __read_version(lines)
    if version != 4.0:
        raise PrflFileReaderException(PrflReaderExceptionType.WrongVersion)

    orientation = __read_orientation(lines)
    x_coordinates, z_coordinates, roughness = __read_coordinates(lines)
    x_outer_crest = __find_outer_crest(x_coordinates, z_coordinates)
    return DikeSchematization(
        orientation,
        x_coordinates,
        z_coordinates,
        roughness,
        min(x_coordinates),
        x_outer_crest,
    )


def __read_version(lines: list[list[str]]) -> float:
    version_line = __find_line_by_keyword(lines, "VERSIE")
    try:
        return float(version_line[1])
    except:
        raise PrflFileReaderException(PrflReaderExceptionType.NoValidVersion)


def __read_orientation(lines: list[str]):
    orientation_line = __find_line_by_keyword(lines, "RICHTING")
    try:
        return float(orientation_line[1])
    except:
        raise PrflFileReaderException(PrflReaderExceptionType.NoValidOrientation)


def __read_coordinates(lines: list[str]):
    coordinates_line = __find_line_by_keyword(lines, "DIJK")
    n_coordinates = int(coordinates_line[1]) if coordinates_line is not None else None
    if n_coordinates is None:
        raise PrflFileReaderException(PrflReaderExceptionType.NoDikeProfile)

    try:
        i_start = lines.index(coordinates_line) + 1
        x_cooordaintes = []
        z_cooordaintes = []
        roughnesses = []
        for i in range(i_start, i_start + n_coordinates, 1):
            x_cooordaintes.append(float(lines[i][0]))
            z_cooordaintes.append(float(lines[i][1]))
            if i < i_start + n_coordinates - 1:
                roughnesses.append(float(lines[i][2]))

        return x_cooordaintes, z_cooordaintes, roughnesses
    except:
        raise PrflFileReaderException(PrflReaderExceptionType.IncorrectCoordinates)


def __find_outer_crest(x_coordinates: list[float], z_coordinates: list[float]):
    previous_z = z_coordinates[0]
    i_max = 0
    for i, z in enumerate(z_coordinates):
        if z < previous_z:
            break
        previous_z = z
        i_max = i

    return x_coordinates[i_max]


def __find_line_by_keyword(lines: list[str], keyword: str):
    return next((line for line in lines if len(line) > 1 and line[0] == keyword), None)
