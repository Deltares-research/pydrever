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

from pydrever.calculation._dikernel._dikernelcreferences import *
import pydrever.calculation._dikernel._messagehelper as _message_helper

from DiKErnel.Util import Event, SimpleResult


def test_message_helper_parses_error_messages():
    c_events = List[Event]()
    c_events.Add(Event("test", EventType.Error))
    c_result = SimpleResult(False, c_events)

    warnings, errors = _message_helper.parse_messages(c_result)
    assert len(warnings) == 0
    assert len(errors) == 1
    assert errors[0] == "test"


def test_message_helper_parses_warning_messages():
    c_events = List[Event]()
    c_events.Add(Event("test", EventType.Warning))
    c_result = SimpleResult(False, c_events)

    warnings, errors = _message_helper.parse_messages(c_result)
    assert len(warnings) == 1
    assert len(errors) == 0
    assert warnings[0] == "test"
