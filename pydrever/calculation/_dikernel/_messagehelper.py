from pydrever.calculation._dikernel._dikernelcreferences import *


def parse_messages(c_output):
    if c_output is None:
        return [], []
    warnings = list(i.Message for i in c_output.Events if i.Type == EventType.Warning)
    errors = list(i.Message for i in c_output.Events if i.Type == EventType.Error)
    return warnings, errors
