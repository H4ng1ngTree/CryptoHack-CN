## Hint

- 为什么曲线参数达成一致后，给定一个 $x$ 值，对应的 $y$ 值只可能有两个？
- 为什么题目使用的素数满足 $p \equiv 3 \mod 4$，就能帮助我们从 $y^2$ 求出 $y$？
- 怎么只输入一位信息，就能确定到底是哪一个 $y$？

## 思路

这题最开始卡住的地方，其实就是上面这三个问题。

第一个问题：为什么给定 $x$ 之后，$y$ 只可能有两个？

因为曲线方程是：

$$
Y^2 = X^3 + 497X + 1768 \mod 9739
$$

当 $x$ 已经给定时，右边就是一个确定的数。也就是说，我们只是在有限域里解：

```text
y^2 = rhs
```

平方根最多就是两个，而且它们互为相反数：

```text
y 和 -y mod p
```

第二个问题：为什么 $p \equiv 3 \mod 4$ 有用？

这里用到一个结论：如果 $p \equiv 3 \mod 4$，那么 $a$ 的平方根可以直接写成：

$$
a^{(p+1)/4} \mod p
$$

所以把 Alice 发来的 $x(Q_A) = 4726$ 代入曲线，先算出 $y^2$，再用这个指数把 $y$ 求出来：

```python
rhs = (xA**3 + A * xA + B) % P_MOD
y = pow(rhs, (P_MOD + 1) // 4, P_MOD)
```

第三个问题：怎么只用一位信息来确定是哪一个 $y$？

因为两个候选值是 $y$ 和 $-y \mod p$。它们一奇一偶，所以额外传一位就够了，比如传“这个 $y$ 是奇数还是偶数”，接收方就能从两个候选值里选出正确的那个。这也是压缩椭圆曲线点时常见的思路。

不过本题更省事：题面已经告诉我们，无论选哪一个候选 $y$，最后共享秘密的 $x$ 坐标都一样。因此我们任选一个点作为 $Q_A$，计算：

$$
S = [n_B]Q_A
$$

这里 $n_B = 6534$。最后拿 $S$ 的 $x$ 坐标派生 AES key，再解密即可。

## 代码

核心步骤是先恢复 $y$，再做标量乘法：

```python
xA = 4726
nB = 6534

rhs = (xA**3 + A * xA + B) % P_MOD
y = pow(rhs, (P_MOD + 1) // 4, P_MOD)

QA = (xA, y)
S = scalar_multiplication(QA, nB, A, P_MOD)
shared_x = S[0]
```

完整代码见本页下方的 `WP.py` 下载链接。

## Result

```text
y candidates: 6287, 3452
shared secret: (1791, 2181)
shared secret with other y: (1791, 7558)
shared x: 1791
crypto{3ff1c1ent_k3y_3xch4ng3}
```

## Flag

```text
crypto{3ff1c1ent_k3y_3xch4ng3}
```
