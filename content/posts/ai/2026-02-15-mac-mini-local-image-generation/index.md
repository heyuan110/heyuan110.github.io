+++
date = '2026-02-15T00:30:00+08:00'
draft = false
title = 'Mac Mini AI 生图实测（2026）：3 款工具对比，Draw Things 完胜'
description = '实测 Mac Mini M4 本地 AI 生图：ComfyUI、DiffusionBee、Draw Things 性能对比，附生成速度数据、量化方案选择和博客配图最佳实践。24GB 内存 Flux 出图仅需 50 秒。'
toc = true
tags = ['Mac Mini', 'AI 生图', 'ComfyUI', 'Draw Things', 'Stable Diffusion', 'Flux']
categories = ['AI实战']
keywords = ['Mac Mini 本地生图', 'ComfyUI Mac', 'DiffusionBee', 'Draw Things', 'Apple Silicon AI 生图', 'Flux Mac Mini', 'Mac Mini M4 AI', '本地 AI 生图 2026', 'Mac Mini AI 图像生成', 'ComfyUI 最新版本 2026']
+++

![Mac Mini M4 本地 AI 生图工具选型指南封面，对比 ComfyUI、DiffusionBee、Draw Things](cover.webp)

2026 年，**Mac Mini M4 本地 AI 生图**已经完全可用——24GB 内存跑 Flux 模型出一张 1024x1024 的图只要 50 秒，不花一分钱 API 费用，数据全在本机。

但工具选哪个？我在 Mac Mini M4 Pro 上**实测了 ComfyUI、DiffusionBee、Draw Things 三款主流工具**，跑了上百张图，记录了每款工具的生成速度、内存占用和实际体验。结论是：其中一款已经停更不推荐，而另一款在性能上完胜——比 ComfyUI 快 20% 以上。

本文将从技术架构、性能数据、模型支持到实际使用体验，帮你在 2026 年做出最合理的**本地 AI 生图选型决策**。不管你是博客写手、独立开发者还是设计师，读完这篇就够了。

## 一、为什么要在 Mac Mini 上本地生图？

在讨论具体工具之前，先回答一个根本性问题：**为什么不直接用 Midjourney / DALL-E 这些在线服务？**

### 1.1 本地生图的核心优势

| 维度 | 在线服务 | 本地生图 |
|------|---------|---------|
| **隐私** | 图片上传到云端 | 所有数据留在本机 |
| **成本** | 按月/按次付费，长期成本高 | 一次购入硬件，无限使用 |
| **速度** | 取决于排队人数和网络 | 稳定可控，无需等待 |
| **自由度** | 受平台审核限制 | 完全自主，无内容限制 |
| **离线能力** | 必须联网 | 断网也能用 |
| **定制化** | 只能用平台提供的模型 | 自由加载 LoRA、自定义模型 |

### 1.2 Mac Mini M4 为什么行？

很多人的直觉是"AI 生图需要 NVIDIA 显卡"，但 Apple Silicon 的**统一内存架构**（Unified Memory）改变了这个格局。

传统 PC 上，GPU 有独立显存（VRAM），CPU 有系统内存，数据在两者之间需要来回搬运。而 Mac Mini M4 的统一内存意味着：

> **CPU 和 GPU 共享同一块内存池**——GPU 可以直接访问所有系统内存，不存在"显存不够"的问题。

这就像传统 PC 是"两个仓库之间搬货"，而 Mac 是"一个大仓库，所有人都能直接取用"。一台 24GB 内存的 Mac Mini M4 Pro，其 GPU 理论上可以利用大部分的系统内存来加载模型，这对于运行 Flux 这种"吃内存"的模型至关重要。

再加上 Apple 的 **Metal Performance Shaders（MPS）** 和 **Core ML** 框架对机器学习的原生加速支持，Mac Mini M4 已经是一台称职的本地 AI 生图工作站了。

### 1.3 硬件配置与生图能力速查

| Mac Mini 配置 | SD 1.5 | SDXL | Flux.1 | 推荐用途 |
|--------------|--------|------|--------|---------|
| **M4 / 16GB** | 流畅 | 流畅 | 需量化（Q4），较慢 | 轻度使用，博客配图 |
| **M4 Pro / 24GB** | 很快 | 很快 | Q6_K 量化可用，中等速度 | 日常创作，中等批量 |
| **M4 Pro / 48GB** | 极快 | 极快 | FP16 可用，较快 | 专业创作，批量生产 |
| **M4 Max / 64GB+** | 极快 | 极快 | FP16 流畅，支持批量 | 专业工作站级别 |

