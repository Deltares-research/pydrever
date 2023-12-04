from dikerneloutputlocations import OutputLocation
from dikernelcalculationsettings import CalculationSettings


class DikernelInput:
    def __init__(self):
        self.DikeOrientation: float = None
        self.HydraulicInput: HydraulicInput = None
        self.DikeSchematization: DikeSchematization = None
        self.OutputLocations: list[OutputLocation] = None
        self.Settings: list[CalculationSettings] = None


class DikeSchematization:
    def __init__(self):
        self.XPositions: list[float] = None
        self.ZPositions: list[float] = None
        self.Roughnesses: list[float] = None
        self.OuterToe: float = None
        self.OuterCrest: float = None
        self.CrestOuterBerm: float = None
        self.NotchOuterBerm: float = None
        self.InnerCrest: float = None
        self.InnerToe: float = None


class HydraulicInput:
    def __init__(
        self,
        timeSteps: list[float],
        waterLevels: list[float],
        waveHeights: list[float],
        wavePeriods: list[float],
        waveAngles: list[float],
    ):
        self.TimeSteps = timeSteps
        self.WaterLevels = waterLevels
        self.WaveHeights = waveHeights
        self.WavePeriods = wavePeriods
        self.WaveDirections = waveAngles
