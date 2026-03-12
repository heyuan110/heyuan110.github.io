+++
date = '2026-01-14T14:38:00+08:00'
title = 'Claude Code Complete Guide: From Beginner to Power User'
description = 'Master Claude Code, Anthropic official CLI tool. Learn installation, CLAUDE.md setup, Skills, Subagents, MCP integration, and advanced workflows for developers and non-technical users.'
toc = true
tags = ['Claude Code', 'AI Tools', 'Anthropic', 'CLI Tools', 'Productivity', 'Automation']
categories = ['AI Guides']
keywords = ['Claude Code guide', 'Claude Code tutorial', 'Anthropic CLI tool', 'AI coding assistant', 'Claude Code setup', 'Claude Code tips', 'Claude Code CLAUDE.md', 'Claude Code MCP']
+++

![Claude Code terminal AI assistant](cover.webp)

Have you ever wished for an AI assistant that could actually *do things* — not just give advice, but directly edit files, run commands, and handle repetitive tasks? **Claude Code** is exactly that. Built by Anthropic, it runs in your terminal as a fully agentic AI assistant that understands your needs and takes action.

**It's not just for programmers.** While Claude Code excels at coding, it can also help product managers organize documentation, assist ops engineers with log analysis, help admin staff process data reports, and automate tedious repetitive work for anyone.

Whether you're a senior developer, product manager, DevOps engineer, or office administrator, this guide will take you from zero to proficient with Claude Code.

## What Is Claude Code?

### Core Concept

**Claude Code** is Anthropic's official command-line tool (CLI) — an agentic AI tool that runs directly in your terminal.

Unlike ordinary AI chat, Claude Code's defining feature is: **it can execute actions directly**.

| Feature | Description |
|---------|-------------|
| Terminal-native | Not a chat window or IDE plugin — a command-line tool |
| Action-capable | Can directly edit files, run commands, process data |
| Context-aware | Automatically analyzes project structure and file contents |
| Natural language | Describe what you need in plain English, Claude implements it |

**A simple analogy**: If ChatGPT is a "consultant" who only gives advice, Claude Code is an "assistant" who can actually get things done.

### What Can It Do?

Claude Code solves four major categories of problems:

**Build features**: Tell Claude what you want to build, and it will plan, write code, and make sure it runs.

```bash
# Example: Ask Claude to build a user registration feature
claude "Build a user registration endpoint with email verification"
```

**Example conversation**:

```
You: Build a user registration endpoint with email verification

Claude: I'll help you implement that. Let me first understand the project structure...

[Claude automatically analyzes the project]

I can see this is an Express + MongoDB project. I'll:
1. Create an auth.js route in routes/
2. Create a User model in models/
3. Implement email verification code sending
4. Add necessary input validation

Starting implementation...

[Claude automatically creates files and writes code]

Done! I've created these files:
- routes/auth.js - Registration and verification endpoints
- models/User.js - User model
- utils/email.js - Email sending utility

Want to test it? Run npm run dev and hit POST /api/auth/register
```

**Debug and fix**: Describe a bug or paste an error message, and Claude will analyze the codebase, locate the issue, and implement a fix.

```bash
# Example: Ask Claude to fix a bug
claude "What does this error mean? Fix it: TypeError: Cannot read property 'map' of undefined"
```

**Code navigation**: Ask anything about your codebase, and Claude will find the answer.

```bash
# Example: Understand code structure
claude "Where is the authentication logic implemented in this project?"
```

**Automation**: Fix lint issues, resolve merge conflicts, generate release notes, and handle other tedious tasks.

```bash
# Example: Auto-fix code style issues
claude "Fix all ESLint errors"
```

### Beyond Coding: Non-Technical Use Cases

Claude Code's capabilities extend well beyond programming. At its core, it's an intelligent assistant that can manipulate files and execute commands:

**Document processing**: Organize, convert, and batch-process documents.

```
You: Convert all Word documents in the docs folder to PDF

Claude: Let me check what documents are in the folder...

[Claude lists files]

Found 15 Word documents. I'll use LibreOffice for conversion...

[Claude runs conversion]

All done! 15 PDFs saved to docs/pdf/.
```

**Data analysis**: Process Excel and CSV data, generate statistical reports.

```
You: Analyze the sales data in sales.csv, find the best-selling products

Claude: Let me read and analyze this data file...

[Claude reads data]

Analysis results:
Data overview: 1,234 sales records across 45 products

Top 5 by sales volume:
1. Wireless Mouse - 892 units, $8,920 revenue
2. Mechanical Keyboard - 654 units, $13,080 revenue
3. USB Hub - 543 units, $5,430 revenue
...

Want me to generate a detailed analysis report?
```

**File organization**: Automatically classify, rename, and archive files.

**Information extraction**: Extract data from web pages and documents into structured formats.

### Who Is It For?

Claude Code lowers the technical barrier, benefiting people with different backgrounds:

| Role | Use Cases | Example |
|------|-----------|---------|
| **Software Engineers** | Write code, fix bugs, refactor, code review | "Refactor this class into a functional component" |
| **Product Managers** | Validate ideas, understand technical implementation | "Is this feature technically feasible? What files need to change?" |
| **DevOps Engineers** | Write scripts, automate operations tasks | "Write a script to monitor server CPU and alert if it exceeds 80%" |
| **Tech Leads** | Understand the codebase, review team work | "What core logic changed in this sprint? Any risk areas?" |
| **QA Engineers** | Write test cases, analyze test coverage | "Add boundary test cases for this payment module" |
| **Non-Technical Staff** | Learn programming, automate simple tasks | "Write a Python script to auto-organize my downloads folder daily" |

### Comparison with Other AI Coding Tools

| Feature | Claude Code | GitHub Copilot | Cursor | ChatGPT |
|---------|-------------|----------------|--------|---------|
| Environment | Terminal | IDE plugin | Standalone IDE | Web/App |
| Execute actions | Yes | No | Yes | No |
| Project understanding | Entire codebase | Current file | Entire codebase | Requires pasting |
| Git operations | Direct execution | No | Partial | No |
| Run commands | Yes | No | Yes | No |
| Pricing | Pro subscription | $10/mo | $20/mo | Plus $20/mo |

