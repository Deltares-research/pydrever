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
import numpy as numpy
from dikerosion.data.dikerneloutputspecification import OutputLocationSpecification
from dikerosion.data.dikernelcalculationsettings import CalculationSettings


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


class HydrodynamicConditions:
    def __init__(
        self,
        time_steps: list[float],
        water_levels: list[float],
        wave_heights: list[float],
        wave_periods: list[float],
        wave_directions: list[float],
    ):
        """
        Constructor for the hydrodynamic input.

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
                "Length of the specified series for waterlevels, wave heights, wave periods and wave angles needs to be exactly 1 less than the length of the specified time steps."
            )

        self.time_steps = time_steps
        self.water_levels = water_levels
        self.wave_heights = wave_heights
        self.wave_periods = wave_periods
        self.wave_directions = wave_directions
        # TODO: Maybe automatically correct the wave directions?


class DikernelInput:
    def __init__(
        self,
        hydrodynamic_input: HydrodynamicConditions,
        dike_schematization: DikeSchematization,
    ):
        """
        Constructor for the DikernelInput class.

        Args:
            hydrodynamicInput (HydrodynamicInput): object containing the hydrodynamic input
            dikeSchematization (DikeSchematization): object containing the dike schematization
        """
        self.hydrodynamic_input: HydrodynamicConditions = hydrodynamic_input
        """Hydrodynamic input specification - instance variable."""
        self.dike_schematization: DikeSchematization = dike_schematization
        """Schematization of the dike cross-shore profile and characteristic points - instance variable."""
        self.output_locations: list[OutputLocationSpecification] = None
        """Specification of the desired calculation and output locations - instance variable."""
        self.settings: list[CalculationSettings] = None
        """List of calculation settings that are used for the various types of revetments - instance variable."""
        self.start_time: float = None
        """Optional start time of the calculation - instance variable."""
        self.stop_time: float = None
        """Optional stop time of the calculation - instance variable."""
        self.output_time_steps: list[float] = None
        """Optional list of desired output time steps. This will add output times to the calculation - instance variable."""
        # Results are not filtered based on this list (cumulative values such as the damage increment in the results would not make sense anymore).

    def get_run_time_steps(self) -> list[float]:
        """
        This method combines all time steps and required output time steps to for
        a list of time steps that needs to be used during calculation.

        It combines the specified time steps for hydrodynamic conditions and the
        specified output time steps and then takes all time steps between the
        optional start and stop times (including the start and stop times).
        """
        run_time_steps = self.hydrodynamic_input.time_steps
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

        if self.stop_time is not None:
            run_time_steps = list(
                time_step
                for time_step in numpy.union1d(run_time_steps, [self.stop_time])
                if time_step <= self.start_time
            )
        return run_time_steps

    def get_run_input(self) -> DikernelInput:
        """
        Returns manipulated input that incorporates the desired output time steps and start time of the calculation in the hydrodynamic input.

        Returns:
            DikernelInput: A manipulated input object that can be used to calculate.
        """
        time_steps = self.hydrodynamic_input.time_steps
        run_time_steps = self.get_run_time_steps()
        run_hydrodynamics = HydrodynamicConditions(
            run_time_steps,
            self.__interpolate_time_series(
                time_steps, self.hydrodynamic_input.water_levels, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydrodynamic_input.wave_heights, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydrodynamic_input.wave_periods, run_time_steps
            ),
            self.__interpolate_time_series(
                time_steps, self.hydrodynamic_input.wave_directions, run_time_steps
            ),
        )
        run_input = DikernelInput(run_hydrodynamics, self.dike_schematization)
        run_input.output_locations = self.output_locations
        run_input.settings = self.settings
        return run_input

    @staticmethod
    def __interpolate_time_series(
        time_steps: list[float], values: list[float], target_time_steps: list[float]
    ) -> list[float]:
        """
        Private method to interpolate time series and add the target_time_steps to the list.

        Args:
            time_steps (list[float]): Original specification of the time steps of the hydrodynamic forcing.
            values (list[float]): Values for each time step in the original time series.
            target_time_steps (list[float]): Desired output time steps that needs to be added to the time series.

        Returns:
            list[float]: A list of values for the combined list of time steps and target_time_steps.
        """
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
