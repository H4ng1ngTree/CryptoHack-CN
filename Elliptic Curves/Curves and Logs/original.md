# Curves and Logs

**40 pts - 4712 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

This challenge introduces the elliptic-curve discrete logarithm problem and elliptic-curve Diffie-Hellman key exchange.

Use:

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739},\quad G=(1804,5368)
$$

Alice sends:

$$
Q_A=(815,3190)
$$

Your secret integer is:

$$
n_B=1829
$$

Compute the shared secret. Then hash the decimal string representation of the shared secret's $x$-coordinate with SHA-1. The hexadecimal digest is the flag.

> The starter curve is intentionally small and not cryptographically secure.
