+++
date = '2026-03-09T14:00:00+08:00'
draft = false
title = 'MCP 安全危机：60 天内曝出 30 个 CVE，到底怎么了？'
description = 'MCP 安全危机实录：2026 年 1-2 月 60 天内曝出 30+ 个 CVE，受影响下载 43.7 万次，被扫描的 2614 个 MCP 实现中 82% 存在路径穿越风险、43% 的漏洞是 Shell 注入。附攻击模式分析、mcp-scan 扫描方法与防御清单。'
toc = true
tags = ['MCP', 'Security', 'AI Agent', 'Claude Code']
categories = ['AI Guides']
keywords = ['mcp 安全', 'mcp 漏洞', 'mcp security 2026', 'mcp cve', 'model context protocol 安全', 'mcp 工具投毒', 'mcp 提示注入']

[[params.faqItems]]
question = "2026 年至今有多少个 MCP 相关的 CVE？"
answer = "截至 2026 年 3 月初，已有超过 30 个与 MCP 服务端和工具链相关的 CVE 被提交。大部分集中在 2026 年 1 月至 2 月之间，漏洞类型涵盖命令注入、路径穿越到完整的远程代码执行（RCE）。"

[[params.faqItems]]
question = "在 Claude Code 中使用 MCP 服务安全吗？"
answer = "安全，但需要做好防护。Claude Code 内置了权限控制，所有 MCP 工具调用都需要用户确认。不过你仍然应该审计 MCP 服务端、定期运行 mcp-scan、锁定服务版本，并对所有凭据遵循最小权限原则。"

[[params.faqItems]]
question = "最常见的 MCP 漏洞类型是什么？"
answer = "执行/Shell 注入占所有已报告 MCP 漏洞的 43%，其次是工具链基础设施缺陷（20%）、认证绕过（13%）和路径穿越（10%）。大多数漏洞的根源都是服务端输入校验不足。"

[[params.faqItems]]
question = "如何扫描我的 MCP 配置是否存在漏洞？"
answer = "最快的方式是在项目目录下运行 uvx mcp-scan。它会读取你的 MCP 配置文件，连接每个服务端，检查工具描述是否有投毒迹象，并与已知漏洞数据库进行比对。整个扫描过程通常不到 30 秒。"

[[params.faqItems]]
question = "mcp-scan 支持 Cursor 等其他 AI IDE 吗？"
answer = "支持。mcp-scan 兼容 Claude Code、Claude Desktop、Cursor、Windsurf 以及任何使用标准 MCP 配置文件的客户端。它会自动检测已安装的客户端并扫描其配置。"
+++

**30 个 CVE，60 天，437,000 次受影响下载。** Model Context Protocol 从"前景看好的开放标准"变成"活跃的攻击面"，速度远超所有人的预期。

2026 年 1 月到 2 月之间，安全研究人员针对 MCP 服务端、客户端和基础设施提交了超过 30 个 CVE。漏洞类型从简单的路径穿越到 CVSS 评分 9.6 的远程代码执行，而涉及的软件包下载量接近 50 万次。问题的根源并非什么高深的零日漏洞——而是缺少输入校验、没有认证机制，以及对工具描述的盲目信任。

如果你正在生产环境中运行 MCP 服务——哪怕只是在 [Claude Code](/zh/posts/ai/2026-02-28-claude-code-complete-guide/) 或 Cursor 里做实验——这篇文章就是你的实战指南，帮你搞清楚出了什么问题以及如何保护自己。

如果你对 MCP 还不太了解，建议先阅读 [MCP 协议详解](/zh/posts/ai/2026-02-28-mcp-protocol-explained/) 再继续。

## 1. 数据说话：MCP 不断扩大的攻击面

MCP 生态在 2025 年下半年到 2026 年初经历了爆发式增长，但安全审查完全跟不上节奏。

以下是截至 2026 年 2 月的关键数据：

| 指标 | 数值 | 来源 |
|------|------|------|
| 注册表中的官方 MCP 服务端 | 518 | MCP Registry 审计，2026 年 2 月 |
| 缺少认证的服务端 | 38–41% | Invariant Labs / 社区扫描 |
| 扫描的 MCP 实现总数 | 2,614 | 学术安全调研，2026 年 1 月 |
| 文件操作存在路径穿越风险 | 82% | 同上 |
| 代码注入风险 | 67% | 同上 |
| 命令注入风险 | 34% | 同上 |
| SSRF 暴露率 | 36.7% | Adversa AI SecureClaw 报告 |
| 已提交 CVE（2026 年 1-2 月） | 30+ | NVD / GitHub Security Advisories |

