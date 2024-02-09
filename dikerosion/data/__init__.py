"""
 Copyright (C) Stichting Deltares 2024. All rights reserved.
 
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
