# Point Addition

**30 pts - 5444 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

This challenge asks you to implement the elliptic-curve point addition law over a finite field.

## Algorithm for adding two points: $P + Q$

```text
(a) If P = O, then P + Q = Q.
(b) Otherwise, if Q = O, then P + Q = P.
(c) Otherwise, write P = (x_1, y_1) and Q = (x_2, y_2).
(d) If x_1 = x_2 and y_1 = -y_2, then P + Q = O.
(e) Otherwise:
    (e1) if P != Q: lambda = (y_2 - y_1) / (x_2 - x_1)
    (e2) if P = Q: lambda = (3x_1^2 + a) / 2y_1
(f) x_3 = lambda^2 - x_1 - x_2
(h) y_3 = lambda(x_1 - x_3) - y_1
(i) P + Q = (x_3, y_3)
```

> In a finite field, all operations are performed modulo $p$. Division is implemented by multiplication with a modular inverse; for example, $5^{-1} \equiv 9 \pmod{11}$.

Use the curve:

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739}
$$

> Test values: for $X=(5274,2841)$ and $Y=(8669,740)$, assert that $X+Y=(1024,4440)$ and $X+X=(7284,2107)$.

Given:

$$
P=(493,5564),\quad Q=(1539,4742),\quad R=(4403,5202)
$$

find:

$$
S(x,y)=P+P+Q+R
$$

> After computing $S$, verify that it lies on $E(\mathbb{F}_p)$.

Enter flag here: `crypto{x,y}`
