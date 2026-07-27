# Point Addition

30 pts · 5449 Solves

While working with elliptic curve cryptography, we will need to add points together. In the background challenges, we did this geometrically by finding a line that passed through two points, finding the third intersection and then reflecting along the y-axis.

It turns out that there is an efficient algorithm for calculating the point addition law for an elliptic curve.

Taken from "An Introduction to Mathematical Cryptography", Jeffrey Hoffstein, Jill Pipher, Joseph H. Silverman, the following algorithm will calculate the addition of two points on an elliptic curve.

## Algorithm for the addition of two points: `P + Q`

(a) If `P = O`, then `P + Q = Q`.

(b) Otherwise, if `Q = O`, then `P + Q = P`.

(c) Otherwise, write `P = (x_1, y_1)` and `Q = (x_2, y_2)`.

(d) If `x_1 = x_2` and `y_1 = -y_2`, then `P + Q = O`.

(e) Otherwise:

- (e1) if `P ≠ Q`: `λ = (y_2 - y_1) / (x_2 - x_1)`
- (e2) if `P = Q`: `λ = (3x_1^2 + a) / 2y_1`

(f) `x_3 = λ^2 - x_1 - x_2`

(h) `y_3 = λ(x_1 - x_3) - y_1`

(i) `P + Q = (x_3, y_3)`

We are working with a finite field, so the above calculations should be done modulo `p`, and we do not "divide" by an integer, we instead multiply by the modular inverse of a number. e.g. `5^{-1} ≡ 9 mod 11`.

We will work with the following elliptic curve, and prime:

```text
E: Y^2 = X^3 + 497X + 1768 mod 9739
```

You can test your algorithm by asserting: `X + Y = (1024, 4440)` and `X + X = (7284, 2107)` for `X = (5274, 2841)` and `Y = (8669, 740)`.

Using the above curve, and the points `P = (493, 5564)`, `Q = (1539, 4742)`, `R = (4403, 5202)`, find the point `S(x, y) = P + P + Q + R` by implementing the above algorithm.

After calculating `S`, substitute the coordinates into the curve. Assert that the point `S` is in `E(F_p)`.

Enter flag here: `crypto{x,y}`
