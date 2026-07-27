# Montgomery's Ladder

**40 分 - 2229 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

这道侧信道题引入 Montgomery 阶梯这一标量乘法计算方法。

## $E(\mathbb{F}_p)$ 上的 Montgomery 二进制算法

```text
输入：P in E(F_p)，n 位整数 k = sum 2^i k_i，且 k_{n-1}=1
输出：[k]P in E(F_p)

1. 令 (R0, R1) = (P, [2]P)。
2. 对 i 从 n - 2 递减到 0：
   3. 如果 k_i = 0，令 (R0, R1) = ([2]R0, R0 + R1)。
   4. 否则，令 (R0, R1) = (R0 + R1, [2]R1)。
5. 返回 R0。
```

使用如下 Montgomery 形式曲线：

$$
E : Y^2 = X^3 + 486662X^2 + X \pmod{2^{255}-19}
$$

给定 `G.x = 9`，请计算下列点的十进制 $x$ 坐标：

$$
Q=[\texttt{0x1337c0decafe}]G
$$

## Montgomery 曲线的仿射坐标公式

对于：

$$
E : By^2 = x^3 + Ax^2 + x
$$

```text
加法，P != Q：
alpha = (y_2 - y_1) / (x_2 - x_1)
x_3 = B alpha^2 - A - x_1 - x_2
y_3 = alpha(x_1 - x_3) - y_1

倍点：
alpha = (3x_1^2 + 2A x_1 + 1) / (2B y_1)
x_3 = B alpha^2 - A - 2x_1
y_3 = alpha(x_1 - x_3) - y_1
```

> 所有运算都应在模 $p$ 的意义下进行。

在此输入 flag：`crypto{...}`
