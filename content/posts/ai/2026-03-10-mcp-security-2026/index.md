+++
date = '2026-03-04T10:00:00+08:00'
draft = false
title = 'MCP Security 2026: 30 CVEs in 60 Days — What Went Wrong'
description = 'A deep dive into 30 MCP vulnerabilities filed in 60 days. Covers attack patterns, CVE timeline, OWASP Agentic Top 10, security tools comparison, and a practical defense checklist for MCP server operators.'
toc = true
tags = ['MCP', 'Security', 'AI Agent', 'Claude Code']
categories = ['AI Guides']
keywords = ['mcp security', 'mcp vulnerabilities', 'mcp security 2026', 'mcp cve', 'model context protocol security', 'mcp tool poisoning', 'mcp prompt injection']

[[params.faqItems]]
question = "How many MCP CVEs have been filed in 2026 so far?"
answer = "As of early March 2026, over 30 CVEs related to MCP servers and tooling have been filed. The majority were reported between January and February 2026, covering vulnerabilities ranging from command injection and path traversal to full remote code execution."

[[params.faqItems]]
question = "Is it safe to use MCP servers with Claude Code?"
answer = "Yes, but with precautions. Claude Code has built-in permission controls that require user approval before executing MCP tool calls. However, you should still audit your MCP servers, run mcp-scan regularly, pin server versions, and follow the principle of least privilege for all credentials."

[[params.faqItems]]
question = "What is the most common MCP vulnerability type?"
answer = "Exec/shell injection accounts for 43% of all reported MCP vulnerabilities. This is followed by tooling infrastructure flaws (20%), authentication bypass (13%), and path traversal (10%). Most of these stem from insufficient input validation on the server side."

[[params.faqItems]]
question = "How do I scan my MCP setup for vulnerabilities?"
answer = "The fastest way is to run uvx mcp-scan in your project directory. It reads your MCP configuration, connects to each server, inspects tool descriptions for poisoning indicators, and checks against known vulnerability databases. The scan takes under 30 seconds for most setups."

[[params.faqItems]]
question = "Does mcp-scan work with Cursor and other AI IDEs?"
answer = "Yes. mcp-scan supports Claude Code, Claude Desktop, Cursor, Windsurf, and any client that uses standard MCP configuration files. It automatically detects which clients are installed and scans their configurations."
+++

**30 CVEs. 60 days. 437,000 compromised downloads.** The Model Context Protocol went from "promising open standard" to "active threat surface" faster than anyone predicted.

Between January and February 2026, security researchers filed over 30 CVEs targeting MCP servers, clients, and infrastructure. The vulnerabilities ranged from trivial path traversals to a CVSS 9.6 remote code execution flaw in a package downloaded nearly half a million times. And the root causes were not exotic zero-days — they were missing input validation, absent authentication, and blind trust in tool descriptions.

If you are running MCP servers in production — or even just experimenting with them in [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/) or Cursor — this article is your field guide to what went wrong and how to protect yourself.

For readers new to MCP, start with the [MCP Protocol Explained](/posts/ai/2026-02-28-mcp-protocol-explained/) guide before diving in.

## 1. The Numbers: MCP's Growing Attack Surface

The MCP ecosystem grew explosively through late 2025 and into 2026. That growth outpaced security review by a wide margin.

Here are the numbers as of February 2026:

| Metric | Value | Source |
|--------|-------|--------|
| Official MCP servers in registry | 518 | MCP Registry audit, Feb 2026 |
| Servers lacking authentication | 38–41% | Invariant Labs / community scans |
| Total MCP implementations scanned | 2,614 | Academic security survey, Jan 2026 |
| Implementations with file ops prone to path traversal | 82% | Same survey |
| Code injection risk | 67% | Same survey |
| Command injection risk | 34% | Same survey |
| SSRF exposure rate | 36.7% | Adversa AI SecureClaw report |
| CVEs filed (Jan–Feb 2026) | 30+ | NVD / GitHub Security Advisories |

The headline stat is stark: among 2,614 MCP implementations surveyed by security researchers, **82% use file operations that are vulnerable to path traversal attacks**. Two-thirds have some form of code injection risk. Over a third are susceptible to command injection.

These are not theoretical risks. Every single category has at least one confirmed CVE with a public exploit.

### Attack Type Breakdown

When we categorize the 30+ CVEs by attack vector, a clear pattern emerges:

