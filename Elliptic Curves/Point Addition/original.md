# Point Addition

**30 pts - 5449 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Original challenge

While working with elliptic curve cryptography, we will need to add points together. In the background challenges, we did this geometrically by finding a line that passed through two points, finding the third intersection and then reflecting along the $y$-axis.

It turns out that there is an efficient algorithm for calculating the point addition law for an elliptic curve.

Taken from "An Introduction to Mathematical Cryptography", *Jeffrey Hoffstein, Jill Pipher, Joseph H. Silverman*, the following algorithm will calculate the addition of two points on an elliptic curve

```text
**Algorithm for the addition of two points: P + Q**

(a) If P = O, then P + Q = Q.
(b) Otherwise, if Q = O, then P + Q = P.
(c) Otherwise, write P = (x_{1}, y_{1}) and Q = (x_{2}, y_{2}).
(d) If x_{1} = x_{2} and y_{1} = -y_{2}, then P + Q = O.
(e) Otherwise:
(e1) if P \neq Q: \lambda = (y_{2} - y_{1}) / (x_{2} - x_{1})
(e2) if P = Q: \lambda = (3x_{1}^2 + a) / 2y_{1}
(f) x_{3} = lambda^2 - x_{1} - x_{2}
(h) y_{3} = lambda(x_{1} -x_{3}) - y_{1}
(i) P + Q = (x_{3}, y_{3})
```

> We are working with a finite field, so the above calculations should be done modulo $p$, and we do not "divide" by an integer, we instead multiply by the modular inverse of a number. e.g. $5^{-1} \equiv 9 \mod 11$.

We will work with the following elliptic curve, and prime:

$$
E: Y^{2} = X^{3} + 497 X + 1768 \mod 9739
$$

> You can test your algorithm by asserting: $X + Y = (1024, 4440)$ and $X + X = (7284, 2107)$ for $X = (5274, 2841)$ and $Y = (8669, 740)$.

Using the above curve, and the points $P = (493, 5564), Q = (1539, 4742), R = (4403,5202)$, find the point $S(x,y) = P + P + Q + R$ by implementing the above algorithm.

> After calculating $S$, substitute the coordinates into the curve. Assert that the point $S$ is in $E(\mathbb{F}_p)$
