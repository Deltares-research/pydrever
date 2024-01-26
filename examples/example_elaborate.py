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

# region Imports
import sys
import os

sys.path.append(os.getcwd())

from dikerosion.data.dikerneloutput import CalculationMethod
from dikerosion.data.toplayertypes import TopLayerType

from dikerosion.data.dikernelinput import (
    DikernelInput,
    DikeSchematization,
    HydrodynamicConditions,
)
from dikerosion.data.dikerneloutputspecification import (
    OutputLocationSpecification,
    GrassWaveImpactOutputLocationSpecification,
    GrassWaveRunupOutputLocationSpecification,
    GrassOvertoppingOutputLocationSpecification,
    AsphaltOutputLocationSpecification,
    NordicStoneOutputLocationSpecification,
)
from dikerosion.data.dikernelcalculationsettings import (
    CalculationSettings,
    AsphaltCalculationSettings,
    NaturalStoneCalculationSettings,
    NaturalStoneTopLayerSettings,
    GrassWaveImpactCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    AsphaltTopLayerSettings,
    GrasCoverCumulativeOverloadTopLayerSettings,
    GrassCoverWaveImpactTopLayerSettings,
)

from dikerosion.dikernel.dikernel import Dikernel

from dikerosion.data.quantities import TimeDependentOutputQuantity

from dikerosion.visualization.visualization_damage import (
    plot_damage_levels,
    plot_hydrodynamic_conditions,
    plot_development_per_location,
    plot_development,
)
import matplotlib.pyplot as plt

# endregion


# region define calculation input
def get_calculation_input() -> DikernelInput:
    input = DikernelInput(get_hydrodynamic_conditions(), get_dike_profile())
    input.output_locations = get_output_locations()
    input.settings = get_calculation_settings()
    return input


