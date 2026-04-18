#!/usr/bin/env bash
# youtube-fetch: pull transcript + metadata + (optional) key frames from a YouTube video
# Usage:
#   fetch.sh <url> [--frames] [--transcribe] [--full] [--out <dir>] [--whisper-model <m>]

set -euo pipefail

# ─── preflight: check required tools and guide user to install missing ones ────
detect_pkg_manager() {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    if command -v brew >/dev/null 2>&1; then echo "brew"; else echo "macos-no-brew"; fi
  elif command -v apt-get >/dev/null 2>&1; then echo "apt"
  elif command -v dnf >/dev/null 2>&1; then echo "dnf"
  elif command -v pacman >/dev/null 2>&1; then echo "pacman"
  else echo "unknown"
  fi
}

install_hint() {
  local tool="$1"
  local pm
  pm="$(detect_pkg_manager)"
  echo "" >&2
  echo "❌ 缺少依赖：$tool" >&2
  case "$tool" in
    yt-dlp)
      case "$pm" in
        brew)         echo "   👉 brew install yt-dlp" >&2 ;;
        apt)          echo "   👉 sudo apt install -y yt-dlp   # 或: pip install -U yt-dlp" >&2 ;;
        dnf)          echo "   👉 sudo dnf install -y yt-dlp   # 或: pip install -U yt-dlp" >&2 ;;
        pacman)       echo "   👉 sudo pacman -S yt-dlp" >&2 ;;
        *)            echo "   👉 pip install -U yt-dlp        # 跨平台通用" >&2 ;;
      esac
      ;;
    ffmpeg)
      case "$pm" in
        brew)         echo "   👉 brew install ffmpeg" >&2 ;;
        apt)          echo "   👉 sudo apt install -y ffmpeg" >&2 ;;
        dnf)          echo "   👉 sudo dnf install -y ffmpeg" >&2 ;;
        pacman)       echo "   👉 sudo pacman -S ffmpeg" >&2 ;;
        macos-no-brew)echo "   👉 先装 Homebrew (https://brew.sh) 后: brew install ffmpeg" >&2 ;;
        *)            echo "   👉 https://ffmpeg.org/download.html" >&2 ;;
      esac
      ;;
    whisper)
      echo "   👉 pip install -U openai-whisper" >&2
      echo "      （首次运行会下载模型：medium ~1.5GB / large ~3GB）" >&2
      ;;
    python3)
      case "$pm" in
        brew)         echo "   👉 brew install python@3.12" >&2 ;;
        apt)          echo "   👉 sudo apt install -y python3" >&2 ;;
        *)            echo "   👉 https://www.python.org/downloads/" >&2 ;;
      esac
      ;;
  esac
  echo "" >&2
}

require_tool() {
  local tool="$1"
  if ! command -v "$tool" >/dev/null 2>&1; then
    install_hint "$tool"
    exit 1
  fi
}

# ─── doctor 子命令：只检测环境，不跑任务 ────────────────────────────────────
if [[ "${1:-}" == "doctor" || "${1:-}" == "--doctor" ]]; then
  echo "🩺 youtube-fetch 环境体检"
  echo ""
  PASS=true
  for t in python3 yt-dlp; do
    if command -v "$t" >/dev/null 2>&1; then
      echo "  ✅ $t          $(command -v "$t")"
    else
      echo "  ❌ $t          未安装（必需）"
      PASS=false
    fi
  done
  for t in ffmpeg whisper deno; do
    if command -v "$t" >/dev/null 2>&1; then
      echo "  ✅ $t          $(command -v "$t")"
    else
      case "$t" in
        ffmpeg) echo "  ⚠️  $t          未安装（仅 --frames 时需要）" ;;
        whisper) echo "  ⚠️  $t          未安装（仅无字幕的视频做兜底转写时需要）" ;;
        deno) echo "  ⚠️  $t          未安装（YouTube JS challenge 需要 → brew install deno）" ;;
      esac
    fi
  done
  # yt-dlp version freshness check (YouTube changes protocol often)
  if command -v yt-dlp >/dev/null 2>&1; then
    YTV=$(yt-dlp --version 2>/dev/null | head -1)
    YTV_DATE=$(echo "$YTV" | tr '.' ' ' | awk '{printf "%04d-%02d-%02d", $1, $2, $3}')
    DAYS_OLD=$(python3 -c "from datetime import datetime; d=datetime.strptime('$YTV_DATE','%Y-%m-%d'); print((datetime.now()-d).days)" 2>/dev/null || echo "0")
    if [[ "$DAYS_OLD" -gt 60 ]]; then
      echo "  ⚠️  yt-dlp 版本 $YTV 已 $DAYS_OLD 天，YouTube 反爬频繁更新，建议升级 → pip install -U yt-dlp"
    fi
  fi
  # yt-dlp-ejs plugin check
  if python3 -c "import yt_dlp_ejs" 2>/dev/null; then
    echo "  ✅ yt-dlp-ejs    已安装（解 YouTube JS challenge 必需）"
  else
    echo "  ⚠️  yt-dlp-ejs    未安装 → pip install yt-dlp-ejs"
  fi
  echo ""
  if $PASS; then
    echo "✅ 必需依赖齐全，可以使用本 skill"
    echo ""
    echo "💡 想用 --transcribe（无字幕视频转写）需要："
    echo "   • whisper:     pip install -U openai-whisper"
    echo "   • deno:        brew install deno"
    echo "   • yt-dlp-ejs:  pip install yt-dlp-ejs"
    exit 0
  else
    echo "❌ 必需依赖缺失，请按上面提示安装"
    for t in python3 yt-dlp; do
      command -v "$t" >/dev/null 2>&1 || install_hint "$t"
    done
    exit 1
  fi