最核心的数据触目惊心：在研究人员调查的 2,614 个 MCP 实现中，**82% 的文件操作存在路径穿越漏洞**。三分之二有某种形式的代码注入风险，超过三分之一容易受到命令注入攻击。

这些不是纸上谈兵的理论风险——每一个类别都至少有一个已确认的 CVE 和公开的利用代码。

### 攻击类型分布

把这 30 多个 CVE 按攻击向量分类后，规律非常清晰：

- **43% — 执行/Shell 注入**：最大头。MCP 服务端把用户输入直接传给 Shell 命令，没有任何过滤。
- **20% — 工具链基础设施缺陷**：不是服务端本身的问题，而是 MCP 客户端、Inspector 和代理工具的漏洞。
- **13% — 认证绕过**：服务端要么没有认证，要么认证实现有缺陷。
- **10% — 路径穿越**：文件系统相关服务端的沙箱逃逸和目录穿越。
- **14% — 其他**：包括 SSRF、跨租户泄露、供应链攻击和信任机制绕过。

执行/Shell 注入占比最高并不令人意外。很多 MCP 服务端本质上就是命令行工具的薄封装层，直接用字符串拼接调用 `exec()` 或 `subprocess.run()` 的诱惑很大，而后果极其严重。

## 2. 时间线：重大 MCP 漏洞回顾（2025–2026）

漏洞时间线讲述了一个发现速度不断加快的故事。从 2025 年中期几个研究者的零星披露，到 2026 年初 CVE 井喷。

### 2025 年 4 月 — WhatsApp 工具投毒

**攻击类型**：工具投毒（Tool Poisoning）

研究人员证实 WhatsApp MCP Server 存在工具投毒漏洞。攻击者在工具描述中注入恶意指令，可以诱使 AI Agent 执行非预期操作——具体来说就是**窃取整个聊天记录**。这是最早被公开演示的 MCP 攻击之一，暴露了一个根本性问题：AI Agent 对工具描述无条件信任。

这个攻击不需要绕过认证，也不需要利用代码漏洞。AI Agent 只是忠实地执行了它在工具元数据中找到的指令，把这些指令当作了权威命令。

### 2025 年 5 月 — GitHub MCP 提示注入

**攻击类型**：提示注入（Prompt Injection）

GitHub MCP Server 遭受了提示注入攻击。攻击者在公开的 GitHub Issue 和 Pull Request 中嵌入精心构造的提示。当 AI Agent 通过 MCP 服务端处理这些内容时，被操纵将**私有仓库代码**泄露到公开的 Pull Request 中。

这次攻击凸显了通过 MCP 工具处理不可信内容的危险性。任何从外部平台读取用户生成内容的 MCP 服务端都是潜在的提示注入入口。

### 2025 年 6 月 — Asana 跨租户数据泄露

**攻击类型**：跨租户暴露（Cross-Tenant Exposure）

Asana MCP Server 的访问控制逻辑存在缺陷，导致一个租户的 AI Agent 可以访问其他租户的项目数据。在 SaaS 环境中，跨租户隔离是最基本的安全边界，而这个漏洞直接击穿了这道防线。

### 2025 年 6 月 — MCP Inspector 远程代码执行（CVE-2025-49596）

**攻击类型**：远程代码执行（RCE）

颇具讽刺意味的是，Anthropic 自家的 MCP Inspector 工具——原本用于调试和检查 MCP 服务端——本身就包含一个远程代码执行漏洞。开发者用来检查 MCP 服务端安全性的工具，自己却成了攻击入口。

这个 CVE 提醒我们，整个 MCP 工具链（不仅仅是单个服务端）都是攻击面的一部分。

### 2025 年 7 月 — mcp-remote 命令注入（CVE-2025-6514）

**攻击类型**：命令注入 | **CVSS**：9.6 | **下载量**：437,000+

这是一个分水岭事件。`mcp-remote` 是一个广泛使用的远程 MCP 服务连接工具，其中存在命令注入漏洞。攻击者可以构造恶意的远程 MCP 服务端 URL，在客户端机器上执行任意命令。

