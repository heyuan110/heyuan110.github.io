+++
date = '2026-01-14T14:38:00+08:00'
title = 'Claude Code从入门到精通：终端里的全能AI助手完全指南'
description = '全面介绍 Anthropic 官方 AI 工具 Claude Code，从基础概念到高级用法，涵盖安装配置、日常使用、CLAUDE.md、Skills、Subagent 等核心功能。无论你是开发者、产品经理、运维人员还是行政财务，都能从中找到提升效率的方法。'
toc = true
tags = ['Claude Code', 'AI 工具', 'Anthropic', '命令行工具', '效率工具', '自动化']
categories = ['AI实战']
keywords = ['Claude Code 使用指南', 'Claude Code 教程', 'Anthropic CLI 工具', 'AI 编程助手', 'Claude Code 入门']
+++
![Claude Code 终端 AI 助手](cover.webp)

你是否曾经希望有一个真正能「动手干活」的 AI 助手——不只是给你建议，而是能直接帮你处理文件、执行命令、完成各种重复性工作？**Claude Code** 正是 Anthropic 官方推出的这样一款工具——它运行在终端里，是一个能够理解你的需求并付诸行动的全能助手。

**它不只是程序员的专属工具**。虽然 Claude Code 在编程领域表现出色，但它同样能帮助产品经理整理文档、帮运维人员分析日志、帮行政财务人员处理数据报表、帮任何人自动化那些繁琐的重复工作。

无论你是资深开发者、产品经理、运维人员，还是行政财务同学，这篇文章都将带你从零开始，全面掌握 Claude Code 的使用方法，找到属于你的效率提升之道。

## 一、什么是 Claude Code？

### 1. 核心定位

**Claude Code** 是 Anthropic 推出的官方命令行工具（CLI），它是一个「代理型 AI 工具」（Agentic AI Tool），直接运行在你的终端中。

与普通的 AI 聊天不同，Claude Code 的最大特点是：**它可以直接执行操作**。

| 特点 | 说明 |
|------|------|
| 终端原生 | 不是聊天窗口，不是 IDE 插件，而是命令行工具 |
| 可执行操作 | 能直接编辑文件、运行命令、处理数据 |
| 理解上下文 | 自动分析项目结构和文件内容 |
| 自然语言交互 | 用大白话描述需求，Claude 帮你实现 |

**一个简单的类比**：如果说 ChatGPT 是「顾问」，只能给你建议；那么 Claude Code 就是「助理」，能真正动手帮你干活。

### 2. 能做什么？

Claude Code 主要解决四大类问题：

**构建功能**：告诉 Claude 你想做什么，它会制定计划、编写代码、确保代码能跑。

```bash
# 示例：让 Claude 帮你写一个用户注册功能
claude "帮我实现一个用户注册接口，包含邮箱验证"
```

**实际对话场景**：

```
你：帮我实现一个用户注册接口，包含邮箱验证

Claude：我来帮你实现用户注册接口。让我先了解一下项目结构...

[Claude 自动分析项目]

我看到这是一个 Express + MongoDB 的项目。我将：
1. 在 routes/ 下创建 auth.js 路由
2. 在 models/ 下创建 User 模型
3. 实现邮箱验证码发送功能
4. 添加必要的输入验证

现在开始实现...

[Claude 自动创建文件、编写代码]

完成！我已经创建了以下文件：
- routes/auth.js - 注册和验证接口
- models/User.js - 用户模型
- utils/email.js - 邮件发送工具

要测试一下吗？运行 npm run dev 后访问 POST /api/auth/register
```

**调试修复**：描述 Bug 或粘贴报错信息，Claude 会分析代码库、定位问题、实施修复。

```bash
# 示例：让 Claude 帮你修 Bug
claude "这个报错是什么意思？帮我修复：TypeError: Cannot read property 'map' of undefined"
```

**实际对话场景**：

```
你：运行时报错 TypeError: Cannot read property 'map' of undefined，
    在 UserList.jsx 第 23 行

Claude：让我检查一下这个文件...

[Claude 读取 UserList.jsx]

找到问题了！在第 23 行你直接对 users 调用 map，但 users 初始值是 undefined。

问题代码：
const UserList = () => {
  const [users, setUsers] = useState();  // 初始值是 undefined
  return users.map(user => <div>{user.name}</div>);  // 报错
}

我来修复它：

[Claude 修改文件]

修复方案：
1. 给 useState 设置初始空数组
2. 添加加载状态判断

修改后：
const UserList = () => {
  const [users, setUsers] = useState([]);  // 改为空数组
  const [loading, setLoading] = useState(true);

  if (loading) return <div>加载中...</div>;
  return users.map(user => <div key={user.id}>{user.name}</div>);
}

已修复！同时我还加了 key 属性避免 React 警告。
```

**代码导航**：询问关于代码库的任何问题，Claude 会帮你找到答案。

```bash
# 示例：了解代码结构
claude "这个项目的认证逻辑在哪里实现的？"
```

**实际对话场景**：

```
你：这个项目的认证逻辑在哪里实现的？我想了解用户登录的完整流程

Claude：让我帮你梳理一下认证流程...

[Claude 搜索并分析相关文件]

这个项目使用 JWT 认证，完整流程如下：

📁 认证相关文件：
├── middleware/auth.js      - JWT 验证中间件
├── routes/auth.js          - 登录注册接口
├── services/AuthService.js - 认证业务逻辑
└── utils/jwt.js            - Token 生成与验证

🔄 登录流程：
1. 用户提交 POST /api/auth/login (routes/auth.js:45)
2. AuthService.login() 验证密码 (services/AuthService.js:23)
3. 验证通过后生成 JWT (utils/jwt.js:12)
4. 返回 token 给前端

🔒 请求验证流程：
1. 前端在 Header 携带 Authorization: Bearer <token>
2. auth 中间件解析并验证 token (middleware/auth.js:8)
3. 验证通过则将 user 挂载到 req.user
4. 验证失败返回 401

需要我详细解释某个部分吗？
```

**自动化任务**：修复 lint 问题、解决合并冲突、生成发布说明等繁琐工作。

```bash
# 示例：自动修复代码风格问题
claude "修复所有 ESLint 报错"
```

**实际对话场景**：

```
你：项目里有很多 ESLint 报错，帮我全部修复

Claude：让我先运行 ESLint 看看有哪些问题...

[Claude 执行 npm run lint]

发现 47 个问题，分布在 12 个文件中：
- 28 个 "prefer-const" 警告
- 12 个 "no-unused-vars" 错误
- 5 个 "react-hooks/exhaustive-deps" 警告
- 2 个 "no-console" 警告

开始修复...

[Claude 逐个修改文件]

✅ 已修复 45 个问题
⚠️ 2 个问题需要你确认：

1. src/utils/debug.js:15 - console.log 是调试代码还是需要保留？
2. src/hooks/useAuth.js:23 - unused 变量 `refreshToken` 是预留功能吗？

请告诉我如何处理这两个。
```

**🌟 非编程场景同样出色**

虽然上面的例子偏向编程，但 Claude Code 的能力远不止于此。它本质上是一个能操作文件和执行命令的智能助手：

**文档处理**：整理、转换、批量处理各种文档。

```
你：帮我把 docs 文件夹下的所有 Word 文档转换成 PDF

Claude：好的，让我先看看文件夹里有哪些文档...

[Claude 列出文件]

找到 15 个 Word 文档。我将使用 LibreOffice 进行转换...

[Claude 执行转换]

✅ 全部完成！15 个 PDF 已保存到 docs/pdf/ 文件夹。
```

**数据分析**：处理 Excel、CSV 数据，生成统计报告。

```
你：分析一下 sales.csv 里的销售数据，找出销量最好的产品

Claude：让我读取并分析这个数据文件...

[Claude 读取数据]

分析结果：
📊 数据概览：共 1,234 条销售记录，涵盖 45 种产品

🏆 销量 Top 5：
1. 无线鼠标 - 销量 892 件，销售额 ¥89,200
2. 机械键盘 - 销量 654 件，销售额 ¥130,800
3. USB 扩展坞 - 销量 543 件，销售额 ¥54,300
...

需要我生成详细的分析报告吗？
```

**文件整理**：自动分类、重命名、归档文件。

```
你：把下载文件夹整理一下，按文件类型分类

Claude：好的，让我看看下载文件夹的内容...

[Claude 分析文件]

找到 156 个文件，我将按以下方式整理：
- 图片 (32 个) → Downloads/图片/
- 文档 (45 个) → Downloads/文档/
- 视频 (12 个) → Downloads/视频/
- 压缩包 (28 个) → Downloads/压缩包/
- 其他 (39 个) → Downloads/其他/

确认执行吗？

你：执行

Claude：[自动移动文件]

✅ 整理完成！文件已按类型归类到对应文件夹。
```

**信息提取**：从网页、文档中提取需要的信息。

```
你：帮我从这 20 个简历 PDF 中提取姓名、电话、邮箱，整理成表格

Claude：好的，让我处理这些简历...

[Claude 逐个读取 PDF]

已提取 20 位候选人的信息，保存到 candidates.xlsx：

| 姓名 | 电话 | 邮箱 | 学历 |
|------|------|------|------|
| 张三 | 138xxxx1234 | zhang@email.com | 本科 |
| 李四 | 139xxxx5678 | li@email.com | 硕士 |
...

需要添加其他字段吗？
```

**💰 财务场景：报表与数据处理**

```
财务小李：我需要把这个月的费用报销单汇总，按部门统计总额

Claude：好的，让我处理这些报销数据...

[Claude 读取 expense_reports.xlsx]

📊 2025年1月费用报销汇总

| 部门 | 报销笔数 | 总金额 | 占比 |
|------|----------|--------|------|
| 销售部 | 45 笔 | ¥128,500 | 35.2% |
| 市场部 | 32 笔 | ¥89,200 | 24.5% |
| 研发部 | 28 笔 | ¥76,800 | 21.1% |
| 行政部 | 18 笔 | ¥45,300 | 12.4% |
| 人事部 | 12 笔 | ¥24,800 | 6.8% |

💡 发现异常：
- 销售部「差旅费」同比增长 45%，建议核查
- 有 3 笔报销金额超过 ¥10,000，需要总监审批

要生成详细的分部门报表吗？
```

```
财务小李：帮我核对一下银行流水和我们的收款记录，看有没有差异

Claude：好的，让我对比这两份数据...

[Claude 读取 bank_statement.csv 和 payment_records.xlsx]

🔍 核对结果：

✅ 匹配成功：bindicate 287 笔，金额 ¥1,892,450.00
⚠️ 银行有但系统无：3 笔
  - 01-15 ¥5,000.00 (转账备注：王明 货款)
  - 01-18 ¥12,800.00 (转账备注：深圳XX公司)
  - 01-22 ¥3,200.00 (转账备注：退款)

⚠️ 系统有但银行无：1 笔
  - 订单 #20250120-089，¥8,900.00，客户：张总

建议：
1. 3 笔未入账款项需要补录系统
2. 订单 #20250120-089 可能客户尚未付款，建议跟进

要我生成差异明细表吗？
```