fi

# ─── parse args ────────────────────────────────────────────────────────────────
URL=""
EXTRACT_FRAMES=false
FORCE_TRANSCRIBE=false
NO_AUTO_WHISPER=false
DOWNLOAD_VIDEO=false
OUT_DIR=""
WHISPER_MODEL="medium"
SCENE_THRESHOLD="0.4"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --frames) EXTRACT_FRAMES=true; shift ;;
    --transcribe|--prefer-whisper) FORCE_TRANSCRIBE=true; shift ;;
    --no-auto-whisper) NO_AUTO_WHISPER=true; shift ;;
    --full) EXTRACT_FRAMES=true; DOWNLOAD_VIDEO=true; shift ;;
    --out) OUT_DIR="$2"; shift 2 ;;
    --whisper-model) WHISPER_MODEL="$2"; shift 2 ;;
    --scene) SCENE_THRESHOLD="$2"; shift 2 ;;
    -h|--help)
      cat <<EOF
Usage: fetch.sh <url> [选项]
       fetch.sh doctor                      # 检查环境依赖

选项:
  --frames               用 ffmpeg 场景检测抽关键帧
  --prefer-whisper       跳过自动字幕，直接走 whisper（中文视频强烈推荐）
  --transcribe           = --prefer-whisper（保留别名）
  --full                 = --frames + 保留视频文件
  --out <dir>            自定义输出目录（默认 cache/youtube/<id>/）
  --whisper-model <m>    whisper 模型 tiny/base/small/medium/large（默认 medium）
  --scene <0.0-1.0>      ffmpeg 场景检测阈值（默认 0.4）
EOF
      exit 0
      ;;
    -*)
      echo "Unknown flag: $1" >&2
      exit 1
      ;;
    *) URL="$1"; shift ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Usage: fetch.sh <url> [--frames] [--prefer-whisper] [--full] [--out <dir>] [--whisper-model <m>]" >&2
  echo "       fetch.sh --help          # 完整帮助" >&2
  echo "       fetch.sh doctor          # 检查环境依赖" >&2
  exit 1
fi

# Preflight: required tools (yt-dlp + python3 are always required)
require_tool python3
require_tool yt-dlp
# ffmpeg only needed if extracting frames or downloading video
if [[ "$EXTRACT_FRAMES" == true || "$DOWNLOAD_VIDEO" == true ]]; then
  require_tool ffmpeg
fi
# whisper only needed if --transcribe forced (auto-fallback also checks at runtime)
if [[ "$FORCE_TRANSCRIBE" == true ]]; then
  require_tool whisper
fi

# Resolve video id
VIDEO_ID="$(yt-dlp --get-id --no-warnings "$URL" 2>/dev/null | head -n1 || true)"
if [[ -z "$VIDEO_ID" ]]; then
  echo "Could not resolve video id from: $URL" >&2
  exit 1
fi

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="cache/youtube/$VIDEO_ID"
fi
mkdir -p "$OUT_DIR"
echo "==> Output dir: $OUT_DIR"

