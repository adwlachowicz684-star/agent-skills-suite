#!/usr/bin/env python3
"""校验用的正则常量与小工具。单独成文件，保持每个文件 <200 行。"""
import re

try:
    import yaml
except ImportError:
    yaml = None

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME, MAX_DESC = 64, 1024
WARN_LINES, MAX_LINES = 300, 500

# 反例引用标记：含这些词的行是在"示范错误"，不算违规
NEG = re.compile(r"(禁用|不要|避免|禁止|不许|反例|如|例|❌|TODO|从环境变量)")
# nuance clause 典型形态：「……，除非 X」。用标点精确锚定，避免误报反例行
NUANCE = re.compile(r"[，,、；;]\s*(除非|unless|如有需要|if needed|except|特殊情况|如果不)")
NOOP = re.compile(r"(请(认真|仔细|务必)|要(仔细|认真)|尽量详细|注意思考|"
                  r"think carefully|be careful|be thorough)")
VAGUE = re.compile(r"(尽量|酌情|合适即可|适当即可|when appropriate|if needed)")
SDO = re.compile(r"(第一步|然后|接着|随后|步骤\s*[123一二三]|首先)")
REF_LINK = re.compile(r"\[[^\]]+\]\((?!http)([^)#]+\.md)\)")
TOC = re.compile(r"^#{1,3} .*目录", re.M)

# 安全：疑似硬编码凭据（SKILL.md 是明文且会被自动加载，泄露面大于普通文档）
SECRET = re.compile(
    r"(sk-[A-Za-z0-9]{8,}|ghp_[A-Za-z0-9]{10,}|AKIA[0-9A-Z]{10,}"
    r"|password\s*[:=]\s*[\"'][^\"']{4,}|passwd\s*[:=]\s*[\"']"
    r"|jdbc:[a-z]+://|mongodb(\+srv)?://[^\s]*:[^\s@]+@"
    r"|https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", re.I)
# 高危操作
RISKY = re.compile(r"(rm\s+-rf|git\s+push\s+(-f|--force)|drop\s+table|truncate\s+table"
                   r"|kubectl\s+delete|--no-verify|force\s+push)", re.I)
# 高危操作的确认门槛
GATE = re.compile(r"(确认|confirm|人工|先输出将要执行|ask|审批|dry[-\s]?run)")
# 网络访问 / 潜在数据外泄（见 skill-evaluating/references/security-review.md）
NETWORK = re.compile(r"https?://|(?:^|\s)(curl|wget|fetch|requests\.(?:get|post)|urllib"
                     r"|axios|http\.request)\s*[(（]", re.I)
# 循环
LOOP = re.compile(r"(回到第\s*\d+\s*步|重试|重复执行|循环执行|重新运行|repeat until)", re.I)
# 循环守卫
GUARD = re.compile(r"(最多|最大次数|上限|不超过|max\s*\d|at most|最多重试)")
# 硬编码项目专属路径——换个用户就断
ABS_PATH = re.compile(r"(?<![\w`~/])(/Users/|/home/[a-z]+/|C:\\\\Users\\\\|/mnt/c/Users/)",
                      re.I)

CODE_FENCE = re.compile(r"```.*?```", re.S)


def strip_code(text):
    """去掉围栏代码块后再做内容检查——示例里的 rm -rf 不是真指令。"""
    return CODE_FENCE.sub("", text)


def first_hit(lines, pat, skip):
    """返回第一条命中 pat 且不含 skip 标记的行，没有则 None。"""
    for ln in lines:
        if pat.search(ln) and not skip.search(ln):
            return ln
    return None


def parse_frontmatter(text):
    """返回 (frontmatter_dict, body)。失败返回 (None, text)。"""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end < 0:
        return None, text
    raw, body = text[3:end].strip(), text[end + 4:]
    if yaml:
        try:
            return (yaml.safe_load(raw) or {}), body
        except yaml.YAMLError:
            pass
    fm = {}
    for line in raw.split("\n"):
        m = re.match(r"^([a-zA-Z_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm, body
