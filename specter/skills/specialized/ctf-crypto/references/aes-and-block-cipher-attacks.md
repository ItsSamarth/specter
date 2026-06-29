# AES and Block Cipher Attacks

## Encryption Mode Quick Reference

| Mode | Characteristics | Exploitable Weakness |
|------|------|-----------|
| ECB | Same plaintext → same ciphertext | Pattern recognition, reordering attacks |
| CBC | Previous ciphertext block feeds into current encryption | IV flipping, Padding Oracle |
| CTR | Stream-style encryption | nonce reuse → XOR leakage |
| CFB | Similar to a stream cipher | IV flipping |
| OFB | Similar to a stream cipher | nonce reuse |
| GCM | Authenticated encryption | nonce reuse → keystream recovery |

## ECB Byte Flipping

```python
from Crypto.Cipher import AES

# In ECB mode, identical plaintext blocks produce identical ciphertext blocks
# Attack: identify repeated ciphertext blocks → infer plaintext structure
# Ciphertext blocks can be reordered to alter the plaintext structure

def ecb_detect(ciphertext, block_size=16):
    """Detect ECB mode (look for repeated blocks)"""
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    return len(blocks) != len(set(blocks))
```

## CBC IV Flipping Attack

```python
"""
Principle: In CBC, P[i] = Decrypt(C[i]) XOR C[i-1]
Modifying a byte of C[i-1] → flips the corresponding byte of P[i]

Use: modifying the IV alters the first plaintext block; modifying C[i-1] alters the i-th plaintext block
Cost: the plaintext P[i-1] corresponding to C[i-1] gets corrupted
"""

def cbc_iv_flip(ciphertext, known_plain, target_plain, block_size=16):
    """Flip the first CBC plaintext block (by modifying the IV)"""
    iv = bytearray(ciphertext[:block_size])
    for i in range(block_size):
        iv[i] = iv[i] ^ known_plain[i] ^ target_plain[i]
    return bytes(iv) + ciphertext[block_size:]
```

## Padding Oracle Attack

```python
"""
Principle: during CBC decryption, if the padding is invalid the server returns a different error
By brute-forcing byte by byte, the error/success difference is used to recover the plaintext

Conditions:
1. CBC mode is used
2. The server returns different responses for padding errors vs. ciphertext errors
3. Modified ciphertext can be submitted repeatedly
"""

def padding_oracle_attack(oracle, ciphertext, block_size=16):
    """Padding Oracle attack to recover plaintext
    
    oracle: a function that takes ciphertext and returns True (padding correct) / False (padding incorrect)
    """
    blocks = [ciphertext[i:i+block_size] for i in range(0, len(ciphertext), block_size)]
    plaintext = b''
    
    for block_idx in range(1, len(blocks)):
        prev_block = bytearray(blocks[block_idx - 1])
        curr_block = blocks[block_idx]
        intermediate = bytearray(block_size)
        
        for byte_pos in range(block_size - 1, -1, -1):
            padding_val = block_size - byte_pos
            
            # Construct the test ciphertext
            test_block = bytearray(block_size)
            for k in range(byte_pos + 1, block_size):
                test_block[k] = intermediate[k] ^ padding_val
            
            found = False
            for guess in range(256):
                test_block[byte_pos] = guess
                test_cipher = bytes(test_block) + curr_block
                
                if oracle(test_cipher):
                    intermediate[byte_pos] = guess ^ padding_val
                    found = True
                    break
            
            if not found:
                raise Exception(f"Padding oracle attack failed at byte {byte_pos}")
        
        # Recover the plaintext
        for i in range(block_size):
            plaintext += bytes([intermediate[i] ^ prev_block[i]])
    
    return plaintext
```

## GCM Nonce Reuse Attack

```python
"""
When the same nonce is used for two encryptions:
- Both encryptions use the same keystream
- C1 = P1 XOR keystream
- C2 = P2 XOR keystream
- C1 XOR C2 = P1 XOR P2

If P1 is known, P2 can be recovered
"""

def gcm_nonce_reuse(c1, c2, p1):
    """Recover plaintext by exploiting GCM nonce reuse"""
    return bytes(a ^ b ^ c for a, b, c in zip(c1, c2, p1))
```

## CTR Nonce Reuse

```python
"""
In CTR mode, nonce reuse is equivalent to stream cipher key reuse
C1 = P1 XOR keystream
C2 = P2 XOR keystream
C1 XOR C2 = P1 XOR P2
"""

def ctr_nonce_reuse(c1, c2, known_p1):
    """Recover plaintext by exploiting CTR nonce reuse"""
    return bytes(a ^ b ^ c for a, b, c in zip(c1, c2, known_p1))
```
