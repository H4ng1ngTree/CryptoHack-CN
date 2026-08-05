P = (8045, 6936)
p = 9739

x, y = P
Q = (x, (-y) % p)

print(Q)
print("crypto{" + str(Q[0]) + "," + str(Q[1]) + "}")
