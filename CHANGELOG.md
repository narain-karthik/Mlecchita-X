# Changelog

## 0.2.0
- Removed all use of `random.Random` / Mersenne Twister.
- Added HMAC-SHA-256 PRF stream.
- Added rejection-sampled Fisher-Yates permutation generation.
- Added domain separation for internal derivations.
- Switched key/nonce generation to `secrets`.
- Added explicit exception classes.
- Added fresh-nonce test and permutation tests.
- Reorganized package into PyPI-ready `src/` layout.
- Expanded README and SECURITY documentation.
- Added console entry point `mlecchita-x`.
- Marked 12 rounds explicitly as experimental, not a proven security margin.
