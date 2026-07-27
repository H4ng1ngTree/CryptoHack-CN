# Scalar Multiplication

**35 pts - 4950 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

Scalar multiplication is repeated point addition, for example:

$$
[3]P=P+P+P
$$

This challenge introduces the double-and-add algorithm.

```text
Input:  P in E(F_p), integer n > 0
Output: Q = [n]P in E(F_p)

1. Set Q = P and R = O.
2. While n > 0:
   3. If n = 1 mod 2, set R = R + Q.
   4. Set Q = [2]Q and n = floor(n / 2).
   5. Continue while n > 0.
6. Return R.
```

Use:

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739}
$$

> Test value: for $X=(5323,5438)$, assert $[1337]X=(1089,6931)$.

Given $P=(2339,2213)$, find $Q(x,y)=[7863]P$.

Enter flag here: `crypto{x,y}`