- **43% — Exec/shell injection**: The dominant category. MCP servers that pass user input to shell commands without sanitization.
- **20% — Tooling infrastructure flaws**: Vulnerabilities in MCP clients, inspectors, and proxy tools — not the servers themselves.
- **13% — Authentication bypass**: Servers that either lack auth entirely or implement it incorrectly.
- **10% — Path traversal**: Sandbox escapes and directory traversal in filesystem-related servers.
- **14% — Other**: Including SSRF, cross-tenant exposure, supply chain attacks, and trust mechanism bypasses.

The concentration in exec/shell injection is not surprising. Many MCP servers are thin wrappers around command-line tools. The temptation to call `exec()` or `subprocess.run()` with string interpolation is strong, and the consequences are severe.

## 2. Timeline: Major MCP Vulnerabilities (2025–2026)

The vulnerability timeline tells a story of accelerating discovery. What started with a handful of researcher disclosures in mid-2025 became a flood of CVEs by early 2026.

### April 2025 — WhatsApp Tool Poisoning

**Attack type**: Tool Poisoning

Researchers demonstrated that the WhatsApp MCP Server was vulnerable to tool poisoning. By injecting malicious instructions into tool descriptions, attackers could trick AI agents into executing unintended operations — specifically, exfiltrating **entire chat histories**. This was one of the first publicly demonstrated MCP attacks and revealed a fundamental problem: AI agents trust tool descriptions implicitly.

The attack required no authentication bypass or code exploitation. The AI agent simply followed the instructions it found in the tool metadata, treating them as authoritative.

### May 2025 — GitHub MCP Prompt Injection

**Attack type**: Prompt Injection

The GitHub MCP Server fell victim to a prompt injection attack. Attackers embedded carefully crafted prompts in public GitHub Issues and Pull Requests. When an AI agent processed these through the MCP server, it was manipulated into leaking **private repository code** into public Pull Requests.

This attack highlighted the danger of processing untrusted content through MCP tools. Any MCP server that reads user-generated content from external platforms is a potential prompt injection vector.

### June 2025 — Asana Cross-Tenant Data Exposure

**Attack type**: Cross-Tenant Exposure

A flaw in the Asana MCP Server's access control logic allowed one tenant's AI agent to access project data belonging to other tenants. In SaaS environments, cross-tenant isolation is the most fundamental security boundary. This vulnerability broke that boundary completely.

### June 2025 — MCP Inspector RCE (CVE-2025-49596)

**Attack type**: Remote Code Execution

In an ironic twist, Anthropic's own MCP Inspector tool — designed for debugging and inspecting MCP servers — contained a remote code execution vulnerability. The very tool developers used to check their MCP servers was itself an attack vector.

This CVE underscored that the entire MCP toolchain, not just individual servers, is part of the attack surface.

### July 2025 — mcp-remote Command Injection (CVE-2025-6514)

**Attack type**: Command Injection | **CVSS**: 9.6 | **Downloads**: 437,000+

This was the watershed moment. `mcp-remote`, a widely-used package for connecting to remote MCP servers, contained a command injection vulnerability. Attackers could craft malicious remote MCP server URLs that would execute arbitrary commands on the client machine.

With over 437,000 downloads, CVE-2025-6514 became the first documented MCP vulnerability with mass-scale impact. Its CVSS score of 9.6 reflected the trivial exploitability and critical severity. This was the first fully documented MCP RCE in the wild.

### July 2025 — Cursor Trust Bypass (CVE-2025-54136, MCPoison)

**Attack type**: Trust Bypass

Researchers discovered that Cursor IDE's MCP trust mechanism was fundamentally broken. Once a user approved an MCP server configuration, **it was never re-validated**. Attackers exploited this by submitting a benign-looking MCP configuration to gain approval, then injecting malicious logic in subsequent updates. The malicious changes took effect silently.

This vulnerability class — dubbed "MCPoison" — affects any MCP client that caches trust decisions without periodic re-validation.

### August 2025 — Filesystem MCP Sandbox Escape

**Attack type**: Sandbox Escape / Path Traversal

Anthropic's official Filesystem MCP Server was supposed to restrict file access to specified directories. Attackers bypassed this restriction using path traversal techniques, gaining read and write access to arbitrary files outside the sandbox.

For context on how Claude Code's own security model handles filesystem access, see the [Claude Code Security deep dive](/posts/ai/2026-02-22-claude-code-security/).

### September 2025 — Postmark MCP Supply Chain Attack

**Attack type**: Supply Chain Attack

