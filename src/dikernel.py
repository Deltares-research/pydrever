import ctypes
import os


class DiKernel:
    calculatorDll = ctypes.cdll.LoadLibrary(
        os.getcwd() + "\src\dikerneldll\DiKErnel.Core.dll"
    )
    inputDll = ctypes.cdll.LoadLibrary(
        os.getcwd() + "\src\dikerneldll\DiKErnel.Integration.dll"
    )

    def run(self, dikernelInput):
        self.calculatorDll.printf()
        # calculator = self.calculatorDll.Calculator(dikernelInput)
        # calculator.WaitForCompletion()
        # return calculator.Result
