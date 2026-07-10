+++
date = '2026-07-09T18:00:00+08:00'
aliases = ['/posts/ai/2026-07-10-seedream-5-pro/']
draft = false
title = 'Seedream 5.0 Pro 上线：字节生图杀入 Gemini 腹地？API 实操与选型'
description = 'Seedream 5.0 Pro 于 2026 年 7 月 8 日上线火山方舟：1K 单张 0.3 元、2K 0.6 元，按张计费。本文核检"超过 Gemini"的真实出处，给出开通、调用、计费全流程实操，以及和即梦、Seedance 的联动关系与选型结论。'
toc = true
tags = ['Seedream', 'ByteDance', 'AI Image Generation', 'Gemini']
keywords = ['seedream 5.0 教程', '即梦 api', '豆包生图', 'seedream 5.0 pro 价格', '火山方舟 生图 api', 'seedream 对比 gemini', '字节 生图模型']

[[params.faqItems]]
question = "Seedream 5.0 Pro 是什么？怎么开通？"
answer = "Seedream 5.0 Pro 是字节 Seed 团队 2026 年 7 月 8 日发布的生图模型，主打交互式精准编辑和 14 国语言文字渲染。在火山方舟控制台开通模型服务、创建 API Key 即可调用，Model ID 为 doubao-seedream-5-0-pro-260628，也可在方舟体验中心免代码试用。"

[[params.faqItems]]
question = "Seedream 5.0 Pro 生图多少钱一张？"
answer = "按张计费：1K 档 0.3 元/张，2K 档 0.6 元/张，以 236 万像素（约 1536×1536）为分界；输入参考图 0.02 元/张，首张免费。响应里的 output_tokens 只是信息字段，不按 token 收费。"

[[params.faqItems]]
question = "Seedream 5.0 Pro 真的超过 Gemini 了吗？"
answer = "没有第三方数据支撑。截至 2026 年 7 月 10 日，它未上榜 LMArena 和 Artificial Analysis（榜首是 GPT Image 2，Elo 1338）；Atlas Cloud 独立测试其英文文字准确率 89.5%，低于 GPT-Image 2 的 98.5%。它的真实优势是价格和交互编辑，不是画质登顶。"

[[params.faqItems]]
question = "Seedream 5.0 Pro 和即梦是什么关系？"
answer = "同源不同壳：Seedream 5.0 Pro 是模型本体，通过火山方舟 API 提供；即梦（海外版 Dreamina）和豆包是搭载它的 C 端产品，发布后陆续接入。开发者走 API 按张付费，普通用户在即梦里用会员额度。"

[[params.faqItems]]
question = "Seedream 5.0 Pro 和 5.0 Lite 怎么选？"
answer = "Pro 是精度特化版：独占坐标/涂鸦交互编辑，但只能单图输出、上限 2K；Lite 支持组图（一次最多 15 张）、流式输出、联网搜索、上限 4K，价格更低。要精准改图选 Pro，要批量产图或 4K 选 Lite。"
+++

![Seedream 5.0 Pro API 实操教程与 Gemini 对比核检](cover.webp)

「字节生图超过 Gemini」这个刷屏说法里，最反直觉的一点是：字节自己从来没这么说过。Seedream 5.0 Pro 的官方一页纸原话是「全球第一梯队通用场景生图大模型」——是"第一梯队"，不是"第一"。而且截至 7 月 10 日，这个"超过 Gemini"的模型在 LMArena 和 Artificial Analysis 上一个榜都没上。

宣传和证据之间的这道裂缝，值得掰开看——因为裂缝底下藏的真实故事，比编出来的那个更值钱。我花了两天把火山方舟的 API 文档、官方教程和对客一页纸完整读了一遍，又去查了目前仅有的第三方数据。

先交代清楚：我还没实际充值跑图，本文所有内容基于官方文档、官方样张和第三方基准测试，不是我自己的出图。文档读得够深，核检宣传、算清账目、标出坑位，这些足够了。

我的判断一句话：**Seedream 5.0 Pro 不是更好的 Gemini，是另一个物种——它把生图 API 从"抽卡机"改造成了"编辑器"，价格只有 GPT-Image 2 的四分之一左右。** 拿它跟 Gemini 比单图颜值，你会失望；拿它当生产管线里的精准改图工具，你会发现对手货架上根本没有对位产品。

## 「超过 Gemini」三层核检：出处到底是什么

我沿用[写 GPT-5.6 发布时的厂商跑分打折框架](/zh/posts/ai/2026-07-10-gpt-5-6-general-availability/)：谁测的、测的什么、第三方能不能复现。三层剥下来，标题党的成色一目了然。

**第一层，字节官方怎么说。** 官方口径就是「第一梯队」，从头到尾没提超过 Gemini 或 GPT-Image 2。这比多数大厂发布会克制——"超过 Gemini"是社交媒体传播中加的戏，也就是说这个说法最响亮的版本，找不到一个愿意署名负责的作者。