A malicious package impersonating the Postmark email service was uploaded to the MCP registry. Developers who installed it received a functional-seeming email MCP server that quietly exfiltrated API keys and environment variables in the background.

This was a classic supply chain attack adapted for the MCP ecosystem — and it worked because the MCP registry lacked adequate vetting of submissions.

### October 2025 — Smithery Path Traversal

**Attack type**: Path Traversal

Smithery, a popular MCP server hosting platform, had a path traversal vulnerability in its isolation layer. Attackers could break out of their container boundary and read Docker credentials and environment variables belonging to other users' MCP deployments.

### January–February 2026 — The CVE Flood

The first two months of 2026 saw an unprecedented wave of MCP CVE filings. Security teams at Check Point, Invariant Labs, Adversa AI, and independent researchers collectively identified and reported dozens of new vulnerabilities. Among the discoveries:

- **Check Point** found that Claude Code itself could be attacked through malicious hooks, MCP configurations, and environment variables. Their research demonstrated attack chains combining multiple MCP weaknesses.
- Multiple MCP servers on popular registries were found to have basic **SSRF vulnerabilities**, allowing attackers to pivot from the MCP server into internal networks.
- Several community-maintained MCP servers were found to use **`eval()` or `exec()`** on unsanitized inputs, creating trivial RCE paths.

For details on Claude Code hooks and how to secure them, see the [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/).

## 3. Five Core Attack Patterns

Analyzing the full CVE dataset reveals five recurring attack patterns. Understanding these patterns is more valuable than memorizing individual CVEs — they represent the structural weaknesses of the MCP ecosystem.

### Pattern 1: Tool Poisoning

**What it is**: Injecting malicious instructions into MCP tool descriptions or metadata. The AI agent reads these descriptions and follows them as if they were legitimate instructions.

**Why it works**: AI agents treat tool descriptions as trusted input. There is no standard mechanism for validating or signing tool descriptions. An attacker who controls (or can modify) a tool description effectively controls the agent's behavior when using that tool.

**Real-world example**: The WhatsApp MCP attack (April 2025) used tool description poisoning to exfiltrate chat histories without any code exploit.

**Defense**: Always review tool descriptions before approving MCP servers. Use `mcp-scan` to detect anomalous tool descriptions. In [Claude Code](/posts/ai/2026-02-28-claude-code-complete-guide/), never auto-approve MCP tools from untrusted sources.

### Pattern 2: Prompt Injection via External Data

**What it is**: Planting malicious prompts in data sources that MCP servers read — GitHub issues, Slack messages, database records, emails, or any other external content.

**Why it works**: MCP servers act as bridges between AI agents and external systems. When an AI agent processes content from these systems, it cannot reliably distinguish between legitimate data and injected prompts. The AI treats all content as context, making it susceptible to instructions embedded in that content.

**Real-world example**: The GitHub MCP prompt injection (May 2025) used public Issues to exfiltrate private repository code.

**Defense**: Treat all external data as untrusted. Implement output filtering on MCP servers. Use structured data formats rather than free text where possible. Consider running MCP operations that process external content in sandboxed environments.

### Pattern 3: Trust Bypass

**What it is**: Exploiting weaknesses in how MCP clients store and validate trust decisions. Once a user approves an MCP server, the attacker modifies the server's behavior knowing it will not be re-checked.

**Why it works**: Most MCP clients implement a "trust on first use" (TOFU) model. The initial approval is thorough, but subsequent changes go unverified. This creates a window where approved servers can be silently compromised.

**Real-world example**: Cursor's MCPoison vulnerability (CVE-2025-54136) exploited exactly this pattern.

**Defense**: Pin MCP server versions. Use hash-based verification for MCP configurations. Periodically re-audit approved servers. Monitor for configuration changes in your MCP setup files.

### Pattern 4: Supply Chain Attack

**What it is**: Publishing malicious MCP servers to registries, either by impersonating legitimate services or by compromising existing packages.

**Why it works**: The MCP registry ecosystem is still maturing. Vetting processes are minimal. Developers often install MCP servers based on name recognition alone, without verifying the publisher's identity or inspecting the source code.

**Real-world example**: The Postmark supply chain attack (September 2025) published a functional but backdoored MCP server to the registry.

**Defense**: Only install MCP servers from verified publishers. Review source code before installation. Use `mcp-scan` to check for known malicious packages. Pin versions and monitor for unexpected updates. For a curated list of vetted MCP servers, see [Best MCP Servers for Claude Code](/posts/ai/2026-03-05-best-mcp-servers-claude-code/).

