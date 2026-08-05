## Hint

- 这题和 Smooth Criminal 不一样，不是看 `G.order()` 能不能拆。题目甚至专门写了：

  ```sage
  assert is_prime(E.order())
  ```

  所以 Pohlig-Hellman 那条路基本走不通。

- 但它只检查了 `E.order()` 是素数，没有避开更危险的情况：

  ```sage
  E.order() == p
  ```

  如果曲线阶刚好等于底层有限域的模数 `p`，这条曲线就是 anomalous curve，也叫 trace one curve，可以用 Smart Attack。

- 这里先把几个术语按做题需要理解一下：

  ```text
  GF(p)：只看 mod p 的有限域世界。
  Qp：p-adic 数域，不只看 mod p，还会继续看 mod p^2, mod p^3, ...
  lift：不是把 GF(p) 直接变成 Qp，而是把曲线和点抬到 Qp 里，要求它们 mod p 看回去还是原来的曲线和点。
  ```

- 为什么要 lift 到 `Qp`？因为在 `GF(p)` 里，如果 `E.order() = p`，那么：

  ```text
  [p]G = O
  [p]A = O
  ```

  两个点都塌成无穷远点 `O`，信息没了。lift 到 `Qp` 之后再算 `[p]G` 和 `[p]A`，它们不是完全等于 `O`，而是两个“mod p 看起来像 O”的近 O 点。这个时候，GF(p) 看不见的高阶 p-adic 信息还在。

- `p-adic` 的“近”不是普通距离近，而是看差值能被多少个 `p` 整除。比如在 `5-adic` 里：

  ```text
  6 - 1 = 5
  26 - 1 = 25 = 5^2
  126 - 1 = 125 = 5^3
  ```

  所以 `126` 和 `1` 普通意义下很远，但在 `5-adic` 里很近，因为它们一直像到 `mod 125` 这一层。不过它们不是完全一样，因为到 `mod 625` 就分开了。

- Smart Attack 最抽象的地方是：靠近 `O` 的时候，椭圆曲线点加法可以近似变成普通加法。这里用的局部参数一般写成：

  $$
  z(P) = -\frac{x(P)}{y(P)}
  $$

  在 `O` 附近可以理解成：

  ```text
  z(P + Q) ≈ z(P) + z(Q)
  ```

  所以如果：

  ```text
  A = [n]G
  ```

  lift 到 `Qp` 后两边乘 `p`：

  ```text
  [p]A = [n]([p]G)
  ```

  再用 `z = -x/y` 线性化，就变成：

  ```text
  z([p]A) = n * z([p]G)
  ```

  最后直接除：

  ```text
  n = z([p]A) / z([p]G)
  ```

  这就是 Smart Attack 的核心。

## 思路

题目输出里给了两个关键点：

```text
Generator: G
Public Key: A
```

源码里生成公钥的逻辑是：

```sage
private = randint(1, E.order() - 1)
public = G * private
```

所以：

$$
A = [n_A]G
$$

我们的目标就是先用 Smart Attack 从 `G` 和 `A` 里求出 `n_A`。

先检查曲线：

```sage
print(E.order() == p)
```

如果这里是 `True`，说明这条曲线是 anomalous curve。然后用 Smart Attack：

```sage
nA = smart_attack(G, A)
```

拿到 `nA` 后，后面就和前面的 ECDH 题一样了。源码里共享秘密是：

```sage
secret = shared_secret(B, nA)
```

也就是：

$$
S = [n_A]B
$$

然后取 `S.x`，按源码方式生成 AES key：

```python
key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
```

最后用题目给的 `iv` 和 `encrypted_flag` 做 AES-CBC 解密。

<p class="download-row"><a class="download-link" href="./WP.sage" download>下载解题代码（WP.sage）</a></p>

## 代码

这题要用 Sage，保存成 `WP.sage` 后运行：

```bash
sage WP.sage
```