**📋 行政场景：文档与事务管理**

```
行政小张：下周要开年度总结会，帮我整理一下会议材料

Claude：好的，让我帮你准备会议材料...

请告诉我：
1. 会议时间和地点？
2. 参会人员名单在哪里？
3. 需要准备哪些材料？

行政小张：下周三下午2点，大会议室，参会名单在 attendees.xlsx，
         需要准备签到表、会议议程、各部门的 PPT 合集

Claude：明白了，开始准备...

[Claude 处理文件]

✅ 已完成：

1. 📝 签到表 (sign_in_sheet.xlsx)
   - 已按部门分组排列 48 位参会人员
   - 包含：姓名、部门、职位、签到栏、备注栏

2. 📋 会议议程 (agenda.docx)
   - 已生成标准会议议程模板
   - 时间：2025年1月22日 14:00-17:00
   - 地点：大会议室

3. 📑 PPT 合集 (annual_summary_2024.pptx)
   - 已合并 6 个部门的 PPT（共 124 页）
   - 按议程顺序排列
   - 已统一字体和页码格式

还需要准备茶歇安排表吗？
```

```
行政小张：公司要搬到新办公室，帮我做个资产盘点清单

Claude：好的，让我帮你整理资产清单...

[Claude 读取 assets.xlsx]

📦 办公资产盘点清单

## 按类别统计

| 类别 | 数量 | 预估价值 |
|------|------|----------|
| 电脑设备 | 86 台 | ¥430,000 |
| 办公家具 | 124 件 | ¥186,000 |
| 会议设备 | 12 套 | ¥96,000 |
| 打印设备 | 8 台 | ¥64,000 |
| 其他 | 45 件 | ¥22,500 |

## 按楼层分布

- 3楼（研发）：89 件
- 4楼（销售+市场）：76 件
- 5楼（行政+财务+人事）：58 件
- 会议室：12 件

## 需要特别注意

⚠️ 以下设备搬运需专业人员：
- 服务器机柜 x 2（3楼机房）
- 大型复印机 x 2（4楼、5楼）
- 投影仪 x 3（需要重新安装）

已生成完整清单 asset_inventory.xlsx，包含每件资产的编号、
位置、负责人、搬运注意事项。
```

**📊 运营场景：数据分析与报告**

```
运营小王：帮我分析一下上周的用户活跃数据

Claude：好的，让我分析用户活跃情况...

[Claude 读取 user_activity.csv]

📈 上周用户活跃分析报告（1月13日-1月19日）

## 核心指标

| 指标 | 本周 | 上周 | 环比 |
|------|------|------|------|
| DAU（日均） | 12,450 | 11,800 | +5.5% ↑ |
| WAU | 45,200 | 43,100 | +4.9% ↑ |
| 人均使用时长 | 18.5分钟 | 16.2分钟 | +14.2% ↑ |
| 新用户数 | 3,240 | 2,890 | +12.1% ↑ |
| 次日留存率 | 42.3% | 39.8% | +2.5pp ↑ |

## 用户行为分析

🔥 热门功能 Top 5：
1. 首页浏览 - 89,234 次
2. 商品搜索 - 45,678 次
3. 购物车 - 23,456 次
4. 订单查询 - 18,234 次
5. 个人中心 - 15,678 次

📉 流失节点：
- 商品详情 → 加入购物车：转化率 32%（行业均值 38%）
- 购物车 → 提交订单：转化率 28%（需要优化）

💡 建议：
1. 购物车页面转化率偏低，建议增加优惠提示
2. 新用户次日留存提升明显，继续保持新人引导策略

要我生成完整的周报 PPT 吗？
```

```
运营小王：我们下周要做促销活动，帮我预估一下需要备多少货

Claude：好的，让我基于历史数据做个预估...

[Claude 分析 sales_history.xlsx 和 promotion_history.xlsx]

🎯 促销活动备货建议

## 分析依据
- 参考：过去 6 次同类促销活动数据
- 活动类型：满减促销
- 预计持续：3 天

## 热销商品备货建议

| 商品 | 日常销量 | 促销预估 | 建议备货 | 安全库存 |
|------|----------|----------|----------|----------|
| A款连衣裙 | 50件/天 | 200件/天 | 800件 | 含20%余量 |
| B款T恤 | 80件/天 | 280件/天 | 1,200件 | 含20%余量 |
| C款牛仔裤 | 35件/天 | 150件/天 | 600件 | 含20%余量 |
| D款外套 | 25件/天 | 100件/天 | 400件 | 含20%余量 |

## 风险提示

⚠️ 以下商品当前库存不足：
- A款连衣裙：现有 520 件，缺口 280 件
- C款牛仔裤：现有 450 件，缺口 150 件

📦 建议：立即联系供应商补货，预计需要 3 个工作日到货

## 预估销售额

- 保守估计：¥450,000
- 正常预期：¥580,000
- 乐观预期：¥720,000

要我生成详细的备货清单发给仓库吗？
```

### 3. 适合谁用？

Claude Code 的强大之处在于它降低了技术门槛，让不同背景的人都能受益：

| 角色 | 使用场景 | 实际例子 |
|------|----------|----------|
| **开发工程师** | 写代码、改 Bug、重构、代码审查 | "帮我把这个类重构成函数式组件" |
| **产品经理** | 快速验证想法、理解技术实现 | "这个需求技术上能实现吗？大概要改哪些地方？" |
| **运维人员** | 编写脚本、自动化运维任务 | "写一个脚本监控服务器 CPU，超过 80% 就报警" |
| **技术管理者** | 了解代码库、审查团队工作 | "这次迭代改了哪些核心逻辑？有没有风险点？" |
| **测试工程师** | 编写测试用例、分析测试覆盖率 | "为这个支付模块补充边界测试用例" |
| **非技术人员** | 学习编程、完成简单自动化任务 | "帮我写个 Python 脚本，每天自动整理下载文件夹" |

**非技术人员使用示例**：

```
财务小王：我每个月要把销售数据从 Excel 复制到报表系统，能自动化吗？

Claude：当然可以！让我帮你写一个 Python 脚本。

你需要告诉我：
1. Excel 文件在哪个文件夹？
2. 报表系统是网页还是软件？
3. 数据要怎么对应？

财务小王：Excel 在 D:/销售数据/ 文件夹，报表是网页系统，
         Excel 的 A 列是产品名，B 列是销售额

Claude：明白了，我来实现...

[Claude 创建脚本]

完成！使用方法：
1. 双击 "运行.bat" 文件
2. 输入报表系统的账号密码
3. 脚本会自动完成剩下的工作

我还加了日志功能，每次运行会记录在 log.txt 里，
方便你追溯。要我演示一下吗？
```

### 4. 与其他 AI 编程工具的对比

| 特性 | Claude Code | GitHub Copilot | Cursor | ChatGPT |
|------|-------------|----------------|--------|---------|
| 运行环境 | 终端 | IDE 插件 | 独立 IDE | 网页/APP |
| 执行操作 | ✅ 可以 | ❌ 不能 | ✅ 可以 | ❌ 不能 |
| 理解项目 | ✅ 整个代码库 | ⚠️ 当前文件 | ✅ 整个代码库 | ❌ 需要粘贴 |
| Git 操作 | ✅ 直接执行 | ❌ 不能 | ⚠️ 部分支持 | ❌ 不能 |
| 运行命令 | ✅ 可以 | ❌ 不能 | ✅ 可以 | ❌ 不能 |
| 价格 | Pro 订阅 | $10/月 | $20/月 | Plus $20/月 |

## 二、如何安装 Claude Code？

### 1. 前置条件

开始之前，你需要：

- **Claude 订阅**：Pro（$20/月）、Max（$100/月）、Teams 或 Enterprise 版本
- 或者 **Claude API 账户**：按 Token 计费使用

**系统要求**：

| 操作系统 | 版本要求 |
|----------|----------|
| macOS | 10.15 (Catalina) 或更高 |
| Linux | Ubuntu 20.04+ / Debian 10+ |
| Windows | Windows 10+ (需要 WSL 或 Git Bash) |

### 2. 安装方法

**方法一：macOS / Linux / WSL（推荐）**

打开终端，执行一行命令：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

安装完成后，重新加载 Shell 配置：

```bash
# 如果用 Bash
source ~/.bashrc

# 如果用 Zsh
source ~/.zshrc
```

**方法二：macOS 使用 Homebrew**

```bash
# 安装
brew install --cask claude-code

# 更新
brew upgrade --cask claude-code
```

**方法三：Windows PowerShell**

以管理员身份打开 PowerShell：

```powershell
irm https://claude.ai/install.ps1 | iex
```

**方法四：Windows 使用 WinGet**

```powershell
# 安装
winget install Anthropic.ClaudeCode

# 更新
winget upgrade Anthropic.ClaudeCode
```

**方法五：npm 安装（已弃用，不推荐）**

```bash
# 需要 Node.js 18+
npm install -g @anthropic-ai/claude-code
```

### 3. 验证安装

```bash
# 查看版本
claude --version

# 运行诊断（强烈推荐）
claude doctor
```

`claude doctor` 会自动检测以下问题并给出修复建议：

- Node.js 版本是否满足要求
- 环境变量是否正确配置
- 网络连接是否正常
- 认证状态是否有效

**示例输出**：

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

### 4. 首次登录

安装完成后，进入你的项目目录，启动 Claude Code：

```bash
cd your-project
claude
```

首次运行会自动打开浏览器，引导你完成登录认证：

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

### 5. 使用 API Key（可选）

如果你不想用浏览器登录，可以使用 API Key：

```bash
# 设置环境变量
export ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx

# 或者在启动时指定
claude --api-key sk-ant-xxxxxxxxxxxxx
```

**获取 API Key**：

