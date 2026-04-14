+++
date = '2026-04-14T10:00:00+08:00'
draft = false
title = 'OpenClaw 工具与 Skill 完全手册 2026：内置工具清单 + 自定义开发'
description = 'OpenClaw 2026 内置工具完整参数速查，含 write tool 的 path 和 content 参数详解、ClawHub skill 加载机制、SKILL.md 格式、tavily-search 配置，以及国内网络下的自定义 Skill 开发实操。'
toc = true
image = "cover.webp"
tags = ['OpenClaw', 'AI Agent Framework', 'ClawHub', 'Skills', 'Developer Tools']
keywords = ['OpenClaw 工具', 'OpenClaw Skill 开发', 'ClawHub skill', 'SKILL.md 格式', 'tavily-search 配置', 'OpenClaw Write 参数', 'OpenClaw 自定义 Skill', 'OpenClaw 国内网络']

[[params.faqItems]]
question = "OpenClaw 的 tavily-search skill 是什么，怎么配置？"
answer = "tavily-search 是 ClawHub 里最常用的联网搜索 skill，位置在 clawhub/skills/tavily-search/SKILL.md。参数包括 query（必填）、max_results（默认 5）、search_depth（basic 或 advanced）、include_domains/exclude_domains。配置三步：1) openclaw skills install tavily-search；2) 在 ~/.openclaw/.env 里写入 TAVILY_API_KEY；3) openclaw skills list 验证加载。国内用户需要给 api.tavily.com 配代理，否则会超时。"

[[params.faqItems]]
question = "怎么写一个自定义的 OpenClaw Skill？"
answer = "在 <workspace>/clawhub/skills/<skill 名字>/ 下创建 SKILL.md 即可，不需要写任何代码。SKILL.md 的 frontmatter 必须有 name 和 description 两个字段，description 决定 agent 什么时候调用这个 skill（所以要写成触发条件而不是名词标题）。skill 文件夹里可以放脚本、模板，body 里用相对路径引用。保存后执行 openclaw skills reload 即可生效。"

[[params.faqItems]]
question = "openclaw write tool 的 path 和 content 参数怎么用？"
answer = "openclaw write tool 只接受两个参数：path 和 content，都是必填字符串。path 必须是**绝对路径**（以 / 或 Windows 盘符开头），不会展开 ~ 也不会按 cwd 解析相对路径——填错了会直接报 'parent directory not found'。content 是字面量的文件全文，原样写入，不做任何模板替换、变量插值或编码转换，永远以 UTF-8 写。Write 没有 append/mode/encoding 这类可选参数，它永远是**整体覆盖**。要追加内容就先 Read、拼接、再 Write；要写二进制就把内容 base64 编码放进 content，后面用 Bash 步骤解码。"

[[params.faqItems]]
question = "OpenClaw 的 Write 工具有哪些参数？"
answer = "Write 工具只有两个参数：path（必填，必须是绝对路径）和 content（必填，完整文件内容字符串）。会直接覆盖已有文件不会提示。注意 Write 不会自动创建父目录，所以调用前要先用 Bash mkdir -p 建好。另外 content 是字面量，不会做任何模板渲染或环境变量替换。"

[[params.faqItems]]
question = "遇到 permission denied 怎么排查？"
answer = "OpenClaw 有本地权限白名单，位置在 ~/.openclaw/permissions.json。任何不在白名单里的 Bash 命令都需要交互式确认。在 CI 环境里用 openclaw permissions add 'git *' 提前加白，或直接编辑 permissions.json 的 allowedCommands 数组。如果是文件读写报错，先检查路径是不是绝对路径——OpenClaw 不会展开 ~ 也不会按 cwd 解析相对路径。"

[[params.faqItems]]
question = "OpenClaw 从哪些目录加载 skill？优先级如何？"
answer = "OpenClaw 按三级优先级加载：1) <workspace>/clawhub/skills/（项目级，最高优先级）；2) ~/.openclaw/skills/（用户级）；3) ClawHub 远程仓库（系统级，本地有缓存）。同名 skill 按优先级覆盖。openclaw skills list 会打印每个 skill 实际加载的路径，可以看到哪一级生效。"
+++

![OpenClaw 工具与 Skill 完全手册 2026 封面图展示 ClawHub skill 架构与工具参数](cover.webp)

