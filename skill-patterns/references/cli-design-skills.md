# Agent 兼容 CLI 的设计约定

> 一个容易被忽略但回报很高的技能类别：
> **让你自己的命令行工具变得 agent 好用**。
> 这条同时改善人类和 agent 的体验。

## 目录

- [为什么值得做成技能](#为什么值得做成技能)
- [四条设计约定](#四条设计约定)
- [标志设计](#标志设计)
- [输出格式](#输出格式)
- [退出码](#退出码)
- [可组合性](#可组合性)
- [自查清单](#自查清单)

## 为什么值得做成技能

> ⭐ **agent 与 CLI 的交互模式和人类不同**：
> 人类看一眼就懂，agent 靠解析。
> 一个对人类友好的 CLI 对 agent 可能是灾难。

典型失败：

```
□ 交互式提示（agent 会挂死）
□ 进度条和彩色转义（污染解析）
□ 输出混在 stderr 里
□ 出错仍然 exit 0
□ 输出格式随 TTY 与否变化
```

呼应 《skill-scripting》`script-engineering.md` 的
「脚本必须非交互、JSON 输出、区分退出码、幂等」——
**这里是同一套原则在 CLI 设计上的应用**。

## 四条设计约定

```
1. ⭐ 所有输入都通过命令行参数传入——绝不交互提示
2. ⭐ 提供 --help，给出清晰的用法
3. ⭐ 尽可能输出结构化数据（JSON）
4. ⭐ 返回有意义的退出码和错误信息
```

外加一条对 agent 特别重要的：

```
5. ⭐ 默认安全行为——破坏性操作默认 dry-run
```

## 标志设计

**优先长标志，但保证短标志存在**：

```
✅ --output json   -o json
✅ --dry-run       -n
❌ -x（没有长名，agent 和人都要查文档）
```

**给每个参数一个明确的默认值**：

```
✅ 未指定分支时用 main
❌ 未指定时问用户
```

> ⭐ **不要给选项菜单——做决定，让用户覆盖。**
> 呼应 `skill-principles.md`（**`skill-crafting`**）同一条：
> "Don't offer menus of options—make the decision and let the user override."

**破坏性操作必须有 `--dry-run` 且默认开启**：

```bash
mytool cleanup --dry-run    # ⭐ 默认：只显示会删什么
mytool cleanup --force      # 显式确认才真删
```

## 输出格式

**核心规则**：输出格式**不能随环境变化**。

```
❌ TTY 时彩色 + 表格，非 TTY 时纯文本
✅ 恒定格式；颜色用 --color 显式开启
```

**给机器读的通道**：

```bash
mytool list --format json     # ⭐ 结构化输出
mytool list --format table    # 给人看
```

**JSON 输出的约定**：

```json
{
  "ok": true,
  "data": [ ... ],
  "warnings": [],
  "errors": []
}
```

> ⭐ **把 `ok`、`warnings`、`errors` 做成固定字段**——
> agent 不需要猜"这次到底算成功吗"。

呼应 `output-contract.md`（**`skill-crafting`**）的 Schema-First：
**边界校验要在技能边界做，失败要"响亮"**。

## 退出码

| 码 | 含义 | agent 该怎么做 |
|---|---|---|
| 0 | 成功 | 继续 |
| 1 | 通用失败 | 读 stderr，报告 |
| 2 | ⭐ 用法错误（参数不对） | 修参数重试 |
| 10 | ⭐ 校验失败 | 修输入重试 |
| 20 | ⭐ 资源未找到 | 不要重试 |
| 130 | 被中断（SIGINT） | 停止 |

> ⭐ **区分"要不要重试"比区分"成功失败"更有用**：
> 20（未找到）重试没意义，10（校验失败）改输入再试有意义。

呼应 《skill-scripting》`script-engineering.md`：
**退出码要区分类型，否则 SKILL.md 的错误处理章节没法精准回退**。

**错误信息要给"下一步"**：

```
❌ Error: failed
✅ Error: config file not found at .mytool.yaml
   To create one: mytool init
```

## 可组合性

**能做管道的一环**：

```bash
mytool list --format json | jq '.data[].id' | xargs -n1 mytool inspect
```

**支持从 stdin 读**：

```bash
cat items.txt | mytool process -
```

**幂等**：

```
⭐ 同一输入跑两次，结果和副作用都一致
   ——agent 超时重试时这条救命
```

呼应 `error-handling.md`（**`skill-crafting`**）：
**工具超时后 agent 重试，不能产生重复项**。

## 自查清单

```
□ 没有任何交互提示？
□ 所有输入都能通过参数传入？
□ 有 --help 且用法清晰？
□ 支持 --format json？
□ 输出格式不随 TTY 变化？
□ 破坏性操作默认 dry-run？
□ 退出码区分类型（尤其区分"可重试"与"不可重试"）？
□ 错误信息带"下一步该做什么"？
□ 能从 stdin 读、能管道出去？
□ 幂等吗？
□ 每个参数都有明确默认值？
□ 有 --version？
```

## 一个完整示例

```bash
#!/usr/bin/env bash
# mytool —— agent 兼容的命令行工具
set -euo pipefail

FORMAT="table"
DRY_RUN=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)   FORMAT="$2"; shift 2 ;;
    --dry-run)  DRY_RUN=1; shift ;;
    --force)    DRY_RUN=0; shift ;;
    --help)     usage; exit 0 ;;
    --version)  echo "mytool 1.2.0"; exit 0 ;;
    *)          echo "unknown flag: $1" >&2; usage >&2; exit 2 ;;
  esac
done

# ⭐ 破坏性操作默认 dry-run
if [[ "$DRY_RUN" -eq 1 ]]; then
  echo '{"ok":true,"data":[],"warnings":["dry-run: nothing was changed"],"errors":[]}'
  exit 0
fi
```

## 自查

- [ ] 你的工具能被 agent 无歧义地解析吗？
- [ ] 超时重试会产生重复副作用吗？
- [ ] agent 能区分"改输入重试"和"别重试"吗？
- [ ] 输出格式在任何环境下都一致吗？
