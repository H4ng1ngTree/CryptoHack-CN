# Montgomery's Ladder

**40 分 - 2230 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

这一分类中包含许多不安全的椭圆曲线密码实现。选择糟糕的曲线会导致协议被破坏，并带来有趣的谜题；但即使所选曲线本身是安全的，私钥仍然可能从设备中被提取出来。

学习私密信息的一种技术是侧信道分析。从高层来看，当系统使用秘密值执行操作时，可能会通过耗时、电路完成的工作量等数据泄漏关于该秘密的信息。

针对 ECDSA 签名的计时攻击可能泄漏 nonce 的信息；再结合诸如 [LadderLeak](https://eprint.iacr.org/2020/615.pdf) 这样的复杂攻击，可能对协议造成致命影响。为了防御这类攻击，人们做了大量工作，使椭圆曲线点的标量乘法以常数时间方式运行。

椭圆曲线上点标量乘法的常数时间算法中，一个关键组成部分基于 Montgomery 阶梯。本题的目标是在群 $E(\mathbb{F}_p)$ 中实现其最基础版本：Montgomery 二进制算法。

```text
群 E(F_p) 中的 Montgomery 二进制算法

输入：P \in E(F_p)，以及 n 位整数 k = sum 2^i k_i，其中 k_{n-1} = 1
输出：[k]P \in E(F_p)

1. 将 (R_0, R_1) 设为 (P, [2]P)
2. 对 i 从 n - 2 递减到 0：
3.   如果 k_i = 0：
4.       将 (R_0, R_1) 设为 ([2]R_0, R_0 + R_1)
5.   否则：
6.       将 (R_0, R_1) 设为 (R_0 + R_1, [2]R_1)
7. 返回 R_0
```

> 从高层看，请注意：无论 $k$ 的当前比特是什么，每一步都会同时执行一次倍点和一次加法操作。可以将其与 starter 挑战中的 double-and-add 算法作比较。当然这里仍然存在一些明显问题：执行步数会泄漏 $k$ 的比特长度，而且算法中仍有 `if` 分支，分支行为可能泄漏 $k$ 的比特结构。感兴趣的学习者可以参考 [Montgomery curves and their arithmetic](https://eprint.iacr.org/2017/212.pdf) 中的算法 8，对实现进行改进。

我们将使用如下椭圆曲线：

$$
E: Y^{2} = X^{3} + 486662 X^{2} + X \mod 2^{255} - 19
$$

使用上述曲线，以及满足 `G.x = 9` 的生成点，请实现上述算法，并求出点 `Q = [0x1337c0decafe] G` 的 $x$ 坐标（十进制表示）。

这条曲线是 Montgomery 形式，而不是本系列许多题中使用的 Weierstrass 形式。虽然可以把这条曲线映射到 Weierstrass 形式，并复用旧的倍点与加法公式，但我们建议直接使用 Montgomery 曲线的公式：$E : By^{2} = x^{3} + Ax^{2} + x$。为此，题面给出了该曲线在仿射坐标中的加法和倍点公式。若想了解一组优美且快速的射影坐标公式，请参考 [Montgomery curves and the Montgomery ladder](https://eprint.iacr.org/2017/293.pdf)。

```text
Montgomery 曲线加法公式（仿射坐标）

输入：P, Q \in E(F_p)，且 P \neq Q
输出：R = (P + Q) \in E(F_p)

(x_1, y_1), (x_2, y_2) = P, Q
alpha = (y_{2} - y_{1}) / (x_{2} - x_{1})
x_{3} = B alpha^{2} - A - x_{1} - x_{2}
y_{3} = alpha (x_{1} - x_{3}) - y_{1}
R = (x_{3}, y_{3})
```

```text
Montgomery 曲线倍点公式（仿射坐标）

输入：P \in E(F_p)
输出：R = [2]P \in E(F_p)

(x_1, y_1) = P
alpha = (3x^{2}_{1} + 2Ax_{1} + 1) / (2By_{1})
x_{3} = B alpha^{2} - A - 2x_{1}
y_{3} = alpha(x_{1} - x_{3}) - y_{1}
R = (x_{3}, y_{3})
```

注意：所有运算都在模 $p$ 的意义下进行。

> 关于 Montgomery 阶梯的一般介绍，推荐阅读 [Montgomery curves and the Montgomery ladder](https://eprint.iacr.org/2017/293.pdf)。若需要一个清晰的实现算法，推荐结合 [Montgomery curves and their arithmetic](https://eprint.iacr.org/2017/212.pdf) 中的算法 4 `LADDER`、算法 1 `xADD` 和算法 2 `xDBL`。
