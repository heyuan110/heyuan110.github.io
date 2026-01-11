---
title: "Claude Code 记忆术：一个文件让 AI 永远记住你是谁"
date: 2026-01-12T00:00:00+08:00
author: "bruce"
description: "手把手教你配置 CLAUDE.md，让 Claude Code 记住你的开发环境、代码风格和工作习惯，告别重复自我介绍"
toc: true
images:
tags:
  - AI
  - Claude Code
  - CLAUDE.md
  - 效率工具
categories:
  - AI实战
---

![Memory Guide](memory-guide.jpg)

## 一、每次都要自我介绍，烦不烦？

用 Claude Code 写代码，体验确实好。

但有个问题：**它不记事**。

每次开新对话，你都得重复一遍：

- "我们项目用的是 pnpm，不是 npm"
- "代码风格要遵循 ESLint + Prettier"
- "Git 提交信息用中文，格式是 type: description"
- "这个项目是 React 18 + TypeScript + Tailwind"

说一次还行，天天说？烦。

更要命的是团队协作——你配置好了，同事那边又是一张白纸，Claude 给他生成的代码风格跟你的完全不一样。

**CLAUDE.md 就是解决这个问题的。**

用一句话定义：

> **CLAUDE.md 就是 Claude 的"入职手册"——写一次，永远生效。**

就像新员工入职要看公司手册一样，Claude 每次启动都会先读这份文件，然后按照里面的规矩干活。

## 二、CLAUDE.md 到底是什么

### 2.1 本质就是一份 Markdown 文件

没有什么黑科技，就是一个普通的 Markdown 文件，放在项目根目录或者用户目录下。

你在里面写什么，Claude 就记住什么：

- 项目背景和技术栈
- 代码规范和风格要求
- 常用命令和工作流程
- 你的个人偏好

举个最简单的例子：

```markdown
# 项目概述

这是一个基于 Next.js 14 的电商后台管理系统。

## 技术栈

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Prisma + PostgreSQL

## 代码规范

- 使用函数式组件，不用 class 组件
- 状态管理用 Zustand
- 所有函数必须有 TypeScript 类型注解
- 变量命名用 camelCase，组件用 PascalCase

## 常用命令

- 开发：pnpm dev
- 构建：pnpm build
- 测试：pnpm test
```

就这么简单。Claude 读了这份文件，就"知道"了你的项目是什么样的，以后生成的代码自然就符合你的规范。

### 2.2 什么时候会被读取

每次你启动 Claude Code 或开始新对话时，它会**自动读取** CLAUDE.md 文件。

你不需要手动@它，不需要每次都说"请先看一下我的配置文件"——它自己就会去找。

读取顺序是这样的：

1. 先读全局配置 `~/.claude/CLAUDE.md`
2. 再读项目配置 `./CLAUDE.md`
3. 最后读个人配置 `./CLAUDE.local.md`

后面的会覆盖前面的。这个设计很聪明：全局放通用规则，项目放项目规范，个人放个人偏好。

### 2.3 CLAUDE.md vs Skill：什么区别？

很多人分不清这两个东西，简单对比：

| 特性 | CLAUDE.md | Skill |
|------|-----------|-------|
| 作用 | 定义"你是谁" | 定义"怎么干活" |
| 内容 | 项目背景、代码规范、偏好设置 | 具体任务的执行流程 |
| 触发 | 自动加载，每次对话都生效 | 遇到相关任务时激活 |
| 类比 | 员工手册 | 岗位 SOP |

**简单说**：

- CLAUDE.md 告诉 Claude "你在什么环境下工作"
- Skill 告诉 Claude "遇到这类任务该怎么做"

两者是互补的，不是替代关系。

## 三、三层配置体系

CLAUDE.md 支持三层配置，满足不同场景的需求。

### 3.1 项目级：CLAUDE.md

放在项目根目录，**提交到 Git**，团队所有人共享。

```
your-project/
├── CLAUDE.md        ← 这个
├── package.json
├── src/
└── ...
```

**适合放什么**：

- 项目技术栈说明
- 团队代码规范
- 目录结构说明
- 常用命令

**核心原则**：这里的内容是团队共识，所有人都要遵守。

### 3.2 个人级：CLAUDE.local.md

放在项目根目录，**不提交到 Git**（加到 .gitignore）。

```
your-project/
├── CLAUDE.md
├── CLAUDE.local.md  ← 这个
├── .gitignore       ← 把 CLAUDE.local.md 加进去
└── ...
```

**适合放什么**：

