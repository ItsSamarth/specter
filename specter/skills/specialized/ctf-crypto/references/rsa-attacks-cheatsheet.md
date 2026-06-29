# RSA Attack Cheatsheet

## Attack Selection Decision Tree

```
Known n, e, c
├── e very small (e=3)?
│   ├── Same plaintext encrypted multiple times (multiple c)? → Håstad broadcast attack
│   └── Only one set? → small-exponent root attack (low probability)
├── Multiple (n, e, c)?
│   ├── Same n? → common modulus attack
│   ├── Same e? → Håstad broadcast attack
│   └── p or q share a common factor? → GCD factorization
├── e very large (>65537)?
│   └── d may be small → Wiener attack
├── n factorable?
│   ├── Fermat factorization (p≈q)
│   ├── Pollard p-1 (p-1 has small factors)
│   ├── Williams p+1 (p+1 has small factors)
│   └── online lookup (factordb)
└── Partial information known?
    ├── partial plaintext → Coppersmith
    ├── partial p → Coppersmith
    └── partial d → direct construction
```

## Small Exponent Attack (e=3)

### Low-Exponent Broadcast Attack (Håstad)
```python
from gmpy2 import iroot
from functools import reduce

def hastard_broadcast(cs, ns, e=3):
    """When the same plaintext is encrypted under e different moduli n"""
    # Solve via CRT
    N = reduce(lambda a, b: a * b, ns)
    x = 0
    for i in range(e):
        Mi = N // ns[i]
        yi = pow(Mi, -1, ns[i])
        x += cs[i] * Mi * yi
    x %= N
    m = iroot(x, e)
    if m[1]:
        return int(m[0])
    return None
```

## Common Modulus Attack

```python
from gmpy2 import gcd

def common_modulus_attack(c1, c2, e1, e2, n):
    """Same plaintext, same n, encrypted with different e"""
    g, s1, s2 = extended_gcd(e1, e2)
    if s1 < 0:
        c1 = pow(c1, -1, n)
        s1 = -s1
    if s2 < 0:
        c2 = pow(c2, -1, n)
        s2 = -s2
    m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
    return m

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x
```

## Wiener Attack (large e, small d)

```python
def wiener_attack(e, n):
    """Effective when d < n^(1/4)"""
    cf = continued_fraction(e, n)
    convergents = get_convergents(cf)
    for k, d in convergents:
        if k == 0:
            continue
        phi = (e * d - 1) // k
        # Check whether this is a valid phi
        x = n - phi + 1
        disc = x * x - 4 * n
        if disc >= 0:
            s = int(disc ** 0.5)
            if s * s == disc:
                return d
    return None
```

## Fermat Factorization (p ≈ q)

```python
from gmpy2 import is_square, iroot

def fermat_factor(n):
    """Effective when p and q are close to each other"""
    a = iroot(n, 2)[0] + 1
    b2 = a * a - n
    while not is_square(b2):
        a += 1
        b2 = a * a - n
    p = a + iroot(b2, 2)[0]
    q = a - iroot(b2, 2)[0]
    return int(p), int(q)
```

## Pollard p-1 Attack

```python
from math import gcd

def pollard_p1(n, B=100000):
    """Effective when all factors of p-1 are smaller than B"""
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        d = gcd(a - 1, n)
        if 1 < d < n:
            return d, n // d
    return None
```

## Coppersmith Attack (partial plaintext known)

```python
# Using SageMath
# When the high or low bits of the plaintext are known
# m = known_part + unknown_part
# unknown_part < n^(1/e)

# Sage implementation:
P.<x> = PolynomialRing(Zmod(n))
f = (known_prefix + x)^e - c
f = f.monic()
roots = f.small_roots()
if roots:
    m = known_prefix + roots[0]
```

## Online Factorization Tools

- https://factordb.com — look up already-factored n
- http://sagecell.sagemath.org — online Sage computation
