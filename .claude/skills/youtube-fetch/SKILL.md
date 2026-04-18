---
name: youtube-fetch
description: "抓取 YouTube（及 yt-dlp 支持的其它平台）视频的完整字幕、元数据、章节、关键帧。使用此 skill 当用户：(1) 提供视频 URL 让你写文章 (2) 让你总结/分析一段视频 (3) 需要从视频里提取 PPT/界面截图。自动处理：有字幕直接抓 yt-dlp 字幕、无字幕降级到 whisper 转写、--frames 用 ffmpeg 场景检测抽关键帧。"
---

# YouTube Fetch — 视频素材一键抓取

把视频转成 LLM 可读的素材包：纯文本字幕、带时间戳字幕、章节、元数据、封面，按需抽关键帧。

## 何时使用

- 用户给一个视频 URL（YouTube / Bilibili / 任何 yt-dlp 支持的平台），需要把内容当文章素材
- 需要总结/分析一段视频
- 需要从视频里提取 PPT 切换、UI 截图、代码画面

⚠️ 不要再用 WebFetch 硬抓 YouTube/Bilibili 页面——拿到的只有 footer。视频内容必须走本 skill。

## 用法

```bash
bash .claude/skills/youtube-fetch/fetch.sh <url> [选项]
```

### 选项

| 选项 | 作用 |
|------|------|
| `--frames` | 用 ffmpeg 场景检测抽关键帧（PPT 切换、UI 截图） |
| `--prefer-whisper` | 跳过自动字幕，直接走 whisper（中文视频强烈推荐） |
| `--transcribe` | 同 `--prefer-whisper`（保留别名） |
| `--no-auto-whisper` | 关闭「中文视频自动启用 whisper」的智能判断 |
| `--full` | = `--frames` + 保留 `video.mp4` 本体 |
| `--out <dir>` | 自定义输出目录（默认 `cache/youtube/<videoId>/`） |
| `--whisper-model <m>` | whisper 模型 tiny/base/small/medium/large（默认 medium） |
| `--scene <0.0-1.0>` | ffmpeg 场景检测阈值（默认 0.4，PPT 类视频可降到 0.3） |

**字幕来源决策（自动判断）**：

```
1. 视频有人工字幕（uploader uploaded）         → 用人工字幕（最准）
2. 视频只有 YouTube auto-subtitle + 英文       → 用 auto-subtitle
3. 视频只有 YouTube auto-subtitle + 中文       → 自动切 whisper（auto-sub 中文质量差）
4. 视频完全没字幕                              → 自动切 whisper
5. 用户加 --prefer-whisper 或 --transcribe     → 跳过所有字幕，强制 whisper
6. 用户加 --no-auto-whisper                    → 关闭中文自动判断，按 1-2 走
```

## 输出结构

```
cache/youtube/<videoId>/
├── metadata.json      # 标题/作者/时长/描述/view count/upload date
├── transcript.srt     # 带时间戳字幕（SRT）
├── transcript.txt     # 纯文本字幕（喂 LLM 最方便）
├── transcript.md      # 带时间戳的可读 markdown，每行一句
├── chapters.json      # YouTube 章节（如果作者打了）
├── thumbnail.jpg      # 视频封面
├── frames/            # 仅 --frames 时
│   └── scene-NNNN.jpg
└── video.mp4          # 仅 --full 时保留
```

## 决策矩阵

| 场景 | 命令 |
|------|------|
| 文字内容为主的视频，写文章 | `bash fetch.sh <url>` |
| 演讲/教程/课程，需要看 PPT | `bash fetch.sh <url> --frames` |
| 视频没有字幕，或字幕乱码 | `bash fetch.sh <url> --transcribe` |
| 想完整保留素材以备后用 | `bash fetch.sh <url> --full` |
| PPT 密集的演讲，要更多关键帧 | `bash fetch.sh <url> --frames --scene 0.3` |

## 与 blog-writer 的协作

**写「参考视频 <url>，写一篇」类型文章时的标准前置动作：**

1. 调本 skill 拿全文：`bash .claude/skills/youtube-fetch/fetch.sh <url>`
2. Read `cache/youtube/<id>/transcript.txt` 形成对视频的完整理解
3. Read `cache/youtube/<id>/metadata.json` 取标题、作者、时长、章节
4. 技术演讲类加 `--frames` 参数，后续用 Read 直接看 frames/scene-*.jpg 抽关键画面
5. 进入 blog-writer 的步骤 2「深度研究」+ 步骤 3「形成判断」
6. 写作时用 `transcript.md` 的时间戳定位回原视频引用

## 依赖

**必需（每次都要）**：
- `python3` ≥ 3.8 — 解析 SRT 和 JSON
- `yt-dlp` ≥ 2026.03 — 下载字幕和音频（`pip install -U yt-dlp`，YouTube 反爬频繁更新，旧版会失败）

**仅 `--frames` 需要**：
- `ffmpeg` — `brew install ffmpeg`

**无字幕兜底转写需要（auto-detect 中文视频也会触发）**：
- `whisper` — `pip install -U openai-whisper`
- `deno` — `brew install deno`（解 YouTube JS challenge 必需，2026 年起 YouTube 强制）
- `yt-dlp-ejs` — `pip install yt-dlp-ejs`（yt-dlp 的 EJS 插件，配合 deno 使用）

**一键体检环境**：

```bash
bash .claude/skills/youtube-fetch/fetch.sh doctor
```

输出会标 ✅/❌/⚠️ 并给具体安装命令。

## 已知坑

- **YouTube cookie 验证**：偶尔会报 "sign in to confirm you're not a bot"，加 `--cookies-from-browser chrome` 解决
  ```bash
  yt-dlp --cookies-from-browser chrome ...  # 直接改 fetch.sh 第 60 行那条
  ```
- **中文 auto-subtitle 质量参差**：YouTube 中文自动字幕断句和错字偶尔严重，关键观点核对原视频 1 分钟左右
- **whisper 中文准确率**：`medium` 约 85%，`large` 约 92% 但慢 3 倍。技术演讲推荐 large
- **ffmpeg 场景阈值**：默认 0.4 适合大部分视频。PPT 切换密集（演讲）→ 0.3；电影类长镜头 → 0.6
- **Bilibili / 抖音**：URL 直接喂 yt-dlp 也能抓，但中国平台经常需要 cookie + UA 伪装
- **超长视频**：>2 小时的视频，whisper 转写可能要 30 分钟以上。先看有没有字幕避免无谓等待

## 故障排查

| 报错 | 原因 | 解决 |
|------|------|------|
| `Could not resolve video id` | URL 不对或地区限制 | 换 URL 或挂代理 |
| `No subtitle track found` 但视频明明有字幕 | 字幕语言不在默认 list 里 | 改 fetch.sh 第 51 行 `--sub-langs` 加目标语言 |
| `whisper: command not found` | whisper 没装 | `pip install -U openai-whisper` |
| 抽出的 frames 数量异常少 | 场景检测阈值太高 | 加 `--scene 0.3` |
| 抽出 frames 数量爆炸（>100） | 场景检测阈值太低 | 加 `--scene 0.5` 或 `--scene 0.6` |
