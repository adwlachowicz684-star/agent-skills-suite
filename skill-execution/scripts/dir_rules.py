# -*- coding: utf-8 -*-
"""目录级检查：references/ scripts/ assets/ 的组织与工程纪律。

从 skill_rules.py 拆出，避免单文件超过 200 行（见 references/script-engineering.md）。
"""
import os
import re

from skill_patterns import (  # noqa: E402
    SECRET, ABS_PATH, REF_LINK, TOC,
)


def check_dirs(path, skill_text=""):
    errs, warns = [], []
    refs = os.path.join(path, "references")
    # 所有可能引用 assets/ 的文本：SKILL.md + 全部 references
    corpus = skill_text
    if os.path.isdir(refs):
        for f in os.listdir(refs):
            fp = os.path.join(refs, f)
            if f.endswith(".md") and os.path.isfile(fp):
                corpus += open(fp, encoding="utf-8").read()
    if os.path.isdir(refs):
        for f in sorted(os.listdir(refs)):
            fp = os.path.join(refs, f)
            if not f.endswith(".md") or not os.path.isfile(fp):
                continue
            txt = open(fp, encoding="utf-8").read()
            sub = REF_LINK.findall(txt)
            if sub:
                errs.append(f"references/{f} 链向了其他 md（{sub[0]}）——禁止 A→B→C 链套")
            n = len(txt.split("\n"))
            if n > 300:
                warns.append(f"references/{f} {n} 行，超过 300——建议按子主题拆分")
            elif n > 100 and not TOC.search(txt):
                warns.append(f"references/{f} {n} 行但无目录——超过 100 行应加 TOC")

    sc = os.path.join(path, "scripts")
    if os.path.isdir(sc):
        for f in sorted(os.listdir(sc)):
            fp = os.path.join(sc, f)
            if not os.path.isfile(fp):
                continue
            if f.endswith((".py", ".sh")) and not os.access(fp, os.X_OK):
                warns.append(f"scripts/{f} 不可执行——建议 chmod +x")
            txt = open(fp, encoding="utf-8").read()
            n = len(txt.split("\n"))
            if n > 200:
                warns.append(f"scripts/{f} {n} 行，超过 200——建议拆分")
            # 脚本工程纪律（见 references/script-engineering.md）
            # 只扫描"真实代码行"：跳过正则定义与字符串字面量，避免校验器扫自己时误报
            code_lines = [
                ln for ln in txt.split("\n")
                if not ln.strip().startswith("#")
                and "re.compile(" not in ln and "Pattern(" not in ln and "re." not in ln
            ]
            code = "\n".join(code_lines)
            if SECRET.search(code):
                warns.append(f"scripts/{f} 疑似硬编码凭据——走环境变量，绝不写进文件")
            if ABS_PATH.search(code):
                warns.append(f"scripts/{f} 硬编码绝对路径——换机器/项目就断，改用相对路径")
            if f.endswith(".py"):
                # input() 必须是真实调用，而不是被引号包起来的字符串
                if re.search(r"[^'\"`]\binput\s*\(", code):
                    warns.append(f"scripts/{f} 用了交互式 input 调用——非交互环境会挂死，改成参数")
                # 以下两条只约束"给 agent 独立执行的脚本"。
                # 有 __main__ 的是给人用的 CLI 入口，输出给人看、异常直接抛是合理设计；
                # 被同目录其他脚本 import 的是库模块，异常由调用方统一处理——同样不适用。
                is_cli = 'if __name__' in code
                stem = f.rsplit(".", 1)[0]
                is_lib = any(
                    re.search(rf"^\s*(from|import)\s+{re.escape(stem)}\b", o, re.M)
                    for g in sorted(os.listdir(sc)) if g.endswith(".py") and g != f
                    for o in [open(os.path.join(sc, g), encoding="utf-8").read()]
                )
                if not is_cli and not is_lib:
                    if "except" not in code and "open(" in code:
                        warns.append(f"scripts/{f} 有文件操作但无异常处理——错误会意外向上抛")
                    if "print(" in code and "json" not in code and n > 30:
                        warns.append(f"scripts/{f} 输出疑似非结构化——优先 JSON，数据与诊断分离")

    # assets/：未被任何地方引用的资源是噪音（见 references/directory-contract.md）
    ast_dir = os.path.join(path, "assets")
    if os.path.isdir(ast_dir) and corpus:
        for f in sorted(os.listdir(ast_dir)):
            fp = os.path.join(ast_dir, f)
            if not os.path.isfile(fp):
                continue
            if f not in corpus and f.rsplit(".", 1)[0] not in corpus:
                warns.append(f"assets/{f} 未被 SKILL.md 或 references 引用——"
                             f"未被引用的资源是噪音，会稀释检索")
    return errs, warns
