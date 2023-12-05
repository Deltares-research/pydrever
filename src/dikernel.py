import clr

clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Integration.dll")
clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Core.dll")

from dikernelinput import DikernelInput
from dikerneloutput import (
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    NaturalStoneOutputLocation,
)
from dikernelinputparser import DikernelInputParser


from DiKErnel.Core import Calculator
from DiKErnel.Core.Data import LocationDependentOutput

from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import AsphaltRevetmentWaveImpactLocationDependentOutput
from DiKErnel.Integration.Data.GrassRevetmentOvertopping import GrassRevetmentOvertoppingLocationDependentOutput
from DiKErnel.Integration.Data.GrassRevetmentWaveImpact import GrassRevetmentWaveImpactLocationDependentOutput

# TODO: also implement runup calculations
# from DiKErnel.Integration.Data.GrassRevetmentWaveRunup import GrassRevetmentWaveRunupRayleighLocationDependentOutput
from DiKErnel.Integration.Data.NaturalStoneRevetment import NaturalStoneRevetmentLocationDependentOutput


class Dikernel:
    @staticmethod
    def run(dikernelInput: DikernelInput) -> list[DikernelOutputLocation]:
        cInput = DikernelInputParser.ConvertToCInput(dikernelInput)
        calculator = Calculator(cInput)
        calculator.WaitForCompletion()
        return Dikernel.ConvertToDikernelOutput(calculator.Result.Data, dikernelInput)

    @staticmethod
    def ConvertToDikernelOutput(cOutput, input: DikernelInput) -> list[DikernelOutputLocation]:
        outputLocations = list[float]()
        i = 0
        for cOutputLocation in cOutput.LocationDependentOutputItems:
            cOutputLocation = cOutput.LocationDependentOutputItems[i]
            xPosition = input.OutputLocations[i].XPosition
            outputLocations.append(Dikernel.__createOutputLocation(cOutputLocation, xPosition))
            i = i + 1
        return outputLocations

    @staticmethod
    def __createOutputLocation(cOutputLocation: LocationDependentOutput, xPosition: float):
        momentOfFailure = (
            next((item for item in cOutputLocation.TimeDependentOutputItems if item is not None), None).TimeOfFailure
            if not None
            else None
        )

        timeDependentOutputItems = cOutputLocation.TimeDependentOutputItems
        damageDevelopment = list(item.Damage for item in timeDependentOutputItems)
        damageIncrement = list(item.IncrementDamage for item in timeDependentOutputItems)

        match cOutputLocation:
            case AsphaltRevetmentWaveImpactLocationDependentOutput():
                return AsphaltWaveImpactOutputLocation(
                    xPosition,
                    momentOfFailure,
                    damageDevelopment,
                    damageIncrement,
                    cOutputLocation.Z,
                    cOutputLocation.OuterSlope,
                    cOutputLocation.LogFlexuralStrength,
                    cOutputLocation.StiffnessRelation,
                    cOutputLocation.ComputationalThickness,
                    cOutputLocation.EquivalentElasticModulus,
                    list(item.MaximumPeakStress for item in timeDependentOutputItems),
                    list(item.AverageNumberOfWaves for item in timeDependentOutputItems),
                )
            case GrassRevetmentOvertoppingLocationDependentOutput():
                return GrassOvertoppingOutputLocation(
                    xPosition,
                    momentOfFailure,
                    damageDevelopment,
                    damageIncrement,
                    list(item.VerticalDistanceWaterLevelElevation for item in timeDependentOutputItems),
                    list(item.RepresentativeWaveRunup2P for item in timeDependentOutputItems),
                    list(item.CumulativeOverload for item in timeDependentOutputItems),
                    list(item.AverageNumberOfWaves for item in timeDependentOutputItems),
                )
            case GrassRevetmentWaveImpactLocationDependentOutput():
                return GrassWaveImpactOutputLocation(
                    xPosition,
                    momentOfFailure,
                    damageDevelopment,
                    damageIncrement,
                    cOutputLocation.Z,
                    cOutputLocation.MinimumWaveHeight,
                    cOutputLocation.MaximumWaveHeight,
                    list(item.LoadingRevetment for item in timeDependentOutputItems),
                    list(item.UpperLimitLoading for item in timeDependentOutputItems),
                    list(item.LowerLimitLoading for item in timeDependentOutputItems),
                    list(item.WaveAngle for item in timeDependentOutputItems),
                    list(item.WaveAngleImpact for item in timeDependentOutputItems),
                    list(item.WaveHeightImpact for item in timeDependentOutputItems),
                )
                """
                    TODO: Implement wave runup calculations
                    case GrassRevetmentWaveRunupRayleighLocationDependentOutput():
                    grassRevetmentWaveRunupRayleighTimeDependentOutputItems = cOutputLocation.TimeDependentOutputItems

                    return GrassWaveRunupOutputLocation(
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.IncrementDamage).ToList(),
                        grassRevetmentWaveRunupRayleighLocationDependentOutput.Z,
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.VerticalDistanceWaterLevelElevation).ToList(),
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.WaveAngle).ToList(),
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.WaveAngleImpact).ToList(),
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.RepresentativeWaveRunup2P).ToList(),
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.CumulativeOverload).ToList(),
                        grassRevetmentWaveRunupRayleighTimeDependentOutputItems
                            .Select(tdo => tdo.AverageNumberOfWaves).ToList()) """
            case NaturalStoneRevetmentLocationDependentOutput():
                return NaturalStoneOutputLocation(
                    xPosition,
                    momentOfFailure,
                    damageDevelopment,
                    damageIncrement,
                    cOutputLocation.Z,
                    cOutputLocation.Resistance,
                    list(item.OuterSlope for item in timeDependentOutputItems),
                    list(item.SlopeUpperLevel for item in timeDependentOutputItems),
                    list(item.SlopeUpperPosition for item in timeDependentOutputItems),
                    list(item.SlopeLowerLevel for item in timeDependentOutputItems),
                    list(item.SlopeLowerPosition for item in timeDependentOutputItems),
                    list(item.LoadingRevetment for item in timeDependentOutputItems),
                    list(item.SurfSimilarityParameter for item in timeDependentOutputItems),
                    list(item.WaveSteepnessDeepWater for item in timeDependentOutputItems),
                    list(item.UpperLimitLoading for item in timeDependentOutputItems),
                    list(item.LowerLimitLoading for item in timeDependentOutputItems),
                    list(item.DepthMaximumWaveLoad for item in timeDependentOutputItems),
                    list(item.DistanceMaximumWaveElevation for item in timeDependentOutputItems),
                    list(item.NormativeWidthOfWaveImpact for item in timeDependentOutputItems),
                    list(item.HydraulicLoad for item in timeDependentOutputItems),
                    list(item.WaveAngle for item in timeDependentOutputItems),
                    list(item.WaveAngleImpact for item in timeDependentOutputItems),
                    list(item.ReferenceTimeDegradation for item in timeDependentOutputItems),
                    list(item.ReferenceDegradation for item in timeDependentOutputItems),
                )
