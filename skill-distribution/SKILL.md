---
name: skill-distribution
description: Agent Skills 的打包发布、版本管理、团队共享与组织推广。用于把技能打包分发、定语义化版本与 git tag 回滚、写迁移指引、跨机器 / 离线环境部署、在团队里建立共享技能库、推动同事真正用起来，或处理许可与知识产权归属。
  Do NOT use for 写技能内容本身（用 skill-authoring）、团队采用与推广（用 skill-adoption）、瘦身拆分（用 skill-refining）、质量打分（用 skill-evaluating），也不用于单纯的技术选型咨询。
---

# 发布、分发与推广

## 边界

- 用于：**打包发布** · **版本与回滚** · **依赖与供应链** · **离线部署** · **许可归属** · **上架运维**
- 不用于：写技能内容 · 瘦身拆分 · 质量打分 · 单纯选型咨询
- ⭐ **团队采用、推广、PR 流程与采用度量 → 《skill-adoption》**

## 核心原则

> ⭐ **多数技能计划不是死在代码里，是死在组织里。**

```
□ 一次微妙的错误，会让人退回手工⭐ 并告诉两个同事
□ ⭐ 如果"技能输出不对"的唯一回应是放弃它、退回临时提示词
   → 你的库会腐烂
□ ⭐ 如果有一条快速、无责怪的提交修复路径
   → 每次失灵都变成小改进，信任复利式增长
```

> ⭐ **所有安装命令都必须带 `#vX.Y.Z` 后缀**——
> 真实事故：一次不带版本后缀的覆盖，导致下游所有依赖它的技能全部中断。

## 路由表（按需深读）
| `skill-distribution/references/sdk-programmatic-skills.md` | ⭐⭐★★★ SDK 里默认不加载；★slash_commands 可编程确认；query() 天然隔离 |
| `skill-distribution/references/localization-zh-adaptation.md` | ⭐⭐★★★ 本地化≠翻译；★上游同步分层；评测集也要本地化 |
| `skill-distribution/references/plugin-vs-skill-packaging.md` | ⭐⭐⭐★ 技能=内容 插件=容器 市场=渠道；★skills 字段指向父目录 |
| `skill-distribution/references/dependency-resolution-conflicts.md` | ⭐⭐ 结构化声明 required/optional + conflicts；★可选依赖缺失=降级 |
| `skill-distribution/references/skill-discovery-at-scale.md` | ⭐⭐ 15万技能下的发现机制；⭐⭐⭐ 给agent可信入口三要素 |
| `skill-distribution/references/gray-release-rollback.md` | ⭐⭐⭐ 版本级指标拆分：10%全挂=大盘掉1-2点；跳档代价 |
| `skill-distribution/references/dependency-lockfile.md` | ⭐ 依赖与 lockfile：36.6% 隐藏依赖 + 五步加固 |
| `skill-distribution/references/cross-agent-portability.md` | ⭐ 跨平台：破坏可移植的三件事 + 中性目录 |
| `skill-distribution/references/skill-as-business-rule.md` | ⭐⭐⭐⭐⭐ 技能是业务规则的数字孪生；⭐⭐⭐⭐ 改 description 最危险（70% 事故）|
| `skill-distribution/references/enterprise-marketplace-ops.md` | ⭐ 企业市场运维三阶段与遥测盲区 |
| `skill-distribution/references/distribution-three-ways.md` | ⭐ Git / 插件市场 / 企业托管，优先级与 MDM |
| `skill-distribution/references/supply-chain-trust.md` | ⭐ 供应链信任：像对待代码依赖一样对待技能 |

**打包与发布**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **技能包：可寻址产物、锁文件与 pin 纪律** | `references/skill-packs.md` |
| ⭐ **优先级冲突：企业>个人>项目>插件，同名必被盖** | `references/priority-conflict.md` |
| ⭐ **使用分析：把技能库接进工程目录、清库** | `references/usage-analytics.md` |
| ⭐ **两级审核：命名空间 + 全局、四种状态** | `references/review-governance.md` |
| **命名规范：硬约束、动词 vs 名词、改名的代价** | `references/naming-convention.md` |
| ⭐ **回滚演练：验收标准是 eval 回到基线** | `references/rollback-drill.md` |
| ⭐ **变更日志：记 why 与影响，不是 git log** | `references/changelog-practice.md` |
| ⭐ **打包布局、provenance、git tag** | `references/packaging.md` |
| ⭐ **团队采用与推广（冷启动、PR 流程、度量）** | **`skill-adoption`** |
| **语义化版本 / 回滚 / 迁移指引** | `references/release-versioning.md` |
| **版本兼容与废弃四阶段** | `references/versioning-compat.md` |
| **许可与知识产权归属** | `references/licensing-ip.md` |

**环境与运维**：

| 你要做的事 | 读 |
|---|---|
| ⭐ **离线与私有化部署** | `references/air-gapped.md` |
| **技能库运维与健康诊断** | `references/library-ops.md` |
| ⭐ **上架列表页与安装后断言** | `references/marketplace-listing.md` |

## Critical Rules

**版本**：

- 每个正式版本对应一个 git tag——**回滚就是切回上一个 tag**
- ⭐ registry 保留最近几个版本，**不要只保留最新一条**
- ⭐ 有依赖的技能**回滚要成组**——避免 A 新 B 旧的不一致状态
- 破坏性变更**单独通知**，不混在普通修复里；优先保留旧参数标为废弃
- ⭐ 用内容寻址（tree SHA）而非只看版本号

**打包**：

- ⭐ 仓库必须**扁平**，分类用 metadata 字段而非子目录
- ⚠️ 更浅层的 SKILL.md **会遮蔽其下所有技能**
- 测试夹具 `evals/files/SKILL.md` **会多发布一个坏技能**——按本质命名并在安装后断言数量

**离线**：

- ⭐ `cloud_fallback: false` 是最关键的一行——否则会尝试访问云端 API 并触发安全告警
- 每个外部依赖**必须在传输时捆绑**，运行时不 `npm install`

## 常见借口

| Agent 说 | 回应 |
|---|---|
| "先发布，版本以后再补" | 没有 tag 就没有回滚。先打 tag 再发布。 |
| "回滚就是删掉重装" | 回滚要成组处理依赖，且要保留历史版本记录。 |
| "团队里发个链接就行" | 没有 PR 评审和修复路径的技能库会腐烂。 |
| "大家装上自然会用" | 推广卡在第一次体验。入门任务必须精选。 |
| "许可证随便写个 MIT" | 代码与内容许可逻辑不同；仓库 MIT 不等于技能 MIT。 |

## 脚本

```bash
python scripts/validate_skill.py ./my-skill      # 发布前校验
python scripts/estimate_tokens.py ./my-skill     # 记录基线
```
