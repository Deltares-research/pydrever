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

from pydrever.data import (
    DikernelInput,
    HydrodynamicConditions,
    DikeSchematization,
    AsphaltLayerSpecification,
    OutputLocationSpecification,
    NordicStoneLayerSpecification,
    GrassWaveImpactLayerSpecification,
    GrassWaveRunupLayerSpecification,
    GrassOvertoppingLayerSpecification,
    CalculationSettings,
    AsphaltCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    GrassWaveImpactCalculationSettings,
    GrassWaveRunupCalculationSettings,
    NaturalStoneCalculationSettings,
    NaturalStoneTopLayerSettings,
    GrassCumulativeOverloadTopLayerSettings,
    GrassWaveImpactTopLayerSettings,
    TopLayerType,
)
from pydrever.calculation._dikernel import _inputservices as _input_service
from pydrever.calculation._dikernel import _messagehelper as _message_helper
from pydrever.calculation._dikernel._dikernelcreferences import *


def parse(input: DikernelInput) -> ICalculationInput:
    """
    Static method to parse a DikernelInput class to the equivalent C#-typed class.

    Args:
        input (DikernelInput): The specified calculation input.

    Returns:
        CalculationInput[C#]: The C#-typed input class produced by dikernels "CalculationInputBuilder".
    """
    builder = CalculationInputBuilder(input.dike_schematization.dike_orientation)
    __add_dike_profile_to_builder(builder, input.dike_schematization)
    __add_hydrodynamics_to_builder(builder, input.hydrodynamic_input)
    __add_output_location_specifications_to_builder(builder, input)
    # TODO: In future this way of working should maybe changed to the way Calculator.Calculate() works?
    composed_input = builder.Build()

    warnings, errors = _message_helper.parse_messages(composed_input)

    return composed_input.Data, warnings, errors


def __add_dike_profile_to_builder(builder: CalculationInputBuilder, dike_schematization: DikeSchematization) -> CalculationInputBuilder:
    """This function adds the specified dike profile to the C# input builder.
    First all dike segments are added, then all characteristic points are translated to C#

    Args:
        builder (CalculationInputBuilder): The C# object used to build DiKErnel input
        dike_schematization (DikeSchematization): The python object containing the dike schematization

    Returns:
        CalculationInputBuilder[C#]: The C#-typed builder with the added hydrodynamic conditions.
    """
    for i in range(len(dike_schematization.x_positions) - 1):
        x_start = dike_schematization.x_positions[i]
        z_start = dike_schematization.z_positions[i]
        x_end = dike_schematization.x_positions[i + 1]
        z_end = dike_schematization.z_positions[i + 1]
        roughness = dike_schematization.roughnesses[i]
        builder.AddDikeProfileSegment(x_start, z_start, x_end, z_end, roughness)

    if dike_schematization.x_outer_toe is not None:
        builder.AddDikeProfilePoint(dike_schematization.x_outer_toe, CharacteristicPointType.OuterToe)

    if dike_schematization.x_crest_outer_berm is not None:
        builder.AddDikeProfilePoint(
            dike_schematization.x_crest_outer_berm,
            CharacteristicPointType.CrestOuterBerm,
        )

    if dike_schematization.x_notch_outer_berm is not None:
        builder.AddDikeProfilePoint(
            dike_schematization.x_notch_outer_berm,
            CharacteristicPointType.NotchOuterBerm,
        )

    if dike_schematization.x_outer_crest is not None:
        builder.AddDikeProfilePoint(dike_schematization.x_outer_crest, CharacteristicPointType.OuterCrest)

    if dike_schematization.x_inner_crest is not None:
        builder.AddDikeProfilePoint(dike_schematization.x_inner_crest, CharacteristicPointType.InnerCrest)

    if dike_schematization.x_inner_toe is not None:
        builder.AddDikeProfilePoint(dike_schematization.x_inner_toe, CharacteristicPointType.InnerToe)


