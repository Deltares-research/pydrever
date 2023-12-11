from dikernelinput import DikernelInput, HydraulicInput, DikeSchematization
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
)
from dikernelcreferences import *
from toplayertypes import TopLayerType


class DikernelInputParser:
    @staticmethod
    def parsedikernelinput(dikernelInput: DikernelInput):
        builder = CalculationInputBuilder(dikernelInput.DikeOrientation)
        DikernelInputParser.__addDikeProfileToBuilder(builder, dikernelInput.DikeSchematization)
        DikernelInputParser.__addHydraulicsToBuilder(builder, dikernelInput.HydraulicInput)
        DikernelInputParser.__addOutputLocationSpecificationsToBuilder(builder, dikernelInput)
        composedInput = builder.Build()
        return composedInput.Data

    @staticmethod
    def __addDikeProfileToBuilder(builder: CalculationInputBuilder, dikeSchematization: DikeSchematization):
        """This function adds the specified dike profile to the C# input builder.
        First all dike segments are added, then all characteristic points are translated to C#

        Args:
            builder (CalculationInputBuilder): The C# object used to build DiKErnel input
            dikernelInput (DikernelInput): The python object containing all calculation input
        """
        for i in range(len(dikeSchematization.XPositions) - 1):
            xStart = dikeSchematization.XPositions[i]
            zStart = dikeSchematization.ZPositions[i]
            xEnd = dikeSchematization.XPositions[i + 1]
            zEnd = dikeSchematization.ZPositions[i + 1]
            roughness = dikeSchematization.Roughnesses[i]
            builder.AddDikeProfileSegment(xStart, zStart, xEnd, zEnd, roughness)

        if dikeSchematization.OuterToe is not None:
            builder.AddDikeProfilePoint(dikeSchematization.OuterToe, CharacteristicPointType.OuterToe)

        if dikeSchematization.CrestOuterBerm is not None:
            builder.AddDikeProfilePoint(dikeSchematization.CrestOuterBerm, CharacteristicPointType.CrestOuterBerm)

        if dikeSchematization.NotchOuterBerm is not None:
            builder.AddDikeProfilePoint(dikeSchematization.NotchOuterBerm, CharacteristicPointType.NotchOuterBerm)

        if dikeSchematization.OuterCrest is not None:
            builder.AddDikeProfilePoint(dikeSchematization.OuterCrest, CharacteristicPointType.OuterCrest)

        if dikeSchematization.InnerCrest is not None:
            builder.AddDikeProfilePoint(dikeSchematization.InnerCrest, CharacteristicPointType.InnerCrest)

        if dikeSchematization.InnerToe is not None:
            builder.AddDikeProfilePoint(dikeSchematization.InnerToe, CharacteristicPointType.InnerToe)

    @staticmethod
    def __addHydraulicsToBuilder(builder: CalculationInputBuilder, hydraulicInput: HydraulicInput):
        for i in range(len(hydraulicInput.WaterLevels) - 1):
            builder.AddTimeStep(
                Double(hydraulicInput.TimeSteps[i]),
                Double(hydraulicInput.TimeSteps[i + 1]),
                Double(hydraulicInput.WaterLevels[i]),
                Double(hydraulicInput.WaveHeights[i]),
                Double(hydraulicInput.WavePeriods[i]),
                Double(hydraulicInput.WaveDirections[i]),
            )

        return builder

    @staticmethod
    def __addOutputLocationSpecificationsToBuilder(
        builder: CalculationInputBuilder, dikernelInput: DikernelInput
    ) -> CalculationInputBuilder:
        locationDataItems = dikernelInput.OutputLocations
        calculationSettings = dikernelInput.Settings

        for locationData in locationDataItems:
            match locationData:
                case AsphaltOutputLocationSpecification():
                    builder.AddAsphaltWaveImpactLocation(
                        DikernelInputParser.__createAsphaltWaveImpactConstructionProperties(
                            locationData,
                            next((ci for ci in calculationSettings if isinstance(ci, AsphaltCalculationSettings)))
                            if calculationSettings is not None
                            else None,
                        )
                    )
                case NordicStoneOutputLocationSpecification():
                    builder.AddNaturalStoneLocation(
                        DikernelInputParser.__createNaturalStoneConstructionProperties(
                            locationData,
                            next((ci for ci in calculationSettings if isinstance(ci, NaturalStoneCalculationSettings)))
                            if calculationSettings is not None
                            else None,
                        )
                    )

                case GrassWaveImpactOutputLocationSpecification():
                    builder.AddGrassWaveImpactLocation(
                        DikernelInputParser.__createGrassWaveImpactConstructionProperties(
                            locationData,
                            next(
                                (
                                    ci
                                    for ci in calculationSettings
                                    if isinstance(ci, GrassWaveImpactCalculationSettings)
                                )
                            )
                            if calculationSettings is not None
                            else None,
                        )
                    )
                case GrassOvertoppingOutputLocationSpecification():
                    builder.AddGrassOvertoppingLocation(
                        DikernelInputParser.__createGrassOvertoppingConstructionProperties(
                            locationData,
                            next(
                                (
                                    ci
                                    for ci in calculationSettings
                                    if isinstance(ci, GrassWaveOvertoppingCalculationSettings)
                                )
                            )
                            if calculationSettings is not None
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
    def __createAsphaltWaveImpactConstructionProperties(
        locationData: AsphaltOutputLocationSpecification, settings: AsphaltCalculationSettings
    ):
        properties = AsphaltRevetmentWaveImpactLocationConstructionProperties(
            locationData.XPosition,
            AsphaltRevetmentTopLayerType.HydraulicAsphaltConcrete,
            locationData.FlexuralStrent,
            locationData.SoilElasticity,
            locationData.TopLayerThickness,
            locationData.TopLayerElasticModulus,
        )

        topLayer = (
            next((l for l in settings.TopLayersSettings if l.TopLayerType == locationData.TopLayerType), None)
            if settings is not None
            else None
        )

        properties.InitialDamage = locationData.InitialDamage
        properties.ThicknessSubLayer = locationData.SubLayerThickness
        properties.ElasticModulusSubLayer = locationData.SubLayerElasticModulus
        properties.FailureNumber = settings.FailureNumber if settings is not None else None
        properties.DensityOfWater = settings.DensityOfWater if settings is not None else None
        properties.AverageNumberOfWavesCtm = settings.FactorCtm if settings is not None else None
        properties.FatigueAlpha = topLayer.FatigueAsphaltAlpha if topLayer is not None else None
        properties.FatigueBeta = topLayer.FatigueAsphaltBeta if topLayer is not None else None
        properties.StiffnessRelationNu = topLayer.StiffnessRatioNu if topLayer is not None else None
        properties.ImpactNumberC = settings.ImpactNumberC if settings is not None else None
        properties.WidthFactors = (
            DikernelInputParser.__convertToCList(settings.WidthFactors) if settings is not None else None
        )
        properties.DepthFactors = (
            DikernelInputParser.__convertToCList(settings.DepthFactors) if settings is not None else None
        )
        properties.ImpactFactors = (
            DikernelInputParser.__convertToCList(settings.ImpactFactors) if settings is not None else None
        )

        return properties

    @staticmethod
    def __createNaturalStoneConstructionProperties(
        locationData: NordicStoneOutputLocationSpecification, settings: NaturalStoneCalculationSettings
    ):
        properties = NaturalStoneRevetmentLocationConstructionProperties(
            locationData.XPosition,
            NaturalStoneRevetmentTopLayerType.NordicStone,
            locationData.TopLayerThickness,
            locationData.RelativeDensity,
        )

        topLayer = (
            next((l for l in settings.TopLayersSettings if l.TopLayerType == locationData.TopLayerType), None)
            if settings is not None
            else None
        )

        properties.InitialDamage = locationData.InitialDamage
        properties.FailureNumber = settings.FailureNumber if settings is not None else None
        properties.HydraulicLoadAp = topLayer.StabilityPlungingA if topLayer is not None else None
        properties.HydraulicLoadBp = topLayer.StabilityPlungingB if topLayer is not None else None
        properties.HydraulicLoadCp = topLayer.StabilityPlungingC if topLayer is not None else None
        properties.HydraulicLoadNp = topLayer.StabilityPlungingN if topLayer is not None else None
        properties.HydraulicLoadAs = topLayer.StabilitySurgingA if topLayer is not None else None
        properties.HydraulicLoadBs = topLayer.StabilitySurgingB if topLayer is not None else None
        properties.HydraulicLoadCs = topLayer.StabilitySurgingC if topLayer is not None else None
        properties.HydraulicLoadNs = topLayer.StabilitySurgingN if topLayer is not None else None
        properties.HydraulicLoadXib = topLayer.Xib if topLayer is not None else None
        properties.SlopeUpperLevelAus = settings.SlopeUpperLevel if settings is not None else None
        properties.SlopeLowerLevelAls = settings.SLopeLowerLevel if settings is not None else None
        properties.UpperLimitLoadingAul = settings.UpperLimitLoadingA if settings is not None else None
        properties.UpperLimitLoadingBul = settings.UpperLimitLoadingB if settings is not None else None
        properties.UpperLimitLoadingCul = settings.UpperLimitLoadingC if settings is not None else None
        properties.LowerLimitLoadingAll = settings.LowerLimitLoadingA if settings is not None else None
        properties.LowerLimitLoadingBll = settings.LowerLimitLoadingB if settings is not None else None
        properties.LowerLimitLoadingCll = settings.LowerLimitLoadingC if settings is not None else None
        properties.DistanceMaximumWaveElevationAsmax = (
            settings.DistanceMaximumWaveElevationA if settings is not None else None
        )
        properties.DistanceMaximumWaveElevationBsmax = (
            settings.DistanceMaximumWaveElevationB if settings is not None else None
        )
        properties.NormativeWidthOfWaveImpactAwi = (
            settings.NormativeWidthOfWaveImpactA if settings is not None else None
        )
        properties.NormativeWidthOfWaveImpactBwi = (
            settings.NormativeWidthOfWaveImpactB if settings is not None else None
        )
        properties.WaveAngleImpactBetamax = settings.WaveAngleImpactBetaMax if settings is not None else None

        return properties

    @staticmethod
    def __createGrassWaveImpactConstructionProperties(
        locationData: GrassWaveImpactOutputLocationSpecification, settings: GrassWaveImpactCalculationSettings
    ):
        topLayerType = (
            GrassRevetmentTopLayerType.ClosedSod
            if locationData.TopLayerType == TopLayerType.GrassClosedSod
            else GrassRevetmentTopLayerType.OpenSod
        )
        properties = GrassRevetmentWaveImpactLocationConstructionProperties(locationData.XPosition, topLayerType)

        topLayer = (
            next((l for l in settings.TopLayersSettings if l.TopLayerType == locationData.TopLayerType), None)
            if settings is not None
            else None
        )

        properties.InitialDamage = locationData.InitialDamage
        properties.FailureNumber = settings.FailureNumber if settings is not None else None
        properties.TimeLineAgwi = topLayer.StanceTimeLineA if topLayer is not None else None
        properties.TimeLineBgwi = topLayer.StanceTimeLineB if topLayer is not None else None
        properties.TimeLineCgwi = topLayer.StanceTimeLineC if topLayer is not None else None
        properties.MinimumWaveHeightTemax = settings.Temax if settings is not None else None
        properties.MaximumWaveHeightTemin = settings.Temin if settings is not None else None
        properties.WaveAngleImpactNwa = settings.WaveAngleImpactN if settings is not None else None
        properties.WaveAngleImpactQwa = settings.WaveAngleImpactQ if settings is not None else None
        properties.WaveAngleImpactRwa = settings.WaveAngleImpactR if settings is not None else None
        properties.UpperLimitLoadingAul = settings.LoadingUpperLimit if settings is not None else None
        properties.LowerLimitLoadingAll = settings.LoadingLowerLimit if settings is not None else None

        return properties

    @staticmethod
    def __createGrassOvertoppingConstructionProperties(
        locationData: GrassOvertoppingOutputLocationSpecification, settings: GrassWaveOvertoppingCalculationSettings
    ):
        topLayerType = None
        match locationData.TopLayerType:
            case TopLayerType.GrassClosedSod:
                topLayerType = GrassRevetmentTopLayerType.ClosedSod
            case TopLayerType.GrassOpenSod:
                topLayerType = GrassRevetmentTopLayerType.OpenSod

        properties = GrassRevetmentOvertoppingLocationConstructionProperties(locationData.XPosition, topLayerType)

        topLayer = (
            next((l for l in settings.TopLayersSettings if l.TopLayerType == locationData.TopLayerType), None)
            if settings is not None
            else None
        )

        properties.InitialDamage = locationData.InitialDamage
        properties.IncreasedLoadTransitionAlphaM = locationData.IncreasedLoadTransitionAlphaM
        properties.ReducedStrengthTransitionAlphaS = locationData.ReducedStrengthTransitionAlphaS
        properties.FailureNumber = settings.FailureNumber if settings is not None else None
        properties.CriticalCumulativeOverload = topLayer.CriticalCumulativeOverload if topLayer is not None else None
        properties.CriticalFrontVelocity = topLayer.CriticalFrontVelocity if topLayer is not None else None
        properties.DikeHeight = settings.DikeHeight if settings is not None else None
        properties.AccelerationAlphaAForCrest = settings.AccelerationAlphaAForCrest if settings is not None else None
        properties.AccelerationAlphaAForInnerSlope = (
            settings.AccelerationAlphaAForInnerSlope if settings is not None else None
        )
        properties.FixedNumberOfWaves = settings.FixedNumberOfWaves if settings is not None else None
        properties.FrontVelocityCwo = settings.FrontVelocityCwo if settings is not None else None
        properties.AverageNumberOfWavesCtm = settings.FactorCtm if settings is not None else None

        return properties

    @staticmethod
    def __convertToCList(lst: list[list[float]]):
        cList = List[ValueTuple[Double, Double]]()
        if lst is not None:
            for l in lst:
                cList.Add(ValueTuple[Double, Double](l[0], l[1]))
        return cList
