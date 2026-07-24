# Architecture

Mlecchita-X is a secret-key experimental cipher.

Each message receives a fresh 128-bit nonce. HMAC-SHA-256 domain-separated derivations generate round material. A round performs key-dependent byte substitution, key-dependent position permutation, reversible prefix-XOR diffusion, and XOR round-key mixing.

The same key and nonce deterministically reproduce inverse transformations for decryption. The final container is authenticated with HMAC-SHA-256 before decryption returns plaintext.

The historical Mlecchita Vikalpa connection is conceptual: secret writing and substitution inspire the key-controlled substitution layer. The modern cryptographic mechanisms are project inventions.
