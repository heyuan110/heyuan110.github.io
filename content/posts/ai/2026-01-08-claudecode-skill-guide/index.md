+++
date = '2026-01-08T10:00:00+08:00'
title = 'Claude Code Skills Guide: Teach AI Your Exact Workflow'
description = 'Learn how to create Claude Code Skills with three practical examples: financial reporting, interview question generation, and Amazon listing optimization.'
toc = true
tags = ['AI', 'Claude Code', 'Skills', 'Productivity']
categories = ['AI Guides']
keywords = ['Claude Code Skills tutorial', 'SKILL.md guide', 'Claude Code custom skills', 'AI workflow automation', 'how to create Claude Code Skill']
+++
![Skill Guide](skill-guide.webp)

## Why Skills Matter

In the age of LLMs, everyone wants AI that understands their specific work. The problem is that AI is general-purpose. It does not know your company's report format, your hiring criteria, or your product's unique selling points.

Explaining everything from scratch every time is exhausting.

Claude Code Skills solve this problem: **you package your domain expertise into a set of instructions that Claude learns once and follows every time**.

Put simply:

> **A Skill is an instruction manual that teaches Claude how to do your job the way you do it.**

No coding required. You just need to clearly describe: what to do, how to do it, and what to watch out for.

## What Exactly Is a Skill?

### It Is Just a Markdown File

A Skill is not some complex technology. It is a folder containing a single `SKILL.md` file.

This file tells Claude:

- What this skill is called
- When to use it
- How to execute it
- What pitfalls to avoid

Here is a minimal example:

```markdown
---
name: daily-report
description: Generate a structured daily work report
---

# Daily Report Generator

## Task
Generate a well-formatted daily report based on work items provided by the user.

## Output Format
1. Completed today
2. Planned for tomorrow
3. Items needing coordination

## Guidelines
- Keep each item under 20 words
- Sort by priority
```

That is all it takes. Once Claude reads this file, it "knows" how your team writes daily reports.

### Where to Put the Files

Skill folders go inside the `.claude/skills/` directory:

```
.claude/
└── skills/
    └── daily-report/
        └── SKILL.md
```

You can place them in a project directory (scoped to that project) or in `~/.claude/skills/` (available across all projects).

### Skills vs Slash Commands

Many people confuse these two. Here is the difference:

| Feature | Skill | Slash Command |
|---------|-------|---------------|
| Location | `.claude/skills/` | `.claude/commands/` |
| Trigger | Claude auto-detects | User types `/command` |
| Best for | Complex workflows, automatic recognition | Simple operations, manual trigger |
| Structure | Folder + SKILL.md | Single .md file |

**The rule of thumb**:
- Want Claude to decide when to use it automatically? Create a Skill.
- Want to trigger it manually? Create a Slash Command.

## When Should You Use a Skill?

Not every scenario needs a Skill. These are the best use cases:

### Repetitive Workflows

Weekly reports, recurring approval processes, documents that always follow the same template.

### Domain-Specific Knowledge

Your industry has specialized terminology, specific standards, or professional requirements that Claude needs to learn.

### Fixed Output Formats

The output must match a company template, include specific fields, or follow a particular structure.

### Team Standardization

Multiple team members use Claude but need consistent output. Put the Skill in the project repo so everyone shares it.

## Three Practical Examples

Theory only gets you so far. Here are three ready-to-use examples you can copy directly.

### Example 1: Finance - Monthly Financial Report

**Scenario**: Every month you receive financial data (revenue, expenses, profit) and need to generate an analysis report.

**Create the Skill**:

```bash
mkdir -p .claude/skills/finance-report
```

**SKILL.md contents**:

````markdown
---
name: finance-report
description: Analyze financial data and generate a monthly report with KPIs, YoY/MoM comparisons, anomaly alerts, and recommendations
---

# Monthly Financial Report Skill

## Overview

Generate a structured monthly financial analysis report from user-provided data.

## Input Requirements

The user should provide the following (as tables, text, or screenshots):
- Current month revenue breakdown
- Current month expense breakdown
- Previous month / same period last year data (for comparison)

## Analysis Framework

### 1. Key Metrics Overview
- Total revenue, total expenses, net profit
- Gross margin, net margin
- Revenue composition by segment

