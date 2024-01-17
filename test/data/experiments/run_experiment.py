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
import matplotlib.pyplot as plt

sys.path.append(os.getcwd() + "\src")
sys.path.append(os.getcwd() + "\src\dikerneldll")

from experiment_bgd_deltaflume import BgdDeltaFlumeExperiment
from dikernel import Dikernel
from visualization import (
    plot_hydraulic_conditions,
    plot_damage_levels,
    plot_development_per_location,
    TimeDependentOutputQuantity,
)

input = BgdDeltaFlumeExperiment.get_calculation_input()
kernel = Dikernel(input)
plot_hydraulic_conditions(input)

validationResult = kernel.validate()
if not validationResult:
    for message in kernel.validation_messages:
        print(message)
    quit()

runResult = kernel.run()
if not runResult:
    for message in kernel.validation_messages:
        print(message)
    quit()

output = kernel.output

plot_damage_levels(output, input)
for location in output:
    f = plot_development_per_location(
        location, TimeDependentOutputQuantity.DamageDevelopment, input
    )
    f.suptitle("Location x = %0.2f[m]" % location.x_position)
    f.tight_layout()

plt.show()
