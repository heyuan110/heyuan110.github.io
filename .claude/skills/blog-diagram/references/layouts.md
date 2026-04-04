# 布局定义

每种布局的视觉结构描述，用于构造生图提示词。

## linear-progression（线性流程）

```
视觉结构：水平或垂直排列的节点，用箭头依次连接。
适合：时间线、步骤教程、版本演进。
提示词关键描述：
- "Linear progression from left to right"
- "Connected steps with directional arrows"
- "Sequential flow, each step as a labeled card/node"
```

## binary-comparison（双栏对比）

```
视觉结构：左右分屏，中间有视觉分隔线。每侧列出各自的要点。
适合：A vs B、优缺点、before/after。
提示词关键描述：
- "Split layout, left side vs right side"
- "Clear visual separator in the center"
- "Symmetric structure, each side with icon + label pairs"
```

## comparison-matrix（对比矩阵）

```
视觉结构：网格/表格形式，行是维度，列是对比对象，交叉处填评分或图标。
适合：多工具横评、多维度对比。
提示词关键描述：
- "Grid matrix with rows and columns"
- "Column headers for compared items, row headers for criteria"
- "Check marks, scores, or color-coded cells at intersections"
```

## hierarchical-layers（层级金字塔）

```
视觉结构：上窄下宽的层级结构，从顶到底递进。
适合：技术栈、优先级金字塔、抽象层级。
提示词关键描述：
- "Pyramid or layered stack, widening from top to bottom"
- "Each layer labeled with its level name"
- "Color gradient from top (darkest/most important) to bottom"
```

## hub-spoke（中心辐射）

```
视觉结构：中心一个大节点，周围放射连接多个子节点。
适合：核心概念+关联要素、生态系统图、功能模块图。
提示词关键描述：
- "Central hub node connected to surrounding spoke nodes"
- "Radial layout, spokes evenly distributed around center"
- "Hub is largest/most prominent, spokes are smaller"
```

## tree-branching（树状分支）

```
视觉结构：从根节点向下/向右展开分支，逐级细化。
适合：分类体系、决策树、目录结构。
提示词关键描述：
- "Tree structure branching from root to leaves"
- "Each branch splits into sub-branches"
- "Indentation or spatial separation shows hierarchy"
```

## bento-grid（模块化方格）

```
视觉结构：不同大小的方格模块组成网格布局，每个模块一个主题。
适合：功能概览、多主题摘要、仪表盘。
提示词关键描述：
- "Bento box grid layout with varied-size modules"
- "Each module contains an icon + label + brief description"
- "Clean borders between modules, consistent padding"
```

## funnel（漏斗）

```
视觉结构：从上到下逐渐变窄的漏斗形状，每层标注数量/阶段。
适合：转化漏斗、筛选过程、用户旅程。
提示词关键描述：
- "Funnel shape, wide at top, narrow at bottom"
- "Each layer labeled with stage name and metric"
- "Color darkens or changes at each stage"
```

## circular-flow（环形循环）

```
视觉结构：环形闭合的流程，箭头指示循环方向。
适合：生命周期、反馈循环、持续改进流程。
提示词关键描述：
- "Circular flow diagram with clockwise arrows"
- "Steps arranged in a ring, connected by curved arrows"
- "No clear start/end, emphasizing continuous cycle"
```

## venn-diagram（维恩图）

```
视觉结构：2-3 个重叠的圆形区域，交集部分标注共同特征。
适合：概念重叠、技能交集、领域关系。
提示词关键描述：
- "Overlapping circles (2-3)"
- "Each circle labeled, intersection area highlighted"
- "Distinct colors for each circle, blended in overlap"
```

## bridge（桥梁）

```
视觉结构：左侧是问题/现状，右侧是目标/方案，中间是桥梁/路径。
适合：问题→解决方案、现状→目标。
提示词关键描述：
- "Two sides connected by a bridge element"
- "Left: problem/current state, Right: solution/target"
- "Bridge shows the transformation path"
```

## dashboard（仪表盘）

```
视觉结构：多个独立的指标卡片和小图表组合在一起。
适合：KPI 展示、数据概览、性能指标。
提示词关键描述：
- "Dashboard layout with multiple metric cards"
- "Each card shows a number, trend arrow, and label"
- "Mix of bar charts, line charts, and big numbers"
```
