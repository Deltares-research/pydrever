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

# region Imports
import sys
import os
import numpy
import matplotlib.pyplot as plt
import copy

sys.path.append(os.getcwd())

from dikerosion.data import (
    DikernelInput,
    DikeSchematization,
    HydrodynamicConditions,
    GrassWaveImpactOutputLocationSpecification,
    TopLayerType,
)
from dikerosion.dikernel import Dikernel
from dikerosion.visualization import (
    plot_hydrodynamic_conditions,
    animate_damage_development,
)

# endregion

# region Input specification
"""
Define the dike schematization:
    x-coordinates
    z-coordinate
    roughnesses (per segment, from one x towards the next x)
    characteristic points (outer toe and outer crest are )
"""
x_positions = [0.0, 24.0, 35.0, 41.0, 45.01, 50, 60, 70]
z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
dike_schematization = DikeSchematization(
    0.0, x_positions, z_positions, roughnesses, 24.0, 45.01
)

"""
Specify hydrodynamic conditions"
    Time steps (always start with the start time of the time series)
    Water levels (for each period between two time steps)
    Wave heights (for each period between two time steps)
    Wave periods (for each period between two time steps)
    Wave directions (relative to north, for each period between two time steps)
"""
# time_steps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
# water_levels = [1.2, 1.9, 2.8, 2.7, 2.0]
# wave_heights = [0.5, 0.9, 1.2, 1.1, 0.8]
# wave_periods = [6.0, 6.0, 6.0, 6.0, 6.0]
# wave_directions = [60.0, 70.0, 80.0, 90.0, 100.0]

# hydrodynamic_conditions = HydrodynamicConditions(
#     time_steps, water_levels, wave_heights, wave_periods, wave_directions
# )

time_steps = numpy.linspace(
    0.0, 126000.0, int(126000.0 / 1000.0), dtype=float, endpoint=True
)

phase_water_levels = numpy.pi / 64.0
amplitude_water_levels = 1.3
minimum_water_level = 0.5
water_levels = (
    amplitude_water_levels
    * (1 - numpy.cos(time_steps[1:] / 1000.0 * phase_water_levels))
    + minimum_water_level
)

phase_wave_heights = numpy.pi / 32.0
ampltude_waves = 0.5
minimum_wave_height = 0.8
wave_heights = (
    ampltude_waves * (1 - numpy.cos(time_steps[1:] / 1000.0 * phase_wave_heights))
    + minimum_wave_height
)

# wave_periods = 7.0 + time_steps[1:] * 0
wave_periods = 7.0 + time_steps[1:] / 1000.0 * 0.01
wave_directions = time_steps[1:] * 0 + 15.0
# wave_directions = -20 + time_steps[1:] / 1000.0 * 0.5
# wave_directions = [
#    d + 360 if d < 0 else d - 360 if d > 360 else d for d in wave_directions
# ]

hydrodynamic_conditions = HydrodynamicConditions(
    time_steps, water_levels, wave_heights, wave_periods, wave_directions
)

"""
Create the input object
"""
input = DikernelInput(hydrodynamic_conditions, dike_schematization)

"""
Define output time steps and start time for the calculation
"""
input.start_time = 0.0
output_time_steps = numpy.arange(0.0, 126000, 1000)
output_time_steps = numpy.union1d(hydrodynamic_conditions.time_steps, output_time_steps)
# input.output_time_steps = output_time_steps

"""
Define output locations. For eacht location where a calculation should be performed, 
define a locations that specifies the required input (based on the type of revetment)
"""
base_specification = GrassWaveImpactOutputLocationSpecification(
    None, TopLayerType.GrassClosedSod
)
base_x_min = 25.00
base_x_max = 45.00
stepsizes = [1, 0.5, 0.1, 0.05, 0.01]

inputs = []
x_output_positions = []
damage_numbers = []
for stepsize in stepsizes:
    new_input = copy.deepcopy(input)

    n_steps = numpy.ceil((base_x_max - base_x_min) / stepsize)
    x_positions = numpy.linspace(base_x_min, base_x_max, n_steps.astype(int))
    output_specifications = []
    for x_position in x_positions:
        new_location = copy.deepcopy(base_specification)
        new_location.x_position = x_position
        output_specifications.append(new_location)

    new_input.output_locations = output_specifications

    kernel = Dikernel(new_input)
    validation_result = kernel.validate()
    if not validation_result:
        print("Something went wrong:")
        for message in kernel.validation_messages:
            print("   %s" % (message))
        quit()

    runresult = kernel.run()

    inputs.append(new_input)
    x_output_positions.append([l.x_position for l in kernel.output])
    damage_numbers.append([l.damage_development[-1] for l in kernel.output])


animate_damage_development(kernel.input, kernel.output)
plot_hydrodynamic_conditions(input)

colors = plt.cm.tab10(numpy.linspace(0, 1, len(inputs)))
markers = ["x", "o", "s", "d", "."]

fig = plt.figure()
ax1 = plt.subplot(2, 1, 1)
ax1.legend()
# fig.suptitle("", fontsize=16)

for i_series, x_series in enumerate(x_output_positions):
    ax1.plot(
        x_series,
        damage_numbers[i_series],
        color=colors[i_series],
        marker=None,
        label="stapgrootte = %s [m]" % stepsizes[i_series],
        linestyle="solid",
    )
ax1.set(ylabel="damage levels [m]")
ax1.legend()
ax1.grid()

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

plt.show()
# endregion
