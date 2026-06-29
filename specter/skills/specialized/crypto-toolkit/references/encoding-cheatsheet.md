# Encoding Identification Quick Reference

## Quick Identification Flow

```
Input string
  ├─ Contains %XX → URL encoding → url_decode
  ├─ Contains &# or &#x → HTML entity → html_decode
  ├─ Contains \uXXXX → Unicode escape → unicode_decode
  ├─ Contains .- and only dots/dashes/spaces → Morse → morse_decode
  ├─ Three Base64 segments joined by . → JWT → jwt_decode
  ├─ Trailing = padding + A-Za-z0-9+/ → Base64 → base64_decode
  ├─ Trailing = padding + A-Z2-7 → Base32 → base32_decode
  ├─ Pure hex chars (0-9a-f) even length → Hex → hex_decode
  ├─ Uppercase letters + digits, no padding → possibly Base58 → base58_decode
  ├─ Letter-shift pattern (e.g. E→M, A→I) → Caesar → caesar_decode
  └─ Cannot determine → auto_decode
```

## Base64 Variants

| Variant | Character Set | Use Case |
|------|--------|------|
| Standard Base64 | `A-Za-z0-9+/=` | General purpose |
| URL-safe Base64 | `A-Za-z0-9-_` | URL parameters |
| Base64url (JWT) | `A-Za-z0-9_-` no padding | JWT |

## Base58

| Variant | Excluded Characters | Use Case |
|------|---------|------|
| Bitcoin | `0OIl` | Address encoding |
| Flickr | `0OIl` | Short URLs |
| Ripple | `0OIl` | Address encoding |

## Common Obfuscation Patterns

### Double Encoding
```
Original: admin
→ URL encoding: %61%64%6D%69%6E
→ Double URL encoding: %2561%2564%256D%2569%256E
```

### Base64 + Hex Chain
```
Original: NsScTf.php
→ Hex: 4e73536354662e706870
→ Base64: TnNTY1RmLnBocA==
```

### ROT13 Nested
```
Original: password
→ ROT13: cnffjbeq
→ ROT13 again: password (ROT13 is its own inverse)
```

## Length vs. Encoding Comparison

| Plaintext length | Base64 length | Hex length | Base32 length |
|---------|------------|---------|------------|
| 1 byte | 4 chars | 2 chars | 8 chars |
| 4 bytes | 8 chars | 8 chars | 8 chars |
| 8 bytes | 12 chars | 16 chars | 16 chars |
| 16 bytes | 24 chars | 32 chars | 28 chars |

## Common CTF Encoding Chains

1. **Base64 → Plaintext** — most common
2. **Base64 → Hex → Plaintext** — double encoding
3. **Base64 → Base64 → Plaintext** — nested Base64
4. **Hex → Base64 → ROT13 → Plaintext** — triple-layer encoding
5. **URL encoding → Base64 → Plaintext** — common in web scenarios
6. **Morse → Base64 → Hex → Plaintext** — crypto challenges

## Post-Decode Verification

After decoding, check if the result:
- [ ] Is readable ASCII/UTF-8 text
- [ ] Looks like a path (/xxx/yyy.php)
- [ ] Looks like a URL (http://...)
- [ ] Contains flag format (flag{...}, NSSCTF{...})
- [ ] Is still encoded (needs another round of decoding)
