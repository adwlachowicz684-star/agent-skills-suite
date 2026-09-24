# 脚本 CLI 契约：模型怎么读懂你的脚本

> 相关：《skill-crafting》的 `deterministic-scripts.md` ·
> `scripts-guidance.md` · 《skill-structuring》的 `directory-decision-matrix.md`
> 前置：`deterministic-scripts.md` 讲"脚本要确定性且可复现"，
> 这份讲⭐ 脚本与调用方（模型）之间的接口约定。

---

## 目录

- [1. ⭐ 四个硬性要求](#1--四个硬性要求)
- [2. ⭐⭐ 退出码要分级](#2--退出码要分级)
- [3. ⭐ 输出要结构化](#3--输出要结构化)
- [4. 常量必须有理由](#4-常量必须有理由)
- [5. ⭐ 幂等与凭据](#5--幂等与凭据)

---

## 1. ⭐ 四个硬性要求

> ⭐ **模型调用脚本，本质是把一段指令交给子进程，
> 然后读标准输出、判断退出码。**

**① 标准输入输出要干净**

```
⭐ 结果只往 stdout 写
⭐ 调试信息走 stderr
```

> ⭐⭐ 否则模型会把你打的调试日志当成结果来解析。
> 这是"脚本明明成功了但输出很怪"的头号原因。

**② 退出码要正确**

```
0 = 成功；非 0 = 失败
```

> ⭐⭐ 模型判断脚本是否成功，很多时候**不是看你输出的文字，而是看退出码**。
> ⭐ 如果脚本里某个环节失败了还继续往下走，最后撑死打一行 "success"——**那就是在骗模型**。

**③ 参数要尽量简单**

```
⭐ 能通过命令行参数传入的，就不要让模型去修改脚本里的常量
· 参数少一点，默认值多一点
· 输入输出路径优先用相对路径，并在 SKILL.md 里写清工作目录
```

**④ ⭐ 不要设计交互式逻辑**

```
⭐ 不要在命令行里要求手动录密码、交互式确认
——那会让模型彻底卡在交互等待上
```

---

## 2. ⭐⭐ 退出码要分级

> ⭐ **不要让脚本只用 `exit(1)` 草草报错。**

```python
EXIT_OK                 = 0
EXIT_VALIDATION_FAILED  = 10
EXIT_TEMPLATE_NOT_FOUND = 20
EXIT_DATA_TOO_LARGE     = 30
EXIT_UNKNOWN            = 99
```

**为什么值得分**：

```
⭐ SKILL.md 的 Error Handling 章节可以基于错误码⭐ 精准回退
```

> 一个具体价值的例子：
>
> ```
> 如果脚本因网络超时挂了 → 退出码非 0
> → ⭐ 模型知道是"脚本执行有问题"，去查 stderr
> → ⭐ 而不是把"接口不通"误判成"测试未通过"
> ```
>
> ⭐ **这个小细节非常影响模型后续的决策链路**——
> 一个笼统的 1 会让它去改测试，而真正要修的是网络。

**另一个常见约定**（更细的分级）：

```
EXIT_SUCCESS         = 0
EXIT_INVALID_INPUT   = 1
EXIT_FILE_NOT_FOUND  = 2
EXIT_PERMISSION_ERROR = 3
```

> 两种都可以，关键是**同一技能内保持一致，且错误码要在 SKILL.md 里写明**。

---

## 3. ⭐ 输出要结构化

```
⭐ 一切能被 JSON 表达的结果，就输出 JSON
⭐ 不要输出一堆中英文夹杂的自然语言
```

**推荐结构**（含 warnings 与 stats 是加分项）：

```json
{
  "status": "success",
  "output_path": "outputs/oct-monthly.xlsx",
  "warnings": ["Column 'revenue_q4' contained 3 null values"],
  "stats": {"rows": 1284, "sheets": 4}
}
```

> ⭐ 这让模型更容易解析，也让**自动化测试更稳定**——
> 断言可以打在字段上，而不是去匹配一句自然语言。

**另一个好用的模式**：把排障提示写进 reference 文件，
让模型遇到异常状态码时去查：

```
troubleshooting.md 里写：
   "502 大概率是网关问题"
   "401 先检查 Token 是否过期"
```

> 模型查到后会把原因写进最终报告——比让它自己猜强得多。

---

## 4. 常量必须有理由

```python
# ✅ 好：每个魔数都有理由
TIMEOUT     = 30   # HTTP 请求通常 30s 内完成
MAX_RETRIES = 3    # 多数失败在第二次重试时解决
BATCH_SIZE  = 100  # 内存与 API 调用次数之间的平衡

# ❌ 坏：魔数
TIMEOUT = 47       # 为什么是 47？
```

> ⭐ 这与 `write-reasons-not-rules.md` 是同一条原则在代码里的体现：
> **写原因，不写断言。** 有理由的常量在未来可被安全地修改。

**错误处理也要显式**：

```python
# ✅ 显式处理，给出可行动的错误信息
except PermissionError:
    print(f"ERROR: Cannot access {path} - check permissions")
    return None

# ❌ 让异常直接抛出，模型只看到一段 traceback
```

---

## 5. ⭐ 幂等与凭据

**幂等**：脚本应可安全重复运行

```python
os.makedirs(path, exist_ok=True)          # 目录
def write_if_changed(path, content): ...  # 内容相同则不写
```

**凭据**：

```
⭐⭐ scripts/ 会被加载、被审计、被分享
⭐ ⭐ 任何密钥/Token 出现在脚本里都是事故
需要凭据走环境变量或 vault，绝不写进文件
```

**依赖声明**：

```markdown
## Requirements
pip install pdfplumber python-docx
# 或
pip install -r scripts/requirements.txt
```

> ⭐ 同时建议**优先选纯 Python / 纯 JS 实现的库，避开带原生编译步骤的依赖**
> ——这样谁拿去部署踩坑概率都小得多。

---

## 速查

```
□ ⭐ 结果只写 stdout，调试走 stderr（否则被当结果解析）
□ ⭐⭐ 退出码要分级，SKILL.md 里写明各码含义
□ ⭐⭐ 失败了别打 "success"——那是在骗模型
□ ⭐ 参数少、默认值多、路径用相对 + 正文写明工作目录
□ ⭐ 绝不设计交互式输入（模型会卡死在等待）
□ ⭐ 输出优先 JSON，含 status / warnings / stats
□ 常量写理由，异常显式处理并给可行动信息
□ ⭐ 幂等（可重复运行）
□ ⭐⭐ 脚本里绝不出现凭据
□ 依赖显式声明，优先避开原生编译依赖
```

**一句话**：

> ⭐⭐ **模型判断脚本成败靠的是退出码，不是你打了什么字——
> 失败却打印 "success"，等于在骗它。**
