# Changelog

## 0.2.1
- Added Narain Karthik J as public author and maintainer.
- Added PyPI project links for homepage, repository, issues, changelog, and security policy.
- Added `.gitignore` for build artifacts, virtual environments, local keys, and encrypted demo files.
- Included the GitHub Actions Trusted Publishing workflow in the maintained project tree.
- Improved package presentation metadata.
- No intentional cryptographic algorithm change from 0.2.0.


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
