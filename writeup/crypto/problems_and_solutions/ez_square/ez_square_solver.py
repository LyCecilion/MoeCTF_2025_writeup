"""ez_square_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_square」题目使用。
由 星澜音 编写。
"""

import math

import gmpy2
from Crypto.Util.number import long_to_bytes

# 定义给出的 `n`、`c`、`hint` 和 `e`
n = 83917281059209836833837824007690691544699901753577294450739161840987816051781770716778159151802639720854808886223999296102766845876403271538287419091422744267873129896312388567406645946985868002735024896571899580581985438021613509956651683237014111116217116870686535030557076307205101926450610365611263289149
c = 69694813399964784535448926320621517155870332267827466101049186858004350675634768405333171732816667487889978017750378262941788713673371418944090831542155613846263236805141090585331932145339718055875857157018510852176248031272419248573911998354239587587157830782446559008393076144761176799690034691298870022190
hint = 5491796378615699391870545352353909903258578093592392113819670099563278086635523482350754035015775218028095468852040957207028066409846581454987397954900268152836625448524886929236711403732984563866312512753483333102094024510204387673875968726154625598491190530093961973354413317757182213887911644502704780304
e = 65537


def is_perfect_square(number: int) -> bool:
    """该函数检验传入的 `n` 是否为完全平方数。

    Args:
        n (int): 待检验的整数。

    Returns:
        bool: 是否为完全平方数。
    """
    if number < 0:
        return False
    sqrt = math.isqrt(number)
    return sqrt * sqrt == number


# 验证 `S^2 = k*n + hint` 是否是完全平方数
# 由先前的分析，这里的 `k` 从 `4` 开始取
print("😋 即将开始破解 S = (p+q) 的值。\n")
k = 4
while True:
    print(f"✍️ 现在尝试 k = {k} 的情况……")
    current_s_square = k * n + hint
    if is_perfect_square(current_s_square):
        print(f"\n😎 已找到 k = {k} 使得 (k*n + hint) 为完全平方数！\n")
        break
    k = k + 1

# 验证完成后，保留 S^2 的值
print(f"✍️ 下面我们以 k = {k} 计算 S^2。")
s_square = k * n + hint
s = math.isqrt(s_square)
assert s**2 == s_square
print(f"😎 得到 S^2 的值为 {s_square}\n")

# 使用求根公式得到 p 和 q 的值
print("✍️ 这里我们假定 p < q，使用一元二次方程求根公式得到：")
inner_value = s_square - 4 * n
inner_value_sqrt = math.isqrt(inner_value)
assert inner_value_sqrt**2 == inner_value
p = (s - inner_value_sqrt) // 2
q = (s + inner_value_sqrt) // 2
print(f"p 为 {p}\nq 为 {q}\n")

# 计算 n 和 phi(n) 以及逆元 d
n = p * q
print(f"✍️ 计算得到乘积 n = {n}\n")
phi_n = (p - 1) * (q - 1)
print(f"✍️ 计算欧拉函数 phi(n) = {phi_n}\n")
d = gmpy2.invert(e, phi_n)
print(f"✍️ 计算得到逆元 d = {d}\n")
m = pow(c, d, n)

# 解密 `flag`
flag = long_to_bytes(m)
print(f"🤔 得到了 `flag` 的数值形式为 {m}")
print(f"😎 解密得到的 `flag` 是 {flag.decode()}")
