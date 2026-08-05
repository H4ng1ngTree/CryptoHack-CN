## Hint

- 这题和 Smooth Criminal 不一样，不是看生成元阶能不能拆。题目专门检查了曲线阶是素数，所以 Pohlig-Hellman 那条路基本走不通。

- 但它只检查了曲线阶是素数，没有避开更危险的情况：曲线阶刚好等于底层有限域的模数 $p$。这种曲线就是 anomalous curve，也叫 trace one curve，可以用 Smart Attack。

- 这里先把几个术语按做题需要理解一下：

  - $GF(p)$：只看 mod $p$ 的有限域世界。
  - $Q_p$：$p$-adic 数域，不只看 mod $p$，还会继续看 mod $p^2, p^3, \cdots$。
  - lift：不是把 $GF(p)$ 直接变成 $Q_p$，而是把曲线和点抬到 $Q_p$ 里，要求它们 mod $p$ 看回去还是原来的曲线和点。

- 为什么要 lift 到 $Q_p$？因为在 $GF(p)$ 里，如果曲线阶等于 $p$，那么 $[p]G$ 和 $[p]A$ 都会塌成无穷远点 $O$，信息没了。lift 到 $Q_p$ 之后再算 $[p]G$ 和 $[p]A$，它们不是完全等于 $O$，而是两个“mod $p$ 看起来像 $O$”的近 $O$ 点。这个时候，$GF(p)$ 看不见的高阶 $p$-adic 信息还在。

- $p$-adic 的“近”不是普通距离近，而是看差值能被多少个 $p$ 整除。比如在 $5$-adic 里，$126$ 和 $1$ 普通意义下很远，但它们的差是 $125 = 5^3$，所以在 $5$-adic 里反而很近。不过它们不是完全一样，因为继续往更高层看还是会分开。

- Smart Attack 最抽象的地方是：靠近 $O$ 的时候，椭圆曲线点加法可以近似变成普通加法。这里用的局部参数一般写成：

  $$
  z(P) = -\frac{x(P)}{y(P)}
  $$

  所以如果：

  $$
  A = [n]G
  $$

  lift 到 $Q_p$ 后两边乘 $p$，再用 $z = -x/y$ 线性化，就能把点乘关系变成一个可以直接相除的关系：

  $$
  n = \frac{z([p]A)}{z([p]G)}
  $$

  这就是 Smart Attack 的核心。

## 思路

题目输出里给了两个关键点：生成元 $G$ 和 Alice 的公钥 $A$。源码里生成公钥的逻辑就是私钥乘生成元，所以有：

$$
A = [n_A]G
$$

我们的目标就是先用 Smart Attack 从 $G$ 和 $A$ 里求出 $n_A$。

先检查曲线阶是不是刚好等于 $p$。如果是，说明这条曲线是 anomalous curve，然后就可以用 Smart Attack 求 Alice 私钥。

拿到 $n_A$ 后，后面就和前面的 ECDH 题一样了。用 Alice 私钥去乘 Bob 的公钥 $B$：

$$
S = [n_A]B
$$

然后取共享点的 $x$ 坐标，按源码方式生成 AES key，最后用题目给的 iv 和 encrypted flag 做 AES-CBC 解密。

## 代码

<p class="download-row"><a class="download-link" href="./WP.sage" download>下载解题代码（WP.sage）</a></p>

## Result

脚本会先检查曲线阶是否等于 $p$，再检查求出来的 Alice 私钥是否能还原公钥 $A$。如果两个检查都没问题，最后会输出解密出来的 flag。
