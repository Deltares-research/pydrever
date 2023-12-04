class OutputLocation:
    def __init__(self, xPosition: float, initialDamage: float, calculationMethod: str, topLayerType: str):
        self.XPosition = xPosition
        self.InitialDamage = initialDamage
        self.CalculationMethod = (calculationMethod,)
        self.TopLayerType = topLayerType


class AsphaltOutputLocation(OutputLocation):
    def __init__(
        self,
        xPosition: float,
        beginDamage: float,
        breakStrentAsphalt: float,
        springConstantSoil: float,
        topLayerThickness: float,
        topLayerStiffnessModulus: float,
    ):
        super().__init__(xPosition, beginDamage, "asfaltGolfklap", "waterbouwAsfaltBeton")
        self.FlexuralStrent = breakStrentAsphalt
        self.SoilElasticity = springConstantSoil
        self.TopLayerThickness = topLayerThickness
        self.TopLayerElasticModulus = topLayerStiffnessModulus
        self.SubLayerThickness = None
        self.SubLayerElasticModulus = None
        self.FatigueAlpha = None
        self.FatigueBeta = None
        self.TopLayerStiffnessRelationNu = None


class NordicStoneOutputLocation(OutputLocation):
    def __init__(self, xPosition: float, beginDamage: float, topLayerThickness: float, relativeDensity: float):
        super().__init__(xPosition, beginDamage, "natuursteen", "noorseSteen")
        self.TopLayerThickness = topLayerThickness
        self.RelativeDensity = relativeDensity


class GrassWaveImpactOutputLocation(OutputLocation):
    def __init__(self, xPosition: float, beginDamage: float):
        super().__init__(xPosition, beginDamage, "grasGolfklap", "grasGeslotenZode")


class GrassOvertoppingOutputLocation(OutputLocation):
    def __init__(self, xPosition: float, beginDamage: float, alphaM: float = 1.0, alphaS: float = 1.0):
        super().__init__(xPosition, beginDamage, "grasGolfoverslag", "grasGeslotenZode")
        self.AlphaM = alphaM
        self.AlphaS = alphaS
