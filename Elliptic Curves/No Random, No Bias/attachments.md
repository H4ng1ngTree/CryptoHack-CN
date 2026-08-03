## 附件内容

这里把题目给出的附件直接展开，省得每次再点到 CryptoHack 下载。

### source.py

原始链接：<https://cryptohack.org/static/challenges/source_a911b46ac71942190489524c4456a1be.py>

{% raw %}
```python
from hashlib import sha1
from Crypto.Util.number import bytes_to_long, long_to_bytes
from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256, Public_key, Private_key
from random import randint

G = generator_256
q = G.order()

FLAG = b'crypto{??????????????????}'


def hide_flag(privkey):
    x = bytes_to_long(FLAG)
    p = curve_256.p()
    b = curve_256.b()
    ysqr = (x**3 - 3*x + b) % p
    y = pow(ysqr, (p+1)//4, p)
    Q = ellipticcurve.Point(curve_256, x, y)
    T = privkey.secret_multiplier*Q
    return (int(T.x()), int(T.y()))


def genKeyPair():
    d = randint(1,q-1)
    pubkey = Public_key(G, d*G)
    privkey = Private_key(pubkey, d)
    return pubkey, privkey


def ecdsa_sign(msg, privkey):
    hsh = sha1(msg.encode()).digest()
    nonce = sha1(long_to_bytes(privkey.secret_multiplier) + hsh).digest()
    sig = privkey.sign(bytes_to_long(hsh), bytes_to_long(nonce))
    return {"msg": msg, "r": hex(sig.r), "s": hex(sig.s)}



pubkey, privkey = genKeyPair()
hidden_flag = hide_flag(privkey)

sig1 = ecdsa_sign('I have hidden the secret flag as a point of an elliptic curve using my private key.', privkey)
sig2 = ecdsa_sign('The discrete logarithm problem is very hard to solve, so it will remain a secret forever.', privkey)
sig3 = ecdsa_sign('Good luck!', privkey)

print('Hidden flag:', hidden_flag)
print('\nPublic key:', (int(pubkey.point.x()), int(pubkey.point.y())), '\n')
print(sig1)
print(sig2)
print(sig3)
```
{% endraw %}

### output.txt

原始链接：<https://cryptohack.org/static/challenges/output_b141b43860f2ca53f0e36df40f42f2db.txt>

{% raw %}
```text
Hidden flag: (16807196250009982482930925323199249441776811719221084165690521045921016398804, 72892323560996016030675756815328265928288098939353836408589138718802282948311)

Public key: (48780765048182146279105449292746800142985733726316629478905429239240156048277, 74172919609718191102228451394074168154654001177799772446328904575002795731796)

{'msg': 'I have hidden the secret flag as a point of an elliptic curve using my private key.', 'r': '0x91f66ac7557233b41b3044ab9daf0ad891a8ffcaf99820c3cd8a44fc709ed3ae', 's': '0x1dd0a378454692eb4ad68c86732404af3e73c6bf23a8ecc5449500fcab05208d'}
{'msg': 'The discrete logarithm problem is very hard to solve, so it will remain a secret forever.', 'r': '0xe8875e56b79956d446d24f06604b7705905edac466d5469f815547dea7a3171c', 's': '0x582ecf967e0e3acf5e3853dbe65a84ba59c3ec8a43951bcff08c64cb614023f8'}
{'msg': 'Good luck!', 'r': '0x566ce1db407edae4f32a20defc381f7efb63f712493c3106cf8e85f464351ca6', 's': '0x9e4304a36d2c83ef94e19a60fb98f659fa874bfb999712ceb58382e2ccda26ba'}
```
{% endraw %}
