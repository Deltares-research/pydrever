from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod


class TopLayerSettings:
    def __init__(self, type: TopLayerType):
        self.TopLayerType: TopLayerType = type


class AsphaltTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.WAB)
        self.StiffnessRatioNu: float = None
        self.FatigueAsphaltAlpha: float = None
        self.FatigueAsphaltBeta: float = None


class GrasCoverOvertoppingTopLayerSettings(TopLayerSettings):
    def __init__(self, topLayerType: TopLayerType):
        super().__init__(topLayerType)
        self.CriticalCumulativeOverload: float = None
        self.CriticalFrontVelocity: float = None


class GrassCoverWaveImpactTopLayerSettings(TopLayerSettings):
    def __init__(self, type: TopLayerType):
        super().__init__(type)
        self.StanceTimeLineA: float = None
        self.StanceTimeLineB: float = None
        self.StanceTimeLineC: float = None


class NaturalStoneTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.NordicStone)
        self.StabilityPlungingA: float = None
        self.StabilityPlungingC: float = None
        self.StabilityPlungingB: float = None
        self.StabilityPlungingN: float = None
        self.StabilitySurgingA: float = None
        self.StabilitySurgingB: float = None
        self.StabilitySurgingC: float = None
        self.StabilitySurgingN: float = None
        self.Xib: float = None


class CalculationSettings:
    def __init__(
        self, calculationMethod: CalculationMethod, topLayers: list[TopLayerSettings]
    ):
        self.CalculationMethod: CalculationMethod = calculationMethod
        self.FailureNumber: float = None
        self.TopLayersSettings: list[TopLayerSettings] = topLayers


class AsphaltCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.AsphaltWaveImpact, topLayers)
        self.DensityOfWater: float = None
        self.FactorCtm: float = None
        self.ImpactNumberC: float = None
        self.WidthFactors: list[float, float] = None
        self.DepthFactors: list[float, float] = None
        self.ImpactFactors: list[float, float] = None


class GrassWaveOvertoppingCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveOvertopping, topLayers)
        self.AccelerationAlphaAForCrest: float = None
        self.AccelerationAlphaAForInnerSlope: float = None
        self.FixedNumberOfWaves: int = None
        self.FrontVelocityCwo: float = None
        self.FactorCtm: float = None
        self.DikeHeight: float = None


class GrassWaveImpactCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveImpact, topLayers)
        self.LoadingUpperLimit: float = None
        self.LoadingLowerLimit: float = None
        self.WaveAngleImpactN: float = None
        self.WaveAngleImpactQ: float = None
        self.WaveAngleImpactR: float = None
        self.Temax: float = None
        self.Temin: float = None


class NaturalStoneCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.NaturalStone, topLayers)
        self.DistanceMaximumWaveElevationA: float = None
        self.DistanceMaximumWaveElevationB: float = None
        self.SlopeUpperLevel: float = None
        self.SLopeLowerLevel: float = None
        self.NormativeWidthOfWaveImpactA: float = None
        self.NormativeWidthOfWaveImpactB: float = None
        self.UpperLimitLoadingA: float = None
        self.UpperLimitLoadingB: float = None
        self.UpperLimitLoadingC: float = None
        self.LowerLimitLoadingA: float = None
        self.LowerLimitLoadingB: float = None
        self.LowerLimitLoadingC: float = None
        self.WaveAngleImpactBetaMax: float = None
