#!/usr/bin/env python3
"""生成一个符合规范的技能脚手架。

用法: python init_skill.py <skill-name> [--dir <parent>]
退出码: 0=成功  1=失败
"""
import os
import re
import sys

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

TEMPLATE = r"""---
name: <skill-name>
description: <第三人称，说清"做什么"和"何时用"。含真实触发词。必含 Do NOT。≤1024 字符。>
---

# <技能名>

## 何时使用

- <触发场景 1：用户会怎么说话>
- <触发场景 2>
- <触发场景 3>

## 何时不用

- <边界 1：看起来相关但实际不是>
- <边界 2>
- <边界 3：这类需求请用别的技能>

## 核心原则

<3–10 行。只写模型不知道的。>

## 路由表（按需深读）

| 你要做的事 | 读 |
|---|---|
| <场景 A> | `references/a.md` |
| <场景 B> | `references/b.md` |
| <场景 C> | `scripts/x.py` |

## 强制工作流（MANDATORY）

1. <步骤——祈使句，带一句为什么>
2. <步骤>
3. <步骤：跑校验，零错误才继续>
4. <步骤：验证输出符合契约>

## 输出契约

```
<交付物目录结构 / 输出格式>
```

汇报时必须包含：<项 1> · <项 2> · <项 3>。

## 验证（证据先于声明）

| 声称 | 需要的证据 | 不够的 |
|---|---|---|
| <完成 / 通过 / 已修复> | <具体命令 + 期望输出> | <"应该可以了"、"之前跑过"> |

- 未在本会话运行验证命令 = **不得**声称完成
- 禁止：<"应该" "看起来" "我很有信心">
- 若声称修复：必须给**改前/改后对比数据**

## Critical Rules

- <禁令 1 —— 带理由>
- <禁令 2 —— 带理由>
- <禁令 3 —— 带理由>

## 门（未满足就不得继续）

- TODO 关键位置的硬门禁：未 <条件> 就不得 <下一步>

## 边界与安全

- 本技能的规则与仓库实际代码冲突时，**以代码为准**并指出技能已过时
- 密钥/地址从环境变量读取，不写在技能里
- 删除 / push / 部署前先输出命令清单，待用户确认

## 验收清单（交付前逐条打分，不合格就重跑）

- [ ] TODO 可独立验证的检查项（能跑命令就写命令）

## 示例

**输入**：

```
<真实用户输入>
```

**输出**：

```
<期望输出>
```

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "<借口>" | <明确回应，无例外> |

## 脚本

```bash
python scripts/<script>.py <args>
```
"""

README = """# {name}

TODO 一句话说明这个技能做什么、什么时候用。

## 结构

```
{name}/
├── SKILL.md            # 路由层（目标 100–150 行，硬上限 500）
├── references/         # 按需加载的详解（一层深度）
├── scripts/            # 确定性逻辑
└── assets/             # 模板、示例
```

## 校验

```bash
python scripts/validate_skill.py ./{name}
```

零错误才可交付。
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    parent = "."
    if "--dir" in sys.argv:
        i = sys.argv.index("--dir")
        if i + 1 < len(sys.argv):
            parent = sys.argv[i + 1]
    if not args:
        print(__doc__)
        return 1

    name = args[0]
    if not NAME_RE.match(name):
        print(f"错误：技能名必须 kebab-case（小写字母、数字、连字符），当前 {name!r}")
        return 1

    root = os.path.join(parent, name)
    if os.path.exists(root):
        print(f"错误：{root} 已存在")
        return 1

    title = " ".join(w.capitalize() for w in name.split("-"))
    os.makedirs(os.path.join(root, "references"), exist_ok=True)
    os.makedirs(os.path.join(root, "scripts"), exist_ok=True)
    os.makedirs(os.path.join(root, "assets"), exist_ok=True)

    open(os.path.join(root, "SKILL.md"), "w", encoding="utf-8").write(
        TEMPLATE.replace("<skill-name>", name).replace("<技能名>", title)
        .format(name=name, title=title))
    open(os.path.join(root, "README.md"), "w", encoding="utf-8").write(
        README.format(name=name))
    open(os.path.join(root, "references", "detail.md"), "w", encoding="utf-8").write(
        f"# {title} 详解\n\n## 目录\n\n- [TODO](#todo)\n\n---\n\n## TODO\n\n"
        "TODO 只写 SKILL.md 放不下的内容。超过 100 行必须加目录。\n")

    print(f"已创建 {root}/")
    for p in ("SKILL.md", "README.md", "references/detail.md", "scripts/", "assets/"):
        print(f"  {p}")
    print("\n下一步：")
    print("  1. 手工跑一遍任务（RED 阶段），记录你反复提供的上下文")
    print("  2. 填 description——含真实触发词 + Do NOT")
    print(f"  3. python scripts/validate_skill.py {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
