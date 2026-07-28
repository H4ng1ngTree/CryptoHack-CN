## Hint

- 根据题目给出的 Double and Add 算法，可以直接写出对应代码。
- 这题本质上还是点加法，只是把“重复加很多次”优化成二进制展开。

## 思路

题目要算的是：

```text
Q = [7863]P
```

如果真的把 $P$ 加 7863 次，当然也能做，但是太笨了。题目给的 Double and Add 算法就是在利用二进制：

- 如果当前 $n$ 是奇数，就把当前的 $Q$ 加进结果 $R$。
- 每一轮都把 $Q$ 倍点，也就是变成 $[2]Q$。
- 然后令 $n = n // 2$，继续看下一位。

这里的 `R = None` 还是表示无穷远点 $O$，这样第一次做 `R + Q` 的时候就能直接得到 $Q$。

## 代码

```python
def scalar_multiplication(P, n, a, p):
    Q = P
    R = None

    while n > 0:
        if n % 2 == 1:
            R = point_add(R, Q, a, p)

        Q = point_add(Q, Q, a, p)
        n //= 2

    return R
```

完整代码见本页下方的 `WP.py` 下载链接。

## Result

```text
(9467, 2742)
crypto{9467,2742}
```

## Flag

```text
crypto{9467,2742}
```