## How to Install Claude Code

### Prerequisites

Before starting, you need:

- **Claude subscription**: Pro ($20/mo), Max ($100/mo), Teams, or Enterprise
- Or a **Claude API account**: Pay-per-token usage

**System requirements**:

| OS | Version |
|----|---------|
| macOS | 10.15 (Catalina) or later |
| Linux | Ubuntu 20.04+ / Debian 10+ |
| Windows | Windows 10+ (requires WSL or Git Bash) |

### Installation Methods

**Method 1: macOS / Linux / WSL (Recommended)**

Open your terminal and run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

After installation, reload your shell config:

```bash
# For Bash users
source ~/.bashrc

# For Zsh users
source ~/.zshrc
```

**Method 2: macOS via Homebrew**

```bash
# Install
brew install --cask claude-code

# Update
brew upgrade --cask claude-code
```

**Method 3: Windows PowerShell**

Open PowerShell as administrator:

```powershell
irm https://claude.ai/install.ps1 | iex
```

**Method 4: Windows via WinGet**

```powershell
# Install
winget install Anthropic.ClaudeCode

# Update
winget upgrade Anthropic.ClaudeCode
```

**Method 5: npm (Deprecated, not recommended)**

```bash
# Requires Node.js 18+
npm install -g @anthropic-ai/claude-code
```

### Verify Installation

```bash
# Check version
claude --version

# Run diagnostics (highly recommended)
claude doctor
```

`claude doctor` automatically detects and provides fixes for:

- Node.js version compatibility
- Environment variable configuration
- Network connectivity
- Authentication status

**Example output**:

```
Claude Code Doctor
==================

✅ Node.js version: 20.10.0 (required: >= 18.0.0)
✅ npm version: 10.2.3
✅ Claude Code version: 1.0.25
✅ Authentication: Logged in as user@example.com
✅ API connection: OK (latency: 156ms)
⚠️ Git: Not in a git repository

All checks passed! Claude Code is ready to use.
```

### First Login

After installation, navigate to your project directory and launch Claude Code:

```bash
cd your-project
claude
```

The first run will automatically open your browser for authentication:

```
Welcome to Claude Code!

Opening browser for authentication...
Please log in with your Anthropic account.

Waiting for authentication... ✓

Successfully authenticated as: user@example.com
Subscription: Claude Pro

You're all set! Type your request or /help for commands.

>
```

### Using an API Key (Optional)

If you prefer not to use browser login:

```bash
# Set environment variable
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# Or specify at launch
claude --api-key sk-ant-xxxxxxxxxxxxx
```

**Getting an API key**:

