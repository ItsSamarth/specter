# Cryptography Attack Classification Routing

Based on the known information given in the problem, quickly decide which attack method to use.

## Decision Tree

```
Known conditions
├── Know plaintext + ciphertext?
│   ├── Same key used to encrypt multiple times? → XOR/stream cipher analysis
│   └── Single encryption? → Analyze the encryption mode
├── Know ciphertext + key?
│   ├── Symmetric encryption → Decrypt directly
│   └── Asymmetric encryption → RSA/ECC attack
├── Know n, e, c (RSA)?
│   ├── e is very small → Small exponent attack
│   ├── Multiple sets sharing n → Common modulus attack
│   ├── d is very small → Wiener attack
│   ├── p-1 is smooth → Pollard p-1
│   └── Try online factoring (factordb)
├── Elliptic curve parameters?
│   ├── Smooth order → Pohlig-Hellman
│   ├── Anomalous curve → Smart attack
│   └── ECDSA nonce reuse → Private key recovery
├── Known PRNG output sequence?
│   ├── MT19937 → State recovery
│   ├── LCG → Parameter recovery
│   └── LFSR → Berlekamp-Massey
└── Classical cipher?
    ├── Caesar/ROT13 → Brute force
    ├── Vigenere → Kasiski + frequency
    └── One-Time Pad reuse → Statistical attack
```

## Quick RSA Attack Selection

| Known | Attack |
|------|------|
| n, e, c, e=3 | Small exponent root extraction |
| Multiple sets (n, c), same e, same plaintext | Håstad broadcast |
| Multiple sets (n, c), same n, different e | Common modulus attack |
| n, e, d a very small approximation | Wiener attack |
| n factorable, p≈q | Fermat factorization |
| n factorable, p-1 smooth | Pollard p-1 |
| Known partial plaintext | Coppersmith |
| Queryable in factordb | Online factoring |

## Quick AES/Block Cipher Attack Selection

| Scenario | Attack |
|------|------|
| ECB mode | Mode analysis + block rearrangement |
| CBC mode, controllable IV | IV flipping attack |
| CBC mode, Padding Oracle | Padding Oracle attack |
| CTR/GCM, nonce reuse | Keystream recovery |
| Known partial plaintext | XOR keystream recovery |

## Quick PRNG Attack Selection

| Scenario | Attack |
|------|------|
| Python random(), 624 outputs | MT19937 state recovery |
| 3 consecutive LCG outputs | Parameter recovery |
| LFSR output sequence | Berlekamp-Massey |
| RC4 (after discarding first 3072 bytes) | RC4 Drop attack |

## Quick Classical Cipher Selection

| Ciphertext feature | Attack |
|---------|------|
| Single-character substitution | Frequency analysis |
| Multi-character shift | Caesar brute force |
| Polyalphabetic substitution | Vigenere Kasiski |
| Binary multi-byte XOR | Frequency analysis + key length estimation |
| One-time pad reuse | XOR comparison attack |