### Pattern 5: Cross-Tenant Exposure

**What it is**: Exploiting shared infrastructure to access data belonging to other users or organizations.

**Why it works**: Many MCP servers run on shared hosting platforms or process requests from multiple tenants through the same service. If tenant isolation is not properly implemented at every layer — from request handling to data storage — cross-tenant data leaks become possible.

**Real-world example**: The Asana cross-tenant exposure (June 2025) and the Smithery path traversal (October 2025) both demonstrated this pattern.

**Defense**: Run sensitive MCP servers on dedicated infrastructure. Audit the tenant isolation of any shared MCP hosting platform. Avoid passing multi-tenant credentials to MCP servers.

## 4. The OWASP Agentic Security Top 10

In response to the surge of AI agent vulnerabilities — including many MCP-related issues — OWASP published the **Agentic Security Top 10** in late 2025. This framework provides a structured way to think about the risks specific to AI agent systems.

Here is the full list with MCP relevance notes:

| # | Risk | MCP Relevance |
|---|------|---------------|
| 1 | **Prompt Injection** | Direct: tool description poisoning, external data injection |
| 2 | **Broken Access Control** | Direct: cross-tenant exposure, missing auth on 38% of servers |
| 3 | **Tool Misuse** | Direct: agents calling tools with unintended parameters |
| 4 | **Excessive Agency** | Tools granted more permissions than needed |
| 5 | **Improper Output Handling** | MCP servers returning unsanitized data to agents |
| 6 | **Supply Chain Vulnerabilities** | Direct: malicious MCP packages in registries |
| 7 | **Sensitive Data Disclosure** | API keys and credentials leaked via MCP tool calls |
| 8 | **Insecure Interfaces** | MCP transport layer (stdio, SSE) security gaps |
| 9 | **Denial of Service** | MCP servers with no rate limiting or resource caps |
| 10 | **Insufficient Logging** | Most MCP servers have zero audit trail for tool invocations |

The OWASP framework maps almost perfectly to the vulnerabilities we have seen in the MCP ecosystem. Every one of the top 10 risks has at least one confirmed MCP CVE or documented exploit.

For practitioners, the OWASP list serves as an excellent audit checklist. When evaluating an MCP server, walk through each of the 10 categories and ask: "Is this risk mitigated?"

## 5. Security Tools Comparison

The security community has responded to the MCP vulnerability wave with dedicated scanning and auditing tools. Here are the five most significant options available as of March 2026:

### mcp-scan (Invariant Labs)

The most widely adopted MCP security scanner. Open-source, runs locally, and integrates with all major MCP clients.

- **Install**: `uvx mcp-scan` (requires `uv` package manager)
- **What it does**: Reads MCP config files, connects to each server, inspects tool descriptions for poisoning indicators, checks against a known vulnerability database
- **Clients supported**: Claude Code, Claude Desktop, Cursor, Windsurf
- **Strengths**: Fast (under 30 seconds), no configuration needed, community-maintained vulnerability database
- **Limitations**: Focuses on tool-level scanning; does not audit server source code

### SecureClaw (Adversa AI)

An enterprise-grade MCP security platform with 55 distinct audit checks.

- **Type**: Commercial / SaaS
- **What it does**: Deep security audit of MCP servers including SSRF detection, authentication testing, input validation analysis, and compliance reporting
- **Strengths**: Most comprehensive audit coverage, generates executive-ready reports, continuous monitoring mode
- **Limitations**: Enterprise pricing, requires cloud connectivity for full feature set

### agent-audit

An OWASP-aligned auditing tool designed specifically for AI agent security, including MCP.

- **Type**: Open-source
- **What it does**: Maps MCP server configurations against the OWASP Agentic Security Top 10, generates risk scores and remediation guidance
- **Strengths**: Standards-based approach, good for compliance requirements
- **Limitations**: Newer project, smaller vulnerability database than mcp-scan

### Cisco MCP Scanner

A network-level MCP security scanner from Cisco's security research team.

- **Type**: Open-source
- **What it does**: Analyzes MCP traffic patterns, detects anomalous tool calls, monitors for data exfiltration indicators at the network layer
- **Strengths**: Catches attacks that tool-level scanners miss, integrates with existing network security infrastructure
- **Limitations**: Requires network-level access, more complex setup

### Snyk Agent Scan

