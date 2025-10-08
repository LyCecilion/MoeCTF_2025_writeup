#!/usr/bin/env python3
from math import isqrt
from Crypto.Util.number import long_to_bytes

# 给出的 n, e, c
n = 84605285758757851828457377667762294175752561129610097048351349279840138483398457225774806927631502994733733589395840262513798535197234231207789297886471069978772805190331670685610247724499942260404337703802384815835647029115023558590369107257177909006753910122009460031921101203824769814404613875312981158627
e = 36007582633238869298665544067678113422327323938964762672901735035127703586926259430077542134592019226503943946361640448762427529212920888008258014995041748515569059310310043800176826513779147205500576568904875173836996771537397098255940072198687847850344965265595497240636679977485413228850326441605991445193
c = 25377227886381037011295005467170637635721288768510629994676412581338590878502600384742518383737721726526909112479581593062708169548345605933735206312240456062728769148181062074615706885490647135341795076119102022317083118693295846052739605264954692456155919893515748429944928104584602929468479102980568366803


# ---- 连分数与收敛分数工具 ----
def contfrac(num, den):
    """num/den 的连分数展开 [a0, a1, ...]"""
    while den:
        a = num // den
        yield a
        num, den = den, num - a * den


def convergents(cf):
    """由连分数项生成逐个收敛分数 (k_i, d_i)，表示 k_i/d_i 约等于 e/n"""
    k_prev, k = 1, cf[0]
    d_prev, d = 0, 1
    yield (k, d)
    for a in cf[1:]:
        k_prev, k = k, a * k + k_prev
        d_prev, d = d, a * d + d_prev
        yield (k, d)


def is_perfect_square(x):
    if x < 0:
        return False
    r = isqrt(x)
    return r * r == x


# ---- Wiener 攻击主体 ----
def wiener_attack(e, n):
    # e/n 的连分数
    cf = list(contfrac(e, n))
    for k, d in convergents(cf):
        if k == 0:
            continue
        # 验证 (e*d - 1) 能否被 k 整除，从而候选出 φ(n)
        if (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k

        # 解二次方程 x^2 - (n - phi + 1) x + n = 0
        # 判别式 Δ = (n - phi + 1)^2 - 4n 必须是完全平方数
        s = n - phi + 1
        disc = s * s - 4 * n
        if not is_perfect_square(disc):
            continue
        t = isqrt(disc)
        # 得到 p, q
        p = (s + t) // 2
        q = (s - t) // 2
        if p * q == n and p > 1 and q > 1:
            # 这里的 d 值通常就是私钥 d
            return d, p, q
    return None, None, None


def main():
    d, p, q = wiener_attack(e, n)
    if d is None:
        print("Wiener 攻击失败：未能恢复 d。")
        return
    print(f"Recovered d: {d}")
    print(f"p: {p}\nq: {q}")

    m = pow(c, d, n)
    flag = long_to_bytes(m)
    try:
        print("flag =", flag.decode())
    except UnicodeDecodeError:
        print("flag (bytes) =", flag)


if __name__ == "__main__":
    main()
