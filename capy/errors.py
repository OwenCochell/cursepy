"""
CAPY excpetions and errors
"""


class CapyBaseException(BaseException):

    """
    CFABaseException - Base exception all CFA excaptions will inherit!

    This will NOT be raised by any CFA component!
    This exception can be used to identify the custom CFA exceptions.
    """

    pass


class ProtocolMismatch(CapyBaseException):
    """
    Exception raised when a protocol mismatch has occurred.

    A 'protocol mismatch' is when a handler attempts to assign
    a protocol object that does not match the protocol object 
    currently assigned to the handler name.
    """

    pass


class HandlerRaise(CapyBaseException):
    """
    Exception raised when the 'RaiseHandler' is called.

    This exception will not be raised anywhere else!
    """

    pass