# Step 1: metadata + thumbnail + captions (no video download)
echo "==> Fetching metadata + auto-subtitles + thumbnail..."
yt-dlp \
  --no-warnings \
  --write-auto-subs --write-subs \
  --sub-langs "zh-Hans,zh,zh-CN,zh-TW,en,en-US,en-GB" \
  --convert-subs srt \
  --write-info-json --write-thumbnail --skip-download \
  -o "$OUT_DIR/source.%(ext)s" \
  "$URL" 2>&1 | tail -8 || true

# Normalize file names
[[ -f "$OUT_DIR/source.info.json" ]] && mv "$OUT_DIR/source.info.json" "$OUT_DIR/metadata.json"
for ext in jpg webp png; do
  if [[ -f "$OUT_DIR/source.$ext" ]]; then
    mv "$OUT_DIR/source.$ext" "$OUT_DIR/thumbnail.$ext"
    break
  fi
done

# Auto-detect Chinese videos: prefer whisper over auto-subs (which are notoriously bad for Chinese)
if [[ "$FORCE_TRANSCRIBE" != true && "$NO_AUTO_WHISPER" != true && -f "$OUT_DIR/metadata.json" ]]; then
  IS_CHINESE_AUTO_ONLY=$(python3 - <<PY
import json, re
m = json.load(open("$OUT_DIR/metadata.json"))
title = (m.get("title") or "") + (m.get("uploader") or "") + (m.get("channel") or "")
has_chinese = bool(re.search(r"[\u4e00-\u9fff]", title))
manual_subs = m.get("subtitles") or {}
auto_subs = m.get("automatic_captions") or {}
# True only if Chinese video AND no manual subs (auto-only situation)
print("yes" if has_chinese and not manual_subs else "no")
PY
)
  if [[ "$IS_CHINESE_AUTO_ONLY" == "yes" ]]; then
    echo "==> ⚠️  检测到中文视频且无人工字幕，自动启用 --prefer-whisper（YouTube 中文自动字幕质量较差）"
    echo "    （想用自动字幕请加 --no-auto-whisper，本次跳过此判断）"
    FORCE_TRANSCRIBE=true
    require_tool whisper
  fi
fi

# Pick the best caption file (Chinese first, then English)
CAPTION_FILE=""
for lang in zh-Hans zh zh-CN zh-TW en en-US en-GB; do
  for cand in "$OUT_DIR/source.$lang.srt"; do
    if [[ -f "$cand" ]]; then
      CAPTION_FILE="$cand"
      break 2
    fi
  done
done

# Whisper fallback
if [[ -z "$CAPTION_FILE" || "$FORCE_TRANSCRIBE" == true ]]; then
  if [[ -z "$CAPTION_FILE" ]]; then
    echo "==> No subtitle track found. Falling back to whisper..."
  else
    echo "==> --transcribe forced. Running whisper..."
  fi
  require_tool whisper
  # Download bestaudio without mp3 conversion (whisper handles webm/m4a/opus/mp3 directly)
  # --no-mtime avoids ffmpeg dependency for post-processing
  yt-dlp --no-warnings --no-mtime -f "bestaudio" \
    -o "$OUT_DIR/audio.%(ext)s" "$URL" 2>&1 | tail -3
  AUDIO_FILE=$(ls "$OUT_DIR"/audio.* 2>/dev/null | grep -vE '\.(part|ytdl)$' | head -1)
  if [[ -z "$AUDIO_FILE" || ! -s "$AUDIO_FILE" ]]; then
    echo "❌ 音频下载失败。常见原因：" >&2
    echo "   1. yt-dlp 版本过旧 → pip install -U yt-dlp" >&2
    echo "   2. 缺 deno（解 JS challenge）→ brew install deno" >&2
    echo "   3. 缺 yt-dlp-ejs 插件 → pip install yt-dlp-ejs" >&2
    echo "   4. 视频被地区限制 → 挂代理重试" >&2
    exit 1
  fi
  echo "==> Audio downloaded: $AUDIO_FILE ($(du -h "$AUDIO_FILE" | cut -f1))"
  whisper "$AUDIO_FILE" \
    --model "$WHISPER_MODEL" \
    --output_format srt \
    --output_dir "$OUT_DIR" 2>&1 | tail -3
  AUDIO_BASE=$(basename "$AUDIO_FILE" | sed 's/\.[^.]*$//')
  mv "$OUT_DIR/$AUDIO_BASE.srt" "$OUT_DIR/transcript.srt"
  CAPTION_FILE="$OUT_DIR/transcript.srt"
else
  echo "==> Using subtitle file: $CAPTION_FILE"
  cp "$CAPTION_FILE" "$OUT_DIR/transcript.srt"
fi