下载量超过 43.7 万次，CVE-2025-6514 成为第一个有大规模影响的 MCP 漏洞。CVSS 9.6 的评分反映了其极低的利用门槛和极高的严重程度。这是第一个在实际环境中被完整记录的 MCP RCE。

### 2025 年 7 月 — Cursor 信任绕过（CVE-2025-54136，MCPoison）

**攻击类型**：信任绕过（Trust Bypass）

研究人员发现 Cursor IDE 的 MCP 信任机制存在根本性缺陷。用户一旦批准某个 MCP 服务端配置，之后**就再也不会重新验证**。攻击者先提交一个看起来无害的 MCP 配置获得批准，然后在后续更新中注入恶意逻辑，修改会悄无声息地生效。

这类漏洞被命名为"MCPoison"，影响所有缓存信任决策但不做定期重新验证的 MCP 客户端。

### 2025 年 8 月 — 文件系统 MCP 沙箱逃逸

**攻击类型**：沙箱逃逸 / 路径穿越

Anthropic 官方的 Filesystem MCP Server 原本应该限制文件访问在指定目录内，但攻击者通过路径穿越技术绕过了这个限制，获得了沙箱外任意文件的读写权限。

关于 Claude Code 自身安全模型如何处理文件系统访问，请参阅 [Claude Code 安全深度分析](/zh/posts/ai/2026-02-22-claude-code-security/)。

### 2025 年 9 月 — Postmark MCP 供应链攻击

**攻击类型**：供应链攻击（Supply Chain Attack）

有人在 MCP 注册表上传了一个冒充 Postmark 邮件服务的恶意包。安装了这个包的开发者会得到一个看似正常工作的邮件 MCP 服务端，但它在后台悄悄窃取 API 密钥和环境变量。

这是经典的供应链攻击在 MCP 生态中的翻版——之所以得逞，是因为 MCP 注册表缺乏足够的提交审核机制。

### 2025 年 10 月 — Smithery 路径穿越

**攻击类型**：路径穿越

Smithery 是一个热门的 MCP 服务端托管平台，其隔离层存在路径穿越漏洞。攻击者可以突破容器边界，读取其他用户 MCP 部署的 Docker 凭据和环境变量。

### 2026 年 1-2 月 — CVE 大爆发

2026 年头两个月见证了史无前例的 MCP CVE 提交潮。Check Point、Invariant Labs、Adversa AI 的安全团队以及独立研究人员集中发现并报告了数十个新漏洞。主要发现包括：

- **Check Point** 发现 Claude Code 本身可以通过恶意 Hooks、MCP 配置和环境变量进行攻击。他们的研究展示了组合多个 MCP 弱点的攻击链。
- 热门注册表上的多个 MCP 服务端被发现存在基本的 **SSRF 漏洞**，攻击者可以通过 MCP 服务端渗透进内网。
- 多个社区维护的 MCP 服务端被发现对未过滤的输入使用 **`eval()` 或 `exec()`**，直接产生 RCE 路径。

关于 Claude Code Hooks 的详细信息和安全加固方法，请参阅 [Claude Code Hooks 指南](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/)。

## 3. 五种核心攻击模式

分析完整的 CVE 数据集，可以归纳出五种反复出现的攻击模式。理解这些模式比记住单个 CVE 更有价值——它们代表了 MCP 生态的结构性弱点。

### 模式一：工具投毒

**是什么**：在 MCP 工具描述或元数据中注入恶意指令。AI Agent 读取这些描述后，会把它们当作合法指令来执行。

**为什么有效**：AI Agent 默认信任工具描述。目前没有标准机制来验证或签名工具描述。控制了工具描述的攻击者，等于控制了 Agent 使用该工具时的行为。

**真实案例**：2025 年 4 月的 WhatsApp MCP 攻击通过工具描述投毒窃取聊天记录，全程没有利用任何代码漏洞。

**防御方法**：批准 MCP 服务端前务必审查工具描述。使用 `mcp-scan` 检测异常工具描述。在 [Claude Code](/zh/posts/ai/2026-02-28-claude-code-complete-guide/) 中，绝不自动批准来自不可信来源的 MCP 工具。

### 模式二：通过外部数据进行提示注入

**是什么**：在 MCP 服务端会读取的数据源中植入恶意提示——GitHub Issue、Slack 消息、数据库记录、邮件或任何外部内容。

