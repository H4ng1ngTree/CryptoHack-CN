from hashlib import sha1

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# ============================================================
# 0. 题目给的数据
# ============================================================

p = Integer(99061670249353652702595159229088680425828208953931838069069584252923270946291)
a = Integer(1)
b = Integer(4)

E = EllipticCurve(GF(p), [a, b])
G = E(
    43190960452218023575787899214023014938926631792651638044680168600989609069200,
    20971936269255296908588589778128791635639992476076894152303569022736123671173,
)

ax = Integer(87360200456784002948566700858113190957688355783112995047798140117594305287669)
bx = Integer(6082896373499126624029343293750138460137531774473450341235217699497602895121)

iv = "ceb34a8c174d77136455971f08641cc5"
encrypted_flag = "b503bf04df71cfbd3f464aec2083e9b79c825803a4d4a43697889ad29eb75453"

BOUND = 2^64


# ============================================================
# 1. 用小因子 + CRT 恢复 64-bit 私钥
# ============================================================

def recover_secret_by_crt(A):
    """已知 A = [n]G 且 n < 2^64，用小子群离散对数 + CRT 恢复 n。"""
    N = G.order()
    residues = []
    moduli = []
    modulus_product = Integer(1)

    print("[1] G order:")
    print(N)
    print()

    print("[2] factor(G order):")
    print(factor(N))
    print()

    for q, e in factor(N):
        q_power = Integer(q)^Integer(e)

        # 投影到阶为 q_power 的小子群。
        Gq = (N // q_power) * G
        Aq = (N // q_power) * A

        # Aq = [n]Gq，所以这里求出来的是 n mod q_power。
        r = discrete_log(Aq, Gq, ord=q_power, operation='+')

        residues.append(Integer(r))
        moduli.append(q_power)
        modulus_product *= q_power

        print(f"[3] nA mod {q_power} = {r}")
        print(f"    current modulus product = {modulus_product}")
        print()

        # 乘积超过 2^64 后，64-bit 范围内最多只剩一个候选。
        if modulus_product > BOUND:
            break

    n = Integer(crt(residues, moduli))
    return n, modulus_product


# 题目只给了 Alice 公钥的 x 坐标。
# 同一个 x 可能对应 A 和 -A，所以两个 lift 出来的点都试一下。
nA = None
used_modulus = None

for A in E.lift_x(ax, all=True):
    candidate, M = recover_secret_by_crt(A)

    print("[4] CRT candidate:")
    print(candidate)
    print()

    if candidate < BOUND and (candidate * G).xy()[0] == ax:
        nA = candidate
        used_modulus = M
        print("[5] found Alice private nA:")
        print(nA)
        print()
        break

if nA is None:
    raise ValueError("failed to recover Alice private key")

print("[6] modulus product > 2^64:")
print(used_modulus > BOUND)
print()

print("[7] check public x:")
print((nA * G).xy()[0] == ax)
print()


# ============================================================
# 2. 用 Alice 私钥和 Bob 公钥恢复共享秘密
# ============================================================

# Bob 也只发了 x 坐标。这里任意 lift 一个 y 都可以，
# 因为 B 和 -B 乘出来的点互为相反点，x 坐标相同。
B = E.lift_x(bx)
S = nA * B
shared_secret = Integer(S.xy()[0])

print("[8] shared x:")
print(shared_secret)
print()


# ============================================================
# 3. 按源码 AES-CBC 解密
# ============================================================

key = sha1(str(shared_secret).encode("ascii")).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
flag = unpad(cipher.decrypt(bytes.fromhex(encrypted_flag)), 16).decode()

print("[9] flag:")
print(flag)