写了半年 OpenClaw，我发现国内社区最缺的不是概念文章，而是**查得到参数的工具手册**。半夜 agent 报错，你需要的不是"什么是 Skill 的设计哲学"，而是"Write 工具第二个参数到底叫 content 还是 text"、"SKILL.md 的 frontmatter 是不是必须用三个短横线"、"tavily-search 在国内网络下为啥加载不出来"。

这篇文章就是这份手册。覆盖 **OpenClaw 2026** 的 9 个内置工具、ClawHub skill 加载机制、SKILL.md 完整契约、tavily-search 实操配置、自定义 skill 开发流程，以及我踩过的 5 个常见坑。如果你已经在用 OpenClaw 写 skill，建议直接 Ctrl+F 找你要的工具名；如果刚入门，先看 [OpenClaw 架构深度解析](/zh/posts/ai/2026-02-14-openclaw-architecture-deep-dive/)。

---

## 为什么需要这份手册

OpenClaw 官方文档是**为理解设计的，不是为查询设计的**。想知道 skill 的哲学？官网写得不错。想知道 Write 工具到底有几个参数？你得翻三篇教程交叉对照才能确认。

我吃过这个亏。去年调试一个自定义 skill 加载失败，我花了两小时才发现是 SKILL.md 的 `---` 分隔符被编辑器替换成了全角破折号。后来写一个 CI 脚本调用 OpenClaw，我凭直觉给 Bash 工具的 `timeout` 参数传了 `60`，结果命令直接被杀——因为那个字段单位是**毫秒**不是秒。这些时间本来都是可以省的，只要有一张查询表。

另外一个动机是 **GSC 数据**。我自己博客的搜索后台显示，"openclaw write tool parameters path content"、"openclaw clawhub skill skill.md tavily-search" 这些长尾词合计有**上万次展示**，但点击率接近 0——因为没有任何一篇文章直接回答这些问题。所有现有文章都在讲理念。这个位置有一个巨大的"参考手册"形状的空洞。

---

## 9 个内置工具的精确签名

OpenClaw 内置 9 个工具，除非在 `openclaw.json` 里通过 `disabled_tools` 显式禁用，否则每个 agent 都能用。下面给出每个工具的**精确参数名、类型、最常踩的坑**。

### Read——读文件

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `path` | string | 是 | **必须绝对路径**；相对路径在部分平台静默失败 |
| `offset` | integer | 否 | 起始行号（1-indexed） |
| `limit` | integer | 否 | 最大读取行数，默认 2000 |

**最常见的错**是传相对路径。OpenClaw 不会展开 `~` 也不会按当前工作目录解析，它把字符串按字面量使用。一定要传 `/Users/你/project/config.json` 这种完整路径。

读目录会报错不会列出内容，想列目录用 Glob 或 Bash `ls`。读超过 2000 行的文件会被**静默截断**——想读完整文件就要循环传 `offset` 和 `limit`。

### Write——写文件

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `path` | string | 是 | 绝对路径；父目录必须已存在 |
| `content` | string | 是 | 完整内容；直接覆盖不会提示 |

三个团队踩过同一个坑：Write **不会自动创建父目录**。如果调用 `Write("/tmp/new/sub/file.txt", "...")` 但 `/tmp/new/sub` 不存在，直接报错——不会静默 mkdir。正确做法是先用 Bash 跑一次 `mkdir -p`。

第二个坑是 `content` **完全按字面量写入**。OpenClaw 不做任何模板渲染、不替换环境变量、不转义特殊字符。你传什么，磁盘上就是什么。

### Edit——改文件

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `path` | string | 是 | 绝对路径，文件必须存在 |
| `old_string` | string | 是 | 除非 `replace_all=true`，否则必须唯一 |
| `new_string` | string | 是 | 必须与 `old_string` 不同 |
| `replace_all` | boolean | 否 | 默认 false |

**同一会话中必须先 Read 后 Edit**。OpenClaw 强制这个规则以防止覆盖 agent 没看过的改动。跳过 Read 会直接报 "file not read in this session"。

`old_string` 必须唯一这个约束是编辑失败的主因。如果你想替换 `return x` 但文件里有三处，Edit 会拒绝执行。解决办法是加上足够的上下文（通常 2-3 行），让字符串在整个文件里唯一。

### Bash——跑命令

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `command` | string | 是 | 单条 shell 命令；链式用 `&&` |
| `timeout` | integer | 否 | **毫秒**，默认 120000，最大 600000 |
| `run_in_background` | boolean | 否 | 异步执行，Monitor 流式读 |