**为什么有效**：MCP 服务端充当 AI Agent 和外部系统之间的桥梁。当 AI Agent 处理这些系统的内容时，无法可靠地区分正常数据和注入的提示。AI 把所有内容都当作上下文，因此容易受到嵌入其中的指令操控。

**真实案例**：2025 年 5 月的 GitHub MCP 提示注入利用公开 Issue 窃取私有仓库代码。

**防御方法**：将所有外部数据视为不可信。在 MCP 服务端实现输出过滤。尽可能使用结构化数据格式而非自由文本。考虑在沙箱环境中运行处理外部内容的 MCP 操作。

### 模式三：信任绕过

**是什么**：利用 MCP 客户端存储和验证信任决策的弱点。一旦用户批准了某个 MCP 服务端，攻击者修改其行为而不会被重新检查。

**为什么有效**：大多数 MCP 客户端采用"首次使用即信任"（TOFU）模型。首次审批流程比较严格，但后续变更不做验证。这就创造了一个窗口期，已批准的服务端可以被悄悄篡改。

**真实案例**：Cursor 的 MCPoison 漏洞（CVE-2025-54136）利用的正是这种模式。

**防御方法**：锁定 MCP 服务端版本。使用基于哈希的配置验证。定期重新审计已批准的服务端。监控 MCP 配置文件的变更。

### 模式四：供应链攻击

**是什么**：在注册表上发布恶意 MCP 服务端，通过冒充合法服务或篡改已有包来实施。

**为什么有效**：MCP 注册表生态仍在发展中，审核机制很薄弱。开发者往往凭名称直觉安装 MCP 服务端，不会验证发布者身份或审查源码。

**真实案例**：2025 年 9 月的 Postmark 供应链攻击在注册表上发布了一个功能正常但暗藏后门的 MCP 服务端。

**防御方法**：只安装来自经过验证的发布者的 MCP 服务端。安装前审查源代码。使用 `mcp-scan` 检查已知恶意包。锁定版本并监控异常更新。推荐参考 [Claude Code 最佳 MCP 服务端精选](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/)。

### 模式五：跨租户暴露

**是什么**：利用共享基础设施访问其他用户或组织的数据。

**为什么有效**：许多 MCP 服务端运行在共享托管平台上，或通过同一服务处理多个租户的请求。如果租户隔离没有在每一层（从请求处理到数据存储）都正确实现，跨租户数据泄露就会成为可能。

**真实案例**：2025 年 6 月的 Asana 跨租户暴露和 2025 年 10 月的 Smithery 路径穿越都属于这种模式。

**防御方法**：在专用基础设施上运行敏感 MCP 服务端。审计共享 MCP 托管平台的租户隔离机制。避免向 MCP 服务端传递多租户凭据。

## 4. OWASP Agentic Security Top 10

作为对 AI Agent 漏洞激增（包括大量 MCP 相关问题）的回应，OWASP 在 2025 年底发布了 **Agentic Security Top 10**。这个框架为思考 AI Agent 系统特有的风险提供了结构化方法。

完整列表及其与 MCP 的关联如下：

| # | 风险 | MCP 关联度 |
|---|------|-----------|
| 1 | **提示注入** | 直接相关：工具描述投毒、外部数据注入 |
| 2 | **访问控制失效** | 直接相关：跨租户暴露、38% 的服务端缺少认证 |
| 3 | **工具滥用** | 直接相关：Agent 以非预期参数调用工具 |
| 4 | **过度授权** | 工具获得的权限超出实际需要 |
| 5 | **不当输出处理** | MCP 服务端返回未过滤的数据给 Agent |
| 6 | **供应链漏洞** | 直接相关：注册表中的恶意 MCP 包 |
| 7 | **敏感数据泄露** | API 密钥和凭据通过 MCP 工具调用泄露 |
| 8 | **不安全的接口** | MCP 传输层（stdio、SSE）的安全缺口 |
| 9 | **拒绝服务** | MCP 服务端缺乏速率限制或资源上限 |
| 10 | **日志不足** | 大多数 MCP 服务端对工具调用完全没有审计日志 |

OWASP 框架几乎完美映射了我们在 MCP 生态中看到的漏洞。Top 10 的每一项风险都至少对应一个已确认的 MCP CVE 或已记录的利用方式。

对于实际操作者来说，OWASP 列表是一份出色的审计清单。评估 MCP 服务端时，逐一过一遍这 10 个类别，问自己："这个风险有没有被缓解？"

