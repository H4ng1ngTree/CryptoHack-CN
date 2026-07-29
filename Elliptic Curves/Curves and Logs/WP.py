from hashlib import sha1


A = 497
B = 1768
MOD = 9739

QA = (815, 3190)
nB = 1829


def point_add(P, Q, a, p):
    """椭圆曲线 y^2 = x^3 + ax + b mod p 上的点加法。"""
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P + (-P) = O
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
    """Double and Add：计算 [n]P。"""
    Q = P
    R = None  # None 表示无穷远点 O

    while n > 0:
        if n % 2 == 1:
            R = point_add(R, Q, a, p)

        Q = point_add(Q, Q, a, p)
        n //= 2

    return R


def is_on_curve(P, a, b, p):
    """检查点 P 是否在曲线上。"""
    if P is None:
        return True

    x, y = P
    return (y**2 - (x**3 + a * x + b)) % p == 0


shared_secret = scalar_multiplication(QA, nB, A, MOD)
assert is_on_curve(shared_secret, A, B, MOD)

shared_x = shared_secret[0]
digest = sha1(str(shared_x).encode()).hexdigest()
flag = f"crypto{{{digest}}}"

assert shared_secret == (7929, 707)
assert shared_x == 7929
assert digest == "80e5212754a824d3a4aed185ace4f9cac0f908bf"
assert flag == "crypto{80e5212754a824d3a4aed185ace4f9cac0f908bf}"

print("shared secret:", shared_secret)
print("shared x:", shared_x)
print("digest:", digest)
print(flag)
