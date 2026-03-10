+++
date = '2026-02-27T10:00:00+08:00'
draft = false
title = 'AI Agent Security: Protecting Automated Workflows in 2026'
description = 'Learn how to secure AI agent workflows against prompt injection, tool poisoning, and MCP vulnerabilities. Covers OWASP Agentic Top 10, real CVEs, defense strategies, and security tools.'
toc = true
tags = ['AI Security', 'MCP', 'AI Agent', 'Claude Code']
categories = ['AI Guides']
keywords = ['ai agent security', 'mcp security vulnerabilities', 'ai coding security', 'prompt injection defense', 'ai agent attack surface', 'owasp agentic top 10']

[[params.faqItems]]
question = "What is the biggest security risk with AI coding agents?"
answer = "Prompt injection is currently the most dangerous threat. Attackers embed hidden instructions in code repositories, GitHub Issues, or web pages that AI agents read. These injected prompts can manipulate the agent into executing arbitrary commands, leaking sensitive data, or modifying files without user approval. In 2025-2026, multiple CVEs demonstrated real-world prompt injection attacks against tools like GitHub Copilot, Cursor, and MCP servers."

[[params.faqItems]]
question = "How do I scan my MCP servers for vulnerabilities?"
answer = "The fastest way is to run 'uvx mcp-scan' in your project directory. This open-source tool from Invariant Labs reads your MCP configuration, connects to each server, inspects tool descriptions for poisoning indicators, and checks against known vulnerability databases. It supports Claude Code, Claude Desktop, Cursor, and Windsurf. The scan takes under 30 seconds for most setups."

[[params.faqItems]]
question = "Can AI agents be used to improve code security?"
answer = "Yes. AI-powered security tools like Claude Code can perform semantic code analysis that goes beyond pattern matching. They understand code intent, trace data flow across functions, and detect vulnerabilities that traditional SAST tools miss. However, AI security scanning should complement, not replace, human security review and established tools like Snyk or Semgrep."

[[params.faqItems]]
question = "What is the OWASP Agentic Security Top 10?"
answer = "Published in late 2025, the OWASP Agentic Security Top 10 is a framework for understanding risks specific to AI agent systems. It covers prompt injection, broken access control, tool misuse, excessive agency, improper output handling, supply chain vulnerabilities, sensitive data disclosure, insecure interfaces, denial of service, and insufficient logging. It has become the standard reference for auditing AI agent deployments."
+++

![AI Agent Security: protecting automated workflows against prompt injection, tool poisoning, and MCP vulnerabilities](cover.webp)

AI agents are transforming software development. Tools like [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), GitHub Copilot, and Cursor can read entire codebases, execute shell commands, modify files across projects, and interact with external services through protocols like MCP. That power comes with an expanded attack surface that traditional security models were never designed to handle.

In the first two months of 2026 alone, over 30 CVEs were filed against MCP servers and AI agent tooling. Security researchers demonstrated prompt injection attacks that leaked private repository code, tool poisoning techniques that exfiltrated chat histories, and remote code execution vulnerabilities in packages downloaded nearly half a million times.

This article is a comprehensive guide to securing AI agent workflows. Whether you are a developer running Claude Code on personal projects or an engineering lead deploying AI agents across your organization, understanding these threats — and the defenses available — is no longer optional.

## The Expanding AI Agent Attack Surface

Traditional software has well-understood security boundaries. User input goes through validation, authentication gates protect sensitive endpoints, and sandboxes contain untrusted code. AI agents break all of these assumptions.

An AI coding agent typically has:

- **Read access to your entire codebase** including configuration files, environment variables, and secrets
- **Write access to the filesystem** to create and modify any file
- **Shell execution capability** to run arbitrary commands
- **Network access** through MCP servers and API integrations
- **Context from untrusted sources** including GitHub Issues, Pull Requests, documentation, and web pages

This combination creates a unique threat model. The agent is simultaneously a powerful tool and a potential attack vector. It processes untrusted input (code, documentation, user prompts) and has the privileges to act on malicious instructions embedded in that input.

### Why Traditional Security Falls Short

Conventional security tools operate on static analysis patterns. A SAST scanner looks for known vulnerability signatures — SQL injection patterns, hardcoded credentials, unsafe deserialization calls. These tools do not understand the semantic meaning of code, and they certainly do not account for an AI agent that interprets natural language instructions embedded in tool metadata.