## 5. 安全工具横评

安全社区已经针对 MCP 漏洞浪潮推出了专门的扫描和审计工具。以下是截至 2026 年 3 月最值得关注的五款：

### mcp-scan（Invariant Labs）

目前使用最广泛的 MCP 安全扫描器。开源、本地运行、支持所有主流 MCP 客户端。

- **安装**：`uvx mcp-scan`（需要 `uv` 包管理器）
- **功能**：读取 MCP 配置文件，连接每个服务端，检查工具描述是否有投毒迹象，与已知漏洞数据库比对
- **支持客户端**：Claude Code、Claude Desktop、Cursor、Windsurf
- **优势**：速度快（30 秒内完成）、零配置、社区维护的漏洞数据库
- **局限**：专注于工具层面扫描，不审计服务端源码

### SecureClaw（Adversa AI）

企业级 MCP 安全平台，包含 55 项独立审计检查。

- **类型**：商业 / SaaS
- **功能**：深度安全审计，包括 SSRF 检测、认证测试、输入校验分析和合规报告
- **优势**：审计覆盖面最广、可生成管理层报告、支持持续监控模式
- **局限**：企业定价，完整功能需要云端连接

### agent-audit

一款基于 OWASP 标准的审计工具，专为 AI Agent 安全设计，覆盖 MCP。

- **类型**：开源
- **功能**：将 MCP 服务端配置与 OWASP Agentic Security Top 10 进行映射，生成风险评分和修复建议
- **优势**：基于标准的方法论，适合合规需求
- **局限**：项目较新，漏洞数据库不如 mcp-scan 完善

### Cisco MCP Scanner

思科安全研究团队推出的网络层 MCP 安全扫描器。

- **类型**：开源
- **功能**：分析 MCP 流量模式，检测异常工具调用，在网络层监控数据外泄指标
- **优势**：能捕获工具层扫描器遗漏的攻击，可集成现有网络安全基础设施
- **局限**：需要网络层访问权限，部署较复杂

### Snyk Agent Scan

Snyk 将其依赖扫描平台扩展到了 MCP 和 AI Agent 依赖领域。

- **类型**：商业（有免费版）
- **功能**：扫描 MCP 服务端依赖中的已知漏洞，监控供应链攻击，集成 CI/CD 流水线
- **优势**：利用 Snyk 庞大的漏洞数据库，已使用 Snyk 的团队可以无缝衔接
- **局限**：聚焦依赖层面的漏洞，不扫描工具描述或运行时行为

### 工具对比矩阵

| 功能 | mcp-scan | SecureClaw | agent-audit | Cisco Scanner | Snyk Agent |
|------|----------|------------|-------------|---------------|------------|
| **价格** | 免费 | 企业级 | 免费 | 免费 | 免费增值 |
| **工具投毒检测** | 是 | 是 | 部分 | 否 | 否 |
| **依赖扫描** | 否 | 是 | 否 | 否 | 是 |
| **OWASP 映射** | 否 | 是 | 是 | 否 | 否 |
| **网络分析** | 否 | 否 | 否 | 是 | 否 |
| **CI/CD 集成** | 基础 | 是 | 否 | 是 | 是 |
| **部署时间** | < 1 分钟 | 数小时 | 数分钟 | 数小时 | 数分钟 |
| **最适合** | 个人开发者 | 企业 | 合规场景 | SOC 团队 | 开发团队 |

**建议**：先用 `mcp-scan` 快速获得可见性。如果需要依赖链监控，加上 Snyk Agent Scan。有合规要求的企业环境考虑 SecureClaw。

## 6. 实战防御清单

基于上述漏洞模式和可用工具，这里提供一份按优先级排列的防御清单，适用于所有 MCP 服务端运维者。

### 优先级 1 — 今天就做

这些操作针对最常见和最严重的漏洞模式，投入极少但能立即见效。

- [ ] **运行 `mcp-scan`** 扫描当前 MCP 配置。有发现就先修再往下走。
- [ ] **锁定 MCP 服务端版本**。生产环境绝不使用 `@latest`。指定精确版本：`npx @package/name@2.1.3`。
- [ ] **审查工具描述**。检查每个已批准 MCP 服务端的工具描述，留意异常指令、URL 或对敏感数据的引用。
- [ ] **移除闲置 MCP 服务端**。不在用的服务端就是多余的攻击面。运行 `claude mcp list` 删掉所有不活跃的。
- [ ] **检查认证**。对每个访问外部服务的 MCP 服务端，确认凭据使用了最小必要权限。轮换所有被广泛共享过的凭据。

