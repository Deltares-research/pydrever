from __future__ import annotations
from dikerneloutputlocations import OutputLocationSpecification
from dikernelcalculationsettings import CalculationSettings
import numpy as numpy


class DikeSchematization:
    def __init__(
        self,
        xPositions: list[float],
        zPositions: list[float],
        roughnesses: list[float],
        xOuterToe: float,
        xOuterCrest: float,
    ):
        """Contructor for a schematization of a dike profile.

        Args:
            xPositions (list[float]): list of cross-shore positions
            zPositions (list[float]): list of dike heights in meter correspoinding to the cross-shore positions. zPositions needs to be of the samen length as xPositions
            roughnesses (list[float]): a list of roughness coefficients per dike segment. By definition the length of this list is equal to the length of xPositions - 1
            xOuterToe (float): The cross-shore location of the toe of the dike at the outer slope
            xOuterCrest (float): The cross-shore location of the (outer) crest of the dike
        """
        self.XPositions: list[float] = xPositions
        self.ZPositions: list[float] = zPositions
        self.Roughnesses: list[float] = roughnesses
        self.OuterToe: float = xOuterToe
        self.OuterCrest: float = xOuterCrest
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
        waveDirections: list[float],
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
            or nrTimeSteps - 1 != len(waveDirections)
        ):
            raise Exception(
                "length of the specified series for waterlevels, wave heights, wave periods and wave angles needs to be exactly 1 less than the length of the specified time steps."
            )

        self.TimeSteps = timeSteps
        self.WaterLevels = waterLevels
        self.WaveHeights = waveHeights
        self.WavePeriods = wavePeriods
        self.WaveDirections = waveDirections


class DikernelInput:
    def __init__(
        self,
        dikeOrientation: float,
        hydraulicInput: HydraulicInput,
        dikeSchematization: DikeSchematization,
    ):
        """Constructor for the DikernelInput class.

        Args:
            dikeOrientation (float): orientation of the dike normal
            hydraulicInput (HydraulicInput): object containing the hydraulics input
            dikeSchematization (DikeSchematization): object containing the dike schematization
        """
        self.DikeOrientation: float = dikeOrientation
        self.HydraulicInput: HydraulicInput = hydraulicInput
        self.DikeSchematization: DikeSchematization = dikeSchematization
        self.OutputLocations: list[OutputLocationSpecification] = None
        self.Settings: list[CalculationSettings] = None
        self.StartTime: float = None
        self.OutputTimeSteps: list[float] = None

    def getruntimesteps(self) -> list[float]:
        runTimeSteps = self.HydraulicInput.TimeSteps
        if self.OutputTimeSteps is not None:
            runTimeSteps = numpy.union1d(runTimeSteps, self.OutputTimeSteps).tolist()

        if self.StartTime is not None:
            runTimeSteps = list(
                timeStep
                for timeStep in numpy.union1d(runTimeSteps, [self.StartTime])
                if timeStep >= self.StartTime
            )
        return runTimeSteps

    def getruninput(self) -> DikernelInput:
        timeSteps = self.HydraulicInput.TimeSteps
        runTimeSteps = self.getruntimesteps()
        runWaterLevels = self.__interpolatetimeseries(
            timeSteps, self.HydraulicInput.WaterLevels, runTimeSteps
        )
        runWaveHeights = self.__interpolatetimeseries(
            timeSteps, self.HydraulicInput.WaveHeights, runTimeSteps
        )
        runWavePeriods = self.__interpolatetimeseries(
            timeSteps, self.HydraulicInput.WavePeriods, runTimeSteps
        )
        runWaveDirections = self.__interpolatetimeseries(
            timeSteps, self.HydraulicInput.WaveDirections, runTimeSteps
        )
        runHydraulics = HydraulicInput(
            runTimeSteps,
            runWaterLevels,
            runWaveHeights,
            runWavePeriods,
            runWaveDirections,
        )
        runInput = DikernelInput(
            self.DikeOrientation, runHydraulics, self.DikeSchematization
        )
        runInput.OutputLocations = self.OutputLocations
        runInput.Settings = self.Settings
        return runInput

    @staticmethod
    def __interpolatetimeseries(
        timeSteps: list[float], values: list[float], targetTimeSteps: list[float]
    ) -> list[float]:
        iargs = 1
        itarget = 1
        targetValues = list[float]()
        while itarget < len(targetTimeSteps):
            if (
                targetTimeSteps[itarget] > timeSteps[iargs]
                and iargs < len(timeSteps) - 1
            ):
                iargs = iargs + 1
                continue
            targetValues.append(values[iargs - 1])
            itarget = itarget + 1

        return targetValues
