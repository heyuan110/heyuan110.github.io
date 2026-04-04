# 各类型提示词模板

每种类型都有固定的提示词结构。用文章中的真实数据填充模板。

## 通用规则

所有提示词都必须包含：
- 布局结构描述（先说构图，再说内容）
- 文章中的真实数据做标签（具体数字、术语）
- 语义化配色（红=警告、绿=高效、蓝=技术）
- 风格特征描述
- 画幅声明
- `No watermarks, no logos.`

## infographic（信息图）

```
[标题] - 数据可视化

布局: [网格/放射/层级]

区域:
- 区域 1: [数据点，用文章中的具体数值]
- 区域 2: [对比，用文章中的具体指标]
- 区域 3: [总结/结论]

标签: [文章中的具体数字、百分比、术语]
配色: [语义化配色方案]
风格: [风格特征]
画幅: 16:9

干净构图，充足留白。简洁背景。主元素居中。
```

## scene（场景）

```
[标题] - 氛围场景

焦点: [主体]
氛围: [灯光、情绪、环境]
情绪: [要传达的情感]
色温: [暖/冷/中性]
风格: [风格特征]
画幅: 16:9

No text, no watermarks, no logos.
```

## flowchart（流程图）

```
[标题] - 流程图

布局: [左右/上下/环形]

步骤:
1. [步骤名] - [简述]
2. [步骤名] - [简述]
...

连接: [箭头类型、决策点]
风格: [风格特征]
画幅: 16:9

干净构图，充足留白。
```

## comparison（对比图）

```
[标题] - 对比视图

左侧 - [选项 A]:
- [要点 1，用文章数据]
- [要点 2，用文章数据]

右侧 - [选项 B]:
- [要点 1，用文章数据]
- [要点 2，用文章数据]

分隔: [视觉分隔方式]
风格: [风格特征]
画幅: 16:9
```

## framework（架构图）

```
[标题] - 概念架构

结构: [层级/网络/矩阵]

节点:
- [概念 1] - [角色]
- [概念 2] - [角色]

关系: [节点如何连接]
风格: [风格特征]
画幅: 16:9

干净构图，充足留白。
```

## timeline（时间线）

```
[标题] - 时间线

方向: [水平/垂直]

事件:
- [日期/阶段 1]: [里程碑]
- [日期/阶段 2]: [里程碑]

标记: [视觉标识]
风格: [风格特征]
画幅: 16:9
```

## 风格修饰词速查

| 风格 | 添加到提示词的关键描述 |
|------|-------------------|
| flat-vector | `Flat vector illustration, clean outlines, geometric shapes, uniform fills, no gradients, no shadows` |
| blueprint | `Technical blueprint style, engineering diagram, grid background, precise lines, cool blue tones` |
| minimal | `Ultra-minimal, generous whitespace (60%+), single focal element, subtle colors` |
| warm | `Warm hand-drawn style, organic lines, friendly rounded shapes, soft warm colors` |
| editorial | `Magazine-style infographic, professional layout, clean typography areas, balanced composition` |
| digital | `Polished digital style, subtle gradients, modern interface aesthetic, clean edges` |

## 避免事项

- 模糊描述（"一张好看的图"）
- 字面化的隐喻图
- 缺少具体标签/数据
- 没有描述布局就直接描述内容
- 用通用装饰元素代替内容相关元素
