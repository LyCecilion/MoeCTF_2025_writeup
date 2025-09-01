<!--markdownlint-disable MD033 MD041-->

<div align="center">

# 🔑 密码学 题解 🔒

</div>

## Crypto 入门指北

> [!NOTE]
> **FLAG:** `moectf{th1s_1s_y0ur_f1rst_ElG@m@l}`

下载并分析题目给定的 Python 文件（排版有优化）：

```python
#!/usr/bin/env python3
from random import *

from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes, random
from Crypto.Util.number import *
from secret import flag


def generate_elgamal_keypair(bits=512):
    p = getPrime(bits)

    for _ in range(1000):
        g = getRandomRange(2, 5)
        if pow(g, (p - 1) // 2, p) != 1:
            break

    x = randrange(2, p - 1)
    y = pow(g, x, p)

    return p, g, y, x


key = generate_elgamal_keypair(bits=512)
p, g, y, x = key

print("=== 公钥 (p, g, y) ===")
print("p =", p)
print("g =", g)
print("y =", y)
print()

k = randrange(1, p - 2)
m = bytes_to_long(flag)
c1 = pow(g, k, p)
c2 = (m * pow(y, k, p)) % p

print("=== 密文 (c1, c2) ===")
print("c1 =", c1)
print("c2 =", c2)
# 不小心把 `x` 输出了（）
print("x =", x)

"""
=== 公钥 (p, g, y) ===
p = 11540963715962144951763578255357417528966715904849014985547597657698304891044841099894993117258279094910424033273299863589407477091830213468539451196239863
g = 2
y = 8313424783366011287014623582773521595333285291380540689467073212212931648415580065207081449784135835711205324186662482526357834042013400765421925274271853

=== 密文 (c1, c2) ===
c1 = 6652053553055645358275362259554856525976931841318251152940464543175108560132949610916012490837970851191204144757409335011811874896056430105292534244732863
c2 = 2314913568081526428247981719100952331444938852399031826635475971947484663418362533363591441216570597417789120470703548843342170567039399830377459228297983
x = 8010957078086554284020959664124784479610913596560035011951143269559761229114027738791440961864150225798049120582540951874956255115884539333966429021004214
"""
```

题目提示：

> 此处的 `secret` 模块可以理解为存储了明文 `flag`的 Python 文件，属于未知信息，而非公开的可用模块。你需要尝试从密文去恢复原始的 `flag`，而不是去下载 `secret` 模块。`secrets` 则是一个用于生成管理密码的安全随机数的 Python 标准库。`bytes_to_long` 函数用于将 `flag` 编码为整数。

从 `generate_elgamal_keypair` 就能看出来，它实现了一个 ElGamal 加密算法。

ElGamal 加密算法建立在一个大素数 $p$ 以及模 $p$ 的乘法群 $\Z^*_p$ 上，其乘法群的集合包含 $1, 2, 3, \cdots, p - 1$ 这些数，乘法群的运算为模 $p$ 运算，即对其中两个数相乘后，结果若超过了 $p - 1$，则除以 $p$ 且取其余数作结果。

我们熟知群具有这样的几个特点：封闭性、结合律、单位元、存在逆元；而对于一个大素数 $p$，集合 $S = \{1, 2, \cdots, p - 1\}$ 作为模 $p$ 的乘法群集合，模 $p$ 运算作为乘法群的运算法则，它们也具备群的条件，这在后文给出了说明。

一个这样的模 $p$ 乘法群存在生成元 $g$。生成元 $g$ 具有非常重要的性质：它的

$$
g^1, g^2, g^3, \cdots, g^{p - 1} \pmod{p}
$$

恰好能覆盖 $\Z^*_p$ 中的所有数。

在正向计算的情况下，给定指数 $x$（私钥），计算 $y = g^x \mod p$（公钥）是容易的；但在逆向计算的情况下，给定公钥 $y$ 和底数 $g$，求出私钥 $x$ 使得 $g^x \equiv y \pmod{p}$ 就是离散对数问题，求解 $x$ 在算法上是困难的，这便是 ElGamal 算法的安全之处，这在后文也给出了说明。

不过，题目给出的 Python 脚本已经给定了 $x$，我们便可以直接用来解密。编写脚本如下：

```python
"""ez_des_brute_force.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_DES」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""
from Crypto.Util.number import long_to_bytes

p = 11540963715962144951763578255357417528966715904849014985547597657698304891044841099894993117258279094910424033273299863589407477091830213468539451196239863
x = 8010957078086554284020959664124784479610913596560035011951143269559761229114027738791440961864150225798049120582540951874956255115884539333966429021004214
c1 = 6652053553055645358275362259554856525976931841318251152940464543175108560132949610916012490837970851191204144757409335011811874896056430105292534244732863
c2 = 2314913568081526428247981719100952331444938852399031826635475971947484663418362533363591441216570597417789120470703548843342170567039399830377459228297983

# 计算共享秘密 s
s = pow(c1, x, p)

# 计算 s 的模逆元（使用费马小定理）
s_inv = pow(s, p-2, p)

# 计算明文 m
m = (c2 * s_inv) % p

# 将 m 转换为字节序列（flag）
flag = long_to_bytes(m)

print(flag)
```

运行后，输出：

```plain
b'moectf{th1s_1s_y0ur_f1rst_ElG@m@l}'
```

即可得到 `flag`。

### 乘法群的条件

#### 封闭性

群的封闭性要求一个集合中的两个数经过运算后，其结果一定还在这个集合里。

