# 提示词构造指南

## 通用结构

所有图表的提示词按这个顺序组织：

```
[标题] - [布局类型]

布局: [从 layouts.md 中提取的视觉结构描述]

内容区域:
- 区域 1: [具体内容，用真实数据]
- 区域 2: [具体内容，用真实数据]
...

标签: [文章中的具体数字、术语、指标]
配色: [语义化配色方案]
风格: [风格修饰词]
画幅: [16:9 / 1:1 / 9:16]

干净构图，充足留白。简洁背景。
No watermarks, no logos.
```

## 风格修饰词速查

| 风格 | 提示词关键描述 |
|------|--------------|
| craft | `Hand-crafted paper texture, warm organic feel, craft materials, cutout style` |
| blueprint | `Technical blueprint, engineering diagram, grid background, precise lines, cool blue tones` |
| corporate | `Flat vector, vibrant colors, bold shapes, modern corporate illustration` |
| schematic | `Technical schematic, precise lines, component diagram, engineering precision` |
| wireframe | `Grayscale wireframe, UI mockup style, clean lines, minimal` |
| chalkboard | `Chalk on blackboard, white/colored chalk, hand-drawn, educational` |
| pixel | `Pixel art, 8-bit retro, grid-aligned, chunky shapes` |
| minimal | `Ultra-minimal line art, single weight stroke, maximum whitespace` |

## 核心原则

1. **先布局后内容** — 先描述空间结构，再填充具体内容
2. **用真实数据** — 标签、数字、术语都来自文章，不要编造
3. **语义化配色** — 颜色传达含义（红=警告/差、绿=好/高效、蓝=技术/中性、橙=注意）
4. **留白优先** — 40-60% 的空间是留白，不要填满
5. **简化人物** — 如果需要人物，用简化轮廓，不要写实

## 避免事项

- 模糊描述（"一张好看的架构图"）
- 没有真实数据的空标签
- 过于复杂的场景（超过 8 个节点就开始混乱）
- 依赖 AI 生成精确文字（大段文字会乱码）
