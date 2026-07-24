import base64
import hashlib
import hmac
import secrets

from .exceptions import AuthenticationError, InvalidContainerError
from .primitives import (
    ROUNDS, sbox, position_permutation, substitute, permute,
    inverse_permute, diffuse, inverse_diffuse, xor_bytes,
    round_key, derive_bytes,
)

MAGIC = b"MX02"
NONCE_SIZE = 16
TAG_SIZE = 32
HEADER_SIZE = 4 + NONCE_SIZE + 8

def _validate_key(key: bytes) -> None:
    if not isinstance(key, (bytes, bytearray)) or len(key) != 32:
        raise ValueError("Key must be exactly 32 bytes.")

def _auth_key(key: bytes, nonce: bytes) -> bytes:
    return derive_bytes(key, nonce, b"auth-key", 0, 32)

def _encrypt_core(data: bytes, key: bytes, nonce: bytes) -> bytes:
    state = bytes(data)
    for r in range(ROUNDS):
        box, _ = sbox(key, nonce, r)
        state = substitute(state, box)
        positions, _ = position_permutation(key, nonce, r, len(state))
        state = permute(state, positions)
        state = diffuse(state)
        state = xor_bytes(state, round_key(key, nonce, r, len(state)))
    return state

def _decrypt_core(data: bytes, key: bytes, nonce: bytes) -> bytes:
    state = bytes(data)
    for r in range(ROUNDS - 1, -1, -1):
        state = xor_bytes(state, round_key(key, nonce, r, len(state)))
        state = inverse_diffuse(state)
        _, inverse_positions = position_permutation(key, nonce, r, len(state))
        state = inverse_permute(state, inverse_positions)
        _, inverse_box = sbox(key, nonce, r)
        state = substitute(state, inverse_box)
    return state

def encrypt(data: bytes, key: bytes) -> bytes:
    _validate_key(key)
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    nonce = secrets.token_bytes(NONCE_SIZE)
    ciphertext = _encrypt_core(data, key, nonce)
    header = MAGIC + nonce + len(data).to_bytes(8, "big")
    tag = hmac.new(_auth_key(key, nonce), header + ciphertext, hashlib.sha256).digest()
    return header + ciphertext + tag

def decrypt(blob: bytes, key: bytes) -> bytes:
    _validate_key(key)
    if not isinstance(blob, bytes) or len(blob) < HEADER_SIZE + TAG_SIZE:
        raise InvalidContainerError("Invalid Mlecchita-X container.")
    if blob[:4] != MAGIC:
        raise InvalidContainerError("Unsupported or invalid Mlecchita-X container.")

    nonce = blob[4:20]
    declared_len = int.from_bytes(blob[20:28], "big")
    ciphertext = blob[28:-TAG_SIZE]
    tag = blob[-TAG_SIZE:]
    expected = hmac.new(_auth_key(key, nonce), blob[:28] + ciphertext, hashlib.sha256).digest()

    if not hmac.compare_digest(tag, expected):
        raise AuthenticationError("Authentication failed: wrong key or modified ciphertext.")
    if declared_len != len(ciphertext):
        raise InvalidContainerError("Invalid declared plaintext length.")

    plaintext = _decrypt_core(ciphertext, key, nonce)
    if len(plaintext) != declared_len:
        raise InvalidContainerError("Decrypted length validation failed.")
    return plaintext

def encrypt_text(text: str, key: bytes) -> str:
    raw = encrypt(text.encode("utf-8"), key)
    return "MX02:" + base64.urlsafe_b64encode(raw).decode("ascii")

def decrypt_text(token: str, key: bytes) -> str:
    if not token.startswith("MX02:"):
        raise InvalidContainerError("Text token must start with MX02:")
    try:
        raw = base64.urlsafe_b64decode(token[5:].encode("ascii"))
    except Exception as exc:
        raise InvalidContainerError("Invalid Base64 token.") from exc
    return decrypt(raw, key).decode("utf-8")
