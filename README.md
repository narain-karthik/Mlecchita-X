# Mlecchita-X

**Experimental Python cryptography research library inspired by the historical concept of Mlecchita Vikalpa.**

Author & Maintainer: **Narain Karthik J**  
Current version: **0.2.1**  
Python: **3.10+**  
License: **MIT**

> **Important:** Mlecchita-X is educational/research software. It has not undergone sufficient independent cryptanalysis and must not be used to protect sensitive production data.

## Quick start

Install from PyPI:

```cmd
python -m pip install --upgrade mlecchita-x
```

Python:

```python
from mlecchita_x import generate_key, encrypt_text, decrypt_text

key = generate_key()
token = encrypt_text("Vanakkam", key)
print(token)
print(decrypt_text(token, key))
```

CLI:

```cmd
mlecchita-x keygen -o my.key
mlecchita-x encrypt-text --key my.key "HELLO"
```

---

## Goals

Mlecchita-X is intended to:
- demonstrate reversible secret-key encryption;
- explore key-dependent substitution as a computational reinterpretation of secret writing;
- provide a clean codebase for cryptanalysis and experimentation;
- demonstrate nonce use, authentication, key handling, permutation, diffusion, and round functions;
- make weaknesses and unproven assumptions explicit rather than presenting an experimental cipher as established security.

## Architecture

```text
                       256-bit Secret Key
                               |
                               v
                     HMAC-SHA-256 Derivation
                               |
                 +-------------+-------------+
                 |                           |
                 v                           v
           Round Material              Authentication Key
                 |
                 v
Plaintext -> Dynamic S-box -> Position Permutation
                               |
                               v
                         Prefix-XOR Diffusion
                               |
                               v
                         Round-key XOR
                               |
                         repeat N rounds
                               |
                               v
                           Ciphertext
                               |
                               v
                      HMAC Authentication
                               |
                               v
                    MX02 Encrypted Container
```

### Dynamic substitution

For each round, Mlecchita-X derives deterministic pseudorandom material from the secret key, nonce, round number, and a domain label. It uses that stream with rejection sampling and Fisher-Yates to generate a reversible permutation of all 256 byte values.

This replaces the earlier v0.1 use of Python `random.Random`. Mersenne Twister is not a cryptographic PRNG and is no longer used anywhere in the active implementation.

### Position permutation

Byte positions are independently permuted using a separately domain-separated HMAC-SHA-256 stream. The same key and nonce reproduce the same permutation for decryption.

### Diffusion

The current research prototype uses a reversible prefix-XOR chain. This is intentionally documented as an **unproven design component** and is a major target for future cryptanalysis.

### Key mixing

Every round XORs the state with independently derived round material.

### Authentication

The encrypted container is authenticated with HMAC-SHA-256 using a separately derived authentication key. Authentication is checked before plaintext is returned.

HMAC protects integrity/authenticity of the container; it does **not** prove that the custom encryption construction is secure.

## Encryption workflow

```text
Input bytes
   |
Generate fresh 128-bit nonce
   |
Derive round material from key + nonce
   |
Dynamic substitution
   |
Position permutation
   |
Diffusion
   |
Round-key XOR
   |
Repeat experimental round count
   |
Build MX02 header
   |
HMAC-SHA-256 authentication
   |
MX02 container
```

## Decryption workflow

```text
MX02 container
   |
Parse header + nonce
   |
Verify HMAC
   |
Wrong key / modified data? -> Reject
   |
Reverse rounds
   |
Inverse key mixing
   |
Inverse diffusion
   |
Inverse permutation
   |
Inverse substitution
   |
Original bytes
```

## Installation

After publication:

```cmd
pip install mlecchita-x
```

For local development:

```cmd
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## Python API

```python
from mlecchita_x import generate_key, encrypt, decrypt

key = generate_key()
ciphertext = encrypt(b"HELLO", key)
plaintext = decrypt(ciphertext, key)

print(plaintext)
```

Text helpers:

```python
from mlecchita_x import generate_key, encrypt_text, decrypt_text

key = generate_key()
token = encrypt_text("Vanakkam", key)
print(token)
print(decrypt_text(token, key))
```

## CLI

After installation:

```cmd
mlecchita-x keygen -o my.key
mlecchita-x encrypt-text --key my.key "HELLO"
mlecchita-x decrypt-text --key my.key "MX02:..."
```

Files:

```cmd
mlecchita-x encrypt-file --key my.key input.txt encrypted.mx
mlecchita-x decrypt-file --key my.key encrypted.mx recovered.txt
```

The module form also works:

```cmd
python -m mlecchita_x.cli --help
```

## Tests

```cmd
python -m unittest discover -s tests -v
```

The tests cover byte round trips, Unicode text, wrong-key rejection, ciphertext tampering, unique nonces/ciphertexts, and permutation validity.

## Versioning

`0.x` releases are research/alpha releases. The default round count and internal design may change as cryptanalysis reveals weaknesses.

## Security

Read `SECURITY.md` before using or evaluating the library. Statistical properties such as high entropy or approximately 50% avalanche behavior are **not proof of cryptographic security**.
