"""ez_des_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_DES」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""

import itertools
import string

from Crypto.Cipher import DES

# 定义给定的 `c`
c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'

# 构建与原脚本相同的字符集，并指定 DES 密钥的前缀
CHARACTERS = string.ascii_letters + string.digits + string.punctuation
PREFIX = "ezdes"
print("🥱 即将遍历全体可能的字符串，并将其作为 DES 密钥以尝试解密……")

for p in itertools.product(CHARACTERS, repeat=3):
    try:
        # 构造 DES 密钥
        key_suffix = "".join(p)
        key = (PREFIX + key_suffix).encode("utf-8")

        # 尝试使用密钥解密 `c`
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted_data = cipher.decrypt(c)

        # 匹配解密结果
        if decrypted_data.startswith(b"moectf{"):
            print("\n😋 破解成功!")
            print(f"👀 找到密钥: {key.decode('utf-8')}")

            original_length = decrypted_data[-1]
            flag = decrypted_data[:original_length]

            print(f"👍 成功恢复 `flag`: {flag.decode('utf-8')}")
            break

    except Exception as e:
        continue

else:
    print("\n😢 破解失败，未找到正确的密钥。")
