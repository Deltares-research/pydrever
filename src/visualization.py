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

from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutputLocation
import matplotlib.pyplot as plt
import numpy as numpy


def plot_hydraulic_conditions(input: DikernelInput):
    """
    This method produces a plot that shows the specified hydrodynamic boundary
    conditions as well as the schematized intervals to produce output steps.

    Args:
        input (DikernelInput): The dikernel input that needs to be visualized.

    Returns:
        figure handle: The handle of the produced figure
    """
    run_input = input.get_run_input()

    fig, axs = plt.subplots(ncols=2, nrows=2)
    fig.suptitle("Hydraulic conditions", fontsize=16)

    """
    Water levels
    """
    axs[0, 0].plot(
        run_input.hydraulic_input.time_steps,
        [None] + run_input.hydraulic_input.water_levels,
        "gx",
        linestyle="dotted",
    )
    axs[0, 0].plot(
        input.hydraulic_input.time_steps,
        [None] + input.hydraulic_input.water_levels,
        "bo",
    )
    axs[0, 0].set(ylabel="Water level [m]")
    axs[0, 0].grid()

    """
    Wave heights
    """
    axs[1, 0].plot(
        run_input.hydraulic_input.time_steps,
        [None] + run_input.hydraulic_input.wave_heights,
        "gx",
        linestyle="dotted",
    )
    axs[1, 0].plot(
        input.hydraulic_input.time_steps,
        [None] + input.hydraulic_input.wave_heights,
        "bo",
    )
    axs[1, 0].set(xlabel="Time step [s]", ylabel="Wave height [m]")
    axs[1, 0].grid()

    """
    Wave periods
    """
    axs[0, 1].plot(
        run_input.hydraulic_input.time_steps,
        [None] + run_input.hydraulic_input.wave_periods,
        "gx",
        linestyle="dotted",
    )
    axs[0, 1].plot(
        input.hydraulic_input.time_steps,
        [None] + input.hydraulic_input.wave_periods,
        "bo",
    )
    axs[0, 1].set(ylabel="Wave periods [s]")
    axs[0, 1].grid()

    """
    Wave directions
    """
    axs[1, 1].plot(
        run_input.hydraulic_input.time_steps,
        [None] + run_input.hydraulic_input.wave_directions,
        "gx",
        linestyle="dotted",
    )
    axs[1, 1].plot(
        input.hydraulic_input.time_steps,
        [None] + input.hydraulic_input.wave_directions,
        "bo",
    )
    axs[1, 1].set(xlabel="Time step [s]", ylabel="Wave angles [degrees]")
    axs[1, 1].grid()

    fig.tight_layout()

    return fig


def plot_damage_levels(output: list[DikernelOutputLocation], input: DikernelInput):
    """
    This

    Args:
        output (list[DikernelOutputLocation]): The calculation output
        input (DikernelInput): The specified calculation input (containing the cross-shore profile)

    Returns:
        figure handle: The handle of the produced figure
    """

    damagelevels = list(loc.final_damage for loc in output)
    xLocationPositions = list(loc.x_position for loc in output)

    fig = plt.figure()
    """
    Plot the final damage level.
    """
    ax1 = plt.subplot(2, 1, 1)
    ax1.grid()
    ax1.set(xlabel="Cross-shore position [x]", ylabel="Damage (end of storm)")
    plt.axhline(1.0, color="red", linewidth=2.0, linestyle="--")
    ax1.plot(
        xLocationPositions, damagelevels, linestyle="none", marker="o", color="black"
    )

    """
    Plot the cross-shore profile and output locations indicating whether the critical 
    damage level was reached or not.
    """
    xFailed = list(loc.x_position for loc in output if loc.failed)
    xPassed = list(loc.x_position for loc in output if not loc.failed)
    zFailed = numpy.interp(
        xFailed,
        input.dike_schematization.x_positions,
        input.dike_schematization.z_positions,
    )
    zPassed = numpy.interp(
        xPassed,
        input.dike_schematization.x_positions,
        input.dike_schematization.z_positions,
    )

    ax2 = plt.subplot(2, 1, 2, sharex=ax1)
    ax2.grid()
    ax2.set(ylabel="Height [m]", xlabel="Cross-shore position [x]")
    ax2.plot(
        input.dike_schematization.x_positions,
        input.dike_schematization.z_positions,
        linestyle="solid",
        color="black",
        marker="o",
    )
    ax2.plot(xPassed, zPassed, marker="o", color="g")
    ax2.plot(xFailed, zFailed, marker="x", color="r")

    fig.tight_layout()

    return fig
