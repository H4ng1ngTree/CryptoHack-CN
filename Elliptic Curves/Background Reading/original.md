# Background Reading

**5 pts - 7039 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

This introductory challenge explains the motivation for elliptic curve cryptography and introduces elliptic curves in short Weierstrass form:

$$
E : Y^2 = X^3 + aX + b
$$

The page presents point addition geometrically: draw a line through two points, find the third intersection with the curve, and reflect that point to obtain the sum. For point doubling, use the tangent line at the point.

The point at infinity $O$ is introduced as the identity element. The elliptic-curve group operation satisfies:

```text
P + O = O + P = P
P + (-P) = O
(P + Q) + R = P + (Q + R)
P + Q = Q + P
```

For curves over finite fields, the curve is considered as a finite set of points with coordinates in $\mathbb{F}_p$, together with $O$.

The flag asks for the mathematical name of a group whose operation is commutative.
