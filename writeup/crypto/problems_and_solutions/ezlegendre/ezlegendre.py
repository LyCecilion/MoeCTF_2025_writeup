from Crypto.Util.number import bytes_to_long, getPrime
from secret import flag

p = 258669765135238783146000574794031096183
a = 144901483389896508632771215712413815934


def encrypt_flag(flag):
    ciphertext = []
    plaintext = "".join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = getPrime(16)
        d = randint(1, 10)
        n = pow(a + int(b) * d, e, p)
        ciphertext.append(n)
    return ciphertext


print(encrypt_flag(flag))
