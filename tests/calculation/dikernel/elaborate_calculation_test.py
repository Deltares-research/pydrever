from pydrever.data import DikeSchematization
import numpy
from pydrever.data import HydrodynamicConditions
from pydrever.data import (
    RevetmentZoneSpecification,
    HorizontalRevetmentZoneDefinition,
    TopLayerType,
    GrassWaveImpactLayerSpecification,
    GrassWaveRunupLayerSpecification,
    GrassOvertoppingLayerSpecification,
    AsphaltLayerSpecification,
    NordicStoneLayerSpecification,
)
from pydrever.data import (
    AsphaltCalculationSettings,
    NaturalStoneCalculationSettings,
    GrassWaveImpactCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    NaturalStoneTopLayerSettings,
    GrassCumulativeOverloadTopLayerSettings,
    GrassWaveImpactTopLayerSettings,
)
from pydrever.data import DikernelInput

from pydrever.calculation import Dikernel
import pytest


@pytest.mark.skip(reason="Only run this test locally")
def test_elaborate_caculation():
    x_positions = [0.0, 25.0, 35.0, 41.0, 45, 50, 60, 70]
    z_positions = [-3, 0.0, 1.5, 1.7, 3.0, 3.1, 0, -1]
    roughnesses = [1, 1, 0.75, 0.5, 0.8, 0.8, 0.8]
    schematization = DikeSchematization(
        dike_orientation=0.0,
        x_positions=x_positions,
        z_positions=z_positions,
        roughnesses=roughnesses,
        x_outer_toe=25.0,
        x_outer_crest=45.0,
    )
    schematization.x_crest_outer_berm = 35.0
    schematization.x_notch_outer_berm = 41.0
    schematization.x_inner_crest = 50.0
    schematization.x_inner_toe = 60.0

    time_steps = numpy.linspace(
        0.0, 126000.0, int(126000.0 / 1000.0), dtype=float, endpoint=True
    )

    phase_water_levels = numpy.pi / 64.0
    amplitude_water_levels = 1.1
    minimum_water_level = 0.5
    water_levels = (
        amplitude_water_levels
        * (1 - numpy.cos(time_steps[1:] / 1000.0 * phase_water_levels))
        + minimum_water_level
    )

    phase_wave_heights = numpy.pi / 64.0
    ampltude_waves = 0.5
    minimum_wave_height = 0.8
    wave_heights = (
        ampltude_waves * (1 - numpy.cos(time_steps[1:] / 1000.0 * phase_wave_heights))
        + minimum_wave_height
    )

    wave_periods = 7.0 + time_steps[1:] / 1000.0 * 0.06

    wave_directions = -20 + time_steps[1:] / 1000.0 * 0.5
    wave_directions = [
        d + 360 if d < 0 else d - 360 if d > 360 else d for d in wave_directions
    ]
    hydrodynamic_conditions = HydrodynamicConditions(
        time_steps=time_steps,
        water_levels=water_levels,
        wave_heights=wave_heights,
        wave_periods=wave_periods,
        wave_directions=wave_directions,
    )

    asphalt_layer = AsphaltLayerSpecification(
        flexural_strength=0.9,
        soil_elasticity=64.0,
        upper_layer_thickness=0.146,
        upper_layer_elasticity_modulus=5712.0,
    )
    # TODO: Move after implementing BaseModel
    asphalt_layer.stiffness_ratio_nu = 0.35
    asphalt_layer.fatigue_asphalt_alpha = 0.5
    asphalt_layer.fatigue_asphalt_beta = 5.4

    nordic_stone_layer = NordicStoneLayerSpecification(
        top_layer_thickness=0.28, relative_density=2.45
    )
    grass_wave_impact_layer = GrassWaveImpactLayerSpecification(
        top_layer_type=TopLayerType.GrassClosedSod
    )
    grass_wave_runup_layer = GrassWaveRunupLayerSpecification(
        outer_slope=0.3, top_layer_type=TopLayerType.GrassClosedSod
    )
    grass_overtopping_layer_closed = GrassOvertoppingLayerSpecification(
        top_layer_type=TopLayerType.GrassClosedSod
    )
    grass_overtopping_layer_open = GrassOvertoppingLayerSpecification(
        top_layer_type=TopLayerType.GrassOpenSod
    )

    revetment_zones = [
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(25.01, 34.9, 0.5), nordic_stone_layer
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(35.1, 40.9, 0.5), asphalt_layer
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(41.1, 44.9, 0.5), grass_wave_impact_layer
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(41.1, 44.9, 0.5), grass_wave_runup_layer
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(45.0, 49.99, 0.5),
            grass_overtopping_layer_closed,
        ),
        RevetmentZoneSpecification(
            HorizontalRevetmentZoneDefinition(52.0, 58, 2.0),
            grass_overtopping_layer_open,
        ),
    ]

    calculation_settings = [
        get_asphalt_calculation_settings(),
        get_natural_stone_calculation_settings(),
        get_grass_wave_impact_calculation_settings(),
        get_grass_wave_overtopping_calculation_settings(),
    ]

    input = DikernelInput(hydrodynamic_conditions, schematization)
    input.output_revetment_zones = revetment_zones
    input.settings = calculation_settings

    dikernel = Dikernel(input)

    run_result = dikernel.run()

    assert run_result