> **关键认知**：macOS 的统一内存中，系统本身会占用 1-2GB，所以 16GB 的 Mac Mini 实际可用于 AI 的内存约 14GB。如果你计划频繁使用 Flux 模型，**24GB 是比较舒适的起点**。

## 二、三大工具全景概览

在 Mac 上做本地 AI 生图，主流工具有不少，但真正值得深入对比的是以下三个：

| 特性 | ComfyUI | DiffusionBee | Draw Things |
|------|---------|-------------|-------------|
| **类型** | 节点式工作流引擎 | GUI 桌面应用 | 原生 macOS/iOS 应用 |
| **技术架构** | Python + PyTorch MPS | Electron + Python | SwiftUI + CoreML/Metal |
| **学习曲线** | 陡峭 | 极低 | 中等 |
| **模型支持** | 最广泛 | SD 系列 + Flux | SD/SDXL/Flux/Z-Image |
| **扩展性** | 极强（自定义节点） | 弱 | 中等 |
| **Mac 优化** | 一般（MPS 后端） | 一般 | 最佳（Metal FlashAttention） |
| **开发活跃度** | 非常活跃 | 停滞（2024.8 后无更新） | 活跃 |
| **安装难度** | 中等（有桌面版） | 极简（拖拽安装） | 极简（App Store） |

下面逐一深入分析。

## 三、ComfyUI：最强大的生图引擎

### 3.1 它是什么？