The AI agent attack surface introduces threats that have no equivalent in traditional software security:

- **Tool descriptions as attack vectors**: MCP servers expose tool metadata that agents treat as trusted instructions. Poisoning these descriptions can redirect agent behavior.
- **Cross-context prompt injection**: Malicious prompts embedded in data the agent processes (GitHub issues, database records, Slack messages) can override the agent's original instructions.
- **Trust persistence attacks**: Once a user approves an AI tool or MCP server, many clients cache that trust decision indefinitely — even if the tool's behavior changes.
- **Agentic chain attacks**: In multi-agent systems, compromising one agent can cascade through the entire chain, with each agent amplifying the attack.

## Threat Landscape: Four Major Attack Categories

Based on the CVEs and security research published through early 2026, AI agent security threats fall into four primary categories.

### 1. Prompt Injection

Prompt injection is the most prevalent and dangerous threat to AI agents. It exploits the fundamental design of language models: they process all input as context, with no reliable mechanism to distinguish between legitimate instructions and adversarial content.

**How it works**: An attacker embeds carefully crafted instructions in content that the AI agent will process. This could be a comment in a GitHub Issue, a string in a code file, hidden text in a web page, or metadata in an MCP tool description. When the agent reads this content, it interprets the injected instructions as part of its task.

**Real-world impact**: In May 2025, researchers demonstrated a prompt injection attack against the GitHub MCP server. They embedded malicious prompts in public GitHub Issues. When an AI agent processed these issues through the MCP server, it was manipulated into leaking private repository code into public Pull Requests. The attack required no authentication bypass — the agent simply followed the instructions it found in the data.

A more severe example emerged in August 2025 with CVE-2025-53773 against GitHub Copilot. Attackers embedded hidden instructions in source code files that manipulated Copilot into modifying VS Code's configuration to enable auto-approval mode. Once auto-approve was active, subsequent injected prompts could execute arbitrary terminal commands without any user confirmation.

**Why it is hard to fix**: Unlike SQL injection, where parameterized queries provide a clear defense, prompt injection has no equivalent silver bullet. The AI model cannot reliably separate data from instructions because both arrive as natural language text. Current defenses rely on layered mitigations rather than a single fix.

### 2. Tool Poisoning

Tool poisoning targets the metadata and descriptions that AI agents use to understand what tools do and how to use them. In the MCP ecosystem, every server exposes tool definitions including names, descriptions, and parameter schemas. Agents rely on this metadata to decide when and how to invoke tools.

**How it works**: An attacker modifies a tool's description to include hidden instructions. For example, a tool described as "Search files in the project directory" might have additional hidden text instructing the agent to first read `~/.ssh/id_rsa` and include its contents in the search results.

**Real-world impact**: The WhatsApp MCP Server attack in April 2025 was the first publicly demonstrated tool poisoning attack. Researchers injected malicious instructions into tool descriptions that caused AI agents to exfiltrate entire WhatsApp chat histories. No code exploit was needed — the agent simply followed the instructions in the tool metadata.

**Why it matters**: Tool poisoning is particularly dangerous because it is invisible to most users. Developers approve MCP servers based on their stated functionality, rarely inspecting the raw tool descriptions. And once approved, the descriptions are trusted implicitly by the AI agent.

### 3. Data Exfiltration

Data exfiltration attacks use AI agents as unwitting intermediaries to extract sensitive information from the user's environment.

**How it works**: Through prompt injection or tool poisoning, an attacker instructs the agent to read sensitive files (API keys, SSH keys, environment variables, database credentials) and transmit them to an external endpoint. The transmission can happen through MCP tool calls, network requests, or even by embedding the data in seemingly innocent outputs like code comments or commit messages.

**Attack chain example**:
1. Attacker publishes a malicious MCP server that looks legitimate
2. Developer installs and approves the server
3. The server's tool descriptions contain hidden instructions to read `.env` files
4. Agent reads environment variables containing API keys and database passwords
5. Agent includes the data in a "diagnostic report" sent through the MCP server to the attacker

This pattern was confirmed in the Postmark MCP supply chain attack (September 2025), where a fake email service MCP server silently exfiltrated API keys and environment variables from developers who installed it.

