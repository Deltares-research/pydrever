import sys
import os
import numpy
import matplotlib.pyplot as plt

sys.path.append(os.getcwd() + "\src")
sys.path.append(os.getcwd() + "\src\dikerneldll")

from visualization import *

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


x_positions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
dike_schematization = DikeSchematization(
    x_positions, z_positions, roughnesses, 25.0, 45.0
)
time_steps = [0.0, 25000.0, 50000.0, 75000.0, 100000.0, 126000.0]
time_steps = list(numpy.array(time_steps) * 0.0001)
water_levels = [1.5, 2.3, 3.5, 3.2, 2.4]
water_levels = list(numpy.array(water_levels) * 0.8)
wave_heights = [3.5, 3.9, 4.2, 4.1, 2.8]
wave_periods = [8.0, 8.0, 8.0, 8.0, 8.0]
wave_directions = [60.0, 70.0, 80.0, 90.0, 100.0]

hydraulic_conditions = HydraulicConditions(
    time_steps, water_levels, wave_heights, wave_periods, wave_directions
)

output_time_steps = numpy.arange(0.0, 12.6, 0.1)
output_time_steps = numpy.union1d(time_steps, output_time_steps)

input = DikernelInput(90.0, hydraulic_conditions, dike_schematization)
input.start_time = 0.0
input.output_time_steps = output_time_steps

input.output_locations = [
    GrassWaveImpactOutputLocationSpecification(41.1, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(41.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(42.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.0, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(43.5, 0.0, TopLayerType.GrassClosedSod),
    GrassWaveImpactOutputLocationSpecification(44.0, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.5, 0.0, TopLayerType.GrassOpenSod),
    GrassWaveImpactOutputLocationSpecification(44.99, 0.0, TopLayerType.GrassClosedSod),
]

kernel = Dikernel(input)
validation_result = kernel.validate()
if validation_result:
    runresult = kernel.run()
    print("Run was: " + "succesfull" if runresult else "unsuccessfull")
    output = kernel.output
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

    runInput = input.get_run_input()
    runTimeSteps = runInput.hydraulic_input.time_steps
    waterLevels2 = runInput.hydraulic_input.water_levels
    waveHeights2 = runInput.hydraulic_input.wave_heights
    wavePeriods2 = runInput.hydraulic_input.wave_periods
    waveDirections2 = runInput.hydraulic_input.wave_directions

    fig = plot_hydraulic_conditions(input)
    # fig.savefig("C:/Test/testimage.png")

    damagelevels = list(loc.final_damage for loc in output)
    xLocationPositions = list(loc.x_position for loc in output)

    fig2, ax = plt.subplots(ncols=1, nrows=1)
    ax.set(xlabel="Cross-shore position [x]", ylabel="Damage (end of storm)")
    ax.tick_params(axis="y", colors="b")
    ax.yaxis.label.set_color("b")
    plt.axhline(1.0, color="red", linewidth=2.0, linestyle="--")
    ax.grid()
    ax.set_facecolor("None")
    ax.plot(xLocationPositions, damagelevels, color="b")

    ax2 = ax.twinx()
    ax2.set(ylabel="Height [m]")
    ax2.plot(
        dike_schematization.x_positions,
        dike_schematization.z_positions,
        linestyle="solid",
        color="lightgray",
        marker="o",
    )
    ax2.set_facecolor("white")
    ax2.tick_params(axis="y", colors="lightgray")
    ax2.yaxis.label.set_color("lightgray")

    ax.set_zorder(1)
    ax2.set_zorder(0)

    fig2.tight_layout()
    plt.show()

else:
    for message in kernel.validation_messages:
        print(message)
