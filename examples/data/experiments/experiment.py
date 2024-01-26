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

from __future__ import annotations
from dikerosion.data import (
    DikernelInput,
    DikeSchematization,
    HydrodynamicConditions,
    CalculationSettings,
)
from abc import ABC, abstractstaticmethod


class Experiment(ABC):
    @abstractstaticmethod
    def get_calculation_input() -> DikernelInput:
        """
        This method returns calculation input for the specific experiment.

        Returns:
            DikernelInput: The input of the specific experiment.
        """
        pass

    @abstractstaticmethod
    def generate_dike_schematization() -> DikeSchematization:
        pass

    @abstractstaticmethod
    def generate_hydrodynamics() -> HydrodynamicConditions:
        pass

    @abstractstaticmethod
    def generate_settings() -> list[CalculationSettings]:
        pass