### 优先级 2 — 本周完成

这些操作需要更多规划，但能解决重大风险。

- [ ] **实施权限边界**。在 Claude Code 中使用权限系统限制哪些 MCP 工具可以无需确认即被调用。配置详情参见 [Claude Code MCP 配置指南](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/)。
- [ ] **审计 MCP 服务端来源**。对每个服务端，验证发布者身份，检查 GitHub 仓库的最近活动和维护者声誉，审阅是否有安全相关的 Issue。
- [ ] **建立监控**。记录所有 MCP 工具调用日志。至少捕获工具名称、输入参数和时间戳，为事件响应提供审计跟踪。
- [ ] **分离敏感操作**。如果某个 MCP 服务端同时处理读写操作，考虑是否可以限制为只读模式。
- [ ] **审查 Hooks 和环境变量**。根据 Check Point 的发现，审计你的 Claude Code Hooks，确保没有 MCP 服务端能访问敏感环境变量。详情参见 [Hooks 指南](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/)。

### 优先级 3 — 持续实践

这些是长期维护安全的良好习惯。

- [ ] **定期扫描**。每周运行 `mcp-scan` 或将其加入 CI 流水线。
- [ ] **订阅 MCP 安全公告**。关注 MCP GitHub 仓库和 NVD 的新 CVE 通知。
- [ ] **隔离测试 MCP 服务端**。新增 MCP 服务端前，先在沙箱环境中测试。
- [ ] **贡献发现**。发现漏洞时通过负责任披露渠道报告。MCP 生态的安全需要社区共同维护。
- [ ] **跟踪协议变更**。MCP 规范正在快速演进，新版本可能带来安全改进（也可能引入新的攻击面）。

## 7. 手把手教你扫描 MCP 配置

以下是使用 `mcp-scan` 扫描 MCP 配置的详细步骤——这是目前最易上手的工具。

### 前置条件

需要 Python 3.10+ 和 `uv` 包管理器：

```bash
# 安装 uv（如果还没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证安装
uv --version
```

### 运行首次扫描

```bash
# 进入项目目录（任意目录均可）
cd ~/your-project

# 运行 mcp-scan，会自动检测 MCP 配置
uvx mcp-scan
```

工具会自动查找 Claude Code、Claude Desktop、Cursor 和 Windsurf 的 MCP 配置文件，连接每个已配置的服务端，获取工具列表并进行分析。

### 解读扫描结果

典型的扫描输出如下：

```
Scanning MCP configuration...
Found 4 MCP servers configured

[1/4] github — npx @modelcontextprotocol/server-github
  ✅ No tool poisoning detected
  ✅ Tool descriptions are clean
  ⚠️  Server version not pinned

[2/4] filesystem — npx @anthropic/mcp-filesystem
  ✅ No tool poisoning detected
  ⚠️  Known vulnerability: sandbox escape (patched in v2.1.0+)
  ❌ Current version v1.8.3 is affected — UPDATE REQUIRED

[3/4] custom-server — node ./mcp/server.js
  ✅ No tool poisoning detected
  ✅ No known vulnerabilities

[4/4] unknown-registry-server — npx @some-random/mcp-tool
  ❌ Tool poisoning indicators detected in "query" tool description
  ⚠️  Publisher not verified
  ❌ REMOVE OR AUDIT THIS SERVER

Summary: 2 issues found, 1 critical
```

### 处理扫描结果

- **❌ 严重发现**：立即处理。在继续使用之前移除或更新受影响的服务端。
- **⚠️ 警告**：安排在一周内解决。版本锁定和更新都是快速修复。
- **✅ 正常**：很好，但要定期重新扫描。新漏洞随时可能被发现。

### 自动化扫描

将 `mcp-scan` 加入开发工作流：

```bash
# 添加到 pre-commit hook 或 CI 步骤
uvx mcp-scan --format json > mcp-scan-results.json

# 发现严重问题时让 CI 失败
uvx mcp-scan --exit-code
```

`--exit-code` 参数会在发现严重漏洞时返回非零退出码，适合作为 CI/CD 的门禁检查。

## 8. 展望：接下来会怎样

MCP 安全格局正在快速演变，有几个方向值得关注：