OpenClaw 的 Bash 在持久工作目录里跑，但**不共享 shell 状态**——你在一次调用里 `export FOO=bar`，下一次调用看不到。需要在单次调用内生效就内联前缀：`PATH=/opt/tools:$PATH mytool`。

`timeout` 单位是**毫秒**，不是秒。我见过有人传 `timeout: 60` 期望 1 分钟，结果立刻被杀。

### Grep——搜内容

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `pattern` | string | 是 | 完整 ripgrep 正则语法 |
| `path` | string | 否 | 文件或目录，默认 cwd |
| `glob` | string | 否 | 如 `*.py` |
| `output_mode` | enum | 否 | `files_with_matches`（默认）/`content`/`count` |
| `-n` | boolean | 否 | 显示行号，仅 `output_mode: content` 有效 |
| `-i` | boolean | 否 | 忽略大小写 |
| `-C` | integer | 否 | 上下文行数 |
| `multiline` | boolean | 否 | 跨行匹配 |

Grep 底层是 ripgrep，所以字面花括号需要转义（`interface\{\}`），`.` 默认不匹配换行。`output_mode` 最值得记——默认 `files_with_matches` 只返回路径列表，这正是你后续 Read 时想要的。

### Glob——找文件

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `pattern` | string | 是 | 如 `**/*.ts` |
| `path` | string | 否 | 搜索目录 |

用 Glob **按文件名找文件**，不是按内容。结果按修改时间排序（最新优先），查"我最近改过哪些文件"特别好用。

### Task——派生子 agent

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `description` | string | 是 | 任务标题 |
| `prompt` | string | 是 | 给子 agent 的完整指令 |
| `subagent_type` | string | 是 | 已注册的 agent 类型名 |

Task 会派生一个拥有独立上下文窗口的子 agent。**子 agent 看不到父会话**——你需要的所有信息都要塞进 `prompt` 里。返回值是子 agent 的最终消息，不包含它的中间工具调用。

### TodoWrite——维护任务列表

| 参数 | 类型 | 必填 | 备注 |
|------|------|------|------|
| `todos` | array | 是 | 每次调用**替换**整个列表 |

替换语义是反直觉的。TodoWrite 不是追加，而是每次传完整的当前状态，包括已完成和进行中的项。忘了这点，agent 会以为任务丢了。

### WebFetch / WebSearch——联网

这两个受 `openclaw.json` 里 `webAccess` 策略管控。参数简单（WebFetch 传 `url`、WebSearch 传 `query`），但如果没返回结果，**先看 `webAccess.allowedDomains`**——OpenClaw 在 production 模式下默认拒绝非白名单域名。国内用户还要注意，如果通过代理访问，代理配置在 `~/.openclaw/proxy.json`，不是操作系统的 `HTTP_PROXY`。

---

## ClawHub Skill 架构

OpenClaw 最容易混淆的地方是 "skill" 有两层含义：一层是**内置工具**（runtime 硬编码的 Read/Write 那些），另一层是 **ClawHub skill**（SKILL.md + 附加文件）。这一节讲后者。

### SKILL.md 格式

每个 ClawHub skill 是一个文件夹，里面必须有 `SKILL.md`。frontmatter 的契约极简：

```markdown
---
name: my-skill-name
description: 当用户提到 X、Y、Z 时触发，用来完成 A、B、C 操作。
---

# Skill Body

skill 被触发后 agent 读到的指令。
可以包含代码块、示例、引用其他文件。
```

我违反过、也后悔过的两条规则：

**`description` 不是文档，是触发条件。** OpenClaw 会把每个 skill 的 `description` 塞进 agent 的 system prompt 作为"工具目录"。如果写"处理天气相关请求"，agent 可能会用；如果写"天气 skill"，agent 永远不知道什么时候该用。把 description 写成**触发条件句**，不是名词标题。

**附加文件放在 skill 文件夹内，用相对路径引用。** skill 需要一个 Python 脚本？把它放在 SKILL.md 旁边，在 body 里写 `执行 scripts/fetch.py`。agent 会以 skill 文件夹为根解析路径。不要写绝对路径——别的用户安装后会全部失效。

### 加载优先级

OpenClaw 按三级目录扫描，越具体越优先：

