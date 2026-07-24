class MlecchitaXError(Exception):
    """Base exception."""

class AuthenticationError(MlecchitaXError):
    """Wrong key or modified ciphertext."""

class InvalidContainerError(MlecchitaXError):
    """Malformed or unsupported encrypted container."""
