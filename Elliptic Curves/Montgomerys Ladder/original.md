# Montgomery's Ladder

**40 pts - 2229 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

This side-channel challenge introduces Montgomery's ladder as a scalar-multiplication method.

## Montgomery binary algorithm in $E(\mathbb{F}_p)$

```text
Input: P in E(F_p), n-bit integer k = sum 2^i k_i with k_{n-1}=1
Output: [k]P in E(F_p)

1. Set (R0, R1) = (P, [2]P).
2. For i = n - 2 down to 0:
   3. If k_i = 0, set (R0, R1) = ([2]R0, R0 + R1).
   4. Else, set (R0, R1) = (R0 + R1, [2]R1).
5. Return R0.
```

Use the Montgomery-form curve:

$$
E : Y^2 = X^3 + 486662X^2 + X \pmod{2^{255}-19}
$$

Given `G.x = 9`, find the decimal $x$-coordinate of:

$$
Q=[\texttt{0x1337c0decafe}]G
$$

## Affine formulas for a Montgomery curve

For:

$$
E : By^2 = x^3 + Ax^2 + x
$$

```text
Addition, P != Q:
alpha = (y_2 - y_1) / (x_2 - x_1)
x_3 = B alpha^2 - A - x_1 - x_2
y_3 = alpha(x_1 - x_3) - y_1

Doubling:
alpha = (3x_1^2 + 2A x_1 + 1) / (2B y_1)
x_3 = B alpha^2 - A - 2x_1
y_3 = alpha(x_1 - x_3) - y_1
```

> All operations are performed modulo $p$.

Enter flag here: `crypto{...}`