- 你个人的编码习惯
- 本地环境特殊配置
- 临时的调试说明

**举个例子**：团队规范是用英文注释，但你自己开发时喜欢先用中文写，最后再改成英文——这种"个人小癖好"就放这里。

### 3.3 全局级：~/.claude/CLAUDE.md

放在用户主目录下，**跨项目通用**。

```
~/.claude/
└── CLAUDE.md        ← 这个
```

**适合放什么**：

- 你的个人信息（名字、角色）
- 通用的编码偏好
- 对所有项目都适用的规则

**举个例子**：

```markdown
# 关于我

我是 Bruce，全栈工程师，主要用 TypeScript 和 Go。

## 通用偏好

- 代码注释用中文
- Git 提交信息用中文
- 优先使用函数式编程风格
- 不喜欢过度封装，保持简单
```

### 三层优先级

当三个文件都存在时，加载顺序是：

```
全局 → 项目 → 个人
```

**后加载的内容会覆盖先加载的。**

比如：
- 全局设置了"注释用英文"
- 项目没设置
- 个人设置了"注释用中文"

最终生效的是"注释用中文"。

| 配置层级 | 文件路径 | 是否提交 Git | 作用范围 |
|----------|----------|--------------|----------|
| 全局 | ~/.claude/CLAUDE.md | - | 所有项目 |
| 项目 | ./CLAUDE.md | 是 | 当前项目（团队共享） |
| 个人 | ./CLAUDE.local.md | 否 | 当前项目（仅自己） |

## 四、四种操作方式

### 4.1 /init - 一键初始化

最简单的方式。在项目目录下运行 Claude Code，输入：

```
/init
```

Claude 会自动分析你的项目结构，生成一份 CLAUDE.md 初稿。

它会读取 package.json、tsconfig.json、.eslintrc 等配置文件，自动识别你的技术栈和规范。

**优点**：省事，适合快速开始。

**缺点**：生成的内容比较通用，需要手动补充细节。

### 4.2 # 语法 - 快速追加

对话过程中，随时可以用 `#` 开头的语句往 CLAUDE.md 里加内容。

```
# 所有 API 请求都要加 loading 状态处理
```

Claude 会把这条规则追加到配置文件里。

**适合场景**：写代码过程中发现一个规则需要记住，顺手加进去。

### 4.3 /memory - 可视化编辑

输入：

```
/memory
```

会打开一个交互式界面，让你查看和编辑当前的 CLAUDE.md 内容。

可以选择编辑哪一层的配置（全局/项目/个人）。

### 4.4 @ 引用 - 模块化组合

当配置内容很多时，可以拆分成多个文件，用 `@` 语法引用：

```markdown
# 项目配置

@docs/architecture.md
@docs/api-conventions.md
@docs/testing-guide.md
```

Claude 会自动读取这些被引用的文件。

**适合场景**：大型项目，配置内容超过几百行时，拆分成模块更易维护。

## 五、三个配置模板

### 5.1 个人开发者模板

适合独立开发者，配置自己的通用偏好。

放在 `~/.claude/CLAUDE.md`：

```markdown
# 关于我

我是 [你的名字]，[你的角色]。

## 编码偏好

- 代码注释用中文
- Git 提交信息用中文，格式：`type: description`
- 优先使用函数式编程
- 变量命名要有意义，不用 a、b、c、temp 这种
- 不写多余的注释，代码本身要有可读性

## 工作习惯

- 改完代码先跑一遍 lint
- 提交前确保没有 TypeScript 报错
- 不要一次改太多文件，小步提交

## 我不喜欢的

- 过度封装
- 没必要的设计模式
- 太长的函数（超过 50 行就该拆了）
```

### 5.2 团队协作模板

适合团队项目，放在项目根目录 `CLAUDE.md`，提交到 Git。

````markdown
# 项目名称

[一句话描述项目是什么]

## 技术栈

- 框架：Next.js 14 (App Router)
- 语言：TypeScript 5.x（strict 模式）
- 样式：Tailwind CSS
- 状态管理：Zustand
- 数据库：PostgreSQL + Prisma
- 测试：Vitest + Testing Library

## 目录结构

```
src/
├── app/          # Next.js App Router 页面
├── components/   # 可复用组件
│   ├── ui/       # 基础 UI 组件
│   └── features/ # 业务组件
├── lib/          # 工具函数和配置
├── hooks/        # 自定义 Hooks
├── stores/       # Zustand stores
├── types/        # TypeScript 类型定义
└── services/     # API 调用层
```

## 代码规范