def get_hydrodynamic_conditions() -> HydrodynamicConditions:
    time_steps = [
        0.0,
        2269.440000000016,
        4538.879999999999,
        6808.320000000018,
        9077.760000000031,
        11347.200000000015,
        13616.64,
        15180.292682926836,
        16371.902439024394,
        17563.51219512195,
        18755.12195121951,
        19946.731707317074,
        21138.341463414636,
        22329.951219512193,
        23521.560975609762,
        24713.170731707323,
        25904.780487804877,
        27096.390243902435,
        28287.999999999993,
        29479.60975609755,
        30671.219512195123,
        31862.829268292684,
        33054.43902439024,
        34246.04878048779,
        35437.65853658537,
        36629.26829268294,
        37820.87804878049,
        39012.487804878045,
        40204.0975609756,
        41395.70731707315,
        42587.31707317072,
        43778.92682926828,
        44970.53658536586,
        46162.14634146341,
        47353.75609756097,
        48545.36585365854,
        49736.9756097561,
        50928.58536585365,
        52120.195121951205,
        53311.804878048766,
        54503.41463414634,
        55695.0243902439,
        56883.317073170736,
        58078.243902439026,
        59269.85365853659,
        60461.46341463415,
        61653.0731707317,
        62844.68292682927,
        64036.29268292684,
        65227.9024390244,
        66419.51219512196,
        67611.12195121952,
        68802.73170731709,
        69994.34146341465,
        71185.95121951221,
        72377.56097560977,
        73569.17073170732,
        74760.78048780488,
        75952.39024390244,
        77144.0,
        78335.60975609756,
        79527.21951219512,
        80718.82926829268,
        81910.43902439025,
        83102.0487804878,
        84293.65853658537,
        85485.26829268293,
        86676.87804878049,
        87868.48780487805,
        89060.09756097561,
        90251.70731707317,
        91441.65853658537,
        92634.9268292683,
        93826.53658536586,
        95018.14634146342,
        96209.75609756098,
        97401.36585365854,
        98592.9756097561,
        99784.58536585367,
        100976.19512195123,
        102167.80487804877,
        103359.41463414633,
        104551.0243902439,
        105742.63414634146,
        106934.24390243902,
        108125.85365853658,
        109317.46341463414,
        110509.0731707317,
        111700.68292682926,
        112892.29268292683,
        114083.90243902439,
        115275.51219512195,
        116467.12195121951,
        117658.73170731707,
        118850.34146341463,
        120041.9512195122,
        121233.56097560977,
        122425.17073170733,
        123616.78048780489,
        124808.39024390245,
        126000.0,
    ]
    water_levels = [
        0.50,
        0.50,
        0.51,
        0.52,
        0.54,
        0.56,
        0.59,
        0.62,
        0.66,
        0.70,
        0.75,
        0.80,
        0.85,
        0.91,
        0.97,
        1.04,
        1.10,
        1.17,
        1.25,
        1.32,
        1.40,
        1.48,
        1.56,
        1.64,
        1.72,
        1.80,
        1.88,
        1.96,
        2.04,
        2.12,
        2.20,
        2.28,
        2.35,
        2.43,
        2.50,
        2.56,
        2.63,
        2.69,
        2.75,
        2.80,
        2.85,
        2.90,
        2.94,
        2.98,
        3.01,
        3.04,
        3.06,
        3.08,
        3.09,
        3.10,
        3.10,
        3.10,
        3.09,
        3.08,
        3.06,
        3.04,
        3.01,
        2.98,
        2.94,
        2.90,
        2.85,
        2.80,
        2.75,
        2.69,
        2.63,
        2.56,
        2.50,
        2.43,
        2.35,
        2.28,
        2.20,
        2.12,
        2.04,
        1.96,
        1.88,
        1.80,
        1.72,
        1.64,
        1.56,
        1.48,
        1.40,
        1.32,
        1.25,
        1.17,
        1.10,
        1.04,
        0.97,
        0.91,
        0.85,
        0.80,
        0.75,
        0.70,
        0.66,
        0.62,
        0.59,
        0.56,
        0.54,
        0.52,
        0.51,
        0.50,
    ]
    wave_heights = [
        0.80,
        0.80,
        0.80,
        0.81,
        0.82,
        0.82,
        0.84,
        0.85,
        0.86,
        0.88,
        0.90,
        0.91,
        0.94,
        0.96,
        0.98,
        1.01,
        1.03,
        1.06,
        1.09,
        1.12,
        1.15,
        1.18,
        1.21,
        1.24,
        1.27,
        1.30,
        1.33,
        1.36,
        1.39,
        1.42,
        1.45,
        1.48,
        1.51,
        1.54,
        1.57,
        1.59,
        1.62,
        1.64,
        1.66,
        1.69,
        1.70,
        1.72,
        1.74,
        1.75,
        1.76,
        1.78,
        1.78,
        1.79,
        1.80,
        1.80,
        1.80,
        1.80,
        1.80,
        1.79,
        1.78,
        1.78,
        1.76,
        1.75,
        1.74,
        1.72,
        1.70,
        1.69,
        1.66,
        1.64,
        1.62,
        1.59,
        1.57,
        1.54,
        1.51,
        1.48,
        1.45,
        1.42,
        1.39,
        1.36,
        1.33,
        1.30,
        1.27,
        1.24,
        1.21,
        1.18,
        1.15,
        1.12,
        1.09,
        1.06,
        1.03,
        1.01,
        0.98,
        0.96,
        0.94,
        0.91,
        0.90,
        0.88,
        0.86,
        0.85,
        0.84,
        0.82,
        0.82,
        0.81,
        0.80,
        0.80,
    ]
    wave_periods = [
        7,
        7.06,
        7.12,
        7.18,
        7.24,
        7.3,
        7.36,
        7.42,
        7.48,
        7.54,
        7.6,
        7.66,
        7.72,
        7.78,
        7.84,
        7.9,
        7.96,
        8.02,
        8.08,
        8.14,
        8.2,
        8.26,
        8.32,
        8.38,
        8.44,
        8.5,
        8.56,
        8.62,
        8.68,
        8.74,
        8.8,
        8.86,
        8.92,
        8.98,
        9.04,
        9.1,
        9.16,
        9.22,
        9.28,
        9.34,
        9.4,
        9.46,
        9.52,
        9.58,
        9.64,
        9.7,
        9.76,
        9.82,
        9.88,
        9.94,
        10,
        10.06,
        10.12,
        10.18,
        10.24,
        10.3,
        10.36,
        10.42,
        10.48,
        10.54,
        10.6,
        10.66,
        10.72,
        10.78,
        10.84,
        10.9,
        10.96,
        11.02,
        11.08,
        11.14,
        11.2,
        11.26,
        11.32,
        11.38,
        11.44,
        11.5,
        11.56,
        11.62,
        11.68,
        11.74,
        11.8,
        11.86,
        11.92,
        11.98,
        12.04,
        12.1,
        12.16,
        12.22,
        12.28,
        12.34,
        12.4,
        12.46,
        12.52,
        12.58,
        12.64,
        12.7,
        12.76,
        12.82,
        12.88,
        12.94,
    ]
    wave_directions = [
        -20 + 360,
        -19.5 + 360,
        -19 + 360,
        -18.5 + 360,
        -18 + 360,
        -17.5 + 360,
        -17 + 360,
        -16.5 + 360,
        -16 + 360,
        -15.5 + 360,
        -15 + 360,
        -14.5 + 360,
        -14 + 360,
        -13.5 + 360,
        -13 + 360,
        -12.5 + 360,
        -12 + 360,
        -11.5 + 360,
        -11 + 360,
        -10.5 + 360,
        -10 + 360,
        -9.5 + 360,
        -9 + 360,
        -8.5 + 360,
        -8 + 360,
        -7.5 + 360,
        -7 + 360,
        -6.5 + 360,
        -6 + 360,
        -5.5 + 360,
        -5 + 360,
        -4.5 + 360,
        -4 + 360,
        -3.5 + 360,
        -3 + 360,
        -2.5 + 360,
        -2 + 360,
        -1.5 + 360,
        -1 + 360,
        -0.5 + 360,
        0,
        0.5,
        1,
        1.5,
        2,
        2.5,
        3,
        3.5,
        4,
        4.5,
        5,
        5.5,
        6,
        6.5,
        7,
        7.5,
        8,
        8.5,
        9,
        9.5,
        10,
        10.5,
        11,
        11.5,
        12,
        12.5,
        13,
        13.5,
        14,
        14.5,
        15,
        15.5,
        16,
        16.5,
        17,
        17.5,
        18,
        18.5,
        19,
        19.5,
        20,
        20.5,
        21,
        21.5,
        22,
        22.5,
        23,
        23.5,
        24,
        24.5,
        25,
        25.5,
        26,
        26.5,
        27,
        27.5,
        28,
        28.5,
        29,
        29.5,
    ]
    return HydrodynamicConditions(
        time_steps, water_levels, wave_heights, wave_periods, wave_directions
    )


