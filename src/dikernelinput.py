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
from dikerneloutputlocations import OutputLocationSpecification
from dikernelcalculationsettings import CalculationSettings
import numpy as numpy


class DikeSchematization:
    def __init__(
        self,
        x_positions: list[float],
        z_positions: list[float],
        roughnesses: list[float],
        x_outer_toe: float,
        x_outer_crest: float,
    ):
        """Contructor for a schematization of a dike profile.

        Args:
            x_positions (list[float]): list of cross-shore positions
            z_positions (list[float]): list of dike heights in meter correspoinding to the cross-shore positions. zPositions needs to be of the samen length as xPositions
            roughnesses (list[float]): a list of roughness coefficients per dike segment. By definition the length of this list is equal to the length of xPositions - 1
            x_outer_toe (float): The cross-shore location of the toe of the dike at the outer slope
            x_outer_crest (float): The cross-shore location of the (outer) crest of the dike
        """
        self.x_positions: list[float] = x_positions
        self.z_positions: list[float] = z_positions
        self.roughnesses: list[float] = roughnesses
        self.outer_toe: float = x_outer_toe
        self.outer_crest: float = x_outer_crest
        self.crest_outer_berm: float = None
        self.notch_outer_berm: float = None
        self.inner_crest: float = None
        self.inner_toe: float = None


class HydraulicConditions:
    def __init__(
        self,
        time_steps: list[float],
        water_levels: list[float],
        wave_heights: list[float],
        wave_periods: list[float],
        wave_directions: list[float],
    ):
        """Constructor for the hydraulic input.

        Args:
            time_steps (list[float]): list of timesteps.
            water_levels (list[float]): list of waterlevels
            wave_heights (list[float]): list of significant wave heights (Hs)
            wave_periods (list[float]): list of wave periods
            wave_directions (list[float]): list of wave directions
        Raises:
            Exception: In case the length of either the specified water level series, the wave heights, wave periods or wave angles is not exactly 1 less than the length of the specified time steps.
        """
        nr_time_steps = len(time_steps)
        if (
            nr_time_steps - 1 != len(water_levels)
            or nr_time_steps - 1 != len(wave_heights)
            or nr_time_steps - 1 != len(wave_periods)
            or nr_time_steps - 1 != len(wave_directions)
        ):
            raise Exception(
                "length of the specified series for waterlevels, wave heights, wave periods and wave angles needs to be exactly 1 less than the length of the specified time steps."
            )

        self.time_steps = time_steps
        self.water_levels = water_levels
        self.wave_heights = wave_heights
        self.wave_periods = wave_periods
        self.wave_directions = wave_directions


class DikernelInput:
    def __init__(
        self,
        dike_orientation: float,
        hydraulic_input: HydraulicConditions,
        dike_schematization: DikeSchematization,
    ):
        """Constructor for the DikernelInput class.

        Args:
            dikeOrientation (float): orientation of the dike normal
            hydraulicInput (HydraulicInput): object containing the hydraulics input
            dikeSchematization (DikeSchematization): object containing the dike schematization
        """
        self.dike_orientation: float = dike_orientation
        self.hydraulic_input: HydraulicConditions = hydraulic_input
        self.dike_schematization: DikeSchematization = dike_schematization
        self.output_locations: list[OutputLocationSpecification] = None
        self.settings: list[CalculationSettings] = None
        self.start_time: float = None
        self.output_time_steps: list[float] = None

    def getruntimesteps(self) -> list[float]:
        run_time_steps = self.hydraulic_input.time_steps
        if self.output_time_steps is not None:
            run_time_steps = numpy.union1d(
                run_time_steps, self.output_time_steps
            ).tolist()

        if self.start_time is not None:
            run_time_steps = list(
                time_step
                for time_step in numpy.union1d(run_time_steps, [self.start_time])
                if time_step >= self.start_time
            )
        return run_time_steps

    def get_run_input(self) -> DikernelInput:
        time_steps = self.hydraulic_input.time_steps
        run_time_steps = self.getruntimesteps()
        run_hydraulics = HydraulicConditions(
            run_time_steps,
            self.__interpolate_time_series(
                time_steps, self.hydraulic_input.water_levels, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydraulic_input.wave_heights, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydraulic_input.wave_periods, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydraulic_input.wave_directions, run_time_steps
            ),
        )
        run_input = DikernelInput(
            self.dike_orientation, run_hydraulics, self.dike_schematization
        )
        run_input.output_locations = self.output_locations
        run_input.settings = self.settings
        return run_input

    @staticmethod
    def __interpolate_time_series(
        time_steps: list[float], values: list[float], target_time_steps: list[float]
    ) -> list[float]:
        iargs = 1
        itarget = 1
        target_values = list[float]()
        while itarget < len(target_time_steps):
            if (
                target_time_steps[itarget] > time_steps[iargs]
                and iargs < len(time_steps) - 1
            ):
                iargs = iargs + 1
                continue
            target_values.append(values[iargs - 1])
            itarget = itarget + 1

        return target_values
