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

import matplotlib.pyplot as plt
import numpy as numpy
from dikerosion.data import (
    DikernelInput,
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    NaturalStoneOutputLocation,
    TimeDependentOutputQuantity,
)


def plot_hydrodynamic_conditions(input: DikernelInput):
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
    fig.suptitle("Hydrodynamic conditions", fontsize=16)

    """
    Water levels
    """
    axs[0, 0].plot(
        run_input.hydrodynamic_input.time_steps,
        numpy.concatenate(
            ([None], run_input.hydrodynamic_input.water_levels), axis=None
        ),
        "gx",
        linestyle="dotted",
    )
    axs[0, 0].plot(
        input.hydrodynamic_input.time_steps,
        numpy.concatenate(([None], input.hydrodynamic_input.water_levels), axis=None),
        "bo",
    )
    axs[0, 0].set(ylabel="Water level [m]")
    axs[0, 0].grid()

    """
    Wave heights
    """
    axs[1, 0].plot(
        run_input.hydrodynamic_input.time_steps,
        numpy.concatenate(
            ([None], run_input.hydrodynamic_input.wave_heights), axis=None
        ),
        "gx",
        linestyle="dotted",
    )
    axs[1, 0].plot(
        input.hydrodynamic_input.time_steps,
        numpy.concatenate(([None], input.hydrodynamic_input.wave_heights), axis=None),
        "bo",
    )
    axs[1, 0].set(xlabel="Time step [s]", ylabel="Wave height [m]")
    axs[1, 0].grid()

    """
    Wave periods
    """
    axs[0, 1].plot(
        run_input.hydrodynamic_input.time_steps,
        numpy.concatenate(
            ([None], run_input.hydrodynamic_input.wave_periods), axis=None
        ),
        "gx",
        linestyle="dotted",
    )
    axs[0, 1].plot(
        input.hydrodynamic_input.time_steps,
        numpy.concatenate(([None], input.hydrodynamic_input.wave_periods), axis=None),
        "bo",
    )
    axs[0, 1].set(ylabel="Wave periods [s]")
    axs[0, 1].grid()

    """
    Wave directions
    """
    axs[1, 1].plot(
        run_input.hydrodynamic_input.time_steps,
        numpy.concatenate(
            ([None], run_input.hydrodynamic_input.wave_directions), axis=None
        ),
        "gx",
        linestyle="dotted",
    )
    axs[1, 1].plot(
        input.hydrodynamic_input.time_steps,
        numpy.concatenate(
            ([None], input.hydrodynamic_input.wave_directions), axis=None
        ),
        "bo",
    )
    axs[1, 1].set(xlabel="Time step [s]", ylabel="Wave angles [degrees]")
    axs[1, 1].grid()

    fig.tight_layout()

    return fig


