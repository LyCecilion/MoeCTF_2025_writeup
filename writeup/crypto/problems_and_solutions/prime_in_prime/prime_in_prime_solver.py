import gmpy2
from Crypto.Util.number import long_to_bytes

# --- 请将从题目中获取的值填入此处 ---
N = 214573917396475151591439896765340649356903366282510444643717995836268241944086135730442283063193255393603869402234028852312016590097601494284791676448001267763372323062884418596889759120350628812186406667350758599829877640794231128163608814018423074272718202058782335546144064988748275832931793658220184699303
e = 65537
g = 73484977888603783021476338660533250408703389103657907428651575929878729152777
enc = 49286646888982964532457878423948757700937118706141638346625071009061730002909495567061807689872070340382970279453224387751923897721080202354534089230325929411325064104922189262557791044445049532087245955298868504045172441275341650423890273895540164235535897925083392664030102071783198499588031261031158836202
# -----------------------------------------

# 1. 根据 N = 2*h*g + 1 计算 h
print("[+] Calculating h...")
h = (N - 1) // (2 * g)
print(f"h = {h}")

# 2. 计算初始的 S_0 和 P_0
P_0 = h // (2 * g)
S_0 = h % (2 * g)
print(f"[+] Initial S_0 = {S_0}")
print(f"[+] Initial P_0 = {P_0}")

# 3. 循环搜索正确的 k 值以修正 S 和 P
print("[+] Searching for correct S and P by iterating k...")
a, b = 0, 0
found = False
for k in range(10):  # k 几乎总是一个非常小的整数，循环 10 次已足够
    S = S_0 + k * (2 * g)
    P = P_0 - k

    # Delta = S^2 - 4P
    # 检查 Delta 是否为非负数
    if S**2 < 4 * P:
        continue

    delta = S**2 - 4 * P

    # 检查 Delta 是否为完全平方数
    if gmpy2.is_square(delta):
        print(f"[+] Success! Found a perfect square for delta with k={k}.")
        sqrt_delta = gmpy2.isqrt(delta)

        # 求解 a 和 b
        # 确保分子可以被 2 整除
        if (S + sqrt_delta) % 2 == 0:
            a = (S + sqrt_delta) // 2
            b = (S - sqrt_delta) // 2
            found = True
            break  # 找到解，跳出循环

if not found:
    print("[-] Failed to find a valid solution after trying several values of k.")
else:
    print(f"a = {a}")
    print(f"b = {b}")

    # 4. 计算 p 和 q
    print("[+] Calculating factors p and q...")
    p = 2 * g * a + 1
    q = 2 * g * b + 1

    # 验证 p 和 q 的正确性
    if p * q == N:
        print("[+] Factorization successful!")
        print(f"p = {p}")
        print(f"q = {q}")

        # 5. 计算 phi(N) 和私钥 d
        print("[+] Calculating private key d...")
        phi = (p - 1) * (q - 1)
        d = gmpy2.invert(e, phi)
        print(f"d = {d}")

        # 6. 解密
        print("[+] Decrypting message...")
        decrypted_message = pow(enc, d, N)

        # 7. 将解密后的数字转换为字节得到 flag
        flag = long_to_bytes(decrypted_message)
        print("\n[+] Success! Flag found:")
        print(flag.decode())
    else:
        print("[-] Error: Factorization failed. p * q does not equal N.")