# SRT -> plain text + paragraph-broken markdown
echo "==> Generating plain text + markdown transcripts..."
python3 - "$OUT_DIR" <<'PY'
import re, sys, os, json, pathlib

out = pathlib.Path(sys.argv[1])
srt = (out / "transcript.srt").read_text(encoding="utf-8", errors="ignore")

blocks = re.split(r"\n\n+", srt.strip())
lines = []
md_lines = []
for block in blocks:
    parts = block.split("\n")
    if len(parts) < 3:
        continue
    # parts[0] index, parts[1] timestamp, parts[2:] text
    timestamp = parts[1] if "-->" in parts[1] else ""
    content = " ".join(p.strip() for p in parts[2:] if p.strip())
    if not content:
        continue
    lines.append(content)
    if timestamp:
        start = timestamp.split(" --> ")[0].split(",")[0]
        md_lines.append(f"[{start}] {content}")

(out / "transcript.txt").write_text(" ".join(lines), encoding="utf-8")
(out / "transcript.md").write_text("\n".join(md_lines), encoding="utf-8")
PY

# Extract chapters
echo "==> Extracting chapters (if any)..."
python3 - "$OUT_DIR" <<'PY'
import json, sys, pathlib
out = pathlib.Path(sys.argv[1])
meta_path = out / "metadata.json"
if not meta_path.exists():
    (out / "chapters.json").write_text("[]")
    sys.exit(0)
meta = json.loads(meta_path.read_text(encoding="utf-8"))
chapters = meta.get("chapters") or []
(out / "chapters.json").write_text(json.dumps(chapters, indent=2, ensure_ascii=False))
PY

# Optional: download video for frame extraction or --full
if [[ "$DOWNLOAD_VIDEO" == true || "$EXTRACT_FRAMES" == true ]]; then
  if [[ ! -f "$OUT_DIR/video.mp4" ]]; then
    echo "==> Downloading video (<=720p)..."
    yt-dlp --no-warnings -f "best[height<=720][ext=mp4]/best[height<=720]" \
      -o "$OUT_DIR/video.mp4" "$URL" 2>&1 | tail -3
  fi
fi

# Optional: scene-change frames
if [[ "$EXTRACT_FRAMES" == true ]]; then
  echo "==> Extracting scene-change frames (threshold=$SCENE_THRESHOLD)..."
  mkdir -p "$OUT_DIR/frames"
  ffmpeg -y -hide_banner -loglevel error -i "$OUT_DIR/video.mp4" \
    -vf "select='gt(scene,$SCENE_THRESHOLD)',scale=1280:-1" \
    -vsync vfr -frame_pts 1 \
    "$OUT_DIR/frames/scene-%04d.jpg"
  FRAME_COUNT=$(ls "$OUT_DIR/frames"/*.jpg 2>/dev/null | wc -l | tr -d ' ')
  echo "==> Extracted $FRAME_COUNT key frames"
fi

# Cleanup intermediate files
rm -f "$OUT_DIR"/source.*.srt "$OUT_DIR"/source.*.vtt "$OUT_DIR/audio.mp3"

# Final summary
echo ""
echo "✅ Done."
python3 - "$OUT_DIR" <<'PY'
import json, sys, pathlib
out = pathlib.Path(sys.argv[1])
meta = json.loads((out / "metadata.json").read_text(encoding="utf-8")) if (out / "metadata.json").exists() else {}
title = meta.get("title", "N/A")
uploader = meta.get("uploader") or meta.get("channel") or "N/A"
duration = meta.get("duration", 0)
m, s = divmod(int(duration), 60)
text = (out / "transcript.txt").read_text(encoding="utf-8") if (out / "transcript.txt").exists() else ""
chapters = json.loads((out / "chapters.json").read_text(encoding="utf-8")) if (out / "chapters.json").exists() else []
print(f"📺 Title:      {title}")
print(f"👤 Uploader:   {uploader}")
print(f"⏱  Duration:   {m}m{s}s")
print(f"📝 Transcript: {len(text)} chars / {len(text.split())} space-tokens")
print(f"📑 Chapters:   {len(chapters)}")
print(f"📂 Files in {out}:")
for p in sorted(out.iterdir()):
    if p.is_dir():
        n = sum(1 for _ in p.iterdir())
        print(f"   {p.name}/  ({n} files)")
    else:
        size = p.stat().st_size
        unit = "B" if size < 1024 else f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
        if size >= 1024:
            print(f"   {p.name}  ({unit})")
        else:
            print(f"   {p.name}  ({size} B)")
PY
