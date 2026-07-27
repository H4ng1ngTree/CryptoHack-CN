---
layout: default
title: Point Negation
---

# Point Negation

## 原文题目

Using the above curve, and the point `P(8045, 6936)`, find the point `Q(x, y)` such that `P + Q = O`.

Remember, we're working in a finite field now, so you'll need to correctly handle negative numbers.

## 翻译题目

给定上面的椭圆曲线，以及点 `P = (8045, 6936)`，求点 `Q(x, y)`，使得：

```text
P + Q = O
```

这里的 `O` 是无穷远点。注意现在是在有限域里运算，所以要正确处理负数取模。

## 我的个人解答

### 1. 先想最笨的方法

你可以把所有点都试一遍，看哪个点和 `P` 相加后变成 `O`。  
但这太慢了，因为模数 `9739` 下可能性很多。

### 2. 关键规律

椭圆曲线里，点的逆元是：

```text
(x, y) -> (x, -y mod p)
```

也就是：

- `x` 不变
- `y` 变成模 `p` 下的相反数

### 3. 小例子

如果模数是 `7`，点是：

```text
(3, 2)
```

那么它的逆元是：

```text
(3, -2 mod 7) = (3, 5)
```

因为 `2 + 5 = 7 ≡ 0 (mod 7)`。

### 4. 回到本题

```text
p = 9739
P = (8045, 6936)
```

所以：

```text
Q = (8045, -6936 mod 9739)
```

计算：

```text
9739 - 6936 = 2803
```

因此：

```text
Q = (8045, 2803)
```

## Flag

```text
crypto{8045,2803}
```

## 代码思路

只要做一次取负：

```python
p = 9739
x, y = 8045, 6936
q = (x, (-y) % p)
print(q)
```