对于任意 $a, b \in S$，考虑到 $p$ 为素数，且 $p \nmid a, p \nmid b$ 因为 $1 \leq a, b \leq p - 1 < p$，所以 $p \nmid a \cdot b$（这可以由反证法得到，因为如果 $p \mid a \cdot b$，必然有 $p \mid a$ 或 $p \mid b$），所以

$$
\boxed{a \cdot b \mod p \in S}
$$

#### 结合律

形式上，一个在集合 $S$ 上的二元运算 $*$ 被称之为可结合的（即满足结合律）若其满足以下的结合律：

$$
(x*y)*z = x*(y*z) \quad \forall x, y, z \in S
$$

模乘法继承了整数的结合律 $(a \cdot b) \cdot c = a \cdot (b \cdot c)$，而模运算和乘法操作是良好兼容的，也就是说，在乘法运算中无论何时取模，最终的计算结果都是一致的。即，我们有

$$
\boxed{(a \cdot b) \mod p \equiv ((a \mod p) \cdot (b \mod p)) \mod p}
$$

下面给出一个证明：

设

$$
a = q_a p + r_a, \quad 0 \leq r_a < p, \quad \quad
b = q_b p + r_b, \quad 0 \leq r_b < p
$$

其中 $r_a = a \mod p$、$r_b = b \mod p$。

注意到

$$
ab = (q_a p + r_a)(q_b p + r_b) = p(pq_aq_b + q_ar_b + q_br_a) + r_ar_b
$$

因此 $(a \cdot b) \mod p = r_ar_b$。又由 $(a \mod p) \cdot (b \mod p) = r_ar_b$，证毕。

#### 单位元

显然的，有

$$
\boxed{1 \cdot a = a \equiv a \pmod{p}}
$$

#### 逆元

类比乘法运算中 $3 \times \frac{1}{3} = 1$，我们说实数意义下的 $\frac{1}{3}$ 是 $3$ 的逆元。逆元的要求是群定义的核心，它使得群具有「可逆」的性质，允许我们解决方程和撤销运算，换句话说，它保证了群的完整性和对称性。

