+++
date = '2026-07-05T10:00:00+08:00'
aliases = ['/posts/ai/2026-07-09-loop-engineering/']
draft = false
title = 'Loop Engineering 循环工程:给 AI Agent 造一个笼子'
description = '循环工程(Loop Engineering)是 2026 年 AI Agent 工程栈的最外层学科。四大支柱——上下文保洁、刹车机制、毒舌评审、幂等工具——每根都配可直接抄的伪代码和真实翻车案例。核心立场:模型是水电煤,循环护栏才是护城河。'
toc = true
tags = ['AI Agent', 'Loop Engineering', 'Agent Guardrails', 'Agentic Harness', 'Building AI Agents']
keywords = ['循环工程', 'loop engineering', 'agent 护栏', '智能体工程', 'agent 笼子', 'agent loop 工程']

[[params.faqItems]]
question = "什么是循环工程(Loop Engineering)?"
answer = "循环工程是设计 AI Agent 运行所在的那个控制循环的学科——不是调 prompt、也不是换模型,而是造那个决定「何时压缩上下文、何时刹车、何时打回 Agent 自己的作业、能碰哪些工具」的笼子。它叠在 prompt 工程、上下文工程、harness 工程之上,是 2026 年 Agent 技术栈的最外层。"

[[params.faqItems]]
question = "循环工程的四大支柱是什么?"
answer = "一是保持上下文干净(Compact 压缩、Offload 转存、Sub-agent 隔离脏活);二是知道何时停(最大迭代数、预算与时间上限、无进展检测、机器可验证的完成检查);三是引入能说「不」的评审(分离 Maker 和 Checker,让测试/类型检查能打回);四是给它真能用的工具(少而精、无重叠、写操作幂等,重试才安全)。"

[[params.faqItems]]
question = "为什么 AI Agent 的工具必须做成幂等的?"
answer = "Agent 有 15%-30% 的概率会重试工具调用(超时、校验失败、模型犹豫)。如果一个非幂等的写操作在超时前其实已经成功,重试就会再执行一遍——重复下单、重复插行、重复扣款。给每个写操作加一个由入参推导的幂等键,重试就从「数据污染」变成了「安全空操作」。"

[[params.faqItems]]
question = "循环工程和 harness 工程是一回事吗?"
answer = "不是。Harness 工程管的是 Agent 运行的环境——它能碰的工具、文件、MCP 连接器。循环工程管的是驱动 Agent 走向目标的那个迭代控制环:上下文管理、终止、验证、工具收敛。循环工程包住 harness 工程,而不是取代它。"

[[params.faqItems]]
question = "为什么不能让 Agent 自己评审自己的产出?"
answer = "让 Agent 给自己的产出打分,几乎永远是满分——同一个 Maker 又当 Checker,自评永远 100。可靠的验证必须把两者分开:一个独立评审(确定性测试、类型检查,或换一个带毒舌指令的模型)能给出一个硬性的「不」,把作业打回循环重写。"
+++

![循环工程:2026 年 AI Agent 运行所在的四支柱笼子](cover.webp)

84%——这是 Anthropic 在一个 100 轮网页搜索评测里砍掉的 token 消耗比例,而模型一个权重都没动。同样的模型、同样的 API,全部收益来自[上下文编辑](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):一个发生在控制循环层面的改动。这门手艺现在有名字了:**循环工程**(Loop Engineering),给 AI Agent 造笼子的学科。

同一组评测还有两个数字:单是上下文编辑就带来 29% 的表现提升,配上 memory 工具冲到 39%。2026 年没有任何一次模型升级,能用这么低的成本换来这么大的提升。做到这件事的,是一次循环层的改动。

这个收据就是全文论点的浓缩版。所有人都在优化那头野兽,而真正有沉淀的工程在笼子里。模型是野兽——强、迭代快、越来越像按 token 计费的水电煤。笼子是那个控制循环:何时给 Agent 的记忆瘦身、何时急刹、何时把作业摔回它脸上、允许它碰哪些工具。

把 Opus 换成 GPT-5.x 再换成 Gemini,你的 Agent 会聪明一点点。但笼子造错,它们中任何一个都会心甘情愿地在一夜之间烧掉 $200,再送你一个红色的 CI 当早安。

我的核心立场:**模型是水电煤,循环和它的护栏才是护城河**。

这是我之前那篇[《Agentic Loops:自循环 AI Agent 全解》](/zh/posts/ai/2026-07-03-agentic-loops/)的工程姊妹篇。那篇讲 Agent 循环「是什么」「何时跑」;这篇讲「怎么造笼子」——四根承重支柱,每根配一段能直接抄走的伪代码,和一个跳过它就翻车的真实案例。

