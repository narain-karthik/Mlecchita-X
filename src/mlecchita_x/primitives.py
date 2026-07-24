import hashlib
import hmac

ROUNDS = 12  # Experimental default, NOT a proven security margin.

def _prf_block(key: bytes, nonce: bytes, label: bytes, round_no: int, counter: int) -> bytes:
    msg = (
        b"MX02|" + nonce + b"|" + label + b"|" +
        round_no.to_bytes(2, "big") + b"|" + counter.to_bytes(8, "big")
    )
    return hmac.new(key, msg, hashlib.sha256).digest()

def derive_bytes(key: bytes, nonce: bytes, label: bytes, round_no: int, length: int) -> bytes:
    out = bytearray()
    counter = 0
    while len(out) < length:
        out.extend(_prf_block(key, nonce, label, round_no, counter))
        counter += 1
    return bytes(out[:length])

class PRFStream:
    def __init__(self, key: bytes, nonce: bytes, label: bytes, round_no: int):
        self.key = key
        self.nonce = nonce
        self.label = label
        self.round_no = round_no
        self.counter = 0
        self.buffer = bytearray()

    def _refill(self):
        self.buffer.extend(
            _prf_block(self.key, self.nonce, self.label, self.round_no, self.counter)
        )
        self.counter += 1

    def read(self, n: int) -> bytes:
        while len(self.buffer) < n:
            self._refill()
        out = bytes(self.buffer[:n])
        del self.buffer[:n]
        return out

    def randbelow(self, upper: int) -> int:
        if upper <= 0:
            raise ValueError("upper must be positive")
        nbytes = max(1, (upper.bit_length() + 7) // 8)
        space = 1 << (8 * nbytes)
        limit = space - (space % upper)
        while True:
            candidate = int.from_bytes(self.read(nbytes), "big")
            if candidate < limit:
                return candidate % upper

def fisher_yates(n: int, stream: PRFStream) -> list[int]:
    values = list(range(n))
    for i in range(n - 1, 0, -1):
        j = stream.randbelow(i + 1)
        values[i], values[j] = values[j], values[i]
    return values

def sbox(key: bytes, nonce: bytes, round_no: int):
    table = fisher_yates(256, PRFStream(key, nonce, b"sbox", round_no))
    inverse = [0] * 256
    for i, value in enumerate(table):
        inverse[value] = i
    return table, inverse

def position_permutation(key: bytes, nonce: bytes, round_no: int, size: int):
    table = fisher_yates(size, PRFStream(key, nonce, b"position", round_no))
    inverse = [0] * size
    for new_pos, old_pos in enumerate(table):
        inverse[old_pos] = new_pos
    return table, inverse

def substitute(data: bytes, table: list[int]) -> bytes:
    return bytes(table[b] for b in data)

def permute(data: bytes, table: list[int]) -> bytes:
    return bytes(data[old_pos] for old_pos in table)

def inverse_permute(data: bytes, inverse: list[int]) -> bytes:
    out = bytearray(len(data))
    for old_pos, new_pos in enumerate(inverse):
        out[old_pos] = data[new_pos]
    return bytes(out)

def diffuse(data: bytes) -> bytes:
    out = bytearray(data)
    for i in range(1, len(out)):
        out[i] ^= out[i - 1]
    return bytes(out)

def inverse_diffuse(data: bytes) -> bytes:
    out = bytearray(data)
    for i in range(len(out) - 1, 0, -1):
        out[i] ^= out[i - 1]
    return bytes(out)

def xor_bytes(data: bytes, mask: bytes) -> bytes:
    return bytes(a ^ b for a, b in zip(data, mask))

def round_key(key: bytes, nonce: bytes, round_no: int, size: int) -> bytes:
    return derive_bytes(key, nonce, b"round-key", round_no, size)
