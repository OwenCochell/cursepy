"""
cursepy exceptions and errors
"""


class CurseBaseException(BaseException):
    """
    CFABaseException - Base exception all CFA exceptions will inherit!

    This will NOT be raised by any CFA component!
    This exception can be used to identify the custom CFA exceptions.
    """

    pass


class ProtocolMismatch(CurseBaseException):
    """
    Exception raised when a protocol mismatch has occurred.

    A 'protocol mismatch' is when a handler attempts to assign
    a protocol object that does not match the protocol object 
    currently assigned to the handler name.
    """

    pass


class HandlerRaise(CurseBaseException):
    """
    Exception raised when the 'RaiseHandler' is called.

    This exception will not be raised anywhere else!
    """

    pass


class HandlerNotImplemented(CurseBaseException):
    """
    Exception raised when this handler implementation is not implemented.
    
    Usually, this occurs when no handlers are attached to the given operation.
    """
    
    pass


class HandlerNotSupported(CurseBaseException):
    """
    Exception raised when an operation is not supported by a handler.
    
    For example, the CF handlers do not support getting info on a specific category.
    Because of this, each time that handler is called,
    this exception will be raised.
    """
    
    pass
