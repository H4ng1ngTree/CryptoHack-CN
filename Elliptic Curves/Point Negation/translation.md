# Point Negation

**10 分 - 6118 人解决**

来源：<https://cryptohack.org/challenges/ecc/>

## 中文翻译

在 starter 系列题目中，统一使用如下椭圆曲线：

$$
E : Y^2 = X^3 + 497X + 1768 \pmod{9739}
$$

给定：

$$
P=(8045,6936)
$$

请寻找点 $Q(x,y)$，使得：

$$
P+Q=O
$$

> 注意：当前运算发生在有限域中，因此负坐标需要在模 $p$ 的意义下处理。

在此输入 flag：`crypto{x,y}`