**协议层改进**：MCP 规范团队正在推进内置认证标准、工具描述签名和服务端证明机制。这些变更有望从协议层面解决工具投毒和供应链攻击的根源，而不是依赖外部工具。

**注册表审核**：主要 MCP 注册表正在实施发布者验证和自动安全扫描。这将减少（但不能消除）供应链风险。

**客户端防御**：AI 编码工具正在添加更细粒度的权限控制。Claude Code 已经要求 MCP 工具调用必须经过明确批准，[Hooks 系统](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/)提供了额外的控制点。预计其他客户端也会跟进。

**企业落地障碍**：MCP 生态当前的安全状况是企业采用的重大阻碍。有严格安全要求的组织正在等待签名工具、验证注册表和标准化审计框架带来的成熟度。

60 天内 30 个 CVE 是一记警钟。MCP 社区正在积极响应，但生态要达到生产部署所需的安全基线还需要数月时间。在此期间，上面的防御清单就是你最好的保护措施。

## 9. 常见问题

**问：现在可以在生产环境中安全使用 MCP 服务端吗？**

可以，但有不少前提条件。锁定版本、定期扫描、最小权限、只安装来自可信且经过验证的来源的服务端。风险是可控的，但不可忽视。

**问：我们公司要求 SOC 2 合规，能用 MCP 吗？**

没有额外控制措施的话不行。你需要对所有 MCP 工具调用进行全面日志记录、定期漏洞扫描、访问控制，以及针对 MCP 相关威胁的事件响应计划。SecureClaw 和 agent-audit 可以帮助做合规映射。

**问：stdio 传输比 SSE 更安全吗？**

总体来说是的。stdio 传输在本地运行，不暴露网络端点。SSE（Server-Sent Events）传输需要正确的认证、TLS 和网络访问控制。如果不需要远程 MCP 服务端，优先使用 stdio。

**问：Claude Code 如何防御 MCP 攻击？**

Claude Code 实现了多层防护：所有 MCP 工具调用需要明确的权限确认、Hooks 系统支持自定义校验、以及沙箱执行环境。完整分析请阅读 [Claude Code 安全指南](/zh/posts/ai/2026-02-22-claude-code-security/)。

**问：应该自建 MCP 服务端还是用社区的？**

两种方式各有利弊。自建服务端让你完全掌控，但安全要自己负责。社区服务端受益于更广泛的测试，但引入了供应链风险。对于关键操作，经过安全审计的自建服务端更安全。对于通用工具，来自[精选列表](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/)的经过审查的社区服务端是合理选择。

## 10. 延伸阅读

- [MCP 协议详解：完整技术指南](/zh/posts/ai/2026-02-28-mcp-protocol-explained/) — 先理解 MCP 工作原理，再谈安全加固
- [Claude Code 完全指南](/zh/posts/ai/2026-02-28-claude-code-complete-guide/) — 掌握使用 MCP 的 AI 编码工具
- [Claude Code 安全深度分析](/zh/posts/ai/2026-02-22-claude-code-security/) — Claude Code 如何防御本文描述的攻击
- [Claude Code MCP 配置指南](/zh/posts/ai/2026-02-28-claude-code-mcp-setup/) — 在 Claude Code 中安全配置 MCP 服务端
- [Claude Code 最佳 MCP 服务端精选](/zh/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — 经过审查的可信 MCP 服务端
- [Claude Code Hooks 指南](/zh/posts/ai/2026-02-28-claude-code-hooks-guide/) — 用 Hooks 为 MCP 操作添加自定义安全控制

## 相关阅读

- [MCP 安全实战指南：AI Agent 时代的攻防博弈与防护策略](/zh/posts/ai/2026-02-23-mcp-security-guide/) — MCP 安全的系统化攻防指南
- [MCP 协议全面解析：AI 连接万物的通用标准](/zh/posts/ai/2026-02-20-mcp-protocol-guide/) — MCP 协议本身
- [Claude Code Security 深度解析](/zh/posts/ai/2026-02-22-claude-code-security/) — Claude Code 侧的安全机制
- [2026 年 AI 代码安全工具横评](/zh/posts/ai/2026-03-13-ai-code-security-tools-compared/) — 安全工具的横向对比
- [AI Agent 安全指南：2026 年自动化工作流防护全攻略](/zh/posts/ai/2026-02-27-ai-agent-security/) — 更宽的 Agent 安全面
