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

from enum import Enum


class TimeDependentOutputQuantity(Enum):
    DamageDevelopment = "damage_development"  # All
    DamageIncrement = "damage_increment"  # All
    MaximumPeakStress = "maximum_peak_stress"  # Asphalt
    AverageNumberOfWaves = "average_number_of_waves"  # Asphalt, GrassOvertopping
    VerticalDistanceWaterLevelElevation = (
        "vertical_distance_water_level_elevation"  # GrassOvertopping
    )
    RepresentativeWaveRunup2P = "representative_wave_runup_2p"  # GrassOvertopping
    CumulativeOverload = "cumulative_overload"  # GrassOvertopping
    LoadingRevetment = "loading_revetment"  # GrassWaveImpact, NaturalStone
    UpperLimitLoading = "upper_limit_loading"  # GrassWaveImpact, NaturalStone
    LowerLimitLoading = "lower_limit_loading"  # GrassWaveImpact, NaturalStone
    WaveAngle = "wave_angle"  # GrassWaveImpact, NaturalStone
    WaveAngleImpact = "wave_angle_impact"  # GrassWaveImpact, NaturalStone
    WaveHeightImpact = "wave_height_impactt"  # GrassWaveImpact
    OuterSlope = "outer_slope"  # NaturalStone
    SlopeUpperLevel = "slope_upper_level"  # NaturalStone
    SlopeUpperPosition = "slope_upper_position"  # NaturalStone
    SlopeLowerLevel = "slope_lower_level"  # NaturalStone
    SlopeLowerPosition = "slope_lower_position"  # NaturalStone
    SurfSimilatiryParameter = "surf_similarity_parameter"  # NaturalStone
    WaveSteepnessDeepWater = "wave_steepness_deep_water"  # NaturalStone
    DepthMaximumWaveLoad = "depth_maximum_wave_load"  # NaturalStone
    DistanceMaximumWaveElevation = "distance_maximum_wave_elevation"  # NaturalStone
    NormativeWidthOfWaveImpact = "normative_width_of_wave_impact"  # NaturalStone
    HydraulicLoad = "hydraulic_load"  # NaturalStone
    ReferenceTimeDegradation = "reference_time_degradation"  # NaturalStone
    ReferenceDegradation = "reference_degradation"  # NaturalStone
