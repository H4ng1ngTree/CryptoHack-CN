## Hint

- 题目已经给了 Alice 的点 $Q_A$。
- 我这边也知道自己的私钥 $n_B$。
- 所以先算 $[n_B]Q_A$，再拿结果的 x 坐标做 SHA1。

## 思路

这题我就不想太复杂了。

题目给的是 Alice 的公钥点 $Q_A = (815, 3190)$，还有 Bob 自己的私钥 $n_B = 1829$。

那 Bob 这边要算的就是：

$$
S = [n_B]Q_A
$$

也就是直接拿 1829 去乘 Alice 发来的点。

这里没必要去求 Alice 的私钥，因为题目也不是让我们反推那个东西。前面已经写过点加法和标量乘法了，所以这里直接拿来用。

算出来以后共享点是 $S = (7929, 707)$。题目说只要 x 坐标，所以就是 7929。然后对这个 x 坐标做 SHA1，最后把结果放进 `crypto{}` 里。

## 代码

<p class="download-row"><a class="download-link" href="./WP.py" download>下载解题代码（WP.py）</a></p>

## Result

共享点是 $(7929, 707)$，共享 x 坐标是 7929，最后得到：

crypto{80e5212754a824d3a4aed185ace4f9cac0f908bf}

## Flag

crypto{80e5212754a824d3a4aed185ace4f9cac0f908bf}
