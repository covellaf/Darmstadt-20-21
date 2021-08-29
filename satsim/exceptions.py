
class InvalidComponentState(Exception):
    pass


class InvalidSimulatorState(Exception):
    pass


class InvalidEventTime(Exception):
    pass


class InvalidCycleTme(Exception):
    pass


class InvalidEventId(Exception):
    pass


class InvalidEventName(Exception):
    pass


class EntryPointAlreadySubscribed(Exception):
    pass


class EntryPointNotSubscribed(Exception):
    pass

# as defined on page 39, 5.2.1 c. :
class InvalidObjectName(Exception):
    pass


# do we need to define the exception class?
# class Exception():
    # def __init__(self, description, name, message, sender=None)
    # # the sender needs to be specified if the exception originates from a SMP Object