def get_asphalt_calculation_settings() -> AsphaltCalculationSettings:
    settings = AsphaltCalculationSettings(
        density_of_water=1000.0,
        factor_ctm=1.0,
        impact_number_c=1.0,
        width_factors=[
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
        ],
        depth_factors=[
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
        ],
        impact_factors=[
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
        ],
    )

    return settings


def get_natural_stone_calculation_settings() -> NaturalStoneCalculationSettings:
    topLayer = NaturalStoneTopLayerSettings(
        top_layer_type=TopLayerType.NordicStone,
        stability_plunging_a=4.0,
        stability_plunging_b=0.0,
        stability_plunging_c=0.0,
        stability_plunging_n=-0.9,
        stability_surging_a=0.8,
        stability_surging_b=0.0,
        stability_surging_c=0.0,
        stability_surging_n=0.6,
        xib=2.9,
    )

    settings = NaturalStoneCalculationSettings(
        top_layers_settings=[topLayer],
        distance_maximum_wave_elevation_a=0.42,
        distance_maximum_wave_elevation_b=0.9,
        slope_upper_level=0.05,
        sLope_lower_level=1.5,
        normative_width_of_wave_impact_a=0.96,
        normative_width_of_wave_impact_b=0.11,
        upper_limit_loading_a=0.1,
        upper_limit_loading_b=0.6,
        upper_limit_loading_c=4.0,
        lower_limit_loading_a=0.1,
        lower_limit_loading_b=0.2,
        lower_limit_loading_c=4.0,
        wave_angle_impact_beta_max=78.0,
    )
    return settings


def get_grass_wave_impact_calculation_settings() -> GrassWaveImpactCalculationSettings:
    top_layer_closed_sod = GrassWaveImpactTopLayerSettings(
        top_layer_type=TopLayerType.GrassClosedSod,
        stance_time_line_a=1,
        stance_time_line_b=-0.000009722,
        stance_time_line_c=0.25,
    )
    top_layer_open_sod = GrassWaveImpactTopLayerSettings(
        top_layer_type=TopLayerType.GrassOpenSod,
        stance_time_line_a=0.8,
        stance_time_line_b=-0.00001944,
        stance_time_line_c=0.25,
    )

    settings = GrassWaveImpactCalculationSettings(
        top_layers_settings=[top_layer_closed_sod, top_layer_open_sod],
        loading_upper_limit=0.0,
        loading_lower_limit=0.5,
        wave_angle_impact_n=0.6666666666666667,
        wave_angle_impact_q=0.35,
        wave_angle_impact_r=10.0,
        te_max=3600000.0,
        te_min=3.6,
    )
    return settings


def get_grass_wave_overtopping_calculation_settings() -> (
    GrassWaveOvertoppingCalculationSettings
):
    top_layer_closed_sod = GrassCumulativeOverloadTopLayerSettings(
        top_layer_type=TopLayerType.GrassClosedSod,
        critical_cumulative_overload=7000.0,
        critical_front_velocity=6.6,
    )

    settings = GrassWaveOvertoppingCalculationSettings(
        top_layers_settings=[top_layer_closed_sod],
        acceleration_alpha_a_for_crest=1.0,
        acceleration_alpha_a_for_inner_slope=1.4,
        fixed_number_of_waves=10000,
        front_velocity_c_wo=1.45,
        average_number_of_waves_factor_ctm=0.92,
    )
    return settings
