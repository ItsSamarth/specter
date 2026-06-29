---
name: ctf-crypto
description: CTF cryptography attack knowledge base — RSA attacks (small exponent / common modulus / Wiener / Coppersmith), AES attacks (Padding Oracle / ECB byte flipping / GCM nonce reuse), ECC attacks, LFSR/LCG/PRNG attacks, classical ciphers, LWE lattice attacks
---

# CTF Cryptography Attack Knowledge Base

A practical attack knowledge base for CTF Crypto challenges, providing **specific attack parameters, mathematical formulas, and Python code snippets**.

**Difference from `crypto-toolkit`**:
- `crypto-toolkit` → encoding/decoding operation tools (base64 decode, MD5 hashing, AES encrypt/decrypt)
- `ctf-crypto` → cryptographic attack knowledge (how to perform RSA small-exponent attacks, how to exploit a Padding Oracle)

## Core Principles

1. **Identify the cryptosystem first** — look at key length, encryption mode, and known quantities to determine the attack direction
2. **Tool verification** — use `python_execute` to run attack code, and `crypto_decode` for auxiliary encoding/decoding
3. **Parameter sensitivity** — cryptographic attacks are extremely sensitive to parameters and must be calculated precisely

## Scenario Routing

| Scenario | Reference Doc | Core Attacks |
|------|---------|---------|
| RSA attacks | `rsa-attacks-cheatsheet.md` | small e / common modulus / Wiener / Pollard / Fermat / Coppersmith |
| AES / block cipher attacks | `aes-and-block-cipher-attacks.md` | ECB flipping / Padding Oracle / GCM nonce reuse |
| ECC attacks | `ecc-attacks-cheatsheet.md` | small subgroup / invalid curve / Smart / Pohlig-Hellman |
| PRNG / stream cipher attacks | `prng-and-stream-cipher-attacks.md` | MT19937 / LCG / LFSR / RC4 |
| Classical ciphers | `classic-cipher-attacks.md` | Vigenere / XOR frequency analysis / OTP reuse |
| Lattice attacks | `lattice-and-lwe-attacks.md` | LLL / BKZ / HNP / LWE embedding |

## Quick Triage Guide

| Challenge Characteristics | Possible Attack | Recommended Reference |
|---------|---------|---------|
| Given n, e, c | RSA | rsa-attacks-cheatsheet.md |
| e=3 or very small e | RSA small-exponent attack | rsa-attacks-cheatsheet.md |
| Multiple (n, e, c) with the same n | RSA common-modulus attack | rsa-attacks-cheatsheet.md |
| Large n but large e | Wiener attack | rsa-attacks-cheatsheet.md |
| AES-CBC + decryption oracle | Padding Oracle | aes-and-block-cipher-attacks.md |
| AES-ECB + controllable plaintext | ECB byte flipping | aes-and-block-cipher-attacks.md |
| Elliptic curve parameters | ECC attack | ecc-attacks-cheatsheet.md |
| Given a sequence of random numbers | PRNG prediction | prng-and-stream-cipher-attacks.md |
| Given ciphertext and partial plaintext | XOR / stream cipher | classic-cipher-attacks.md |
| Matrix / vector operations | Lattice attack | lattice-and-lwe-attacks.md |