Snyk's extension of their dependency scanning platform to cover MCP and AI agent dependencies.

- **Type**: Commercial (free tier available)
- **What it does**: Scans MCP server dependencies for known vulnerabilities, monitors for supply chain attacks, integrates with CI/CD pipelines
- **Strengths**: Leverages Snyk's massive vulnerability database, familiar workflow for teams already using Snyk
- **Limitations**: Focused on dependency-level vulnerabilities, does not scan tool descriptions or runtime behavior

### Tools Comparison Matrix

| Feature | mcp-scan | SecureClaw | agent-audit | Cisco Scanner | Snyk Agent |
|---------|----------|------------|-------------|---------------|------------|
| **Price** | Free | Enterprise | Free | Free | Freemium |
| **Tool poisoning detection** | Yes | Yes | Partial | No | No |
| **Dependency scanning** | No | Yes | No | No | Yes |
| **OWASP mapping** | No | Yes | Yes | No | No |
| **Network analysis** | No | No | No | Yes | No |
| **CI/CD integration** | Basic | Yes | No | Yes | Yes |
| **Setup time** | < 1 min | Hours | Minutes | Hours | Minutes |
| **Best for** | Individual devs | Enterprises | Compliance | SOC teams | Dev teams |

**Recommendation**: Start with `mcp-scan` for immediate visibility. Add Snyk Agent Scan if you need dependency chain monitoring. Consider SecureClaw for enterprise environments with compliance requirements.

## 6. Practical Defense Checklist

Based on the vulnerability patterns and available tools, here is a prioritized defense checklist for anyone running MCP servers.

### Priority 1 — Do This Today

These actions address the most common and severe vulnerability patterns. They require minimal effort and provide immediate protection.

- [ ] **Run `mcp-scan`** on your current MCP configuration. Fix any findings before proceeding.
- [ ] **Pin MCP server versions**. Never use `@latest` in production. Specify exact versions: `npx @package/name@2.1.3`.
- [ ] **Review tool descriptions** for every MCP server you have approved. Look for unusual instructions, URLs, or references to sensitive data.
- [ ] **Remove unused MCP servers**. Every server you are not actively using is unnecessary attack surface. Run `claude mcp list` and remove anything dormant.
- [ ] **Check authentication**. For every MCP server that accesses external services, verify that credentials use the minimum necessary permissions. Rotate any credentials that have been shared broadly.

### Priority 2 — Do This Week

These actions require more planning but address significant risks.

- [ ] **Implement permission boundaries**. In Claude Code, use the permission system to restrict which MCP tools can be called without explicit approval. See [Claude Code MCP Setup](/posts/ai/2026-02-28-claude-code-mcp-setup/) for configuration details.
- [ ] **Audit MCP server sources**. For each server, verify the publisher identity, check the GitHub repository for recent activity and maintainer reputation, and review open issues for security reports.
- [ ] **Set up monitoring**. Log all MCP tool invocations. At minimum, capture the tool name, input parameters, and timestamp. This provides an audit trail for incident response.
- [ ] **Separate sensitive operations**. If an MCP server handles both read and write operations, consider whether you can restrict it to read-only mode for your use case.
- [ ] **Review hooks and environment variables**. Following the Check Point findings, audit your Claude Code hooks and ensure no MCP server has access to sensitive environment variables. See the [Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) for details.

### Priority 3 — Ongoing Practices

These are habits that maintain security over time.

- [ ] **Schedule regular scans**. Run `mcp-scan` weekly or add it to your CI pipeline.
- [ ] **Subscribe to MCP security advisories**. Follow the MCP GitHub repository and NVD alerts for new CVEs.
- [ ] **Test MCP servers in isolation**. Before adding a new MCP server to your workflow, test it in a sandboxed environment first.
- [ ] **Contribute findings**. If you discover a vulnerability, report it through responsible disclosure channels. The MCP ecosystem benefits from community security research.
- [ ] **Stay updated on protocol changes**. The MCP specification is evolving rapidly. New versions may introduce security improvements (or new attack surfaces).

## 7. How to Scan Your MCP Setup Now

Here is a step-by-step guide to scanning your MCP configuration with `mcp-scan`, the most accessible tool available.

### Prerequisites

You need Python 3.10+ and the `uv` package manager:

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

### Running Your First Scan

```bash
# Navigate to your project directory (or any directory)
cd ~/your-project

# Run mcp-scan — it auto-detects your MCP configuration
uvx mcp-scan
```

