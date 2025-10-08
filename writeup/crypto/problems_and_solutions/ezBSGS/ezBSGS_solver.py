"""ezBSGS_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ezBSGS」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""

import math


def bsgs(a: int, b: int, p: int) -> int | None:
    """该函数使用 Baby-Step Giant-Step 算法解决 `a^x equiv b (mod p)` 问题。

    Args:
        a (int): 底数
        b (int): 结果
        p (int): 模数

    Returns:
        int | None: 返回计算出的 `x`。若未计算出 `x`，则返回 `None`。
    """

    # 计算 Giant-Step 行动一次的前进次数，使用 `m = ceil(sqrt(p))`
    m = int(math.sqrt(p)) + 1
    print(f"👣 计算得到 Giant-Step 行动一次，前进的次数为 {m}\n")

    # 计算 Baby-Step 的前进，并计入哈希表
    print("========== 下面开始 Baby-Step 的前进 ==========")
    baby_steps = {}
    val = b
    for j in range(m):
        # `baby_steps` 的键是位置 `(b * a^j) mod p`，值是前进次数 `j`
        baby_steps[val] = j
        val = (val * a) % p
    print(f"😋 已完成 {len(baby_steps)} 次 Baby-Step 前进，并将结果存入哈希表。\n")

    # 计算 Giant-Step 的行动，并检索哈希表以尝试匹配
    print("========== 下面开始 Giant-Step 的行动 ==========")

    # 计算 Giant-Step 的第 1 次行动
    giant_stride = pow(a, m, p)
    giant_val = giant_stride
    for i in range(1, m + 1):
        # 在哈希表中查找当前 Giant-Step 前进到的位置
        if giant_val in baby_steps:
            j = baby_steps[giant_val]
            x = i * m - j
            print(f"😰 在第 i = {i} 次 Giant-Step 行动时匹配成功！")
            print(f"😎 Giant-Step 计算结果: {giant_val}")
            print(f"👀 哈希表中匹配的 Baby-Step 前进次数: {j}")
            print(f"🥰 计算最终解 x = {i} * {m} - {j} = {x}")
            return x

        # 若匹配失败，则继续查找
        giant_val = (giant_val * giant_stride) % p

    # 如果循环结束仍未匹配成功，则可能无解
    return None


if __name__ == "__main__":
    # 定义 `BASE`、`RESULT` 和 `MODULUS` 的值
    BASE = 13
    RESULT = 114514
    MODULUS = 100000000000099

    print("将使用下面的参数，以 BSGS 算法求解目标的 `x`：")
    print(f"a = {BASE}")
    print(f"b = {RESULT}")
    print(f"p = {MODULUS}")
    print("🤔 正在求解，请等待……\n")

    # 调用 BSGS 算法求解
    x = bsgs(BASE, RESULT, MODULUS)

    print("\n================ 🧮 最终结果 ⏱️ ================")
    if x is not None:
        print(f"🎮 方程的解 x = {x}\n")

        # 验证结果
        print("================= 🔍 验证解 🤔 =================")
        verification = pow(BASE, x, MODULUS)
        print(f"计算 {BASE}^{x} mod {MODULUS}……")
        print(f"计算结果: {verification}")
        print(f"目标结果: {RESULT}")
        if verification == RESULT:
            print(f"✅ 验证成功！方程的解确为 {x}。\n")
            print("`flag`: moectf{" + str(x) + "}")
        else:
            print("❌ 验证失败。\n")
    else:
        print("😭 方程无解。\n")
