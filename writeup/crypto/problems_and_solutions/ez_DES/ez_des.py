import secrets
import string

from Crypto.Cipher import DES

flag = "moectf{???}"
characters = string.ascii_letters + string.digits + string.punctuation
key = "ezdes" + "".join(secrets.choice(characters) for _ in range(3))
assert key[:5] == "ezdes"
key = key.encode("utf-8")
l = 8


def encrypt(text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = text + (l - len(text) % l) * chr(len(text))
    data = cipher.encrypt(padded_text.encode("utf-8"))
    return data


c = encrypt(flag, key)
print("c =", c)

# c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'
