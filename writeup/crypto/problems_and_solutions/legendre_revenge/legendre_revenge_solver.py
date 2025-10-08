# ctf_crypto_solver.py
# 依赖: pycryptodome, gmpy2
# pip install pycryptodome gmpy2

from Crypto.Cipher import AES
from itertools import product
import gmpy2
import sys

# ---------- paste constants from the challenge ----------
p = 251
e = 65537

# challenge constants (from prompt)
p_ = 71583805456773770888820224577418671344500223401233301642692926000191389937709
V = 1679283667939124174051653611794421444808492935736643969239278575726980681302

text_val = 26588763961966808496088145486940545448967891102453278501457496293530671899568

a = [
    [239, 239, 251, 239],
    [233, 227, 233, 251],
    [251, 239, 251, 233],
    [233, 227, 251, 233],
]

lis0 = [
    [341, 710, 523, 1016],
    [636, 366, 441, 790],
    [637, 347, 728, 426],
    [150, 184, 421, 733],
]
lis1 = [
    [133, 301, 251, 543],
    [444, 996, 507, 1005],
    [18, 902, 379, 878],
    [235, 448, 836, 263],
]
# ------------------------------------------------------


# ---------- small helpers ----------
def function_ch(x, modp):
    """Replicate challenge's function: if x>=modp return x; else if x is quadratic residue modp -> x^2 modp, else x^3 modp"""
    if x >= modp:
        return x
    if pow(x, (modp - 1) // 2, modp) == 1:
        return pow(x, 2, modp)
    else:
        return pow(x, 3, modp)


def matrix_to_str(matrix):
    # challenge: flatten by rows then cols, then rstrip nulls
    b = bytes(sum([[matrix[row][col] for col in range(4)] for row in range(4)], []))
    return b.rstrip(b"\0")


def str_to_matrix(s):
    # challenge: matrix = [[function(s[row + 4*col],p) for row in range(4)] for col in range(4)]
    matrix = [
        [function_ch(s[row + 4 * col], p) for row in range(4)] for col in range(4)
    ]
    return matrix


def forward_round(plaintext16, cipher, a_mat):
    """Replicate exactly one forward round in challenge:
    enc = cipher.encrypt(plaintext16)
    matrix = str_to_matrix(enc)
    for row,col: lis bit uses matrix[row][col] > a[row][col]//2
    matrix = [[function(matrix[col][row], a[col][row]) for row in range(4)] for col in range(4)]
    out = matrix_to_str(matrix)
    returns out (16 bytes) and bitmat (4x4 of 0/1)
    """
    enc = cipher.encrypt(plaintext16)
    # build initial matrix as challenge: outer index = col, inner = row
    M = [[function_ch(enc[row + 4 * col], p) for row in range(4)] for col in range(4)]
    # bit matrix using matrix[row][col] (note indexing transpose in challenge)
    bitmat = [[0] * 4 for _ in range(4)]
    for row in range(4):
        for col in range(4):
            bitmat[row][col] = 1 if M[row][col] > a_mat[row][col] // 2 else 0
    # second application: matrix[col][row] -> function(..., a[col][row])
    M2 = [
        [function_ch(M[col][row], a_mat[col][row]) for row in range(4)]
        for col in range(4)
    ]
    out = matrix_to_str(M2)
    return out, bitmat


# ---------- Tonelli-Shanks sqrt mod p_ ----------
def tonelli_shanks(n, p):
    """Return a sqrt r such that r^2 = n mod p (p odd prime) or raise if non-residue"""
    if n == 0:
        return 0
    assert gmpy2.powmod(n, (p - 1) // 2, p) == 1
    if p % 4 == 3:
        return int(gmpy2.powmod(n, (p + 1) // 4, p))
    # Find Q and S with p-1 = Q * 2^S, Q odd
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1
    # find z a quadratic non-residue
    z = 2
    while gmpy2.powmod(z, (p - 1) // 2, p) != p - 1:
        z += 1
    M = S
    c = int(gmpy2.powmod(z, Q, p))
    t = int(gmpy2.powmod(n, Q, p))
    R = int(gmpy2.powmod(n, (Q + 1) // 2, p))
    while True:
        if t == 0:
            return 0
        if t == 1:
            return R
        # find least i (0 < i < M) with t^(2^i) = 1
        i = 1
        t2i = (t * t) % p
        while t2i != 1:
            t2i = (t2i * t2i) % p
            i += 1
            if i >= M:
                raise RuntimeError("TS failed")
        b = int(gmpy2.powmod(c, 1 << (M - i - 1), p))
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p


# ---------- bits extraction from lis (MSB-first) ----------
def lis_to_bitmats(lis):
    """Convert lis (4x4 ints) into list of 10 bit-matrices (round 0..9), MSB-first as in challenge shift<<1 then add."""
    rounds = 10
    bitmats = []
    for r in range(rounds):
        bm = [
            [(lis[row][col] >> (rounds - 1 - r)) & 1 for col in range(4)]
            for row in range(4)
        ]
        bitmats.append(bm)
    return bitmats


# ---------- invert one round ----------
def invert_one_round(current_text16, bitmat, a_mat, cipher):
    """
    Given the output bytes after one round (current_text16), the bit matrix for that round,
    and the a matrix, find all candidate previous plain 16-byte blocks.

    Strategy: for each position (row,col) the mapping is:
        j = col + 4*row  (index in enc)
        k = row*4 + col  (index in output)
    We need x in [0..255] such that:
        m = function_ch(x, p)
        bit condition: (m > a[row][col]//2) == bitmat[row][col]
        and function_ch(m, a[row][col]) % ? == out_byte (but function_ch returns integer possibly >= 256).
    However matrix_to_str flattened raw integers into bytes; therefore the values must fit into 0..255.
    So we require function_ch(m, a[row][col]) == out_byte_byte (0..255).
    """
    if len(current_text16) < 16:
        # If rstrip removed trailing zeros, pad to 16 with zeros to reconstruct the full 4x4
        current_text = current_text16 + b"\x00" * (16 - len(current_text16))
    else:
        current_text = current_text16[:16]

    # For each position j (enc index), build candidate bytes x
    per_pos_candidates = []
    for row in range(4):
        for col in range(4):
            j = col + 4 * row
            k = row * 4 + col
            target_out = current_text[k]
            a_param = a_mat[row][col]
            want_bit = bitmat[row][col]
            candidates = []
            for x in range(256):
                m = function_ch(x, p)  # m in 0..p-1 (since x<p)
                # bit check
                bit = 1 if m > a_param // 2 else 0
                if bit != want_bit:
                    continue
                # second function
                val = function_ch(m, a_param)
                # But note: matrix_to_str used bytes(...) where each element must be 0..255
                if val == target_out:
                    candidates.append(x)
            if len(candidates) == 0:
                # no solution for this position -> impossible
                return []
            per_pos_candidates.append(candidates)

    # Now combine candidates: the total search size = product of len(cands)
    total = 1
    for c in per_pos_candidates:
        total *= len(c)
    # Heuristic: if total too big, give up to prevent explosion
    MAX_COMB = 3_000_000
    if total > MAX_COMB:
        print(
            f"[!] candidate space too large: {total} combinations -> abort this branch",
            file=sys.stderr,
        )
        return []

    prev_texts = []
    # iterate cartesian product
    for combo in product(*per_pos_candidates):
        enc = bytes(combo)
        # decrypt to get previous plaintext
        prev_plain = cipher.decrypt(enc)
        # verify by forward_round to be safe
        out2, bit2 = forward_round(prev_plain, cipher, a_mat)
        # out2 may be shorter due to rstrip, but compare as in challenge
        if out2 == current_text16 or (
            len(out2) >= len(current_text16)
            and out2[: len(current_text16)] == current_text16
        ):
            # also ensure bit2 equals provided bitmat
            if bit2 == bitmat:
                prev_texts.append(prev_plain)
    return prev_texts


# ---------- overall backtracking for one 16-byte chain ----------
def backtrack_chain(final_block16, lis, a_mat, cipher, rounds=10):
    """Given final 16B block (after 10 rounds), backtrack all possible original plaintexts."""
    bitmats = lis_to_bitmats(lis)
    # start from final block (this is text_[t] after 10 rounds)
    curr_candidates = [final_block16]
    for r in reversed(range(rounds)):
        print(
            f"[+] backtracking round {r} ... current candidates: {len(curr_candidates)}"
        )
        next_candidates = []
        bm = bitmats[r]
        for cand in curr_candidates:
            prevs = invert_one_round(cand, bm, a_mat, cipher)
            if prevs:
                next_candidates.extend(prevs)
        # deduplicate
        # convert to bytes to dedup
        uniq = {}
        for b in next_candidates:
            uniq[b] = True
        curr_candidates = list(uniq.keys())
        if not curr_candidates:
            print(f"[!] no candidates found at round {r}, aborting this branch")
            return []
    return curr_candidates


# ---------- find key by brute (0..65535) ----------
def find_key():
    print("[*] searching key in 0..65535 ...")
    for k in range(1 << 16):
        if pow(k, 2 * e, p_) == V:
            print(f"[+] found key = {k}")
            return k
    print("[!] key not found")
    return None


# ---------- main ----------
def main():
    key = find_key()
    if key is None:
        return
    aes_key_bytes = (key << 107).to_bytes(
        16, "big"
    )  # same as long_to_bytes(key<<107) with 16B
    print(f"[*] AES key bytes (hex): {aes_key_bytes.hex()}")
    cipher = AES.new(aes_key_bytes, AES.MODE_ECB)

    # modular sqrt of text_val
    print("[*] computing modular sqrt of text_val ...")
    if gmpy2.powmod(text_val, (p_ - 1) // 2, p_) != 1:
        print("[!] text_val is not quadratic residue mod p_, cannot sqrt")
        return
    r = tonelli_shanks(text_val, p_)
    roots = [int(r), int(p_ - r)]
    print(f"[*] two roots computed. trying both...")

    # try each root -> split into two 16-byte blocks
    sols = []
    for root in roots:
        b32 = int(root).to_bytes(32, "big")
        block0 = b32[:16]
        block1 = b32[16:]
        print(f"[*] trying root: {root}")
        # backtrack t=0 using lis0, t=1 using lis1
        print("[*] backtracking block0 with lis0 ...")
        cand0 = backtrack_chain(block0, lis0, a, cipher)
        print(f"[*] backtracking block1 with lis1 ...")
        cand1 = backtrack_chain(block1, lis1, a, cipher)
        # combine cartesian product of cand0 x cand1 to form flags
        for p0 in cand0:
            for p1 in cand1:
                flag_bytes = p0 + p1
                # attempt to decode as utf-8/printable
                try:
                    flag_str = flag_bytes.decode("utf-8")
                except:
                    flag_str = None
                sols.append((flag_bytes, flag_str))
    # report solutions
    if not sols:
        print("[!] no candidate flags recovered.")
    else:
        print(f"[+] found {len(sols)} candidate flag(s):")
        for idx, (fb, fs) in enumerate(sols):
            if fs and all(32 <= ord(ch) <= 126 for ch in fs):
                print(f"[*] Candidate {idx}: {fs}")
            else:
                print(f"[*] Candidate {idx}: bytes(hex) = {fb.hex()}")
                if fs:
                    print(f"    as utf-8 (nonprintable?): {fs!r}")


if __name__ == "__main__":
    main()