1. `<workspace>/clawhub/skills/` ——项目级，最高
2. `~/.openclaw/skills/` ——用户级
3. ClawHub 远程仓库 ——系统级，本地有缓存

同名 skill 按上述顺序覆盖。跑 `openclaw skills list` 可以看每个 skill 实际加载的路径，谁覆盖谁一眼看清。

### tavily-search 完整配置（国内场景）

tavily-search 是最常被搜索的 ClawHub skill，这里给出国内网络下的实操配置。skill 位置 `clawhub/skills/tavily-search/SKILL.md`，参数：

| 参数 | 类型 | 默认 | 备注 |
|------|------|------|------|
| `query` | string | 必填 | 自然语言查询 |
| `max_results` | integer | 5 | 1-20，越多费用越高 |
| `search_depth` | string | `basic` | basic(1 积分)/advanced(2 积分) |
| `include_domains` | array | 无 | 限定搜索域名 |
| `exclude_domains` | array | 无 | 排除域名 |
| `include_answer` | boolean | true | 返回 Tavily 的 AI 摘要 |

配置步骤：

```bash
# 1. 安装 skill
openclaw skills install tavily-search

# 2. 写入 API Key
echo 'TAVILY_API_KEY=tvly-xxxx' >> ~/.openclaw/.env

# 3. 国内用户必须配代理
cat > ~/.openclaw/proxy.json <<EOF
{
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "allowedDomains": ["api.tavily.com"]
}
EOF

# 4. 验证
openclaw skills list | grep tavily
```

**国内替代方案**：如果你不想折腾海外 API，可以自己写一个基于 Bing/SerpAPI 的 skill，只需要一份 SKILL.md + 一个 curl 命令，参考下一节的自定义 skill 示例改造即可。实际用下来，国内查中文内容用 Bing 的准确率反而比 Tavily 高。

如果 `openclaw skills list` 没显示 tavily-search，九成是 SKILL.md 的 frontmatter `---` 被富文本编辑器替换成了特殊字符。用 `hexdump -C SKILL.md | head` 看前几个字节，正常的 `---` 是 `2d 2d 2d`；如果看到 `e2 80 94`（em dash）就得重写。

---

## 自定义一个可用的 Skill

下面是一个最小可用的 skill，查询指定城市的当前天气。保存到 `<workspace>/clawhub/skills/weather/SKILL.md`：

```markdown
---
name: weather
description: 当用户询问某个城市的当前天气、温度、气象时触发。调用 wttr.in 返回简短天气摘要。
---

# Weather Skill

被触发时，从用户消息中提取城市名，执行：

    curl -s "wttr.in/${CITY}?format=3"

解析输出，用友好的一句话回复。
如果城市名不明确（如"老家"），先向用户确认。
```

就这样——不用注册、不用编译。保存后 `openclaw skills reload`，agent 就能用。

三条分辨"能用的 skill"和"不能用的 skill"的原则：

**让 description 承担加载权重。** agent 在决定是否调用之前**只看 description**，根本看不到 body。如果 description 不能让触发条件一眼可见，agent 就会漏调。我第一个 skill 的 description 改了三次，agent 才开始稳定触发。

**body 写成动作导向。** body 是 agent **已经决定**调用之后才读的。所以不要写"这个 skill 是用来...的"这种导言，直接列步骤。

**用 git 管理 skill 目录。** 每个上过生产的 skill 都至少经历过一次 regression。skill 是纯文本文件夹，在 skill 根目录 `git init` 零成本。更深入的版本管理策略在 [OpenClaw 记忆管理策略](/zh/posts/ai/2026-01-31-openclaw-memory-strategy/) 里讲过。

---

## OpenClaw vs CrewAI vs AutoGen vs LangGraph

这张对比表是我当初选型时希望有的。四个框架理论上都能搭多 agent 系统，差别在**胶水代码由谁写**。

| 维度 | OpenClaw | CrewAI | AutoGen | LangGraph |
|------|----------|--------|---------|-----------|
| 语言 | 单二进制（Go） | Python | Python / .NET | Python / JS |
| Agent 定义 | SOUL.md + SKILL.md | Python 类 | Python dataclass | 图节点 |
| 多 agent 路由 | 8 级 bindings + Lobster | Crew 编排 | GroupChat | 显式图边 |
| 消息通道 | 内置（飞书/Slack/企微） | 自己搭 | 自己搭 | 自己搭 |
| Skill 开发 | Markdown 文件，零代码 | Python tool 类 | Python 函数 | Python 函数 |
| 部署 | `openclaw serve` | 你的框架 | 你的框架 | 你的框架 |
| 适合场景 | IM/ChatOps 机器人 | 研究型工作流 | 对话式多 agent | 复杂有状态图 |

