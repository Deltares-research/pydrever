import clr  # This reguires the package pythonnet to be added to the environment.

# TODO: How to dynamically locate and add these dll's?
clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Integration.dll")
clr.AddReference("C:/src/dikerosion-pyton/src/dikerneldll/DiKErnel.Core.dll")

from System import Double, ValueTuple
from System.Collections.Generic import List

from DiKErnel.Core import Calculator, Validator
from DiKErnel.Core.Data import (
    LocationDependentOutput,
    CalculationOutput,
    CharacteristicPointType,
    ValidationResultType,
    CalculationState,
)

from DiKErnel.Integration.Data.AsphaltRevetmentWaveImpact import (
    AsphaltRevetmentWaveImpactLocationDependentOutput,
    AsphaltRevetmentWaveImpactLocationConstructionProperties,
    AsphaltRevetmentTopLayerType,
)
from DiKErnel.Integration.Data.GrassRevetment import GrassRevetmentTopLayerType
from DiKErnel.Integration.Data.GrassRevetmentOvertopping import (
    GrassRevetmentOvertoppingLocationDependentOutput,
    GrassRevetmentOvertoppingLocationConstructionProperties,
)
from DiKErnel.Integration.Data.GrassRevetmentWaveImpact import (
    GrassRevetmentWaveImpactLocationDependentOutput,
    GrassRevetmentWaveImpactLocationConstructionProperties,
)
from DiKErnel.Integration.Data.NaturalStoneRevetment import (
    NaturalStoneRevetmentLocationDependentOutput,
    NaturalStoneRevetmentLocationConstructionProperties,
    NaturalStoneRevetmentTopLayerType,
)

from DiKErnel.Integration.Data.GrassRevetmentWaveRunup import (
    GrassRevetmentWaveRunupRayleighLocationDependentOutput,
    GrassRevetmentWaveRunupLocationConstructionProperties,
)

from DiKErnel.Integration import CalculationInputBuilder