def __add_hydrodynamics_to_builder(
    builder: CalculationInputBuilder,
    hydrodynamic_conditions: HydrodynamicConditions,
) -> CalculationInputBuilder:
    """
    This method adds the specified hydrodynamic input to the C# builder.

    Args:
        builder (CalculationInputBuilder): The C# object used to build DiKErnel input.
        hydrodynamic_conditions (HydrodynamicConditions): The specified hydrodynamic conditions.

    Returns:
        CalculationInputBuilder[C#]: The C#-typed builder with the added hydrodynamic conditions.
    """
    for i in range(len(hydrodynamic_conditions.water_levels)):
        builder.AddTimeStep(
            Double(hydrodynamic_conditions.time_steps[i]),
            Double(hydrodynamic_conditions.time_steps[i + 1]),
            Double(hydrodynamic_conditions.water_levels[i]),
            Double(hydrodynamic_conditions.wave_heights[i]),
            Double(hydrodynamic_conditions.wave_periods[i]),
            Double(hydrodynamic_conditions.wave_directions[i]),
        )

    return builder


def __add_output_location_specifications_to_builder(builder: CalculationInputBuilder, input: DikernelInput) -> CalculationInputBuilder:
    locations = _input_service.get_output_locations_from_input(input)
    settings = input.settings

    for location in locations:
        match location.top_layer_specification:
            case AsphaltLayerSpecification():
                builder.AddAsphaltWaveImpactLocation(
                    __create_asphalt_wave_impact_construction_properties(
                        location.x_position,
                        location.top_layer_specification,
                        __get_asphalt_calculation_settings(location, settings),
                    ),
                )
            case NordicStoneLayerSpecification():
                builder.AddNaturalStoneWaveImpactLocation(
                    __create_natural_stone_construction_properties(
                        location.x_position,
                        location.top_layer_specification,
                        __get_natural_stone_calculation_settings(location, settings),
                    )
                )

            case GrassWaveImpactLayerSpecification():
                builder.AddGrassWaveImpactLocation(
                    __create_grass_wave_impact_construction_properties(
                        location.x_position,
                        location.top_layer_specification,
                        __get_grass_wave_impact_calculation_settings(location, settings),
                    )
                )
            case GrassOvertoppingLayerSpecification():
                # TODO:Add possibility to calculate with analytical solution
                # AddGrassWaveOvertoppingRayleighAnalyticalLocation
                builder.AddGrassWaveOvertoppingRayleighDiscreteLocation(
                    __create_grass_overtopping_construction_properties(
                        location.x_position,
                        location.top_layer_specification,
                        __get_grass_wave_overtopping_calculation_settings(location, settings),
                    )
                )
            case GrassWaveRunupLayerSpecification():
                # TODO: Add AddGrassWaveRunupBattjesGroenendijkAnalyticalLocation
                builder.AddGrassWaveRunupRayleighDiscreteLocation(
                    __create_grass_wave_runup_construction_properties(
                        location.x_position,
                        location.top_layer_specification,
                        __get_grass_wave_runup_calculation_settings(location, settings),
                    )
                )
    return builder


def __create_asphalt_wave_impact_construction_properties(
    x_position: float,
    layer: AsphaltLayerSpecification,
    settings: AsphaltCalculationSettings | None,
):
    properties = AsphaltWaveImpactLocationConstructionProperties(
        x_position,
        AsphaltWaveImpactTopLayerType.HydraulicAsphaltConcrete,
        layer.flexural_strength,
        layer.soil_elasticity,
        layer.upper_layer_thickness,
        layer.upper_layer_elasticity_modulus,
    )

    properties.InitialDamage = layer.initial_damage
    properties.FailureNumber = settings.failure_number if settings is not None else None
    properties.DensityOfWater = settings.density_of_water if settings is not None else None
    properties.ThicknessSubLayer = layer.sub_layer_thickness
    properties.ElasticModulusSubLayer = layer.sub_layer_elastic_modulus
    properties.AverageNumberOfWavesCtm = settings.factor_ctm if settings is not None else None
    properties.FatigueAlpha = layer.fatigue_asphalt_alpha
    properties.FatigueBeta = layer.fatigue_asphalt_beta
    properties.ImpactNumberC = settings.impact_number_c if settings is not None else None
    properties.StiffnessRelationNu = layer.stiffness_ratio_nu
    if settings is not None:
        properties.WidthFactors = __convert_to_cList(settings.width_factors) if settings.width_factors is not None else None
        properties.DepthFactors = __convert_to_cList(settings.depth_factors) if settings.depth_factors is not None else None
        properties.ImpactFactors = __convert_to_cList(settings.impact_factors) if settings.impact_factors is not None else None
    else:
        properties.WidthFactors = None
        properties.DepthFactors = None
        properties.ImpactFactors = None

    return properties


