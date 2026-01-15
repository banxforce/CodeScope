## Phase 4 更新内容

### Phase 4 Goal

> Phase 4 的主要目标是将 LLM 引入 CodeScope 核心语义流水线，实现：
> - **LLM 驱动的意图分析**：Requirement → IntentAnalysis  
> - **结构化需求拆解**：Requirement → PromptPlan  
> - **可回放、可审计的执行规划**：生成 PromptStep 列表  
> - **保持 deterministic**，暂不执行检索或生成最终答案  
> 本阶段重点是 **规划与结构化**，而非执行或检索。

---

### 核心组件

#### 1. RequirementParserLLM

- 将用户输入的需求文本转换为 `Requirement` 对象  
- 提取字段：
  - domain, stage, core_intent, entities, operations  
  - non_functional, constraints, implicit_signals  
- 支持附加字段（Phase 4 可选）：
  - confidence, warnings, assumptions  
- 输出示例：

```python
Requirement(
    domain='用户管理',
    stage=None,
    core_intent='优化用户表查询性能',
    entities=['用户表', '查询性能'],
    operations=['refactor'],
    non_functional=['性能'],
    constraints=[],
    implicit_signals=['对速度有较高期望'],
    confidence=0.75,
    warnings=['AMBIGUOUS_SCOPE', 'NON_FUNCTIONAL_UNCLEAR'],
    assumptions=['用户表存在于某个数据库系统中', '存在需要优化的具体查询']
)
```

##### Warning 判定语义

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

---

#### 2. IntentAnalyzerLLM

* 基于 Requirement 生成 `IntentAnalysis`
* 字段：

  * primary_intent, secondary_intents, complexity_level
  * key_decisions, risks, assumptions
* 输出严格对应数据模型，无 Prompt 或生成细节
* 示例：

```python
IntentAnalysis(
    primary_intent='review',
    secondary_intents=['refactor'],
    complexity_level='medium',
    key_decisions=[
        '是否需要评估当前查询性能的基准',
        '是否需要在数据一致性与查询速度之间进行权衡',
        '是否考虑优化对现有业务逻辑的影响'
    ],
    risks=[
        '优化范围不明确，可能导致工作边界不清',
        '非功能性要求（性能）的具体目标不清晰，难以衡量优化效果'
    ],
    assumptions=['用户表存在于某个数据库系统中', '存在需要优化的具体查询']
)
```

---

#### 3. DrivenPromptPlannerLLM

* 将 Requirement + IntentAnalysis → PromptPlan
* PromptPlan 由若干 PromptStep 组成，每步包含：

  * step_id, purpose, prompt_ref, input_requirements
  * output_type, constraints, optional
* 支持 JSON 输出与校验，不使用 eval
* 执行策略：`sequential`
* 严格遵守字段规范与复杂度规则

#### 系统提示词

* `REQUIREMENT_SYSTEM_PROMPT`：指导 RequirementParserLLM
* `INTENT_ANALYSIS_SYSTEM_PROMPT`：指导 IntentAnalyzerLLM
* `PROMPT_PLANNER_SYSTEM_PROMPT_CN`：指导 DrivenPromptPlannerLLM

> 所有 LLM 模块仅输出结构化 JSON，不生成解释或 Markdown

---

### Phase 4 流程概览

```text
用户输入文本
        │
        ▼
RequirementParserLLM
        │
        ▼
Requirement (结构化)
        │
        ▼
IntentAnalyzerLLM
        │
        ▼
IntentAnalysis (结构化)
        │
        ▼
DrivenPromptPlannerLLM
        │
        ▼
PromptPlan (结构化蓝图)
```

> 注意：Phase 4 不执行最终 Prompt，也不进行 RAG 检索或结果生成。

---