```python
from hashlib import sha1
from random import randint

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# ============================================================
# 0. 题目给的数据
# ============================================================

p = 0xa15c4fb663a578d8b2496d3151a946119ee42695e18e13e90600192b1d0abdbb6f787f90c8d102ff88e284dd4526f5f6b6c980bf88f1d0490714b67e8a2a2b77
a = 0x5e009506fcc7eff573bc960d88638fe25e76a9b6c7caeea072a27dcd1fa46abb15b7b6210cf90caba982893ee2779669bac06e267013486b22ff3e24abae2d42
b = 0x2ce7d1ca4493b0977f088f6d30d9241f8048fdea112cc385b793bce953998caae680864a7d3aa437ea3ffd1441ca3fb352b0b710bb3f053e980e503be9a7fece

E = EllipticCurve(GF(p), [a, b])

# output.txt 里打印出来的 Generator
G = E(
    3034712809375537908102988750113382444008758539448972750581525810900634243392172703684905257490982543775233630011707375189041302436945106395617312498769005,
    4986645098582616415690074082237817624424333339074969364527548107042876175480894132576399611027847402879885574130125050842710052291870268101817275410204850,
)

# output.txt 里打印出来的 Alice public key: A = [nA]G
A = E(
    4748198372895404866752111766626421927481971519483471383813044005699388317650395315193922226704604937454742608233124831870493636003725200307683939875286865,
    2421873309002279841021791369884483308051497215798017509805302041102468310636822060707350789776065212606890489706597369526562336256272258544226688832663757,
)

# source.sage 里 Bob 的 public key
B = E(
    0x7f0489e4efe6905f039476db54f9b6eac654c780342169155344abc5ac90167adc6b8dabacec643cbe420abffe9760cbc3e8a2b508d24779461c19b20e242a38,
    0xdd04134e747354e5b9618d8cb3f60e03a74a709d4956641b234daa8a65d43df34e18d00a59c070801178d198e8905ef670118c15b0906d3a00a662d3a2736bf,
)

iv = "719700b2470525781cc844db1febd994"
encrypted_flag = "335470f413c225b705db2e930b9d460d3947b3836059fb890b044e46cbb343f0"


# ============================================================
# 1. Smart Attack
# ============================================================

def lift_point(Ep, P):
    """把 GF(p) 上的点 P lift 到 Qp 上，要求 y 坐标模 p 后还是原来的 y。"""
    x0, y0 = P.xy()

    candidates = Ep.lift_x(ZZ(x0), all=True)
    for R in candidates:
        if GF(p)(R.xy()[1]) == y0:
            return R

    raise ValueError("point lift failed")


def smart_attack(P, Q):
    """
    已知 Q = [k]P，且 E.order() == p 时，用 Smart Attack 求 k。
    """
    E0 = P.curve()
    assert E0.order() == p

    # 这里不是换一条完全不同的曲线，而是把原曲线 lift 到 Qp。
    # 系数加上 p 的倍数后，mod p 看回去还是同一条曲线。
    # 这样做可以保留 GF(p) 看不见的高阶 p-adic 信息。
    Ep = EllipticCurve(
        Qp(p, 20),
        [ZZ(t) + randint(0, p) * p for t in E0.a_invariants()],
    )

    Pp = lift_point(Ep, P)
    Qp_lift = lift_point(Ep, Q)

    # 因为 E.order() = p，所以在 GF(p) 里 [p]P 和 [p]Q 都是 O。
    # lift 到 Qp 后，它们不是完全等于 O，而是非常接近 O。
    pP = p * Pp
    pQ = p * Qp_lift

    # 在 O 附近，用 z = -x/y 作为局部参数。
    # 这里点加法会被线性化，所以 z([p]Q) = k * z([p]P)。
    xP, yP = pP.xy()
    xQ, yQ = pQ.xy()
    zP = -(xP / yP)
    zQ = -(xQ / yQ)

    k = ZZ(zQ / zP) % p
    return k


print("[1] E.order() == p:")
print(E.order() == p)
print()

nA = smart_attack(G, A)
print("[2] Alice private nA:")
print(nA)
print()

print("[3] check nA * G == A:")
print(nA * G == A)
print()


# ============================================================
# 2. 用 nA 算共享秘密，再按源码 AES-CBC 解密
# ============================================================

S = nA * B
shared_secret = int(S.xy()[0])

print("[4] shared point:")
print(S)
print()

print("[5] shared x:")
print(shared_secret)
print()

key = sha1(str(shared_secret).encode("ascii")).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
flag = unpad(cipher.decrypt(bytes.fromhex(encrypted_flag)), 16).decode("ascii")

print("[6] flag:")
print(flag)
```

## Result

脚本会先检查：

```text
E.order() == p
nA * G == A
```

如果两个检查都没问题，最后会输出解密出来的 flag。