def __create_natural_stone_construction_properties(
    x_position: float,
    layer: NordicStoneLayerSpecification,
    settings: NaturalStoneCalculationSettings | None,
):
    properties = NaturalStoneWaveImpactLocationConstructionProperties(
        x_position,
        NaturalStoneWaveImpactTopLayerType.NordicStone,
        layer.top_layer_thickness,
        layer.relative_density,
    )

    top_layer = __get_first_natural_stone_toplayer_of_type(settings, layer.top_layer_type)

    properties.InitialDamage = layer.initial_damage
    properties.FailureNumber = settings.failure_number if settings is not None else None
    properties.HydraulicLoadAp = top_layer.stability_plunging_a if top_layer is not None else None
    properties.HydraulicLoadBp = top_layer.stability_plunging_b if top_layer is not None else None
    properties.HydraulicLoadCp = top_layer.stability_plunging_c if top_layer is not None else None
    properties.HydraulicLoadNp = top_layer.stability_plunging_n if top_layer is not None else None
    properties.HydraulicLoadAs = top_layer.stability_surging_a if top_layer is not None else None
    properties.HydraulicLoadBs = top_layer.stability_surging_b if top_layer is not None else None
    properties.HydraulicLoadCs = top_layer.stability_surging_c if top_layer is not None else None
    properties.HydraulicLoadNs = top_layer.stability_surging_n if top_layer is not None else None
    properties.HydraulicLoadXib = top_layer.xib if top_layer is not None else None
    properties.SlopeUpperLevelAus = settings.slope_upper_level if settings is not None else None
    properties.SlopeLowerLevelAls = settings.sLope_lower_level if settings is not None else None
    properties.UpperLimitLoadingAul = settings.upper_limit_loading_a if settings is not None else None
    properties.UpperLimitLoadingBul = settings.upper_limit_loading_b if settings is not None else None
    properties.UpperLimitLoadingCul = settings.upper_limit_loading_c if settings is not None else None
    properties.LowerLimitLoadingAll = settings.lower_limit_loading_a if settings is not None else None
    properties.LowerLimitLoadingBll = settings.lower_limit_loading_b if settings is not None else None
    properties.LowerLimitLoadingCll = settings.lower_limit_loading_c if settings is not None else None
    properties.DistanceMaximumWaveElevationAsmax = settings.distance_maximum_wave_elevation_a if settings is not None else None
    properties.DistanceMaximumWaveElevationBsmax = settings.distance_maximum_wave_elevation_b if settings is not None else None
    properties.NormativeWidthOfWaveImpactAwi = settings.normative_width_of_wave_impact_a if settings is not None else None
    properties.NormativeWidthOfWaveImpactBwi = settings.normative_width_of_wave_impact_b if settings is not None else None
    properties.WaveAngleImpactBetamax = settings.wave_angle_impact_beta_max if settings is not None else None

    return properties


def __create_grass_wave_impact_construction_properties(
    x_position: float,
    layer: GrassWaveImpactLayerSpecification,
    settings: GrassWaveImpactCalculationSettings | None,
):
    top_layer_type = GrassTopLayerType.ClosedSod if layer.top_layer_type == TopLayerType.GrassClosedSod else GrassTopLayerType.OpenSod
    properties = GrassWaveImpactLocationConstructionProperties(x_position, top_layer_type)

    topLayer = __get_first_grass_wave_impact_toplayer_of_type(settings, layer.top_layer_type)

    properties.InitialDamage = layer.initial_damage
    properties.FailureNumber = settings.failure_number if settings is not None else None
    properties.TimeLineAgwi = topLayer.stance_time_line_a if topLayer is not None else None
    properties.TimeLineBgwi = topLayer.stance_time_line_b if topLayer is not None else None
    properties.TimeLineCgwi = topLayer.stance_time_line_c if topLayer is not None else None
    properties.MinimumWaveHeightTemax = settings.te_max if settings is not None else None
    properties.MaximumWaveHeightTemin = settings.te_min if settings is not None else None
    properties.WaveAngleImpactNwa = settings.wave_angle_impact_n if settings is not None else None
    properties.WaveAngleImpactQwa = settings.wave_angle_impact_q if settings is not None else None
    properties.WaveAngleImpactRwa = settings.wave_angle_impact_r if settings is not None else None
    properties.UpperLimitLoadingAul = settings.loading_upper_limit if settings is not None else None
    properties.LowerLimitLoadingAll = settings.loading_lower_limit if settings is not None else None

    return properties


