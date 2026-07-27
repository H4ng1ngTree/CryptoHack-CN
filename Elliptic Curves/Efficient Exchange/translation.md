# Efficient Exchange

**50 分 - 4264 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

本题讨论一种椭圆曲线 Diffie-Hellman 交换：Alice 的公钥只发送 $x$ 坐标。

在本组题目中，素数模数满足：

$$
p \equiv 3 \pmod{4}
$$

使用：

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739},\quad G=(1804,5368)
$$

Alice 发送：

$$
x(Q_A)=4726
$$

你的秘密整数为 $n_B=6534$。请计算共享秘密，并结合 `decrypt.py` 与如下数据解密 flag：

```python
{
    'iv': 'cd9da9f1c60925922377ea952afc212c',
    'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'
}
```

## 题目文件

- `decrypt.py`
