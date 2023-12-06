from dikerneloutputlocations import OutputLocation
from dikernelcalculationsettings import CalculationSettings


class DikeSchematization:
    def __init__(self, xPositions: list[float], zPositions: list[float], roughnesses: list[float]):
        """Contructor for a schematization of a dike profile.

        Args:
            xPositions (list[float]): list of cross-shore positions
            zPositions (list[float]): list of dike heights in meter correspoinding to the cross-shore positions. zPositions needs to be of the samen length as xPositions
            roughnesses (list[float]): a list of roughness coefficients per dike segment. By definition the length of this list is equal to the length of xPositions - 1
        """
        self.XPositions: list[float] = xPositions
        self.ZPositions: list[float] = zPositions
        self.Roughnesses: list[float] = roughnesses
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
        """Constructor for the hydraulic input.

        Args:
            timeSteps (list[float]): list of timesteps.
            waterLevels (list[float]): list of waterlevels
            waveHeights (list[float]): list of significant wave heights (Hs)
            wavePeriods (list[float]): list of wave periods
            waveAngles (list[float]): list of wave angles
        Raises:
            Exception: In case the length of either the specified water level series, the wave heights, wave periods or wave angles is not exactly 1 less than the length of the specified time steps.
        """
        nrTimeSteps = len(timeSteps)
        if (
            nrTimeSteps - 1 != len(waterLevels)
            or nrTimeSteps - 1 != len(waveHeights)
            or nrTimeSteps - 1 != len(wavePeriods)
            or nrTimeSteps - 1 != len(waveAngles)
        ):
            raise Exception(
                "length of the specified series for waterlevels, wave heights, wave periods and wave angles needs to be exactly 1 less than the length of the specified time steps."
            )

        self.TimeSteps = timeSteps
        self.WaterLevels = waterLevels
        self.WaveHeights = waveHeights
        self.WavePeriods = wavePeriods
        self.WaveDirections = waveAngles


class DikernelInput:
    def __init__(self, dikeOrientation: float, hydraulicInput: HydraulicInput, dikeSchematization: DikeSchematization):
        """Constructor for the DikernelInput class.

        Args:
            dikeOrientation (float): orientation of the dike normal
            hydraulicInput (HydraulicInput): object containing the hydraulics input
            dikeSchematization (DikeSchematization): object containing the dike schematization
        """
        self.DikeOrientation: float = dikeOrientation
        self.HydraulicInput: HydraulicInput = hydraulicInput
        self.DikeSchematization: DikeSchematization = dikeSchematization
        self.OutputLocations: list[OutputLocation] = None
        self.Settings: list[CalculationSettings] = None
