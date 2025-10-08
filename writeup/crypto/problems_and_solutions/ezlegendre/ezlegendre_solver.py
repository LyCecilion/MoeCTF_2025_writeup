"""ezlegendre_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ezlegendre」题目使用。
由 星澜音 在 Gemini 的帮助下编写。
"""

# 在这里填入已知的常量和 `output.txt` 的文件名。
p = 258669765135238783146000574794031096183
a = 144901483389896508632771215712413815934
FILENAME = "output.txt"


def legendre_symbol(num, prime):
    """该函数用于计算 Legendre Symbol。"""
    return pow(num, (prime - 1) // 2, prime)


def solve():
    """主解密函数。"""
    try:
        # 从 output.txt 读取密文
        with open(FILENAME, "r", encoding="utf-8") as f:
            # 读取文件内容，去除可能存在的方括号和多余空格
            content = f.read().strip()
            if content.startswith("[") and content.endswith("]"):
                content = content[1:-1]

            # 按逗号分割，并将每个字符串转换为整数
            ciphertext = [int(n.strip()) for n in content.split(",")]
        print(f"成功读取 {len(ciphertext)} 个加密数字。")

    except FileNotFoundError:
        print("错误：未找到 output.txt 文件。请确保该文件与脚本在同一目录下。")
        return
    except (ValueError, IndexError):
        print("错误：无法解析 output.txt 的内容。请确保文件格式为以逗号分隔的数字。")
        return

    # 1. 计算代表比特 '0' 的基准勒让德符号
    symbol_for_zero = legendre_symbol(a, p)
    print(f"计算出代表 '0' 的勒让德符号值为: {symbol_for_zero}")

    # 用于存储解密出的二进制比特流
    binary_flag = ""

    # 2. 遍历所有密文，恢复出二进制的 `flag`
    for n in ciphertext:
        current_symbol = legendre_symbol(n, p)
        # 3. 比较符号并判断比特
        if current_symbol == symbol_for_zero:
            binary_flag += "0"
        else:
            binary_flag += "1"

    print("\n已成功恢复二进制 `flag` 字符串。正在转换为文本...")

    # 4. 将二进制字符串转换回 ASCII 文本
    flag = ""
    for i in range(0, len(binary_flag), 8):
        byte = binary_flag[i : i + 8]
        # 确保我们处理的是完整的 8 位字节
        if len(byte) == 8:
            # 将 8 位二进制转换为整数，再从整数转换为对应的 ASCII 字符
            flag += chr(int(byte, 2))

    print("\n" + "=" * 30)
    print("🎉 解密成功! 🎉")
    print(f"`flag`: {flag}")
    print("=" * 30)


if __name__ == "__main__":
    solve()
