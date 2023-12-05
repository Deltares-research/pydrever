from dikernelinput import DikernelInput, HydraulicInput, DikeSchematization
from dikerneloutputlocations import (
    AsphaltOutputLocation,
    NordicStoneOutputLocation,
    GrassWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
)
from dikernelcalculationsettings import (
    AsphalCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    GrassWaveImpactCalculationSettings,
    NaturalStoneCalculationSettings,
)
import clr

clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Integration.dll")
clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Core.dll")

from System import Double, ValueTuple
from System.Collections.Generic import List

from DiKErnel.Integration import CalculationInputBuilder
from DiKErnel.Core.Data import CharacteristicPointType
from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import (
    AsphaltRevetmentWaveImpactLocationConstructionProperties,
)
from DiKErnel.Integration.Data.NaturalStoneRevetment import NaturalStoneRevetmentLocationConstructionProperties
from DiKErnel.Integration.Data.GrassRevetmentOvertopping import GrassRevetmentOvertoppingLocationConstructionProperties
from DiKErnel.Integration.Data.GrassRevetmentWaveImpact import GrassRevetmentWaveImpactLocationConstructionProperties

# TODO: Also allow runup calculaitons
# from DiKErnel.Integration.Data.GrassRevetmentWaveRunup import GrassRevetmentWaveRunupLocationConstructionProperties

from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import AsphaltRevetmentTopLayerType
from DiKErnel.Integration.Data.GrassRevetment import GrassRevetmentTopLayerType
from DiKErnel.Integration.Data.NaturalStoneRevetment import NaturalStoneRevetmentTopLayerType


