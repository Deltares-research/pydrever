"""
 Copyright (C) Stichting Deltares 2023-2024. All rights reserved.
 
 This file is part of the dikernel-python toolbox.
 
 This program is free software; you can redistribute it and/or modify it under the terms of
 the GNU Lesser General Public License as published by the Free Software Foundation; either
 version 3 of the License, or (at your option) any later version.
 
 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 See the GNU Lesser General Public License for more details.
 
 You should have received a copy of the GNU Lesser General Public License along with this
 program; if not, see <https://www.gnu.org/licenses/>.
 
 All names, logos, and references to "Deltares" are registered trademarks of Stichting
 Deltares and remain full property of Stichting Deltares at all times. All rights reserved.
"""

"""
This file adds all relevent C# classes as import. 
"""

import clr
import os


dll_base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dikerneldll")
clr.AddReference(os.path.join(dll_base_path, "DiKErnel.Core.dll"))
clr.AddReference(os.path.join(dll_base_path, "DiKErnel.Integration.dll"))


from System import Double, ValueTuple
from System.Collections.Generic import List

from DiKErnel.Core import Calculator, Validator
from DiKErnel.Core.Data import (
    LocationDependentOutput,
    CalculationOutput,
    CharacteristicPointType,
    ValidationResultType,
    CalculationState,
    ICalculationInput,
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
