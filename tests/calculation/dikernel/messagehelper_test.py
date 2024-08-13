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
