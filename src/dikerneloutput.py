from calculationmethods import CalculationMethod


class DikernelOutputLocation:
    def __init__(
        self,
        calculationType: CalculationMethod,
        xPosition: float,
        timeOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
    ):
        self.__xPosition = xPosition
        self.__timeOfFailure = timeOfFailure
        self.__damageDevelopment = damageDevelopment
        self.__damageIncrement = damageIncrement
        self.__calculationType = calculationType

    @property
    def CalculationMethod(self) -> CalculationMethod:
        """
        Returns:
            CalculationMethod: The calculation method that was used at this output location.
        """
        return self.__calculationType

    @property
    def XPosition(self) -> float:
        """
        Returns:
            float: The cross-shore position of the calculated location.
        """
        return self.__xPosition

    @property
    def Failed(self) -> bool:
        """
        Returns:
            bool: Whether the revetment has failed at this position.
        """
        return self.__timeOfFailure is not None

    @property
    def TimeOfFailure(self) -> float:
        """
        Returns:
            float: The moment (time step) this location failed. None if it did not fail.
        """
        return self.__timeOfFailure

    @property
    def DamageDevelopment(self) -> list[float]:
        """
        Returns:
            list[float]: The damage level at the end of each time step.
        """
        return self.__damageDevelopment

    @property
    def Damage(self) -> float:
        return self.__damageDevelopment[-1] if self.__damageDevelopment is not None else 0.0

    @property
    def DamageIncrement(self) -> list[float]:
        """
        Returns:
            list[float]: The increment of the damage level during each time step.
        """
        return self.__damageIncrement


class AsphaltWaveImpactOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        xPosition: float,
        timeOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        z: float,
        outerSlope: float,
        logFlexuralStrength: float,
        stiffnessRelation: float,
        computationalThickness: float,
        equivalentElasticModulus: float,
        maximumPeakStress: list[float],
        averageNumberOfWaves: list[float],
    ):
        super().__init__(
            CalculationMethod.AsphaltWaveImpact, xPosition, timeOfFailure, damageDevelopment, damageIncrement
        )
        self.__zPosition = z
        self.__outerSlope = outerSlope
        self.__logFlexuralStrength = logFlexuralStrength
        self.__stiffnessRelation = stiffnessRelation
        self.__computationalThickness = computationalThickness
        self.__equivalentElasticModulus = equivalentElasticModulus
        self.__maximumPeakStress = maximumPeakStress
        self.__averageNumberOfWaves = averageNumberOfWaves

    @property
    def ZPosition(self) -> float:
        return self.__zPosition

    @property
    def OuterSlope(self) -> float:
        return self.__outerSlope

    @property
    def LogFlexuralStrength(self) -> float:
        return self.__logFlexuralStrength

    @property
    def StiffnessRelation(self) -> float:
        return self.__stiffnessRelation

    @property
    def ComputationalThickness(self) -> float:
        return self.__computationalThickness

    @property
    def EquivalentElasticModulus(self) -> float:
        return self.__equivalentElasticModulus

    @property
    def MaximumPeakStress(self) -> list[float]:
        return self.__maximumPeakStress

    @property
    def AverageNumberOfWaves(self) -> list[float]:
        return self.__averageNumberOfWaves


class GrassOvertoppingOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        xPosition: float,
        timeOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        verticalDistanceWaterLevelElevation: list[float],
        representativeWaveRunup2P: list[float],
        cumulativeOverload: list[float],
        averageNumberOfWaves: list[float],
    ):
        super().__init__(
            CalculationMethod.GrassWaveOvertopping, xPosition, timeOfFailure, damageDevelopment, damageIncrement
        )
        self.__verticalDistanceWaterLevelElevation = verticalDistanceWaterLevelElevation
        self.__representativeWaveRunup2P = representativeWaveRunup2P
        self.__cumulativeOverload = cumulativeOverload
        self.__averageNumberOfWaves = averageNumberOfWaves

    @property
    def VerticalDistanceWaterLevelElevation(self) -> list[float]:
        return self.__verticalDistanceWaterLevelElevation

    @property
    def RepresentativeWaveRunup2P(self) -> list[float]:
        return self.__representativeWaveRunup2P

    @property
    def CumulativeOverload(self) -> list[float]:
        return self.__cumulativeOverload

    @property
    def AverageNumberOfWaves(self) -> list[float]:
        return self.__averageNumberOfWaves


class GrassWaveImpactOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        xPosition: float,
        timeOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        z: float,
        minimumWaveHeight: float,
        maximumWaveHeight: float,
        loadingRevetment: list[float],
        upperLimitLoading: list[float],
        lowerLimitLoading: list[float],
        waveAngle: list[float],
        waveAngleImpact: list[float],
        waveHeightImpact: list[float],
    ):
        super().__init__(
            CalculationMethod.GrassWaveImpact, xPosition, timeOfFailure, damageDevelopment, damageIncrement
        )
        self.__zPosition = z
        self.__minimumWaveHeight = minimumWaveHeight
        self.__maximumWaveHeight = maximumWaveHeight
        self.__loadingRevetment = loadingRevetment
        self.__upperLimitLoading = upperLimitLoading
        self.__lowerLimitLoading = lowerLimitLoading
        self.__waveAngle = waveAngle
        self.__waveAngleImpact = waveAngleImpact
        self.__waveHeightImpact = waveHeightImpact

    @property
    def ZPosition(self) -> float:
        return self.__zPosition

    @property
    def MinimumWaveHeight(self) -> float:
        return self.__minimumWaveHeight

    @property
    def MaximumWaveHeight(self) -> float:
        return self.__maximumWaveHeight

    @property
    def LoadingRevetment(self) -> list[float]:
        return self.__loadingRevetment

    @property
    def UpperLimitLoading(self) -> list[float]:
        return self.__upperLimitLoading

    @property
    def LowerLimitLoading(self) -> list[float]:
        return self.__lowerLimitLoading

    @property
    def WaveAngle(self) -> list[float]:
        return self.__waveAngle

    @property
    def WaveAngleImpact(self) -> list[float]:
        return self.__waveAngleImpact

    @property
    def WaveHeightImpact(self) -> list[float]:
        return self.__waveHeightImpact


class NaturalStoneOutputLocation(DikernelOutputLocation):
    def __init__(
        self,
        xPosition: float,
        timeOfFailure: float,
        damageDevelopment: list[float],
        damageIncrement: list[float],
        z: float,
        resistance: float,
        outerSlope: list[float],
        slopeUpperLevel: list[float],
        slopeUpperPosition: list[float],
        slopeLowerLevel: list[float],
        slopeLowerPosition: list[float],
        loadingRevetment: list[float],
        surfSimilarityParameter: list[float],
        waveSteepnessDeepWater: list[float],
        upperLimitLoading: list[float],
        lowerLimitLoading: list[float],
        depthMaximumWaveLoad: list[float],
        distanceMaximumWaveElevation: list[float],
        normativeWidthOfWaveImpact: list[float],
        hydraulicLoad: list[float],
        waveAngle: list[float],
        waveAngleImpact: list[float],
        referenceTimeDegradation: list[float],
        referenceDegradation: list[float],
    ):
        super().__init__(CalculationMethod.NaturalStone, xPosition, timeOfFailure, damageDevelopment, damageIncrement)
        self.__zPosition = z
        self.__resistance = resistance
        self.__outerSlope = outerSlope
        self.__slopeUpperLevel = slopeUpperLevel
        self.__slopeUpperPosition = slopeUpperPosition
        self.__slopeLowerLevel = slopeLowerLevel
        self.__slopeLowerPosition = slopeLowerPosition
        self.__loadingRevetment = loadingRevetment
        self.__surfSimilarityParameter = surfSimilarityParameter
        self.__waveSteepnessDeepWater = waveSteepnessDeepWater
        self.__upperLimitLoading = upperLimitLoading
        self.__lowerLimitLoading = lowerLimitLoading
        self.__depthMaximumWaveLoad = depthMaximumWaveLoad
        self.__distanceMaximumWaveElevation = distanceMaximumWaveElevation
        self.__normativeWidthOfWaveImpact = normativeWidthOfWaveImpact
        self.__hydraulicLoad = hydraulicLoad
        self.__waveAngle = waveAngle
        self.__waveAngleImpact = waveAngleImpact
        self.__referenceTimeDegradation = referenceTimeDegradation
        self.__referenceDegradation = referenceDegradation

    @property
    def ZPosition(self) -> float:
        return self.__zPosition

    @property
    def Resistance(self) -> float:
        return self.__resistance

    @property
    def OuterSlope(self) -> list[float]:
        return self.__outerSlope

    @property
    def SlopeUpperLevel(self) -> list[float]:
        return self.__slopeUpperLevel

    @property
    def SlopeUpperPosition(self) -> list[float]:
        return self.__slopeUpperPosition

    @property
    def SlopeLowerLevel(self) -> list[float]:
        return self.__slopeLowerLevel

    @property
    def SlopeLowerPosition(self) -> list[float]:
        return self.__slopeLowerPosition

    @property
    def LoadingRevetment(self) -> list[float]:
        return self.__loadingRevetment

    @property
    def SurfSimilarityParameter(self) -> list[float]:
        return self.__surfSimilarityParameter

    @property
    def WaveSteepnessDeepWater(self) -> list[float]:
        return self.__waveSteepnessDeepWater

    @property
    def UpperLimitLoading(self) -> list[float]:
        return self.__upperLimitLoading

    @property
    def LowerLimitLoading(self) -> list[float]:
        return self.__lowerLimitLoading

    @property
    def DepthMaximumWaveLoad(self) -> list[float]:
        return self.__depthMaximumWaveLoad

    @property
    def DistanceMaximumWaveElevation(self) -> list[float]:
        return self.__distanceMaximumWaveElevation

    @property
    def NormativeWidthOfWaveImpact(self) -> list[float]:
        return self.__normativeWidthOfWaveImpact

    @property
    def HydraulicLoad(self) -> list[float]:
        return self.__hydraulicLoad

    @property
    def WaveAngle(self) -> list[float]:
        return self.__waveAngle

    @property
    def WaveAngleImpact(self) -> list[float]:
        return self.__waveAngleImpact

    @property
    def ReferenceTimeDegradation(self) -> list[float]:
        return self.__referenceTimeDegradation

    @property
    def ReferenceDegradation(self) -> list[float]:
        return self.__referenceDegradation