class DikernelInputParser:
    @staticmethod
    def ConvertToCInput(dikernelInput: DikernelInput):
        builder = CalculationInputBuilder(dikernelInput.DikeOrientation)
        DikernelInputParser.__addDikeProfileToBuilder(builder, dikernelInput.DikeSchematization)
        DikernelInputParser.__addHydraulicsToBuilder(builder, dikernelInput.HydraulicInput)
        DikernelInputParser.__addOutputLocationsToBuilder(builder, dikernelInput)
        composedInput = builder.Build()
        # TODO: Validate input with DiKErnel.Core.Validator()
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
    def __addOutputLocationsToBuilder(
        builder: CalculationInputBuilder, dikernelInput: DikernelInput
    ) -> CalculationInputBuilder:
        locationDataItems = dikernelInput.OutputLocations
        calculationSettings = dikernelInput.Settings

        for locationData in locationDataItems:
            match locationData:
                case AsphaltOutputLocation():
                    builder.AddAsphaltWaveImpactLocation(
                        DikernelInputParser.__createAsphaltWaveImpactConstructionProperties(
                            locationData,
                            next((ci for ci in calculationSettings if isinstance(ci, AsphalCalculationSettings))),
                        )
                    )
                case NordicStoneOutputLocation():
                    builder.AddNaturalStoneLocation(
                        DikernelInputParser.__createNaturalStoneConstructionProperties(
                            locationData,
                            next(
                                (ci for ci in calculationSettings if isinstance(ci, NaturalStoneCalculationSettings))
                            ),
                        )
                    )

                case GrassWaveImpactOutputLocation():
                    builder.AddGrassWaveImpactLocation(
                        DikernelInputParser.__createGrassWaveImpactConstructionProperties(
                            locationData,
                            next(
                                (
                                    ci
                                    for ci in calculationSettings
                                    if isinstance(ci, GrassWaveImpactCalculationSettings)
                                )
                            ),
                        )
                    )
                case GrassOvertoppingOutputLocation():
                    builder.AddGrassOvertoppingLocation(
                        DikernelInputParser.__createGrassOvertoppingConstructionProperties(
                            locationData,
                            next(
                                (
                                    ci
                                    for ci in calculationSettings
                                    if isinstance(ci, GrassWaveOvertoppingCalculationSettings)
                                )
                            ),
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
        locationData: AsphaltOutputLocation, settings: AsphalCalculationSettings
    ):
        properties = AsphaltRevetmentWaveImpactLocationConstructionProperties(
            locationData.XPosition,
            AsphaltRevetmentTopLayerType.HydraulicAsphaltConcrete,
            locationData.FlexuralStrent,
            locationData.SoilElasticity,
            locationData.TopLayerThickness,
            locationData.TopLayerElasticModulus,
        )

        topLayer = next((l for l in settings.TopLayers if l.TopLayerType == locationData.TopLayerType), None)

        properties.InitialDamage = locationData.InitialDamage
        properties.ThicknessSubLayer = locationData.SubLayerThickness
        properties.ElasticModulusSubLayer = locationData.SubLayerElasticModulus
        properties.FailureNumber = settings.FailureNumber
        properties.DensityOfWater = settings.DensityOfWater
        properties.AverageNumberOfWavesCtm = settings.FactorCtm
        properties.FatigueAlpha = topLayer.FatigueAsphaltAlpha
        properties.FatigueBeta = topLayer.FatigueAsphaltBeta
        properties.StiffnessRelationNu = topLayer.StiffnessRatioNu
        properties.ImpactNumberC = settings.ImpactNumberC
        properties.WidthFactors = DikernelInputParser.__convertToCList(settings.WidthFactors)
        properties.DepthFactors = DikernelInputParser.__convertToCList(settings.DepthFactors)
        properties.ImpactFactors = DikernelInputParser.__convertToCList(settings.ImpactFactors)

        return properties

    @staticmethod
    def __createNaturalStoneConstructionProperties(
        locationData: NordicStoneOutputLocation, settings: NaturalStoneCalculationSettings
    ):
        properties = NaturalStoneRevetmentLocationConstructionProperties(
            locationData.XPosition,
            NaturalStoneRevetmentTopLayerType.NordicStone,
            locationData.TopLayerThickness,
            locationData.RelativeDensity,
        )

        topLayer = next((l for l in settings.TopLayers if l.TopLayerType == locationData.TopLayerType), None)

        properties.InitialDamage = locationData.InitialDamage
        properties.FailureNumber = settings.FailureNumber
        properties.HydraulicLoadAp = topLayer.StabilityPlungingA
        properties.HydraulicLoadBp = topLayer.StabilityPlungingB
        properties.HydraulicLoadCp = topLayer.StabilityPlungingC
        properties.HydraulicLoadNp = topLayer.StabilityPlungingN
        properties.HydraulicLoadAs = topLayer.StabilitySurgingA
        properties.HydraulicLoadBs = topLayer.StabilitySurgingB
        properties.HydraulicLoadCs = topLayer.StabilitySurgingC
        properties.HydraulicLoadNs = topLayer.StabilitySurgingN
        properties.HydraulicLoadXib = topLayer.Xib
        properties.SlopeUpperLevelAus = settings.SlopeUpperLevel
        properties.SlopeLowerLevelAls = settings.SLopeLowerLevel
        properties.UpperLimitLoadingAul = settings.UpperLimitLoadingA
        properties.UpperLimitLoadingBul = settings.UpperLimitLoadingB
        properties.UpperLimitLoadingCul = settings.UpperLimitLoadingC
        properties.LowerLimitLoadingAll = settings.LowerLimitLoadingA
        properties.LowerLimitLoadingBll = settings.LowerLimitLoadingB
        properties.LowerLimitLoadingCll = settings.LowerLimitLoadingC
        properties.DistanceMaximumWaveElevationAsmax = settings.DistanceMaximumWaveElevationA
        properties.DistanceMaximumWaveElevationBsmax = settings.DistanceMaximumWaveElevationB
        properties.NormativeWidthOfWaveImpactAwi = settings.NormativeWidthOfWaveImpactA
        properties.NormativeWidthOfWaveImpactBwi = settings.NormativeWidthOfWaveImpactB
        properties.WaveAngleImpactBetamax = settings.WaveAngleImpactBetaMax

        return properties

    @staticmethod
    def __createGrassWaveImpactConstructionProperties(
        locationData: GrassWaveImpactOutputLocation, settings: GrassWaveImpactCalculationSettings
    ):
        topLayerType = (
            GrassRevetmentTopLayerType.ClosedSod
            if locationData.TopLayerType == "grasGeslotenZode"
            else GrassRevetmentTopLayerType.OpenSod
        )
        properties = GrassRevetmentWaveImpactLocationConstructionProperties(locationData.XPosition, topLayerType)

        topLayer = next((l for l in settings.TopLayers if l.TopLayerType == locationData.TopLayerType), None)

        properties.InitialDamage = locationData.InitialDamage
        properties.FailureNumber = settings.FailureNumber
        properties.TimeLineAgwi = topLayer.StanceTimeLineA
        properties.TimeLineBgwi = topLayer.StanceTimeLineB
        properties.TimeLineCgwi = topLayer.StanceTimeLineC
        properties.MinimumWaveHeightTemax = settings.Temax
        properties.MaximumWaveHeightTemin = settings.Temin
        properties.WaveAngleImpactNwa = settings.WaveAngleImpactN
        properties.WaveAngleImpactQwa = settings.WaveAngleImpactQ
        properties.WaveAngleImpactRwa = settings.WaveAngleImpactR
        properties.UpperLimitLoadingAul = settings.LoadingUpperLimit
        properties.LowerLimitLoadingAll = settings.LoadingLowerLimit

        return properties

    @staticmethod
    def __createGrassOvertoppingConstructionProperties(
        locationData: GrassOvertoppingOutputLocation, settings: GrassWaveOvertoppingCalculationSettings
    ):
        topLayerType = (
            GrassRevetmentTopLayerType.ClosedSod
            if locationData.TopLayerType == "grasGeslotenZode"  # TODO: Implement enum value
            else GrassRevetmentTopLayerType.OpenSod
        )

        properties = GrassRevetmentOvertoppingLocationConstructionProperties(locationData.XPosition, topLayerType)

        topLayer = next((l for l in settings.TopLayers if l.TopLayerType == locationData.TopLayerType), None)

        properties.InitialDamage = locationData.InitialDamage
        properties.IncreasedLoadTransitionAlphaM = locationData.IncreasedLoadTransitionAlphaM
        properties.ReducedStrengthTransitionAlphaS = locationData.ReducedStrengthTransitionAlphaS
        properties.FailureNumber = settings.FailureNumber
        properties.CriticalCumulativeOverload = topLayer.CriticalCumulativeOverload
        properties.CriticalFrontVelocity = topLayer.CriticalFrontVelocity
        properties.DikeHeight = settings.DikeHeight
        properties.AccelerationAlphaAForCrest = settings.AccelerationAlphaAForCrest
        properties.AccelerationAlphaAForInnerSlope = settings.AccelerationAlphaAForInnerSlope
        properties.FixedNumberOfWaves = settings.FixedNumberOfWaves
        properties.FrontVelocityCwo = settings.FrontVelocityCwo
        properties.AverageNumberOfWavesCtm = settings.FactorCtm

        return properties

    @staticmethod
    def __convertToCList(lst: list[list[float]]):
        cList = List[ValueTuple[Double, Double]]()
        for l in lst:
            cList.Add(ValueTuple[Double, Double](l[0], l[1]))
        return cList
