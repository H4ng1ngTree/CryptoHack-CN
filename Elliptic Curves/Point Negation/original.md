# Point Negation

**10 pts - 6118 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

For the starter challenges, use the curve:

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739}
$$

Given:

$$
P=(8045,6936)
$$

find a point $Q(x,y)$ such that:

$$
P+Q=O
$$

> Work in the finite field, so negative coordinates must be handled modulo $p$.

Enter flag here: `crypto{x,y}`
