from dikerosion.data.calculationmethods import CalculationMethod
from dikerosion.data.toplayertypes import TopLayerType
from dikerosion.data.quantities import TimeDependentOutputQuantity

from dikerosion.data.dikernelcalculationsettings import (
    AsphaltCalculationSettings,
    AsphaltTopLayerSettings,
    CalculationSettings,
    GrasCoverCumulativeOverloadTopLayerSettings,
    GrassCoverWaveImpactTopLayerSettings,
    GrassWaveImpactCalculationSettings,
    GrassWaveOvertoppingCalculationSettings,
    GrassWaveRunupCalculationSettings,
    NaturalStoneCalculationSettings,
    NaturalStoneTopLayerSettings,
    TopLayerSettings,
)
from dikerosion.data.dikernelinput import (
    DikernelInput,
    DikeSchematization,
    HydrodynamicConditions,
)
from dikerosion.data.dikerneloutput import (
    DikernelOutputLocation,
    AsphaltWaveImpactOutputLocation,
    GrassOvertoppingOutputLocation,
    GrassWaveImpactOutputLocation,
    GrassWaveRunupOutputLocation,
    NaturalStoneOutputLocation,
)
from dikerosion.data.dikerneloutputspecification import (
    AsphaltOutputLocationSpecification,
    GrassOvertoppingOutputLocationSpecification,
    GrassWaveImpactOutputLocationSpecification,
    GrassWaveRunupOutputLocationSpecification,
    NordicStoneOutputLocationSpecification,
    OutputLocationSpecification,
)
