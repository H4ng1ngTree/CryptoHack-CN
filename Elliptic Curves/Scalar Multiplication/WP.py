def scalar_multiplication(P, n, a, p):
    """Double and Add：计算 [n]P。"""
    Q = P
    R = None   # None 表示无穷远点 O

    while n > 0:
        if n % 2 == 1:
            R = point_add(R, Q, a, p)

        Q = point_add(Q, Q, a, p)
        n //= 2

    return R


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
        slope = ((y2 - y1) * pow(x2 - x1, -1, p)) % p
    else:
        slope = ((3 * x1**2 + a) * pow(2 * y1, -1, p)) % p

    x3 = (slope**2 - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p

    return x3, y3


def is_on_curve(P, a, b, p):
    """检查点 P 是否在曲线 y^2 = x^3 + ax + b mod p 上。"""
    if P is None:
        return True

    x, y = P
    return (y**2 - (x**3 + a * x + b)) % p == 0


A = 497
B = 1768
MOD = 9739

# 题目给的测试样例
X = (5323, 5438)
assert scalar_multiplication(X, 1337, A, MOD) == (1089, 6931)

# 题目要求计算 [7863]P
P = (2339, 2213)
Q = scalar_multiplication(P, 7863, A, MOD)

# 验证结果确实在曲线上
assert is_on_curve(Q, A, B, MOD)

print(Q)
print("crypto{" + str(Q[0]) + "," + str(Q[1]) + "}")
