# Point Addition - WP

## Hint

- 无穷远点 $O$ 没有普通的数值坐标，可以在 Python 中用 `None` 表示。
- Python 原生支持元组，所以普通点可以直接写成 `(x, y)`。
- 因为题目工作在有限域 $\mathbb{F}_p$ 中，所有坐标计算都要对 `p` 取模。
- 有限域里不能直接使用普通除法。若公式中出现：

```text
A / B
```

在模 `p` 的意义下应写成：

```python
A * pow(B, -1, p)
```

其中 `pow(B, -1, p)` 表示 `B` 在模 `p` 下的乘法逆元。

## 代码

```python
A = 497
B = 1768
P_MOD = 9739


def point_add(P, Q, a, p):
    """Add two points on y^2 = x^3 + ax + b over F_p.

    The point at infinity O is represented by None.
    """
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P and Q are vertical opposites, so P + Q = O.
    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        slope = (y2 - y1) * pow(x2 - x1, -1, p)
    else:
        slope = (3 * x1**2 + a) * pow(2 * y1, -1, p)

    slope %= p

    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return x3, y3


def is_on_curve(P, a, b, p):
    if P is None:
        return True

    x, y = P
    return (y**2 - (x**3 + a * x + b)) % p == 0


P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

S = point_add(P, P, A, P_MOD)
S = point_add(S, Q, A, P_MOD)
S = point_add(S, R, A, P_MOD)

assert is_on_curve(S, A, B, P_MOD)

print(S)
print("crypto{" + str(S[0]) + "," + str(S[1]) + "}")
```

## Result

```text
(4215, 2162)
crypto{4215,2162}
```
