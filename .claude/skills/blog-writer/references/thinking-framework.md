# 判断框架详细示例

## 示例 1：Harness Engineering 文章

### 3.1 核心立场
关于 Harness Engineering，我认为**模型是 AI Agent 中最不重要的部分**，因为 LangChain 不换模型只改 harness 就从 TerminalBench 第 30 名升到第 5 名（52.8%→66.5%）。

### 3.2 常见误解
- 误解 1："GPT-6 出来就好了" → 实际上大部分 Agent 失败不是模型问题，是 harness 问题。Opus 4.6 在 Claude Code 里排 #33，换个 harness 排 #5。
- 误解 2："CLAUDE.md 写得越详细越好" → ETH Zurich 研究：超过 60 行反而降低 20% 表现，同时增加 token 成本。
- 误解 3："约束限制了 Agent 的能力" → Ashby 定律：约束是可靠自主运行的前提条件。解题空间越窄，harness 越能全面覆盖。

### 3.3 真实案例
- OpenAI Codex 团队：7 名工程师用 harness engineering 写了 100 万行代码，零行人写
- LangChain：不换模型，只改 harness，TerminalBench 从 #30 升到 #5
- Stripe Minions：每周合并 1,300+ PR，用"两次失败升级规则"防止无限重试
- 本博客：GSC CTR 从 0.33% 通过 FAQ + 内链优化提升（验证中）

### 3.4 边界条件
- 该用：生产级 AI Agent，需要稳定性和可预测性
- 不该用：一次性实验、原型验证（直接 prompt 就够了）
- 代价：前期投入时间搭建 harness 基础设施，不适合快速迭代的探索阶段

### 3.5 读者行动
- 从今天开始写 CLAUDE.md（控制在 60 行以内）
- 给现有项目加一个 PostToolUse hook 做自动类型检查
- 用 feedback 日志收集 Agent 失败模式，据此改进 harness

### 3.6 叙事弧线
1. 开头用反常识结论引爆："模型是最不重要的部分"
2. 读者直觉反驳：怎么可能？模型不是核心吗？
3. 用 LangChain 案例证明：同模型不同 harness，天壤之别
4. 定义 harness：Guides（前馈）+ Sensors（反馈）
5. 拆解 3 个误区
6. 给出 5 层实操指南（从 CLAUDE.md 到架构约束）
7. 说明边界：什么时候不需要 harness engineering

---

## 示例 2：Claude Code vs Cursor vs Copilot 三方对比

### 3.1 核心立场
关于 AI 编程工具选择，我认为**大多数开发者应该同时用两个工具而不是只选一个**，因为三个工具的设计哲学根本不同，没有一个能覆盖所有场景。

### 3.2 常见误解
- 误解 1："选最贵的就行" → Copilot $10/月解决 80% 的日常编辑，Claude Code $200/月只在复杂重构时才值这个价
- 误解 2："Cursor Composer 2 是自研模型" → 底座是月之暗面 Kimi K2.5，75% 算力训练不等于 75% 贡献

### 3.3 真实案例
- 我个人栈：Cursor + Composer 2 处理 80% 日常，Claude Code 处理 20% 复杂任务
- Cursor Composer 2 在 CursorBench 61.3 vs Claude Opus 58.0：只差 3.7 分，感知不到
- 成本：Composer 2 $0.50/M vs Opus $15/M，差 30 倍

### 3.4 边界条件
- Claude Code 赢：>1 万行重构、安全审计、架构决策
- Cursor 赢：日常编辑、Tab 补全、IDE 集成
- Copilot 赢：多 IDE 支持、价格最低、不想换编辑器

### 3.5 读者行动
"如果你只能花 $10/月 → Copilot。如果你写代码超过 4 小时/天 → 加 Cursor。如果你经常做大型重构 → 再加 Claude Code。"

---

## 判断框架自检

写完判断框架后，用以下问题自检：

1. 如果删掉核心立场，文章还能成立吗？→ 如果能，说明立场太弱
2. 误解部分是真正反常识的吗？→ "X 也有缺点"不算反常识
3. 案例是真实的还是编造的？→ 编造案例比没有案例更糟
4. 边界条件是具体的还是"视情况而定"？→ 后者等于没说
5. 行动建议是可执行的还是空泛的？→ "值得关注"是空泛的
