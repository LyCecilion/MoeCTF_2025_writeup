"""extract_passwords.py

该 Python 脚本供 MoeCTF 2025 的 Misc 赛道中，「万里挑一」题目使用。
由 星澜音 在 Claude 的帮助下编写。
"""

import os
import re
import shutil
import zipfile


def setup_temp_dir():
    """该函数设置解压 `.zip` 文件时的临时目录。"""

    if os.path.exists("temp_extract"):
        shutil.rmtree("temp_extract")
    os.makedirs("temp_extract")
    return "temp_extract"


def extract_passwords(
    zip_path, temp_dir, max_depth=10, current_depth=0, passwords=None, path_prefix=""
):
    """该函数递归地解压 `password.zip` 及其子压缩包。

    Args:
        zip_path (str): 压缩包路径。
        temp_dir (str): 临时目录路径。
        max_depth (int, optional): 解压时的递归深度。这里，Claude 为了确保递归完全进行，
                                   将其默认值设为了 10。实际上，由于我们完全已知压缩包结构，可以精确指定 `max_depth` 的值。
        current_depth (int, optional): 解压时的当前深度。
        passwords (str, optional): 解压得到的密码。
        path_prefix (str, optional): 路径的前缀。
    """
    if passwords is None:
        passwords = set()

    if current_depth >= max_depth:
        return passwords

    current_path = (
        f"{path_prefix}/{os.path.basename(zip_path)}"
        if path_prefix
        else os.path.basename(zip_path)
    )

    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

            # 检查是否存在 `pwd.txt`，如果有，就在其中匹配密码；如果没有，则跳过并继续向下递归解压。
            if "pwd.txt" in zip_ref.namelist():
                pwd_path = os.path.join(temp_dir, "pwd.txt")
                with open(pwd_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    password = None
                    # 尝试精确匹配密码格式。
                    match = re.search(r"The password is:([a-f0-9]+)", content)
                    if match:
                        password = match.group(1)
                    else:
                        # 尝试宽松匹配密码格式。
                        match = re.search(
                            r"password.*?[: ]([a-f0-9]+)", content, re.IGNORECASE
                        )
                        if match:
                            password = match.group(1)
                        else:
                            # 在完全无法正确匹配密码格式时，尝试匹配任何可能的密码，其判断标准为 16~40 个字符的字母、数字字符串。
                            match = re.search(r"([a-f0-9]{16,40})", content)
                            if match:
                                password = match.group(1)

                    if password:
                        passwords.add(password)
                        print(f"找到密码: {password} (来自 {current_path})")

            # 递归处理所有子 `zip` 文件。
            for i in range(10):
                sub_zip = os.path.join(temp_dir, f"{i}.zip")
                if os.path.exists(sub_zip):
                    sub_dir = os.path.join(temp_dir, f"extract_{i}")
                    if not os.path.exists(sub_dir):
                        os.makedirs(sub_dir)
                    extract_passwords(
                        sub_zip,
                        sub_dir,
                        max_depth,
                        current_depth + 1,
                        passwords,
                        current_path,
                    )
    except Exception as e:
        print(f"处理 {zip_path} 时出错：{str(e)[:100]}……")

    return passwords


def main():
    """主函数开始处理压缩包 `password.zip` 的解压。"""

    temp_dir = setup_temp_dir()

    # 解压第 1 层压缩包。
    try:
        with zipfile.ZipFile("password.zip", "r") as zip_ref:
            zip_ref.extractall(temp_dir)
    except Exception as e:
        print(f"无法解压 `password.zip`：{e}")
        return

    # 递归地提取所有密码。
    print("开始提取所有可能的密码……")
    all_passwords = set()

    # 处理所有 `zip` 文件。
    for i in range(10):
        sub_zip = os.path.join(temp_dir, f"{i}.zip")
        if os.path.exists(sub_zip):
            sub_dir = os.path.join(temp_dir, f"extract_{i}")
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)
            passwords = extract_passwords(sub_zip, sub_dir, max_depth=10)
            all_passwords.update(passwords)

    print(f"总共找到 {len(all_passwords)} 个不同的密码。")

    # 将密码保存在 `extracted_passwords.txt` 中。
    with open("extracted_passwords.txt", "w", encoding="utf-8") as f:
        for pwd in all_passwords:
            f.write(f"{pwd}\n")
    print("所有密码已保存到 `extracted_passwords.txt` 文件中。")

    # 清理临时文件。
    print("正在清理临时文件……")
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"清理临时文件时出错: {e}")


if __name__ == "__main__":
    main()
