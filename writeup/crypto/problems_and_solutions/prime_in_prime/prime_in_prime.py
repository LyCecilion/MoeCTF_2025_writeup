from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
import random, gmpy2
from secret import flag


class RSAEncryptor:
    def __init__(self):
        self.g = self.a = self.b = 0
        self.e = 65537
        self.factorGen()
        self.product()

    def factorGen(self):
        while True:
            self.g = getPrime(256)
            while not gmpy2.is_prime(2 * self.g * self.a + 1):
                self.a = random.randint(2**255, 2**256)
            while not gmpy2.is_prime(2 * self.g * self.b + 1):
                self.b = random.randint(2**255, 2**256)
            self.h = 2 * self.g * self.a * self.b + self.a + self.b
            if gmpy2.is_prime(self.h):
                self.N = 2 * self.h * self.g + 1
                print(len(bin(self.N)))
                return

    def encrypt(self, msg):
        return pow(msg, self.e, self.N)

    def product(self):
        self.flag = bytes_to_long(flag)
        self.enc = self.encrypt(self.flag)
        self.show()
        print(f"enc={self.enc}")

    def show(self):
        print(f"N={self.N}")
        print(f"e={self.e}")
        print(f"g={self.g}")


RSAEncryptor()
