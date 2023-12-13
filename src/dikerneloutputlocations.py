from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod


class OutputLocationSpecification:
    def __init__(
        self,
        x_position: float,
        initial_damage: float,
        calculation_method: CalculationMethod,
        top_layer_type: TopLayerType,
    ):
        self.x_position = x_position
        self.initial_damage = initial_damage
        self.calculation_method = calculation_method
        self.top_layer_type = top_layer_type


class AsphaltOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        break_strent_asphalt: float,
        spring_constant_soil: float,
        top_layer_thickness: float,
        top_layer_stiffness_modulus: float,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.AsphaltWaveImpact,
            TopLayerType.WAB,
        )
        self.flexural_strent = break_strent_asphalt
        self.soil_elasticity = spring_constant_soil
        self.top_layer_thickness = top_layer_thickness
        self.top_layer_elastic_modulus = top_layer_stiffness_modulus
        self.sub_layer_thickness = None
        self.sub_layer_elastic_modulus = None
        self.fatigue_alpha = None
        self.fatigue_beta = None
        self.top_layer_stiffness_relation_nu = None


class NordicStoneOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        top_layer_thickness: float,
        relative_density: float,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.NaturalStone,
            TopLayerType.NordicStone,
        )
        self.top_layer_thickness = top_layer_thickness
        self.relative_density = relative_density


class GrassWaveImpactOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self, x_position: float, begin_damage: float, top_layer_type: TopLayerType
    ):
        super().__init__(
            x_position, begin_damage, CalculationMethod.GrassWaveImpact, top_layer_type
        )


class GrassOvertoppingOutputLocationSpecification(OutputLocationSpecification):
    def __init__(
        self,
        x_position: float,
        begin_damage: float,
        top_layer_type: TopLayerType,
        alpha_m: float = 1.0,
        alpha_s: float = 1.0,
    ):
        super().__init__(
            x_position,
            begin_damage,
            CalculationMethod.GrassWaveOvertopping,
            top_layer_type,
        )
        self.increased_load_transition_alpha_m = alpha_m
        self.increased_load_transition_alpha_s = alpha_s
