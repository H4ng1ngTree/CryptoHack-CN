# Point Negation

**10 pts - 6125 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Original challenge

In the background section, we covered the basics of how we can view point addition over an elliptic curve as being an abelian group operation. In this geometric picture we allowed the coordinates on the curve to be any real number.

To apply elliptic curves in a cryptographic setting, we study elliptic curves which have coordinates in a finite field $\mathbb{F}_p$.

We will still be considering elliptic curves of the form $E: Y^{2} = X^{3} + a X + b $, which satisfy the following conditions: $a,b \in \mathbb{F}_p$ and $4a^{3} + 27 b^{2} \neq 0$. However, we no longer think of the elliptic curve as a geometric object, but rather a set of points defined by

$$
E(\mathbb{F}_p) = \{(x,y) : x,y \in \mathbb{F}_p \textrm{ satisfying } y^{2} = x^{3} + a x + b \} \cup O
$$

> Note: Everything we covered in the background still holds. The identity of the group is the point at infinity: $O$, and the addition law is unchanged. Given two points in $E(\mathbb{F}_p)$, the addition law will generate another point in $E(\mathbb{F}_p)$.

For all the challenges in the starter set, we will be working with the elliptic curve

$$
E: Y^{2} = X^{3} + 497 X + 1768 \mod 9739
$$

Using the above curve, and the point $P(8045,6936)$, find the point $Q(x,y)$ such that $P + Q = O$.

> Remember, we're working in a finite field now, so you'll need to correctly handle negative numbers.

**Resources:**
- [The Animated Elliptic Curve: Visualizing Elliptic Curve Cryptography](https://curves.xargs.org/)