### 2. Year-over-Year and Month-over-Month Analysis
- Compare with previous month (MoM)
- Compare with same period last year (YoY)
- Flag growth/decline percentages

### 3. Anomaly Alerts
- Any single expense exceeding budget by 20%+
- Revenue decline exceeding 10% in any business line
- Profit margins below industry average

### 4. Recommendations
- Provide 2-3 actionable recommendations based on data
- Be specific, not generic

## Output Format

```
# [Month] Financial Analysis Report

## 1. Key Metrics
| Metric | This Month | Last Month | MoM | Last Year | YoY |
|--------|-----------|------------|-----|-----------|-----|
| Revenue | xxx | xxx | +x% | xxx | +x% |
| ... | ... | ... | ... | ... | ... |

## 2. Revenue Structure Analysis
[Charts or descriptions]

## 3. Expense Analysis
[Key expense items analysis]

## 4. Anomaly Alerts
- [Anomaly item 1]
- [Anomaly item 2]

## 5. Recommendations
1. [Specific recommendation 1]
2. [Specific recommendation 2]
```

## Guidelines

- Round all numbers to 2 decimal places
- Use +/- signs for percentage changes
- Highlight anomalies clearly
- Base all recommendations on actual data
````

**How to use it**:

Drop your financial data (Excel screenshot, text, CSV) into Claude. It will automatically recognize the Skill and generate the report in the correct format.

---

### Example 2: HR - Interview Question Generation

**Scenario**: An HR manager receives a job description and needs to quickly generate targeted interview questions.

**Create the Skill**:

```bash
mkdir -p .claude/skills/interview-questions
```

**SKILL.md contents**:

````markdown
---
name: interview-questions
description: Generate structured interview questions from a job description, covering technical skills, soft skills, and culture fit
---

# Interview Question Generator Skill

## Overview

Automatically generate a structured set of interview questions from a job description (JD) to help interviewers evaluate candidates comprehensively.

## Input Requirements

The user provides:
- Job title
- Job responsibilities
- Requirements/qualifications
- (Optional) Company culture / team characteristics

## Question Generation Framework

### 1. Technical Competency (3-5 questions)

Design questions targeting the core skills listed in the JD.

Format per question:
- The question
- What it assesses
- Key points in an excellent answer

### 2. Project Experience (2-3 questions)

Use the STAR method to evaluate real project experience.

- Situation: What was the context
- Task: What was the assignment
- Action: What did they do
- Result: What was the outcome

### 3. Soft Skills (2-3 questions)

Assess communication, collaboration, and resilience.

### 4. Culture Fit (1-2 questions)

Evaluate alignment with company values and career goals.

## Output Format

```
# [Job Title] Interview Question Sheet

## Section 1: Technical Competency (Weight: 40%)

### Q1: [Question]
- Assesses: xxx
- Strong answer includes: xxx
- Follow-up: xxx

### Q2: [Question]
...

## Section 2: Project Experience (Weight: 30%)

### Q1: Describe a project you led in [relevant domain]
- Assesses: Project management, technical depth
- Follow-ups:
  - What was the biggest challenge?
  - What would you do differently?

## Section 3: Soft Skills (Weight: 20%)

### Q1: [Question]
...

## Section 4: Culture Fit (Weight: 10%)

### Q1: [Question]
...

---
Scoring guide:
- Rate each question 1-5
- Final score = weighted average
- Recommended hire threshold: 3.5+
```

## Guidelines

- Questions must be specific (avoid vague questions like "How would you describe yourself?")
- Always include follow-up directions for the interviewer
- Adjust weights based on role requirements
- Avoid legally prohibited questions (age, marital status, religion, etc.)
````

**How to use it**:

Send a JD to Claude and say "generate interview questions for this role." It will automatically follow this framework.

---

### Example 3: Amazon Operations - Listing Optimization (Professional)

**Scenario**: An Amazon seller needs to optimize a product listing to improve search ranking and conversion rate. This is not simple copywriting polish -- it is systematic optimization based on algorithm rules and competitor analysis.

**Create the Skill**:

```bash
mkdir -p .claude/skills/amazon-listing-pro
```

**SKILL.md contents**:

````markdown
---
name: amazon-listing-pro
description: Expert in Amazon A9/COSMO/Rufus algorithms. Generate high-converting listing copy based on competitor analysis and keyword data
---

