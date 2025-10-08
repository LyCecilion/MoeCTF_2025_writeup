from random import randrange
from Crypto.Util.number import getPrime, bytes_to_long
from secret import flag

assert len(flag) % 5 == 0

block_size = len(flag) // 5
m_blocks = [
    bytes_to_long(flag[i * block_size : (i + 1) * block_size]) for i in range(5)
]
p = getPrime(128)


def make_mask(n, p):
    from sage.all import identity_matrix, det

    upper = identity_matrix(n)
    low = identity_matrix(n)
    for i in range(n - 1):
        for j in range(i + 1, n):
            upper[i, j] = randrange(1, p)
            low[j, i] = randrange(1, p)
    result = upper * low
    assert det(result) == 1
    return result


def matrix_to_list(mat):
    return [list(row) for row in mat]


Noise = [[randrange(1, p) for _ in range(5)] for _ in range(4)]
Noise.append(m_blocks)

M = matrix(Noise)
A = make_mask(5, p)
C = A * M

print(f"p={p}")
print(f"C={matrix_to_list(C)}")
