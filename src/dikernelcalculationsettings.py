from toplayertypes import TopLayerType
from calculationmethods import CalculationMethod


class TopLayerSettings:
    def __init__(self, type: TopLayerType):
        self.top_layer_type: TopLayerType = type


class AsphaltTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.WAB)
        self.stiffness_ratio_nu: float = None
        self.fatigue_asphalt_alpha: float = None
        self.fatigue_asphalt_beta: float = None


class GrasCoverOvertoppingTopLayerSettings(TopLayerSettings):
    def __init__(self, topLayerType: TopLayerType):
        super().__init__(topLayerType)
        self.critical_cumulative_overload: float = None
        self.critical_front_velocity: float = None


class GrassCoverWaveImpactTopLayerSettings(TopLayerSettings):
    def __init__(self, type: TopLayerType):
        super().__init__(type)
        self.stance_time_line_a: float = None
        self.stance_time_line_b: float = None
        self.stance_time_line_c: float = None


class NaturalStoneTopLayerSettings(TopLayerSettings):
    def __init__(self):
        super().__init__(TopLayerType.NordicStone)
        self.stability_plunging_a: float = None
        self.stability_plunging_b: float = None
        self.stability_plunging_c: float = None
        self.stability_plunging_n: float = None
        self.stability_surging_a: float = None
        self.stability_surging_b: float = None
        self.stability_surging_c: float = None
        self.stability_surging_n: float = None
        self.xib: float = None


class CalculationSettings:
    def __init__(
        self, calculationMethod: CalculationMethod, topLayers: list[TopLayerSettings]
    ):
        self.CalculationMethod: CalculationMethod = calculationMethod
        self.failure_number: float = None
        self.top_layers_settings: list[TopLayerSettings] = topLayers


class AsphaltCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.AsphaltWaveImpact, topLayers)
        self.density_of_water: float = None
        self.factor_ctm: float = None
        self.impact_number_c: float = None
        self.width_factors: list[float, float] = None
        self.depth_factors: list[float, float] = None
        self.impact_factors: list[float, float] = None


class GrassWaveOvertoppingCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveOvertopping, topLayers)
        self.acceleration_alpha_a_for_crest: float = None
        self.acceleration_alpha_a_for_inner_slope: float = None
        self.fixed_number_of_waves: int = None
        self.front_velocity_c_wo: float = None
        self.factor_ctm: float = None
        self.DikeHeight: float = None


class GrassWaveImpactCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.GrassWaveImpact, topLayers)
        self.loading_upper_limit: float = None
        self.loading_lower_limit: float = None
        self.wave_angle_impact_n: float = None
        self.wave_angle_impact_q: float = None
        self.wave_angle_impact_r: float = None
        self.te_max: float = None
        self.te_min: float = None


class NaturalStoneCalculationSettings(CalculationSettings):
    def __init__(self, topLayers: list[TopLayerSettings]):
        super().__init__(CalculationMethod.NaturalStone, topLayers)
        self.distance_maximum_wave_elevation_a: float = None
        self.distance_maximum_wave_elevation_b: float = None
        self.slope_upper_level: float = None
        self.sLope_lower_level: float = None
        self.normative_width_of_wave_impact_a: float = None
        self.normative_width_of_wave_impact_b: float = None
        self.upper_limit_loading_a: float = None
        self.upper_limit_loading_b: float = None
        self.upper_limit_loading_c: float = None
        self.lower_limit_loading_a: float = None
        self.lower_limit_loading_b: float = None
        self.lower_limit_loading_c: float = None
        self.wave_angle_impact_beta_max: float = None