1. 访问 [console.anthropic.com](https://console.anthropic.com)
2. 登录你的账户
3. 进入 API Keys 页面
4. 创建新的 Key 并复制

## 三、基础使用指南

### 1. 启动方式

Claude Code 提供多种启动方式，适应不同场景：

```bash
# 方式一：交互式对话（最常用）
claude

# 方式二：带初始问题启动
claude "这个项目是做什么的？"

# 方式三：单次查询模式（执行完自动退出）
claude -p "生成一份 API 文档"

# 方式四：继续上次对话
claude -c
# 或
claude --continue

# 方式五：选择历史会话恢复
claude --resume
```

**各模式对比**：

| 启动方式 | 适用场景 | 是否保留对话 |
|----------|----------|--------------|
| `claude` | 日常开发、探索代码库 | ✅ 保留 |
| `claude "问题"` | 快速提问并继续对话 | ✅ 保留 |
| `claude -p "问题"` | 自动化脚本、CI/CD | ❌ 不保留 |
| `claude -c` | 继续昨天的工作 | ✅ 保留 |
| `claude --resume` | 切换不同任务的对话 | ✅ 保留 |

**会话管理示例**：

```bash
# 查看所有历史会话
claude --resume

# 输出：
Recent sessions:
1. [2h ago]  "修复登录 Bug" - src/auth.js
2. [1d ago]  "重构用户模块" - src/users/
3. [3d ago]  "添加支付功能" - src/payment/

Select a session to resume (1-3) or press Enter to start new:
```

### 2. 常用斜杠命令

在交互式对话中，可以使用斜杠命令：

| 命令 | 功能 | 使用场景 |
|------|------|----------|
| `/help` | 显示帮助信息 | 忘记命令时查看 |
| `/clear` | 清空当前对话历史 | 开始新任务时 |
| `/compact` | 压缩对话历史 | 对话太长影响性能时 |
| `/exit` | 退出 Claude Code | 结束工作 |
| `/status` | 显示账户状态 | 查看订阅信息 |
| `/cost` | 显示 Token 使用情况 | 监控用量 |
| `/config` | 配置设置 | 修改默认行为 |
| `/init` | 初始化项目 | 为新项目创建 CLAUDE.md |
| `/memory` | 编辑项目记忆 | 修改 CLAUDE.md |
| `/permissions` | 管理工具权限 | 授权或禁止某些操作 |
| `/bug` | 报告 Bug | 发现问题时反馈 |

**命令使用示例**：

```
> /status

Account Status
==============
Email: user@example.com
Plan: Claude Pro
Usage this month: 2.3M tokens
Remaining: Unlimited

> /cost

Session Cost
============
Tokens used: 45,230
  - Input: 38,500
  - Output: 6,730
Estimated cost: $0.23

> /compact

Compressing conversation history...
Before: 128,000 tokens
After: 24,000 tokens
Saved: 81% tokens

Context maintained for:
- File changes made
- Key decisions
- Current task status
```

### 3. 文件引用

使用 `@` 符号可以引用文件或目录，让 Claude 聚焦于特定代码：

```bash
# 引用单个文件
claude "帮我优化 @./src/utils/auth.js 这个文件的性能"

# 引用多个文件
claude "对比 @./src/old-api.js 和 @./src/new-api.js 的差异"

# 引用整个目录
claude "分析 @./src/components 目录下所有组件的代码质量"

# 引用特定类型的文件
claude "检查 @./src/**/*.test.js 所有测试文件的覆盖率"
```

**实际对话示例**：

```
你：@./src/utils/date.js 这个文件有什么问题？

Claude：让我分析一下这个日期工具文件...

[Claude 读取文件]

发现以下几个问题：

1. **时区处理不一致** (第 23-45 行)
   - formatDate() 使用本地时区
   - parseDate() 假设是 UTC
   建议：统一使用 UTC 或明确指定时区

2. **性能问题** (第 67 行)
   - 每次调用都创建新的 Intl.DateTimeFormat
   建议：缓存 formatter 实例

3. **潜在 Bug** (第 89 行)
   - isValidDate() 没有处理 Invalid Date
   建议：添加 isNaN() 检查

4. **缺少类型定义**
   建议：添加 JSDoc 或 TypeScript 类型

需要我帮你修复这些问题吗？
```

### 4. 执行 Shell 命令

在对话中使用 `!` 前缀执行 Shell 命令：

```bash
# 在 Claude Code 对话中
!git status
!npm run test
!docker ps
!ls -la src/
```

**实际对话示例**：

```
你：帮我看看当前有哪些 Docker 容器在运行

Claude：让我查看一下...

> !docker ps

CONTAINER ID   IMAGE          PORTS                    STATUS
a1b2c3d4e5f6   postgres:14    0.0.0.0:5432->5432/tcp   Up 2 hours
b2c3d4e5f6g7   redis:7        0.0.0.0:6379->6379/tcp   Up 2 hours
c3d4e5f6g7h8   nginx:latest   0.0.0.0:80->80/tcp       Up 30 mins

当前有 3 个容器在运行：
- PostgreSQL 数据库 (端口 5432)
- Redis 缓存 (端口 6379)
- Nginx 反向代理 (端口 80)

需要我帮你做什么操作吗？比如查看日志、重启容器等。
```

### 5. 选择模型

根据任务复杂度选择合适的模型：

```bash
# 使用 Sonnet（日常任务，速度快，性价比高）
claude --model sonnet

# 使用 Opus（复杂任务，更强大，更贵）
claude --model opus

# 使用 Haiku（简单任务，最快最便宜）
claude --model haiku
```

**模型选择建议**：

| 模型 | 适用场景 | 响应速度 | 成本 |
|------|----------|----------|------|
| **Haiku** | 简单问答、代码补全、格式化 | 最快 | 最低 |
| **Sonnet** | 日常开发、Bug 修复、代码审查 | 较快 | 中等 |
| **Opus** | 复杂架构设计、大规模重构、疑难问题 | 较慢 | 较高 |

### 6. 实用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Tab` | 自动补全文件路径 |
| `Ctrl+C` | 中断当前操作 |
| `Ctrl+D` | 退出 Claude Code |
| `↑` / `↓` | 浏览历史命令 |
| `#` | 快速添加指令到 CLAUDE.md |
| `Esc` | 取消当前输入 |
| `Esc Esc` | 中断 Claude 操作并探索替代方案 |

## 四、CLAUDE.md：项目记忆文件

### 1. 什么是 CLAUDE.md？

`CLAUDE.md` 是一个特殊的 Markdown 文件，Claude Code 会在每次启动时自动读取它。你可以把它理解为「项目说明书」或「AI 助手的工作手册」。

**为什么需要它？**

LLM 是无状态的——每次对话开始，Claude 都是一张白纸。`CLAUDE.md` 就像是给 Claude 的「入职培训材料」，让它快速了解你的项目。

通过这个文件，你可以：

- 告诉 Claude 项目的技术栈和架构
- 定义代码风格规范和命名约定
- 说明常用命令和开发流程
- 记录项目特殊约定和注意事项
- 指定禁止修改的文件或目录

### 2. 文件位置与优先级

`CLAUDE.md` 可以放在多个位置，Claude 会按优先级合并读取：

| 位置 | 作用范围 | 是否提交 Git |
|------|----------|--------------|
| `~/.claude/CLAUDE.md` | 全局生效，所有项目 | 不提交 |
| 项目根目录 `CLAUDE.md` | 当前项目，团队共享 | ✅ 建议提交 |
| 项目根目录 `CLAUDE.local.md` | 当前项目，个人配置 | ❌ 不提交 |
| 子目录 `CLAUDE.md` | 特定目录 | 视情况 |

**示例场景**：

```
~/.claude/CLAUDE.md          # 你的全局偏好：使用中文回复、代码风格等
project/CLAUDE.md            # 项目规范：团队约定、技术栈、命令等
project/CLAUDE.local.md      # 你的个人设置：API Key 位置、本地路径等
project/src/api/CLAUDE.md    # API 模块专属规范：接口设计原则等
```

### 3. 快速创建

**方法一：自动生成**

```bash
# 进入项目目录
cd your-project

# 让 Claude 分析项目并生成
claude /init
```

Claude 会分析项目结构，自动生成一份初始配置：

```
Analyzing project structure...

Found:
- package.json (Node.js project)
- React components in src/
- Jest tests in __tests__/
- ESLint configuration

Generated CLAUDE.md with:
- Tech stack summary
- Common commands
- Code style guidelines
- Project structure overview

Review and edit as needed: ./CLAUDE.md
```

**方法二：从模板创建**

```bash
# 创建文件
touch CLAUDE.md

# 编辑
code CLAUDE.md  # 或 vim CLAUDE.md
```

**方法三：在对话中用 # 键快速添加**

```
你：记住，这个项目的测试命令是 npm run test:unit

[按 # 键]

Claude：已添加到 CLAUDE.md：
# 测试命令
- `npm run test:unit`：运行单元测试
```

### 4. 完整示例：前端项目

````markdown
# 项目说明

这是公司内部的电商管理后台，使用 React 18 + TypeScript + Ant Design。

# 技术栈

- 前端框架：React 18 + TypeScript
- UI 组件：Ant Design 5.x
- 状态管理：Zustand
- 请求库：Axios + React Query
- 构建工具：Vite
- 测试框架：Jest + React Testing Library

# 常用命令

- `pnpm dev`：启动开发服务器 (http://localhost:5173)
- `pnpm build`：构建生产版本
- `pnpm test`：运行所有测试
- `pnpm test:watch`：监听模式运行测试
- `pnpm lint`：运行 ESLint 检查
- `pnpm lint:fix`：自动修复 lint 问题
- `pnpm type-check`：运行 TypeScript 类型检查

# 代码规范

- 组件使用函数式 + Hooks，不要用 Class 组件
- 使用 TypeScript 严格模式，不允许 any
- CSS 使用 CSS Modules，文件名 `*.module.scss`
- 变量命名 camelCase，组件命名 PascalCase
- 每个组件一个文件夹，包含 index.tsx 和 index.module.scss

# 项目结构

```
src/
├── components/     # 通用组件
├── pages/          # 页面组件
├── hooks/          # 自定义 Hooks
├── services/       # API 请求
├── stores/         # Zustand 状态
├── utils/          # 工具函数
├── types/          # TypeScript 类型定义
└── constants/      # 常量定义
```

# Git 规范

- 提交信息格式：`<type>(<scope>): <description>`
- type: feat / fix / docs / style / refactor / test / chore
- 示例：`feat(user): 添加用户列表分页功能`

# 注意事项

- 提交前必须通过 lint 和 type-check
- 新功能必须有对应的单元测试
- API 密钥在 .env.local 文件，不要提交
- 不要直接修改 src/generated/ 目录（自动生成的代码）
````

### 5. 完整示例：后端项目

````markdown
# 项目说明

用户服务微服务，负责用户注册、登录、权限管理。

# 技术栈

- 语言：Go 1.21
- 框架：Gin
- 数据库：PostgreSQL 14 + Redis 7
- ORM：GORM
- 认证：JWT
- 文档：Swagger

# 常用命令

- `make run`：启动服务 (http://localhost:8080)
- `make test`：运行测试
- `make test-coverage`：生成覆盖率报告
- `make build`：编译生产版本
- `make docker-build`：构建 Docker 镜像
- `make migrate-up`：执行数据库迁移
- `make migrate-down`：回滚数据库迁移
- `make swagger`：生成 Swagger 文档

# 目录结构

```
├── cmd/            # 程序入口
├── internal/       # 内部包（不对外暴露）
│   ├── handler/    # HTTP 处理器
│   ├── service/    # 业务逻辑
│   ├── repository/ # 数据访问
│   └── model/      # 数据模型
├── pkg/            # 公共包（可对外暴露）
├── migrations/     # 数据库迁移文件
└── docs/           # Swagger 文档
```

# 代码规范

- 遵循 Go 官方代码规范
- 错误必须处理，不能忽略
- 使用结构化日志 (zerolog)
- 数据库操作必须在 repository 层
- 业务逻辑必须在 service 层

# 环境变量

```
DATABASE_URL=postgres://user:pass@localhost:5432/users
REDIS_URL=redis://localhost:6379
JWT_SECRET=xxx
```

# 注意事项

- 敏感配置在 .env 文件，不要提交
- 数据库迁移文件一旦提交不能修改，只能新增
- 所有 API 必须有 Swagger 注释
````

### 6. 完整示例：全局配置

在 `~/.claude/CLAUDE.md` 设置全局偏好：

```markdown
# 我的 Claude Code 偏好设置

## 语言

- 请始终使用中文与我交流
- 代码注释使用中文
- Git 提交信息使用中文

## 代码风格

- 优先使用函数式编程风格
- 变量和函数命名要语义化
- 复杂逻辑必须添加注释
- 不要使用缩写（除非是通用缩写如 API、URL）

## 工作习惯

- 修改代码前先解释你的思路
- 每次只做一件事，避免大范围修改
- 修改后告诉我如何验证

## 安全提醒

- 永远不要在代码中硬编码密码或 API Key
- 不要删除或覆盖 .env 文件
- 谨慎处理用户输入，防止注入攻击
```

### 7. 最佳实践

**保持简洁**：研究表明，LLM 能稳定遵循约 150-200 条指令，CLAUDE.md 建议控制在 100-300 行。

```markdown
# ❌ 不好的写法：啰嗦
我们的项目是一个电商系统，主要功能包括用户管理、商品管理、订单管理等。
这个项目使用了 React 作为前端框架，因为 React 是目前最流行的前端框架之一，
它具有组件化、虚拟 DOM 等特点...

# ✅ 好的写法：简洁
# 技术栈
- React 18 + TypeScript
- Node.js + Express
- PostgreSQL + Redis
```

**使用要点式**：用简短的要点代替长段落。

```markdown
# ❌ 不好的写法
当你需要运行测试的时候，你应该使用 npm run test 命令。如果你想要
运行单个测试文件，你可以使用 npm run test -- --testPathPattern=xxx。
另外，如果你想查看测试覆盖率，可以运行 npm run test:coverage。

# ✅ 好的写法
# 测试命令
- `npm test`：运行所有测试
- `npm test -- --testPathPattern=xxx`：运行指定文件
- `npm test:coverage`：生成覆盖率报告
```

**只写通用规则**：Claude 会忽略与当前任务无关的内容，所以只放普遍适用的信息。

**使用渐进式披露**：把详细信息放在单独文件，在 CLAUDE.md 中引用：

```markdown
# 更多信息

- API 设计规范见 `docs/api-guidelines.md`
- 数据库设计见 `docs/database-schema.md`
- 部署流程见 `docs/deployment.md`
```

## 五、Skills：技能系统

### 1. 什么是 Skills？

Skills（技能）是 Claude Code 的扩展系统，本质上是预设的 Markdown 指南。当你调用某个技能时，Claude 会自动加载对应的指南，按照指南完成任务。

**打个比方**：Skills 就像是「标准作业程序（SOP）」。比如 `/commit` 技能告诉 Claude：「生成提交信息时，要先看改了什么，然后按照 Conventional Commits 规范写」。

### 2. 内置技能详解

Claude Code 内置了一些常用技能：

| 技能 | 功能 | 使用场景 |
|------|------|----------|
| `/commit` | 智能生成 Git 提交信息 | 完成代码修改后 |
| `/review-pr` | 代码审查 | 审查团队成员的 PR |
| `/pdf` | 处理 PDF 文档 | 阅读、提取 PDF 内容 |
| `/docx` | 处理 Word 文档 | 编辑、生成 Word 文档 |
| `/xlsx` | 处理 Excel 表格 | 分析、生成 Excel 表格 |
| `/frontend-design` | 前端界面设计 | 实现 UI 设计稿 |
| `/bug` | 报告 Bug | 发现 Claude Code 问题时 |

**实际使用示例 - `/commit`**：

```
你：/commit

Claude：让我分析一下你的改动...

[Claude 执行 git diff]

检测到以下改动：
- 修改了 src/auth/login.js (登录逻辑优化)
- 新增了 src/auth/logout.js (退出登录功能)
- 修改了 tests/auth.test.js (补充测试用例)

建议的提交信息：

feat(auth): 优化登录逻辑并添加退出登录功能

- 重构登录验证流程，提升性能
- 新增 logout 接口，支持清除 session
- 补充 auth 模块单元测试

是否使用这个提交信息？(y/n/edit)

你：y

[Claude 执行 git commit]

✅ 提交成功！
```

**实际使用示例 - `/review-pr`**：

````
你：/review-pr 156

Claude：正在获取 PR #156 的信息...

PR #156: 添加购物车功能
作者: @developer
分支: feature/shopping-cart → main
改动: 12 个文件，+856/-23 行

开始审查...

[Claude 逐个分析改动文件]

---
## 代码审查报告

### ✅ 优点
1. 代码结构清晰，购物车逻辑封装在独立模块
2. 有完整的单元测试覆盖
3. 类型定义完善

### ⚠️ 建议改进
1. **src/cart/CartService.js:45** - 价格计算可能有精度问题
   ```javascript
   // 当前代码
   const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

   // 建议改为
   const total = items.reduce((sum, item) =>
     sum + Math.round(item.price * item.quantity * 100) / 100, 0);
   ```

2. **src/cart/CartContext.js:23** - 缺少错误处理
   建议添加 try-catch 包裹 API 调用

3. **tests/cart.test.js** - 缺少边界测试
   建议添加：空购物车、超大数量、负数价格等测试用例

### ❌ 需要修复
1. **src/cart/utils.js:12** - 可能导致 XSS 攻击
   ```javascript
   // 危险！直接使用用户输入
   innerHTML = `商品名: ${item.name}`;

   // 应该转义或使用 textContent
   textContent = `商品名: ${item.name}`;
   ```

### 总结
代码质量良好，修复 XSS 问题后可以合并。
````

**实际使用示例 - `/pdf`（适合行政、法务、财务）**：

```
你：/pdf 帮我分析这份供应商合同 contracts/supplier-2024.pdf

Claude：正在分析合同文件...

📄 合同基本信息：
- 合同名称：年度物料供应合同
- 甲方：我司
- 乙方：XX材料有限公司
- 签订日期：2024年3月15日
- 合同期限：2024年4月1日 - 2025年3月31日

💰 关键商业条款：
1. 合同总金额：580万元
2. 付款方式：月结30天
3. 违约金比例：合同金额的5%

⚠️ 需要注意的条款：
1. 第8.3条：供应商有权在原材料涨价超过10%时调整价格
2. 第12.1条：争议解决地为乙方所在地法院
3. 第15条：自动续约条款，需提前60天书面通知终止

📋 与上一版合同的主要差异：
- 付款周期从45天缩短至30天
- 新增了质量索赔的时效限制（7天）
- 删除了价格保护条款

需要我生成详细的合同摘要报告吗？
```

**实际使用示例 - `/xlsx`（适合财务、运营、销售）**：

```
你：/xlsx 分析一下 reports/sales-q4.xlsx 的销售数据

Claude：正在分析销售数据表格...

📊 Q4 销售数据分析报告

一、整体概况
- 总销售额：2,847 万元
- 同比增长：23.5%
- 环比增长：8.2%
- 订单数量：12,543 笔
- 客单价：2,270 元

二、产品销售排名
| 排名 | 产品类目 | 销售额 | 占比 | 同比 |
|------|----------|--------|------|------|
| 1 | 智能家居 | 892万 | 31.3% | +45% |
| 2 | 个护美妆 | 673万 | 23.6% | +18% |
| 3 | 数码配件 | 521万 | 18.3% | +12% |
| 4 | 家居日用 | 438万 | 15.4% | -5% |
| 5 | 其他 | 323万 | 11.4% | +8% |

三、区域分析
- 华东区贡献最大（42%），但增速放缓
- 西南区增速最快（+67%），值得重点投入
- 东北区下滑明显（-12%），需要分析原因

四、异常数据提醒
⚠️ 发现3条可能的数据错误：
- 第156行：单价为负数
- 第892行：数量超过10000（远超平均值）
- 第1203行：日期格式异常

需要我生成可视化图表或导出分析报告吗？
```

**实际使用示例 - `/docx`（适合行政、人事、市场）**：

```
你：/docx 帮我整理会议记录 notes/meeting-0115.txt 生成正式的会议纪要文档

Claude：正在处理会议记录并生成正式文档...

✅ 已生成会议纪要：docs/会议纪要-2024年度规划讨论会-0115.docx

📋 文档内容预览：

═══════════════════════════════════
    2024年度规划讨论会 会议纪要
═══════════════════════════════════

【会议信息】
- 时间：2024年1月15日 14:00-16:30
- 地点：公司3楼大会议室
- 主持人：张总
- 记录人：李秘书
- 参会人员：各部门负责人（共12人）

【会议议程】
1. 2023年度工作总结（30分钟）
2. 2024年度目标讨论（60分钟）
3. Q1重点项目确认（40分钟）
4. 其他事项（20分钟）

【主要决议】
1. 确定2024年营收目标为1.2亿元（同比+20%）
2. Q1启动新零售项目，预算300万
3. 3月底前完成组织架构调整

【待办事项】
| 事项 | 负责人 | 截止日期 |
|------|--------|----------|
| 提交部门年度计划 | 各部门 | 1月25日 |
| 新零售项目方案 | 市场部 | 2月10日 |
| 招聘计划初稿 | 人事部 | 1月30日 |

【下次会议】
- 时间：2024年1月29日 14:00
- 议题：Q1项目启动会

═══════════════════════════════════

文档已按照公司模板格式排版，包含页眉页脚和标准字体。
需要调整格式或补充内容吗？
```

### 3. 创建自定义技能

你可以创建自己的技能，存放在 `.claude/skills/` 目录：

```
.claude/
└── skills/
    └── my-skill/
        ├── skill.md       # 技能定义（必需）
        └── templates/     # 模板文件（可选）
```

**示例：创建一个「生成 API 文档」技能**

````markdown
# .claude/skills/api-docs/skill.md

# API 文档生成器

## 描述

为项目中的 API 接口生成 Markdown 格式的文档。

## 触发条件

当用户调用 /api-docs 时执行。

## 执行步骤

1. 扫描项目中的路由文件（支持 Express、Koa、Fastify）
2. 提取每个接口的信息：
   - 请求方法（GET/POST/PUT/DELETE）
   - 路径
   - 参数（path、query、body）
   - 响应格式
3. 按模块分组生成文档
4. 输出到 docs/api.md

## 文档格式

每个接口按以下格式输出：

### [方法] /路径

**描述**: 接口功能说明

**请求参数**:
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|

**响应示例**:
```json
{
  "code": 0,
  "data": {}
}
```

## 注意事项

- 如果接口有 JSDoc 注释，优先使用注释中的描述
- 敏感接口（如包含 password、token）要标注安全警告
- 废弃的接口要标注 [DEPRECATED]
````

**使用自定义技能**：

```
你：/api-docs

Claude：开始生成 API 文档...

[Claude 扫描路由文件]

发现 3 个路由模块：
- routes/auth.js (5 个接口)
- routes/users.js (8 个接口)
- routes/products.js (12 个接口)

正在生成文档...

[Claude 创建 docs/api.md]

✅ API 文档已生成！
文件位置: docs/api.md
包含 25 个接口的完整文档

要预览一下吗？
```

**示例：创建一个「组件生成器」技能**

````markdown
# .claude/skills/create-component/skill.md

# React 组件生成器

## 描述

快速创建符合项目规范的 React 组件。

## 参数

$ARGUMENTS - 组件名称

## 执行步骤

1. 解析组件名称，转换为 PascalCase
2. 在 src/components/ 下创建组件文件夹
3. 生成以下文件：
   - index.tsx (组件主文件)
   - index.module.scss (样式文件)
   - index.test.tsx (测试文件)
   - types.ts (类型定义)

## 模板

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

**使用**：

```
你：/create-component UserProfile

Claude：正在创建 UserProfile 组件...

[Claude 创建文件]

✅ 组件创建完成！

src/components/UserProfile/
├── index.tsx        # 组件主文件
├── index.module.scss # 样式文件
├── index.test.tsx   # 测试文件
└── types.ts         # 类型定义

组件已导出，可以这样使用：
import { UserProfile } from '@/components/UserProfile';
```

### 4. 技能市场

除了自己创建，你还可以使用社区分享的技能。官方维护了一个技能示例目录：

```bash
# 查看可用的示例技能
ls ~/.claude/skills/examples/

# 复制到项目中使用
cp -r ~/.claude/skills/examples/changelog .claude/skills/
```

## 六、Subagent：子代理系统

### 1. 什么是 Subagent？

Subagent（子代理）是 Claude Code 的高级功能，允许创建专门化的 AI 子实例。每个子代理有自己的：

- 独立上下文窗口
- 专业领域知识
- 可用工具集

**打个比方**：主 Claude 是「项目经理」，可以根据需要召唤不同的「专家顾问」来处理特定任务。这样做的好处是：

1. **节省 Token**：子代理有独立上下文，不会污染主对话
2. **专业性更强**：针对特定任务优化的提示词效果更好
3. **并行处理**：可以同时派出多个子代理处理不同任务

### 2. 内置子代理类型

| 类型 | 用途 | 可用工具 |
|------|------|----------|
| `Explore` | 快速探索代码库 | Read, Grep, Glob |
| `Plan` | 设计实现方案 | Read, Grep, Glob |
| `Bash` | 执行命令 | Bash |
| `code-reviewer` | 代码审查 | Read, Grep, Glob, Bash |
| `general-purpose` | 通用任务 | 全部工具 |

### 3. 实际使用场景

**场景一：探索大型代码库**

```
你：这个项目有几十万行代码，帮我找到所有处理支付的地方

Claude：这是一个大型代码库搜索任务，我来派出 Explore 子代理...

[Explore 子代理启动]

Explore Agent: 正在搜索支付相关代码...

搜索策略：
1. 文件名包含 pay/payment/checkout
2. 代码包含 payment/charge/refund 关键词
3. 目录结构分析

搜索结果：

📁 核心支付模块
├── src/services/payment/
│   ├── PaymentService.ts (支付服务主入口)
│   ├── StripeProvider.ts (Stripe 支付)
│   ├── AlipayProvider.ts (支付宝)
│   └── WechatPayProvider.ts (微信支付)

📁 支付相关接口
├── src/routes/payment.ts (支付 API 路由)
├── src/routes/webhook.ts (支付回调处理)

📁 支付相关组件
├── src/components/Checkout/ (结账页面)
├── src/components/PaymentForm/ (支付表单)

📁 支付工具函数
├── src/utils/payment.ts (价格计算、格式化)

共找到 23 个相关文件，要深入分析哪个部分？
```

**场景二：设计复杂功能**

````
你：我需要实现一个秒杀系统，帮我设计方案

Claude：这是一个需要仔细规划的复杂功能，让我派出 Plan 子代理...

[Plan 子代理启动]

Plan Agent: 正在分析项目现状并设计秒杀系统方案...

## 秒杀系统设计方案

### 一、系统分析

**现有架构**：
- 后端：Node.js + Express
- 数据库：PostgreSQL
- 缓存：Redis
- 队列：无（需要引入）

**流量预估**：
- 按 10000 QPS 设计

### 二、核心挑战

1. **高并发读**：秒杀页面的库存查询
2. **高并发写**：扣减库存、创建订单
3. **超卖问题**：库存不能变负数
4. **性能问题**：数据库扛不住峰值流量

### 三、技术方案

```
[用户] → [Nginx 限流] → [API 网关]
                              ↓
                     [Redis 预减库存]
                              ↓
                    [RabbitMQ 异步队列]
                              ↓
                    [订单服务消费处理]
                              ↓
                      [PostgreSQL]
```

### 四、关键实现

1. **库存预热**
   - 秒杀开始前将库存加载到 Redis
   - 使用 Redis 原子操作 DECR 扣减

2. **请求限流**
   - Nginx 层：IP 限流 100 req/s
   - API 层：用户级限流，每人每秒 1 次

3. **异步下单**
   - 库存扣减成功后发消息到队列
   - 消费者异步创建订单
   - 用户端轮询订单状态

4. **超卖防护**
   ```lua
   -- Redis Lua 脚本，原子性扣减
   if redis.call('GET', KEYS[1]) > 0 then
     return redis.call('DECR', KEYS[1])
   else
     return -1
   end
   ```

### 五、实现步骤

1. [ ] 安装配置 RabbitMQ
2. [ ] 实现 Redis 库存缓存层
3. [ ] 实现限流中间件
4. [ ] 实现秒杀接口
5. [ ] 实现订单消费者
6. [ ] 添加监控告警
7. [ ] 压力测试

### 六、文件清单

需要创建/修改的文件：
- `src/services/seckill/SeckillService.ts`
- `src/services/seckill/StockCache.ts`
- `src/services/seckill/OrderConsumer.ts`
- `src/middlewares/rateLimit.ts`
- `src/routes/seckill.ts`
- `docker-compose.yml` (添加 RabbitMQ)

预计工作量：3-5 天

---

这个方案是否符合你的需求？要我开始实现吗？
````

**场景三：代码审查**

````
你：帮我审查一下今天写的代码

Claude：让我派出 code-reviewer 子代理来审查...

[code-reviewer 子代理启动]

Code Reviewer: 正在检查今天的代码改动...

> git diff --stat HEAD~5

分析范围：最近 5 次提交，涉及 8 个文件

---

## 代码审查报告

### 📊 总体评分：7.5/10

### ✅ 优点

1. **命名清晰** - 变量和函数命名语义化
2. **模块化好** - 功能拆分合理
3. **有测试覆盖** - 新功能都有单元测试

### ⚠️ 建议改进

**1. src/services/UserService.ts:67**
```typescript
// 当前：N+1 查询问题
const users = await User.findAll();
for (const user of users) {
  user.orders = await Order.findByUserId(user.id); // 循环内查询
}

// 建议：使用 JOIN 或批量查询
const users = await User.findAll({
  include: [{ model: Order }]
});
```

**2. src/utils/validator.ts:23**
```typescript
// 当前：正则表达式可能导致 ReDoS
const emailRegex = /^([a-zA-Z0-9_\-\.]+)+@([a-zA-Z0-9_\-\.]+)+\.([a-zA-Z]{2,})$/;

// 建议：使用更安全的正则或库
import isEmail from 'validator/lib/isEmail';
```

**3. src/components/DataTable.tsx:45**
- 缺少 loading 状态处理
- 缺少空数据提示
- 建议添加错误边界

### ❌ 必须修复

**1. src/routes/api.ts:89** - SQL 注入风险！
```typescript
// 危险代码
const query = `SELECT * FROM users WHERE name = '${req.query.name}'`;

// 必须使用参数化查询
const users = await User.findAll({
  where: { name: req.query.name }
});
```

### 📝 其他建议

- 添加 API 请求的超时处理
- 考虑添加请求重试机制
- 建议补充边界测试用例

---

需要我帮你修复这些问题吗？
````

**场景四：市场竞品调研（适合市场、运营人员）**

```
你：帮我收集一下主要竞品最近的动态，我要准备下周的竞品分析会

Claude：这是一个信息收集任务，我来派出 Explore 子代理帮你搜集资料...

[Explore 子代理启动]

Explore Agent: 正在收集竞品信息...

收集范围：
1. 各竞品官网产品更新
2. 公开的新闻报道和PR稿
3. 社交媒体官方账号动态
4. 行业报告和分析文章

---

## 竞品动态汇总报告（最近30天）

### 竞品A - XX科技

📢 重大动态：
- 1月8日：发布新版App 5.0，主打AI推荐功能
- 1月3日：宣布完成C轮融资2亿美元
- 12月28日：与YY平台达成战略合作

💡 产品更新：
- 新增智能客服机器人
- 优化了搜索算法
- 上线会员积分体系

📊 市场动作：
- 在地铁投放大量广告
- 开启春节促销活动

### 竞品B - ZZ互联

📢 重大动态：
- 1月10日：CEO在行业峰会发表演讲
- 1月5日：开放API接口给第三方开发者
- 12月25日：推出企业版产品

💡 产品更新：
- 大幅降价（平均降幅20%）
- 新增数据导出功能
- 改进了移动端体验

### 竞品C - WW网络

📢 重大动态：
- 1月12日：传闘在筹备IPO
- 1月6日：裁员消息（未经证实）

---

📎 我已将详细资料整理到 reports/竞品分析-202401.xlsx
包含：时间线、信息来源链接、截图存档

需要我针对某个竞品深入分析吗？
```

**场景五：财务报表整理（适合财务人员）**

```
你：帮我把这个月的费用报销单都整理一下，按部门汇总

Claude：这是一个数据整理任务，我来派出子代理帮你处理...

[general-purpose 子代理启动]

正在扫描费用报销文件夹...

发现 47 份报销单据：
- PDF 扫描件：32 份
- Excel 表格：10 份
- 图片（发票照片）：5 份

正在提取和核对信息...

---

## 2024年1月费用报销汇总

### 按部门统计

| 部门 | 笔数 | 金额（元）| 占比 |
|------|------|----------|------|
| 销售部 | 18 | 45,680.00 | 38.2% |
| 市场部 | 12 | 32,150.00 | 26.9% |
| 技术部 | 8 | 18,900.00 | 15.8% |
| 行政部 | 5 | 12,300.00 | 10.3% |
| 人事部 | 4 | 10,500.00 | 8.8% |
| **合计** | **47** | **119,530.00** | **100%** |

### 按费用类型统计

| 类型 | 金额（元）| 占比 |
|------|----------|------|
| 差旅费 | 52,300.00 | 43.8% |
| 招待费 | 28,400.00 | 23.8% |
| 办公费 | 18,200.00 | 15.2% |
| 交通费 | 12,630.00 | 10.6% |
| 其他 | 8,000.00 | 6.7% |

### ⚠️ 异常提醒

发现 3 笔需要关注的报销：

1. **销售部-王xx** - 招待费 8,500 元
   - 超过单笔5000元审批标准
   - 缺少招待对象说明

2. **市场部-李xx** - 差旅费 6,200 元
   - 住宿费超标（实际450/晚，标准350/晚）
   - 建议补充超标说明

3. **技术部-张xx** - 办公费 3,800 元
   - 发票日期为去年11月，超过报销时限

---

📊 汇总表已导出：reports/费用报销汇总-202401.xlsx
📋 异常报销清单：reports/待处理报销-202401.xlsx

需要我生成给领导的报销情况简报吗？
```

**场景六：行政文档批量处理（适合行政人员）**

```
你：公司有200多个制度文件要更新，把里面的公司旧名称都改成新名称

Claude：这是一个批量文档处理任务，我来派出子代理处理...

[general-purpose 子代理启动]

正在扫描制度文件夹...

发现 238 个文档文件：
- Word文档(.docx)：156 个
- PDF文件：52 个
- Excel表格：30 个

正在分析文档内容...

---

## 文档批量更新报告

### 任务概述
- 替换内容：「XX有限公司」→「XX集团股份有限公司」
- 涉及文件：238 个

### 处理结果

✅ **已完成更新**：186 个文件

| 文件类型 | 数量 | 替换处数 |
|----------|------|----------|
| Word文档 | 156 | 1,247 处 |
| Excel表格 | 30 | 89 处 |

⚠️ **需要手动处理**：52 个文件

PDF 文件无法直接编辑，已生成替换清单：
- 文件名
- 页码
- 需替换位置的截图标注

📁 **输出文件夹结构**：
```
制度文件_已更新/
├── 已更新/           # 156个Word + 30个Excel
├── 待手动处理/        # 52个PDF文件
├── 原文件备份/        # 所有原始文件
└── 处理报告.xlsx      # 详细替换日志
```

### 额外发现

在处理过程中还发现：
1. 有 12 个文件包含已过期的联系电话
2. 有 8 个文件的落款日期超过3年未更新
3. 有 5 个文件存在两个版本（可能重复）

是否需要一并处理这些问题？
```

### 4. 创建自定义子代理

在 `.claude/agents/` 目录创建配置文件：

**示例：创建一个「安全审计」子代理**

```yaml
# .claude/agents/security-auditor.yaml

name: security-auditor
description: "安全审计专家，专门检查代码中的安全漏洞"

system_prompt: |
  你是一位资深的安全审计专家，精通 OWASP Top 10 和各类安全漏洞。

  在审计代码时，重点检查：

  1. 注入攻击
     - SQL 注入
     - NoSQL 注入
     - OS 命令注入
     - LDAP 注入

  2. 认证与会话管理
     - 弱密码策略
     - 会话固定
     - 不安全的 Token 存储

  3. 敏感数据暴露
     - 硬编码的密钥/密码
     - 明文传输敏感数据
     - 日志中的敏感信息

  4. XSS 跨站脚本
     - 反射型 XSS
     - 存储型 XSS
     - DOM 型 XSS

  5. 不安全的反序列化
  6. 使用含已知漏洞的组件
  7. 不足的日志记录和监控

  发现问题时，要给出：
  - 问题位置（文件:行号）
  - 风险等级（严重/高/中/低）
  - 问题描述
  - 修复建议
  - 修复代码示例

tools:
  - Read
  - Grep
  - Glob
  - Bash

max_tokens: 8000
```

**示例：创建一个「性能优化」子代理**

```yaml
# .claude/agents/performance-optimizer.yaml

name: performance-optimizer
description: "性能优化专家，分析和优化代码性能"

system_prompt: |
  你是一位性能优化专家，精通前端和后端的性能调优。

  分析时关注：

  前端性能：
  - 包体积分析
  - 渲染性能
  - 内存泄漏
  - 网络请求优化

  后端性能：
  - 数据库查询优化
  - 缓存策略
  - 并发处理
  - 内存使用

  给出建议时要：
  - 量化性能提升（如：减少 50% 加载时间）
  - 提供具体的代码修改
  - 说明优化原理
  - 评估实现成本

tools:
  - Read
  - Grep
  - Glob
  - Bash

max_tokens: 8000
```

**使用自定义子代理**：

````
你：用 security-auditor 检查一下登录模块

Claude：让我派出安全审计专家检查登录模块...

[security-auditor 子代理启动]

Security Auditor: 开始安全审计 src/auth/ 目录...

## 安全审计报告 - 登录模块

### 🔴 严重问题 (2)

**1. SQL 注入风险**
- 文件：`src/auth/login.js:34`
- 风险等级：严重
```javascript
// 问题代码
const user = await db.query(
  `SELECT * FROM users WHERE email = '${email}'`
);

// 修复方案
const user = await db.query(
  'SELECT * FROM users WHERE email = $1',
  [email]
);
```

**2. 密码明文日志**
- 文件：`src/auth/login.js:28`
- 风险等级：严重
```javascript
// 问题代码
console.log(`Login attempt: ${email}, password: ${password}`);

// 修复方案
console.log(`Login attempt: ${email}`);
// 永远不要记录密码！
```

### 🟠 高风险问题 (3)

**1. 缺少登录频率限制**
- 可能被暴力破解
- 建议：添加 rate limiting，如 5 次失败后锁定 15 分钟

**2. 弱密码策略**
- 当前：仅要求 6 位以上
- 建议：至少 8 位，包含大小写字母和数字

**3. Session 未绑定 IP**
- 会话可能被劫持
- 建议：将 Session 与客户端 IP 绑定

### 🟡 中等风险 (2)

（详细内容...）

### 📊 审计统计

- 扫描文件：12 个
- 发现问题：7 个
  - 严重：2
  - 高：3
  - 中：2

建议优先修复严重和高风险问题。需要我帮你修复吗？
````

## 七、配置与权限管理

### 1. 配置文件层级

Claude Code 使用三层配置文件，优先级从高到低：

| 文件 | 位置 | 用途 | 是否提交 Git |
|------|------|------|--------------|
| 本地配置 | `.claude/settings.local.json` | 个人偏好 | ❌ 不提交 |
| 项目配置 | `.claude/settings.json` | 团队共享 | ✅ 提交 |
| 用户配置 | `~/.claude/settings.json` | 全局设置 | - |

### 2. 权限管理详解

Claude Code 默认会在执行敏感操作前请求确认。你可以预先授权或禁止某些操作：

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

**权限规则详解**：

| 规则 | 含义 |
|------|------|
| `Read` | 允许读取任意文件 |
| `Write(src/**)` | 允许写入 src 目录下的所有文件 |
| `Bash(npm *)` | 允许执行 npm 开头的命令 |
| `Read(.env*)` | 禁止读取 .env 开头的文件 |
| `Bash(rm -rf *)` | 禁止执行危险的删除命令 |

**实际效果**：

```
你：帮我删除 node_modules 目录

Claude：我需要执行 rm -rf node_modules。
但根据配置，我没有权限执行 rm -rf 命令。

建议手动执行：
rm -rf node_modules

或者修改 .claude/settings.json 添加权限：
"allowedTools": ["Bash(rm -rf node_modules)"]
```

### 3. 完整配置示例

```json
{
  "model": "sonnet",
  "allowedTools": [
    "Read",
    "Write(src/**)",
    "Write(tests/**)",
    "Write(docs/**)",
    "Bash(npm *)",
    "Bash(pnpm *)",
    "Bash(git *)",
    "Bash(docker *)",
    "Bash(make *)"
  ],
  "deniedTools": [
    "Read(.env*)",
    "Write(.env*)",
    "Read(**/*secret*)",
    "Write(**/*secret*)",
    "Read(**/*credential*)",
    "Write(**/*credential*)",
    "Bash(rm -rf /)",
    "Bash(sudo *)",
    "Bash(* > /dev/*)",
    "Bash(curl * | bash)"
  ],
  "autoApprove": {
    "read": true,
    "edit": false,
    "write": false,
    "bash": false
  },
  "gitConfig": {
    "autoCommit": false,
    "commitMessageTemplate": "<type>(<scope>): <description>",
    "signCommits": true
  }
}
```

### 4. 环境变量

```bash
# 认证相关
export ANTHROPIC_API_KEY=sk-ant-xxxxx  # API Key 认证

# 模型选择
export CLAUDE_MODEL=sonnet             # 默认模型

# 代理设置（企业网络）
export HTTPS_PROXY=http://proxy.company.com:8080
export HTTP_PROXY=http://proxy.company.com:8080

# 调试
export CLAUDE_DEBUG=true               # 开启调试日志
```

### 5. Hooks：自动化钩子

Hooks 允许你在 Claude 执行某些操作前后自动运行命令：

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

**实际效果**：

```
Claude：我刚创建了 src/components/Button.tsx

[PostToolUse Hook 触发]
> npx prettier --write src/components/Button.tsx
> npx eslint --fix src/components/Button.tsx

文件已自动格式化。
```

## 八、高级使用技巧

### 1. 探索-计划-编码-提交 工作流

这是官方推荐的最佳实践工作流：

```
# 第一步：探索
你：帮我了解一下用户认证是怎么实现的

Claude：[使用 Explore 子代理搜索代码库]
找到了，让我给你梳理一下认证流程...

# 第二步：计划
你：我想添加 OAuth2 登录，帮我设计方案

Claude：[使用 Plan 子代理设计方案]
我来制定一个详细的实现计划...

你：这个方案不错，但我们用 Passport.js 而不是自己实现

Claude：好的，我调整一下方案...

# 第三步：编码
你：开始实现吧

Claude：[按计划逐步实现]
我先安装依赖，然后创建配置文件...

# 第四步：提交
你：/commit

Claude：[分析改动，生成提交信息]
建议的提交信息：feat(auth): 添加 Google OAuth2 登录支持
```

### 2. 测试驱动开发（TDD）

```
# 第一步：让 Claude 写测试
你：为用户登录功能编写单元测试，要覆盖以下场景：
    - 正常登录
    - 密码错误
    - 用户不存在
    - 账户被锁定

Claude：[创建测试文件]
我创建了 tests/auth/login.test.ts，包含 12 个测试用例...

# 第二步：运行测试（应该失败）
你：运行测试

Claude：
> npm test tests/auth/login.test.ts

❌ 12 个测试，12 个失败
这是预期的，因为功能还没实现。

# 第三步：实现功能
你：现在实现功能让测试通过

Claude：[实现代码]
我来实现登录逻辑...

# 第四步：验证
你：再运行一次测试

Claude：
> npm test tests/auth/login.test.ts

✅ 12 个测试，12 个通过
所有测试都通过了！
```

### 3. 多窗口并行工作

使用 Git Worktree 在多个终端同时运行 Claude Code：

```bash
# 终端 1：继续主分支的工作
cd project
claude

# 终端 2：同时处理紧急 Bug 修复
git worktree add ../project-hotfix hotfix/payment-bug
cd ../project-hotfix
claude
```

**好处**：
- 两个 Claude 实例独立工作，互不影响
- 可以同时处理不同的任务
- 避免频繁切换分支导致的上下文丢失

### 4. CI/CD 集成

**GitHub Actions 示例**：

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
          claude -p "审查这个 PR 的代码改动，检查：
          1. 代码质量和最佳实践
          2. 潜在的 Bug
          3. 安全问题
          4. 性能问题

          输出 Markdown 格式的审查报告。" > review.md

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

**自动生成发布说明**：

```bash
# 获取两个版本之间的提交
git log v1.0.0..v1.1.0 --oneline | claude -p "
根据这些 Git 提交记录，生成发布说明。

格式要求：
## 版本 1.1.0

### ✨ 新功能
- ...

### 🐛 Bug 修复
- ...

### 📝 其他改动
- ...
"
```

### 5. 管道操作

结合 Unix 管道使用 Claude：

```bash
# 分析错误日志
cat error.log | claude -p "分析这些错误日志，找出最常见的问题和解决建议"

# 实时监控日志
tail -f app.log | claude -p "监控这个日志流，发现以下情况时立即提醒我：
1. 错误率突然上升
2. 响应时间超过 2 秒
3. 数据库连接失败"

# 代码统计分析
find src -name "*.ts" | xargs wc -l | claude -p "分析这个代码统计，告诉我：
1. 哪些模块代码量最大
2. 是否有需要拆分的大文件"

# 依赖分析
npm list --json | claude -p "分析这个依赖树，找出：
1. 过时的依赖
2. 有已知安全漏洞的依赖
3. 可以合并的重复依赖"
```

### 6. 图片辅助开发

Claude Code 支持直接处理图片：

```bash
# 方式一：直接拖拽图片到终端
claude "按照这个设计稿实现页面" [拖入设计图]

# 方式二：粘贴截图
# macOS: Cmd+Ctrl+Shift+4 截图后 Cmd+V 粘贴

# 方式三：引用图片文件
claude "分析 @./designs/homepage.png 这个设计稿，告诉我需要哪些组件"
```

**实际对话**：

```
你：[拖入设计稿图片]
    按这个设计稿实现登录页面

Claude：我分析了这个设计稿，需要实现以下元素：

布局：
- 左侧：品牌 Logo + 装饰图
- 右侧：登录表单

表单元素：
- 标题 "Welcome Back"
- 邮箱输入框
- 密码输入框（带显示/隐藏切换）
- "记住我" 复选框
- "忘记密码" 链接
- 登录按钮（渐变色 #6366f1 → #8b5cf6）
- 分割线 "Or continue with"
- 社交登录按钮（Google、GitHub、Apple）
- "还没有账户？注册" 链接

样式细节：
- 圆角：12px
- 阴影：柔和投影
- 字体：Inter

开始实现吗？
```

### 7. 使用检查清单管理大任务

对于复杂任务，让 Claude 创建检查清单来跟踪进度：

```
你：帮我把项目从 JavaScript 迁移到 TypeScript，先列个清单

Claude：好的，我来创建一个迁移清单：

## JavaScript → TypeScript 迁移清单

### 阶段一：基础设置
- [ ] 安装 TypeScript 和类型定义
- [ ] 创建 tsconfig.json
- [ ] 配置构建工具支持 TS
- [ ] 更新 ESLint 配置

### 阶段二：核心文件迁移
- [ ] src/index.js → src/index.ts
- [ ] src/app.js → src/app.ts
- [ ] src/config/ (5 个文件)
- [ ] src/utils/ (12 个文件)

### 阶段三：业务逻辑迁移
- [ ] src/services/ (8 个文件)
- [ ] src/controllers/ (15 个文件)
- [ ] src/middlewares/ (6 个文件)

### 阶段四：类型定义
- [ ] 创建 API 请求/响应类型
- [ ] 创建数据库模型类型
- [ ] 创建配置类型

### 阶段五：测试与验证
- [ ] 更新测试文件
- [ ] 运行类型检查
- [ ] 运行测试套件
- [ ] 构建生产版本

---

总计：约 50 个文件需要迁移
预计工作量：2-3 天

从哪个阶段开始？

你：从阶段一开始

Claude：开始阶段一：基础设置

[x] 安装 TypeScript 和类型定义
> npm install -D typescript @types/node @types/express

[x] 创建 tsconfig.json
[Claude 创建配置文件]

[x] 配置构建工具支持 TS
[Claude 修改 webpack.config.js]

[x] 更新 ESLint 配置
[Claude 修改 .eslintrc.js]

✅ 阶段一完成！

要继续阶段二吗？
```

## 九、MCP：模型上下文协议

### 1. 什么是 MCP？

MCP（Model Context Protocol）是一个开放协议，让 Claude Code 能够安全地连接外部工具和数据源。

**打个比方**：如果说 Claude 的大脑是「思考能力」，那 MCP 就是给它装上了「手」——让它能操作各种外部系统。

```
┌─────────────────┐
│   Claude Code   │
└────────┬────────┘
         │ MCP 协议
         ▼
┌────────────────────────────────────────────┐
│              MCP 服务器                      │
├──────────┬──────────┬──────────┬───────────┤
│ GitHub   │ Slack    │ Database │ FileSystem│
│ 服务器    │ 服务器    │ 服务器    │ 服务器     │
└──────────┴──────────┴──────────┴───────────┘
```

### 2. 添加 MCP 服务器

```bash
# 添加文件系统访问（扩展访问范围）
claude mcp add filesystem -- npx @modelcontextprotocol/server-filesystem /path/to/allowed/dir

# 添加 GitHub 集成
claude mcp add github -- npx @modelcontextprotocol/server-github

# 添加 Slack 集成
claude mcp add slack -- npx @modelcontextprotocol/server-slack

# 添加 SQLite 数据库
claude mcp add sqlite -- npx @modelcontextprotocol/server-sqlite /path/to/database.db

# 添加 PostgreSQL
claude mcp add postgres -- npx @modelcontextprotocol/server-postgres "postgresql://user:pass@localhost/db"

# 添加浏览器自动化
claude mcp add puppeteer -- npx @modelcontextprotocol/server-puppeteer
```

### 3. 常用 MCP 服务器及使用场景

| 服务器 | 功能 | 使用场景 |
|--------|------|----------|
| **filesystem** | 文件系统访问 | 访问项目外的文件 |
| **github** | GitHub 操作 | 管理仓库、PR、Issue |
| **slack** | Slack 消息 | 发送通知、读取频道消息 |
| **sqlite** | SQLite 数据库 | 查询本地数据库 |
| **postgres** | PostgreSQL | 查询生产数据库 |
| **puppeteer** | 浏览器自动化 | 网页测试、截图、爬虫 |
| **notion** | Notion 文档 | 读写 Notion 页面 |
| **google-drive** | Google Drive | 读取云端文档 |
| **figma** | Figma 设计 | 获取设计稿信息 |

### 4. 实际使用示例

**示例：GitHub 集成**

```
你：帮我看看 PR #156 的状态，如果检查都通过了就合并

Claude：让我通过 GitHub MCP 查看...

[通过 MCP 调用 GitHub API]

PR #156 状态：
- 标题：添加用户导出功能
- 作者：@developer
- CI 检查：✅ 全部通过 (3/3)
- 审查：✅ 已批准 (2 人)
- 冲突：无

所有条件满足，正在合并...

[通过 MCP 执行合并]

✅ PR #156 已成功合并到 main 分支！
```

**示例：数据库查询**

```
你：帮我查一下昨天新注册了多少用户，按渠道分组

Claude：让我查询数据库...

[通过 MCP 连接 PostgreSQL]

> SELECT channel, COUNT(*) as count
  FROM users
  WHERE created_at >= '2025-01-13'
  GROUP BY channel
  ORDER BY count DESC;

查询结果：

| 渠道 | 新用户数 |
|------|----------|
| organic | 1,234 |
| google_ads | 567 |
| referral | 234 |
| facebook | 123 |

总计：2,158 新用户

要我生成一份详细报告吗？
```

**示例：Slack 通知**

```
你：部署完成后，在 #deployments 频道发个通知

Claude：好的，让我发送 Slack 消息...

[通过 MCP 发送 Slack 消息]

✅ 已发送到 #deployments：

---
🚀 **部署通知**

**服务**: user-service
**版本**: v1.2.3
**环境**: production
**时间**: 2025-01-14 15:30:00

**改动摘要**:
- 添加用户导出功能
- 修复登录超时问题
- 优化数据库查询性能

**部署者**: @bruce
---
```

### 5. 配置 MCP 服务器

MCP 配置存储在 `~/.claude/mcp.json`：

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

## 十、不同角色的使用指南

### 1. 开发工程师

**日常开发流程**：

```bash
# 早上：继续昨天的工作
claude -c

# 遇到问题：快速求助
claude "这个报错什么意思？[粘贴报错]"

# 代码审查：自动审查自己的代码
claude "审查一下我今天的改动"

# 下班前：整理提交
claude /commit
```

**常用提示词模板**：

```
# 新功能开发
"帮我实现 [功能描述]，要求：
1. [具体要求1]
2. [具体要求2]
参考现有的 [相似功能/文件]"

# Bug 修复
"[报错信息]
这个错误发生在 [场景描述]
帮我找出原因并修复"

# 代码重构
"重构 @[文件路径]，目标：
1. 提高可读性
2. 减少重复代码
3. 保持现有功能不变"

# 性能优化
"@[文件路径] 这个文件性能有问题，
现象是 [问题描述]
帮我分析并优化"
```

### 2. 产品经理

**了解技术实现**：

```
你：我想了解用户注册流程的技术实现，不需要代码细节，
    只需要告诉我整体架构和关键节点

Claude：让我帮你梳理一下...

用户注册流程概览：

1. **前端表单提交**
   - 用户填写：邮箱、密码、昵称
   - 前端验证：格式、强度

2. **后端处理**
   - 验证邮箱是否已注册
   - 密码加密存储
   - 生成验证码

3. **邮件发送**
   - 发送验证邮件
   - 有效期 24 小时

4. **邮箱验证**
   - 用户点击链接
   - 激活账户

5. **数据存储**
   - 用户表 (users)
   - 验证记录表 (verifications)

整个流程约 3-5 秒完成注册，邮件可能延迟 1-2 分钟。

有什么想深入了解的吗？
```

**验证需求可行性**：

```
你：我想做一个功能：用户可以用微信扫码登录，
    技术上能实现吗？需要什么条件？

Claude：这个功能可以实现。让我分析一下...

## 微信扫码登录技术分析

### 可行性：✅ 可实现

### 前置条件
1. **微信开放平台账号**
   - 需要企业资质认证
   - 费用：300元/年

2. **已备案域名**
   - 回调地址必须备案
   - 需要 HTTPS

3. **开发工作量**
   - 前端：约 2 天
   - 后端：约 3 天
   - 测试：约 2 天

### 用户体验流程
1. 用户点击「微信登录」按钮
2. 页面显示二维码
3. 用户打开微信扫码
4. 微信弹出授权确认
5. 用户同意后自动登录

### 注意事项
- 首次登录需绑定手机号（建议）
- 需处理微信昵称特殊字符
- 需缓存头像到自己服务器

### 替代方案
如果暂时没有企业资质，可以考虑：
- 手机号验证码登录
- 邮箱登录

需要我整理一份详细的需求文档吗？
```

### 3. 运维人员

**编写监控脚本**：

```
你：帮我写一个监控脚本，每 5 分钟检查一次服务器状态，
    CPU 超过 80% 或内存超过 90% 就发邮件告警

Claude：好的，我来创建监控脚本...

[创建 monitor.sh]

脚本已创建！功能说明：

📄 monitor.sh

功能：
- 每 5 分钟检查 CPU 和内存使用率
- 超过阈值发送邮件告警
- 记录日志到 /var/log/monitor.log

使用方法：

1. 配置邮件信息
   export ALERT_EMAIL=ops@company.com
   export SMTP_SERVER=smtp.company.com

2. 设置执行权限
   chmod +x monitor.sh

3. 添加到 crontab
   */5 * * * * /path/to/monitor.sh

4. 查看日志
   tail -f /var/log/monitor.log

要我帮你部署吗？
```

**分析日志**：

```
你：分析一下这份错误日志，找出主要问题

[粘贴日志]

Claude：让我分析这份日志...

## 日志分析报告

### 时间范围
2025-01-14 10:00 - 11:00（1 小时）

### 问题概览

| 错误类型 | 次数 | 占比 |
|----------|------|------|
| 数据库连接超时 | 156 | 45% |
| Redis 连接失败 | 89 | 26% |
| 请求超时 | 67 | 19% |
| 其他错误 | 35 | 10% |

### 根因分析

**主要问题：数据库连接池耗尽**

10:15 开始出现大量数据库连接超时：
```
[10:15:23] Error: Connection pool exhausted, waiting...
[10:15:24] Error: Query timeout after 30000ms
```

**原因推测**：
1. 连接池配置过小（当前：10，建议：50）
2. 存在慢查询未释放连接
3. 10:00-10:15 流量峰值

**关联问题**：
- Redis 失败是因为重试机制导致雪崩
- 请求超时是数据库问题的连锁反应

### 建议措施

**紧急**：
1. 增加数据库连接池大小
2. 重启 Redis 连接

**长期**：
1. 添加慢查询告警
2. 优化高频查询
3. 增加熔断机制

需要我帮你修改配置吗？
```

### 4. 非技术人员

**学习编程**：

````
你：我是财务，完全不懂编程，但想学着用 Python 处理 Excel
    能从最基础的教我吗？

Claude：当然可以！让我从最基础的开始教你。

## Python 处理 Excel 入门教程

### 第一步：理解基本概念

把 Python 想象成一个「超级计算器」：
- 你给它指令
- 它帮你执行
- 就像 Excel 里的公式，但更强大

### 第二步：写第一个程序

创建一个文件 `hello.py`，内容：

```python
print("你好，我开始学 Python 了！")
```

运行方式：
1. 打开终端（Windows 按 Win+R，输入 cmd）
2. 输入 python hello.py
3. 你会看到打印出的文字

### 第三步：处理 Excel

这是一个简单的例子：

```python
# 导入 Excel 处理工具（就像 Excel 里的插件）
import pandas as pd

# 读取 Excel 文件
data = pd.read_excel("销售数据.xlsx")

# 查看前几行
print(data.head())

# 计算销售额总和
total = data["销售额"].sum()
print(f"总销售额: {total}")
```

我帮你创建这个文件吗？你可以用你自己的 Excel 试试。
````

**自动化日常工作**：

```
你：我每天要把下载文件夹里的 PDF 发票按月份整理到不同文件夹，
    能自动化吗？

Claude：完全可以！我来帮你创建一个自动整理脚本。

[创建 organize_invoices.py]

脚本已创建！使用方法超级简单：

### 使用步骤

1. **双击运行**
   - 直接双击 `运行整理.bat` 文件
   - 或者双击 `organize_invoices.py`

2. **它会自动**
   - 扫描「下载」文件夹里的所有 PDF
   - 读取文件修改日期
   - 创建「2025年01月」这样的文件夹
   - 把文件移动到对应月份的文件夹

3. **运行结果**
   下载/
   ├── 2025年01月/
   │   ├── 发票001.pdf
   │   └── 发票002.pdf
   ├── 2024年12月/
   │   └── 发票003.pdf
   └── organize_invoices.py

### 设置定时运行（可选）

如果想每天自动运行：
1. 打开「任务计划程序」
2. 创建基本任务
3. 设置每天下午 6 点运行

要我帮你设置定时任务吗？
```

## 十一、常见问题解答

### 1. 安装问题

**Q: 安装后无法运行，提示 command not found**

```bash
# 1. 重新加载 Shell 配置
source ~/.bashrc  # Bash 用户
source ~/.zshrc   # Zsh 用户

# 2. 检查 PATH
echo $PATH | grep -i claude

# 3. 手动添加到 PATH（如果需要）
export PATH="$HOME/.claude/bin:$PATH"

# 4. 运行诊断
claude doctor
```

**Q: 安装时报错 permission denied**

```bash
# 不要使用 sudo！这是常见错误
# ❌ 错误
sudo npm install -g @anthropic-ai/claude-code

# ✅ 正确：使用推荐的安装方式
curl -fsSL https://claude.ai/install.sh | bash
```

**Q: Windows 上安装失败**

```powershell
# 1. 确保以管理员身份运行 PowerShell

# 2. 设置执行策略
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 3. 重新安装
irm https://claude.ai/install.ps1 | iex
```

### 2. 认证问题

**Q: 浏览器登录后 CLI 没反应**

```bash
# 检查是否在等待认证
# 如果卡住了，按 Ctrl+C 取消，然后重试

# 或者使用 API Key 方式
export ANTHROPIC_API_KEY=sk-ant-xxxxx
claude
```

**Q: 提示订阅无效**

```
确认以下几点：
1. 你的 Claude 订阅是否激活？
2. 是 Pro/Max/Teams/Enterprise 版本吗？
3. 登录的是否是正确的账号？

可以访问 https://claude.ai/settings 检查订阅状态
```

### 3. 使用问题

**Q: Claude 不理解我的项目**

```
解决方案：

1. 确保在项目根目录运行
   cd /path/to/your/project
   claude

2. 创建 CLAUDE.md 文件
   claude /init

3. 使用 @ 引用具体文件
   claude "帮我看看 @./src/main.js 这个文件"

4. 给足够的上下文
   claude "这是一个 React 项目，使用 TypeScript，
          帮我在 src/components 下创建一个 Button 组件"
```

**Q: 对话太长导致响应变慢或报错**

```bash
# 方案 1：压缩历史（保留上下文摘要）
> /compact

# 方案 2：清空重新开始（完全清除）
> /clear

# 方案 3：开始新会话
> /exit
claude
```

**Q: Claude 修改了不该改的文件**

```bash
# 1. 用 Git 回退
git checkout -- path/to/file

# 2. 配置禁止访问
# 在 .claude/settings.json 添加：
{
  "deniedTools": [
    "Write(path/to/protected/**)"
  ]
}
```

**Q: 如何查看 Claude 要执行什么操作**

```
Claude 在执行敏感操作前会请求确认：

Claude: 我需要执行以下操作：
        [Write] 创建文件 src/new-file.js
        [Bash] npm install lodash

        确认执行？(y/n/explain)

输入 explain 可以让 Claude 解释为什么要这样做
```

### 4. 性能问题

**Q: 响应很慢**

```
可能原因和解决方案：

1. 网络问题
   - 检查网络连接
   - 如果在公司网络，配置代理

2. 对话太长
   - 使用 /compact 压缩历史

3. 项目太大
   - 使用 @ 指定具体文件，而不是让 Claude 全局搜索

4. 模型选择
   - 简单任务用 Sonnet，更快
   claude --model sonnet
```

**Q: Token 消耗太快**

```bash
# 1. 查看当前消耗
> /cost

# 2. 减少消耗的技巧：
- 精简 CLAUDE.md
- 避免让 Claude 读取大文件
- 用具体的问题代替开放性问题
- 完成一个任务后 /clear 开始新任务
```

### 5. 安全问题

**Q: Claude 会看到我的敏感信息吗？**

```
Claude Code 的安全机制：

1. 默认不读取 .env 文件
2. 可以配置禁止访问敏感文件
3. 执行敏感操作前会请求确认

你可以这样加强保护：

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

**Q: 代码会被发送到云端吗？**

```
是的，与 Claude 的交互会发送到 Anthropic 的服务器。

但是：
1. Anthropic 不会用你的代码训练模型
2. 对话数据有保留期限
3. 企业版可以选择私有部署

如果项目高度敏感，建议：
1. 使用企业版私有部署
2. 或者使用 Amazon Bedrock / Google Vertex AI 版本
```

**Q: 如何防止 Claude 执行危险命令？**

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

## 十二、总结

Claude Code 是一个强大的 AI 编程助手，它的核心优势在于：

### 核心价值

1. **终端原生**：无需切换窗口，在开发环境中直接使用
2. **可执行操作**：不只是聊天，而是真正能动手干活
3. **理解上下文**：能分析整个代码库，给出针对性建议
4. **高度可定制**：通过 CLAUDE.md、Skills、Subagent 扩展能力

### 适用场景

| 场景 | 推荐用法 |
|------|----------|
| 日常开发 | 交互式对话 `claude` |
| 快速提问 | 带问题启动 `claude "问题"` |
| 自动化流程 | 单次模式 `claude -p "指令"` |
| 代码审查 | `/review-pr` 技能 |
| 项目初始化 | `/init` 生成 CLAUDE.md |
| CI/CD 集成 | GitHub Actions + claude -p |

### 学习路径建议

**第一周：入门**
- 安装并完成认证
- 学会基本对话
- 创建第一个 CLAUDE.md

**第二周：进阶**
- 熟悉斜杠命令
- 学会使用内置技能
- 配置权限和设置

**第三周：高级**
- 创建自定义技能
- 使用 Subagent
- 集成 MCP 服务器

**持续优化**
- 根据使用经验完善 CLAUDE.md
- 创建适合团队的自定义工具
- 分享最佳实践

无论你是想提高编码效率的开发者、需要处理数据的业务人员、管理团队的技术负责人，还是想自动化日常工作的行政财务同学，Claude Code 都值得一试。它代表了 AI 工具的未来方向——不是替代人类，而是成为每个人的智能助手，帮你把繁琐的工作交给 AI，让你专注于更有价值的事情。

**相关链接**：

- [Claude Code 官方文档](https://code.claude.com/docs/en/overview)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude Code 最佳实践](https://www.anthropic.com/engineering/claude-code-best-practices)
- [CLAUDE.md 写作指南](https://www.humanlayer.dev/blog/writing-a-good-claude-md)
- [Claude Code 命令速查表](https://shipyard.build/blog/claude-code-cheat-sheet/)


## 相关阅读

- [Claude Code 命令大全（高频命令速查）](/zh/posts/ai/2025-01-23-claude-code-commands/)
- [Claude Code Hooks 机制详解（自动化关键）](/zh/posts/ai/2026-02-18-claude-code-hooks-guide/)
- [Claude Code 浏览器自动化方案对比](/zh/posts/ai/2026-01-28-claude-code-browser-automation/)
- [OpenClaw 使用教程（从单工具到多 Agent）](/zh/posts/ai/2026-02-12-openclaw-usage-tutorial/)
- [Codex CLI 实战指南（跨工具工作流）](/zh/posts/ai/2026-02-12-codex-cli-mastery-guide/)
