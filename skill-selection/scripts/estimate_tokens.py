#!/usr/bin/env python3
"""估算技能包的 token 占用与预算占比。

用法:
  python estimate_tokens.py ./my-skill            # 单个技能
  python estimate_tokens.py ~/.claude/skills      # 整个技能库

输出三层成本：启动常驻 / 按需加载 / 不进上下文。
退出码: 0=在预算内  1=超预算  2=参数错误
"""
import os
import re
import sys

# Claude tokenizer 经验系数：CJK 约 0.75 token/字，ASCII 约 1 token/4 字符
CJK = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]")
CJK_PER_TOKEN = 0.75
ASCII_CHARS_PER_TOKEN = 4.0
# 描述总预算 = 上下文窗口的 2%
WINDOWS = {"200k": 200_000, "1m": 1_000_000}
DESC_BUDGET_PCT = 0.02
# 单技能描述目标（字符）
DESC_TARGET = (300, 500)
# 正文行数（与 validate_skill.py 口径一致）
BODY_WARN, BODY_MAX = 300, 500


def tok(text):
    """按 CJK / ASCII 分别估算，比单一系数准。"""
    n_cjk = len(CJK.findall(text))
    n_ascii = len(text) - n_cjk
    return int(n_cjk * CJK_PER_TOKEN + n_ascii / ASCII_CHARS_PER_TOKEN)


def read(p):
    try:
        return open(p, encoding="utf-8").read()
    except (OSError, UnicodeDecodeError):
        return ""


def scan_dir(d):
    """返回 (frontmatter, body, refs[(name,size)], scripts[(name,size)])."""
    skill_md = os.path.join(d, "SKILL.md")
    text = read(skill_md)
    desc, body = "", text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            desc = text[3:end]
            body = text[end + 4:]
    refs, scripts = [], []
    for sub, acc in (("references", refs), ("scripts", scripts)):
        sd = os.path.join(d, sub)
        if os.path.isdir(sd):
            for f in sorted(os.listdir(sd)):
                fp = os.path.join(sd, f)
                if os.path.isfile(fp):
                    acc.append((f, os.path.getsize(fp)))
    return desc, body, refs, scripts


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    root = args[0]
    if not os.path.isdir(root):
        print(f"错误：{root} 不是目录")
        return 2

    # 收集技能目录：root 本身是技能，或 root 下每个子目录是技能
    if os.path.isfile(os.path.join(root, "SKILL.md")):
        skills = [root]
    else:
        skills = [os.path.join(root, d) for d in sorted(os.listdir(root))
                  if os.path.isfile(os.path.join(root, d, "SKILL.md"))]
    if not skills:
        print(f"错误：{root} 下没找到任何 SKILL.md")
        return 2

    total_desc = 0
    rows = []
    over = False
    for s in skills:
        desc, body, refs, scripts = scan_dir(s)
        d_chars = len(desc.strip())
        b_lines = len(body.strip().split("\n"))
        total_desc += d_chars
        flag = ""
        if d_chars > DESC_TARGET[1] * 2:
            flag = "  ⚠ 描述过长"
            over = True
        elif d_chars < DESC_TARGET[0]:
            flag = "  · 描述偏短（易欠触发）"
        # 行数与 validate_skill.py 同口径；token 只作参考（中文密度高于英文）
        if b_lines > BODY_MAX:
            flag += "  ❌ 正文超 500 行，须拆"
            over = True
        elif b_lines > BODY_WARN:
            flag += "  ⚠ 正文超 300 行，建议拆"
        rows.append((os.path.basename(s), d_chars, b_lines, tok(body),
                     tok("".join(read(os.path.join(s, "references", f))
                                 for f, _ in refs)),
                     len(refs), len(scripts), flag))

    print("=== 三层成本 ===")
    print(f"{'技能':<22}{'描述字符':>8}{'正文行':>7}{'正文tok':>9}"
          f"{'ref tok':>9}{'ref数':>7}{'脚本':>6}")
    for n, d, bl, bt, r, nr, ns, flag in rows:
        print(f"{n:<22}{d:>8}{bl:>7}{bt:>9}{r:>9}{nr:>7}{ns:>6}{flag}")

    desc_tok = tok("描" * total_desc)  # 描述以中文为主，按 CJK 口径估
    print(f"\n启动常驻（全部描述）：{len(skills)} 个技能 = "
          f"{total_desc} 字符 ≈ {desc_tok} tokens")

    for label, win in WINDOWS.items():
        budget_chars = win * DESC_BUDGET_PCT
        pct = total_desc / budget_chars * 100 if budget_chars else 0
        mark = "❌ 超预算" if pct > 100 else ("⚠ 接近" if pct > 80 else "✅")
        print(f"  占 {label} 窗口 2% 预算（{int(budget_chars)} 字符）的 "
              f"{pct:.1f}%  {mark}")
        if pct > 100:
            over = True

    print("\n规则：")
    print("  · 单个 description 目标 300–500 字符（这是硬约束，按字符算）")
    print(f"  · 正文行数 >{BODY_WARN} 建议拆，>{BODY_MAX} 必须拆（与 validate 同口径）")
    print("  · token 列仅供参考：中文信息密度高于英文，同样行数 token 更多")
    print("  · references/ 与 scripts/ 不进上下文，除非被读取")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main())
