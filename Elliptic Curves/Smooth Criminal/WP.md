## Hint

- 题干名字叫 Smooth Criminal，基本就是在暗示这题和 smooth 有关。
- 这里的 smooth 不是去拆模数 `p`，而是去看基点 `G` 的阶 `G.order()`。因为我们要求的是 `P = [n]G` 里的 `n`，这个离散对数问题发生在 `G` 生成的循环子群里，所以真正影响难度的是 `G` 的阶。
- 如果 `G.order()` 能分解成很多小因子，Sage 就可以把椭圆曲线离散对数拆开算，最后再用 CRT 拼回去。
- AES 那一段不用猜，直接按源码里的通路接：先算共享点 `[n]B`，取它的 x 坐标，`SHA1` 后截前 16 字节当 AES key，然后用题目给的 `iv` 和 `encrypted_flag` 解密。

## 思路

这题我一开始也容易把几个点搞混。题目输出的这个点：

```text
Point(x=280810182131414898730378982766101210916, y=291506490768054478159835604632710368904)
```

不是 `G`，也不是最终的 shared secret。结合源码看，它其实是 Alice 发给 Bob 的公钥，也就是：

$$
P = [n]G
$$

所以我们真正要做的第一步，是从 `P` 和 `G` 里面把 Alice 的私钥 `n` 找回来。

正常情况下，椭圆曲线离散对数很难直接求。但是这题的问题出在 `G` 的阶上。我们先看：

```python
N = G.order()
print(factor(N))
```

这里分解出来是：

```text
2^2 * 3^7 * 139 * 165229 * 31850531 * 270778799 * 179317983307
```

这个阶比较光滑，所以 `P = [n]G` 这个离散对数就能拆成小问题。手写的话大概是：对每个因子分别求 `n` 的同余，然后用 CRT 合起来。这里我就直接让 Sage 做这一步：

```python
n = P.log(G)
```

这行看起来很短，但它背后已经把分解、分段求离散对数、CRT 这些事情包掉了。所以脚本里看不到手写的 CRT，不是没用，而是 Sage 在 `log` 里面帮我们做了。

拿到 `n` 之后，就可以按源码继续走了。源码里加密用的是：

```python
shared_secret = gen_shared_secret(B, n)
```

而 `gen_shared_secret(B, n)` 本质上就是算：

$$
S = [n]B
$$

然后取 `S.x` 当共享秘密。最后 AES 的 key 生成方式也要和源码完全一致：

```python
key = sha1(str(shared_secret).encode('ascii')).digest()[:16]
```

`iv` 和 `encrypted_flag` 是十六进制字符串，而 `AES.new()` 和 `decrypt()` 要吃的是 bytes，所以这里还要用 `bytes.fromhex(...)` 转一下。

<p class="download-row"><a class="download-link" href="./WP.sage" download>下载解题代码（WP.sage）</a></p>

## 代码

完整脚本如下。这里用的是 Sage 环境，保存成 `WP.sage` 后用：

```bash
sage WP.sage
```

```python
from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# ============================================================
# 0. 题目给的数据
# ============================================================

# 曲线是 y^2 = x^3 + 2x + 3 mod p
p = 310717010502520989590157367261876774703
a = 2
b = 3
E = EllipticCurve(GF(p), [a, b])

# 题目源码里的基点 G
G = E(
    179210853392303317793440285562762725654,
    105268671499942631758568591033409611165,
)

# output.txt 里打印出来的点
# 它不是 G，也不是 shared secret
# 它是 Alice 的公钥：P = [n]G
P = E(
    280810182131414898730378982766101210916,
    291506490768054478159835604632710368904,
)

# Bob 的公钥，源码里给了
B = E(
    272640099140026426377756188075937988094,
    51062462309521034358726608268084433317,
)

# output.txt 里的密文数据
iv = "07e2628b590095a5e332d397b8a59aa7"
encrypted_flag = "8220b7c47b36777a737f5ef9caa2814cf20c1c1ef496ec21a9b4833da24a008d0870d3ac3a6ad80065c138a2ed6136af"


# ============================================================
# 1. 看 G 的阶
# ============================================================

# G.order() 表示最小的 N，使得 [N]G = O
# 因为 P = [n]G，所以 n 实际上是在 mod N 的意义下循环
N = G.order()
print("[1] G order:")
print(N)
print()

# factor(N) 是把 N 分解成素因子
# 如果分出来都是小因子，说明这个阶很 smooth
print("[2] factor(G order):")
print(factor(N))
print()


# ============================================================
# 2. 从 P = [n]G 里求出 n
# ============================================================

# 这里 Sage 会帮我们做离散对数
# 也就是求 n，使得 P = [n]G
#
# 这一步背后大概就是：
#   - 分解 G 的阶
#   - 对小因子分别求 n 的同余
#   - 用 CRT 拼回 n
n = P.log(G)

print("[3] Alice secret n:")
print(n)
print()

# 这一步只是检查刚才求出来的 n 对不对
# 如果 n * G == P，说明确实找回了 Alice 的私钥
print("[4] check n * G == P:")
print(n * G == P)
print()


# ============================================================
# 3. 用 n 和 Bob 的公钥 B 算共享秘密
# ============================================================

# 源码里真正用于加密的是：
#   shared_secret = gen_shared_secret(B, n)
#
# gen_shared_secret(B, n) 内部其实就是：
#   S = [n]B
#   return S.x
S = n * B
shared_secret = int(S[0])

print("[5] shared point = [n]B:")
print(S)
print()

print("[6] shared x:")
print(shared_secret)
print()


# ============================================================
# 4. 按源码里的方式生成 AES key
# ============================================================

# 源码里是：
#   sha1.update(str(shared_secret).encode('ascii'))
#   key = sha1.digest()[:16]
#
# 所以这里也要一样：
#   先把 shared_secret 转成字符串
#   再 SHA1
#   最后取前 16 字节作为 AES key
key = sha1(str(shared_secret).encode('ascii')).digest()[:16]


# ============================================================
# 5. AES-CBC 解密
# ============================================================

# 题目给的 iv 和 encrypted_flag 都是 hex 字符串
# AES 需要 bytes，所以要 bytes.fromhex(...)
iv_bytes = bytes.fromhex(iv)
ct = bytes.fromhex(encrypted_flag)

# 用同一个 key 和 iv 创建 AES-CBC 解密器
cipher = AES.new(key, AES.MODE_CBC, iv_bytes)

# 解密后还要 unpad，因为源码加密前用了 pad(FLAG, 16)
pt = cipher.decrypt(ct)
flag = unpad(pt, 16).decode()

print("[7] flag:")
print(flag)
```

## Result

运行之后关键输出是：

```text
[6] shared x:
171172176587165701252669133307091694084

[7] flag:
crypto{n07_4ll_curv3s_4r3_s4f3_curv3s}
```

## Flag

```text
crypto{n07_4ll_curv3s_4r3_s4f3_curv3s}
```
