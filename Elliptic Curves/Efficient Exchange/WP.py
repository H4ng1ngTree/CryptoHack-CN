from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


A = 497
B = 1768
P_MOD = 9739

xA = 4726
nB = 6534

iv = "cd9da9f1c60925922377ea952afc212c"
encrypted_flag = "febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8"


def point_add(P, Q, a, p):
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and (y1 + y2) % p == 0:
        return None

    if P != Q:
        slope = (y2 - y1) * pow(x2 - x1, -1, p)
    else:
        slope = (3 * x1**2 + a) * pow(2 * y1, -1, p)

    slope %= p
    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return x3, y3


def scalar_multiplication(P, n, a, p):
    Q = P
    R = None

    while n > 0:
        if n % 2 == 1:
            R = point_add(R, Q, a, p)

        Q = point_add(Q, Q, a, p)
        n //= 2

    return R


rhs = (xA**3 + A * xA + B) % P_MOD

# Since p == 3 mod 4, sqrt(rhs) = rhs^((p + 1) // 4) mod p.
y = pow(rhs, (P_MOD + 1) // 4, P_MOD)
y_other = (-y) % P_MOD

QA = (xA, y)
QA_other = (xA, y_other)
S = scalar_multiplication(QA, nB, A, P_MOD)
S_other = scalar_multiplication(QA_other, nB, A, P_MOD)
shared_x = S[0]

assert (y * y) % P_MOD == rhs
assert (y_other * y_other) % P_MOD == rhs
assert y in (6287, 3452) and y_other in (6287, 3452)
assert S[0] == S_other[0] == 1791

key = sha1(str(shared_x).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, bytes.fromhex(iv))
flag = unpad(cipher.decrypt(bytes.fromhex(encrypted_flag)), 16).decode()

assert flag == "crypto{3ff1c1ent_k3y_3xch4ng3}"

print(f"y candidates: {y}, {y_other}")
print("shared secret:", S)
print("shared secret with other y:", S_other)
print("shared x:", shared_x)
print(flag)
