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

import sys
import os
import numpy
import matplotlib.pyplot as plt

sys.path.append(os.getcwd() + "\src")
sys.path.append(os.getcwd() + "\src\dikerneldll")

# region Imports
from visualization import plot_damage_levels, plot_hydraulic_conditions

from dikernelinput import (
    DikernelInput,
    DikeSchematization,
    HydraulicConditions,
)
from dikerneloutputlocations import (
    GrassWaveImpactOutputLocationSpecification,
)
from toplayertypes import TopLayerType
from dikernel import Dikernel

# endregion

# region Input specification
"""
Define the dike schematization:
    x-coordinates
    z-coordinate
    roughnesses (per segment, from one x towards the next x)
    characteristic points (outer toe and outer crest are )
"""
x_positions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
dike_schematization = DikeSchematization(
    x_positions, z_positions, roughnesses, 25.0, 45.0
)

"""
Specify hydrodynamic conditions"
    Time steps (always start with the start time of the time series)
    Water levels (for each period between two time steps)
    Wave heights (for each period between two time steps)
    Wave periods (for each period between two time steps)
    Wave directions (relative to north, for each period between two time steps)
"""
time_steps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
water_levels = [1.2, 1.9, 2.8, 2.7, 2.0]
wave_heights = [0.5, 0.9, 1.2, 1.1, 0.8]
wave_periods = [6.0, 6.0, 6.0, 6.0, 6.0]
wave_directions = [60.0, 70.0, 80.0, 90.0, 100.0]

hydraulic_conditions = HydraulicConditions(
    time_steps, water_levels, wave_heights, wave_periods, wave_directions
)

"""
Create the input object
"""
input = DikernelInput(90.0, hydraulic_conditions, dike_schematization)

"""
Define output time steps and start time for the calculation
"""
input.start_time = 0.0
output_time_steps = numpy.arange(0.0, 126000, 1000)
output_time_steps = numpy.union1d(time_steps, output_time_steps)
input.output_time_steps = output_time_steps

"""
Define output locations. For eacht location where a calculation should be performed, 
define a locations that specifies the required input (based on the type of revetment)
"""
input.output_locations = [
    GrassWaveImpactOutputLocationSpecification(41.1, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(41.5, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.5, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.5, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(44.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.5, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.99, TopLayerType.GrassClosedSod),
]
# endregion

# region Validation
"""
Validate the input of the calculation
"""
kernel = Dikernel(input)
validation_result = kernel.validate()

if not validation_result:
    for message in kernel.validation_messages:
        print(message)
    quit()
# endregion

# region Perform calculation
"""
Run the calculation
"""
runresult = kernel.run()

"""
Print success (or not)
"""
print("Run was: " + "succesfull" if runresult else "unsuccessfull")
if not runresult:
    for message in kernel.validation_messages:
        print(message)
    quit()
# endregion

# region Output visualization
output = kernel.output

"""
Process the output and print results
"""
print("Number of output locations: " + str(len(output)))
for location in output:
    print(
        "   "
        + ("Failed" if location.failed else "Not failed")
        + ", X: "
        + str(location.x_position)
        + ", Damage level = "
        + str(location.damage_development[-1])
    )

"""
Plot hydrodynamic input
"""
fig = plot_hydraulic_conditions(input)
# fig.savefig("C:/Test/testimage.png")

fig2 = plot_damage_levels(output, input)
# fig2.savefig("C:/Test/testimage.png")

plt.show()
# endregion
