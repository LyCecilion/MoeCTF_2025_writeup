import ctypes

libc = ctypes.CDLL("libc.so.6")
libc.srand(1)

for i in range(1, 11):
    print(f"The random value {i} is: {libc.rand() % 10000}")
