# 生图方案

## 方案 A（首选）：Rube MCP + Gemini AI 生图

### 第一步：搜索工具

```
调用 RUBE_SEARCH_TOOLS：
  query: "generate an AI image from a text prompt"
  session: {generate_id: true}
```

### 第二步：构造提示词并生成

先读取 [base-prompt.md](base-prompt.md) 获取系统级指令，然后根据文章内容和选定的维度构造提示词。

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
# 封面图（固定 1200x630）
python3 .claude/skills/blog-cover-image/references/convert-to-webp.py \
  --url "<s3url>" \
  --output "content/posts/ai/2026-xx-xx-slug/cover.webp" \
  --resize 1200x630
```

如果 AI 生图失败（连接不可用、安全过滤拦截等），使用方案 B。

---

## 方案 B（兜底）：Python/Pillow 程序化生成

当 AI 生图不可用时，用 [pillow-fallback.py](pillow-fallback.py) 程序化生成。

```bash
python3 .claude/skills/blog-cover-image/references/pillow-fallback.py \
  --title "文章标题" \
  --subtitle "文章描述前50字" \
  --tags "tag1,tag2,tag3" \
  --output "content/posts/ai/2026-xx-xx-slug/cover.webp"
```

脚本功能：深色渐变背景 + 自动换行标题 + 副标题 + 标签气泡。支持中英文字体（macOS 优先 STHeiti/PingFang，其他平台回退到默认字体）。

⚠️ 方案 B 生成后必须用 Read 工具查看图片，确认无乱码。
