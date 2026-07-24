# Security Policy and Cryptographic Status

## Read this first

Mlecchita-X is an **experimental research cipher**, not established production cryptography.

Do not use Mlecchita-X to protect:
- passwords or authentication credentials;
- banking/payment information;
- private keys or recovery phrases;
- medical or highly confidential personal information;
- production secrets;
- business-critical confidential files;
- any information for which compromise would cause meaningful harm.

For real applications, use established, reviewed cryptographic libraries and standardized authenticated-encryption constructions.

## Security claims

Mlecchita-X currently claims only software-level properties verified by its tests:
1. With the same valid key, valid ciphertext produced by this implementation can be decrypted back to the original supported input.
2. A modified authenticated container is expected to fail HMAC verification.
3. A different key is expected to fail HMAC verification.
4. Encryption generates a fresh nonce using the operating system CSPRNG.

These are correctness/integrity properties. They are **not a claim of confidentiality strength**.

## Changes made after v0.1 review

### Removal of `random.Random`

v0.1 used Python's `random.Random` (Mersenne Twister), seeded from HMAC-derived material, to shuffle S-box values and byte positions.

Mersenne Twister is not a cryptographic PRNG. Although the seed was secret, using a non-cryptographic generator introduced an unnecessary and insufficiently analyzed dependency.

v0.2 removes `random.Random` completely.

The active implementation now uses:
- HMAC-SHA-256 as a deterministic pseudorandom-function source;
- explicit domain separation between S-box, position-permutation, round-key, and authentication derivations;
- rejection sampling for bounded integers;
- Fisher-Yates for permutation generation.

This addresses the specific Mersenne-Twister concern. It does **not** establish the security of the overall cipher.

### Round count

The default round count is currently **12**.

This number is an experimental engineering parameter, not a derived security margin. No published or formal analysis has demonstrated a maximum successful reduced-round differential or linear attack from which a safe full-round margin could be calculated.

Therefore statements such as "12 rounds makes Mlecchita-X secure" are unsupported and must not be made.

## Known/unproven areas

### Differential cryptanalysis

No formal upper bounds have been established for differential characteristics across the complete round function. The probability and propagation of useful input/output differences require dedicated study.

### Linear cryptanalysis

No formal linear-approximation analysis has established resistance to linear attacks. Key-dependent S-boxes do not automatically eliminate useful correlations.

### Diffusion layer

The current prefix-XOR diffusion transform is reversible and spreads changes, but reversibility and avalanche behavior are not sufficient security arguments.

Its algebraic simplicity may permit structural or differential relationships. This component should be treated as one of the primary candidates for redesign after analysis.

### Key-dependent S-box

Each round uses a key/nonce-derived byte permutation. The permutation-generation procedure is deterministic and avoids Mersenne Twister, but the cryptographic consequences of using dynamically generated S-boxes have not been independently analyzed.

Important unanswered questions include nonlinearity distribution, differential uniformity, linear biases, fixed points, cycle structure, and interactions between round keys and generated S-boxes.

### Position permutation

A key-dependent position permutation provides rearrangement but does not itself provide cryptographic nonlinearity. Its contribution to security must be analyzed together with substitution and diffusion.

### Related-key behavior

No meaningful related-key cryptanalysis has been completed.

### Chosen-plaintext behavior

No comprehensive chosen-plaintext attack analysis has been completed.

### Nonce requirements

A fresh 128-bit nonce is generated for every encryption with `secrets.token_bytes`. Users should not manually reuse nonces. The public API intentionally does not expose nonce selection.

The consequences of nonce reuse in the custom cipher have not been formally bounded, so nonce uniqueness should be considered mandatory.

### Side channels

The Python implementation is not constant-time. Dynamic table lookups, Python object behavior, memory access patterns, interpreter behavior, and execution timing may leak information in hostile local environments.

No side-channel resistance is claimed.

### Denial of service / untrusted inputs

Authenticated ciphertext should still be treated as untrusted input. Applications should impose reasonable size limits before loading very large containers into memory.

## Authentication

Mlecchita-X uses HMAC-SHA-256 with a separately derived authentication key.

The implementation authenticates the header and ciphertext and verifies the tag before decrypting.

This provides a conventional integrity boundary around the experimental cipher. It does not convert an insecure encryption primitive into a secure one if the custom encryption design contains confidentiality weaknesses.

## Randomness

Long-term secret keys and per-message nonces are generated using Python's `secrets` module, which uses operating-system cryptographic randomness.

The implementation does not use `random.Random`.

## What test results do NOT mean

### High entropy

Ciphertext approaching 8 bits/byte of empirical entropy can still be produced by an insecure construction. Entropy is a statistical diagnostic, not a security proof.

### Avalanche near 50%

A cipher can exhibit a strong avalanche effect and still contain exploitable mathematical structure.

### Passing unit tests

Unit tests demonstrate implementation correctness for tested cases. They do not demonstrate resistance to cryptanalysis.

### HMAC success

HMAC-SHA-256 authentication can detect tampering without proving confidentiality of the custom cipher.

## Recommended research before any stronger security claim

At minimum:
1. Differential distribution analysis of generated S-boxes.
2. Linear approximation analysis.
3. Strict Avalanche Criterion testing over all input/output bit positions.
4. Bit-independence testing.
5. Reduced-round differential experiments.
6. Reduced-round linear/correlation experiments.
7. Chosen-plaintext structural testing.
8. Related-key experiments.
9. Analysis/redesign of the diffusion layer.
10. Large multi-key/multi-nonce statistical campaigns.
11. Independent cryptographic review.
12. Published specification and reproducible test vectors.

## Reporting a weakness

Security weaknesses should be documented as research findings. Do not hide negative results: a successful attack against Mlecchita-X is valuable evidence for improving or rejecting a design component.
