# 脚本工程纪律

> `scripts/` 不是放"代码"的地方，是放**确定性操作**的地方。
> 好的脚本像乐高——独立、可组合、接口清晰、行为可预测。

## 目录

- [什么该进脚本](#什么该进脚本)
- [自包含（PEP 723）](#自包含pep-723)
- [Agent 友好设计](#agent-友好设计)
- [错误处理三层](#错误处理三层)
- [结构化输出与退出码](#结构化输出与退出码)
- [幂等性](#幂等性)
- [工程纪律五条](#工程纪律五条)

---

## 什么该进脚本

**核心分界**：

> **如果你希望这个任务每次执行结果都完全一致 → 脚本**
> **如果希望每次都有新的创意或见解 → 让 AI 自己思考**

| ✅ 用脚本 | ❌ 不用脚本 |
|---|---|
| 格式化与转换（Markdown→特定 HTML、统一 JSON/YAML 结构） | 代码审查建议（需具体分析上下文） |
| 数据验证与清理（完整性、类型一致、去重、缺失值） | 架构设计决策（需权衡多因素） |
| 重复性构建（跑测试套件生成报告、打包、生成 API 文档） | 内容创作（需风格与创意） |
| 复杂但固定的工作流（部署、迁移、定时同步） | 调试特定错误（需理解具体代码） |
| 环境配置与检查（依赖版本、环境变量、权限） | 一次性 / 极少重复的任务 |

> **一个判断信号**：观察 agent 的执行轨迹——
> 如果发现它**每次运行都在独立地重新发明同一段逻辑**，
> 那就是该固化的信号。

---

## 自包含（PEP 723）

> **官方推荐：让脚本声明自身依赖，减少环境配置复杂性。**

```python
# /// script
# dependencies = ["beautifulsoup4"]
# ///
from bs4 import BeautifulSoup
```
运行：`uv run scripts/extract.py`

| 语言 | 方案 |
|---|---|
| Python | **PEP 723** 内联依赖 + `uv run` |
| JS/TS | Deno（`npm:cheerio@1.0.0`）或 Bun |
| Ruby | `bundler/inline` |

简单的一次性命令，直接用 `uvx` / `pipx` / `npx` 即可，不必建 `scripts/`。

---

## Agent 友好设计

### ① 绝不交互

> 非交互式 shell 中运行，**无法响应 TTY 提示**——会无限期挂起。

```bash
❌ $ python scripts/deploy.py
   Target environment: _        # 挂死

✅ $ python scripts/deploy.py
   错误：需要 --env 参数。选项：development, staging, production。
   用法：python scripts/deploy.py --env staging --tag v1.2.3
```

### ② `--help` 是 agent 学接口的主要方式

```
用法: scripts/process.py [选项] 输入文件
处理输入数据并生成摘要报告。

选项:
  --format 格式   输出格式: json, csv, table (默认: json)
  --output 文件   写入文件而不是 stdout
  --verbose       进度打印到 stderr

示例:
  scripts/process.py data.csv
  scripts/process.py --format csv --output report.csv data.csv
```

### ③ 错误消息直接影响下一次尝试

> 好的错误要说明：**哪里错了 + 下一步该做什么**。

```python
except KeyError as e:
    print(f"ERROR: 缺少环境变量 {e}", file=sys.stderr)
    print("请检查环境变量或配置文件", file=sys.stderr)
    sys.exit(1)
```

---

## 错误处理三层

| 层次 | 发生位置 | 处理 |
|---|---|---|
| **输入验证错误** | 执行前 | 检查输入，不合法直接拒绝并说明原因 |
| **运行时错误** | 脚本执行中 | 捕获异常，输出结构化错误信息 |
| **结果异常** | 执行完成后 | 验证输出是否符合预期，不符则触发补救 |

**显式处理，别把错误抛给 Claude**：

```python
# ✅ 好
def process(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Creating {path}")
        ...
    except PermissionError:
        print(f"ERROR: Cannot access {path} - check permissions")
        return None

# ❌ 坏：错误意外向上抛
def process(path):
    with open(path) as f:
        return f.read()
```

**SKILL.md 里要配套写错误处理章节**，告诉 agent 遇到问题怎么办：

```markdown
## 错误处理
### 输入问题
- 文件不存在：告知路径有误，请重新上传
- 格式不支持：列出支持格式，请转换后重试
### 执行问题
- 脚本失败：**展示完整错误信息，不要隐藏**
- 依赖未安装：先尝试自动安装，失败则请用户手动装
- 超时：超过 60 秒输出当前进度并询问是否继续
### 结果问题
- 输出为空：重新检查逻辑并说明可能原因
```

> 一条关键约定：**脚本返回非零退出码时，把错误信息交给用户确认，不要猜测原因**。

---

## 结构化输出与退出码

**输出要可解析**：

```python
# ✅ 好：结构化
import json
print(json.dumps({"status": "success",
                  "files_processed": 5, "errors": []}))

# ❌ 坏：非结构化
print("Done! Processed 5 files with no errors.")
```

> **能输出 JSON 就不要输出一堆带颜色的日志**——
> agent 从日志里翻结果，错误率直线上升。
> 分离**数据（stdout）**与**诊断信息（stderr）**。

**退出码要区分类型**，别一律 `exit(1)`：

```python
EXIT_OK                  = 0
EXIT_VALIDATION_FAILED   = 10
EXIT_TEMPLATE_NOT_FOUND  = 20
EXIT_DATA_TOO_LARGE      = 30
EXIT_UNKNOWN             = 99
```

> 有了这个，SKILL.md 的 Error Handling 章节才能**按错误码精准回退**。

---

## 幂等性

> **脚本应该可以安全重复运行。**

```python
def ensure_directory(path):
    """目录不存在才创建（幂等）"""
    os.makedirs(path, exist_ok=True)

def write_if_changed(path, content):
    """内容相同就不写（幂等）"""
    if os.path.exists(path):
        with open(path) as f:
            if f.read() == content:
                return False   # 无需改动
    with open(path, "w") as f:
        f.write(content)
    return True
```

> 这直接关系到 **`skill-evaluating` 的 `metrics.md`** 第 5 层的**幂等性**检查——
> 工具超时后 agent 重试，不能产生重复项。

---

## 工程纪律五条

```
1. 接口要稳定
   脚本的 CLI 接口像公共 API 一样稳定。
   SKILL.md 引用了 --template，就不要随意改成 --tpl。

2. 常量要写理由
   TIMEOUT = 30      # HTTP 请求通常 30s 内完成
   MAX_RETRIES = 3   # 多数失败在第二次重试前解决
   ❌ TIMEOUT = 47   # 为什么 47？

3. 依赖要显式列出
   ## Requirements
   pip install pdfplumber python-docx
   或 pip install -r scripts/requirements.txt

4. 路径用相对路径，基准写清是技能包根目录
   resources/templates/weekly_report_template.md
   ❌ 写绝对路径——换机器换项目直接废

5. 不硬编码任何凭据
   scripts/ 会被加载、被审计、被分享。
   任何密钥/Token 出现在脚本里都是事故。走环境变量或 vault。
```

**目录组织**：

```
scripts/
├── analyze.py      # 主入口
├── validate.py     # 校验工具
└── helpers/
    ├── formatting.py
    └── parsing.py
```

**SKILL.md 里要写明用法是"执行"还是"当参考读"**：

```markdown
执行：`scripts/analyze.py` 从 PDF 抽取表单字段。
参考：抽取算法见 `scripts/analyze.py`（不要直接运行）。
```

> 官方明确：**代码可以同时是可执行工具和文档，
> 但必须说清 Claude 该运行它还是该读它。**

---

## 自查

```
□ 脚本是否完全非交互（不读 TTY）？
□ 是否有 --help？
□ 错误消息是否说明了"下一步该做什么"？
□ 是否用 JSON 输出（数据与诊断分离）？
□ 退出码是否区分了错误类型？
□ 是否幂等（可安全重复运行）？
□ 常量是否写了理由？
□ 依赖是否显式声明（PEP 723 / requirements.txt）？
□ 是否用了相对路径？
□ 是否零硬编码凭据？
□ SKILL.md 是否配套了错误处理章节？
□ 是否写清了"执行"还是"当参考读"？
```