1. Visit [console.anthropic.com](https://console.anthropic.com)
2. Log in to your account
3. Go to the API Keys page
4. Create a new key and copy it

## Basic Usage Guide

### Launch Modes

Claude Code offers multiple launch modes for different scenarios:

```bash
# Mode 1: Interactive conversation (most common)
claude

# Mode 2: Launch with an initial question
claude "What does this project do?"

# Mode 3: One-shot query mode (exits after completion)
claude -p "Generate API documentation"

# Mode 4: Continue last conversation
claude -c
# or
claude --continue

# Mode 5: Resume a specific session
claude --resume
```

**Mode comparison**:

| Launch Mode | Best For | Saves History |
|-------------|----------|---------------|
| `claude` | Daily development, codebase exploration | Yes |
| `claude "question"` | Quick questions with continued conversation | Yes |
| `claude -p "question"` | Automation scripts, CI/CD | No |
| `claude -c` | Continuing yesterday's work | Yes |
| `claude --resume` | Switching between different task conversations | Yes |

### Slash Commands

In interactive mode, use slash commands:

| Command | Function | When to Use |
|---------|----------|-------------|
| `/help` | Show help information | When you forget a command |
| `/clear` | Clear conversation history | When starting a new task |
| `/compact` | Compress conversation history | When long conversations affect performance |
| `/exit` | Exit Claude Code | When finished working |
| `/status` | Show account status | Check subscription info |
| `/cost` | Show token usage | Monitor consumption |
| `/config` | Configuration settings | Modify default behavior |
| `/init` | Initialize project | Create CLAUDE.md for a new project |
| `/memory` | Edit project memory | Modify CLAUDE.md |
| `/permissions` | Manage tool permissions | Authorize or restrict operations |
| `/bug` | Report a bug | When you find an issue |

### File References

Use the `@` symbol to reference files or directories, focusing Claude on specific code:

```bash
# Reference a single file
claude "Optimize the performance of @./src/utils/auth.js"

# Reference multiple files
claude "Compare the differences between @./src/old-api.js and @./src/new-api.js"

# Reference an entire directory
claude "Analyze code quality in all components under @./src/components"

# Reference specific file types
claude "Check coverage for @./src/**/*.test.js test files"
```

### Execute Shell Commands

Use the `!` prefix to execute shell commands within a conversation:

```bash
# Inside Claude Code conversation
!git status
!npm run test
!docker ps
!ls -la src/
```

### Model Selection

Choose the right model based on task complexity:

```bash
# Sonnet (daily tasks, fast, cost-effective)
claude --model sonnet

# Opus (complex tasks, more powerful, higher cost)
claude --model opus

# Haiku (simple tasks, fastest, cheapest)
claude --model haiku
```

**Model selection guide**:

| Model | Best For | Speed | Cost |
|-------|----------|-------|------|
| **Haiku** | Simple Q&A, code completion, formatting | Fastest | Lowest |
| **Sonnet** | Daily development, bug fixes, code review | Fast | Medium |
| **Opus** | Complex architecture design, large-scale refactoring | Slower | Higher |

### Useful Keyboard Shortcuts

| Shortcut | Function |
|----------|----------|
| `Tab` | Auto-complete file paths |
| `Ctrl+C` | Interrupt current operation |
| `Ctrl+D` | Exit Claude Code |
| `Up` / `Down` | Browse command history |
| `#` | Quick-add instructions to CLAUDE.md |
| `Esc` | Cancel current input |
| `Esc Esc` | Interrupt Claude and explore alternatives |

## CLAUDE.md: The Project Memory File

### What Is CLAUDE.md?

`CLAUDE.md` is a special Markdown file that Claude Code automatically reads on every startup. Think of it as a "project handbook" or "AI assistant's onboarding document."

**Why do you need it?**

LLMs are stateless — every conversation starts from a blank slate. `CLAUDE.md` acts as Claude's "onboarding material," helping it quickly understand your project.

Through this file, you can:

- Define the tech stack and architecture
- Set code style guidelines and naming conventions
- Specify common commands and development workflows
- Document project-specific conventions and caveats
- Restrict files or directories from modification

### File Locations and Priority

`CLAUDE.md` can be placed in multiple locations. Claude merges them by priority:

| Location | Scope | Commit to Git? |
|----------|-------|----------------|
| `~/.claude/CLAUDE.md` | Global, all projects | No |
| Project root `CLAUDE.md` | Current project, team-shared | Yes (recommended) |
| Project root `CLAUDE.local.md` | Current project, personal config | No |
| Subdirectory `CLAUDE.md` | Specific directory | Case by case |

**Example setup**:

```
~/.claude/CLAUDE.md          # Your global preferences: language, code style
project/CLAUDE.md            # Project rules: team conventions, tech stack, commands
project/CLAUDE.local.md      # Personal settings: API key location, local paths
project/src/api/CLAUDE.md    # API module-specific rules: interface design principles
```

### Quick Creation

**Method 1: Auto-generate**

```bash
# Navigate to your project
cd your-project

# Let Claude analyze and generate
claude /init
```

**Method 2: Create from template**

```bash
# Create the file
touch CLAUDE.md

# Edit it
code CLAUDE.md  # or vim CLAUDE.md
```

**Method 3: Use the # key in conversation**

```
You: Remember, the test command for this project is npm run test:unit

[Press # key]

Claude: Added to CLAUDE.md:
# Test Commands
- `npm run test:unit`: Run unit tests
```

### Example: Frontend Project

````markdown
# Project Overview

Internal e-commerce admin dashboard using React 18 + TypeScript + Ant Design.

# Tech Stack

- Frontend: React 18 + TypeScript
- UI Components: Ant Design 5.x
- State Management: Zustand
- HTTP Client: Axios + React Query
- Build Tool: Vite
- Testing: Jest + React Testing Library

# Common Commands

- `pnpm dev`: Start dev server (http://localhost:5173)
- `pnpm build`: Build for production
- `pnpm test`: Run all tests
- `pnpm test:watch`: Run tests in watch mode
- `pnpm lint`: Run ESLint
- `pnpm lint:fix`: Auto-fix lint issues
- `pnpm type-check`: Run TypeScript type checking

# Code Standards

- Use functional components + Hooks, no class components
- TypeScript strict mode, no `any`
- CSS Modules with `*.module.scss` naming
- Variables: camelCase, Components: PascalCase
- One folder per component with index.tsx and index.module.scss

# Project Structure

```
src/
├── components/     # Shared components
├── pages/          # Page components
├── hooks/          # Custom Hooks
├── services/       # API requests
├── stores/         # Zustand stores
├── utils/          # Utility functions
├── types/          # TypeScript type definitions
└── constants/      # Constants
```

# Git Convention

- Commit format: `<type>(<scope>): <description>`
- Types: feat / fix / docs / style / refactor / test / chore
- Example: `feat(user): add pagination to user list`

# Important Notes

- Must pass lint and type-check before committing
- New features require unit tests
- API keys are in .env.local — do not commit
- Do not modify src/generated/ directory (auto-generated code)
````

### Example: Backend Project

````markdown
# Project Overview

User service microservice handling registration, login, and permissions.

# Tech Stack

- Language: Go 1.21
- Framework: Gin
- Database: PostgreSQL 14 + Redis 7
- ORM: GORM
- Auth: JWT
- Docs: Swagger

# Common Commands

- `make run`: Start server (http://localhost:8080)
- `make test`: Run tests
- `make test-coverage`: Generate coverage report
- `make build`: Build for production
- `make docker-build`: Build Docker image
- `make migrate-up`: Run database migrations
- `make migrate-down`: Roll back migrations
- `make swagger`: Generate Swagger docs

# Directory Structure

```
├── cmd/            # Entry points
├── internal/       # Internal packages
│   ├── handler/    # HTTP handlers
│   ├── service/    # Business logic
│   ├── repository/ # Data access
│   └── model/      # Data models
├── pkg/            # Public packages
├── migrations/     # Database migrations
└── docs/           # Swagger docs
```

# Code Standards

- Follow Go official style guide
- All errors must be handled, never ignored
- Use structured logging (zerolog)
- Database operations must be in the repository layer
- Business logic must be in the service layer

# Important Notes

- Sensitive config in .env file — do not commit
- Migration files cannot be modified once committed, only new ones added
- All APIs must have Swagger annotations
````

### Best Practices

**Keep it concise**: Research shows LLMs can reliably follow about 150-200 instructions. Aim for 100-300 lines in CLAUDE.md.

```markdown
# Bad: Too verbose
Our project is an e-commerce system with user management, product management,
order management, etc. We use React as our frontend framework because React
is one of the most popular frameworks today with component-based architecture,
virtual DOM, and other features...

# Good: Concise
# Tech Stack
- React 18 + TypeScript
- Node.js + Express
- PostgreSQL + Redis
```

**Use bullet points**: Replace long paragraphs with short bullet points.

**Write universal rules**: Claude ignores content irrelevant to the current task, so only include broadly applicable information.

**Use progressive disclosure**: Put detailed information in separate files and reference them from CLAUDE.md:

```markdown
# More Information

- API design guidelines: `docs/api-guidelines.md`
- Database schema: `docs/database-schema.md`
- Deployment process: `docs/deployment.md`
```

## Skills: The Extension System

### What Are Skills?

Skills are Claude Code's extension system — essentially preset Markdown guides. When you invoke a skill, Claude automatically loads the corresponding guide and follows it to complete the task.

**An analogy**: Skills are like Standard Operating Procedures (SOPs). For example, the `/commit` skill tells Claude: "When generating a commit message, first check what changed, then write it following Conventional Commits format."

### Built-in Skills

| Skill | Function | Use Case |
|-------|----------|----------|
| `/commit` | Smart Git commit message generation | After completing code changes |
| `/review-pr` | Code review | Reviewing team members' PRs |
| `/pdf` | Process PDF documents | Reading and extracting PDF content |
| `/docx` | Process Word documents | Editing and generating Word documents |
| `/xlsx` | Process Excel spreadsheets | Analyzing and generating spreadsheets |
| `/frontend-design` | Frontend UI design | Implementing UI designs |
| `/bug` | Report a bug | When you find a Claude Code issue |

**Example: `/commit`**

```
You: /commit

Claude: Let me analyze your changes...

[Claude runs git diff]

Detected changes:
- Modified src/auth/login.js (login logic optimization)
- Added src/auth/logout.js (logout feature)
- Modified tests/auth.test.js (added test cases)

Suggested commit message:

feat(auth): optimize login logic and add logout feature

- Refactor login validation flow for better performance
- Add logout endpoint with session clearing
- Add auth module unit tests

Use this commit message? (y/n/edit)
```

**Example: `/review-pr`**

````
You: /review-pr 156

Claude: Fetching PR #156 info...

PR #156: Add Shopping Cart Feature
Author: @developer
Branch: feature/shopping-cart → main
Changes: 12 files, +856/-23 lines

Starting review...

---
## Code Review Report

### Strengths
1. Clean code structure with cart logic in a separate module
2. Comprehensive unit test coverage
3. Well-defined types

### Suggestions
1. **src/cart/CartService.js:45** - Price calculation may have precision issues
   ```javascript
   // Current
   const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

   // Suggested
   const total = items.reduce((sum, item) =>
     sum + Math.round(item.price * item.quantity * 100) / 100, 0);
   ```

2. **src/cart/CartContext.js:23** - Missing error handling
   Consider wrapping API calls in try-catch

### Must Fix
1. **src/cart/utils.js:12** - Potential XSS vulnerability
   ```javascript
   // Dangerous! Direct use of user input
   innerHTML = `Product: ${item.name}`;

   // Use textContent instead
   textContent = `Product: ${item.name}`;
   ```

### Summary
Good code quality overall. Fix the XSS issue before merging.
````

### Creating Custom Skills

Create your own skills in the `.claude/skills/` directory:

```
.claude/
└── skills/
    └── my-skill/
        ├── skill.md       # Skill definition (required)
        └── templates/     # Template files (optional)
```

**Example: "API Documentation Generator" skill**

````markdown
# .claude/skills/api-docs/skill.md

# API Documentation Generator

## Description

Generates Markdown documentation for project API endpoints.

## Trigger

Executes when user invokes /api-docs.

## Steps

1. Scan project route files (supports Express, Koa, Fastify)
2. Extract endpoint information:
   - HTTP method (GET/POST/PUT/DELETE)
   - Path
   - Parameters (path, query, body)
   - Response format
3. Group by module
4. Output to docs/api.md

## Documentation Format

### [METHOD] /path

**Description**: Endpoint functionality

**Request Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|

**Response Example**:
```json
{
  "code": 0,
  "data": {}
}
```

## Notes

- Prefer JSDoc comments when available
- Mark security warnings for sensitive endpoints (password, token)
- Mark deprecated endpoints with [DEPRECATED]
````

**Example: "Component Generator" skill**

````markdown
# .claude/skills/create-component/skill.md

# React Component Generator

## Description

Quickly create React components that follow project standards.

## Parameters

$ARGUMENTS - Component name

## Steps

1. Parse component name, convert to PascalCase
2. Create component folder under src/components/
3. Generate these files:
   - index.tsx (main component file)
   - index.module.scss (styles)
   - index.test.tsx (tests)
   - types.ts (type definitions)

## Templates

### index.tsx
```tsx
import React from 'react';
import styles from './index.module.scss';
import type { ${NAME}Props } from './types';

export const ${NAME}: React.FC<${NAME}Props> = (props) => {
  return (
    <div className={styles.container}>
      ${NAME} Component
    </div>
  );
};

export default ${NAME};
```

### types.ts
```typescript
export interface ${NAME}Props {
  className?: string;
  children?: React.ReactNode;
}
```
````

## Subagents: Specialized AI Instances

### What Are Subagents?

Subagents are an advanced Claude Code feature that allows creating specialized AI sub-instances. Each subagent has its own:

- Independent context window
- Specialized domain knowledge
- Available tool set

**An analogy**: The main Claude is the "project manager" who can summon different "specialist consultants" for specific tasks. The benefits:

1. **Token savings**: Subagents have independent context, avoiding pollution of the main conversation
2. **Better specialization**: Task-specific prompts produce better results
3. **Parallel processing**: Multiple subagents can handle different tasks simultaneously

### Built-in Subagent Types

| Type | Purpose | Available Tools |
|------|---------|----------------|
| `Explore` | Quick codebase exploration | Read, Grep, Glob |
| `Plan` | Design implementation plans | Read, Grep, Glob |
| `Bash` | Execute commands | Bash |
| `code-reviewer` | Code review | Read, Grep, Glob, Bash |
| `general-purpose` | General tasks | All tools |

### Real-World Scenarios

**Scenario 1: Exploring a large codebase**

```
You: This project has hundreds of thousands of lines of code.
     Find all payment-related code.

Claude: This is a large-scale codebase search. Let me dispatch an Explore subagent...

[Explore subagent starts]

Explore Agent: Searching for payment-related code...

Search strategy:
1. Filenames containing pay/payment/checkout
2. Code containing payment/charge/refund keywords
3. Directory structure analysis

Results:

Core payment module
├── src/services/payment/
│   ├── PaymentService.ts (main payment service)
│   ├── StripeProvider.ts (Stripe payments)
│   ├── AlipayProvider.ts (Alipay)
│   └── WechatPayProvider.ts (WeChat Pay)

Payment-related endpoints
├── src/routes/payment.ts (payment API routes)
├── src/routes/webhook.ts (payment callback handling)

Payment-related components
├── src/components/Checkout/ (checkout page)
├── src/components/PaymentForm/ (payment form)

Payment utilities
├── src/utils/payment.ts (price calculation, formatting)

Found 23 related files. Want to dive deeper into any section?
```

**Scenario 2: Designing complex features**

````
You: I need to implement a flash sale system. Help me design the architecture.

Claude: This is a complex feature requiring careful planning.
        Let me dispatch a Plan subagent...

[Plan subagent starts]

## Flash Sale System Design

### Current Architecture Analysis

**Existing stack**:
- Backend: Node.js + Express
- Database: PostgreSQL
- Cache: Redis
- Queue: None (needs to be added)

**Traffic estimate**: Design for 10,000 QPS

### Core Challenges

1. **High-concurrency reads**: Inventory queries on the sale page
2. **High-concurrency writes**: Inventory deduction, order creation
3. **Overselling prevention**: Inventory must never go negative
4. **Performance**: Database cannot handle peak traffic directly

### Technical Architecture

```
[Users] → [Nginx Rate Limiting] → [API Gateway]
                                        ↓
                               [Redis Pre-decrement]
                                        ↓
                              [RabbitMQ Async Queue]
                                        ↓
                              [Order Service Consumer]
                                        ↓
                                  [PostgreSQL]
```

### Key Implementation Details

1. **Inventory pre-loading**
   - Load inventory into Redis before sale starts
   - Use atomic Redis DECR for deductions

2. **Rate limiting**
   - Nginx layer: IP rate limit 100 req/s
   - API layer: Per-user limit, 1 request per second

3. **Async order creation**
   - After successful inventory deduction, send message to queue
   - Consumer creates order asynchronously
   - Client polls for order status

4. **Overselling protection**
   ```lua
   -- Redis Lua script for atomic deduction
   if redis.call('GET', KEYS[1]) > 0 then
     return redis.call('DECR', KEYS[1])
   else
     return -1
   end
   ```

### Implementation Steps

1. [ ] Install and configure RabbitMQ
2. [ ] Implement Redis inventory cache layer
3. [ ] Implement rate limiting middleware
4. [ ] Implement flash sale endpoint
5. [ ] Implement order consumer
6. [ ] Add monitoring and alerting
7. [ ] Load testing

Estimated effort: 3-5 days

Does this plan meet your needs? Ready to start implementation?
````

### Creating Custom Subagents

Create configuration files in the `.claude/agents/` directory:

**Example: "Security Auditor" subagent**

```yaml
# .claude/agents/security-auditor.yaml

name: security-auditor
description: "Security audit specialist for detecting code vulnerabilities"

system_prompt: |
  You are a senior security auditor, expert in OWASP Top 10 and various vulnerabilities.

  When auditing code, focus on:

  1. Injection attacks (SQL, NoSQL, OS command, LDAP)
  2. Authentication and session management
  3. Sensitive data exposure
  4. XSS (reflected, stored, DOM-based)
  5. Insecure deserialization
  6. Components with known vulnerabilities
  7. Insufficient logging and monitoring

  When reporting issues, provide:
  - Location (file:line)
  - Severity (Critical/High/Medium/Low)
  - Description
  - Fix recommendation
  - Fix code example

tools:
  - Read
  - Grep
  - Glob
  - Bash

max_tokens: 8000
```

**Example: "Performance Optimizer" subagent**

```yaml
# .claude/agents/performance-optimizer.yaml

name: performance-optimizer
description: "Performance optimization specialist"

system_prompt: |
  You are a performance optimization expert for both frontend and backend.

  Focus areas:

  Frontend:
  - Bundle size analysis
  - Rendering performance
  - Memory leaks
  - Network request optimization

  Backend:
  - Database query optimization
  - Caching strategies
  - Concurrency handling
  - Memory usage

  Always provide:
  - Quantified improvement estimates (e.g., "50% faster load time")
  - Specific code modifications
  - Explanation of optimization principles
  - Implementation cost assessment

tools:
  - Read
  - Grep
  - Glob
  - Bash

max_tokens: 8000
```

## Configuration and Permissions

### Configuration File Hierarchy

Claude Code uses a three-tier configuration system, priority from highest to lowest:

| File | Location | Purpose | Commit to Git? |
|------|----------|---------|----------------|
| Local config | `.claude/settings.local.json` | Personal preferences | No |
| Project config | `.claude/settings.json` | Team-shared settings | Yes |
| User config | `~/.claude/settings.json` | Global settings | N/A |

### Permission Management

Claude Code asks for confirmation before executing sensitive operations. You can pre-authorize or block specific operations:

```json
{
  "allowedTools": [
    "Read",
    "Write(src/**)",
    "Write(tests/**)",
    "Bash(npm *)",
    "Bash(git *)",
    "Bash(pnpm *)"
  ],
  "deniedTools": [
    "Read(.env*)",
    "Write(.env*)",
    "Read(**/secrets/**)",
    "Write(**/secrets/**)",
    "Bash(rm -rf *)",
    "Bash(sudo *)"
  ]
}
```

**Permission rule reference**:

| Rule | Meaning |
|------|---------|
| `Read` | Allow reading any file |
| `Write(src/**)` | Allow writing to all files under src/ |
| `Bash(npm *)` | Allow running npm commands |
| `Read(.env*)` | Block reading .env files |
| `Bash(rm -rf *)` | Block dangerous delete commands |

### Environment Variables

```bash
# Authentication
export ANTHROPIC_API_KEY=sk-ant-xxxxx  # API Key auth

# Model selection
export CLAUDE_MODEL=sonnet             # Default model

# Proxy settings (corporate networks)
export HTTPS_PROXY=http://proxy.company.com:8080
export HTTP_PROXY=http://proxy.company.com:8080

# Debugging
export CLAUDE_DEBUG=true               # Enable debug logging
```

### Hooks: Automation Triggers

Hooks let you automatically run commands before or after Claude performs certain actions:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "tool": "Write",
        "pattern": "*.ts",
        "command": "npx prettier --write $FILE"
      },
      {
        "tool": "Write",
        "pattern": "*.tsx",
        "command": "npx prettier --write $FILE && npx eslint --fix $FILE"
      }
    ],
    "PreCommit": [
      {
        "command": "npm run lint"
      },
      {
        "command": "npm run test"
      }
    ]
  }
}
```

**In practice**:

```
Claude: I just created src/components/Button.tsx

