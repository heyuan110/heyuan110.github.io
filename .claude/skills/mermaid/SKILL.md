---
name: mermaid
description: Create flowcharts, sequence diagrams, state machines, class diagrams, Gantt charts, and mindmaps using simple text-based syntax. Best for process flows, API interactions, and technical documentation. NOT for data-driven charts (use vega), quick KPI visuals (use infographic), or layered system architecture (use architecture).
metadata:
  author: Mermaid is powered by Markdown Viewer — the best multi-platform Markdown extension (Chrome/Edge/Firefox/VS Code) with diagrams, formulas, and one-click Word export. Learn more at https://docu.md
---

# Mermaid Diagram Visualizer

**Quick Start:** Identify diagram type (flowchart/sequence/state/class/ER/gantt/mindmap) → Define nodes with shapes → Connect with arrows → Wrap in ` ```mermaid ` fence. Default: top-to-bottom (`TD`), use `flowchart` over `graph`, Unicode supported.

---

## Critical Syntax Rules

### Rule 1: List Syntax Conflicts
```
❌ [1. Item]     → "Unsupported markdown: list"
✅ [1.Item]      → Remove space after period
✅ [① Item]      → Use circled numbers ①②③④⑤⑥⑦⑧⑨⑩
✅ [(1) Item]    → Use parentheses
```

### Rule 2: Subgraph Naming
```
❌ subgraph AI Agent Core    → Space without quotes
✅ subgraph agent["AI Agent Core"]  → ID with display name
✅ subgraph agent            → Simple ID only
```

### Rule 3: Node References in Subgraphs
```
❌ Title --> AI Agent Core   → Reference display name
✅ Title --> agent           → Reference subgraph ID
```

### Rule 4: Special Characters in Node Text
```
✅ ["Text with spaces"]       → Quotes for spaces
✅ Use #quot; instead of "    → Avoid quotation marks
✅ Use #lpar;#rpar; for ()    → Avoid parentheses
```

### Rule 5: Use flowchart over graph
```
❌ graph TD      → Outdated
✅ flowchart TD  → Supports subgraph directions, more features
```

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| Diagram won't render | Check unmatched brackets, quotes |
| List syntax error | `[1.Item]` not `[1. Item]` |
| Subgraph reference fails | Use ID not display name |
| Too crowded | Trim to 2-3 representatives per branch — see [aesthetics.md §1](references/aesthetics.md) |
| Crossing connections | Use different layout direction or invisible edges `~~~` |
| Ugly / cramped / cut off | See [aesthetics.md](references/aesthetics.md) — do NOT swap to HTML before trying the 6 fixes there |
| Subgraph sizes uneven | Fill sparse groups up to match — [aesthetics.md §3](references/aesthetics.md) |
| LR diagram cut off at right | Switch to TB when subgraphs ≥ 4 — [aesthetics.md §2](references/aesthetics.md) |

## Aesthetics (how to make diagrams not ugly)

Rendering correctly ≠ looking good. When a user says "this chart is ugly / make it prettier / fix the layout," **optimize the existing diagram first — do not switch to HTML/architecture**. Full playbook with before/after examples, density ceilings, theme variable templates, and color palette lives at [references/aesthetics.md](references/aesthetics.md). Run its 10-item self-check after any non-trivial chart.

---

## Output Format

````markdown
```mermaid
[diagram code]
```
````

---

## Related Files

> For diagram-specific syntax and advanced features, refer to references below:

- [syntax.md](references/syntax.md) — Detailed syntax for all 14+ diagram types: flowchart shapes, sequence actors, class relationships, state transitions, ER cardinality, Gantt tasks, and more