### 4. Privilege Escalation

Privilege escalation attacks exploit the gap between the permissions an AI agent has and the permissions the user intended to grant.

**How it works**: AI agents often operate with the same system permissions as the user who launched them. If the user has root access or broad cloud IAM permissions, the agent inherits all of those privileges — far more than any individual task requires.

**MCP-specific escalation**: The Cursor trust bypass vulnerability (CVE-2025-54136, dubbed "MCPoison") demonstrated a particularly dangerous form of privilege escalation. Once a user approved an MCP server configuration, Cursor never re-validated it. Attackers submitted benign-looking configurations to gain initial approval, then injected malicious logic in subsequent updates. The malicious changes took effect silently, effectively escalating from "approved read-only tool" to "arbitrary code execution."

## MCP-Specific Vulnerabilities: A Timeline of Real Incidents

The [Model Context Protocol (MCP)](/posts/ai/2026-02-28-mcp-protocol-explained/) has become the standard for connecting AI agents to external tools and services. Its rapid adoption has also made it a primary target for security researchers and attackers. For a detailed analysis of every MCP CVE filed through early 2026, see [MCP Security 2026: 30 CVEs in 60 Days](/posts/ai/2026-03-10-mcp-security-2026/).

Here are the most significant incidents:

### The Numbers

As of February 2026, the MCP ecosystem presents a concerning security picture:

| Metric | Value |
|--------|-------|
| Official MCP servers in registry | 518 |
| Servers lacking authentication | 38-41% |
| MCP implementations with file ops vulnerable to path traversal | 82% |
| Implementations with code injection risk | 67% |
| CVEs filed (Jan-Feb 2026) | 30+ |
| CVSS 9.6 RCE in a package with 437,000+ downloads | mcp-remote (CVE-2025-6514) |

### Key CVE Timeline

**April 2025 — WhatsApp Tool Poisoning**: First public demonstration of MCP tool poisoning. Malicious tool descriptions caused AI agents to exfiltrate complete chat histories.

**May 2025 — GitHub MCP Prompt Injection**: Attackers planted prompts in public GitHub Issues that manipulated AI agents into leaking private repository code through the GitHub MCP Server.

**June 2025 — Asana Cross-Tenant Exposure**: A flaw in the Asana MCP Server's access control allowed one tenant's AI agent to access other tenants' project data. In SaaS environments, this is the most fundamental security boundary to break.

**June 2025 — MCP Inspector RCE (CVE-2025-49596)**: Anthropic's own debugging tool for MCP servers contained a remote code execution vulnerability. The security auditing tool was itself an attack vector.

**July 2025 — mcp-remote Command Injection (CVE-2025-6514)**: The watershed moment. A CVSS 9.6 command injection flaw in `mcp-remote`, a package with over 437,000 downloads. Malicious remote MCP server URLs could execute arbitrary commands on the client machine.

**July 2025 — Cursor Trust Bypass (CVE-2025-54136)**: Cursor's MCP trust mechanism was fundamentally broken. Once approved, MCP servers were never re-validated, enabling silent injection of malicious logic.

**August 2025 — Filesystem MCP Sandbox Escape**: Anthropic's official Filesystem MCP Server, designed to restrict file access to specified directories, was bypassed using path traversal techniques.

**September 2025 — Postmark Supply Chain Attack**: A malicious package impersonating the Postmark email service was uploaded to the MCP registry, quietly exfiltrating API keys from developers who installed it.

### Vulnerability Type Breakdown

Analyzing the 30+ CVEs by attack vector reveals clear patterns:

- **43% — Exec/shell injection**: MCP servers passing user input to shell commands without sanitization
- **20% — Tooling infrastructure flaws**: Vulnerabilities in MCP clients, inspectors, and proxies
- **13% — Authentication bypass**: Servers lacking auth or implementing it incorrectly
- **10% — Path traversal**: Sandbox escapes in filesystem-related servers
- **14% — Other**: SSRF, cross-tenant exposure, supply chain attacks

The concentration in exec/shell injection is unsurprising. Many MCP servers are thin wrappers around command-line tools, and the temptation to use `exec()` or `subprocess.run()` with string interpolation is strong.

## OWASP Agentic Security Top 10