[PostToolUse Hook triggered]
> npx prettier --write src/components/Button.tsx
> npx eslint --fix src/components/Button.tsx

File auto-formatted.
```

## Advanced Tips and Workflows

### The Explore-Plan-Code-Commit Workflow

This is the officially recommended best practice:

```
# Step 1: Explore
You: Help me understand how user authentication is implemented

Claude: [Uses Explore subagent to search the codebase]
Found it. Let me walk you through the auth flow...

# Step 2: Plan
You: I want to add OAuth2 login. Design an implementation plan.

Claude: [Uses Plan subagent to design the approach]
Here's a detailed implementation plan...

You: Good plan, but let's use Passport.js instead of building from scratch

Claude: OK, let me adjust the plan...

# Step 3: Code
You: Start implementing

Claude: [Implements step by step according to the plan]
I'll install dependencies first, then create config files...

# Step 4: Commit
You: /commit

Claude: [Analyzes changes, generates commit message]
Suggested: feat(auth): add Google OAuth2 login support
```

### Test-Driven Development (TDD)

```
# Step 1: Write tests first
You: Write unit tests for user login covering:
     - Successful login
     - Wrong password
     - User not found
     - Account locked

Claude: [Creates test file]
Created tests/auth/login.test.ts with 12 test cases...