# Amazon Listing Professional Optimization Skill

## Role

You are a Listing optimization expert with deep knowledge of Amazon's algorithms (A9, COSMO, Rufus) and a strong compliance mindset.

## Input Requirements

The user should provide as much of the following as possible (missing data reduces optimization quality):

### Required
1. **Product attribute sheet**: All specific parameters (dimensions, materials, weight, colors, features, etc.)
2. **Target marketplace**: US, EU, Japan, etc.

### Strongly Recommended
3. **Competitor keyword reports**: Traffic source analysis (exported from Helium10, JungleScout, etc.)
4. **ABA keyword data**: Amazon Brand Analytics data for keyword weighting
5. **Competitor listing text**: Copy from top competitors plus Review pros/cons summary

## Workflow

### Step 1: Multi-dimensional Data Analysis

#### 1.1 Rufus Attribute Extraction
Read the product attribute sheet thoroughly and extract all parameters as the **factual foundation** of the Listing. Every claim must be grounded in real attributes -- never fabricate.

#### 1.2 Competitor Landscape Analysis

**Find Parity**:
- Identify selling points that all competitors emphasize
- These are market standards we must cover
- Example: waterproof, durable, eco-friendly materials

**Find Gaps**:
- Spot scenarios that competitors consistently overlook
- Analyze recurring pain points across Reviews
- These are our core differentiation opportunities
- Example: complaints about flimsy packaging, unclear instructions

#### 1.3 COSMO Scene Mapping
Cross-reference competitor keyword reports to identify the real-world usage scenarios customers care about most.

#### 1.4 A9 Keyword Tiering
Based on ABA keyword data, classify keywords into:
- **S-tier**: Top 3 search volume, must appear in the first 80 characters of the title
- **A-tier**: Top 10 search volume, in the title or first bullet point
- **B-tier**: Long-tail keywords, distributed across bullet points and description
- **C-tier**: Synonyms/variants, placed in backend Search Terms

### Step 2: Write the Listing

#### 2.1 Title

**Formula**: [Brand] + [Top ABA keyword] + [Key improvement addressing competitor pain point] + [COSMO scenario] + [Specifications]

**Rules**:
- US marketplace limit: 200 characters, aim for 150-180
- First 80 characters must contain the highest-weight keywords
- Title case (except prepositions)
- No special symbols (hyphens allowed)
- Differentiate from competitors explicitly (e.g., instead of "durable," say "20% thicker double-layer design")

#### 2.2 Bullet Points

**Approach**: 5-point structure that leverages our strengths against common competitor weaknesses.

**Format**: Each bullet starts with an ALL-CAPS phrase header

**Structure**:
- **Point 1 - Pain Point Strike**: Directly address common competitor shortcomings
- **Point 2 - Scene Immersion**: Describe COSMO scenarios competitors underserve
- **Point 3 - Hard Specs**: Reference specific data from the attribute sheet for Rufus
- **Point 4 - Target Audience**: Define ideal users, mention gifting scenarios
- **Point 5 - Trust & Support**: Return policy, brand guarantees

**Length**: 200-250 characters per bullet

#### 2.3 Product Description

**Format**: HTML layout including:
- Brief brand story
- Detailed specifications table
- FAQ section (specifically addressing common competitor negative reviews)

**HTML template**:
```html
<h3>Why Choose [Brand]?</h3>
<p>[Brand differentiation description]</p>

<h3>Specifications</h3>
<ul>
<li><b>Material:</b> [material]</li>
<li><b>Dimensions:</b> [dimensions]</li>
<li><b>Weight:</b> [weight]</li>
</ul>

<h3>FAQ</h3>
<p><b>Q: [Question addressing competitor pain point]?</b></p>
<p>A: [Our solution]</p>
```

#### 2.4 Backend Search Terms

**Rules**:
- Total character count must not exceed 249
- Do not repeat words already used in the title and bullets
- Space-separated, no commas
- Include: synonyms, spelling variants, Spanish keywords (for US marketplace)
- Never include competitor brand names

### Step 3: Compliance Check

**Complete these checks before final output**:

#### 3.1 Promotional Language Check
Scan and remove: Best seller, #1, Top rated, Free shipping, On sale, Limited time, Guarantee, etc.

#### 3.2 Infringement Check
Scan and replace: Competitor brand names, patented terms, unauthorized certifications (e.g., "FDA approved")