def get_dike_profile() -> DikeSchematization:
    x_positions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
    z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
    roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
    schematization = DikeSchematization(
        0.0, x_positions, z_positions, roughnesses, 25.0, 45.0
    )
    schematization.crest_outer_berm = 35.0
    schematization.notch_outer_berm = 41.0
    schematization.inner_crest = 50.0
    schematization.inner_toe = 60.0
    return schematization


def get_output_locations() -> list[OutputLocationSpecification]:
    return [
        NordicStoneOutputLocationSpecification(25.01, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(25.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(26.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(26.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(27.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(27.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(28.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(28.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(29.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(29.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(30.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(30.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(31.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(31.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(32.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(32.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(33.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(33.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(34.0, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(34.5, 0.28, 2.45),
        NordicStoneOutputLocationSpecification(34.9, 0.28, 2.45),
        AsphaltOutputLocationSpecification(35.1, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(35.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(36.0, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(36.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(37.0, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(37.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(38.0, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(38.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(39.0, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(39.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(40.0, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(40.5, 0.9, 64.0, 0.146, 5712.0),
        AsphaltOutputLocationSpecification(40.9, 0.9, 64.0, 0.146, 5712.0),
        GrassWaveImpactOutputLocationSpecification(41.1, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(41.5, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(42.0, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(42.5, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(43.0, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(43.5, TopLayerType.GrassClosedSod),
        GrassWaveImpactOutputLocationSpecification(44.0, TopLayerType.GrassOpenSod),
        GrassWaveImpactOutputLocationSpecification(44.5, TopLayerType.GrassOpenSod),
        GrassWaveImpactOutputLocationSpecification(44.99, TopLayerType.GrassClosedSod),
        GrassWaveRunupOutputLocationSpecification(
            41.5, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(
            42.0, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(
            42.5, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(
            41.1, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(
            43.0, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(
            43.5, 0.3, TopLayerType.GrassClosedSod
        ),
        GrassWaveRunupOutputLocationSpecification(44.0, 0.3, TopLayerType.GrassOpenSod),
        GrassWaveRunupOutputLocationSpecification(44.5, 0.3, TopLayerType.GrassOpenSod),
        GrassWaveRunupOutputLocationSpecification(
            44.99, 0.3, TopLayerType.GrassClosedSod
        ),
        create_grass_overtopping_output_location_closed_sod(45.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(45.5, 0.02),
        create_grass_overtopping_output_location_closed_sod(46.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(46.5, 0.02),
        create_grass_overtopping_output_location_closed_sod(47.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(47.5, 0.02),
        create_grass_overtopping_output_location_closed_sod(48.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(48.5, 0.02),
        create_grass_overtopping_output_location_closed_sod(49.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(49.5, 0.02),
        create_grass_overtopping_output_location_closed_sod(49.99, 0.02),
        create_grass_overtopping_output_location_closed_sod(52.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(54.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(56.0, 0.02),
        create_grass_overtopping_output_location_closed_sod(58.0, 0.02),
    ]


def create_grass_overtopping_output_location_closed_sod(
    x: float, initial_damage: float = 0.0
) -> GrassOvertoppingOutputLocationSpecification:
    specification = GrassOvertoppingOutputLocationSpecification(
        x, TopLayerType.GrassClosedSod
    )
    specification.initial_damage = initial_damage
    return specification


def get_calculation_settings() -> list[CalculationSettings]:
    return [
        get_asphalt_calculation_settings(),
        get_natural_stone_calculation_settings(),
        get_grass_wave_impact_calculation_settings(),
        get_grass_wave_overtopping_calculation_settings(),
    ]


def get_asphalt_calculation_settings() -> AsphaltCalculationSettings:
    top_layer = AsphaltTopLayerSettings()
    top_layer.stiffness_ratio_nu = 0.35
    top_layer.fatigue_asphalt_alpha = 0.5
    top_layer.fatigue_asphalt_beta = 5.4

    settings = AsphaltCalculationSettings([top_layer])
    settings.density_of_water = 1000.0
    settings.factor_ctm = 1.0
    settings.impact_number_c = 1.0
    settings.width_factors = [
        [0.1, 0.0392],
        [0.2, 0.0738],
        [0.3, 0.1002],
        [0.4, 0.1162],
        [0.5, 0.1213],
        [0.6, 0.1168],
        [0.7, 0.1051],
        [0.8, 0.089],
        [0.9, 0.0712],
        [1.0, 0.0541],
        [1.1, 0.0391],
        [1.2, 0.0269],
        [1.3, 0.0216],
        [1.4, 0.015],
        [1.5, 0.0105],
    ]
    settings.depth_factors = [
        [-1.0, 0.005040816326530646],
        [-0.9744897959183674, 0.00596482278562177],
        [-0.9489795918367347, 0.007049651822326582],
        [-0.923469387755102, 0.008280657034496978],
        [-0.8979591836734694, 0.009643192019984783],
        [-0.8724489795918368, 0.011122610376641823],
        [-0.846938775510204, 0.012704265702320014],
        [-0.8214285714285714, 0.014373511594871225],
        [-0.7959183673469388, 0.016115701652147284],
        [-0.7704081632653061, 0.017916189471999994],
        [-0.7448979591836735, 0.019760328652281334],
        [-0.7193877551020409, 0.02163347279084307],
        [-0.6938775510204082, 0.02352097548553716],
        [-0.6683673469387754, 0.025408190334215378],
        [-0.6428571428571429, 0.027280470934729583],
        [-0.6173469387755102, 0.029123170884931715],
        [-0.5918367346938775, 0.030921643782673508],
        [-0.5663265306122449, 0.03266124322580695],
        [-0.5408163265306123, 0.034327322812183814],
        [-0.5153061224489797, 0.03590523613965599],
        [-0.4897959183673469, 0.036419783440920166],
        [-0.4642857142857143, 0.03634372210983519],
        [-0.4387755102040817, 0.03603984556448696],
        [-0.41326530612244894, 0.0355249692161967],
        [-0.3877551020408163, 0.03481590847628564],
        [-0.3622448979591837, 0.033929478756075014],
        [-0.33673469387755095, 0.032882495466886014],
        [-0.31122448979591844, 0.03169177402003989],
        [-0.2857142857142858, 0.03037412982685786],
        [-0.2602040816326531, 0.028946378298661132],
        [-0.23469387755102034, 0.02742533484677094],
        [-0.2091836734693877, 0.02582781488250851],
        [-0.1836734693877552, 0.024170633817195083],
        [-0.15816326530612246, 0.022470607062151843],
        [-0.13265306122448983, 0.02074455002870004],
        [-0.1071428571428571, 0.019009278128160882],
        [-0.08163265306122447, 0.01728160677185561],
        [-0.056122448979591955, 0.015578351371105446],
        [-0.030612244897959218, 0.01391632733723159],
        [-0.005102040816326481, 0.012312350081555283],
        [0.020408163265306145, 0.010783235015397755],
        [0.04591836734693877, 0.00934579755008022],
        [0.0714285714285714, 0.008016853096923902],
        [0.09693877551020402, 0.006813217067250026],
        [0.12244897959183665, 0.005751704872379814],
        [0.1479591836734695, 0.004849131923634483],
        [0.17346938775510212, 0.004122313632335269],
        [0.19897959183673475, 0.0035880654098033892],
        [0.22448979591836737, 0.003263202667360069],
        [0.25, 0.0031645408163265307],
    ]
    settings.impact_factors = [
        [2.0, 0.039],
        [2.4, 0.1],
        [2.8, 0.18],
        [3.2, 0.235],
        [3.6, 0.2],
        [4.0, 0.13],
        [4.4, 0.08],
        [4.8, 0.02],
        [5.2, 0.01],
        [5.6, 0.005],
        [6.0, 0.001],
    ]

    return settings


def get_natural_stone_calculation_settings() -> NaturalStoneCalculationSettings:
    topLayer = NaturalStoneTopLayerSettings()
    topLayer.stability_plunging_a = 4.0
    topLayer.stability_plunging_b = 0.0
    topLayer.stability_plunging_c = 0.0
    topLayer.stability_plunging_n = -0.9
    topLayer.stability_surging_a = 0.8
    topLayer.stability_surging_b = 0.0
    topLayer.stability_surging_c = 0.0
    topLayer.stability_surging_n = 0.6
    topLayer.xib = 2.9

    settings = NaturalStoneCalculationSettings([topLayer])
    settings.distance_maximum_wave_elevation_a = 0.42
    settings.distance_maximum_wave_elevation_b = 0.9
    settings.slope_upper_level = 0.05
    settings.sLope_lower_level = 1.5
    settings.normative_width_of_wave_impact_a = 0.96
    settings.normative_width_of_wave_impact_b = 0.11
    settings.upper_limit_loading_a = 0.1
    settings.upper_limit_loading_b = 0.6
    settings.upper_limit_loading_c = 4.0
    settings.lower_limit_loading_a = 0.1
    settings.lower_limit_loading_b = 0.2
    settings.lower_limit_loading_c = 4.0
    settings.wave_angle_impact_beta_max = 78.0
    return settings


def get_grass_wave_impact_calculation_settings() -> GrassWaveImpactCalculationSettings:
    top_layer_closed_sod = GrassCoverWaveImpactTopLayerSettings(
        TopLayerType.GrassClosedSod
    )
    top_layer_closed_sod.stance_time_line_a = 1
    top_layer_closed_sod.stance_time_line_b = -0.000009722
    top_layer_closed_sod.stance_time_line_c = 0.25
    top_layer_open_sod = GrassCoverWaveImpactTopLayerSettings(TopLayerType.GrassOpenSod)
    top_layer_open_sod.stance_time_line_a = 0.8
    top_layer_open_sod.stance_time_line_b = -0.00001944
    top_layer_open_sod.stance_time_line_c = 0.25

    settings = GrassWaveImpactCalculationSettings(
        [top_layer_closed_sod, top_layer_open_sod]
    )
    settings.loading_upper_limit = 0.0
    settings.loading_lower_limit = 0.5
    settings.wave_angle_impact_n = 0.6666666666666667
    settings.wave_angle_impact_q = 0.35
    settings.wave_angle_impact_r = 10.0
    settings.te_max = 3600000.0
    settings.te_min = 3.6
    return settings


def get_grass_wave_overtopping_calculation_settings() -> (
    GrassWaveOvertoppingCalculationSettings
):
    top_layer_closed_sod = GrasCoverCumulativeOverloadTopLayerSettings(
        TopLayerType.GrassClosedSod
    )
    top_layer_closed_sod.critical_cumulative_overload = 7000.0
    top_layer_closed_sod.critical_front_velocity = 6.6

    settings = GrassWaveOvertoppingCalculationSettings([top_layer_closed_sod])
    settings.acceleration_alpha_a_for_crest = 1.0
    settings.acceleration_alpha_a_for_inner_slope = 1.4
    settings.fixed_number_of_waves = 10000
    settings.front_velocity_c_wo = 1.45
    settings.average_number_of_waves_factor_ctm = 0.92
    return settings


# endregion

input = get_calculation_input()
dikernel = Dikernel(input)

print("Starting validation")
validation_result = dikernel.validate()
print("   Validation was: " + "succesfull" if validation_result else "unsuccessfull")
if not validation_result:
    quit()

print("Starting calculation")
run_result = dikernel.run()
print("   Run was: " + "succesfull" if run_result else "unsuccessfull")
if not run_result:
    quit()

output = dikernel.output
print("   number of output locations: " + str(len(output)))
print("   Number of failed locations: " + str(len([l for l in output if l.failed])))
stones = [o for o in output if o.calculation_method == CalculationMethod.NaturalStone]
print("   Number of natural stone output locations: " + str(len(stones)))
for stone in stones:
    print(
        "      X: "
        + str(stone.x_position)
        + ", Damage lvel = "
        + str(stone.damage_development[-1])
    )

plot_hydrodynamic_conditions(input)

plot_damage_levels(output, input)

# for location in output:
#    plot_development_per_location(
#       location, TimeDependentOutputQuantity.DamageDevelopment, input
#    )

plot_development(output, TimeDependentOutputQuantity.DamageDevelopment, input)

plt.show()