# Step 2: Run tests (should fail)
You: Run the tests

Claude:
> npm test tests/auth/login.test.ts

12 tests, 12 failed
Expected — the feature isn't implemented yet.

# Step 3: Implement the feature
You: Now implement the feature to make tests pass

Claude: [Writes implementation code]

# Step 4: Verify
You: Run tests again

Claude:
> npm test tests/auth/login.test.ts

12 tests, 12 passed
All tests passing!
```

### Multi-Window Parallel Work with Git Worktree

```bash
# Terminal 1: Continue main branch work
cd project
claude

# Terminal 2: Handle an urgent bug fix simultaneously
git worktree add ../project-hotfix hotfix/payment-bug
cd ../project-hotfix
claude
```

**Benefits**:
- Two independent Claude instances working without interference
- Handle multiple tasks simultaneously
- Avoid context loss from frequent branch switching

### CI/CD Integration

**GitHub Actions example**:

```yaml
# .github/workflows/claude-review.yml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Install Claude Code
        run: curl -fsSL https://claude.ai/install.sh | bash

      - name: Run Code Review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "Review the code changes in this PR. Check for:
          1. Code quality and best practices
          2. Potential bugs
          3. Security issues
          4. Performance concerns

          Output a Markdown review report." > review.md

      - name: Post Review Comment
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const review = fs.readFileSync('review.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: review
            });