#### 3.3 Exaggeration Check
Verify all parameter claims come from the product attribute sheet. Do not fabricate features.

#### 3.4 Amazon Format Rules
- No emojis in listings
- No HTML tags in bullet points (HTML is for Description only)
- No full-width characters

## Output Format

```
# [Product Name] Listing Optimization Plan

## 1. Optimized Title
[Title content]
(Character count: xxx/200)

## 2. Bullet Points

1. [PAINPOINT SOLUTION] [Description]
2. [PERFECT FOR] [Description]
3. [PREMIUM QUALITY] [Description]
4. [IDEAL GIFT] [Description]
5. [WORRY-FREE] [Description]

## 3. Product Description (HTML)
[HTML code]

## 4. Backend Search Terms
[Keyword list]
(Character count: xxx/249)

## 5. Competitor Analysis Insights

### Common Competitor Weaknesses:
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

### Our Targeted Improvements:
- For weakness 1: [Our solution]
- For weakness 2: [Our solution]
- For weakness 3: [Our solution]

### Keyword Strategy:
- S-tier: [keyword 1], [keyword 2]
- A-tier: [keyword 1], [keyword 2], [keyword 3]
- Key differentiator: [core differentiation point]
```

## Constraints

1. **Factual accuracy**: Never fabricate features not in the product attribute sheet
2. **Compliance first**: Compliance checks have the highest priority; any violation must be corrected
3. **Holistic view**: Learn from all competitors' strengths, avoid their shared weaknesses -- do not copy any single competitor
4. **Data-driven**: All decisions must be grounded in provided data, never assume market conditions
````

**How to use it**:

Prepare your product attribute sheet and competitor data, then tell Claude: "Optimize this product's Amazon Listing."

The more complete your data, the better the output. With just a product attribute sheet, Claude will optimize using general best practices. With competitor analysis data, it will craft precisely targeted differentiation.

## How to Create Your Own Skill

After seeing the examples, you should realize that creating a Skill is straightforward.

**Four-step process**:

### Step 1: Create the Directory

```bash
mkdir -p .claude/skills/your-skill-name
```

### Step 2: Write SKILL.md

Every SKILL.md should include:

```markdown
---
name: skill-name          # Required, English, use hyphens
description: One-line summary  # Required, tells Claude when to use it
---

# Title

## Overview
What this Skill does

## Input Requirements
What the user needs to provide

## Execution Steps
How to do it

## Output Format
What the result looks like

## Guidelines
What pitfalls to avoid
```

### Step 3: Test

Run it in Claude Code with real input and check whether the output matches your expectations.

### Step 4: Iterate

Refine the SKILL.md based on actual usage. Skills improve as you sharpen the instructions.

**Best practices**:

- Keep SKILL.md between 500-2000 words. Too long and Claude may lose focus on the key points.
- Concrete examples work far better than abstract descriptions.
- The clearer your output format template, the more precisely Claude will follow it.
- In the guidelines section, document specific pitfalls you have encountered -- not vague advice like "be careful."

**Common mistakes**:

- Forgetting the `name` and `description` fields, so Claude does not know when to activate the Skill.
- Vague instructions like "make it more professional" -- define what "professional" means specifically.
- Not providing an output format template, leading to inconsistent results across runs.

## Final Thoughts

At its core, a Skill is your domain expertise turned into structured instructions.

Ten years of financial analysis experience, knowing how to read reports and spot anomalies -- write that down and it becomes a Skill.

Five years of recruiting, knowing which questions reveal real talent -- write that down and it becomes a Skill.

Three years on Amazon, understanding A9 algorithm rules and competitor analysis frameworks -- write that down and you get something like Example 3.

**AI will not replace experts, but it will replace experts who do not know how to use AI.**

A Skill is the simplest way to teach AI your expertise. No code to write, no model to train -- just document your experience as an instruction manual.

Give it a try.

## Related Reading

- [Claude Code Browser Automation: Agent Browser vs Playwright vs DevTools](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [Claude Code Best Practices Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Claude Code Skill Advanced Patterns](/posts/ai/2026-01-12-claudecode-skill-patterns/)
- [Agent Skills: A New Paradigm for AI Programming](/posts/ai/2026-01-19-agent-skills-new-programming/)
