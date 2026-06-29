# Cryptographic Attack Techniques

## 1. Hash Attacks

### Rainbow Table Lookup
- crackstation.net — free, supports MD5/SHA1/SHA256
- cmd5.com — broad coverage
- hashes.org — community maintained

### Hash Length Extension Attack
- Applies to: MD5, SHA1, SHA256, and other Merkle-Damgård-based hashes
- Condition: know `H(message)` and `len(message)`, without knowing message itself
- Tools: hashpump, hash_extender
- Scenario: API signature verification bypass

### Hash Collision
- MD5: fastcoll, HashClash
- SHA1: SHAttered (theoretically feasible)
- Scenario: file integrity bypass, certificate forgery

## 2. Symmetric Encryption Attacks

### ECB Mode Attack
- Identical plaintext blocks → identical ciphertext blocks
- Can rearrange plaintext by rearranging ciphertext blocks
- Can identify repeated patterns (e.g. user role fields)

### CBC Byte-Flipping Attack
- Modifying the IV or previous ciphertext block flips corresponding bytes in the next plaintext block
- Formula: `P[i] = D(C[i]) XOR C[i-1]`
- Modify `C[i-1][j]` → flip `P[i][j]`
- Scenario: modify encrypted user ID, role fields

### Padding Oracle Attack
- Condition: server reveals whether padding is correct
- Recover plaintext byte by byte without the key
- Tools: padbuster, padding-oracle-attacker
- Scenario: ASP.NET, Java serialized tokens

### IV Reuse Attack
- CBC mode with same IV + same Key → information leakage
- Can infer whether plaintext is identical

## 3. RSA Attacks

### Small Public Exponent Attack
- When e=3, if m^3 < n, recover plaintext by taking cube root directly
- Low-exponent broadcast attack: same plaintext encrypted with same e but different n values

### Common Modulus Attack
- Same plaintext encrypted with same n but different e values
- Recover plaintext using extended Euclidean algorithm

### Wiener's Attack
- When d < n^0.25, factor n
- Applies to small private exponent scenarios

### Fermat's Factorization
- When p and q are close, quickly factor n
- Applies to weak key generation

### Known Key File
- Extract parameters from .pem/.der files
- `openssl rsa -text -noout -in key.pem`

## 4. Classical Cipher Attacks

### Caesar Brute Force
- Only 25 possibilities, enumerate directly
- Use frequency analysis to select most likely result

### Vigenère Analysis
- Kasiski test to determine key length
- Index of coincidence to verify key length
- After determining length, solve each column as Caesar cipher

### Rail Fence Cipher
- Common rail counts: 2–8
- Enumerate all possible rail counts
- Check whether result is meaningful

### Bacon's Cipher
- Two fonts/styles → A/B encoding
- Every 5 characters decodes one letter

## 5. JWT Attacks

### None Algorithm Bypass
```json
{"alg": "none", "typ": "JWT"}
```
- Change algorithm to none
- Remove the signature portion
- Some implementations accept unsigned tokens

### RS256 → HS256 Algorithm Confusion
- Change algorithm from RS256 to HS256
- Sign with public key as HMAC key
- If server verifies HS256 signature with public key → bypass

### Weak Key Brute Force
- jwt-tool, jwt-cracker
- Common weak keys: secret, password, 123456, etc.

### JWK / jku Injection
- Embed public key in header (jwk field)
- Or point to attacker-controlled jku URL
- If server trusts the key in the header → forgery

## 6. Encoding Chain Attack Patterns

### WAF Bypass Encoding
- Double URL encoding: `%2527` → `%27` → `'`
- Unicode normalization: `％27` → `'` (full-width to half-width)
- HTML entity: `&#39;` → `'`
- Base64-encode injection parameters

### Encoding in Deserialization
- PHP: base64-encoded serialized objects
- Java: Base64-encoded serialized byte stream
- Python: base64 pickle payloads

## 7. Tool Quick Reference

| Scenario | Tool |
|----------|------|
| General encode/decode | CyberChef |
| Hash cracking | hashcat, john |
| RSA analysis | RsaCtfTool |
| JWT analysis | jwt-tool |
| Padding Oracle | padbuster |
| Hash extension | hashpump |
| Online decode | base64decode.org, cyberchef.org |
