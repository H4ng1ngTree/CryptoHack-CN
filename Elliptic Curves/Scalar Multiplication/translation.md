# Scalar Multiplication

**35 分 - 4950 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

标量乘法可以理解为对同一点进行重复加法，例如：

$$
[3]P=P+P+P
$$

本题引入 double-and-add 算法。

```text
输入：P in E(F_p)，整数 n > 0
输出：Q = [n]P in E(F_p)

1. 令 Q = P，R = O。
2. 当 n > 0 时：
   3. 如果 n = 1 mod 2，则令 R = R + Q。
   4. 令 Q = [2]Q，并令 n = floor(n / 2)。
   5. 当 n > 0 时继续循环。
6. 返回 R。
```

使用：

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739}
$$

> 测试数据：当 $X=(5323,5438)$ 时，应验证 $[1337]X=(1089,6931)$。

给定 $P=(2339,2213)$，求 $Q(x,y)=[7863]P$。

在此输入 flag：`crypto{x,y}`
