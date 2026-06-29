# Lattice Attacks and LWE

## Basic Concepts

```
Lattice: a discrete additive subgroup of Z^n
Basis: a set of linearly independent vectors that generate the lattice
LLL algorithm: finds an approximate shortest vector of the lattice basis (SVP approximation)
CVP (Closest Vector Problem): find the closest vector
SVP (Shortest Vector Problem): find the shortest vector
```

## LLL Algorithm

```python
# SageMath implementation
"""
A = matrix(ZZ, [[...], [...], ...])  # lattice basis matrix
B = A.LLL()  # LLL-reduced basis
# the column vectors of B are near-shortest lattice vectors
```

## Hidden Number Problem (HNP)

```python
"""
Known: partial bits of (d_i, (t_i * a + k_i * d_i) mod p)
Recover: a (private key)
Use Coppersmith to recover k_i
"""
# SageMath
def hnp_attack(d, t, bits, p):
    F.<x> = PolynomialRing(Zmod(p))
    # construct the polynomial...
```

## Coppersmith-Related

```python
"""
Coppersmith finds small roots of a polynomial:
f(x) = 0 mod n, |x| < n^(1/d)
where d is the polynomial degree
"""

# SageMath
def coppersmith_small_root(f, n, d, m):
    """f(x) = 0 mod n, find small root x, |x| < n^(1/(d*omega))"""
    # construct the lattice and run LLL
```

## LWE (Learning With Errors)

```python
"""
LWE problem:
Known: (A, b = As + e) mod q
Recover: s (private key)
where e is a small error vector

Common attacks:
1. Enumerate the small error (when e is very small)
2. BKW algorithm
3. Reduce to SVP/CVP
"""
```

## HNP Attack Template

```python
# SageMath: recover the RSA private key from a partial private key
"""
A variant of the DCP (Diffie-Hellman Claw Problem)
Solve using lattice reduction
"""

# Basic template
"""
F = GF(p)
P.<x> = PolynomialRing(F)

# construct the lattice basis matrix
# apply LLL
# extract the private key from the reduced basis
"""
```

## General Lattice Attack Template

```python
# Consider a lattice attack when you encounter the following scenarios:
# 1. Multiple equations with unknowns and a "small error"
# 2. Partial private key / partial plaintext recovery
# 3. Reducible to the lattice closest vector problem

# Steps:
# 1. Model the problem as a CVP/SVP in a lattice
# 2. Construct the lattice basis matrix
# 3. Reduce using LLL/BKZ
# 4. Extract the solution from the reduced basis
```
