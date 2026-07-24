"""Public API for Mlecchita-X."""
from .cipher import encrypt, decrypt, encrypt_text, decrypt_text
from .keys import generate_key, load_key, save_key
from .exceptions import AuthenticationError, InvalidContainerError

__version__ = "0.2.1"

__all__ = [
    "encrypt", "decrypt", "encrypt_text", "decrypt_text",
    "generate_key", "load_key", "save_key",
    "AuthenticationError", "InvalidContainerError",
]
