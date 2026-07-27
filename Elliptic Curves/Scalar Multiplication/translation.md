# Scalar Multiplication

**35 分 - 4953 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

两个点的标量乘法定义为重复加法：$[3]P = P + P + P$。

在接下来的几道题中，我们会使用标量乘法，以类似 Diffie-Hellman 题目的方式，在不安全信道上建立共享秘密。

下面的算法摘自 Jeffrey Hoffstein、Jill Pipher 与 Joseph H. Silverman 合著的 *An Introduction to Mathematical Cryptography*，它可以高效计算椭圆曲线上一点的标量乘法。

```text
Double and Add 标量乘法算法

输入：P \in E(\mathbb{F}_p)，整数 n > 0
输出：Q = [n]P \in E(\mathbb{F}_p)

1. 令 Q = P，R = O。
2. 当 n > 0 时循环。
3. 如果 n \equiv 1 \mod 2，则令 R = R + Q。
4. 令 Q = [2]Q，并令 n = floor(n/2)。
5. 如果 n > 0，回到第 2 步继续循环。
6. 返回点 R，此时 R = [n]P。
```

> 这并不是最高效的算法。还有许多有趣的方法可以改进这一计算，但它已经足以支撑我们接下来的工作。

我们将使用如下椭圆曲线和素数模数：

$$
E: Y^2 = X^3 + 497 X + 1768 \mod 9739
$$

> 你可以用如下断言测试自己的算法：当 $X = (5323, 5438)$ 时，应有 $[1337] X = (1089, 6931)$。

使用上述曲线，以及点 $P = (2339, 2213)$，请实现上述算法，并求出点 $Q(x,y) = [7863] P$。

> 计算得到 $Q$ 后，请将坐标代回曲线。验证点 $Q$ 属于 $E(\mathbb{F}_p)$。