The tool automatically finds MCP configuration files for Claude Code, Claude Desktop, Cursor, and Windsurf. It connects to each configured server, retrieves tool listings, and runs its analysis.

### Understanding the Output

A typical scan produces output like this:

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

### Acting on Results

- **❌ Critical findings**: Address immediately. Remove or update the affected server before continuing to use it.
- **⚠️ Warnings**: Schedule for resolution within the week. Version pinning and updates are quick fixes.
- **✅ Clean**: Good, but re-scan periodically. New vulnerabilities are discovered regularly.

### Automating Scans

Add `mcp-scan` to your development workflow:

```bash
# Add to a pre-commit hook or CI step
uvx mcp-scan --format json > mcp-scan-results.json

# Fail CI if critical issues are found
uvx mcp-scan --exit-code
```

The `--exit-code` flag returns a non-zero exit code when critical vulnerabilities are found, making it suitable for CI/CD gate checks.

## 8. Looking Ahead: What Comes Next

The MCP security landscape is evolving rapidly. Several developments are worth watching:

**Protocol-level improvements**: The MCP specification team is working on built-in authentication standards, tool description signing, and server attestation. These changes could address the root causes of tool poisoning and supply chain attacks at the protocol level rather than relying on external tools.

**Registry vetting**: Major MCP registries are implementing publisher verification and automated security scanning for submitted servers. This should reduce (but not eliminate) supply chain risks.

**Client-side defenses**: AI coding tools are adding more granular permission controls. Claude Code already requires explicit approval for MCP tool calls, and the [hooks system](/posts/ai/2026-02-28-claude-code-hooks-guide/) provides additional control points. Expect other clients to follow.

**Enterprise adoption blockers**: The current security posture of the MCP ecosystem is a significant barrier to enterprise adoption. Organizations with strict security requirements are waiting for the maturity that signed tools, verified registries, and standardized audit frameworks will bring.

The 30 CVEs in 60 days were a wake-up call. The MCP community is responding, but it will take months for the ecosystem to reach the security baseline that production deployments require. In the meantime, the defense checklist above is your best protection.

## 9. FAQ

**Q: Can I use MCP servers safely in production right now?**

Yes, with significant caveats. Pin versions, scan regularly, use minimal permissions, and only install servers from trusted, verified sources. The risk is manageable but not negligible.

**Q: My organization requires SOC 2 compliance. Can we use MCP?**

Not without additional controls. You will need comprehensive logging of all MCP tool invocations, regular vulnerability scanning, access controls, and an incident response plan specific to MCP-related threats. SecureClaw and agent-audit can help with the compliance mapping.

**Q: Is stdio transport more secure than SSE?**

Generally yes. Stdio transport runs locally and does not expose a network endpoint. SSE (Server-Sent Events) transport requires proper authentication, TLS, and network access controls. If you do not need remote MCP servers, prefer stdio.

**Q: How does Claude Code protect against MCP attacks?**

Claude Code implements several layers of protection: explicit permission prompts for all MCP tool calls, a hooks system for custom validation, and sandboxed execution environments. For a complete analysis, read the [Claude Code Security guide](/posts/ai/2026-02-22-claude-code-security/).

**Q: Should I build my own MCP servers or use community ones?**

Both approaches have trade-offs. Custom servers give you full control but require you to handle security yourself. Community servers benefit from broader testing but introduce supply chain risk. For critical operations, custom servers with security audits are safer. For general-purpose tools, vetted community servers from the [curated list](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) are reasonable.

## 10. Related Reading

- [MCP Protocol Explained: The Complete Technical Guide](/posts/ai/2026-02-28-mcp-protocol-explained/) — Understand how MCP works before securing it
- [Claude Code Complete Guide](/posts/ai/2026-02-28-claude-code-complete-guide/) — Master the AI coding tool that uses MCP
- [Claude Code Security Deep Dive](/posts/ai/2026-02-22-claude-code-security/) — How Claude Code protects against the attacks described here
- [Claude Code MCP Setup Guide](/posts/ai/2026-02-28-claude-code-mcp-setup/) — Configure MCP servers securely in Claude Code
- [Best MCP Servers for Claude Code](/posts/ai/2026-03-05-best-mcp-servers-claude-code/) — Vetted, safe MCP servers you can trust
- [Claude Code Hooks Guide](/posts/ai/2026-02-28-claude-code-hooks-guide/) — Use hooks to add custom security controls to MCP operations