def plot_damage_levels(
    output: list[DikernelOutputLocation],
    input: DikernelInput,
    plot_development: bool = True,
):
    """
    This method plots the damage levels at all output locations (upper plot) and whether
    an output location failed or not (lower plot). Optional (default is True), the
    method also includes the development in time of the damage level in the first plot.

    Args:
        output (list[DikernelOutputLocation]): The calculation output
        input (DikernelInput): The specified calculation input (containing the cross-shore profile)

    Returns:
        figure handle: The handle of the produced figure
    """

    final_damage_levels = list(loc.final_damage for loc in output)
    x_positions_output_locations = list(loc.x_position for loc in output)

    fig = plt.figure()
    """
    Plot the final damage level and development.
    """
    ax1 = plt.subplot(2, 1, 1)
    ax1.grid()
    ax1.set(xlabel="Cross-shore position [x]", ylabel="Damage (end of storm)")

    if plot_development:
        run_times = input.get_run_time_steps()
        x_positions = [loc.x_position for loc in output]

        values = [[None for x in range(len(run_times) - 1)] for y in range(len(output))]
        for i_loc, location in enumerate(output):
            values[i_loc] = getattr(
                location, TimeDependentOutputQuantity.DamageDevelopment.value
            )

        colors = plt.cm.winter(numpy.linspace(0, 1, len(run_times) - 1))
        for i in range(len(values[0])):
            ax1.plot(
                x_positions,
                [row[i] for row in values],
                color=colors[i],
                linestyle="-",
                marker="o",
                markersize=4,
            )

    plt.axhline(1.0, color="red", linewidth=2.0, linestyle="--")
    ax1.plot(
        x_positions_output_locations,
        final_damage_levels,
        linestyle="none",
        marker="o",
        color="black",
    )

    """
    Plot the cross-shore profile and output locations indicating whether the critical 
    damage level was reached or not.
    """
    x_failed = list(loc.x_position for loc in output if loc.failed)
    x_passed = list(loc.x_position for loc in output if not loc.failed)
    z_failed = numpy.interp(
        x_failed,
        input.dike_schematization.x_positions,
        input.dike_schematization.z_positions,
    )
    z_passed = numpy.interp(
        x_passed,
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
    ax2.plot(x_passed, z_passed, linestyle="none", marker="o", color="g")
    ax2.plot(x_failed, z_failed, linestyle="none", marker="x", color="r")

    fig.tight_layout()

    return fig


def plot_development_per_location(
    location: DikernelOutputLocation,
    quantity: TimeDependentOutputQuantity,  # TODO: Maybe plot multiple quantities?
    input: DikernelInput,
):
    """
    This method plots the development of a particular output variable in time for a specific location.

    Args:
        location (DikernelOutputLocation): The location holding the output that should be visualized.
        quantity (TimeDependentOutputQuantity): The quantity that should be visualized.

    Returns:
        figure handle: The handle of the produced figure
    """
    fig = plt.figure()

    run_times = input.get_run_time_steps()
    try:
        values: list[float] = getattr(location, quantity.value)
    except:
        # No such variable in this output locations
        return None

    color = "black"
    match location:
        case AsphaltWaveImpactOutputLocation():
            color = "gray"
        case GrassOvertoppingOutputLocation():
            color = "darkgreen"
        case GrassWaveImpactOutputLocation():
            color = "darkgreen"
        case NaturalStoneOutputLocation():
            color = "black"

    ax = plt.subplot(111)
    ax.grid()
    ax.plot(run_times, [None] + values, color=color)
    ax.set(ylabel=quantity.name, xlabel="Time step [s]")
    fig.suptitle(
        quantity.name + " in time [x = " + str(location.x_position) + " m]",
        fontsize=14,
    )
    fig.tight_layout()

    return fig


def plot_development(
    locations: list[DikernelOutputLocation],
    quantity: TimeDependentOutputQuantity,
    input: DikernelInput,
):
    """
    This method plots the development of a specific quantity in time for all output
    locations (for all cross-shore positions).

    Args:
        locations (list[DikernelOutputLocation]): The output locations to plot results for.
        quantity (TimeDependentOutputQuantity): The quantity that should be visualized.
        input (DikernelInput): Input containing the time steps of the generated output.

    Returns:
        _type_: _description_
    """
    fig = plt.figure()

    run_times = input.get_run_time_steps()
    x_positions = [loc.x_position for loc in locations]

    values = [[None for x in range(len(run_times) - 1)] for y in range(len(locations))]
    for i_loc, location in enumerate(locations):
        values[i_loc] = getattr(location, quantity.value)

    colors = plt.cm.winter(numpy.linspace(0, 1, len(run_times) - 1))

    ax = plt.subplot(111)
    ax.grid()
    for i in range(len(values[0])):
        ax.plot(x_positions, [row[i] for row in values], color=colors[i])

    ax.set(ylabel=quantity.name, xlabel="Cross-shore position [m]")

    fig.tight_layout()

    return fig
