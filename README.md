## Phase 4

### Phase 4 Goal（建议版本）

> Phase 4 aims to integrate LLM into the core semantic pipeline, enabling:
> - LLM-driven intent analysis
> - Structured requirement decomposition
> - Deterministic, reviewable execution planning
> - Without yet executing retrieval or final answer generation.

---

### warning 的判定语义

| Warning                   | 触发语义                   |
| ------------------------- | ---------------------- |
| MULTIPLE_INTENTS          | 一个输入中存在两个及以上可独立执行的核心目标 |
| CORE_INTENT_WEAK          | 无法用一句动词+对象准确概括核心意图     |
| AMBIGUOUS_SCOPE           | 范围边界（全量 / 部分 / 某模块）不明确 |
| UNCLEAR_TARGET            | 目标系统 / 目标对象不清晰         |
| MISSING_KEY_ENTITY        | 执行意图所需的关键实体缺失          |
| UNKNOWN_ENTITY            | 出现无法识别或无法归类的实体         |
| OPERATION_UNCLEAR         | 行为动词模糊（如“处理一下”“优化下”）   |
| CONSTRAINT_MISSING        | 明显需要约束但用户未给出           |
| NON_FUNCTIONAL_UNCLEAR    | 明显涉及性能/安全/稳定性但未明确      |
| DOMAIN_UNCERTAIN          | 无法确定业务/技术领域            |
| STAGE_UNCERTAIN           | 需求所处阶段（设计/开发/排错等）不清    |
| IMPLICIT_ASSUMPTION_HEAVY | 依赖多个未明说的前提假设           |


## README.md（Phase 3 更新内容）

### Phase 3：Intent Reasoning & Prompt Planning ✅

Phase 3 的目标是让 CodeScope 从「基于模板生成指令」升级为
**「具备意图理解、任务拆解与指令规划能力的工程化系统」**。

本阶段不接入 LLM，专注于**结构正确性、可解释性与可扩展性**。

---

### 🎯 Phase 3 解决了什么问题？

在 Phase 2 中，系统已经能够将用户输入结构化为 `Requirement`，并基于模板生成指令。
但仍存在以下限制：

* Prompt 选择不可解释
* 复杂任务只能用单 Prompt 硬扛
* 系统“为什么这样做”无法被记录或回放

Phase 3 引入 **意图推理层与规划层**，解决以上问题。

---

### 🧠 核心能力

#### 1. Intent Analysis（意图分析）

系统会基于 `Requirement` 推断：

* 主意图（design / generate / analyze / review）
* 隐含意图（风险分析、约束检查等）
* 任务复杂度（low / medium / high）
* 关键决策点与潜在风险
* 默认前提假设

对应核心类：

```
codescope/domain/
├── intent_analysis.py
└── intent_analyzer.py
```

---

#### 2. Prompt Planning（指令规划）

系统不再“直接生成 Prompt”，而是先生成 **PromptPlan（执行蓝图）**：

* 明确需要多少步骤
* 每一步的目的与职责
* 步骤之间的输入 / 输出关系
* 是否需要评审或风险分析步骤

对应核心类：

```
codescope/domain/
├── prompt_plan.py
└── prompt_planner.py
```

---

### 🔁 Phase 3 Pipeline

```text
Requirement
   ↓
IntentAnalyzer
   ↓
IntentAnalysis
   ↓
PromptPlanner
   ↓
PromptPlan（可解释、可调试、可回放）
```

当前阶段：

* 使用规则驱动（if / else）
* 不依赖 LLM
* 所有中间结果均可打印与审查

---

### ✅ Phase 3 完成标准

* [x] Prompt 生成前具备明确的意图分析结果
* [x] 支持多 Prompt 步骤规划（Prompt Pipeline）
* [x] Prompt 不再是字符串，而是有职责的 Step
* [x] 系统行为可解释、可测试、可扩展

Phase 3 的交付重点是 **系统结构与决策能力**，而非智能程度。

---

### 🚀 下一阶段（Phase 4 预告）

Phase 4 将在 Phase 3 的稳定结构之上，引入 LLM，用于：

* 增强意图分析准确性
* 辅助 Prompt 规划决策
* 在不破坏可控性的前提下提升智能程度

---
