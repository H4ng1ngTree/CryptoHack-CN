A = 497
B = 1768
P_MOD = 9739


def point_add(P, Q, a, p):
    """Add two points on y^2 = x^3 + ax + b over F_p.

    The point at infinity O is represented by None.
    """
    if P is None:
        return Q
    if Q is None:
        return P

    x1, y1 = P
    x2, y2 = Q

    # P and Q are vertical opposites, so P + Q = O.
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


def is_on_curve(P, a, b, p):
    if P is None:
        return True

    x, y = P
    return (y**2 - (x**3 + a * x + b)) % p == 0


P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

S = point_add(P, P, A, P_MOD)
S = point_add(S, Q, A, P_MOD)
S = point_add(S, R, A, P_MOD)

assert is_on_curve(S, A, B, P_MOD)

print(S)
print(f"crypto{{{S[0]},{S[1]}}}")