### 命名规范
- 文件名：kebab-case（如 `user-profile.tsx`）
- 组件名：PascalCase（如 `UserProfile`）
- 函数/变量：camelCase（如 `getUserById`）
- 常量：UPPER_SNAKE_CASE（如 `MAX_RETRY_COUNT`）

### 组件规范
- 使用函数式组件 + Hooks
- Props 必须定义 TypeScript interface
- 复杂组件拆分成小组件

### Git 规范
- 提交信息格式：`type: description`
- type 可选：feat / fix / refactor / docs / test / chore
- 示例：`feat: 添加用户登录功能`

## 常用命令

```bash
pnpm dev          # 启动开发服务器
pnpm build        # 构建生产版本
pnpm test         # 运行测试
pnpm lint         # 代码检查
pnpm db:migrate   # 数据库迁移
```

## 注意事项

- 所有 API 请求必须处理 loading 和 error 状态
- 敏感信息放 .env.local，不要提交到 Git
- 新增功能必须写单元测试
````

### 5.3 技术栈专用模板

#### React + TypeScript 项目

```markdown
# React 项目规范

## 组件编写规则

- 优先使用函数式组件
- 状态管理：简单用 useState，复杂用 Zustand
- 副作用处理：useEffect 依赖项必须完整
- 避免在 render 中创建新对象/函数（用 useMemo/useCallback）

## 类型定义

- 组件 Props 用 interface，命名为 `XxxProps`
- API 响应类型放 `types/api.ts`
- 不用 any，实在不知道类型用 unknown

## 文件组织

- 一个组件一个文件夹：`ComponentName/index.tsx`
- 组件专用样式：`ComponentName/styles.ts`
- 组件专用类型：`ComponentName/types.ts`
```

#### Python 项目

````markdown
# Python 项目规范

## 代码风格

- 遵循 PEP 8
- 使用 Black 格式化，行宽 88
- 使用 type hints
- docstring 用 Google 风格

## 项目结构

- 入口文件：main.py
- 配置管理：用 pydantic-settings
- 依赖管理：用 Poetry

## 常用命令

```bash
poetry install    # 安装依赖
poetry run pytest # 运行测试
poetry run black . # 格式化代码
```
````

## 六、进阶技巧

### 6.1 模块化拆分大型配置

当 CLAUDE.md 超过 500 行时，维护起来就很痛苦了。

用 `@` 引用拆分成多个文件：

```markdown
# 项目配置

## 基础信息
@docs/overview.md

## 架构说明
@docs/architecture.md

## API 规范
@docs/api-conventions.md

## 测试指南
@docs/testing-guide.md
```

每个被引用的文件专注一个主题，清晰易维护。

### 6.2 CLAUDE.md + Skill 组合拳

CLAUDE.md 定义环境，Skill 定义任务。两者配合效果更好。

**CLAUDE.md** 里写：

```markdown
## 代码审查标准

- 必须有单元测试
- 不能有 console.log
- 不能有硬编码的配置
```

**Skill** 里写具体的审查流程：

```markdown
---
name: code-review
description: 审查代码变更，检查规范和潜在问题
---

# 代码审查 Skill

## 执行步骤

1. 读取 git diff
2. 按 CLAUDE.md 中的代码审查标准检查
3. 输出问题列表和修改建议
```

这样 Skill 会自动引用 CLAUDE.md 里的标准，不用重复写。

### 6.3 团队协作最佳实践

1. **CLAUDE.md 必须提交到 Git**
   - 这是团队共识，所有人都要遵守
   - Code Review 时检查是否符合 CLAUDE.md 的规范

2. **CLAUDE.local.md 加入 .gitignore**
   - 个人偏好不强制给别人
   - 避免冲突

3. **定期更新**
   - 项目演进了，配置也要跟着更新
   - 发现 Claude 总是犯同样的错，就加条规则

4. **新人入职第一件事**
   - 让新人读一遍 CLAUDE.md
   - 这不仅是给 Claude 看的，也是给人看的

## 七、写在最后

CLAUDE.md 的本质，是把"上下文"固化下来。

你每天跟 Claude 说的那些话——项目背景、代码规范、个人偏好——与其每次说一遍，不如写成文件，一劳永逸。

这不只是"让 AI 更好用"，更是"让你的知识变成可复用的资产"。

写好一份 CLAUDE.md，就像给新员工写了一份培训手册。Claude 会按这个手册干活，新来的同事也能通过这份文件快速了解项目规范。

**AI 没有记忆，但你可以给它装一个。**

CLAUDE.md 就是那个记忆体。