In late 2025, OWASP published the Agentic Security Top 10, a framework specifically addressing the risks of AI agent systems. It has quickly become the standard reference for evaluating AI agent security posture.

### The Full List

| # | Risk | What It Means for AI Agent Deployments |
|---|------|----------------------------------------|
| 1 | **Prompt Injection** | Malicious instructions in tool descriptions, external data, or user inputs that redirect agent behavior |
| 2 | **Broken Access Control** | Agents operating with excessive permissions; missing authentication on 38%+ of MCP servers |
| 3 | **Tool Misuse** | Agents calling tools with unintended parameters, either through manipulation or hallucination |
| 4 | **Excessive Agency** | Granting tools more permissions than their task requires — the principle of least privilege violation |
| 5 | **Improper Output Handling** | MCP servers returning unsanitized data that agents pass to users or other systems |
| 6 | **Supply Chain Vulnerabilities** | Malicious MCP packages in registries, compromised dependencies, unvetted third-party tools |
| 7 | **Sensitive Data Disclosure** | API keys, credentials, and PII leaked through MCP tool calls or agent outputs |
| 8 | **Insecure Interfaces** | Security gaps in MCP transport layers (stdio, SSE) and communication channels |
| 9 | **Denial of Service** | MCP servers without rate limiting or resource caps, enabling resource exhaustion attacks |
| 10 | **Insufficient Logging** | Most MCP servers have zero audit trail for tool invocations, making incident response impossible |

### Applying OWASP to Your Stack

The OWASP framework works best as an audit checklist. For every MCP server or AI agent tool in your stack, walk through each of the 10 categories and ask:

1. **Can external data influence this tool's behavior?** (Prompt Injection)
2. **Does this tool enforce authentication and authorization?** (Broken Access Control)
3. **What happens if the agent calls this tool with unexpected parameters?** (Tool Misuse)
4. **Does this tool have access to resources it does not need?** (Excessive Agency)
5. **Is the tool's output sanitized before further processing?** (Improper Output Handling)
6. **Did I verify the publisher and inspect the source before installing?** (Supply Chain)
7. **Could this tool access or leak sensitive data?** (Data Disclosure)
8. **Is the communication channel secure?** (Insecure Interfaces)
9. **Are there rate limits and resource caps?** (DoS)
10. **Am I logging tool invocations for audit?** (Logging)

If any answer is uncertain, that category needs mitigation before production deployment.

## Defense Strategies

Securing AI agent workflows requires a defense-in-depth approach. No single measure is sufficient — effective security combines multiple layers.

### 1. Input Validation and Sanitization

Every input to an AI agent should be treated as potentially hostile.

**For MCP servers**:
- Validate all tool input parameters against strict schemas
- Reject inputs containing shell metacharacters unless explicitly required
- Never pass user input directly to `exec()`, `eval()`, or `subprocess.run()` with `shell=True`
- Use parameterized commands instead of string interpolation

**For agent prompts**:
- Implement prompt boundary markers that help the model distinguish instructions from data
- Filter known injection patterns from external content before passing it to the agent
- Use structured data formats (JSON, Protocol Buffers) instead of free text where possible

```python
# BAD: Direct string interpolation
result = subprocess.run(f"grep {user_input} /var/log/app.log", shell=True)

# GOOD: Parameterized command
result = subprocess.run(["grep", user_input, "/var/log/app.log"])
```

### 2. Permission Scoping and Least Privilege

AI agents should operate with the minimum permissions required for each task.

**Practical implementation**:
- Run AI agents in dedicated user accounts with restricted permissions
- Use read-only filesystem mounts for directories the agent should not modify
- Scope MCP server credentials to the minimum required API permissions
- In Claude Code, use the [Hooks system](/posts/ai/2026-02-28-claude-code-hooks-guide/) to enforce permission boundaries programmatically

**MCP-specific scoping**:
- Pin MCP server versions — never use `@latest` in production
- Remove unused MCP servers (`claude mcp list` and remove anything dormant)
- Separate read and write operations into different MCP servers where possible
- Use environment variable isolation so MCP servers cannot access credentials they do not need

### 3. Sandboxing and Isolation

Containment limits the blast radius when a compromise occurs.

**Options by isolation level**:

