# ML / MLOps 类技能

> ⭐ **这类技能解决的是"编码 agent 反复犯同样的 ML 错误"**：
> 把预处理泄漏进交叉验证 · 用 accuracy 评估不平衡数据 ·
> 忘记 `model.eval()` · 只用稠密检索做 RAG。

## 目录

- [15 个技能的分组](#15-个技能的分组)
- [三条设计原则](#三条设计原则)
- [泄漏安全：最重要的一条](#泄漏安全最重要的一条)
- [诊断决策树](#诊断决策树)

---

## 15 个技能的分组

**数据准备与探索**

| 技能 | 何时用 |
|---|---|
| `exploratory-data-analysis` | 新数据集起步——profiling、分布、相关性、⭐ 泄漏与可视化 |
| `data-cleaning` | 缺失值、重复、类型、离群点——⭐ **仅用训练集做填充** |
| `feature-engineering` | 编码、缩放、日期/文本/聚合特征、⭐ 泄漏安全的目标编码 |
| `pandas-patterns` | 惯用、向量化、省内存的 pandas（无 SettingWithCopyWarning） |
| `imbalanced-data` | 目标稀有（欺诈/流失/疾病）——指标、SMOTE、类别权重、阈值 |

**建模**

| 技能 | 何时用 |
|---|---|
| ⭐ `sklearn-pipelines` | 构建**不把预处理泄漏进 CV** 的 sklearn 模型 |
| `pytorch-training-loop` | 写/审 PyTorch 循环——eval 模式、AMP、检查点、设备 |
| `model-evaluation` | 选指标、验证、校准、混淆矩阵分析 |
| `hyperparameter-tuning` | 随机 vs Optuna、⭐ 泄漏安全的 CV、早停、预算 |

**LLM 与 GenAI**

| 技能 | 何时用 |
|---|---|
| `llm-finetuning` | 全参 vs LoRA/QLoRA、数据格式、transformers/PEFT/TRL |
| ⭐ `rag-pipeline` | 分块、嵌入、⭐ 混合 + 重排检索、评估 |

**MLOps 与可靠性**

| 技能 | 何时用 |
|---|---|
| `experiment-tracking` | 实验需要比较/复现——MLflow/W&B、该记什么、registry |
| ⭐ `reproducible-ml` | 结果必须可复现——种子、环境锁定、数据版本、CUDA 确定性 |
| ⭐ `ml-debugging` | 模型不学习、loss 是 NaN、⭐ **指标好得不像真的**——诊断决策树 |
| `model-serving` | 部署到 API 后面——FastAPI、⭐ 安全加载制品、批处理、ONNX、监控 |

---

## 三条设计原则

> ⭐ **这三条来自一个成熟的 ML 技能包，值得原样抄**：

```
① ⭐ 默认泄漏安全
   每个数据类技能都只在训练集上拟合变换

② ⭐ 具体胜过抽象
   给真实代码模式，不给模糊建议

③ ⭐ 包含陷阱
   ⭐ 每个技能都以"agent 实际会犯的错误"结尾

④ 可组合
   技能之间互相交接：
   EDA → 清洗 → 特征 → pipeline → 评估 → 服务
```

> ⭐ 第 ③ 条呼应 `skill-authoring` 的 `skill-types.md`：**Gotchas 是信号最高的部分**。
> 第 ④ 条呼应 `skill-orchestration` 的 `composition.md`：技能通过路由协作。

---

## 泄漏安全：最重要的一条

> ⭐ **这是 ML 技能与通用编码技能最大的区别**：

```
❌ 常见错误
   先在整个数据集上 fit 标准化/填充器/目标编码，
   再做交叉验证
   → 验证集信息泄漏进训练，分数虚高

✅ 正确
   ⭐ 每个数据类技能都只在训练集上拟合变换
   ⭐ 用 pipeline 把变换包进 CV 的每一折
```

> ⭐ 呼应 `legacy-modernization.md` 的特征化测试思路：
> **"指标好得不像真的"本身就是一个需要诊断的症状**——
> 所以 `ml-debugging` 把"metrics look too good"列为触发条件之一。

---

## 诊断决策树

```
模型不学习 / loss 是 NaN / 指标好得不像真的
  ↓
ml-debugging 的诊断决策树
```

**可复现性的四个要素**（`reproducible-ml`）：

```
□ 种子
□ ⭐ 环境锁定
□ ⭐ 数据版本
□ CUDA 确定性
```

**实验追踪该记什么**（`experiment-tracking`）——不是"都记"，而是有选择。

**RAG 的关键**（`rag-pipeline`）：

```
□ 分块
□ 嵌入
□ ⭐ 混合检索 + 重排（⭐ 不能只用稠密检索）
□ 评估
```

> 呼应 `skill-selection` 的 `skill-vs-rag.md`：技能教的是**怎么用好检索**，
> 而不是替代检索本身。

---

## 自查

```
□ 是否默认泄漏安全（只在训练集上拟合变换）？
□ ⭐ 是否把"指标好得不像真的"列为需诊断的症状？
□ 是否有诊断决策树（而非笼统建议）？
□ 每个技能是否以"agent 实际会犯的错误"结尾？
□ ⭐ 是否给了真实代码模式（而非抽象建议）？
□ 技能之间是否可交接（EDA→清洗→特征→pipeline→评估→服务）？
□ RAG 是否含混合检索 + 重排（而非只用稠密）？
□ 是否含 PyTorch 的 eval 模式、AMP、检查点？
□ ⭐ 可复现性是否含数据版本与环境锁定（不只是种子）？
□ 部署是否含安全加载制品（而非 pickle 一把梭）？
□ 不平衡数据是否避免用 accuracy？
□ 微调是否区分了全参与 LoRA/QLoRA？
□ 超参调优是否强调泄漏安全的 CV？
□ 实验追踪是否说明了"该记什么"？
```
