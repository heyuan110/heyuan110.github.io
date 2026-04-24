# 搜索词动态聚类算法

在本地 Bash 工具中用 `python3 << 'PYEOF'` 执行以下代码（RUBE 过渡期也可用其远程沙箱），对 GSC 搜索词进行动态聚类分析。

## 核心代码

```python
# 1. 按语言分类
zh_queries = [q for q in queries if any(ord(c) > 0x4e00 for c in q['keys'][0])]
en_queries = [q for q in queries if not any(ord(c) > 0x4e00 for c in q['keys'][0])]

# 2. 提取高频词根做动态聚类（不预设固定集群）
from collections import Counter
def extract_clusters(queries, top_n=8):
    """从关键词中提取高频主题词，动态生成集群"""
    words = []
    for q in queries:
        kw = q['keys'][0].lower()
        # 提取2-gram和关键实体
        tokens = kw.split()
        words.extend([' '.join(tokens[i:i+2]) for i in range(len(tokens)-1)])
    freq = Counter(words).most_common(top_n)
    return freq  # 返回最高频的主题词作为集群名
```

## 关键原则

- **不要预设固定集群**。热点会变——上个月的头部关键词下个月可能消失
- 每次运行都从数据中动态发现当前的热点集群
- 中文搜索词（含汉字）和英文搜索词分别聚类

## 输出格式

```
中文搜索 Top 5 集群（按展示量）：
1. <集群名> — XX 个关键词，总展示 XX
2. ...

英文搜索 Top 5 集群（按展示量）：
1. <集群名> — XX 个关键词，总展示 XX
2. ...
```
