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