def __create_grass_overtopping_construction_properties(
    x_position: float,
    layer: GrassOvertoppingLayerSpecification,
    settings: GrassWaveOvertoppingCalculationSettings | None,
):
    topLayerType = None
    match layer.top_layer_type:
        case TopLayerType.GrassClosedSod:
            topLayerType = GrassTopLayerType.ClosedSod
        case TopLayerType.GrassOpenSod:
            topLayerType = GrassTopLayerType.OpenSod

    properties = GrassWaveOvertoppingRayleighDiscreteLocationConstructionProperties(x_position, topLayerType)

    topLayer = __get_first_grass_cumulative_overload_toplayer_of_type(settings, layer.top_layer_type)

    properties.InitialDamage = layer.initial_damage
    properties.FailureNumber = settings.failure_number if settings is not None else None
    properties.CriticalCumulativeOverload = topLayer.critical_cumulative_overload if topLayer is not None else None
    properties.CriticalFrontVelocity = topLayer.critical_front_velocity if topLayer is not None else None
    properties.IncreasedLoadTransitionAlphaM = layer.increased_load_transition_alpha_m
    properties.ReducedStrengthTransitionAlphaS = layer.increased_load_transition_alpha_s
    properties.AverageNumberOfWavesCtm = settings.average_number_of_waves_factor_ctm if settings is not None else None

    # TODO: Only if calculating discrete, not analytical
    properties.FixedNumberOfWaves = settings.fixed_number_of_waves if settings is not None else None

    properties.FrontVelocityCwo = settings.front_velocity_c_wo if settings is not None else None
    properties.AccelerationAlphaAForCrest = settings.acceleration_alpha_a_for_crest if settings is not None else None
    properties.AccelerationAlphaAForInnerSlope = settings.acceleration_alpha_a_for_inner_slope if settings is not None else None
    properties.DikeHeight = settings.dike_height if settings is not None else None

    return properties


def __create_grass_wave_runup_construction_properties(
    x_position: float,
    layer: GrassWaveRunupLayerSpecification,
    settings: GrassWaveRunupCalculationSettings | None,
) -> GrassWaveRunupRayleighDiscreteLocationConstructionProperties:
    topLayerType = None
    match layer.top_layer_type:
        case TopLayerType.GrassClosedSod:
            topLayerType = GrassTopLayerType.ClosedSod
        case TopLayerType.GrassOpenSod:
            topLayerType = GrassTopLayerType.OpenSod

    properties = GrassWaveRunupRayleighDiscreteLocationConstructionProperties(x_position, topLayerType)

    top_layer = __get_first_grass_cumulative_overload_toplayer_of_type(settings, layer.top_layer_type)

    # TODO: These properties have changed in C# I think.
    properties.FixedNumberOfWaves = settings.fixed_number_of_waves if settings is not None else None
    properties.FrontVelocityCu = settings.front_velocity_cu if settings is not None else None
    properties.InitialDamage = layer.initial_damage
    properties.FailureNumber = settings.failure_number if settings is not None else None
    properties.IncreasedLoadTransitionAlphaM = layer.increased_load_transition_alpha_m
    properties.ReducedStrengthTransitionAlphaS = layer.increased_load_transition_alpha_s
    # properties.RepresentativeWaveRunup2PGammab = layer.reduced_strength_transition_2p_gamma_b
    # properties.RepresentativeWaveRunup2PGammaf = layer.reduced_strength_transition_2p_gamma_f
    properties.AverageNumberOfWavesCtm = settings.average_number_of_waves_factor_ctm if settings is not None else None
    # properties.RepresentativeWaveRunup2PAru = (settings.representative_wave_runup_2p_aru) if settings is not None else None
    # properties.RepresentativeWaveRunup2PBru = (settings.representative_wave_runup_2p_bru) if settings is not None else None
    # properties.RepresentativeWaveRunup2PCru = (settings.representative_wave_runup_2p_cru) if settings is not None else None
    # properties.WaveAngleImpactAbeta = settings.wave_angle_impact_a_beta if settings is not None else None
    # properties.WaveAngleImpactBetamax = settings.wave_angle_impact_beta_max if settings is not None else None
    properties.CriticalCumulativeOverload = top_layer.critical_cumulative_overload if top_layer is not None else None
    properties.CriticalFrontVelocity = top_layer.critical_front_velocity if top_layer is not None else None

    return properties


