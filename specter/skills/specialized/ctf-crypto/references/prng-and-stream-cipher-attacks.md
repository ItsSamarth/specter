# PRNG and Stream Cipher Attacks

## MT19937 ( Mersenne Twister ) Attack

```python
# MT19937 state recovery (given 624 outputs)
from ctypes import *

def untemper(y):
    y ^= y >> 18
    y ^= (y << 15) & 0xefc60000
    y ^= (y << 7) & 0x9d2c5680
    y ^= (y << 14) & 0x9d2c5680
    y ^= (y << 13) & 0x9d2c5680
    y ^= (y << 11) & 0x9d2c5680
    y ^= y >> 18
    return y

def recover_mt(outputs):
    """Recover internal state from 624 consecutive MT19937 outputs"""
    state = [untemper(y) for y in outputs[:624]]
    MT = c_ulong * 624
    mt = MT(*state)
    index = 624
    def twist():
        global index, mt
        for i in range(227):
            y = (mt[i] & 0x80000000) + (mt[(i+1)%624] & 0x7fffffff)
            mt[i] = mt[(i+397) % 624] ^ (y >> 1)
            if y & 1:
                mt[i] ^= 0x9908b0df
        index = 0
    return mt, twist, index
```

## LCG (Linear Congruential Generator) Attack

```python
"""
LCG: s_{n+1} = a * s_n + c (mod m)
When parameters are known: recurse directly
When parameters are unknown: given 3 sets of (s, s_next), a, c, m can be solved
"""

def lcg_attack(states):
    """Recover LCG parameters (a, c, m) from 3 consecutive states"""
    s0, s1, s2 = states[0], states[1], states[2]
    # s1 = a*s0 + c (mod m)
    # s2 = a*s1 + c (mod m)
    # s2 - s1 = a*(s1 - s0) (mod m)
    # Extended Euclidean to solve a, m
```

## LFSR (Linear Feedback Shift Register) Attack

```python
"""
Berlekamp-Massey algorithm: recover the LFSR feedback polynomial from the output sequence
"""

def berlekamp_massey(s):
    """Recover the shortest LFSR feedback polynomial from a binary sequence"""
    # Sage implementation
    # F.<x> = GF(2)[]
    # s_seq = sequence(s)
    # return list(lfsr_sequence(f, [1]+[0]*15, len(s)))
```

## Known-Plaintext Attack (XOR Stream Cipher)

```python
"""
Stream cipher: C = P XOR keystream
If part of the plaintext P is known, keystream = C XOR P can be recovered
The keystream can be used to decrypt other ciphertexts
"""

def xor_attack(ciphertext, known_plaintext):
    """XOR stream cipher known-plaintext attack"""
    key = bytes(a ^ b for a, b in zip(ciphertext, known_plaintext))
    return key

def xor_decrypt(key, ciphertext):
    """Decrypt with the recovered keystream"""
    return bytes(a ^ b for a, b in zip(key, ciphertext))
```

## RC4 攻击

```python
"""
RC4 已知弱点：
1. RC4 Drop (丢弃前 N 字节后，密钥流接近随机)
2. 某些密钥初始化有偏差
"""

def rc4_drop(ciphertext, drop=3072):
    """RC4 Drop N 字节后解密"""
```

## Python random 模块预测

```python
import random

# 如果能访问 Python random 状态，可以预测未来随机数
# 已知 624 * 4 = 2496 字节的状态
state = random.getstate()
# 推进随机数
random.setstate(state)
next_val = random.randint(0, 2**31)
```
