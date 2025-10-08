from Crypto.Util.number import *
from Crypto.Cipher import AES
import gmpy2
import random
from secrets import flag

p = 251
e = 65537


def function(x, p):
    y = 0
    if x >= p:
        y = x
    elif pow(x, (p - 1) // 2, p) == 1:
        y = pow(x, 2, p)
    else:
        y = pow(x, 3, p)
    return y


def matrix_to_str(matrix):
    b = bytes(sum([[matrix[row][col] for col in range(4)] for row in range(4)], []))
    return b.rstrip(b"\0")


def str_to_matrix(s):
    matrix = [[function(s[row + 4 * col], p) for row in range(4)] for col in range(4)]
    return matrix


a = [[random.choice([227, 233, 239, 251]) for row in range(4)] for col in range(4)]
p_ = getPrime(256)

text_ = [
    [
        pow(bytes_to_long(flag[(row + col * 4) * 2 : (row + col * 4) * 2 + 2]), -2, p_)
        + 1
        for row in range(4)
    ]
    for col in range(4)
]
key = 0
for row in range(4):
    for col in range(4):
        key *= 2
        key += (pow(text_[row][col], (p_ - 1) // 2, p_) + 1) % p_ // 2

assert len(flag) == 32
assert (
    p_ == 71583805456773770888820224577418671344500223401233301642692926000191389937709
)
assert (
    pow(key, 2 * e, p_)
    == 1679283667939124174051653611794421444808492935736643969239278575726980681302
)


text_ = [flag[:16], flag[16:]]
cipher = AES.new(long_to_bytes(key << 107), AES.MODE_ECB)
for t in range(2):
    lis = [[0 for row in range(4)] for col in range(4)]
    for i in range(10):
        enc = cipher.encrypt(text_[t])
        matrix = str_to_matrix(enc)
        for row in range(4):
            for col in range(4):
                lis[row][col] = lis[row][col] << 1
                if matrix[row][col] > a[row][col] // 2:
                    lis[row][col] += 1
        matrix = [
            [function(matrix[col][row], a[col][row]) for row in range(4)]
            for col in range(4)
        ]
        text_[t] = matrix_to_str(matrix)
    print(f"lis{t}={lis}")

text = pow(bytes_to_long(text_[0] + text_[1]), 2, p_)
print(f"text={text}")
print(f"a={a}")