我们要证明，对于 $\forall a \in S$ 存在一个逆元 $b \in S$ 使得 $a \cdot b \equiv 1 \pmod{p}$。我们有 [裴蜀定理（Bézout's lemma）](https://oi-wiki.org/math/number-theory/bezouts/)：

> 设 $a, b$ 为不全为 0 的整数。那么，对于 $\forall x, y \in \Z$ 都有 $\gcd{(a, b) | ax+by}$ 成立；而且，$\exist x, y \in \Z$ 使得 $ax + by = \gcd(a, b)$ 成立。

略去证明（因为星澜音不会），我们知道，由于 $p$ 是一个大的素数，任意 $a \in \{1, 2, \cdots, p - 1\}$ 都满足 $\gcd(a, p) = 1$，因此存在整数 $x, y$ 使得

$$
ax + py = 1
$$

对上式两侧取模 $p$，可得

$$
ax \equiv 1 \pmod{p}
$$

因此，$x \mod p$ 即 $a$ 的逆元。取一个 $b = x \mod p$ 使得 $b \in S$，即得到了 $a$ 在模 $p$ 乘法群的逆元 $b$。

$$
\boxed{\forall a \in S, \exists b \in S \text{ such that } a \cdot b \equiv 1 \pmod{p}}
$$

### ElGamal 算法浅析

在 ElGamal 算法的加密过程中，假设发送方 Alice 和接收方 Bob 在传递消息 $m$ 其中 $m \in \Z^*_p$，首先，Bob 要生成一个公钥和私钥：

1. Bob 选择一个大素数 $p$；
2. Bob 选择一个生成元 $g \in \Z^*_p$；
3. Bob 随机生成一个私钥 $x$ 满足 $1 \leq x \leq p - 2$；
4. Bob 计算公钥 $y = g^x \mod p$。

Bob 将公钥 $(p, g, y)$ 公开并将私钥 $x$ 保密。随后，Alice 将加密消息 $m$：

1. Alice 获取 Bob 的公钥 $(p, g, y)$；
2. Alice 随机选择一个临时密钥 $k$ 满足 $1 \leq k \leq p - 2$；
3. Alice 计算第一部分密文：$c_1 = g^k \mod p$；
4. Alice 计算第二部分密文：$c_2 = m \cdot y^k \mod p$。

随后 Alice 将密文 $(c_1, c_2)$ 发送给 Bob。随后 Bob 将用其私钥 $x$ 解密密文：

1. Bob 收到 Alice 的密文 $(c_1, c_2)$；
2. Bob 计算共享秘密 $s = c_1^x \mod p$，这是因为 $c_1 = g^k \mod p$ 即 $c_1 \equiv g^k \pmod{p}$，根据模运算的性质有 $c_1^x \equiv (g^k)^x \mod p$ 所以 $s = c_1^x \mod p = g^{kx} \mod p$；
3. Bob 计算 $s$ 的模 $p$ 逆元 $s^{-1}$，使得 $s \cdot s^{-1} \equiv 1 \pmod{p}$;
4. Bob 恢复消息，以 $m = c_2 \cdot s^{-1} \mod p$。

第 4 步中，展开后，有

$$
\begin{align*}
m
&= c_2 \cdot s^{-1} \mod p \\
&= (m \cdot y^k) \cdot s^{-1} \mod p \\
&= (m \cdot g^{xk}) \cdot s^{-1} \mod p \\
&= (m \cdot s^{-1} \mod p) \cdot (g^{xk} \mod p) \\
&= m \cdot s \cdot s^{-1} \mod p \\
&= m \cdot 1 \mod p \\
&= m
\end{align*}
$$

## ez_DES

> [!NOTE]
> **FLAG:** `moectf{_Ju5t envmEra+e.!}` <sub>（存疑）</sub>

分析题目给出的 Python 脚本（排版有优化）：

```python
import secrets
import string

from Crypto.Cipher import DES

# flag = "moectf{???}"
characters = string.ascii_letters + string.digits + string.punctuation
key = "ezdes" + "".join(secrets.choice(characters) for _ in range(3))
assert key[:5] == "ezdes"
key = key.encode("utf-8")
l = 8


def encrypt(text, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = text + (l - len(text) % l) * chr(len(text))
    data = cipher.encrypt(padded_text.encode("utf-8"))
    return data


c = encrypt(flag, key)
print("c =", c)

# c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'
```

总而言之，程序生成了一个以 `ezdes` 开头的 8 个字符长度的 DES 密钥，并用它加密了未给出的 `flag`。这倒是不要求我们了解 DES 密钥的原理了，毕竟我们在 `Crypto.Cipher` 中有现成的加密和解密工具，这是极好的😋直接上爆破脚本！

```python
"""ez_des_brute_force.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_DES」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""

import itertools
import string

from Crypto.Cipher import DES

# 在这里将 `c` 替换为源代码中给出的 `c`。
c = b'\xe6\x8b0\xc8m\t?\x1d\xf6\x99sA>\xce \rN\x83z\xa0\xdc{\xbc\xb8X\xb2\xe2q\xa4"\xfc\x07'

# 构建与原脚本相同的字符集，并指定 DES 密钥的前缀。
CHARACTERS = string.ascii_letters + string.digits + string.punctuation
PREFIX = "ezdes"
print("正在准备遍历全体可能的 DES 密钥……")

for p in itertools.product(CHARACTERS, repeat=3):
    try:
        # 构造 DES 密钥。
        key_suffix = "".join(p)
        key = (PREFIX + key_suffix).encode("utf-8")

        # 尝试使用密钥解密 `c`。
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted_data = cipher.decrypt(c)

        # 匹配解密结果的条件。
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
```

运行后得到

```plain
PS S:\MoeCTF\Crypto> python .\ez_des_brute_force.py
正在准备遍历全体可能的 DES 密钥……

😋 破解成功!
👀 找到密钥: ezdes8br
👍 成功恢复 `flag`: moectf{_Ju5t envmEra+e.!}
```

不过目前为止零音无法用这个 `flag` 通过提交🤔不会是假阳性吧？

## baby_next

> [!NOTE]
> **FLAG:** `moectf{vv0W_p_m1nu5_q_i5_r34l1y_sm4lI}`

题目给出的 Python 脚本内，有一个自定义的 RSA 算法：

```python
from functools import reduce

from gmpy2 import next_prime
from secret import flag

from Crypto.Util.number import *

assert len(flag) == 38
assert flag[:7] == b"moectf{"
assert flag[-1:] == b"}"


def main():
    p = getPrime(512)
    q = int(reduce(lambda res, _: next_prime(res), range(114514), p))

    n = p * q
    e = 65537

    m = bytes_to_long(flag)

    c = pow(m, e, n)

    print(f"{n = }")
    print(f"{c = }")


if __name__ == "__main__":
    main()

"""
n = 96742777571959902478849172116992100058097986518388851527052638944778038830381328778848540098201307724752598903628039482354215330671373992156290837979842156381411957754907190292238010742130674404082688791216045656050228686469536688900043735264177699512562466087275808541376525564145453954694429605944189276397
c = 17445962474813629559693587749061112782648120738023354591681532173123918523200368390246892643206880043853188835375836941118739796280111891950421612990713883817902247767311707918305107969264361136058458670735307702064189010952773013588328843994478490621886896074511809007736368751211179727573924125553940385967
"""
```

标准的 RSA 算法将在后文提及。我们只需要知道，解密需要 $m = c^d \mod n$，而 $c$ 和 $n$ 都已经给出，当务之急是求出 $d$。$d$ 是 $e$ 的模 $\phi(n)$ 的逆元，而 $e$ 已知，$n$ 已知，则只需要计算出 $\phi(n)$ 即可😋不过……这就需要分解 $n$ 了😭这玩意的确做不到……题目既然说了很好分解，那我们只能寄希望于 $p$ 和 $q$ 的生成逻辑了：

```python
p = getPrime(512)
q = int(reduce(lambda res, _: next_prime(res), range(114514), p))
```

看到了一个令人振奋的事实！$p$ 是随机生成的 512 位质数，而 $q$ 是 $p$ 之后的第 114514 个质数！尽管 $p$ 很大使得 $p$ 周围的质数分布已经尤为稀疏，但 114514 相比于一个 512 位质数来说还是足够小的，我们可以认为，$p$ 和 $q$ 是足够接近的！

现在问题便有了眉目。考虑到 $p$ 和 $q$ 足够接近，我们可以认为，其算术平均数 $a = \frac{p + q}{2}$ 和 $\sqrt{n}$ 也应该是足够接近的。再设 $b = \frac{q - p}{2}$，可以得到 $p = a - b$ 和 $q = a + b$，代入 $n$ 的计算公式有：

$$
n = p \times q = (a+b)(a-b) = a^2 - b^2
$$

也就是

$$
a^2 - n = b^2
$$

考虑到 $b$ 是正整数，所以 $a^2 - n$ 必须是一个完全平方数！考虑 $b$ 逐渐增大，即，使 $a$ 逐渐增大，我们只需要从 $a = \lceil \sqrt{n} \rceil$ 开始向上迭代即可，找到一个完全平方的 $a^2 - n$，即成功分解了 $n$！

编写 Python 脚本如下：

```python
"""baby_next_decode.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「baby_next」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""

import gmpy2

from Crypto.Util.number import long_to_bytes

# 在这里设置题目给定的数字。
n = 96742777571959902478849172116992100058097986518388851527052638944778038830381328778848540098201307724752598903628039482354215330671373992156290837979842156381411957754907190292238010742130674404082688791216045656050228686469536688900043735264177699512562466087275808541376525564145453954694429605944189276397
c = 17445962474813629559693587749061112782648120738023354591681532173123918523200368390246892643206880043853188835375836941118739796280111891950421612990713883817902247767311707918305107969264361136058458670735307702064189010952773013588328843994478490621886896074511809007736368751211179727573924125553940385967
e = 65537

a = gmpy2.isqrt(n)

# 校验 `a` 的初始值，使得初始的 `a` 满足 $a^2 \geq n$。
if a * a < n:
    a = a + 1

# 在这里搜索目标的 `a`。
print("🔍 开始搜索 `a`……")
while True:
    b_square = a * a - n
    if gmpy2.is_square(b_square):
        print(f"😋 成功找到 a = {a}")
        b = gmpy2.isqrt(b_square)
        break
    a += 1

# 计算 `p` 和 `q` 的值。
p = a - b
q = a + b
print("👍 分解成功！")
print(f"p = {p}")
print(f"q = {q}")

# 确保分解正确。
assert p * q == n

# 计算高斯函数并得到 `m`。
phi = (p - 1) * (q - 1)
d = gmpy2.invert(e, phi)
m = pow(c, d, n)

# 还原 `flag` 的值。
flag = long_to_bytes(m)
print(f"👀 解密得到的 `flag` 是 {flag.decode()}")
```

运行，得到：

```plain
PS S:\MoeCTF\Crypto> python .\baby_next_decode.py
🔍 开始搜索 `a`……
😋 成功找到 a = 9835790642950870702456388102541833011851580184211232019829465812360043670916676289614924432072209183922656300400121695605187082642402117584019839317552729
👍 分解成功！
p = 9835790642950870702456388102541833011851580184211232019829465812360043670916676289614924432072209183922656300400121695605187082642402117584019839297179867
q = 9835790642950870702456388102541833011851580184211232019829465812360043670916676289614924432072209183922656300400121695605187082642402117584019839337925591
👀 解密得到的 `flag` 是 moectf{vv0W_p_m1nu5_q_i5_r34l1y_sm4lI}
```

完成😋

### RSA 算法

在了解 RSA 算法之前，我们需要一些前置数学基础。

**欧拉函数 $\phi(n)$**

欧拉函数 $\phi(n)$ 表示小于或等于 $n$ 的正整数中，与 $n$ 互质的数的个数。例如，对于一个质数 $p$，它与小于自己的所有正整数全部互质，所以

$$
\phi(p) = p - 1
$$

而同理，对于两个不同的质数 $p$ 和 $q$，显然有

$$
\phi(p \times q) = (p - 1) \times (q - 1)
$$

**欧拉定理** <!--markdownlint-disable-line MD036-->

欧拉定理指出，对于任意两个互质的正整数 $a, m$，其中 $\gcd(a, m) = 1, m \geq 2$，有

$$
a^{\phi(m)} \equiv 1 \pmod{m}
$$

下面，我们研究 RSA 算法的全过程：

首先，我们需要生成 RSA 的公钥和私钥。我们选择两个大的质数 $p$ 和 $q$，计算它们的乘积 $n$，以及其欧拉函数 $\phi(n) = (p-1) \times (q-1)$。我们选择一个整数 $e$ 满足 $1 < e < \phi(n)$ 且 $e$ 与 $\phi(n)$ 互质，在这里，$e$ 选择了 65537。现在，我们计算出一个 $d$，使得 $d \times e \equiv 1 \pmod{\phi(n)}$，它即为 $e$ 模 $\phi(n)$ 的逆元。这样，公钥为 $(e, n)$ 而私钥为 $(d, n)$。

我们记明文为 $m$ 而密文为 $c$，它们可以这样互相运算：

$$
c = m^e \mod n\\
m = c^d \mod n
$$

解密过程具有精妙的数学逻辑。在密钥生成过程中，我们有 $d \times e \equiv 1 \pmod{\phi(n)}$，也就是 $\exists k \in \Z$ 使得

$$
e \times d = k \times \phi(n) + 1
$$

所以

$$
c^d = (m^e)^d = m^{e \times d} = m^{k \times \phi(n) + 1}
$$

我们的问题便转换为，证明 $m^{k \times \phi(n) + 1} \equiv m \pmod{n}$。$m$ 与 $n$ 互质时其证明显然，$m$ 与 $n$ 不互质时星澜音不会证明，但它绝对正确，这里就略去了。

## ezBSGS

> [!NOTE]
> **FLAG:** `moectf{18272162371285}`

题目要求我们找到

$$
13^x = 114514 \mod 100000000000099
$$

中 $x$ 的值。按照常理，这个 $x$ ~~可能不小，但绝对很大~~ 如果用普通的枚举法，事实上是难以操作的，我们直接引入 Baby-Step Giant-Step (BSGS) 算法来解决这道题目。

那么，如何理解 BSGS 算法？

例如，我们想找到一个 $x$ 使得 $a^x \equiv b \pmod{p}$：想象一个圆形的巨大操场，在它上面等距环绕着编号为从 $1$ 到 $p$ 的 $p$ 个位置，而我们从位置 $1$ 开始，每乘以一次 $a$，我们就在操场上（在模 $p$ 的意义下）前进 $a$ 倍的距离，我们最终的目标是，在走 $x$ 步之后，正好能停在位置 $b$ 上。最笨的方法就是枚举，我们每走 1 次就看看当前的位置是不是位于 $b$，但这个方法太慢了——题目的问题中，$p$ 的值是 $100,000,000,000,099$……

BSGS 算法就是解决这样的问题的。比如说，我们这次不亲自走了，我们派出两个人，分别叫他们 Baby-Step 和 Giant-Step，让 Baby-Step 一步一步地走，Giant-Step 一段一段地跳，然后让他们寻找一个碰头地点。这里，我们将总步数 $x$ 分为

$$
x = i \cdot m - j
$$

其中：

1. $i$ 表示 Giant-Step 要跳的次数；
2. $m$ 表示 Giant-Step 的一次跳，相当于 Baby-Step 多少次走；
3. $j$ 表示 Baby-Step 要向回走的步数。

先把这个式子代入原方程

$$
a^{i \cdot m - j} \equiv b \pmod{p}
$$

简单的移项后，有

$$
(a^m)^i \equiv b \cdot a^j \pmod{p}
$$

这便是整个算法的核心！现在，我们可以让 Baby-Step 先出发，Baby-Step 站在终点 $b$ 上，走 0 步时，记录一下「从终点走 0 步到这里」，这个位置是 $b \cdot a^0$；走 1 步时，再记录一下「从终点走 1 步到这里」，这个位置是 $b \cdot a^1$……Baby-Step 一直走到 $(m - 1)$ 步，把沿途经过的所有位置和对应的步数都记录在了一个哈希表里。这个哈希表相当于一张地图，它记录了从终点 $b$ 反向出发，走 $m$ 步以内能到达的所有位置。

紧接着，我们让 Giant-Step 再出发，Giant-Step 现在站在起点 $1$ 上，跳 1 次（相当于走了 $m$ 步）后，Giant-Step 会拿出这张地图检验自己所在的位置是不是位于地图上：如果是，那就结束；如果不是，那就再跳一次……Giant-Step 会一直跳，直到跳完第 $i$ 次后，突然发现自己所在的位置被 Baby-Step 标记过！这样，我们就得到了：Giant-Step 从起点 $1$ 跳了 $i$ 次 $m$ 步后到达了这里，而 Baby-Step 从终点 $b$ 往回走了 $j$ 步后也到达了这里！我们便能用这 $i$、$m$ 和 $j$ 算出总步数 $x$ 了。

暴力枚举的复杂度是 $O(p)$，而若使用 BSGS 算法，考虑到 Baby-Step 建立哈希表和 Giant-Step 寻找哈希表，各自最多只需要 走/跳 $m$ 次，我们取 $m = \lceil \sqrt{p} \rceil$，那么总共的计算量最多是 $2 \sqrt{p}$，将复杂度直接降到了 $O(\sqrt{p})$！在我们的问题中，$p$ 的值大约为 $10^{14}$，但 $\sqrt{p}$ 的值仅为 $10^7$，可以认为是容易计算的。

编写 Python 脚本如下：

```python
"""bsgs_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ezBSGS」题目使用。
由 星澜音 在 Gemini 和 DeepSeek 的帮助下编写。
"""

import math


def bsgs(a, b, p):
    """调用 Baby-Step Giant-Step 算法求解问题。"""

    # 计算 Giant-Step 一次跳的步数。
    m = int(math.sqrt(p)) + 1
    print(f"👣 计算得到 Giant-Step 一次跳的步数为 {m}\n")

    # 计算 Baby-Step 并存入哈希表。
    print("------ 下面开始 Baby-Step 的计算 ------")
    baby_steps = {}
    val = b
    for j in range(m):
        # `baby_steps`` 的键是位置，值是步数 `j`。
        baby_steps[val] = j
        val = (val * a) % p
    print(f"😋 已完成 {len(baby_steps)} 个小步计算，并将结果存入哈希表。")
    print("------ 上面完成 Baby-Step 的计算 ------")

    # 计算 Giant-Step 并与哈希表比对。
    print("\n------ 下面开始 Giant-Step 的计算 ------")
    # 计算 Giant-Step 的等效步数。
    giant_stride = pow(a, m, p)
    giant_val = giant_stride
    for i in range(1, m + 1):
        # 在哈希表中查找当前 Giant-Step 计算出的值。
        if giant_val in baby_steps:
            j = baby_steps[giant_val]
            x = i * m - j
            print(f"😰 在第 i = {i} 次 Giant-Step 时匹配成功！")
            print(f"😎 Giant-Step 计算结果: {giant_val}")
            print(f"👀 哈希表中匹配的 Baby-Step 步数: {j}")
            print(f"🥰 计算最终解 x = {i} * {m} - {j} = {x}")
            return x

        # 若匹配失败，则继续查找。
        giant_val = (giant_val * giant_stride) % p

    # 如果循环结束还未匹配成功，则可能无解。
    return None


if __name__ == "__main__":
    # 在这里更改 `BASE`、`RESULT` 和 `MODULUS` 的值。
    BASE = 13
    RESULT = 114514
    MODULUS = 100000000000099

    print("将使用下面的参数，以 BSGS 算法求解目标的 `x`：")
    print(f"a = {BASE}")
    print(f"b = {RESULT}")
    print(f"p = {MODULUS}")
    print("🤔 正在求解，请等待……")

    # 调用 BSGS 算法求解
    x = bsgs(BASE, RESULT, MODULUS)

    print("\n------ 🧮 最终结果 ⏱️ ------")
    if x is not None:
        print(f"🎮 方程的解 x = {x}")

        # 验证结果
        print("\n------ 🔍 验证解 🤔 ------")
        verification = pow(BASE, x, MODULUS)
        print(f"计算 {BASE}^{x} mod {MODULUS}……")
        print(f"计算结果: {verification}")
        print(f"目标结果: {RESULT}")
        if verification == RESULT:
            print(f"✅ 验证成功！方程的解确为 {x}。")
        else:
            print("❌ 验证失败。")
    else:
        print("😭 方程无解。")
```

运行，输出

```plain
PS S:\MoeCTF\Crypto> python .\bsgs_solver.py
将使用下面的参数，以 BSGS 算法求解目标的 `x`：
a = 13
b = 114514
p = 100000000000099
🤔 正在求解，请等待……
👣 计算得到 Giant-Step 一次跳的步数为 10000001

------ 下面开始 Baby-Step 的计算 ------
😋 已完成 10000001 个小步计算，并将结果存入哈希表。
------ 上面完成 Baby-Step 的计算 ------

------ 下面开始 Giant-Step 的计算 ------
😰 在第 i = 1827217 次 Giant-Step 时匹配成功！
😎 Giant-Step 计算结果: 30358557215417
👀 哈希表中匹配的 Baby-Step 步数: 9455932
🥰 计算最终解 x = 1827217 * 10000001 - 9455932 = 18272162371285

------ 🧮 最终结果 ⏱️ ------
🎮 方程的解 x = 18272162371285

------ 🔍 验证解 🤔 ------
计算 13^18272162371285 mod 100000000000099……
计算结果: 114514
目标结果: 114514
✅ 验证成功！方程的解确为 18272162371285。
```

得到结果，嵌套 `moectf{}` 即为答案。

## ez_square

> [!NOTE]
> **FLAG:** `moectf{Ma7hm4t1c5_is_@_k1nd_0f_a2t}`

题目提示了是简单的数学变形，那我们就看看有多简单。这里沿用记号 $p$、$q$、$n$、$e$、$m$ 和 $c$，简记 `hint` 为 $h$。我们的最终目标是解密出 $m$，在前面我们已经讨论过，这一点的前提是解密出 $p$ 和 $q$ 的值。既然已经知道了二者的乘积，我们考虑，若能知道二者的和，则能使用一元二次方程求根公式得到二者各自的值了。接下来，我们朝着这个方向努力。

已知 $n = p \times q$ 和 $h = (p+q)^2 \mod n$。考虑到 $p$ 和 $q$ 均为 `getPrime` 函数生成的 512 位随机数，记 $p \leq q$，显然的，有

$$
1 \leq \frac{q}{p} < 2
$$

知道这一点就很好操作了——事实上，考虑到 $h = (p+q)^2 \mod n$ 可表示为 $(p+q)^2 = k \cdot n + h \quad \text{where } k \in \Z_+$，我们总能通过对 $k$ 有限步的枚举得到 $(p + q)$ 的值。

不过，可能有人会问，**零学姐，为什么你不让** $k = 0$ **呢？** 事实上，集中注意力，我们可以注意到 $h$ 是完全平方数，它的二次根为

$$
\begin{align*}
\sqrt{h} = 2,
&343,458,209,274,425,996,985,047,093,820,\\
&966,198,128,351,630,302,072,151,512,123,\\
&489,799,998,738,482,601,894,111,632,387,\\
&083,653,590,921,895,308,705,989,628,111,\\
&300,210,058,143,690,024,967,352,474,744,452
\end{align*}
$$

这是不是说明 $k = 0$ 是可行的呢？事实上，并不可行，$k = 0$ 会让后续的一元二次方程出现 $\Delta < 0$ 的情况。有更好的方法可以分析出 $k$ 的大致范围，这里留作习题答案略，因为星澜音在实操的时候出错了（）

总之，知道了 $k$ 后我们就知道了 $(p + q)^2$，以此便知道了 $(p + q)$，随后使用一元二次方程求根公式即可。这里我们古法编程一波：

```python
"""ez_square_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_square」题目使用。
由 星澜音 独立编写。
"""

import math
import gmpy2
from Crypto.Util.number import long_to_bytes


# 在这里定义给出的常数。
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


# 我们验证 `S^2 = k*n + hint` 是否是完全平方数。考虑到无论如何均不能有 `(p+q)^2 = n`，这里的 k 从 1 开始取。
print("😋 即将开始破解 S = (p+q) 的值。\n")
k = 1
while True:
    print(f"✍️ 现在尝试 k = {k} 的情况……")
    current_s_square = k * n + hint
    if is_perfect_square(current_s_square):
        print(f"\n😎 已找到 k = {k} 使得 (k*n + hint) 为完全平方数！\n")
        break
    k = k + 1

# 验证完成后，保留 S^2 的值。
print(f"✍️ 下面我们以 k = {k} 计算 S^2。")
s_square = k * n + hint
s = math.isqrt(s_square)
assert s**2 == s_square
print(f"😎 得到 S^2 的值为 {s_square}\n")

# 下面使用求根公式得到 p 和 q 的值。
print("✍️ 这里我们假定 p < q，使用一元二次方程求根公式得到：")
inner_value = s_square - 4 * n
inner_value_sqrt = math.isqrt(inner_value)
assert inner_value_sqrt**2 == inner_value
p = (s - inner_value_sqrt) // 2
q = (s + inner_value_sqrt) // 2
print(f"p 为 {p}\nq 为 {q}\n")

# 下面计算 n 和 phi(n) 以及逆元 d。
n = p * q
print(f"✍️ 计算得到乘积 n = {n}\n")
phi_n = (p - 1) * (q - 1)
print(f"✍️ 计算欧拉函数 phi(n) = {phi_n}\n")
d = gmpy2.invert(e, phi_n)
print(f"✍️ 计算得到逆元 d = {d}\n")
m = pow(c, d, n)

# 下面解密 `flag`。
flag = long_to_bytes(m)
print(f"🤔 得到了 `flag` 的数值形式为 {m}")
print(f"😎 解密得到的 `flag` 是 {flag.decode()}")
```

运行，输出：

```plain
PS S:\MoeCTF\Crypto\ez_square> python .\ez_square_solver.py
😋 即将开始破解 S = (p+q) 的值。

✍️ 现在尝试 k = 1 的情况……
✍️ 现在尝试 k = 2 的情况……
✍️ 现在尝试 k = 3 的情况……
✍️ 现在尝试 k = 4 的情况……

😎 已找到 k = 4 使得 (k*n + hint) 为完全平方数！

✍️ 下面我们以 k = 4 计算 S^2。
😎 得到 S^2 的值为 341160920615455046727221841383116676082058185107901569916776317463514542293762606349463390642226334101447331013748038141618095449915459667608137074320591245224329145033774441198863295191676456574806412099041081655430035776596658427500482701674211070063359658012840102095582718546577589919690353106947757936900

✍️ 这里我们假定 p < q，使用一元二次方程求根公式得到：
p 为 8063541879684999172434156846785579383392012202377476576385935453837904086104134169422578105606735811577484535836740321806192056243591239447944792906642589
q 为 10407000088959425169419203940606545581520363832679548727898058943637902824586736063534210492690389402499379844542729949917492266301734929472912145381387041

✍️ 计算得到乘积 n = 83917281059209836833837824007690691544699901753577294450739161840987816051781770716778159151802639720854808886223999296102766845876403271538287419091422744267873129896312388567406645946985868002735024896571899580581985438021613509956651683237014111116217116870686535030557076307205101926450610365611263289149

✍️ 计算欧拉函数 phi(n) = 83917281059209836833837824007690691544699901753577294450739161840987816051781770716778159151802639720854808886223999296102766845876403271538287419091422725797331161251888046714045858554860903090358989839546595296587587962214702819086418726448415813991003040006306155560285352622882556600281689508672975259520

✍️ 计算得到逆元 d = 15793151114397884057990993199427147863227315687758401357331230024974346143135577765548343912268394316447551960002545238844187653951806734381391229794980055540904871185449244978730207660034093393296729796618211184340316308740957696730272801196496035060576948829482279058860789161094243757081867622869104122113

🤔 得到了 `flag` 的数值形式为 830454077261400323529837823102615274245009794059333438268265634706009918318016885885
😎 解密得到的 `flag` 是 moectf{Ma7hm4t1c5_is_@_k1nd_0f_a2t}
```

哈哈哈，赏心悦目。

## ezlegendre

> [!NOTE]
> **FLAG:** `moectf{Y0u_h@v3_ju5t_s01v3d_7h1s_pr0b13m!}`

分析题目给出的 Python 脚本（排版有优化）：

```python
from Crypto.Util.number import bytes_to_long, getPrime
from secret import flag

p = 258669765135238783146000574794031096183
a = 144901483389896508632771215712413815934


def encrypt_flag(flag):
    ciphertext = []
    plaintext = "".join([bin(i)[2:].zfill(8) for i in flag])
    for b in plaintext:
        e = getPrime(16)
        d = randint(1, 10)
        n = pow(a + int(b) * d, e, p)
        ciphertext.append(n)
    return ciphertext


print(encrypt_flag(flag))
```

首先，程序将 `flag` 的每个字节转换为 8 位二进制字符串（不足 8 位的在前面补 0），随后拼接这些二进制字符串为一个大的二进制字符串 `plaintext`。随后，程序对 `plaintext` 中的每一个二进制比特 `b` 进行如下操作：

1. 生成一个 16 位的随机素数 `e`；
2. 生成一个随机整数 `d`，这里 $1 \leq d \leq 10$；
3. 计算 $n = (a + b \cdot d)^e \mod p$。我们可以根据 `b` 来分情况讨论：若 $b = 0$ 则 $n = a^e \mod p$；若 $b = 1$ 则 $n = (a + d)^e \mod p$；
4. 将 `n` 追加到 `ciphertext` 中。

既然题目已经提示了 Legendre Symbol，我们就看看它如何被用于攻击这一算法。

先了解一个概念「二次剩余」。在通常的数学中，我们所说的「平方根」是指求一个数 $x$ 使得 $x^2 = a$，其中 $x$ 是实数或复数。不过，在模运算中，我们更关心同余关系：在数论中，给定一个奇素数 $p$ 和一个整数 $a$，若存在整数 $x$ 使得

$$
x^2 \equiv a \pmod{p}
$$

我们就说 $a$ 是模 $p$ 下的二次剩余，否则是二次非剩余。这样看来，二次剩余可以认为是在讨论求模意义下开平方运算的可行性。为什么说是「可行性」呢？如我们所见，并不是所有数在模 $p$ 下都能开平方，只有那些是二次剩余的 $a$ 才具有平方根模 $p$。

现在我们引入 Legendre Symbol，它是数论中的一个符号，表示一个整数是否是某个素数模下的二次剩余。给定一个素数 $p$ 和整数 $a$，Legendre Symbol 定义为：

$$
\left( \frac{a}{p} \right) =
\begin{cases}
1, & \text{如果 } a \text{ 是模 } p \text{ 的二次剩余（即存在 } x \text{ 使得 } x^2 \equiv a \pmod{p} ) \\
-1, & \text{如果 } a \text{ 不是模 } p \text{ 的二次剩余（即不存在 } x \text{ 使得 } x^2 \equiv a \pmod{p} ) \\
0, & \text{如果 } a \equiv 0 \pmod{p}
\end{cases}
$$

为什么说它的运用可以攻破这套加密算法的弱点呢？我们考虑：指数 $e$ 是一个 16 位的素数，而除 $2$ 之外的所有素数都是奇数，所以 $e$ 一定是奇数。我们知道，对于奇数 $e$，一个数的 $e$ 次方与其本身在模奇素数 $p$ 下的二次剩余性质相同，即，在 Legendre Symbol 下满足：

$$
\left( \frac{a^e}{p} \right) = \left( \frac{a}{p} \right)
$$

这个性质将在下文证明。总之，我们考虑每一个密文 $n$，计算其 $\left( \dfrac{n}{p} \right)$：

1. 若 $\left( \dfrac{n}{p} \right) \not = \left( \dfrac{a}{p} \right)$ 则必然有 $b = 1$。因为，若 $b = 0$，则根据 $a^e$ 的 Legendre Symbol 性质，必然有 $\left( \dfrac{n}{p} \right) = \left( \dfrac{a}{p} \right)$。
2. 若 $\left( \dfrac{n}{p} \right) = \left( \dfrac{a}{p} \right)$，则 $b$ **应该** 为 $0$。至于我们为什么说是「应该」，因为星澜音自己也拿不准，在任意符合条件的 $a$ 和 $p$ 的情况下，是否始终有 $\left( \dfrac{a + d}{p} \right) = -1, \forall d \in \Z \text{ and } d \in [1, 10]$。这可能需要一定数论知识才能证明 <sub>对不起星澜音这次真不会证明了😭</sub>，但至少题目给出的 $a$ 和 $p$ 经过星澜音手动校验后，确实满足我们刚刚的假设。

这样，我们就逆推出了 `plaintext` 的内容！编写 Python 脚本如下：

```python
"""ez_square_solver.py

该 Python 脚本供 MoeCTF 2025 的 Crypto 赛道中，「ez_square」题目使用。
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
```

运行，输出：

```plain
PS S:\MoeCTF\Crypto> python .\ezledengre_decrypt.py
成功读取 336 个加密数字。
计算出代表 '0' 的勒让德符号值为: 1

已成功恢复二进制 flag 字符串。正在转换为文本...

==============================
🎉 解密成功! 🎉
Flag: moectf{Y0u_h@v3_ju5t_s01v3d_7h1s_pr0b13m!}
==============================
```

### Euler's criterion

Euler's criterion 指出，对于奇素数 $p$ 和整数 $a$，有

$$
\left( \frac{a}{p} \right) \equiv a^{\frac{p - 1}{2}} \pmod{p}
$$

Euler's criterion 的证明需要用到 Fermat 小定理。 ~~后者星澜音不会证明，但星澜音确保后者是正确的。我们可以使用反证法：注意到，若 Euler's criterion 是错误的，则这么多年来绝对会有人推翻这一定理；但这么多年了，该定理仍未被推翻，所以它是正确的。~~

### Legendre Symbol 的乘法性质

$$
\left( \frac{a \cdot b}{p} \right) \equiv (a \cdot b)^{\frac{p = 1}{2}} \pmod{p}
$$

后者由指数运算的性质，可变形为

$$
\left( \frac{a \cdot b}{p} \right) \equiv a^{\frac{p = 1}{2}} \cdot b^{\frac{p = 1}{2}} \pmod{p}
$$

又

$$
\left( \frac{a}{p} \right) \equiv a^{\frac{p - 1}{2}} \pmod{p},\quad
\left( \frac{b}{p} \right) \equiv b^{\frac{p - 1}{2}} \pmod{p}
$$

所以

$$
\left( \frac{ab}{p} \right) \equiv \left( \frac{a}{p} \right) \cdot \left( \frac{b}{p} \right) \pmod{p}
$$

注意到 Legendre Symbol 的值仅为 $-1, 0, 1$ 中的任一，考虑到 $p$ 是奇素数，即 $p > 2$，模 $p$ 下这些值是唯一的（即 $-1 \not\equiv 1 \pmod{p}$），它的值便可以确定了。因此，我们写为

$$
\left( \frac{ab}{p} \right) = \left( \frac{a}{p} \right) \cdot \left( \frac{b}{p} \right)
$$

### $a^e$ 的二次剩余性质

由 Legendre Symbol 的乘法性质，推出 $a^e$ 的二次剩余性质是显然的，唯一需要注意的是，$e$ 在这里必须为奇数，以满足等式两边奇偶性的需求。

### 关于 $b = 0$ 的猜想

星澜音说自己这次不会是真不会了。不过，星澜音觉得，满足模 $p$ 且可二次剩余的数，在 $p$ 为一个极大素数的情况下，分布得应该足够稀疏？至少在一个较大的尺度来看，应该不至于出现两个差小于 $10$ 的。