def __convert_to_cList(lst: list[list[float]]):
    """
    Private method to convert a list of floats (2d) to a C# equivalent.

    Args:
        lst (list[list[float]]): The python typed list

    Returns:
        List[Double] [C#]: The C#-typed equivalent of the specified list.
    """
    cList = List[ValueTuple[Double, Double]]()
    if lst is not None:
        for l in lst:
            cList.Add(ValueTuple[Double, Double](l[0], l[1]))
    return cList


def __get_first_natural_stone_toplayer_of_type(
    settings: CalculationSettings | None, top_layer_type: TopLayerType
) -> NaturalStoneTopLayerSettings | None:
    if settings is not None:
        return (
            next(
                (
                    tls
                    for tls in settings.top_layers_settings
                    if isinstance(tls, NaturalStoneTopLayerSettings) and tls.top_layer_type == top_layer_type
                ),
                None,
            )
            if settings is not None and settings.top_layers_settings is not None
            else None
        )
    else:
        return None


def __get_first_grass_wave_impact_toplayer_of_type(
    settings: CalculationSettings | None, top_layer_type: TopLayerType
) -> GrassWaveImpactTopLayerSettings | None:
    return (
        next(
            (
                tls
                for tls in settings.top_layers_settings
                if isinstance(tls, GrassWaveImpactTopLayerSettings) and tls.top_layer_type == top_layer_type
            ),
            None,
        )
        if settings is not None and settings.top_layers_settings is not None
        else None
    )


def __get_first_grass_cumulative_overload_toplayer_of_type(
    settings: CalculationSettings | None, top_layer_type: TopLayerType
) -> GrassCumulativeOverloadTopLayerSettings | None:
    return (
        next(
            (
                tls
                for tls in settings.top_layers_settings
                if isinstance(tls, GrassCumulativeOverloadTopLayerSettings) and tls.top_layer_type == top_layer_type
            ),
            None,
        )
        if settings is not None and settings.top_layers_settings is not None
        else None
    )


def __get_natural_stone_calculation_settings(
    location: OutputLocationSpecification, settings: list[CalculationSettings] | None
) -> NaturalStoneCalculationSettings | None:
    return (
        location.calculation_settings
        if isinstance(
            location.calculation_settings,
            NaturalStoneCalculationSettings,
        )
        else (
            next(
                (ci for ci in settings if isinstance(ci, NaturalStoneCalculationSettings)),
                None,
            )
            if settings is not None
            else None
        )
    )


def __get_asphalt_calculation_settings(
    location: OutputLocationSpecification, settings: list[CalculationSettings] | None
) -> AsphaltCalculationSettings | None:
    return (
        location.calculation_settings
        if isinstance(
            location.calculation_settings,
            AsphaltCalculationSettings,
        )
        else (
            next(
                (ci for ci in settings if isinstance(ci, AsphaltCalculationSettings)),
                None,
            )
            if settings is not None
            else None
        )
    )


def __get_grass_wave_impact_calculation_settings(
    location: OutputLocationSpecification, settings: list[CalculationSettings] | None
) -> GrassWaveImpactCalculationSettings | None:
    return (
        location.calculation_settings
        if isinstance(
            location.calculation_settings,
            GrassWaveImpactCalculationSettings,
        )
        else (
            next(
                (ci for ci in settings if isinstance(ci, GrassWaveImpactCalculationSettings)),
                None,
            )
            if settings is not None
            else None
        )
    )


def __get_grass_wave_overtopping_calculation_settings(
    location: OutputLocationSpecification, settings: list[CalculationSettings] | None
) -> GrassWaveOvertoppingCalculationSettings | None:
    return (
        location.calculation_settings
        if isinstance(
            location.calculation_settings,
            GrassWaveOvertoppingCalculationSettings,
        )
        else (
            next(
                (ci for ci in settings if isinstance(ci, GrassWaveOvertoppingCalculationSettings)),
                None,
            )
            if settings is not None
            else None
        )
    )


def __get_grass_wave_runup_calculation_settings(
    location: OutputLocationSpecification, settings: list[CalculationSettings] | None
) -> GrassWaveRunupCalculationSettings | None:
    return (
        location.calculation_settings
        if isinstance(
            location.calculation_settings,
            GrassWaveRunupCalculationSettings,
        )
        else (
            next(
                (ci for ci in settings if isinstance(ci, GrassWaveRunupCalculationSettings)),
                None,
            )
            if settings is not None
            else None
        )
    )
