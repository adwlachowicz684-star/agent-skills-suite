#!/usr/bin/env python3
"""生成触发测试集骨架（evals.json）。

用法: python gen_eval_set.py "技能用途一句话" [--out evals.json] [--n 10]
退出码: 0=成功  1=失败

生成的骨架里 should_trigger=false 的条目是**占位**，
必须替换成你自己领域的"近失样本"——共享关键词但需求不同。
这是最关键的负例，通用模板猜不出来。
"""
import argparse
import json
import sys

POS_TMPL = [
    ("直接点名", "帮我{task}"),
    ("口语化", "你帮我{task}一下呗"),
    ("带背景", "我老板让我{task}，明天要用"),
    ("含文件路径", "帮我{task} ~/Downloads/report_final_v2.xlsx"),
    ("隐含意图", "这个文件得整理一下才能交"),
    ("缩写混用", "{task}，thx"),
    ("错别字", "帮我{taskt}下"),
    ("长消息", "是这样的，我们这边有个文件，需要{task}，"
               "具体要求是格式要统一、结论要前置，你看看怎么处理"),
    ("多步工作流的一部分", "先{task}，然后再按结果写个总结"),
    ("只说目标不说手段", "我想知道这批数据到底什么情况"),
]

NEG_HINT = [
    "TODO 近失样本 1：共享关键词，但实际需要的是【别的技能/别的能力】"
    "——例（CSV 分析技能）：把这个 CSV 导入 Postgres（需要 ETL，不是分析）",
    "TODO 近失样本 2：同一个词，但是「查询方法」而非「执行任务」"
    "——例：{task} 一般怎么做？（问方法，不是要执行）",
    "TODO 近失样本 3：要的是别的产物形态"
    "——例：帮我写个{task}的脚本（要代码，不是要结果）",
    "TODO 近失样本 4：属于相邻领域"
    "——例（提交信息技能）：帮我 review 这段代码的 commit（是评审）",
    "TODO 近失样本 5：范围更大，本技能只是其中一步",
    "TODO 近失样本 6：范围更小，本技能是大流程里的多余步骤",
    "TODO 近失样本 7：涉及本技能明确排除的领域（Do NOT 里写过的）",
    "TODO 近失样本 8：同义但不同场景——例：把{task}的结果发给同事（是分发）",
    "TODO 近失样本 9：要的是解释/概念，不是执行",
    "TODO 近失样本 10：需要人工判断，本技能不该自动接手",
]


def build(task, n):
    evals, i = [], 0
    for label, tpl in POS_TMPL[:n]:
        i += 1
        evals.append({
            "id": i,
            "note": f"正例·{label}",
            "prompt": tpl.format(task=task, taskt=task),
            "should_trigger": True,
            "expected_output": "TODO 描述期望输出的关键特征（用于 rubric 评判）",
        })
    for k in range(n):
        i += 1
        evals.append({
            "id": i,
            "note": "负例·近失样本（必须替换为你的领域）",
            "prompt": NEG_HINT[k % len(NEG_HINT)].replace("{task}", task),
            "should_trigger": False,
            "expected_output": None,
        })
    return {
        "skill_name": "TODO-skill-name",
        "_how_to_use": [
            "每条查询跑 3 次（模型行为非确定性）",
            "正例触发率 >0.5（3 次中至少 2 次）",
            "负例触发率 <0.5",
            "用 60/40 分割：训练集上优化 description，验证集上确认泛化",
        ],
        "evals": evals,
    }


def main():
    ap = argparse.ArgumentParser(description="生成触发测试集骨架")
    ap.add_argument("task", help="技能用途的一句话，如'分析 CSV 数据'")
    ap.add_argument("--out", default="evals.json")
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    if not a.task.strip():
        print("错误：需要提供技能用途描述")
        return 1

    data = build(a.task.strip(), a.n)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    pos = sum(1 for e in data["evals"] if e["should_trigger"])
    print(f"已生成 {a.out}：{len(data['evals'])} 条（正例 {pos} · 负例 {len(data['evals'])-pos}）")
    print("\n下一步：")
    print("  1. 把 skill_name 改成真实技能名")
    print("  2. **必须替换所有负例**——通用占位猜不出你领域的近失样本")
    print("  3. 每条跑 3 次，正例触发率 >0.5，负例 <0.5")
    return 0


if __name__ == "__main__":
    sys.exit(main())
