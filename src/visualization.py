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
 
 This is a license template.
"""

from dikernelinput import DikernelInput
import matplotlib.pyplot as plt


def plot_hydraulic_conditions(input: DikernelInput):
    run_input = input.get_run_input()
    time_steps = input.hydraulic_input.time_steps
    water_levels = input.hydraulic_input.water_levels
    wave_heights = input.hydraulic_input.wave_heights
    wave_periods = input.hydraulic_input.wave_periods
    wave_directions = input.hydraulic_input.wave_directions

    run_time_steps = run_input.hydraulic_input.time_steps
    run_water_levels = run_input.hydraulic_input.water_levels
    run_wave_heights = run_input.hydraulic_input.wave_heights
    run_wave_periods = run_input.hydraulic_input.wave_periods
    run_wave_directions = run_input.hydraulic_input.wave_directions

    fig, axs = plt.subplots(ncols=2, nrows=2)
    fig.suptitle("Hydraulic conditions", fontsize=16)
    axs[0, 0].plot(run_time_steps, [None] + run_water_levels, "gx", linestyle="dotted")
    axs[0, 0].plot(time_steps, [None] + water_levels, "bo")
    axs[0, 0].set(ylabel="Water level [m]")
    axs[0, 0].grid()
    axs[1, 0].plot(run_time_steps, [None] + run_wave_heights, "gx", linestyle="dotted")
    axs[1, 0].plot(time_steps, [None] + wave_heights, "bo")
    axs[1, 0].set(xlabel="Time step [s]", ylabel="Wave height [m]")
    axs[1, 0].grid()
    axs[0, 1].plot(run_time_steps, [None] + run_wave_periods, "gx", linestyle="dotted")
    axs[0, 1].plot(time_steps, [None] + wave_periods, "bo")
    axs[0, 1].set(ylabel="Wave periods [s]")
    axs[0, 1].grid()
    axs[1, 1].plot(
        run_time_steps, [None] + run_wave_directions, "gx", linestyle="dotted"
    )
    axs[1, 1].plot(time_steps, [None] + wave_directions, "bo")
    axs[1, 1].set(xlabel="Time step [s]", ylabel="Wave angles [degrees]")
    axs[1, 1].grid()
    fig.tight_layout()
