class DikernelOutputLocation:
    def __init__(self, timeOfFailure, damageDevelopment):
        self.__timeOfFailure = timeOfFailure
        self.__damageDevelopment = damageDevelopment
        pass

    @property
    def Failed(self) -> bool:
        return self.__timeOfFailure is not None

    @property
    def TimeOfFailure(self) -> float:
        return self.__timeOfFailure

    @property
    def DamageDevelopment(self) -> list[float]:
        return self.__damageDevelopment
