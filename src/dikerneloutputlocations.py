from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod


class OutputLocationSpecification:
    def __init__(
        self,
        xPosition: float,
        initialDamage: float,
        calculationMethod: CalculationMethod,
        topLayerType: TopLayerType,
    ):
        self.XPosition = xPosition
        self.InitialDamage = initialDamage
        self.CalculationMethod = calculationMethod
        self.TopLayerType = topLayerType


class AsphaltOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        xPosition: float,
        beginDamage: float,
        breakStrentAsphalt: float,
        springConstantSoil: float,
        topLayerThickness: float,
        topLayerStiffnessModulus: float,
    ):
        super().__init__(
            xPosition,
            beginDamage,
            CalculationMethod.AsphaltWaveImpact,
            TopLayerType.WAB,
        )
        self.FlexuralStrent = breakStrentAsphalt
        self.SoilElasticity = springConstantSoil
        self.TopLayerThickness = topLayerThickness
        self.TopLayerElasticModulus = topLayerStiffnessModulus
        self.SubLayerThickness = None
        self.SubLayerElasticModulus = None
        self.FatigueAlpha = None
        self.FatigueBeta = None
        self.TopLayerStiffnessRelationNu = None


class NordicStoneOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        xPosition: float,
        beginDamage: float,
        topLayerThickness: float,
        relativeDensity: float,
    ):
        super().__init__(
            xPosition,
            beginDamage,
            CalculationMethod.NaturalStone,
            TopLayerType.NordicStone,
        )
        self.TopLayerThickness = topLayerThickness
        self.RelativeDensity = relativeDensity


class GrassWaveImpactOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self, xPosition: float, beginDamage: float, topLayerType: TopLayerType
    ):
        super().__init__(
            xPosition, beginDamage, CalculationMethod.GrassWaveImpact, topLayerType
        )


class GrassOvertoppingOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        xPosition: float,
        beginDamage: float,
        topLayerType: TopLayerType,
        alphaM: float = 1.0,
        alphaS: float = 1.0,
    ):
        super().__init__(
            xPosition, beginDamage, CalculationMethod.GrassWaveOvertopping, topLayerType
        )
        self.IncreasedLoadTransitionAlphaM = alphaM
        self.ReducedStrengthTransitionAlphaS = alphaS
