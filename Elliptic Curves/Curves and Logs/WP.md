## Hint

- 先想清楚什么是 ECDLP：已知 P 和 Q，要反推出 Q = [n]P 里的 n。
- 这题的通信过程和 DH 很像：双方在不安全信道里公开交换信息，但最后能算出同一个共享秘密。
- 题目最后不要拿整个点去哈希，只取共享秘密的 x 坐标，把这个整数转成字符串后做 SHA1。

## 思路

这题其实就是把上一题的标量乘法放进 ECDH 里用一次。

Alice 发来的是：

```text
Q_A = (815, 3190)
```

我的私钥是：

```text
n_B = 1829
```

按照 ECDH 的流程，Bob 这边要算的是：

\[
S = [n_B]Q_A
\]

也就是把 Alice 的公钥点 Q_A 乘上自己的私钥 n_B。这里不用去反推 Alice 的 n_A，因为 ECDLP 本来就是难反推的；我们只需要正常做标量乘法。

算出来共享秘密以后，题目要求取它的 x 坐标。这里容易看错：不是把整个点拼起来，也不是 hash `(x, y)`，而是只把 x 这个整数转成字符串，再算 SHA1。

## 代码

核心就是复用点加法和 double-and-add：

```python
A = 497
B = 1768
MOD = 9739

QA = (815, 3190)
nB = 1829

S = scalar_multiplication(QA, nB, A, MOD)
shared_x = S[0]
flag = sha1(str(shared_x).encode()).hexdigest()
```

完整代码见本页下方的 `WP.py` 下载链接。

## Result

```text
shared secret: (7929, 707)
shared x: 7929
80e5212754a824d3a4aed185ace4f9cac0f908bf
```

## Flag

```text
80e5212754a824d3a4aed185ace4f9cac0f908bf
```