```

**Auto-generate release notes**:

```bash
# Get commits between two versions
git log v1.0.0..v1.1.0 --oneline | claude -p "
Generate release notes from these Git commits.

Format:
## Version 1.1.0

### New Features
- ...

### Bug Fixes
- ...

### Other Changes
- ...
"
```

### Pipe Operations

Combine Claude with Unix pipes:

```bash
# Analyze error logs
cat error.log | claude -p "Analyze these error logs. Find the most common issues and suggest fixes."

# Code statistics analysis
find src -name "*.ts" | xargs wc -l | claude -p "Analyze these code stats. Tell me:
1. Which modules have the most code
2. Are there any files that need splitting?"

# Dependency analysis
npm list --json | claude -p "Analyze this dependency tree. Find:
1. Outdated dependencies
2. Dependencies with known security vulnerabilities
3. Duplicate dependencies that could be consolidated"
```

### Image-Assisted Development

Claude Code supports direct image processing:

```bash
# Method 1: Drag and drop an image into the terminal
claude "Implement this page according to the design" [drop design image]

# Method 2: Paste a screenshot
# macOS: Cmd+Ctrl+Shift+4 to screenshot, then Cmd+V to paste

# Method 3: Reference an image file
claude "Analyze the @./designs/homepage.png design. What components do we need?"
```

### Managing Large Tasks with Checklists

For complex tasks, have Claude create checklists to track progress:

```
You: Help me migrate the project from JavaScript to TypeScript. Start with a checklist.

Claude: Here's the migration checklist:

## JavaScript to TypeScript Migration

### Phase 1: Foundation Setup
- [ ] Install TypeScript and type definitions
- [ ] Create tsconfig.json
- [ ] Configure build tool for TS support
- [ ] Update ESLint configuration

### Phase 2: Core File Migration
- [ ] src/index.js → src/index.ts
- [ ] src/app.js → src/app.ts
- [ ] src/config/ (5 files)
- [ ] src/utils/ (12 files)

### Phase 3: Business Logic Migration
- [ ] src/services/ (8 files)
- [ ] src/controllers/ (15 files)
- [ ] src/middlewares/ (6 files)

### Phase 4: Type Definitions
- [ ] Create API request/response types
- [ ] Create database model types
- [ ] Create configuration types

### Phase 5: Testing and Verification
- [ ] Update test files
- [ ] Run type checking
- [ ] Run test suite
- [ ] Build production version

