# 运行：python solve.py < input.txt
import sys

data = sys.stdin.read().strip().split()
it = iter(data)
T = int(next(it))
xor_sum = 0

for _ in range(T):
    N = int(next(it)); M = int(next(it))
    dp = [0] * (M + 1)
    for _ in range(N):
        c = int(next(it)); omega = int(next(it))
        if c > M:
            # 该物品放不下，跳过；（仍可安全读取 omega）
            continue
        # 01 背包逆序更新
        for w in range(M, c - 1, -1):
            val = dp[w - c] + omega
            if val > dp[w]:
                dp[w] = val
    ans = dp[M]
    xor_sum ^= ans

print(xor_sum)
