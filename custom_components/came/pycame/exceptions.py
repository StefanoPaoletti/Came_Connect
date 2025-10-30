"""Exceptions for Came Connect.

Versione ottimizzata da Stefano Paoletti
Based on original work by Danny Mauro (Den901)
"""
from typing import Optional


class ETIDomoError(Exception):
    """Generic Came Connect exception."""

    def __init__(self, status: str, errno: Optional[int] = None):
        """Initialize Came Connect error."""
        super().__init__(status)
        self.status = status
        self.errno = errno


class ETIDomoConnectionError(ETIDomoError):
    """Came Connect connection exception."""


class ETIDomoConnectionTimeoutError(ETIDomoConnectionError, TimeoutError):
    """Came Connect connection timeout exception."""


class ETIDomoUnmanagedDeviceError(ETIDomoError):
    """Came Connect exception for unmanaged device."""

    def __init__(
        self, status: str = "This device is unmanageable", errno: Optional[int] = None
    ):
        """Initialize unmanaged device error."""
        super().__init__(status, errno)