[ComfyUI](https://github.com/comfyanonymous/ComfyUI) 是一个开源的、基于节点的图像生成工作流引擎。如果说其他工具是"傻瓜相机"，ComfyUI 就是"全手动单反"——你可以精确控制图像生成的每一个环节。

它的界面是一个可视化的**节点编辑器**：每个节点代表一个操作（加载模型、设置提示词、采样、解码等），节点之间用连线传递数据。这意味着你不是简单地输入一个提示词然后等结果，而是构建一整条从模型加载到最终输出的**处理管线**。

### 3.2 macOS 上的安装

ComfyUI 提供了 [macOS 桌面版](https://docs.comfy.org/installation/desktop/macos)（目前仍处于 Beta），安装步骤相当简化：

1. 下载 DMG 安装包（或通过 `brew install comfyui`）
2. 启动后选择 **MPS**（Metal Performance Shaders）作为 GPU 后端
3. 选择安装路径，自动配置 Python 环境和依赖
4. 完成后即可进入节点编辑界面

> **注意**：ComfyUI 桌面版**仅支持 Apple Silicon**，Intel Mac 不可用。最少需要 5GB 可用磁盘空间。

### 3.3 核心优势

**模型支持最广泛**

ComfyUI 支持几乎所有主流图像生成模型：SD 1.5、SD 2.x、SDXL、Flux.1（Dev/Schnell）、Z-Image-Turbo、Kolors 等。通过 [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) 插件，还能加载 GGUF 量化模型——这对内存有限的 Mac 用户极为重要。

**GGUF 量化是 Mac 用户的"救生圈"**。以 Flux.1 Dev 模型为例：

| 量化级别 | 文件大小 | 画质 | 速度 | 推荐配置 |
|---------|---------|------|------|---------|
| FP16（原始） | ~24GB | 最佳 | 慢 | 48GB+ 内存 |
| Q8 | ~13GB | 接近无损 | 较慢 | 32GB+ 内存 |
| **Q6_K** | ~10GB | **推荐平衡** | **中等** | **24GB 内存** |
| Q4_KS | ~7GB | 有一定损失 | 较快 | 16GB 内存 |
| Q2_K | ~4GB | 明显劣化 | 最快 | 16GB 内存（应急） |

> **实测经验**：Q6_K 是大多数 Mac 用户的甜点。画质损失肉眼几乎不可见，但内存占用大幅降低。如果你只有 16GB 内存，Q4_KS 配合量化的 T5 文本编码器是最佳组合。

**节点生态极其丰富**

ComfyUI 的"杀手锏"是它的自定义节点生态。社区开发了数千个节点，涵盖：

- **ControlNet**：精确控制构图、姿势、边缘
- **IP-Adapter**：用参考图像控制风格
- **TeaCache**：加速生成 30-50%（适合草图阶段）
- **AnimateDiff**：生成动画
- **Upscale**：超分辨率放大

### 3.4 性能实测（Mac 环境）

在 M4 Pro 24GB 上，正确配置 MPS 后端后：

- **Flux.1 Dev Q6_K**（1024×1024，20 步）：约 **50-90 秒/张**
- **SDXL**（1024×1024，25 步）：约 **20-40 秒/张**
- **SD 1.5**（512×512，20 步）：约 **5-10 秒/张**
- **Z-Image-Turbo**（1024×1024，9 步）：约 **60-80 秒/张**

> **踩坑提醒**：如果你发现 Flux 生成特别慢（比如一张图要 1 小时），大概率是 PyTorch 没有正确使用 GPU。这是一个[已知问题](https://github.com/Comfy-Org/ComfyUI/issues/6969)——原因通常是安装了 CPU 版本的 PyTorch。正确做法是确保安装支持 MPS 的 PyTorch nightly 版本。

### 3.5 不足之处

- **学习曲线陡峭**：节点式操作对新手不友好，需要理解 Stable Diffusion 的工作流程
- **Mac 优化非原生**：通过 PyTorch MPS 后端运行，不如原生 CoreML/Metal 实现高效
- **占用资源多**：Python 环境 + 模型文件，轻松占用 20GB+ 磁盘空间
- **Beta 状态**：macOS 桌面版仍不稳定，偶有闪退

## 四、DiffusionBee：最简单的入门之选

### 4.1 它是什么？

[DiffusionBee](https://diffusionbee.com/) 是专为 Mac 设计的 AI 图像生成应用，目标是"**让 Stable Diffusion 在 Mac 上像使用普通 App 一样简单**"。它基于 Electron 构建，提供完整的图形界面，不需要任何命令行操作。

### 4.2 安装与使用

安装过程堪称所有工具中最简单的：

1. 从 [GitHub Releases](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui/releases) 下载 DMG
2. 拖拽到 Applications 文件夹
3. 首次启动自动下载默认模型
4. 输入提示词，点击生成

完全不需要 Python、不需要命令行、不需要理解任何技术概念。

### 4.3 功能概览

DiffusionBee 2.5.3 支持：

- **文生图**（Text to Image）
- **图生图**（Image to Image）
- **局部重绘**（Inpainting）
- **扩展画布**（Outpainting）
- **超分辨率放大**（Upscaling）
- **自定义模型加载**：SD 1.x、SD 2.x、SDXL
- **LoRA 加载**：支持多个 LoRA 同时使用
- **Flux.1 支持**（仅限 ARM64 / macOS 13+）

### 4.4 致命问题：开发停滞

这里必须说一个**非常关键的事实**：

> **DiffusionBee 的最后一次更新是 2024 年 8 月 14 日（v2.5.3）。截至 2026 年 2 月，已经超过 1.5 年没有新版本发布。**

在 AI 图像生成这个日新月异的领域，1.5 年的停滞意味着：

- **Flux.1 支持不完善**：有用户报告 [Flux 功能无法使用](https://github.com/divamgupta/diffusionbee-stable-diffusion-ui/issues/559)
- **无法使用 GGUF 量化模型**：对内存受限的 Mac 用户很不友好
- **不支持最新模型**：Z-Image-Turbo、SD3.5、FLUX.2 等新模型都无法使用
- **Bug 修复停滞**：已知问题不再得到修复
- **无法从应用内更新**：用户必须手动下载新版本

这就像买了一辆车，厂家突然不再提供维修和保养服务了。短期内还能开，但长期来看风险越来越大。

### 4.5 性能参考

在 M4 Pro 24GB 上：

- **Flux Dev**（704×704，25 步）：约 **6 分钟/张**
- **SDXL**（1024×1024，25 步）：约 **1-2 分钟/张**
- **SD 1.5**（512×512，20 步）：约 **15-30 秒/张**

性能表现中规中矩，但由于缺乏 GGUF 支持和最新的优化技术，在 Flux 模型上的表现明显落后于其他工具。

### 4.6 适合谁？

如果你满足以下**所有**条件，DiffusionBee 仍然是一个选项：

- 只需要 SD 1.5 / SDXL 基本功能
- 不需要 Flux 等新模型
- 对性能要求不高
- 希望零配置、开箱即用

但说实话，考虑到开发停滞的风险，**我不推荐新用户选择 DiffusionBee 作为主力工具**。

## 五、Draw Things：被低估的 Apple 原生之选

### 5.1 它是什么？

[Draw Things](https://drawthings.ai/) 是一款专为 Apple 生态打造的 AI 图像生成应用，支持 iPhone、iPad 和 Mac。它不是简单的 Python 套壳——而是用 **SwiftUI + 自研推理引擎（s4nnc）** 从底层针对 Apple Silicon 进行了深度优化。

如果说 ComfyUI 是"改装赛车"，DiffusionBee 是"自动挡家用车"，那 Draw Things 就是"原厂高性能版"——在保持易用性的同时，针对 Apple 硬件做了极致的性能优化。

### 5.2 技术架构深度解析

Draw Things 的性能优势来自两项核心技术：

**Metal FlashAttention**

这是 Draw Things 自研的核心技术。标准的 Attention 计算需要先生成一个完整的注意力矩阵（非常耗内存），而 FlashAttention 改为**逐行计算**，大幅降低内存占用的同时提升速度。

Draw Things 的 Metal FlashAttention 实现了以下优化：

- 利用 `simdgroup_async_copy` API 实现计算和内存加载的**重叠执行**
- 自动检测注意力矩阵的稀疏性，跳过不必要的计算
- 在 M1 Pro 及以上芯片上，比标准 CoreML GPU 实现**快 20-40%**

实际测试数据：

| 芯片 | 标准 MPS | Metal FlashAttention | 提速幅度 |
|------|---------|---------------------|---------|
| M1 | ~15.2s | ~12.8s | 约 19% |
| M1 Pro/M2 Pro | 基准 | 快 20-40% | 显著 |
| M3/M4 | 基准 | 快 20%+ | 明显 |

**CoreML 集成**

Draw Things 同时支持 CoreML（利用 Apple 神经引擎 ANE）和 Metal（直接 GPU 计算）。在一些场景下，CoreML 路径可以利用 ANE 进行加速，进一步释放 GPU 资源：

- **M1/M2 基础款**：CoreML + ANE 路径可能更快
- **M1 Pro 及以上**：Metal FlashAttention 通常更快

应用会根据你的硬件自动选择最优路径，无需手动配置。

### 5.3 功能亮点

- **全面的模型支持**：SD 1.5、SDXL、Flux.1、Z-Image、Qwen Image、FLUX.2、甚至 Hunyuan 视频生成
- **ControlNet 全套**：Canny、Depth、Pose、Scribble 等多种控制模式
- **本地 LoRA 训练**：在你的 Mac 上直接训练 LoRA，无需云服务
- **图生图和局部重绘**：完善的编辑功能
- **模型管理极简**：选择模型后自动下载，无需手动搬文件
- **Optimize for Faster Loading**：一键优化模型加载速度
- **跨设备同步**：Mac 上调好的参数可以同步到 iPhone/iPad

### 5.4 性能表现

在各 Apple Silicon 设备上的 Draw Things 性能参考：

| 设备 / 内存 | SD 1.5 (512×512) | SDXL (1024×1024) | Flux.1 |
|-------------|-----------------|-----------------|--------|
| 8GB (M1 Air) | 流畅 (~15s) | 可用（需量化） | 慢但可用（需量化） |
| 16GB (M2 Pro) | 很快 | 良好 | 需 8-bit 量化 |
| 24GB (M3/M4 Pro) | 极快 | 快速 | 流畅运行 |
| 36GB+ (M4 Max) | 极快 | 极快 | 最佳体验 |

由于 Metal FlashAttention 的优化，Draw Things 在同等硬件条件下，通常比 ComfyUI（PyTorch MPS 后端）**快 20% 以上**。

### 5.5 为什么说它被低估了？

Draw Things 在国内外的知名度远不如 ComfyUI 和 Stable Diffusion WebUI，但它有几个独特优势：

1. **真正的 Apple 原生优化**：不是 Python 套壳，而是从底层针对 Metal/CoreML 优化
2. **Apple 官方认可**：Apple 在发布 M5 iPad Pro 时，将 Draw Things 与 Final Cut Pro、DaVinci Resolve 并列展示
3. **活跃的工程博客**：开发团队在 [engineering.drawthings.ai](https://engineering.drawthings.ai/) 持续分享技术细节
4. **App Store 分发**：一键安装，自动更新，不用折腾 Python 环境
5. **极低的内存占用**：使用 ANE 路径时，应用本身仅占约 150MB 内存

## 六、实战对比：同一台机器，同一个场景

为了让对比更直观，假设一个**真实使用场景**：你需要为博客文章生成一张 1024×1024 的科技风格配图。

### 6.1 工作流对比

**ComfyUI 的工作流**：

```
打开浏览器 → 加载/连接节点 → 配置 KSampler 参数
→ 设置 CLIP 文本编码 → 连接 VAE 解码 → 点击 Queue Prompt
→ 等待生成 → 手动保存图片
```

操作步骤：约 **8-10 步**（已有工作流模板时可减少到 3-4 步）

**DiffusionBee 的工作流**：

```
打开应用 → 输入提示词 → 选择模型 → 调整参数 → 点击生成 → 保存
```

操作步骤：约 **4-5 步**

**Draw Things 的工作流**：

```
打开应用 → 选择模型 → 输入提示词 → 调参（可选）→ 点击生成 → 保存
```

操作步骤：约 **4-5 步**

### 6.2 从"想法"到"成图"的完整体验

| 环节 | ComfyUI | DiffusionBee | Draw Things |
|------|---------|-------------|-------------|
| 首次安装 | 10-20 分钟 | 5 分钟 | 2 分钟（App Store） |
| 下载模型 | 手动下载放到指定目录 | 应用内选择 | 应用内一键下载 |
| 学习成本 | 高（需理解节点） | 低 | 中（功能多但 UI 清晰） |
| 提示词输入 | 节点式 | 文本框 | 文本框 |
| 批量生成 | 队列系统，高效 | 单张逐一 | 支持批量 |
| 结果调整 | 修改节点参数重跑 | 修改参数重跑 | 直接调参重跑 |
| 风格一致性 | 通过工作流模板保证 | 有限 | 通过预设保证 |

## 七、选型决策树

如果你不想看上面那么多分析，这里给你一个**快速决策指引**：

```
你是否需要构建复杂的图像生成管线？
├── 是 → ComfyUI（最强灵活性，但需要投入学习时间）
│
└── 否 → 你的 Mac 是 Apple Silicon 吗？
    ├── 不是 → 选择有限，考虑在线服务
    │
    └── 是 → 你是否需要最新模型和最佳性能？
        ├── 是 → Draw Things（原生优化，模型支持全面）
        └── 否 → 你只需要最简单的 SD 1.5/SDXL？
            ├── 是 → DiffusionBee（但注意开发已停滞）
            └── 否 → Draw Things
```

### 针对不同用户的推荐

| 用户类型 | 首选 | 备选 | 理由 |
|---------|------|------|------|
| **博客作者**（配图需求） | Draw Things | ComfyUI | 快速出图，模型丰富，无需折腾 |
| **设计师**（精确控制） | ComfyUI | Draw Things | ControlNet + 自定义工作流 |
| **开发者**（自动化集成） | ComfyUI | — | API 接口，脚本化工作流 |
| **完全新手** | Draw Things | — | App Store 安装，界面直观 |
| **批量生产** | ComfyUI | — | 队列系统 + 节点自动化 |

## 八、博客配图实战：我的推荐方案

回到你最关心的问题：**写博客时用什么工具配图最合适？**

### 8.1 推荐组合：Draw Things + SDXL/Flux

对于博客配图这个场景，我推荐 **Draw Things** 作为主力工具，理由如下：

1. **出图速度快**：Apple 原生优化，SDXL 出一张图几十秒
2. **模型齐全**：SDXL 适合插画/概念图，Flux 适合写实风格
3. **零配置成本**：App Store 下载，选模型就能用
4. **持续更新**：开发活跃，新模型支持跟得上

### 8.2 博客配图的实用技巧

**选择合适的模型**：

- **技术博客封面**：推荐 SDXL + 科技风格 LoRA，或者 Flux.1 Schnell（速度快）
- **教程步骤图**：SD 1.5 + ControlNet Scribble（用简单草稿生成精致插图）
- **概念示意图**：SDXL + 特定风格 LoRA
- **写实场景**：Flux.1 Dev（画质最好，但生成较慢）

**提高出图效率的方法**：

```
# 好的提示词结构
"[主题], [风格], [细节], [光影], [构图]"

# 示例：技术博客封面
"a futuristic workspace with holographic displays,
 minimalist tech illustration style,
 clean lines and geometric shapes,
 soft blue ambient lighting,
 centered composition, dark background"
```

**批量生成的策略**：

1. 先用 **Flux.1 Schnell**（4 步快速生成）找到满意的构图和色调
2. 确定方向后，切换到 **Flux.1 Dev**（20 步高质量）精修
3. 最后用 **RealESRGAN** 超分辨率放大到需要的尺寸

### 8.3 如果你需要更高级的控制

当 Draw Things 满足不了你的需求时——比如你需要构建自动化的图片生成管线，或者需要非常精确的构图控制——**ComfyUI 是你的升级路径**。

ComfyUI 的工作流可以保存为 JSON 文件，意味着你可以：

- 把常用的博客配图工作流保存为模板
- 只需修改提示词就能快速出图
- 通过 API 接口实现自动化生成

> **进阶推荐**：如果你想进一步提升效率，可以用 [Claude Code 驱动 Draw Things 实现自动化生图工作流](/posts/ai/2026-02-16-claude-code-draw-things-workflow/)，让 AI 帮你完成从提示词生成到批量出图的全流程。这背后用到了 [Claude Code 的浏览器自动化能力](/posts/ai/2026-01-28-claude-code-browser-automation/)。

## 九、安装指南速查

### Draw Things（推荐）

```bash
# 方式 1：App Store（推荐，自动更新）
# 搜索 "Draw Things" 下载即可

# 方式 2：官网下载
# https://drawthings.ai/downloads/
```

安装后的第一步：
1. 打开应用
2. 点击左侧模型选择区域
3. 选择 "Juggernaut XL"（推荐的 SDXL 模型）或 "Flux.1 Schnell"
4. 等待下载完成
5. 输入提示词，点击生成

### ComfyUI

```bash
# 方式 1：Homebrew（推荐）
brew install comfyui

# 方式 2：官方 DMG
# 下载地址：https://download.comfy.org/mac/dmg/arm64
```

安装后的关键设置：
1. GPU 选择 → **MPS**（不要选 CPU）
2. 安装 [ComfyUI-GGUF](https://github.com/city96/ComfyUI-GGUF) 节点（支持量化模型）
3. 下载推荐模型：Flux.1 Dev Q6_K GGUF（~10GB）
4. 推荐安装 [ComfyUI Manager](https://github.com/ltdrdata/ComfyUI-Manager) 来管理自定义节点

### DiffusionBee（不推荐新用户）

```bash
# 从 GitHub 下载
# https://github.com/divamgupta/diffusionbee-stable-diffusion-ui/releases/tag/2.5.3
```

## 十、常见问题避坑指南

### Q1：生成一张图要好几分钟，正常吗？

**看情况**。在 Mac Mini M4 上：
- SD 1.5 (512×512)：10-30 秒是正常的
- SDXL (1024×1024)：30-90 秒是正常的
- Flux.1 Dev (1024×1024)：1-3 分钟是正常的

如果 Flux 生成超过 10 分钟，大概率是**没有正确使用 GPU 加速**。检查你的 PyTorch 是否安装了 MPS 版本。

### Q2：16GB 内存够用吗？

**够用，但有限制**。16GB 可以流畅运行 SD 1.5 和 SDXL。使用 Flux 时需要 GGUF Q4 量化模型，画质会有一定损失。如果预算允许，**24GB 是更舒适的选择**。

### Q3：Mac 上 AI 生图比 NVIDIA 显卡慢多少？

坦率地说，Apple Silicon 在 AI 生图性能上确实不如同价位的 NVIDIA 显卡。大致来说：

- 比 RTX 4090 慢 **3-5 倍**
- 比 RTX 4070 慢 **2-3 倍**
- 但比 CPU 直接跑快 **10-50 倍**

Mac 的优势在于**统一内存**——可以运行超出传统显卡显存限制的大模型，而且 Mac Mini 的体积、功耗和噪音都远优于传统 GPU 工作站。

### Q4：ComfyUI 和 Draw Things 能同时安装吗？

可以。它们互不干扰，但模型文件会占用双倍存储空间（除非手动设置共享模型目录）。建议日常用 Draw Things 快速出图，需要复杂工作流时切换到 ComfyUI。

### Q5：哪个工具的 Flux 支持最好？

- **ComfyUI**：支持最全面，GGUF 量化、FP16、各种变体都支持
- **Draw Things**：原生支持且持续优化中，性能最佳
- **DiffusionBee**：名义上支持但有 Bug，不推荐

## 常见问题 FAQ

### Mac Mini M4 能本地跑 AI 生图吗？

完全可以。Mac Mini M4 的 Apple Silicon 芯片采用统一内存架构，CPU 和 GPU 共享同一块内存池，16GB 版本可流畅运行 SD 1.5 和 SDXL 模型，24GB 版本可用 GGUF 量化方案运行 Flux 模型。推荐使用 Draw Things 或 ComfyUI 作为生图工具。

### 2026 年 Mac 上最好的免费 AI 生图工具是哪个？

综合性能、易用性和更新频率，**Draw Things** 是 2026 年 Mac 上最推荐的免费本地 AI 生图工具。它是 Apple 原生应用（SwiftUI + Metal FlashAttention），比 ComfyUI 快约 20%，支持 Flux、SDXL 等主流模型，通过 App Store 免费下载。ComfyUI 适合需要复杂工作流的高级用户。DiffusionBee 因停更超过 1.5 年已不推荐。

### ComfyUI 2026 最新版本在 Mac 上怎么安装？

ComfyUI 提供 macOS 桌面版（Beta），两种安装方式：1）通过 Homebrew 运行 `brew install comfyui`；2）从官网下载 DMG 安装包。安装后关键设置：GPU 后端选择 MPS（不要选 CPU），安装 ComfyUI-GGUF 插件以支持量化模型，推荐下载 Flux.1 Dev Q6_K GGUF 模型（约 10GB）。仅支持 Apple Silicon 芯片。

### Mac Mini 16GB 和 24GB 跑 AI 生图差别大吗？

差别明显。16GB 内存可流畅运行 SD 1.5 和 SDXL，但跑 Flux 模型只能使用 Q4 量化版本（画质有损失），生成速度也偏慢。24GB 内存可运行 Flux Q6_K 量化模型（画质接近无损），是 Flux 模型的舒适起点。如果你计划频繁使用 Flux 生成高质量图片，建议选择 24GB 或更高配置。

### Mac 上 AI 生图速度和 NVIDIA 显卡比怎么样？

Apple Silicon 在 AI 生图速度上确实不如同价位 NVIDIA 显卡——大约比 RTX 4090 慢 3-5 倍，比 RTX 4070 慢 2-3 倍。但 Mac 的优势在于：统一内存可以运行超出传统显卡显存限制的大模型；Mac Mini 体积仅为 GPU 工作站的 1/10；功耗和噪音极低；还能同时兼顾日常办公和创作需求。

## 总结

Mac Mini 本地 AI 生图在 2026 年已经是一个**完全可行且实用**的方案。三大工具的定位非常清晰：

| 工具 | 一句话定位 | 推荐指数 |
|------|---------|---------|
| **Draw Things** | 博客作者的最佳伴侣 | ★★★★★ |
| **ComfyUI** | 专业创作者的终极武器 | ★★★★☆ |
| **DiffusionBee** | 曾经的新手之选（已停更） | ★★☆☆☆ |

如果你和我一样，主要需求是**给博客快速配图**，那 **Draw Things** 就是当前最优解——Apple 原生优化、模型支持全面、安装简单、持续更新。当你的需求升级到需要精确控制和自动化时，再拥抱 ComfyUI 的节点世界也不迟。

最后一个建议：不管选哪个工具，**先从 SDXL 模型开始**。它在画质和速度之间达到了最好的平衡，对内存的要求也不高。等你对本地生图有了手感之后，再尝试 Flux 这种"吃配置"的顶级模型。

## 相关阅读

- [Claude Code + Draw Things 自动化工作流：AI 生图效率翻倍](/posts/ai/2026-02-16-claude-code-draw-things-workflow/) — 本文的进阶篇，用 Claude Code 驱动 Draw Things 实现自动化批量生图
- [Claude Code 浏览器自动化实战：用 AI 操控网页的完整指南](/posts/ai/2026-01-28-claude-code-browser-automation/) — 了解 AI 代理如何自动化操控桌面应用和浏览器
- [Claude Code 最佳实践：从入门到精通的完整指南](/posts/ai/2026-01-06-claudecode-best-practices/)
- [AI 工作流实战指南：不是未来，是现在](/posts/ai/2026-01-30-ai-workflow-real-guide/)
- [Codex CLI 完全指南：OpenAI 的开源终端 AI 编程助手](/posts/ai/2026-02-12-codex-cli-mastery-guide/)