**第二层，第三方榜单。** 截至 2026 年 7 月 10 日：[LMArena 的更新日志](https://arena.ai/blog/leaderboard-changelog/)显示只有 Seedream 5.0 **Lite** 在 2 月 25 日进过榜，5.0 Pro 未收录；[Artificial Analysis 文生图榜](https://artificialanalysis.ai/image/leaderboard/text-to-image)榜首是 GPT Image 2 (high)，Elo 1338，Gemini 的 Nano Banana 系列稳居前五，Seedream 5.0 Pro 同样查无此人。

发布才两天没上榜很正常，但结论很硬：**目前任何方向的"第三方实锤"都不存在**——说它赢没依据，说它输也没依据。

**第三层，唯一的独立实测。** [Atlas Cloud 七月的基准测试](https://www.atlascloud.ai/blog/guides/2026-ai-image-api-benchmark-gpt-image-2-vs-nano-banana-2-pro-vs-seedream-5-0)：Seedream 5.0 英文文字渲染准确率 **89.5%**，落后 GPT-Image 2 的 **98.5%** 和 Nano Banana Pro 的 **94.8%**。单一实验室的数据要打折，但方向和字节自己在文档里承认的「小字结构仍存在不稳定问题」一致。

也就是说，恰恰在传播最热的"文字渲染"维度上，现有证据说明它的英文场景是落后的。它强的是覆盖广——中文加 14 国小语种，不是单字准确率登顶。

> 截至 2026 年 7 月 10 日，Seedream 5.0 Pro 未上榜 LMArena 和 Artificial Analysis。火山方舟定价 1K 图 0.3 元/张、BytePlus 定价 $0.045/张——约为 Gemini 生图的一半、GPT Image 2 (high) 的四分之一，且是目前唯一提供坐标级交互编辑的主流生图 API。

老实记分：画质榜未上榜、英文文字准确率落后、价格约为对手的四分之一到一半、坐标级交互编辑全场独一份。字节不是造了台更大的攻城锤去砸 Gemini 的城墙，而是从定价地板下面挖了条隧道，顺手卖一把对手没有的工具。

## Seedream 5.0 Pro 到底发布了什么

把事实钉死，因为首发当天大量转发把"已上线"和"即将上线"混在一起了。

Seedream 5.0 Pro 于 7 月 8 日在火山方舟上线，Model ID `doubao-seedream-5-0-pro-260628`；海外走 [BytePlus ModelArk](https://docs.byteplus.com/en/docs/ModelArk/1541523)，Model ID `dola-seedream-5-0-pro-260628`。C 端陆续接入豆包、即梦和海外版 Dreamina——和 [Seedance 视频模型](/zh/posts/ai/2026-03-29-seedance-2-bytedance-ai-video/)一模一样的"API + 自家 App"双通道打法。第三方跟进极快，fal.ai 次日就挂上了模型页。

官方四大亮点，三个已上线：① 交互式编辑——在参考图上画框、点坐标、涂鸦、标色块，模型按标记位置做局部生成和替换，Pro 独占，全场最有含金量；② 信息可视化——数据报告、菜单注解这类高密度排版，官方自己标注了小字不稳定，这个诚实值得表扬；③ 原生 14 国小语种文字渲染，含从右往左书写的文字。

一个未上线：图层分离（把生成图拆成可独立编辑的图层）在官方材料里明确写着「即将上线」，7 月 8 日的 API 里没有。看到"Seedream 5.0 Pro 支持图层编辑"的文章，可以直接判定作者没读文档。

## "Pro"是精度特化，不是 Lite 的高配

这是我读 API 文档时最意外的发现，英文圈还没人写：Pro 不是"Lite 加强版"。[官方文档](https://www.volcengine.com/docs/82379/1541523)写得很清楚，给 Pro 传 Lite 的专属参数会**直接报错**，不是静默忽略——这是两个分工不同的工具：

| 能力 | Seedream 5.0 Pro | Seedream 5.0 Lite |
|---|---|---|
| 分辨率上限 | **2K**（1K/2K 档） | **4K**（2K/3K/4K 档） |
| 组图生成 | ❌ 仅单图 | ✅ 一次最多 15 张 |
| 流式输出 | ❌ | ✅ |
| 联网搜索 | ❌ | ✅ |
| 参考图上限 | 10 张 | 14 张 |
| 坐标/涂鸦交互编辑 | ✅ 独占 | ❌ |
| 输出格式 | png / jpeg | png / jpeg |
| 限流 | 500 张/分钟 | 500 张/分钟 |

第一行请再看一遍：**叫"Pro"的模型，分辨率上限反而比"Lite"低。** 字节这里的 Pro 指"精度"，不是"功能全"。Pro 留给"这一张图的文字、位置、人物特征必须分毫不差"的场景；分镜、品牌套图、连环画这种一次出一组的活，或者 4K 交付，正确答案是 Lite。

这个坑会咬到评估团队。别家产品线里贵的模型规格全面碾压便宜的，所以大家的本能是拿 Pro 跑批量任务——然后看它报错，得出"又贵又残废"的结论，把整个系列拉黑。评估姿势错了，结论必然错。

## 火山方舟实操：调用 Seedream 5.0 Pro 的完整链路

以下内容提炼自火山方舟的 [API 文档](https://www.volcengine.com/docs/82379/1541523)和[官方教程](https://www.volcengine.com/docs/82379/1824121)，海外账号看 BytePlus 的镜像文档即可。

国内开发者开通四步：① 注册火山引擎账号并实名认证；② 在方舟控制台「开通管理」里开通 Doubao-Seedream-5.0-Pro 模型服务；③ 「API Key 管理」页创建长效 API Key；④ curl 或 SDK 直接调。不想写代码，先去方舟体验中心把参数玩明白再接 API。

接口是同步的——不像视频生成要建任务再轮询，一次 POST 直接返回图片链接：

```bash
curl https://ark.cn-beijing.volces.com/api/v3/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ARK_API_KEY" \
  -d '{
    "model": "doubao-seedream-5-0-pro-260628",
    "prompt": "充满活力的特写编辑肖像，模特眼神犀利，头戴雕塑感帽子，色彩拼接丰富，景深较浅，Vogue 杂志封面美学，中画幅，强烈工作室灯光。",
    "size": "2K",
    "output_format": "png",
    "watermark": false
  }'
```

接口兼容 OpenAI SDK（`client.images.generate(...)` 直接可用），从 gpt-image 迁移基本是改 base_url 和模型名的工作量。完整调用链路和生产环境最容易踩的坑：

```mermaid
sequenceDiagram
    participant App as 你的应用
    participant Ark as 方舟 API
    participant TOS as 火山对象存储

    App->>Ark: POST /images/generations（提示词 + 参考图）
    Note over Ark: 同步生成，单图返回
    Ark->>TOS: 写入生成结果
    Ark-->>App: 返回 data[0].url 和 usage
    Note over TOS: 图片链接 24 小时后失效
    App->>TOS: 立即下载图片
    App->>App: 转存到自己的存储
```

Pro 版参数速查表（对照 7 月 10 日版文档核对过，建议截图保存）：

| 参数 | 取值/范围 | 备注 |
|---|---|---|
| `prompt` | 建议 ≤300 汉字 / 600 英文词 | 超长后模型会**丢元素**，不是缓慢降质 |
| `image` | URL 或 base64，1-10 张 | 单张 ≤30MB、≤3600 万像素、宽高比 [1/16, 16] |
| `size`（像素模式） | 总像素 921600 - 4624220 | `2048x1024` 合法；`512x512` 低于下限直接报错 |
| `size`（档位模式） | `1K` / `2K` | 宽高比写进 prompt，由模型定尺寸 |
| `output_format` | `png` / `jpeg` | 5.0 新增，4.x 只有 jpeg |
| `response_format` | `url` / `b64_json` | **url 24 小时失效**，务必转存 |
| `watermark` | 默认 `true` | 生产素材显式传 `false`，否则右下角带"AI生成"角标 |
| `sequential_image_generation` / `stream` / `tools` | ❌ | Lite 专属，Pro 传参报错 |

三个从文档里挖出来的要点，英文圈还没人提：

**其一，512×512 的下限墙。** 最小总像素 921600（1280×720），做小图标、缩略图必须生成后自己缩，API 不给小图，低于下限直接拒绝而不是放大。

**其二，prompt 长度是个陷阱。** 文档明确警告超过约 600 英文词/300 汉字后，模型会开始**丢元素**而不是平滑降质。从 gpt-image 迁移长提示词的，先做压缩。

**其三，交互编辑没有专门的 API 字段。** 框、箭头、坐标号、涂鸦都是你自己画在参考图上传的，再用 prompt 描述："在右侧标记区域添加带杯碟的陶瓷咖啡杯，移除所有草图线条"。这意味着标记可以用 Pillow 程序化生成——Seedream 5.0 Pro 因此变成一个**可脚本化的区域编辑器**，整个发布里我认为最值得基于它做产品的就是这一点。

## 计费怎么算：按张，不按 token

先破一个误会：响应里有 `output_tokens` 字段（算法是宽×高÷256），很容易让人以为按 token 计费——**实际是按张**。截至 2026 年 7 月 10 日的价格：

| 渠道 | 1K 输出 | 2K 输出 | 输入参考图 |
|---|---|---|---|
| 火山方舟（国内） | **0.3 元/张** | **0.6 元/张** | 0.02 元/张，首张免费 |
| BytePlus（海外官方） | $0.045 | $0.09 | $0.003/张，首张免费 |
| fal.ai（第三方） | $0.0675 | $0.135 | 额外参考图 $0.0045 |
| GPT Image 2 (high) 参考 | 约 $0.17-0.25 | — | 按 token |

1K/2K 的分界线是 236 万总像素（约 1536×1536），也就是说 1424×800 的 16:9 横图按 1K 档 0.3 元计。粗算一笔账：**月产 1 万张的电商图管线，方舟约 3000-6000 元人民币，GPT Image 2 (high) 约合 1.2 万-1.8 万元**——这是"随手试试"和"走预算审批"的区别。fal 比官方贵 50%，免注册免实名适合快速原型，跑量不划算。

还有一个价格表上不写的合规细节：Seedance 2.0/2.0 mini/2.5 对 Seedream 5.0 Pro **文生图**产出的图片免人脸审核，但**图生图**产出要联系商务做 KYC 认证。"改真人照片再生成视频"的管线中间卡着一道审核门，做数字人业务的先把这条确认清楚再排期。

## 和即梦、豆包是什么关系

一句话：Seedream 5.0 Pro 是发动机，即梦和豆包是装了这台发动机的两辆车。模型本体只通过火山方舟/BytePlus API 提供，按张付费、可进生产系统；即梦（海外版 Dreamina）是面向创作者的 C 端产品，发布后陆续切到 5.0 Pro，用的是会员积分额度。

对开发者的实际意义：**想先免费感受模型上限，去即梦或方舟体验中心玩；要接业务，直接走 API**——官方价三毛钱一张，逆向即梦网页接口那套方案的维护成本已经毫无意义。

## 三类人三个结论：谁该换，谁别动

热闹看完，落到"我该干什么"。我的选型逻辑：

```mermaid
flowchart TD
    A["生图需求"] --> B{"要在已有图上做局部精准修改？"}
    B -- "是" --> C["Seedream 5.0 Pro：坐标/涂鸦编辑，API 独一份"]
    B -- "否" --> D{"英文文字密集的信息图？"}
    D -- "是" --> E["GPT Image 2：英文文字准确率 98.5% 仍领先"]
    D -- "否" --> F{"要组图或 4K 输出？"}
    F -- "是" --> G["Seedream 5.0 Lite：一次 15 张、上限 4K、更便宜"]
    F -- "否" --> H{"数据不能出本机？"}
    H -- "是" --> I["本地方案：Mac + Draw Things 跑 Flux"]
    H -- "否" --> J{"跑量、对成本敏感？"}
    J -- "是" --> C
    J -- "否" --> K["Gemini 系：多模态对话式创作生态"]
```

**做"改图多于生图"的生产管线的，这次发布就是给你的。** 电商、广告、营销物料、中文和小语种海报本地化，都在射程内；OpenAI 兼容接口让试错成本只有半天。月产几千张以上、价差已经是预算量级的团队，同理。

**主产英文信息图的，这次发布跟你没关系。** 89.5% 对 98.5% 的文字准确率差距就是返工率差距，GPT Image 2 该用还得用。要 4K 交付的（讽刺的是该用 Lite 或 4.5）、深度绑定 Gemini 对话式改图流程的，也别动。素材不能出内网的走本地路线——我写过 [Draw Things 完全指南](/zh/posts/ai/2026-02-15-draw-things-ultimate-guide/)和 [Mac mini 本地生图方案](/zh/posts/ai/2026-02-15-mac-mini-local-image-generation/)，零边际成本，隐私可控。

**正在给 Gemini 或 GPT-Image 付费的，你的议价地板刚刚被砸穿。** 字节在生图上复刻了 Seedance 在视频上的打法：接近第一梯队的质量、四分之一的价格、外加对手没有的生产流程特性。"超过 Gemini"今天不成立，但"让 Gemini 的报价单变得难看"已经成立了。接下来两三周盯 LMArena：如果 5.0 Pro 在 Image Edit 榜（它的主场）进前三而价格不动，很多团队的问题就会从"为什么要换"变成"为什么还没换"。

## Related Reading

- [Seedance 2.0 深度解读：字节 AI 视频的集群打法](/zh/posts/ai/2026-03-29-seedance-2-bytedance-ai-video/)——同一战略在视频赛道的先行版
- [GPT-5.6 正式发布全解读](/zh/posts/ai/2026-07-10-gpt-5-6-general-availability/)——本文使用的厂商跑分打折框架出处
- [Draw Things 完全指南](/zh/posts/ai/2026-02-15-draw-things-ultimate-guide/)——API 之外的本地生图路线
- [Mac mini 本地生图方案](/zh/posts/ai/2026-02-15-mac-mini-local-image-generation/)——零边际成本的对照组
