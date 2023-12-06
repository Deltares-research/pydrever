from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod

# TODO: remove unnecessary defaults and add to calculation definition
# TODO: check all settings types in C# classes


class TopLayerSettings:
    def __init__(self, type: TopLayerType):
        self.TopLayerType: TopLayerType = type


class AsphaltTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.WAB)
        self.StiffnessRatioNu: float = 0.35
        self.FatigueAsphaltAlpha: float = 0.5
        self.FatigueAsphaltBeta: float = 5.4


class GrasCoverOvertoppingTopLayerSettings(TopLayerSettings):
    def __init__(self, topLayerType: TopLayerType):
        super().__init__(topLayerType)
        self.CriticalCumulativeOverload: float = 7000.0
        self.CriticalFrontVelocity: float = 6.6


class GrassCoverWaveImpactTopLayerSettings(TopLayerSettings):
    def __init__(self, type: TopLayerType):
        super().__init__(type)
        self.StanceTimeLineA: float = 1.0
        self.StanceTimeLineB: float = -0.000009722
        self.StanceTimeLineC: float = 0.25


class NaturalStoneTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.NordicStone)
        self.StabilityPlungingA: float = 4.0
        self.StabilityPlungingB: float = 0.0
        self.StabilityPlungingC: float = 0.0
        self.StabilityPlungingN: float = -0.9
        self.StabilitySurgingA: float = 0.8
        self.StabilitySurgingB: float = 0.0
        self.StabilitySurgingC: float = 0.0
        self.StabilitySurgingN: float = 0.6
        self.Xib: float = 2.9


class CalculationSettings:
    def __init__(self, calculationMethod: CalculationMethod, topLayers: list[TopLayerSettings]):
        self.CalculationMethod: CalculationMethod = calculationMethod
        self.FailureNumber: float = 1.0
        self.TopLayersSettings: list[TopLayerSettings] = topLayers


class AsphalCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[float]):
        super().__init__(CalculationMethod.AsphaltWaveImpact, topLayers)
        self.DensityOfWater: float = 1000.0
        self.FactorCtm: float = 1.0
        self.ImpactNumberC: float = 1.0
        self.WidthFactors: list[float, float] = [
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
        ]
        self.DepthFactors: list[float, float] = [
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
        ]
        self.ImpactFactors: list[float, float] = [
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
        ]


class GrassWaveOvertoppingCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveOvertopping, topLayers)
        self.AccelerationAlphaAForCrest: float = 1.0
        self.AccelerationAlphaAForInnerSlope: float = 1.4
        self.FixedNumberOfWaves: int = 10000
        self.FrontVelocityCwo: float = 1.45
        self.FactorCtm: float = 0.92
        self.DikeHeight: float = None


class GrassWaveImpactCalculationSettings(CalculationSettings):
    def __init__(self, topLayers):
        super().__init__(CalculationMethod.GrassWaveImpact, topLayers)
        self.LoadingUpperLimit: float = 0.0
        self.LoadingLowerLimit: float = 0.5
        self.WaveAngleImpactN: float = 0.6666666666666667
        self.WaveAngleImpactQ: float = 0.35
        self.WaveAngleImpactR: float = 10.0
        self.Temax: float = 3600000.0
        self.Temin: float = 3.6


class NaturalStoneCalculationSettings(CalculationSettings):
    def __init__(self):
        topLayers = [NaturalStoneTopLayerSettings()]
        super().__init__(CalculationMethod.NaturalStone, topLayers)
        self.DistanceMaximumWaveElevationA: float = 0.42
        self.DistanceMaximumWaveElevationB: float = 0.9
        self.ForcingUpperBoundaryA: float = 0.1
        self.ForcingUpperBoundaryB: float = 0.6
        self.ForcingUpperBoundaryC: float = 4.0
        self.ForcingLowerBoundaryA: float = 0.1
        self.ForcingLowerBoundaryB: float = 0.2
        self.ForcingLowerBoundaryC: float = 4.0
        self.SlopeUpperLevel: float = 0.05
        self.SLopeLowerLevel: float = 1.5
        self.ImpactWageAngleBetaMax: float = 78.0
        self.NormativeWidthOfWaveImpactA: float = 0.96
        self.NormativeWidthOfWaveImpactB: float = 0.11
        self.UpperLimitLoadingA: float = None
        self.UpperLimitLoadingB: float = None
        self.UpperLimitLoadingC: float = None
        self.LowerLimitLoadingA: float = None
        self.LowerLimitLoadingB: float = None
        self.LowerLimitLoadingC: float = None
        self.WaveAngleImpactBetaMax: float = None