| Level | Method | Tradeoff |
|-------|--------|----------|
| **Process** | Run MCP servers in separate processes with restricted syscalls | Low overhead, moderate isolation |
| **Container** | Docker/Podman containers with limited mounts and network | Good balance of isolation and usability |
| **VM** | Full virtual machine isolation | Strongest isolation, highest overhead |
| **Network** | Firewall rules restricting MCP server egress | Prevents data exfiltration, may break functionality |

For most development workflows, container-level isolation provides sufficient protection. Run each MCP server in its own container with:
- No access to the host filesystem beyond the project directory
- No network egress except to approved API endpoints
- Resource limits (CPU, memory) to prevent DoS
- Read-only root filesystem

### 4. Human-in-the-Loop Controls

The most effective defense against AI agent misuse is requiring human approval for sensitive operations.

**Claude Code's permission model** is a good reference implementation. By default, it requires explicit user approval before:
- Executing shell commands
- Modifying files outside the project directory
- Making MCP tool calls
- Sending data to external services

This model creates natural checkpoints where users can review and reject suspicious agent actions. The key is to resist the temptation to enable auto-approve modes, especially for operations involving MCP servers or external services.

**When to require human approval**:
- Any operation that modifies production systems
- Tool calls that access sensitive data (credentials, PII, financial records)
- Network requests to endpoints not on an allowlist
- File modifications outside the project working directory
- Any operation that cannot be easily reversed

The [Kiro IDE review](/posts/ai/2026-03-10-kiro-review/) documented a real-world incident where an AI agent caused an AWS outage due to insufficient human oversight during an automated deployment. This case study reinforces why human-in-the-loop controls matter for production workflows.

### 5. Monitoring and Audit Logging

You cannot detect attacks you do not log.

**What to log for AI agent operations**:
- Every MCP tool invocation (tool name, parameters, timestamp, result status)
- All shell commands executed by the agent
- File read/write operations with paths and sizes
- Network requests initiated by MCP servers
- Permission approval/denial decisions
- Agent session start/end with configuration state

**Alert triggers**:
- MCP tool calls to servers not in the approved list
- File access outside the project directory
- Network requests to unknown endpoints
- Unusual patterns in tool invocation frequency
- Configuration changes to MCP server settings

## AI-Powered Security Tools

The security community has responded to AI agent threats with specialized tools. Two categories are emerging: scanning tools that detect vulnerabilities before deployment, and AI-powered analysis tools that use language models to find security issues.

### mcp-scan (Invariant Labs)

The most widely adopted MCP security scanner. Open-source, runs locally, and integrates with all major AI coding tools.

```bash
# Install and run
uvx mcp-scan

# Example output
# Scanning MCP configuration...
# Found 4 MCP servers configured
# [1/4] github — ✅ Clean
# [2/4] filesystem — ❌ Known vulnerability (update required)
# [3/4] custom-server — ⚠️  Suspicious tool description detected
# [4/4] database — ✅ Clean
```

**What it detects**:
- Tool description poisoning indicators
- Known CVEs affecting installed server versions
- Unpinned server versions
- Suspicious patterns in tool metadata

**Supported clients**: Claude Code, Claude Desktop, Cursor, Windsurf

**Recommendation**: Run `mcp-scan` before deploying any new MCP server, and schedule weekly scans for existing configurations.

### Claude Code as a Security Scanner

Claude Code can perform semantic code security analysis that goes beyond traditional static analysis. While not a replacement for dedicated security tools, it offers capabilities that complement them.

**How it differs from traditional SAST**:

| Capability | Traditional SAST | Claude Code Analysis |
|-----------|-----------------|---------------------|
| Pattern matching | Regex-based signature detection | Semantic understanding of code intent |
| Cross-file analysis | Limited to import chains | Full codebase context |
| Business logic flaws | Cannot detect | Can reason about logic errors |
| False positive rate | High (40-60% typical) | Lower due to contextual understanding |
| Custom vulnerability patterns | Requires rule writing | Natural language description |
| Zero-day detection | No | Possible through reasoning |

**Practical workflow**: Use Claude Code alongside established tools. Run Semgrep or Snyk for known vulnerability patterns, then use Claude Code to review flagged areas with semantic understanding and to check for business logic flaws that rule-based tools miss.

For teams moving from prototype to production, the [Prototype to Production guide](/posts/ai/2026-03-09-prototype-to-production/) covers how to integrate security reviews into your deployment pipeline.

