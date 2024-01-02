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
 
 This is a license template.
"""

from dikernelinput import DikernelInput, HydraulicConditions, DikeSchematization
from dikerneloutputlocations import (
    AsphaltOutputLocationSpecification,
    NordicStoneOutputLocationSpecification,
    GrassWaveImpactOutputLocationSpecification,
    GrassOvertoppingOutputLocationSpecification,
)
from dikernelcalculationsettings import (
    AsphaltCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    GrassWaveImpactCalculationSettings,
    NaturalStoneCalculationSettings,
    AsphaltTopLayerSettings,
    NaturalStoneTopLayerSettings,
    GrasCoverOvertoppingTopLayerSettings,
    GrassCoverWaveImpactTopLayerSettings,
)
from dikernelcreferences import *
from toplayertypes import TopLayerType


class DikernelInputParser:
    @staticmethod
    def parse_dikernel_input(input: DikernelInput):
        builder = CalculationInputBuilder(input.dike_orientation)
        DikernelInputParser.__add_dike_profile_to_builder(
            builder, input.dike_schematization
        )
        DikernelInputParser.__add_hydraulics_to_builder(builder, input.hydraulic_input)
        DikernelInputParser.__add_output_location_specifications_to_builder(
            builder, input
        )
        composed_input = builder.Build()
        return composed_input.Data

    @staticmethod
    def __add_dike_profile_to_builder(
        builder: CalculationInputBuilder, dike_schematization: DikeSchematization
    ):
        """This function adds the specified dike profile to the C# input builder.
        First all dike segments are added, then all characteristic points are translated to C#

        Args:
            builder (CalculationInputBuilder): The C# object used to build DiKErnel input
            dike_schematization (DikeSchematization): The python object containing the dike schematization
        """
        for i in range(len(dike_schematization.x_positions) - 1):
            x_start = dike_schematization.x_positions[i]
            z_start = dike_schematization.z_positions[i]
            x_end = dike_schematization.x_positions[i + 1]
            z_end = dike_schematization.z_positions[i + 1]
            roughness = dike_schematization.roughnesses[i]
            builder.AddDikeProfileSegment(x_start, z_start, x_end, z_end, roughness)

        if dike_schematization.outer_toe is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.outer_toe, CharacteristicPointType.OuterToe
            )

        if dike_schematization.crest_outer_berm is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.crest_outer_berm,
                CharacteristicPointType.CrestOuterBerm,
            )

        if dike_schematization.notch_outer_berm is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.notch_outer_berm,
                CharacteristicPointType.NotchOuterBerm,
            )

        if dike_schematization.outer_crest is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.outer_crest, CharacteristicPointType.OuterCrest
            )

        if dike_schematization.inner_crest is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.inner_crest, CharacteristicPointType.InnerCrest
            )

        if dike_schematization.inner_toe is not None:
            builder.AddDikeProfilePoint(
                dike_schematization.inner_toe, CharacteristicPointType.InnerToe
            )

    @staticmethod
    def __add_hydraulics_to_builder(
        builder: CalculationInputBuilder, hydraulic_conditions: HydraulicConditions
    ):
        for i in range(len(hydraulic_conditions.water_levels) - 1):
            builder.AddTimeStep(
                Double(hydraulic_conditions.time_steps[i]),
                Double(hydraulic_conditions.time_steps[i + 1]),
                Double(hydraulic_conditions.water_levels[i]),
                Double(hydraulic_conditions.wave_heights[i]),
                Double(hydraulic_conditions.wave_periods[i]),
                Double(hydraulic_conditions.wave_directions[i]),
            )

        return builder

    @staticmethod
    def __add_output_location_specifications_to_builder(
        builder: CalculationInputBuilder, input: DikernelInput
    ) -> CalculationInputBuilder:
        locations = input.output_locations
        settings = input.settings

        for location in locations:
            match location:
                case AsphaltOutputLocationSpecification():
                    builder.AddAsphaltWaveImpactLocation(
                        DikernelInputParser.__create_asphalt_wave_impact_construction_properties(
                            location,
                            next(
                                (
                                    ci
                                    for ci in settings
                                    if isinstance(ci, AsphaltCalculationSettings)
                                )
                            )
                            if settings is not None
                            else None,
                        )
                    )
                case NordicStoneOutputLocationSpecification():
                    builder.AddNaturalStoneLocation(
                        DikernelInputParser.__create_natural_stone_construction_properties(
                            location,
                            next(
                                (
                                    ci
                                    for ci in settings
                                    if isinstance(ci, NaturalStoneCalculationSettings)
                                )
                            )
                            if settings is not None
                            else None,
                        )
                    )

                case GrassWaveImpactOutputLocationSpecification():
                    builder.AddGrassWaveImpactLocation(
                        DikernelInputParser.__create_grass_wave_impact_construction_properties(
                            location,
                            next(
                                (
                                    ci
                                    for ci in settings
                                    if isinstance(
                                        ci, GrassWaveImpactCalculationSettings
                                    )
                                )
                            )
                            if settings is not None
                            else None,
                        )
                    )
                case GrassOvertoppingOutputLocationSpecification():
                    builder.AddGrassOvertoppingLocation(
                        DikernelInputParser.__create_grass_overtopping_construction_properties(
                            location,
                            next(
                                (
                                    ci
                                    for ci in settings
                                    if isinstance(
                                        ci, GrassWaveOvertoppingCalculationSettings
                                    )
                                )
                            )
                            if settings is not None
                            else None,
                        )
                    )

                # TODO: Add runup loations
                # GrassRevetmentWaveRunupLocationConstructionProperties constructionProperties =
                #         CreateGrassWaveRunupConstructionProperties(
                #             grassWaveRunupLocationData,
                #             GetCalculationDefinition<JsonInputGrassWaveRunupCalculationData>(
                #                 calculationDataItems, JsonInputCalculationType.GrassWaveRunup));

                #     if (constructionProperties is
                #         GrassRevetmentWaveRunupRayleighLocationConstructionProperties rayleighConstructionProperties)
                #     {
                #         builder.AddGrassWaveRunupRayleighLocation(rayleighConstructionProperties);
                #     }
        return builder

    @staticmethod
    def __create_asphalt_wave_impact_construction_properties(
        location: AsphaltOutputLocationSpecification,
        settings: AsphaltCalculationSettings,
    ):
        properties = AsphaltRevetmentWaveImpactLocationConstructionProperties(
            location.x_position,
            AsphaltRevetmentTopLayerType.HydraulicAsphaltConcrete,
            location.flexural_strent,
            location.soil_elasticity,
            location.top_layer_thickness,
            location.top_layer_elastic_modulus,
        )

        top_layer = DikernelInputParser.__get_first_asphalt_toplayer_of_type(
            settings, location.top_layer_type
        )

        properties.InitialDamage = location.initial_damage
        properties.ThicknessSubLayer = location.sub_layer_thickness
        properties.ElasticModulusSubLayer = location.sub_layer_elastic_modulus
        properties.FailureNumber = (
            settings.failure_number if settings is not None else None
        )
        properties.DensityOfWater = (
            settings.density_of_water if settings is not None else None
        )
        properties.AverageNumberOfWavesCtm = (
            settings.factor_ctm if settings is not None else None
        )
        properties.FatigueAlpha = (
            top_layer.fatigue_asphalt_alpha if top_layer is not None else None
        )
        properties.FatigueBeta = (
            top_layer.fatigue_asphalt_beta if top_layer is not None else None
        )
        properties.StiffnessRelationNu = (
            top_layer.stiffness_ratio_nu if top_layer is not None else None
        )
        properties.ImpactNumberC = (
            settings.impact_number_c if settings is not None else None
        )
        properties.WidthFactors = (
            DikernelInputParser.__convert_to_cList(settings.width_factors)
            if settings is not None
            else None
        )
        properties.DepthFactors = (
            DikernelInputParser.__convert_to_cList(settings.depth_factors)
            if settings is not None
            else None
        )
        properties.ImpactFactors = (
            DikernelInputParser.__convert_to_cList(settings.impact_factors)
            if settings is not None
            else None
        )

        return properties

    @staticmethod
    def __create_natural_stone_construction_properties(
        location: NordicStoneOutputLocationSpecification,
        settings: NaturalStoneCalculationSettings,
    ):
        properties = NaturalStoneRevetmentLocationConstructionProperties(
            location.x_position,
            NaturalStoneRevetmentTopLayerType.NordicStone,
            location.top_layer_thickness,
            location.relative_density,
        )

        top_layer = DikernelInputParser.__get_first_natural_stone_toplayer_of_type(
            settings, location.top_layer_type
        )

        properties.InitialDamage = location.initial_damage
        properties.FailureNumber = (
            settings.failure_number if settings is not None else None
        )
        properties.HydraulicLoadAp = (
            top_layer.stability_plunging_a if top_layer is not None else None
        )
        properties.HydraulicLoadBp = (
            top_layer.stability_plunging_b if top_layer is not None else None
        )
        properties.HydraulicLoadCp = (
            top_layer.stability_plunging_c if top_layer is not None else None
        )
        properties.HydraulicLoadNp = (
            top_layer.stability_plunging_n if top_layer is not None else None
        )
        properties.HydraulicLoadAs = (
            top_layer.stability_surging_a if top_layer is not None else None
        )
        properties.HydraulicLoadBs = (
            top_layer.stability_surging_b if top_layer is not None else None
        )
        properties.HydraulicLoadCs = (
            top_layer.stability_surging_c if top_layer is not None else None
        )
        properties.HydraulicLoadNs = (
            top_layer.stability_surging_n if top_layer is not None else None
        )
        properties.HydraulicLoadXib = top_layer.xib if top_layer is not None else None
        properties.SlopeUpperLevelAus = (
            settings.slope_upper_level if settings is not None else None
        )
        properties.SlopeLowerLevelAls = (
            settings.sLope_lower_level if settings is not None else None
        )
        properties.UpperLimitLoadingAul = (
            settings.upper_limit_loading_a if settings is not None else None
        )
        properties.UpperLimitLoadingBul = (
            settings.upper_limit_loading_b if settings is not None else None
        )
        properties.UpperLimitLoadingCul = (
            settings.upper_limit_loading_c if settings is not None else None
        )
        properties.LowerLimitLoadingAll = (
            settings.lower_limit_loading_a if settings is not None else None
        )
        properties.LowerLimitLoadingBll = (
            settings.lower_limit_loading_b if settings is not None else None
        )
        properties.LowerLimitLoadingCll = (
            settings.lower_limit_loading_c if settings is not None else None
        )
        properties.DistanceMaximumWaveElevationAsmax = (
            settings.distance_maximum_wave_elevation_a if settings is not None else None
        )
        properties.DistanceMaximumWaveElevationBsmax = (
            settings.distance_maximum_wave_elevation_b if settings is not None else None
        )
        properties.NormativeWidthOfWaveImpactAwi = (
            settings.normative_width_of_wave_impact_a if settings is not None else None
        )
        properties.NormativeWidthOfWaveImpactBwi = (
            settings.normative_width_of_wave_impact_b if settings is not None else None
        )
        properties.WaveAngleImpactBetamax = (
            settings.wave_angle_impact_beta_max if settings is not None else None
        )

        return properties

    @staticmethod
    def __create_grass_wave_impact_construction_properties(
        location: GrassWaveImpactOutputLocationSpecification,
        settings: GrassWaveImpactCalculationSettings,
    ):
        top_layer_type = (
            GrassRevetmentTopLayerType.ClosedSod
            if location.top_layer_type == TopLayerType.GrassClosedSod
            else GrassRevetmentTopLayerType.OpenSod
        )
        properties = GrassRevetmentWaveImpactLocationConstructionProperties(
            location.x_position, top_layer_type
        )

        topLayer = DikernelInputParser.__get_first_grass_wave_impact_toplayer_of_type(
            settings, location.top_layer_type
        )

        properties.InitialDamage = location.initial_damage
        properties.FailureNumber = (
            settings.failure_number if settings is not None else None
        )
        properties.TimeLineAgwi = (
            topLayer.stance_time_line_a if topLayer is not None else None
        )
        properties.TimeLineBgwi = (
            topLayer.stance_time_line_b if topLayer is not None else None
        )
        properties.TimeLineCgwi = (
            topLayer.stance_time_line_c if topLayer is not None else None
        )
        properties.MinimumWaveHeightTemax = (
            settings.te_max if settings is not None else None
        )
        properties.MaximumWaveHeightTemin = (
            settings.te_min if settings is not None else None
        )
        properties.WaveAngleImpactNwa = (
            settings.wave_angle_impact_n if settings is not None else None
        )
        properties.WaveAngleImpactQwa = (
            settings.wave_angle_impact_q if settings is not None else None
        )
        properties.WaveAngleImpactRwa = (
            settings.wave_angle_impact_r if settings is not None else None
        )
        properties.UpperLimitLoadingAul = (
            settings.loading_upper_limit if settings is not None else None
        )
        properties.LowerLimitLoadingAll = (
            settings.loading_lower_limit if settings is not None else None
        )

        return properties

    @staticmethod
    def __create_grass_overtopping_construction_properties(
        location: GrassOvertoppingOutputLocationSpecification,
        settings: GrassWaveOvertoppingCalculationSettings,
    ):
        topLayerType = None
        match location.top_layer_type:
            case TopLayerType.GrassClosedSod:
                topLayerType = GrassRevetmentTopLayerType.ClosedSod
            case TopLayerType.GrassOpenSod:
                topLayerType = GrassRevetmentTopLayerType.OpenSod

        properties = GrassRevetmentOvertoppingLocationConstructionProperties(
            location.x_position, topLayerType
        )

        topLayer = DikernelInputParser.__get_first_grass_overtopping_toplayer_of_type(
            settings, location.top_layer_type
        )

        properties.InitialDamage = location.initial_damage
        properties.IncreasedLoadTransitionAlphaM = (
            location.increased_load_transition_alpha_m
        )
        properties.ReducedStrengthTransitionAlphaS = (
            location.increased_load_transition_alpha_s
        )
        properties.FailureNumber = (
            settings.failure_number if settings is not None else None
        )
        properties.CriticalCumulativeOverload = (
            topLayer.critical_cumulative_overload if topLayer is not None else None
        )
        properties.CriticalFrontVelocity = (
            topLayer.critical_front_velocity if topLayer is not None else None
        )
        properties.DikeHeight = settings.DikeHeight if settings is not None else None
        properties.AccelerationAlphaAForCrest = (
            settings.acceleration_alpha_a_for_crest if settings is not None else None
        )
        properties.AccelerationAlphaAForInnerSlope = (
            settings.acceleration_alpha_a_for_inner_slope
            if settings is not None
            else None
        )
        properties.FixedNumberOfWaves = (
            settings.fixed_number_of_waves if settings is not None else None
        )
        properties.FrontVelocityCwo = (
            settings.front_velocity_c_wo if settings is not None else None
        )
        properties.AverageNumberOfWavesCtm = (
            settings.factor_ctm if settings is not None else None
        )

        return properties

    @staticmethod
    def __convert_to_cList(lst: list[list[float]]):
        cList = List[ValueTuple[Double, Double]]()
        if lst is not None:
            for l in lst:
                cList.Add(ValueTuple[Double, Double](l[0], l[1]))
        return cList

    @staticmethod
    def __get_first_asphalt_toplayer_of_type(
        settings: AsphaltCalculationSettings, top_layer_type: TopLayerType
    ) -> AsphaltTopLayerSettings:
        return (
            next(
                (
                    l
                    for l in settings.top_layers_settings
                    if l.top_layer_type == top_layer_type
                ),
                None,
            )
            if settings is not None
            else None
        )

    @staticmethod
    def __get_first_natural_stone_toplayer_of_type(
        settings: NaturalStoneCalculationSettings, top_layer_type: TopLayerType
    ) -> NaturalStoneTopLayerSettings:
        return (
            next(
                (
                    l
                    for l in settings.top_layers_settings
                    if l.top_layer_type == top_layer_type
                ),
                None,
            )
            if settings is not None
            else None
        )

    @staticmethod
    def __get_first_grass_wave_impact_toplayer_of_type(
        settings: GrassWaveImpactCalculationSettings, top_layer_type: TopLayerType
    ) -> GrassCoverWaveImpactTopLayerSettings:
        return (
            next(
                (
                    l
                    for l in settings.top_layers_settings
                    if l.top_layer_type == top_layer_type
                ),
                None,
            )
            if settings is not None
            else None
        )

    @staticmethod
    def __get_first_grass_overtopping_toplayer_of_type(
        settings: GrassWaveOvertoppingCalculationSettings, top_layer_type: TopLayerType
    ) -> GrasCoverOvertoppingTopLayerSettings:
        return (
            next(
                (
                    l
                    for l in settings.top_layers_settings
                    if l.top_layer_type == top_layer_type
                ),
                None,
            )
            if settings is not None
            else None
        )
