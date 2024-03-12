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

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as numpy
from pydrever.data import DikernelInput, DikernelOutputLocation


def animate_damage_development(
    input: DikernelInput, output: list[DikernelOutputLocation]
):
    from matplotlib import animation

    run_input = input.get_run_input()
    x_positions = [l.x_position for l in output]
    damage_development = [[0.0] * len(x_positions)]
    t_output = run_input.hydrodynamic_input.time_steps
    for i_time, time in enumerate(t_output[1:]):
        damage_development.append([l.damage_development[i_time] for l in output])
    max_damage = max(max(damage_development))

    fig = plt.figure()
    fig.suptitle("Tijd = %0.0f [sec]" % (0.0))
    fig.set_figwidth(7.2)
    fig.set_figheight(9)

    ax1 = plt.subplot(3, 1, 1)
    ax1.set(
        xlim=(min(x_positions) - 5, max(x_positions) + 5),
        ylim=(0.0 - 0.1 * max_damage, max_damage * 1.1),
        ylabel="Damage level",
        xlabel="Cross-shore position [x]",
    )
    colors = plt.cm.winter(numpy.linspace(0, 1, len(damage_development)))
    for i_damage, damage in enumerate(damage_development):
        ax1.fill_between(
            x_positions,
            damage,
            damage_development[i_damage - 1] if i_damage > 1 else 0,
            visible=True,
            color=colors[i_damage],
            zorder=len(damage_development) - i_damage,
        )
    (line,) = ax1.plot(x_positions, damage_development[0], linewidth=2, color="black")

    ax2 = plt.subplot(3, 1, 2, sharex=ax1)
    ax2.grid()
    ax2.set(ylabel="Height [m]", xlabel="Cross-shore position [x]")
    ax2.plot(
        input.dike_schematization.x_positions,
        input.dike_schematization.z_positions,
        linestyle="solid",
        color="black",
        marker="o",
    )
    water_level = plt.axhline(0.0, linewidth=2.0, color="blue", linestyle="solid")

    ax3 = plt.subplot(3, 1, 3)
    ax3.grid()
    ax3.set(ylabel="Water level [m]", xlabel="Time step [s]")
    ax3.plot(
        run_input.hydrodynamic_input.time_steps,
        [None] + run_input.hydrodynamic_input.water_levels,
        linestyle="dotted",
    )
    scat = ax3.scatter(
        run_input.hydrodynamic_input.time_steps,
        [None] + run_input.hydrodynamic_input.water_levels,
        c=[None] + run_input.hydrodynamic_input.wave_heights,
        s=10,
        cmap=mpl.colormaps["winter"],
        marker="o",
    )
    vline = plt.axvline(0.0, color="red", linewidth=2.0, linestyle="--")
    color_bar = plt.colorbar(scat, ax=ax3)
    color_bar.set_label("Wave height [m]", rotation=270)

    fig.tight_layout()

    # initialization function: plot the background of each frame
    def init():
        line.set_data(x_positions, damage_development[0])
        return (line,)

    def update_i():
        i_max = len(damage_development) - 1
        i = 0
        while anim.running:
            yield i
            i += anim.direction
            if i < 0:
                i += i_max
            if i > i_max:
                i -= i_max

    def animate(i):
        # for i_area, area in enumerate(areas):
        #    area.visible = i_area <= i
        try:
            line.set_data(x_positions, damage_development[i])
        except:
            print("Oops")
        fig.suptitle("Tijd = %0.0f [sec]" % (t_output[i]))
        vline.set_xdata(t_output[i])
        water_level.set_ydata(
            run_input.hydrodynamic_input.water_levels[max([0, i - 1])]
        )
        fig.canvas.draw()
        return (line,)

    def on_key_press(event):
        if event.key.isspace():
            if anim.running:
                anim.event_source.stop()
            else:
                anim.event_source.start()
            anim.running ^= True

    def on_button_press(event):
        if event.button.name == "LEFT":
            anim.direction = -1
        elif event.button.name == "RIGHT":
            anim.direction = +1
        anim.event_source.frames = update_i

    fig.canvas.mpl_connect("key_press_event", on_key_press)
    fig.canvas.mpl_connect("button_press_event", on_button_press)

    # call the animator.  blit=True means only re-draw the parts that have changed.
    anim = animation.FuncAnimation(
        fig,
        animate,
        init_func=init,
        frames=update_i,
        interval=20,
        blit=True,
    )

    anim.running = True
    anim.direction = +1