Total: ~50 files to migrate
Estimated effort: 2-3 days

Which phase should we start with?
```

## MCP: Model Context Protocol

### What Is MCP?

MCP (Model Context Protocol) is an open protocol that lets Claude Code securely connect to external tools and data sources.

**An analogy**: If Claude's brain provides "thinking ability," MCP gives it "hands" — the ability to interact with external systems.

```
┌─────────────────┐
│   Claude Code   │
└────────┬────────┘
         │ MCP Protocol
         ▼
┌────────────────────────────────────────────┐
│              MCP Servers                    │
├──────────┬──────────┬──────────┬───────────┤
│ GitHub   │ Slack    │ Database │ FileSystem│
│ Server   │ Server   │ Server   │ Server    │
└──────────┴──────────┴──────────┴───────────┘
```

### Adding MCP Servers

```bash
# Add filesystem access (extended scope)
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /path/to/allowed/dir

# Add GitHub integration
claude mcp add github -- npx @modelcontextprotocol/server-github

# Add Slack integration
claude mcp add slack -- npx @modelcontextprotocol/server-slack

# Add SQLite database
claude mcp add sqlite -- npx @modelcontextprotocol/server-sqlite /path/to/database.db

# Add PostgreSQL
claude mcp add postgres -- npx @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost/db"

# Add browser automation
claude mcp add puppeteer -- npx @modelcontextprotocol/server-puppeteer
```

### Common MCP Servers

| Server | Function | Use Case |
|--------|----------|----------|
| **filesystem** | File system access | Access files outside project |
| **github** | GitHub operations | Manage repos, PRs, Issues |
| **slack** | Slack messaging | Send notifications, read channels |
| **sqlite** | SQLite database | Query local databases |
| **postgres** | PostgreSQL | Query production databases |
| **puppeteer** | Browser automation | Web testing, screenshots, scraping |
| **notion** | Notion documents | Read/write Notion pages |
| **google-drive** | Google Drive | Read cloud documents |
| **figma** | Figma designs | Get design file information |

### Usage Examples

**GitHub integration**:

```
You: Check the status of PR #156 and merge it if all checks pass

Claude: Let me check via the GitHub MCP...

[Calls GitHub API via MCP]

PR #156 status:
- Title: Add user export feature
- Author: @developer
- CI checks: All passed (3/3)
- Reviews: Approved (2 reviewers)
- Conflicts: None

All conditions met. Merging now...

[Executes merge via MCP]

PR #156 successfully merged into main!
```

**Database queries**:

```
You: How many users registered yesterday? Group by channel.

Claude: Let me query the database...

[Connects to PostgreSQL via MCP]

> SELECT channel, COUNT(*) as count
  FROM users
  WHERE created_at >= '2025-01-13'
  GROUP BY channel
  ORDER BY count DESC;

Results:

| Channel | New Users |
|---------|-----------|
| organic | 1,234 |
| google_ads | 567 |
| referral | 234 |
| facebook | 123 |

Total: 2,158 new users

Want me to generate a detailed report?
```

### MCP Configuration

MCP config is stored in `~/.claude/mcp.json`:

```json
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "slack": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_TOKEN": "${SLACK_BOT_TOKEN}"
      }
    },
    "database": {
      "command": "npx",
      "args": [
        "@modelcontextprotocol/server-postgres",
        "${DATABASE_URL}"
      ]
    }
  }
}
```

## Role-Specific Usage Guide

### For Software Engineers

**Daily development workflow**:

```bash
# Morning: Continue yesterday's work
claude -c

# Hit a problem: Quick help
claude "What does this error mean? [paste error]"

# Code review: Self-review today's changes
claude "Review my changes from today"

# End of day: Organize commits
claude /commit
```

**Prompt templates**:

```
# New feature development
"Implement [feature description]. Requirements:
1. [Specific requirement 1]
2. [Specific requirement 2]
Reference existing [similar feature/file]"

# Bug fix
"[Error message]
This error occurs when [scenario description]
Find the cause and fix it"

# Refactoring
"Refactor @[file path]. Goals:
1. Improve readability
2. Reduce code duplication
3. Maintain existing functionality"

# Performance optimization
"@[file path] has a performance issue.
Symptom: [problem description]
Analyze and optimize"
```

### For Product Managers

**Understanding technical implementation**:

```
You: Explain the user registration flow. I don't need code details,
     just the overall architecture and key decision points.

Claude: Let me walk you through it...

User Registration Flow Overview:

1. Frontend form submission
   - User provides: email, password, nickname
   - Client-side validation: format, strength

2. Backend processing
   - Check if email is already registered
   - Hash and store password
   - Generate verification code

3. Email delivery
   - Send verification email
   - Valid for 24 hours

4. Email verification
   - User clicks the link
   - Account activated

5. Data storage
   - Users table
   - Verifications table

The entire flow takes about 3-5 seconds to register.
Email may take 1-2 minutes to arrive.
```

### For DevOps Engineers

**Writing monitoring scripts**:

```
You: Write a monitoring script that checks server status every 5 minutes
     and sends an email alert if CPU exceeds 80% or memory exceeds 90%

Claude: I'll create the monitoring script...

[Creates monitor.sh]

Script created! Here's how to use it:

1. Configure email settings
   export ALERT_EMAIL=ops@company.com
   export SMTP_SERVER=smtp.company.com

2. Set execution permissions
   chmod +x monitor.sh

3. Add to crontab
   */5 * * * * /path/to/monitor.sh

4. View logs
   tail -f /var/log/monitor.log
```

## Frequently Asked Questions

### Installation Issues

**Q: Can't run after installation, getting "command not found"**

```bash
# 1. Reload shell config
source ~/.bashrc  # Bash users
source ~/.zshrc   # Zsh users

# 2. Check PATH
echo $PATH | grep -i claude

# 3. Manually add to PATH if needed
export PATH="$HOME/.claude/bin:$PATH"

# 4. Run diagnostics
claude doctor
```

**Q: Installation fails with "permission denied"**

```bash
# Do NOT use sudo! This is a common mistake
# Wrong
sudo npm install -g @anthropic-ai/claude-code

