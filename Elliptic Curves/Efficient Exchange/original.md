# Efficient Exchange

**50 pts - 4264 Solves**

Source: <https://cryptohack.org/challenges/ecc/>

## Clean transcription

This challenge considers an elliptic-curve Diffie-Hellman exchange in which only the $x$-coordinate of Alice's public key is sent.

For these challenges, the prime satisfies:

$$
p \equiv 3 \pmod{4}
$$

Use:

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739},\quad G=(1804,5368)
$$

Alice sends:

$$
x(Q_A)=4726
$$

Your secret integer is $n_B=6534$. Compute the shared secret and use `decrypt.py` with:

```python
{
    'iv': 'cd9da9f1c60925922377ea952afc212c',
    'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'
}
```

## Challenge files

- `decrypt.py`