我在四个框架里都实际跑过项目后的真实推荐：

**选 OpenClaw**：agent 要长期驻在聊天渠道里（飞书、企微、Discord），且希望非工程同事能提交 skill。文件系统优先的设计是杀手锏——PM 可以直接提 PR 加 skill，不用学 Python。

**选 CrewAI**：一次性研究管道。给一个话题、研究、写报告、结束。CrewAI 的 Process 抽象（sequential、hierarchical）为这种场景而生。

**选 AutoGen**：任务中途需要 agent 互相对话的场景。AutoGen 的 GroupChat 比 OpenClaw 的 `sessions_send` 成熟。

**选 LangGraph**：工作流本身就是有状态、有循环、有条件分支的图。如果你在纸上画过状态机，选它。

**不推荐**用 OpenClaw 做纯 CLI 工具或批处理任务，除非已经在用它做别的事。它的渠道优先设计对这种场景是过度设计。这一点我在 [OpenClaw vs 传统 AI Agent 框架](/zh/posts/ai/2026-03-05-openclaw-vs-ai-agents/) 里有更详细的拆解。

---

## 5 个常见错误与修复

按我收到求助的频率排序。

**"skill 加载了但从不触发"**：description 写得太含糊。运行 `openclaw debug tools` 看 agent 实际看到的工具目录。如果 description 是名词短语（"天气工具"），改成触发条件句（"当用户询问某个城市的天气时"）。

**"Write 报 parent directory not found"**：Write 不会 mkdir。前面加 `Bash: mkdir -p $(dirname /path/to/file)`。

**"Edit 报 string not unique"**：`old_string` 匹配到多处。加上下文让它唯一，或者传 `replace_all: true`——但前提是你真的想改所有地方。

**"两个相似 skill agent 选错"**：skill 名字和 description 在触发空间里竞争。如果同时存在 `search-web` 和 `search-docs`，其中一个的 description 要写得更具体（"用于公司内部文档"vs"用于公网"）。用 `openclaw skills list` 把 description 并排看清再决定。

**"Bash 报 permission denied"**：查 `~/.openclaw/permissions.json`。OpenClaw 本地权限白名单，没匹配的命令要交互确认。CI 环境提前用 `openclaw permissions add "git *"` 加白。完整权限模型在 [OpenClaw 多 Agent 配置指南](/zh/posts/ai/2026-04-02-openclaw-multi-agent-setup-guide/) 里。

---

## 记住三件事

如果只带走三点：

**把 description 当触发条件写，不是标题。** 这是 skill 开发第一大错，几乎没有之一。

**所有路径都用绝对路径。** 每个涉及文件的工具（Read、Write、Edit、Glob）都只认绝对路径。相对路径会以让你浪费几小时的方式静默失败。

**把这篇加入书签。** OpenClaw 大版本之间参数名会变，但查询手册的形状稳定。agent 出问题时，十有八九是参数名错了、frontmatter 字段缺了，或者 skill 放错文件夹。先查表再提 bug。

想深入了解生产环境多 agent 模式，[OpenClaw 自动化避坑指南](/zh/posts/ai/2026-02-14-openclaw-automation-pitfalls/) 列了启发本文一半内容的生产事故；社区 skill 浏览去 [ClawHub 官方仓库](https://clawhub.dev)。

## 相关阅读

- [OpenClaw 架构深度解析](/zh/posts/ai/2026-02-14-openclaw-architecture-deep-dive/) ——Gateway-Agent-Skill 模型
- [OpenClaw 多 Agent 配置指南](/zh/posts/ai/2026-04-02-openclaw-multi-agent-setup-guide/) ——bindings、Lobster、成本优化
- [OpenClaw vs 传统 AI Agent 框架](/zh/posts/ai/2026-03-05-openclaw-vs-ai-agents/) ——框架对比
- [OpenClaw 自动化避坑指南](/zh/posts/ai/2026-02-14-openclaw-automation-pitfalls/) ——生产事故案例
- [OpenClaw 记忆管理策略](/zh/posts/ai/2026-01-31-openclaw-memory-strategy/) ——SOUL.md 与记忆治理
