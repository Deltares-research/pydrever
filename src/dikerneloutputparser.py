from dikerneloutput import (
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    NaturalStoneOutputLocation,
)
from dikernelcreferences import *


class DikernelOutputParser:
    @staticmethod
    def parsedikerneloutput(cOutput: CalculationOutput, xPositions: list[float]) -> list[DikernelOutputLocation]:
        outputLocations = list[float]()
        i = 0
        for cOutputLocation in cOutput.LocationDependentOutputItems:
            cOutputLocation = cOutput.LocationDependentOutputItems[i]
            xPosition = xPositions[i]
            outputLocations.append(DikernelOutputParser.__createOutputLocation(cOutputLocation, xPosition))
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
                return DikernelOutputParser.__createAsphaltWaveImpactOutputLocation(
                    xPosition,
                    cOutputLocation.Z,
                    momentOfFailure,
                    cOutputLocation.OuterSlope,
                    cOutputLocation.LogFlexuralStrength,
                    cOutputLocation.StiffnessRelation,
                    cOutputLocation.ComputationalThickness,
                    cOutputLocation.EquivalentElasticModulus,
                    damageDevelopment,
                    damageIncrement,
                    timeDependentOutputItems,
                )
            case GrassRevetmentOvertoppingLocationDependentOutput():
                return DikernelOutputParser.__createGrassOvertoppingOutputLocation(
                    xPosition, momentOfFailure, damageDevelopment, damageIncrement, timeDependentOutputItems
                )
            case GrassRevetmentWaveImpactLocationDependentOutput():
                return DikernelOutputParser.__createGrassWaveImpactOutputLocation(
                    xPosition,
                    cOutputLocation.Z,
                    momentOfFailure,
                    cOutputLocation.MinimumWaveHeight,
                    cOutputLocation.MaximumWaveHeight,
                    damageDevelopment,
                    damageIncrement,
                    timeDependentOutputItems,
                )
            case GrassRevetmentWaveRunupRayleighLocationDependentOutput():
                return None
                """
                    TODO: Implement wave runup calculations
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
                return DikernelOutputParser.__createNaturalStoneOutputLocation(
                    xPosition,
                    cOutputLocation.Z,
                    momentOfFailure,
                    cOutputLocation.Resistance,
                    damageDevelopment,
                    damageIncrement,
                    timeDependentOutputItems,
                )

    @staticmethod
    def __createAsphaltWaveImpactOutputLocation(
        xPosition: float,
        zPosition: float,
        momentOfFailure: float,
        outerSlope: float,
        logFlexuralStrength: float,
        stiffnessRelation: float,
        computationalThickness: float,
        equivalentElasticModulus: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        timeDependentOutputItems,
    ) -> AsphaltWaveImpactOutputLocation:
        return AsphaltWaveImpactOutputLocation(
            xPosition,
            momentOfFailure,
            damageDevelopment,
            damageIncrement,
            zPosition,
            outerSlope,
            logFlexuralStrength,
            stiffnessRelation,
            computationalThickness,
            equivalentElasticModulus,
            list(item.MaximumPeakStress for item in timeDependentOutputItems),
            list(item.AverageNumberOfWaves for item in timeDependentOutputItems),
        )

    @staticmethod
    def __createGrassOvertoppingOutputLocation(
        xPosition: float,
        momentOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        timeDependentOutputItems,
    ) -> GrassOvertoppingOutputLocation:
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

    @staticmethod
    def __createGrassWaveImpactOutputLocation(
        xPosition: float,
        zPosition: float,
        momentOfFailure: float,
        minimumWaveHeight: float,
        maximumWaveHeight: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        timeDependentOutputItems,
    ) -> GrassWaveImpactOutputLocation:
        return GrassWaveImpactOutputLocation(
            xPosition,
            momentOfFailure,
            damageDevelopment,
            damageIncrement,
            zPosition,
            minimumWaveHeight,
            maximumWaveHeight,
            list(item.LoadingRevetment for item in timeDependentOutputItems),
            list(item.UpperLimitLoading for item in timeDependentOutputItems),
            list(item.LowerLimitLoading for item in timeDependentOutputItems),
            list(item.WaveAngle for item in timeDependentOutputItems),
            list(item.WaveAngleImpact for item in timeDependentOutputItems),
            list(item.WaveHeightImpact for item in timeDependentOutputItems),
        )

    @staticmethod
    def __createNaturalStoneOutputLocation(
        xPosition: float,
        zPosition: float,
        momentOfFailure: float,
        resistance: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        timeDependentOutputItems,
    ) -> NaturalStoneOutputLocation:
        return NaturalStoneOutputLocation(
            xPosition,
            momentOfFailure,
            damageDevelopment,
            damageIncrement,
            zPosition,
            resistance,
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