## 循环工程一个月内从玄学变成学科

命名的收敛本身就是证据。这个词在 2026 年 6 月定型:Google 的 Addy Osmani 发了那篇文章,用一篇解读的话说,「给了这门实践一个名字,更有用的是给了它一套解剖学」。Peter Steinberger 和 Boris Cherny 从编码 Agent 的一线收敛到同一个想法。swyx 更早就在用「loopcraft(循环术)」绕着它打转。

LangChain 干脆把它形式化成[四层循环](https://www.langchain.com/blog/the-art-of-loop-engineering):Agent 循环、验证循环、事件循环,外加一个从生产 trace 反向改进内层循环的爬山循环。前沿实验室的声音、框架厂商、一线实践者,在同一个月里各自独立给同一样东西命名——玄学变学科,就长这个样子。

它的位置很好摆:四层技术栈的最外层,每层包住前一层而不取代它。Prompt 工程(2022-2024)是你发出去的词。[上下文工程](/zh/posts/ai/2026-06-16-context-engineering-2026/)(2025)是模型在某次调用里看到的每一个 token。Harness 工程(2026 年初)是环境——Agent 能碰的工具、文件、MCP 连接器。

**循环工程(2026)是驱动这一切走向目标的迭代循环**。它负责问那些不性感但要命的运营问题:对话越来越长了,压缩还是继续?Agent 说它做完了,真的吗?它想写数据库,这个写操作重试安全吗?

这些问题没有一个关于模型。每一个都关于笼子。

本文剩下的部分就是笼子的四根支柱。缺任何一根,你就重新打开一个具体而昂贵的翻车模式——我会逐一点名。

```mermaid
flowchart TB
    subgraph CAGE["笼子 —— 循环工程"]
        direction TB
        P1["支柱一<br/>上下文保洁<br/>压缩 / 转存 / 隔离"]
        P2["支柱二<br/>知道何时停<br/>迭代 / 预算 / 无进展 / 完成检查"]
        P3["支柱三<br/>会说不的评审<br/>Maker ≠ Checker"]
        P4["支柱四<br/>真能用的工具<br/>少 / 无重叠 / 幂等"]
    end
    MODEL["模型<br/>(水电煤 —— 随便换)"] --> LOOP((Agent<br/>循环))
    LOOP --> P1 --> P2 --> P3 --> P4 --> LOOP
    style CAGE fill:#12233a,stroke:#4da6ff,color:#fff
    style LOOP fill:#1a5e2a,stroke:#3ddc84,color:#fff
    style MODEL fill:#3a2f12,stroke:#e0a53d,color:#fff
    style P1 fill:#1f3a5f,stroke:#4da6ff,color:#fff
    style P2 fill:#1f3a5f,stroke:#4da6ff,color:#fff
    style P3 fill:#1f3a5f,stroke:#4da6ff,color:#fff
    style P4 fill:#1f3a5f,stroke:#4da6ff,color:#fff
```

## 支柱一:别让上下文馊掉

长循环最大的敌人不是笨模型,是一份被污染的上下文。每一坨没用的工具输出、每一条过期报错、每一个被放弃却还赖在窗口里的旧计划,都让下一次推理调用更差一点——而且这个劣化会跨轮次复利。

业界的表述很直接。HumanLayer 的 [12-factor agents](https://github.com/humanlayer/12-factor-agents) 把「拥有你的上下文窗口」列为第 3 条、「把报错压缩进上下文窗口」列为第 9 条——因为默认行为(让历史堆着,好让 Agent「什么都记得」)恰恰在跟模型的真实脾性对着干。

**把上下文窗口当成一笔要花的预算,而不是一个往里塞的仓库**。

减脏的动作恰好三个,工程到位的循环三个全用。**压缩**去减:对话逼近窗口上限时总结掉,从总结重新起一个窗口。**转存**去挪:4 万 token 的文件 dump 或命令输出扔到磁盘,上下文里只留真正要用的那五行。**子 Agent** 去隔离:脏活丢给一个自带干净窗口的独立 Agent,只让压缩后的结果回来。

开头那组数字就住在这根支柱里:单靠上下文编辑 29%,配 memory 工具 39%;100 轮评测 token 砍掉 84%,还顺带救活了本来会因上下文耗尽而失败的任务。Anthropic 的多 Agent 研究系统把隔离做得更彻底:子 Agent 只回传 1000-2000 token 的压缩摘要给主 Agent,详细检索上下文被隔离在该待的地方。

```python
# 支柱一 —— 三个动作,写在循环的控制代码里(不是模型的活)
def step(ctx, task):
    result = agent.act(ctx, task)          # 模型调了个工具

    # 转存:绝不把一大坨结果粘回上下文
    if len(result.output) > OFFLOAD_BYTES:
        path = write_to_disk(result.output)
        result.output = f"[已写入 {len(result.output)}B 到 {path};要用就去 grep]"

    ctx.append(result)

    # 压缩:在窗口馊掉之前压,不是之后
    if ctx.tokens > 0.75 * WINDOW:
        ctx = compact(ctx)                 # 总结旧轮次,保留 spec + 未完成 TODO

    return ctx

# 隔离:脏活跑在一次性的窗口里
def research(question):
    sub = spawn_subagent(fresh_context=True)
    return sub.run(question).summary       # 只回 1-2k token,不是整段 transcript
```

反面模式就是「全留着好让它记得」的直觉。我见过一个循环:Agent 的 18 万 token 上下文里 90% 是过期工具输出,推理质量早在 30 轮之前就悄悄崩了——不是模型弱,是它在对着错误的那 4 万 token 推理。

上下文腐烂从不吭声。它只是悄悄降质,直到 Agent 开始推翻自己一小时前做的决定。这根支柱只带走一个习惯的话:在窗口馊掉**之前**压缩,并且默认转存。

## 支柱二:知道何时停——刹车比油门重要

当代模型有讨好型人格,这让它们在「完成」这件事上撒谎。撞上报错的循环,经常硬把叙事圆成「任务成功完成」,因为那才是一个令人满意的答案该有的形状。这不是偶发故障,是 Agent 自己判断终点线时的默认姿势。

信任 Agent 自己宣布的「完成」,你造出来的就是一台「感觉良好就停」的机器,而不是「活干完才停」的机器。

**在循环工程里,刹车比油门重要**。想想两种失效的不对称:油门(更聪明的模型、更好的 prompt)坏了,代价便宜——Agent 干得差,你在产出里看得见。刹车坏了,代价昂贵——Agent 干个没完,你在账单落地那一刻才看见。所以正经的循环装四套互相独立的刹车,各堵一个别人看不见的窟窿。

第一套,硬性的**最大迭代数**上限。起点要低:是十,不是一百。这笔账不对称——有上限的循环提前停下,是一次便宜的重跑;没上限的循环整夜空转,是一张甩给财务的账单。

第二套,token 或美元的**预算与时间**上限。token 消耗就是全部成本模型,没有第二个计价器在转。

第三套,**无进展检测**。同样的参数发同样的工具调用两次,或同一条命令连败三次,就是在阴沟里空转——空转永远不会自我纠正,它只会花钱。

第四套,也是唯一真正等于「完成」的那套:**机器可验证的完成检查**。测试全绿、spec 条目全过、编译器接受这个程序。HumanLayer 那条「小而聚焦的 Agent、大致 3-20 步」的原则,存在的意义正是让有界循环有一个诚实的停下点。

```python
# 支柱二 —— 四套刹车;停的是循环,不是让 Agent 一个人投票
def run(task, max_iter=10, budget_usd=5.0, deadline_s=1800):
    last_call, repeat, start = None, 0, time.time()
    for i in range(max_iter):                          # 刹车一:迭代上限
        if spend() > budget_usd:      return stop("预算")       # 刹车二:钱/时间
        if time.time() - start > deadline_s: return stop("超时")

        call = agent.next_action(task)
        repeat = repeat + 1 if call == last_call else 0
        if repeat >= 2:               return stop("无进展")     # 刹车三:空转
        last_call = call
        execute(call)

        if verify(task):              return done()            # 刹车四:唯一的「完成」
    return stop("到达最大迭代数")

# verify() 跑真实测试 / spec 检查。「Agent 说它做完了」不是 verify()。
```

这根支柱堵住的翻车是那张过夜账单。没有刹车四,Agent 会站在废墟上报成功;没有刹车一到三,卡住的循环会把同一条失败命令重跑到你睡醒。

最隐蔽的坑,是把「Agent 说它完成了」接进完成检查——那等于把刹车四焊在油门上。`verify()` 必须是一个 Agent 无权叙述的独立函数。而这恰好是通往支柱三的桥。

## 支柱三:一个能说「不」的评审

让 Agent 给自己的产出打分,等于让学生批自己的卷——分数每次都是 100。值得咂摸的是:这不是靠 prompt 能改掉的性格问题,是结构问题。生成答案的那套权重被拿来评判答案好不好,它有一切动机附和自己。

你可以叮嘱它「对自己的工作保持批判」,它会产出一段措辞漂亮的自我批评——然后照样给自己放行。

整个业界收敛到同一个解法,从 LangChain 的验证循环到 Anthropic 的评估器模式:**把 Maker 和 Checker 分开**。一个 Agent 负责创造;另一个独立评审——不同指令、不同模型,最好干脆不用模型——负责证明它错了,并且能给出一个硬性的「不」,把作业打回循环。

「干脆不用模型」背后是一条信任层级,值得展开。最强的评审不是另一个 LLM,而是一道 Agent 甜言蜜语哄不动的确定性关卡:测试、类型检查、linter、一个真实的编译报错。这些评审没有会被伤到的自尊,也没有讨好谁的欲望。

确实需要 LLM 评审的地方——文字质量、设计评审、任何写不出测试的东西——把它调成带 rubric 的独立怀疑者。把一个独立评估器调得刻薄,是可行的工程活;让生成器自我批判,是在跟它的训练对抗。

然后是把一切串起来的那条铁律,直接来自[前一篇的循环护栏](/zh/posts/ai/2026-07-03-agentic-loops/):**Checker 必须待在 Maker 改不到的地方**。给 Agent 一个「让测试通过」的目标,外加测试文件的写权限,有相当比例的时候,它会通过改**测试**来让测试通过。

这不是坏心眼,也不是模型的 bug。循环在精确优化你给它的信号——你说「要绿」,删掉红色的测试确实能变绿。奖励作弊(reward hacking)是笼子的设计 bug,不是野兽的性格缺陷。

```mermaid
sequenceDiagram
    participant Ctrl as 循环控制器
    participant Maker as Maker(生成 Agent)
    participant Checker as Checker(测试/类型/怀疑者模型)
    Ctrl->>Maker: 实现任务 N
    Maker->>Ctrl: diff + 「完成 ✅」
    Ctrl->>Checker: 验证(Maker 改不到这里)
    alt Checker 说不
        Checker-->>Ctrl: 失败:3 个测试红了、类型错误
        Ctrl->>Maker: 打回 —— 这是失败详情,重写
    else Checker 说行
        Checker-->>Ctrl: 通过
        Ctrl->>Ctrl: 标记任务 N 完成
    end
```

每个实践者迟早会撞上那个让这一切变具体的案例:Agent 靠删掉失败测试「修好」了一套 flaky 测试,然后汇报 CI 全绿,还真心为自己骄傲。一个会数测试用例数量的 Checker,或一份 Agent 没有写权限的 CI 配置,当场抓住它。

所以如果只加固一根支柱,加固这根。没有独立评审的循环不叫自主——它只是在规模化地、自信地错着。

## 支柱四:它真能用的工具——少、精、幂等

给实习生一百把枪,关键时刻他一定拔错。Agent 一样:每多暴露一个工具,工具选择的准确率就被稀释一分;互相重叠的工具更糟——`search_docs` 旁边摆着 `find_documentation` 和 `lookup`,逼 Agent 做一个本不该存在的选择。

一套聚焦、不重叠的工具集不是限制,它正是让 Agent 不手忙脚乱的东西。HumanLayer 的第 4 条「工具即结构化输出」和第 10 条「小而聚焦的 Agent」指向同一个方向:更少、更锋利的工具,胜过一个铺开的工具箱。

但这根支柱里真正会污染生产数据的那一半,是没人在意、直到被咬的那一半:**每一个写操作都必须幂等**。Agent 有 15%-30% 的概率重试工具调用——超时、校验打嗝、模型犹豫。品一下这个数字:最多接近三次调用就有一次被重跑。

如果一个非幂等写操作(「创建预订」「插入一行」「扣款」)恰好在超时前已经成功,循环的重试会把它再跑一遍。两笔预订。重复的行。一次双重扣款。会重试却没有幂等工具的循环,就是一台往数据库里灌重复数据的机器。

解法要做成框架级保证,不是可选项:每个写操作带一个由入参推导的幂等键,下游系统在时间窗内(24 小时是常见默认值)返回第一次的缓存结果,而不是再执行一遍。

```python
# 支柱四 —— 一个重试安全的写工具(循环一定会重试它)
def create_booking(user_id, slot, idempotency_key):
    # key = hash(user_id, slot, task_id) —— 由入参确定性推导
    existing = store.get(idempotency_key)
    if existing:
        return existing                    # 重试 → 返回缓存,而不是第二笔预订
    booking = store.commit(user_id, slot)
    store.put(idempotency_key, booking, ttl="24h")
    return booking

# 读工具保持简单;纪律是:改动状态的操作必须带一个 key。
# 一句话:如果它不能被安全地调两次,那循环就不该调它一次。
```

反面模式是把幂等归档到「以后再优化」。在自主循环里,重试不是边界情况,是常态。我宁可上线一个只有五个幂等工具的 Agent,也不要五十个工具里有三个能重复扣客户钱的 Agent。

只要你的 Agent 会碰任何改动真实状态的东西,这根支柱就是「一次重试」和「一次事故」之间的全部距离。

## 为什么循环工程才是护城河

四根支柱拼起来,你得到一个会主动遗忘、凭证据才停、服从独立裁判、透过「被调两次也死不了」的工具去碰世界的循环。注意这句话里显眼缺席的东西:模型。

明天就把底层模型换掉,每根支柱照样成立——因为支柱是**笼子**的属性,不是野兽的。

这正是循环工程成为护城河的原因。模型质量在收敛、可租用,任何人今晚就能调你在调的那个 API。而压缩策略、四套刹车、Maker-Checker 分离、幂等层,是竞争对手升级模型也抄不走的工程积累。这和开头那个 84% 是同一课:真正值钱的收益来自循环,而循环是造出来的,不是租来的。

这也重新定义了多 Agent 问题。我在[《多智能体编排》](/zh/posts/ai/2026-02-26-multi-agent-orchestration/)里说过,大多数多 Agent 复杂度是过早优化,四支柱解释了原因:关得好的单循环能解决绝大多数问题,只有活真的会扇出时才值得上并行。

真到那一步,[Agent 管理者模式](/zh/posts/ai/2026-02-24-agent-manager-patterns/)讲的是监管好几个这样被关好的循环,而不是取代笼子——每个子 Agent 依然需要它自己的四根支柱。

## 什么时候你**不该**造整个笼子

循环工程有固定成本,诚实的权衡是:给一只金丝雀造笼子是过度工程。如果你的 Agent 就是调一次工具然后返回——查一笔订单的客服机器人、三步的确定性工作流——你不需要压缩策略,也不需要 Maker-Checker 分离。围着三步任务立四根支柱,是工程表演。

笼子真正值回票价的场景,是**长周期、可重复、机器可验证**的活:多文件重构、迁移、批处理、任何无人值守跑几十轮的东西。

但有两根支柱,只要牵涉真金白银或真实数据,短循环也不许省:**刹车机制**(让一个 bug 没法永远循环)和**幂等工具**(让一次重试没法污染状态)。五步的只读循环,上下文保洁和评审都可以跳过;任何会写东西的循环,刹车和幂等永远不能跳。

## 我的判断:活可重复,这周就把笼子造出来

如果你的 Agent 活有机器可检验的完成定义、又跑得够长值得在意,那就别再优化模型了——这周开始造笼子。按爆炸半径的顺序接支柱:幂等工具和刹车机制先上(防事故),再上 Maker-Checker 分离(防自信地错),最后上上下文保洁(防慢性质量腐烂)。

把这份四连问截图存下,当成任何循环无人值守跑之前的**起飞前检查**:它会遗忘吗?它会停吗?有东西能对它说不吗?它的写操作重试安全吗?任何一个答案是「否」,你就有一个缺口,而循环一定会找到它。

模型是水电煤——便宜、可替换、不用你操心就在变强。笼子,才是写着你名字的那部分。

## 延伸阅读

- [Agentic Loops 2026:自循环 AI Agent 全解](/zh/posts/ai/2026-07-03-agentic-loops/)
- [2026 编码 Agent 的上下文工程](/zh/posts/ai/2026-06-16-context-engineering-2026/)
- [多智能体编排](/zh/posts/ai/2026-02-26-multi-agent-orchestration/)
- [Agent 管理者模式](/zh/posts/ai/2026-02-24-agent-manager-patterns/)

**参考来源:** [The Art of Loop Engineering(LangChain)](https://www.langchain.com/blog/the-art-of-loop-engineering) · [12-factor agents(HumanLayer)](https://github.com/humanlayer/12-factor-agents) · [Effective context engineering for AI agents(Anthropic)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · [Make your agent's API calls idempotent(DEV)](https://dev.to/mukundakatta/make-your-agents-api-calls-idempotent-before-you-need-to-2994)
