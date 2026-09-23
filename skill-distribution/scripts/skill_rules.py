#!/usr/bin/env python3
"""校验规则实现。由 validate_skill.py 调用，也可单独 import。

每个文件保持在 200 行以内（本技能包自己定的规范）。
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dir_rules import check_dirs  # noqa: E402
from skill_patterns import (  # noqa: E402
    NAME_RE, MAX_NAME, MAX_DESC, WARN_LINES, MAX_LINES,
    NEG, NUANCE, NOOP, VAGUE, SDO,
    SECRET, RISKY, GATE, LOOP, GUARD, ABS_PATH, NETWORK,
    strip_code, first_hit, parse_frontmatter,
)


def check_name(fm, dirname):
    errs = []
    nm = str(fm.get("name", "")).strip()
    if not nm:
        return ["缺少必填字段 name"]
    if not NAME_RE.match(nm):
        errs.append(f"name 非法：只允许小写字母/数字/连字符，无首尾连字符、无连续 -- （当前 {nm!r}）")
    if len(nm) > MAX_NAME:
        errs.append(f"name 超过 {MAX_NAME} 字符（当前 {len(nm)}）")
    if nm != dirname:
        errs.append(f"name 与目录名不一致：name={nm!r} 目录={dirname!r}（会静默失败）")
    if "anthropic" in nm or "claude" in nm:
        errs.append("name 含保留词 anthropic / claude")
    return errs


def check_description(fm):
    errs, warns, infos = [], [], []
    ds = str(fm.get("description", "")).strip()
    if not ds:
        return ["缺少必填字段 description"], [], []
    n = len(ds)
    if n > MAX_DESC:
        errs.append(f"description 超过 {MAX_DESC} 字符（当前 {n}）")
    elif n < 40:
        warns.append(f"description 仅 {n} 字符——太短会导致欠触发，建议 80–300")
    if "<" in ds and ">" in ds:
        errs.append("description 含 XML 标签")
    if not re.search(r"(不要|不用于|NOT|不适用)", ds, re.I):
        errs.append("description 缺少 Do NOT——过触发的主因")
    if re.search(r"^(我|我可以|I |I can)", ds):
        warns.append("description 应用第三人称（不写'我可以帮你'）")
    # SDO 陷阱：写了工作流摘要，模型会照摘要做而跳过正文
    if SDO.search(ds):
        warns.append("description 疑似含工作流摘要（SDO 陷阱）——"
                     "模型会照摘要执行而跳过正文，只写'何时用'不写'怎么做'")
    infos.append(f"description 长度 {n} 字符")
    return errs, warns, infos


def check_body(body, size):
    errs, warns, infos = [], [], []
    nl = len(body.strip().split("\n"))
    if nl > MAX_LINES:
        errs.append(f"SKILL.md 正文 {nl} 行，超过硬上限 {MAX_LINES}——必须拆分")
    elif nl > WARN_LINES:
        warns.append(f"SKILL.md 正文 {nl} 行，超过 {WARN_LINES}——建议拆到 references/")
    infos.append(f"SKILL.md 正文 {nl} 行（理想 100–150）")
    if size > 20000:
        warns.append("SKILL.md 超过 20,000 字符——可能被截断（截断保头不保尾）")

    low = body.lower()
    if not (("何时不用" in low) or ("不用于" in low) or ("do not" in low)):
        warns.append("正文缺少'何时不用'章节或 Do NOT 禁令——边界不清会导致乱跑")
    if not re.search(r"(禁止|红线|critical rules|critical\b)", low):
        warns.append("正文缺少 Critical Rules / 禁止项清单")
    if not re.search(r"(^|\n)#{1,3} ", body):
        warns.append("正文无标题结构——模型难以定位")

    plain = strip_code(body)
    lines = plain.split("\n")
    marks = re.compile(r"(❌|TODO|错误形态|反例)")
    # NOOP / VAGUE 用 NEG 跳过（含"禁用'尽量'"这类示范错误的行）；
    # NUANCE 用 marks 跳过（"除非"前是引号而非标点的引用行）
    for pat, msg, skip, lower in (
        (NUANCE, "含例外条款——会重新打开谈判空间且无法限定作用域", marks, False),
        (NOOP, "疑似空操作句（模型默认就会做，白占 token）", NEG, False),
        (VAGUE, "正文含模糊措辞——对模型等于没有约束", NEG, True),
    ):
        src = [l.lower() for l in lines] if lower else lines
        hit = first_hit(src, pat, skip)
        if hit:
            warns.append(f"{msg}：{hit.strip()[:40]}")

    # 安全：疑似硬编码凭据（跳过示范错误的行）
    hit = first_hit(lines, SECRET, NEG)
    if hit:
        warns.append(f"疑似硬编码凭据/内网地址——SKILL.md 是明文且会被自动加载："
                     f"{hit.strip()[:36]}（应改为'从环境变量读取'）")

    # 文件级检查：这些要看整篇是否配了配套机制
    # ⭐ 扫描类规则必须显式声明"不扫什么"，否则会把路由表与引用文本当成规则声明
    loop_src = "\n".join(l for l in plain.split("\n")
                         if not l.lstrip().startswith(("|", ">")))
    for pat, guard, msg in ((RISKY, GATE, "涉及高危操作但未设人工确认门槛——"
                                          "应要求先输出命令清单待用户确认"),
                            (LOOP, GUARD, "涉及重复/循环但未设最大次数——"
                                          "见过循环 200 次烧光 token 的生产事故")):
        if pat.search(loop_src) and not guard.search(loop_src):
            warns.append(msg)

    # 网络访问——潜在的数据外泄途径；这里只提示，是否可信需人工确认
    hit = first_hit(lines, NETWORK, NEG)
    if hit:
        warns.append(f"含网络访问——审查时需确认目标域名是否可信：{hit.strip()[:36]}"
                     f"（见 skill-evaluating/references/security-review.md）")

    # 硬编码项目专属路径——换个用户就断
    hit = first_hit(lines, ABS_PATH, NEG)
    if hit:
        warns.append(f"硬编码项目专属路径——换个用户/机器就断：{hit.strip()[:36]}"
                     f"（改用相对路径或写'在项目根定位 migrations 目录'）")
    return errs, warns, infos


def check(path, strict=False):
    errs, warns, infos = [], [], []
    if not os.path.isdir(path):
        return ["目录不存在"], [], []
    skill_md = os.path.join(path, "SKILL.md")
    if not os.path.isfile(skill_md):
        return ["缺少 SKILL.md"], [], []

    fm, body = parse_frontmatter(open(skill_md, encoding="utf-8").read())
    if fm is None:
        return ["frontmatter 缺失或格式错误：必须以顶格的 --- 开始并以 --- 结束"], [], []

    e = check_name(fm, os.path.basename(os.path.abspath(path)))
    errs += e
    e, w, i = check_description(fm)
    errs, warns, infos = errs + e, warns + w, infos + i
    e, w, i = check_body(body, os.path.getsize(skill_md))
    errs, warns, infos = errs + e, warns + w, infos + i
    e, w = check_dirs(path, open(skill_md, encoding="utf-8").read())
    errs, warns = errs + e, warns + w

    if strict and warns:
        errs.extend(warns)
    return errs, warns, infos