# Correct: Use the recommended installation method
curl -fsSL https://claude.ai/install.sh | bash
```

### Authentication Issues

**Q: Browser login completed but CLI is unresponsive**

```bash
# If stuck, press Ctrl+C to cancel, then retry

# Or use API Key authentication
export ANTHROPIC_API_KEY=sk-ant-xxxxx
claude
```

**Q: Subscription shows as invalid**

```
Check these items:
1. Is your Claude subscription active?
2. Is it Pro/Max/Teams/Enterprise?
3. Are you logged in with the correct account?

Visit https://claude.ai/settings to check subscription status
```

### Usage Issues

**Q: Claude doesn't understand my project**

```
Solutions:

1. Make sure you're running from the project root
   cd /path/to/your/project
   claude

2. Create a CLAUDE.md file
   claude /init

3. Use @ to reference specific files
   claude "Check @./src/main.js for me"

4. Provide enough context
   claude "This is a React project using TypeScript.
          Create a Button component in src/components"
```

**Q: Long conversations causing slow responses or errors**

```bash
# Option 1: Compress history (keeps context summary)
> /compact

# Option 2: Clear and start fresh (complete reset)
> /clear

# Option 3: Start a new session
> /exit
claude
```

**Q: Claude modified files it shouldn't have**

```bash
# 1. Revert with Git
git checkout -- path/to/file

# 2. Configure access restrictions
# In .claude/settings.json:
{
  "deniedTools": [
    "Write(path/to/protected/**)"
  ]
}
```

### Performance Issues

**Q: Responses are very slow**

```
Possible causes and solutions:

1. Network issues
   - Check your connection
   - Configure proxy if on corporate network

2. Long conversation
   - Use /compact to compress history

3. Large project
   - Use @ to reference specific files instead of global search

4. Model selection
   - Use Sonnet for simple tasks (faster)
   claude --model sonnet
```

**Q: Token consumption too high**

```bash
# 1. Check current usage
> /cost

# 2. Tips to reduce consumption:
- Keep CLAUDE.md concise
- Avoid having Claude read large files
- Use specific questions instead of open-ended ones
- /clear after completing a task before starting a new one
```

### Security Concerns

**Q: Will Claude see my sensitive information?**

```
Claude Code security measures:

1. Does not read .env files by default
2. You can configure access restrictions for sensitive files
3. Asks for confirmation before executing sensitive operations

Strengthen protection with:

// .claude/settings.json
{
  "deniedTools": [
    "Read(.env*)",
    "Read(**/*secret*)",
    "Read(**/*credential*)",
    "Read(**/*.pem)",
    "Read(**/*.key)"
  ]
}
```

**Q: Is my code sent to the cloud?**

```
Yes, interactions with Claude are sent to Anthropic's servers.

However:
1. Anthropic does not use your code to train models
2. Conversation data has retention limits
3. Enterprise plans offer private deployment options

For highly sensitive projects:
1. Use Enterprise plan with private deployment
2. Or use Amazon Bedrock / Google Vertex AI versions
```

**Q: How to prevent Claude from running dangerous commands?**

```json
// .claude/settings.json
{
  "deniedTools": [
    "Bash(rm -rf *)",
    "Bash(sudo *)",
    "Bash(chmod 777 *)",
    "Bash(curl * | bash)",
    "Bash(wget * -O - | sh)",
    "Bash(* > /dev/*)",
    "Bash(dd if=*)",
    "Bash(mkfs*)",
    "Bash(:(){:|:&};:)"
  ]
}
```

## Summary

Claude Code is a powerful AI assistant whose core strengths are:

### Core Value Proposition

1. **Terminal-native**: No window switching — work directly in your development environment
2. **Action-capable**: Not just chat — it actually gets things done
3. **Context-aware**: Analyzes your entire codebase for targeted suggestions
4. **Highly customizable**: Extend capabilities through CLAUDE.md, Skills, and Subagents

### Best Use Cases

| Scenario | Recommended Approach |
|----------|---------------------|
| Daily development | Interactive mode: `claude` |
| Quick questions | With initial prompt: `claude "question"` |
| Automation | One-shot mode: `claude -p "instruction"` |
| Code review | `/review-pr` skill |
| Project setup | `/init` to generate CLAUDE.md |
| CI/CD integration | GitHub Actions + `claude -p` |

### Learning Path

**Week 1: Getting Started**
- Install and authenticate
- Learn basic conversation
- Create your first CLAUDE.md

**Week 2: Intermediate**
- Master slash commands
- Learn built-in skills
- Configure permissions and settings

**Week 3: Advanced**
- Create custom skills
- Use Subagents
- Integrate MCP servers

**Ongoing Optimization**
- Refine CLAUDE.md based on experience
- Create team-specific custom tools
- Share best practices

Whether you're a developer looking to boost coding productivity, a business professional who needs to process data, a tech lead managing a team, or an admin looking to automate routine work, Claude Code is worth trying. It represents the future direction of AI tools — not replacing humans, but becoming everyone's intelligent assistant, letting AI handle the tedious work so you can focus on what matters most.

**Useful Links**:

- [Claude Code Official Docs](https://code.claude.com/docs/en/overview)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [CLAUDE.md Writing Guide](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Claude Code Cheat Sheet](https://shipyard.build/blog/claude-code-cheat-sheet/)


## Further Reading

- [Claude Code Command Reference (Quick Lookup)](/posts/ai/2025-01-23-claude-code-commands/)
- [Claude Code Hooks Deep Dive (Automation Key)](/posts/ai/2026-02-18-claude-code-hooks-guide/)
- [Claude Code Browser Automation Comparison](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [OpenClaw Tutorial (From Single Tool to Multi-Agent)](/posts/ai/2026-02-12-openclaw-usage-tutorial/)
- [Codex CLI Mastery Guide (Cross-Tool Workflows)](/posts/ai/2026-02-12-codex-cli-mastery-guide/)