### Enterprise Tools

For organizations requiring compliance-grade security:

- **SecureClaw (Adversa AI)**: Enterprise MCP security platform with 55 audit checks, continuous monitoring, and compliance reporting
- **Snyk Agent Scan**: Dependency-level vulnerability scanning for MCP servers, integrated with CI/CD
- **Cisco MCP Scanner**: Network-level analysis of MCP traffic patterns and data exfiltration detection

## Security Checklist for AI Agent Deployments

Use this checklist before deploying AI agents in any environment that handles sensitive data or has production access.

### Before Deployment

- [ ] Run `mcp-scan` on all configured MCP servers
- [ ] Pin every MCP server to a specific version (no `@latest`)
- [ ] Review tool descriptions for all approved MCP servers
- [ ] Remove MCP servers not actively needed
- [ ] Verify that MCP server credentials use minimum required permissions
- [ ] Audit the source code and publisher identity of each MCP server
- [ ] Test MCP servers in an isolated sandbox before production use
- [ ] Ensure the AI agent runs under a restricted user account, not root/admin

### Runtime Controls

- [ ] Require human approval for shell commands and file modifications
- [ ] Disable auto-approve modes for MCP tool calls
- [ ] Implement network egress filtering for MCP server containers
- [ ] Set resource limits (CPU, memory, disk) for agent processes
- [ ] Enable audit logging for all tool invocations and file operations
- [ ] Configure alerting for anomalous tool usage patterns

### Ongoing Maintenance

- [ ] Schedule weekly `mcp-scan` runs (or integrate into CI/CD)
- [ ] Subscribe to MCP security advisories (GitHub, NVD)
- [ ] Periodically re-audit approved MCP servers for configuration changes
- [ ] Review agent logs monthly for suspicious patterns
- [ ] Update MCP servers promptly when security patches are released
- [ ] Rotate credentials used by MCP servers on a regular schedule
- [ ] Test incident response procedures for agent compromise scenarios

### Team Practices

- [ ] Train developers on AI agent security risks (share this article)
- [ ] Establish a policy for evaluating and approving new MCP servers
- [ ] Document which MCP servers are approved and why
- [ ] Assign security ownership for each AI agent deployment
- [ ] Include AI agent security in your regular security review cycle

## Looking Ahead: The Security Arms Race

AI agent security is in its early stages. The first wave of vulnerabilities — the 30+ MCP CVEs, the Copilot prompt injection, the trust bypass attacks — exposed fundamental design assumptions that need rethinking.

Several trends will shape the landscape in the coming months:

**Protocol-level improvements**: The MCP specification is evolving to include better authentication primitives, tool description signing, and permission scoping. Future versions may require cryptographic verification of tool metadata, making tool poisoning significantly harder.

**Standardized security frameworks**: The OWASP Agentic Top 10 is just the beginning. Expect industry-specific compliance frameworks (SOC 2 for AI agents, HIPAA for healthcare AI agents) to emerge as regulatory attention increases.

**AI-powered defense**: The same language model capabilities that make AI agents powerful also make them effective security tools. Expect to see AI-powered security monitors that analyze agent behavior in real-time, detecting anomalous patterns that rule-based systems miss.

**Supply chain hardening**: MCP registries will likely adopt stricter vetting processes, similar to how npm and PyPI have added security scanning and publisher verification. Signed packages and reproducible builds for MCP servers will become standard.

The organizations that invest in AI agent security now — building the monitoring, establishing the policies, training the teams — will be best positioned as these tools become central to engineering workflows.

## Related Reading

**Internal resources**:
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — Full reference for Claude Code features and configuration
- [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) — Understanding the Model Context Protocol
- [MCP Security 2026: 30 CVEs in 60 Days](/posts/ai/2026-03-10-mcp-security-2026/) — Detailed CVE analysis and defense checklist
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Automating security controls with hooks
- [Prototype to Production](/posts/ai/2026-03-09-prototype-to-production/) — Integrating security into deployment pipelines

**External resources**:
- [OWASP Agentic Security Top 10](https://owasp.org/www-project-agentic-security/) — The official OWASP framework for AI agent security risks
- [mcp-scan on GitHub](https://github.com/invariantlabs-ai/mcp-scan) — Open-source MCP security scanner by Invariant Labs
