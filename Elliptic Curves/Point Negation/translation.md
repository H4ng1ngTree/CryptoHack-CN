# Point Negation

**10 分 - 6118 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

在背景部分中，我们已经介绍了如何把椭圆曲线上的点加法看作一种阿贝尔群运算。在那个几何图像中，我们允许曲线坐标取任意实数。

为了把椭圆曲线应用于密码学场景，我们研究坐标位于有限域 $\mathbb{F}_p$ 中的椭圆曲线。

我们仍然考虑如下形式的椭圆曲线：$E: Y^{2} = X^{3} + a X + b$。它需要满足 $a,b \in \mathbb{F}_p$，并且 $4a^{3} + 27 b^{2} \neq 0$。不过，我们现在不再把椭圆曲线看作几何对象，而是把它看作由如下点构成的集合：

$$
E(\mathbb{F}_p) = \{(x,y) : x,y \in \mathbb{F}_p \textrm{ satisfying } y^{2} = x^{3} + a x + b \} \cup O
$$

> 注意：背景部分介绍的内容仍然成立。群的单位元仍是无穷远点 $O$，加法法则也保持不变。给定 $E(\mathbb{F}_p)$ 中的两个点，加法法则会产生另一个仍属于 $E(\mathbb{F}_p)$ 的点。

在 starter 系列的所有挑战中，我们都将使用如下椭圆曲线：

$$
E: Y^{2} = X^{3} + 497 X + 1768 \mod 9739
$$

使用上述曲线，以及点 $P(8045,6936)$，请寻找点 $Q(x,y)$，使得 $P + Q = O$。

> 请记住：我们现在是在有限域中工作，因此需要正确处理负数。

**资源：**

- [The Animated Elliptic Curve: Visualizing Elliptic Curve Cryptography](https://curves.xargs.org/)
