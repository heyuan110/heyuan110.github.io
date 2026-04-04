# 图表生成方案

## 方案 A（首选）：Rube MCP + Gemini AI 生图

### 第一步：搜索工具

```
调用 RUBE_SEARCH_TOOLS：
  query: "generate an AI image from a text prompt"
  session: {generate_id: true}
```

### 第二步：构造提示词并生成

根据内容和选定的布局/风格构造英文提示词，参考 [prompt-guide.md](prompt-guide.md) 获取提示词构造指南。

```
调用 RUBE_MULTI_EXECUTE_TOOL：
  tool_slug: GEMINI_GENERATE_IMAGE
  arguments:
    prompt: <英文提示词>
    model: "gemini-2.5-flash-image"
    aspect_ratio: "16:9"
  sync_response_to_workbench: false
```

### 第三步：下载并转换

图片 URL 在返回结果的 `data.image.s3url` 中（URL 有时效，需尽快下载）。

使用 [convert-to-webp.py](convert-to-webp.py) 下载并转换：

```bash
python3 .claude/skills/blog-diagram/references/convert-to-webp.py \
  --url "<s3url>" \
  --output "<输出文件名>.webp" \
  --max-width 1200
```

## 重要说明

- **提示词必须用英文**——英文提示词生成效果更好
- **图片中英文版共用**——同一篇文章的中英文版共享所有配图
- 命名格式：`diagram-<简短描述>.webp`（或用户通过 `--output` 指定）
- 最大宽度 1200px，质量 85，WebP 格式
- 生成后必须用 Read 工具查看图片，确认内容与主题相关且结构清晰
