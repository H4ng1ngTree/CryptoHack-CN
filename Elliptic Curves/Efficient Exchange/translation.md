# Efficient Exchange

**50 分 - 4266 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

Alice 和 Bob 正在思考椭圆曲线离散对数问题，以及他们在通信中发送的数据。

他们希望尽可能提高数据传输效率，并意识到发送公钥的 $x$ 坐标和 $y$ 坐标并非都是必要的。

只要 Alice 和 Bob 就曲线参数达成一致，那么对给定的 $x$，可能的 $y$ 值最多只有两个。

事实上，从接收到的 $x$ 值出发，无论取哪一个允许的 $y$ 值，共享秘密的 $x$ 坐标都会相同。

> 在这些挑战中，我们使用的素数满足 $p \equiv 3 \mod 4$，这将帮助你从 $y^{2}$ 求出 $y$。

使用如下曲线、素数和生成元：

$$
E: Y^{2} = X^{3} + 497 X + 1768 \mod 9739, \quad G: (1804,5368)
$$

当 Alice 向你发送 $x(Q_A) = 4726$，且你的秘密整数为 $n_B = 6534$ 时，请计算共享秘密。

使用 `decrypt.py` 文件解码 flag。

```text
{'iv': 'cd9da9f1c60925922377ea952afc212c', 'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'}
```

> 你可以只发送一位信息来说明你的公钥 $y$ 坐标取了两个可能值中的哪一个。请思考如何做到这一点：这两个 $y$ 值之间有什么关系？

**题目文件：**

- [decrypt.py](https://cryptohack.org/static/challenges/decrypt_08c0fede9185868aba4a6ae21aca0148.py)
