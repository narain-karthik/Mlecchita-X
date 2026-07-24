from pathlib import Path
import secrets

KEY_SIZE = 32

def generate_key() -> bytes:
    return secrets.token_bytes(KEY_SIZE)

def save_key(path: str, key: bytes) -> None:
    if len(key) != KEY_SIZE:
        raise ValueError("Mlecchita-X keys must be exactly 32 bytes.")
    Path(path).write_bytes(key)

def load_key(path: str) -> bytes:
    key = Path(path).read_bytes()
    if len(key) != KEY_SIZE:
        raise ValueError("Key file must contain exactly 32 bytes.")
    return key
