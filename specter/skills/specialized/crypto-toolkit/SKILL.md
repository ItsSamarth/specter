---
name: crypto-toolkit
description: Encoding/decoding and encryption/decryption tools — base64/URL/Hex/HTML entity encoding/decoding, MD5/SHA hashing, AES/DES/RSA encryption/decryption, JWT parsing, Caesar/ROT13 ciphers, rail-fence/Vigenere ciphers, Unicode escaping, Morse code, etc.
---

# Encoding/Decoding and Encryption/Decryption Skill

Provides comprehensive encoding/decoding and encryption/decryption capabilities for the encoding, encryption, and obfuscation scenarios commonly encountered in penetration testing.
**Important**: When you encounter any encoded/encrypted string, prefer using the `crypto_decode` tool to decode it rather than guessing by intuition.

## Core Principles

1. **Tool first** — When you encounter base64, hex, URL-encoded, or similar strings, call the `crypto_decode` tool to decode them; do not improvise
2. **Try multiple formats** — If one decoding method gives an unreasonable result, try other encoding formats
3. **Chained decoding** — Multi-layer encoding is common in CTFs (e.g. base64→hex→ROT13); after decoding, check whether the result needs to be decoded again
4. **Verify results** — After decoding, verify the plausibility of the result (is it readable text, does it look like a path/URL/flag, etc.)

## 1. Encoding Identification and Decoding

### Recognizing common encoding features

| Encoding type | Features | Example |
|---------|------|------|
| Base64 | `A-Za-z0-9+/=`, often ends with `=` padding | `TnNTY1RmLnBocA==` |
| Base32 | `A-Z2-7=` | `OBZHK5DFN2A====` |
| Hex | `0-9a-f`, even length | `4e73536354662e706870` |
| URL encoding | `%XX` format | `%2F%61%64%6D%69%6E` |
| HTML entity | `&#xNN;` or `&#NNN;` | `&#x3C;script&#x3E;` |
| Unicode escape | `\uXXXX` or `\UXXXXXXXX` | `\u003c\u0073\u0063` |
| JWT | Three base64 segments separated by `.` | `eyJhbG...` |

### Decoding strategy

1. Identify the encoding type → call the `crypto_decode` tool specifying the corresponding operation
2. Check whether the decoded result is readable/reasonable
3. If unreasonable, try other encoding formats
4. If the result still looks encoded, repeat steps 1-3

## 2. Hashing and Digests

### Common hash types

| Type | Output length | Features |
|------|---------|------|
| MD5 | 32 hex | `e10adc3949ba59abbe56e057f20f883e` |
| SHA1 | 40 hex | `aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d` |
| SHA256 | 64 hex | `2c26b46b68ffc68ff99b453c1d30413413422d7064...` |
| SHA512 | 128 hex | Longer hex string |
| NTLM | 32 hex | Windows hash |
| MySQL5 | 41 characters | `*E6CC90B878B948C35E92B003C792C46758BF4` |

### Hash handling strategy

- Identify the hash type (by length and character set)
- Try online rainbow table lookups (access crackstation, etc., via the fetch tool)
- For hashes with a known salt, try salted brute force

## 3. Symmetric Encryption

### AES/DES/3DES

- Requires a key and a mode (ECB/CBC/CTR, etc.)
- CBC mode requires an IV
- Common padding: PKCS7/ZeroPadding
- Hardcoded keys are often encountered in pentests; prefer extracting them from the source code

## 4. Asymmetric Encryption

### RSA

- Extract parameters from the public/private key file
- RSA with a too-small modulus can be factored
- A known private key can decrypt directly

## 5. Classical Ciphers

| Type | Features | Cracking method |
|------|------|---------|
| Caesar/ROT13 | Letter shift | Brute force all 25 shifts |
| Vigenere | Polyalphabetic substitution | Kasiski/frequency analysis |
| Rail-fence cipher | Character grouping and rearrangement | Try common rail counts |
| Bacon cipher | AB five-letter groups | Lookup table |
| Morse | `.-` dots and dashes | Lookup table |

## 6. JWT Handling

- Decode Header + Payload (base64url)
- Check the algorithm: `none` algorithm bypass, RS256→HS256 algorithm confusion
- Try weak-key signature forgery
- Check time claims such as exp/nbf

## Tool Usage

### `crypto_decode` tool

When you encounter an operation requiring encoding/decoding/encryption/decryption, call this tool:

```
crypto_decode(operation="base64_decode", input="TnNTY1RmLnBocA==")
```

List of supported operations:
- **Encoding**: `base64_encode`, `base32_encode`, `hex_encode`, `url_encode`, `html_encode`, `unicode_encode`, `rot13_encode`, `morse_encode`, `caesar_encode`, `base58_encode`
- **Decoding**: `base64_decode`, `base32_decode`, `hex_decode`, `url_decode`, `html_decode`, `unicode_decode`, `rot13_decode`, `morse_decode`, `caesar_decode`, `base58_decode`
- **Hashing**: `md5_hash`, `sha1_hash`, `sha256_hash`, `sha512_hash`
- **Encryption/Decryption**: `aes_encrypt`, `aes_decrypt`, `des_encrypt`, `des_decrypt`, `rsa_encrypt`, `rsa_decrypt`
- **JWT**: `jwt_decode`, `jwt_encode`
- **Auto-identification**: `auto_decode` (automatically identifies the encoding type and decodes)

## CTF Cryptography Attack Routing

> When you encounter a cryptography attack scenario (encryption algorithm known, need to recover plaintext or key), prefer using the `ctf-crypto` Skill:

| Attack scenario | Route to ctf-crypto | Reference document |
|---------|-----------------|---------|
| RSA small exponent/common modulus/Wiener | `ctf-crypto` | `references/rsa-attacks-cheatsheet.md` |
| AES Padding Oracle/ECB flipping | `ctf-crypto` | `references/aes-and-block-cipher-attacks.md` |
| ECC small subgroup/discrete logarithm | `ctf-crypto` | `references/ecc-attacks-cheatsheet.md` |
| PRNG/MT19937 prediction | `ctf-crypto` | `references/prng-and-stream-cipher-attacks.md` |
| Classical ciphers (Vigenere/XOR) | `ctf-crypto` | `references/classic-cipher-attacks.md` |
| Lattice attacks/LWE | `ctf-crypto` | `references/lattice-and-lwe-attacks.md` |

**This Skill focuses on encoding/decoding operation tools**; for specific cryptography attack methods and parameters, refer to `ctf-crypto`.

## Reference Documents

- `references/encoding-cheatsheet.md` — Encoding identification quick reference
- `references/crypto-attacks.md` — Cryptography attack techniques
- `references/crypto-attacks-roadmap.md` — Cryptography attack classification routing (choose an attack method based on the problem's characteristics)
