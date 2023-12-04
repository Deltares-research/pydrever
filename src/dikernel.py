from dikernelinput import DikernelInput
from dikerneloutput import DikernelOutput
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

from System import Double, Array, ValueTuple
from System.Collections.Generic import List
from DiKErnel.Integration import CalculationInputBuilder
from DiKErnel.Core.Data import CharacteristicPointType
from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import (
    AsphaltRevetmentWaveImpactLocationConstructionProperties,
)
from DiKErnel.Integration.Data.NaturalStoneRevetment import NaturalStoneRevetmentLocationConstructionProperties
from DiKErnel.Integration.Data.GrassRevetmentOvertopping import GrassRevetmentOvertoppingLocationConstructionProperties
from DiKErnel.Integration.Data.GrassRevetmentWaveImpact import GrassRevetmentWaveImpactLocationConstructionProperties
from DiKErnel.Integration.Data.GrassRevetmentWaveRunup import GrassRevetmentWaveRunupLocationConstructionProperties

from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import AsphaltRevetmentTopLayerType
from DiKErnel.Integration.Data.GrassRevetment import GrassRevetmentTopLayerType
from DiKErnel.Integration.Data.NaturalStoneRevetment import NaturalStoneRevetmentTopLayerType


class Dikernel:
    @staticmethod
    def run(dikernelInput: DikernelInput) -> DikernelOutput:
        cInput = Dikernel.ConvertToCInput(dikernelInput)
        calculator = Dikernel.calculatorDll.Calculator(cInput)
        calculator.WaitForCompletion()
        return Dikernel.ConvertToDikernelOutput(calculator.Result)

    @staticmethod
    def ConvertToCInput(dikernelInput: DikernelInput):
        builder = builder = CalculationInputBuilder(dikernelInput.DikeOrientation)
        builder = Dikernel.__addDikeProfileToBuilder(builder, dikernelInput)
        builder = Dikernel.__addHydraulicsToBuilder(builder, dikernelInput)
        builder = Dikernel.__addOutputLocationsToBuilder(builder, dikernelInput)
        return builder.Build()

    @staticmethod
    def __addDikeProfileToBuilder(
        builder: CalculationInputBuilder, dikernelInput: DikernelInput
    ) -> CalculationInputBuilder:
        for i in range(len(dikernelInput.DikeSchematization.XPositions) - 1):
            xStart = dikernelInput.DikeSchematization.XPositions[i]
            zStart = dikernelInput.DikeSchematization.ZPositions[i]
            xEnd = dikernelInput.DikeSchematization.XPositions[i + 1]
            zEnd = dikernelInput.DikeSchematization.ZPositions[i + 1]
            roughness = dikernelInput.DikeSchematization.Roughnesses[i]
            builder.AddDikeProfileSegment(xStart, zStart, xEnd, zEnd, roughness)

        if dikernelInput.DikeSchematization.OuterToe is not None:
            builder.AddDikeProfilePoint(dikernelInput.DikeSchematization.OuterToe, CharacteristicPointType.OuterToe)

        if dikernelInput.DikeSchematization.CrestOuterBerm is not None:
            builder.AddDikeProfilePoint(
                dikernelInput.DikeSchematization.CrestOuterBerm, CharacteristicPointType.CrestOuterBerm
            )

        if dikernelInput.DikeSchematization.NotchOuterBerm is not None:
            builder.AddDikeProfilePoint(
                dikernelInput.DikeSchematization.NotchOuterBerm, CharacteristicPointType.NotchOuterBerm
            )

        if dikernelInput.DikeSchematization.OuterCrest is not None:
            builder.AddDikeProfilePoint(
                dikernelInput.DikeSchematization.OuterCrest, CharacteristicPointType.OuterCrest
            )

        if dikernelInput.DikeSchematization.InnerCrest is not None:
            builder.AddDikeProfilePoint(
                dikernelInput.DikeSchematization.InnerCrest, CharacteristicPointType.InnerCrest
            )

        if dikernelInput.DikeSchematization.InnerToe is not None:
            builder.AddDikeProfilePoint(dikernelInput.DikeSchematization.InnerToe, CharacteristicPointType.InnerToe)

        return builder

    @staticmethod
    def __addHydraulicsToBuilder(
        builder: CalculationInputBuilder, dikernelInput: DikernelInput
    ) -> CalculationInputBuilder:
        hydraulicData = dikernelInput.HydraulicInput

        waterLevels = hydraulicData.WaterLevels
        waveHeightsHm0 = hydraulicData.WaveHeights
        wavePeriodsTm10 = hydraulicData.WavePeriods
        waveDirections = hydraulicData.WaveDirections

        times = hydraulicData.TimeSteps

        for i in range(len(waterLevels) - 1):
            builder.AddTimeStep(
                Double(times[i]),
                Double(times[i + 1]),
                Double(waterLevels[i]),
                Double(waveHeightsHm0[i]),
                Double(wavePeriodsTm10[i]),
                Double(waveDirections[i]),
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
                        Dikernel.__createAsphaltWaveImpactConstructionProperties(
                            locationData,
                            next((ci for ci in calculationSettings if isinstance(ci, AsphalCalculationSettings))),
                        )
                    )
                case NordicStoneOutputLocation():
                    builder.AddNaturalStoneLocation(
                        Dikernel.__createNaturalStoneConstructionProperties(
                            locationData,
                            next(
                                (ci for ci in calculationSettings if isinstance(ci, NaturalStoneCalculationSettings))
                            ),
                        )
                    )

                case GrassWaveImpactOutputLocation():
                    builder.AddGrassWaveImpactLocation(
                        Dikernel.__createGrassWaveImpactConstructionProperties(
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
                        Dikernel.__createGrassOvertoppingConstructionProperties(
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
        properties.WidthFactors = Dikernel.__convertToCList(settings.WidthFactors)
        properties.DepthFactors = Dikernel.__convertToCList(settings.DepthFactors)
        properties.ImpactFactors = Dikernel.__convertToCList(settings.ImpactFactors)

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
            if locationData.TopLayerType == "grasGeslotenZode"
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

    @staticmethod
    def ConvertToDikernelOutput(cOutput) -> DikernelOutput:
        pass
