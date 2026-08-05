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
