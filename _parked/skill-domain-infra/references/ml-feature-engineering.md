# ML 特征工程与泄漏安全

> 特征工程的技能形态：**选型表 + 一条不可协商的铁律**。
> 后者才是技能真正的价值。

## 目录

- [分类变量编码](#分类变量编码)
- [数值缩放选型表](#数值缩放选型表)
- [日期时间特征](#日期时间特征)
- [文本特征](#文本特征)
- [⭐ 泄漏安全：唯一的核心规则](#-泄漏安全唯一的核心规则)
- [为什么泄漏是 ML 技能的第一主题](#为什么泄漏是-ml-技能的第一主题)

## 分类变量编码

```
OneHotEncoder  → 无序类别
OrdinalEncoder → ⭐ 有序类别（要显式给顺序）
```

```python
OrdinalEncoder(categories=[['low', 'medium', 'high']])
```

> ⭐ 注意 `categories` 参数——不传顺序的 OrdinalEncoder
> 会把有序关系编码成随机的，这是常见错误。

## 数值缩放选型表

| 方法 | 何时用 | 对算法的影响 |
|---|---|---|
| **StandardScaler** | 特征近似正态、离群值少 | ⭐ SVM、神经网络、PCA **必需** |
| **RobustScaler** | 有离群值，想要中位数/IQR 中心化 | 同 Standard，更稳健 |
| **MinMaxScaler** | 需要有界区间 [0,1] 或 [-1,1] | 神经网络、图像数据 |
| **PowerTransformer** | 偏态分布，想要正态性 | ⭐ 改善线性模型表现 |
| **QuantileTransformer** | 重尾，想要均匀/正态 | ⭐ 树模型不受影响，线性模型改善 |

> ⭐ 最后一行是关键提醒：
> **树模型对缩放不敏感**——给树模型做 PowerTransformer 是白费功夫。

## 日期时间特征

**组件提取**：

```python
df['year']      = df['timestamp'].dt.year
df['month']     = df['timestamp'].dt.month
df['dayofweek'] = df['timestamp'].dt.dayofweek
df['hour']      = df['timestamp'].dt.hour
```

**⭐ 周期性编码**（保留循环性质）：

```python
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
```

> ⭐ **为什么要 sin/cos**：
> 12 月和 1 月相邻，但数值是 12 和 1——
> 直接用数值会让模型认为它们相距很远。
>
> 这是一个典型的 **Gotchas**：
> 违反了"数字越大表示越多"的合理假设。

**时长特征**：

```python
df['days_since_start'] = (df['timestamp'] - df['timestamp'].min()).dt.days
```

## 文本特征

```python
# 经典 NLP
vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))

# 语义相似度
model = SentenceTransformer('all-MiniLM-L6-v2')

# 基础统计（常被忽略但很有效）
df['text_length'] = df['text'].str.len()
df['word_count']  = df['text'].str.split().str.len()
```

> ⭐ **基础统计特征常被跳过**，
> 但它们便宜、可解释，且对很多任务是强信号。

## ⭐ 泄漏安全：唯一的核心规则

> **始终只在训练数据上 fit，对所有数据 transform。**

```python
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numerical_features),
    ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
])
pipeline = Pipeline([('prep', preprocessor), ('model', RandomForestClassifier())])

# ✅ 正确：只在训练集上 fit
pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)   # ⭐ 不需要手动 transform
```

**最常见的泄漏方式**：

```
❌ 先在整个数据集上 fit_transform，再切分训练/测试
   → 测试集的统计信息已经进入模型
   → ⭐ 离线指标虚高，上线即崩
```

**CV 安全**：交叉验证也要保证
**每一折的 fit 只用该折的训练部分**——
用 Pipeline 包起来就是为了这个。

## 为什么泄漏是 ML 技能的第一主题

呼应 `ml-mlops-skills.md` 已有的三条：

```
□ ⭐ 默认泄漏安全——只在训练集上拟合变换
□ ⭐ "指标好得不像真的"是需诊断的症状，不是好消息
□ 模型可以组织数字，不能生成数字
```

**泄漏的三个特殊性**：

```
1. ⭐ 静默——不报错，指标还很好看
2. ⭐ 延迟暴露——到生产才暴露，且损失已经发生
3. ⭐ 反直觉——越"漂亮"的结果越可疑
```

> 这正好命中 `grounding-verification.md`（**`skill-crafting`**）
> 的核心论点：**表面合规是最危险的失败模式**。
> 一个泄漏的模型在离线评估上**完全合规**。

**所以 ML 技能必须显式写**：

```
□ fit/transform 的边界（硬性）
□ ⭐ "指标异常好" → 触发诊断，而不是庆祝
□ ⭐ 要求报告特征重要性与业务常识是否一致
```

第三条很有用：**如果模型说"用户 ID"是最重要的特征，
几乎肯定是泄漏或过拟合**——业务常识能抓到统计抓不到的问题。

## 自查

- [ ] 有序类别显式传了 `categories` 顺序吗？
- [ ] 缩放方法匹配分布与算法了吗？（树模型不做 PowerTransform）
- [ ] 周期性时间特征用 sin/cos 了吗？
- [ ] 只在训练集上 fit 了吗？
- [ ] 用了 Pipeline 保证 CV 安全吗？
- [ ] 技能里写了"指标异常好要诊断"吗？
- [ ] 要求校验特征重要性与业务常识一致吗？
