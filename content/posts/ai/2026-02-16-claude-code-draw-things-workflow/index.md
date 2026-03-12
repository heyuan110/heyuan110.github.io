+++
date = '2026-02-16T18:00:00+08:00'
draft = false
title = 'Claude Code + Draw Things: Local AI Image Generation on Mac (2026 Guide)'
description = 'Set up Claude Code with Draw Things via MCP for fully local, free AI image generation on Mac. Covers configuration, 4 core tools, prompt engineering, and automated blog illustration workflows.'
toc = true
tags = ['Claude Code', 'Draw Things', 'MCP', 'AI Automation', 'Mac']
categories = ['AI Guides']
keywords = ['Claude Code Draw Things', 'MCP image generation', 'Mac local AI image generation', 'Draw Things MCP Server', 'Claude Code auto generate images', 'AI blog illustrations free']
+++

![Claude Code + Draw Things: Local AI Image Generation on Mac](cover.webp)

What is the most tedious part of writing a technical blog? It is not the code samples or the logic — it is **finding and creating images**.

Every article might cost you 30 minutes to an hour hunting for stock photos, generating images, and resizing them. Midjourney starts at $10/month and requires juggling Discord. DALL-E burns through API credits. Free stock images are generic and forgettable.

But what if **Claude Code could automatically generate images using Draw Things on your Mac while writing your article** — one command, both content and illustrations produced together, **completely free, completely local, no internet required**?

This is not a gimmick. This is real capability enabled by **MCP (Model Context Protocol)**. This guide walks you through setting up the entire workflow.

## The Architecture Behind This Setup

Here is the big picture. The system has three layers:

```
┌─────────────┐     MCP Protocol     ┌──────────────────┐     HTTP API       ┌──────────────┐
│ Claude Code  │ ◄──────────────►    │ mcp-drawthings   │ ◄──────────────►  │ Draw Things  │
│ (AI Brain)   │    stdio comm        │ (Node.js Bridge) │    localhost:7860  │ (Local Engine)│
└─────────────┘                      └──────────────────┘                    └──────────────┘
```

- **Claude Code**: Your AI coding assistant — understands requests, plans tasks, calls tools
- **mcp-drawthings**: An open-source MCP Server that translates Claude Code instructions into HTTP requests Draw Things understands
- **Draw Things**: A native macOS AI image generation engine that leverages Apple Silicon's Metal FlashAttention for fast, fully local computation

These three components are connected through standard protocols. Claude Code does not need to know Draw Things' API specifics — it simply says "generate an image" and the MCP Server handles the rest.

Think of it like telling an assistant "book me a restaurant." You do not care whether they called or used an app — you only care about the result.

## Setup: 3 Steps to Get Running

### Prerequisites

| Requirement | Details |
|-------------|---------|
| **macOS** | Apple Silicon (M1/M2/M3/M4) or Intel Mac |
| **Draw Things** | Free from the App Store |
| **Claude Code** | CLI installed (`npm install -g @anthropic-ai/claude-code`) |
| **Node.js** | v18+ (required by MCP Server) |

### Step 1: Enable the Draw Things API Server

Draw Things has a built-in HTTP API Server, but it is disabled by default:

1. Open Draw Things
2. Go to **Draw Things → Settings** (or press `⌘ + ,`)
3. Find the **"API Server"** or **"HTTP API"** option
4. Check **"Enable API Server"**
5. Keep the default port **7860**

Verify it is working:

```bash
# Verify the API is responding
curl http://127.0.0.1:7860/sdapi/v1/options
```

If you get a JSON response with configuration data, the API is ready.

### Step 2: Register the MCP Server

Register the Draw Things MCP Server in Claude Code with a single command:

```bash
claude mcp add drawthings -- npx -y mcp-drawthings
```

This does three things:
1. Registers an MCP Server named `drawthings` in Claude Code's config
2. Sets the startup command to `npx -y mcp-drawthings` (auto-downloads and runs)
3. Uses stdio for communication

After running this, `~/.claude.json` will contain:

```json
{
  "mcpServers": {
    "drawthings": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "mcp-drawthings"]
    }
  }
}
```

### Step 3: Verify the Connection

Restart Claude Code and type `/mcp` to check the MCP Server status. You should see `drawthings` listed as connected with 4 available tools.

Alternatively, test it directly:

```
Check if Draw Things is running properly
```

Claude Code will call the `check_status` tool and return Draw Things' status.

## The 4 Core Tools Explained

Once configured, Claude Code has access to 4 Draw Things tools. Understanding what each does is essential for building effective workflows.

### check_status — Health Check

**Purpose**: Verify that the Draw Things API Server is running.

**When to use**: Always check before generating images to avoid failed requests.

```
Example conversation:
User: Generate a cover image for my article
Claude Code: (calls check_status first, confirms Draw Things is online, then calls generate_image)
```

This tool takes no parameters and returns the connection status. Simple but critical — the first step in any automation pipeline is **checking the environment**.

### get_config — Read Current Settings

**Purpose**: Retrieve the currently loaded model, resolution, sampler, and other configuration from Draw Things.

**When to use**: Before generating images, check which model is loaded and whether you need to switch.

Returns information including:
- Currently loaded model name
- Default resolution
- Sampler type
- CFG Scale and other parameters

**Practical use**: If you want photorealistic output but an anime model is loaded, Claude Code can use `get_config` results to specify the correct model when calling `generate_image`.

### generate_image — Text-to-Image (Core Tool)

**Purpose**: Generate an image from a text prompt and save it to disk.

This is the most frequently used tool. Parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Image description text |
| `negative_prompt` | string | No | Elements to exclude |
| `width` | int | No | Image width (64-2048, default 512) |
| `height` | int | No | Image height (64-2048, default 512) |
| `steps` | int | No | Inference steps (1-150, default 20) |
| `cfg_scale` | float | No | Prompt guidance strength (1-30, default 7.5) |
| `seed` | int | No | Random seed (-1 = random) |
| `model` | string | No | Model filename |
| `output_path` | string | No | Custom save path |

**Key parameters explained**:

- **steps**: More steps = more detail but slower. Flux.1 Schnell needs only 4 steps; SD 1.5 typically needs 20-30
- **cfg_scale**: Higher values make the image follow the prompt more closely but may over-saturate. Recommended range: 5-10
- **output_path**: Save directly to your article directory, e.g., `content/posts/ai/xxx/cover.webp`

**Example request**:

```
Generate a tech blog cover image:
- Theme: AI programming automation
- Style: techy, dark background, blue-purple tones
- Size: 1200x630
- Save to content/posts/ai/2026-02-16-example/cover.png
```

Claude Code converts this into a `generate_image` call:

```json
{
  "prompt": "A futuristic tech illustration about AI programming automation, dark background with blue and purple gradient, neural network patterns, clean modern style, no text",
  "negative_prompt": "text, watermark, blurry, low quality",
  "width": 1200,
  "height": 630,
  "steps": 20,
  "cfg_scale": 7.5,
  "output_path": "content/posts/ai/2026-02-16-example/cover.png"
}
```

### transform_image — Image-to-Image

**Purpose**: Transform an existing image based on a text prompt — style transfer, modifications, enhancements.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | Transformation description |
| `image_path` | string | No* | Source image file path |
| `image_base64` | string | No* | Source image as Base64 |
| `denoising_strength` | float | No | Transformation intensity (0-1, default 0.75) |
| `negative_prompt` | string | No | Elements to exclude |
| `output_path` | string | No | Save path |

> *At least one of `image_path` or `image_base64` is required.*

**Understanding denoising_strength**:

- **0.1-0.3**: Subtle adjustments, retains 90%+ of the original — good for color/style tweaks
- **0.4-0.6**: Moderate transformation, keeps composition but changes details — good for style transfer
- **0.7-1.0**: Heavy rework, only keeps rough outlines — close to generating from scratch

**Typical use case**:

```
Convert this screenshot to a hand-drawn illustration:
- Source: content/posts/ai/screenshot.png
- Style: hand-drawn illustration, sketch style
- Strength: 0.6
```

## Practical Workflow: Automated Blog Illustrations

Now for the exciting part — **chaining these tools into an automated workflow**.

### The Scenario: One Command, Article + Images Together

Traditional workflow for writing a blog post about "MCP Protocol":

```
Write article (30min) → Find images (20min) → Resize (10min) → Check formatting (5min)
```

With Claude Code + Draw Things:

```
One instruction (1min) → Claude Code handles everything (5-10min)
```

### Full Workflow Demo

Enter this in Claude Code:

```
Write a technical blog post about MCP Protocol, including:
1. Article content
2. Cover image (1200x630, tech style)
3. 2-3 inline images
Save everything to the content/posts/ai/ directory
```

Claude Code's execution process:

```
Step 1: check_status
  → Confirm Draw Things is online ✓

Step 2: get_config
  → Get current model info (Flux.1 Schnell)

Step 3: Write the article
  → Generate index.md with front matter, body, internal links

Step 4: generate_image × 3 (sequential)
  → Cover: 1200×630 tech style
  → Figure 1: architecture diagram style
  → Figure 2: flowchart style

Step 5: Save all files to article directory
  → index.md + cover.webp + fig1.webp + fig2.webp

Step 6: Build verification
  → hugo --minify to confirm no errors
```

**No app switching required** — no browser for stock photos, no Photoshop for resizing, no manual CMS uploads.

### Prompt Engineering: Getting Great Images from AI

When Claude Code calls Draw Things, prompt quality determines image quality. Here is the formula for blog illustrations:

**Cover image formula**:

```
[subject description], [style], [color palette], [composition], [technical keywords]
negative: text, watermark, blurry, low quality, deformed
```

**Real-world examples**:

```
# Technical tutorial cover
"A clean modern illustration of AI workflow automation,
 interconnected nodes and data flows,
 dark blue gradient background,
 minimalist tech style,
 cinematic lighting, professional"

# Tool comparison article cover
"Split screen comparison of different AI tools,
 left side showing cloud services,
 right side showing local computing on Mac,
 tech aesthetic, blue and purple tones,
 isometric perspective"

# Concept explainer cover
"Abstract visualization of Model Context Protocol,
 glowing connection lines between AI and tools,
 futuristic digital landscape,
 dark theme with neon accents"
```

**Model recommendations**:

| Image Type | Recommended Model | Steps | CFG |
|-----------|-------------------|-------|-----|
| Tech-style covers | Flux.1 Schnell | 4 | 3.5 |
| Photorealistic | Juggernaut XL | 25 | 7.0 |
| Illustrations | DreamShaper XL | 25 | 7.5 |
| Quick drafts | SD 1.5 | 15 | 7.0 |

### Advanced: Unifying Visual Style with transform_image

When an article needs multiple images, AI-generated results may look inconsistent. Use `transform_image` to unify the style:

```
1. Generate one "reference image" you are happy with
2. Use transform_image on each additional image, using the reference as a base
3. Set denoising_strength = 0.3-0.5 to preserve content while unifying color and style
```

This is like applying the same filter to a set of photos — different content, consistent visual identity.

## Comparison: Why Go Local?

You might wonder: aren't cloud services like Midjourney and DALL-E 3 more convenient? Here is how they compare:

| Dimension | Claude Code + Draw Things | Midjourney | DALL-E 3 API |
|-----------|---------------------------|------------|-------------|
| **Cost** | Completely free | $10-60/month | $0.04-0.12/image |
| **Privacy** | Local processing, nothing uploaded | Images uploaded to cloud | Images sent to OpenAI |
| **Speed** | M1 Pro: 5-15 sec/image | 30-60 sec/image | 10-20 sec/image |
| **Offline** | Yes | No | No |
| **Custom models** | LoRA/fine-tuned supported | No | No |
| **Batch generation** | Unlimited | Quota limited | Pay per image |
| **Workflow integration** | Native MCP integration | Requires API wrapper | Requires API wrapper |
| **Resolution control** | Fully custom (64-2048) | Fixed options | Fixed options |

**Key advantages summarized**:

1. **Zero cost**: Draw Things is free + Apple Silicon compute is free
2. **Zero latency**: No network transfer — local GPU computes directly
3. **Zero data leakage**: Nothing leaves your machine
4. **Zero restrictions**: No quotas, no content review, no account bans

For technical bloggers, this saves **$120-720 per year** on image generation alone (based on Midjourney's $10/month standard plan).

## End-to-End Pipeline: From Trend Discovery to Publishing

Embed Claude Code + Draw Things into a complete content production pipeline and you can achieve "one-person tech publication" efficiency.

### Pipeline Architecture

```
┌─────────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────┐    ┌──────────┐
│  Discover    │ →  │  Research    │ →  │  Write + Auto   │ →  │  QA     │ →  │  Publish │
│  Trends      │    │  Deep Dive   │    │  Illustration   │    │  Hugo   │    │  Git     │
│  WebSearch   │    │  WebFetch    │    │  Write + Draw   │    │  Build  │    │  Push    │
└─────────────┘    └──────────────┘    └────────────────┘    └─────────┘    └──────────┘
```

### Ready-to-Use Command Template

Here is an end-to-end instruction you can paste directly into Claude Code:

```markdown
Complete the following automated blog publishing workflow:

1. **Research**: Search for the latest developments on "XXX technology", find 3-5 valuable sources
2. **Write article**:
   - Category: AI Guides
   - Style: In-depth technical tutorial, accessible language
   - Requirements: 3000-5000 words with code examples
3. **Auto-generate images**:
   - Cover: 1200×630, tech style, dark background
   - Inline images: 2-3 based on article content
   - All images saved as .webp
4. **Quality check**:
   - Front matter completeness
   - At least 3 internal links
   - Hugo build with no errors
5. **Save to**: content/posts/ai/ directory
```

### Image Format Conversion

Draw Things defaults to PNG output, but blogs benefit from WebP (smaller file size). Claude Code handles the conversion automatically:

```bash
# Convert PNG to WebP after generation
cwebp -q 85 -resize 1200 630 cover.png -o cover.webp
```

If `cwebp` is not installed, Python works too:

```python
from PIL import Image
img = Image.open("cover.png").resize((1200, 630), Image.LANCZOS)
img.save("cover.webp", "WEBP", quality=85)
```

## Troubleshooting

### Q1: Cannot connect to the Draw Things API?

**Symptom**: `check_status` returns a connection failure.

**Steps to fix**:
1. Confirm the Draw Things app is open
2. Confirm the API Server is enabled (Settings → API Server)
3. Verify port 7860: `curl http://127.0.0.1:7860/sdapi/v1/options`
4. If the port is in use, change it in Draw Things settings and update the MCP Server environment variable accordingly

### Q2: Generated images look bad?

**Possible causes**:
- **Prompt too simple**: Include at minimum subject + style + color palette + quality keywords
- **Too few steps**: SD 1.5/SDXL needs at least 20 steps; only Flux.1 Schnell can produce good results in 4 steps
- **Wrong model**: Do not use an anime model for photorealistic needs
- **Unreasonable resolution**: SD 1.5 works best at 512×512, SDXL at 1024×1024

### Q3: MCP Server throws "command not found"?

Make sure Node.js is installed and is version 18 or higher:

```bash
node --version  # Should show v18.x or higher
npx -y mcp-drawthings --help  # Manually test the MCP Server
```

If npx cannot be found, try the full path:

```bash
claude mcp add drawthings -- /usr/local/bin/npx -y mcp-drawthings
```

### Q4: Image generation is slow?

| Chip | 512×512 | 1024×1024 | 1200×630 |
|------|---------|-----------|----------|
| M1 | ~8s | ~25s | ~15s |
| M1 Pro/Max | ~5s | ~15s | ~10s |
| M2 Pro/Max | ~4s | ~12s | ~8s |
| M3 Pro/Max | ~3s | ~9s | ~6s |
| M4 Pro/Max | ~2s | ~7s | ~5s |

> These are approximate times for Flux.1 Schnell at 4 inference steps. Actual speed depends on model, steps, and system load.

If too slow:
- Use Flux.1 Schnell (only 4 steps needed)
- Generate at lower resolution, then upscale with `transform_image`
- Close other GPU-intensive applications

### Q5: Can it generate multiple images simultaneously?

The Draw Things API is synchronous — it processes one request at a time. However, Claude Code **automatically queues requests sequentially**. Just specify how many images you need, and Claude Code generates them one after another.

For higher parallelism, consider running multiple Draw Things instances on different ports with separate MCP Server configurations.

## Advanced Techniques

### Custom LoRA Models for Brand Consistency

If you want a unified brand style across blog illustrations, train your own LoRA model:

1. Use Draw Things' built-in [LoRA training feature](https://www.heyuan110.com/posts/ai/2026-02-15-draw-things-ultimate-guide/) to train your brand style
2. Specify the LoRA model in `generate_image` calls
3. All article images will share a consistent visual DNA

### Screenshot Enhancement Pipeline

Technical articles often include screenshots that look rough in their raw form. Use `transform_image` to polish them:

```
1. Capture raw screenshot → screenshot.png
2. transform_image: add rounded corners, drop shadow, gradient background
3. Output polished image → screenshot_styled.webp
```

### Visual Consistency Across Article Series

When writing a series, define a "visual spec" for Claude Code:

```markdown
# Series Article Image Spec

## Cover Images
- Size: 1200×630
- Colors: Dark blue gradient (#0f172a → #1e3a5f)
- Style: Minimalist tech illustration
- Must include: Abstract graphics related to the topic

## Inline Images
- Size: 800×450
- Style: Match cover image
- Use for: Architecture diagrams, flowcharts, comparisons
```

Add this spec to your CLAUDE.md or Skills file, and Claude Code will follow it automatically every time it generates images.

## Conclusion

The Claude Code + Draw Things combination gives your AI coding assistant **visual creation capabilities**. Through MCP protocol bridging:

- **Generate illustrations while writing** — no more interrupting your flow to find images
- **Fully local execution** — zero cost, zero privacy risk
- **Highly customizable** — model, style, and dimensions are all configurable
- **Pipeline-ready** — from trend discovery to article publishing in one seamless flow

If you are a Mac user, a technical blogger, or anyone who regularly needs illustrations, this setup is worth 10 minutes of your time. Once running, you will experience a **fundamental shift in your writing workflow** — because you never have to worry about images again.

---

**Quick Start Checklist**

```bash
# 1. Install Draw Things (free from the App Store)
# 2. Enable API Server (Settings → API Server → Enable)
# 3. Configure MCP Server
claude mcp add drawthings -- npx -y mcp-drawthings

# 4. Verify (after restarting Claude Code)
# Type: Check if Draw Things is running properly

# 5. Start using it
# Type: Generate a 1200x630 tech-style blog cover image
```

## Related Reading

- [Draw Things Complete Guide: Local AI Image Generation on Mac](/posts/ai/2026-02-15-draw-things-ultimate-guide/)
- [Mac Mini Local AI Image Generation: Best Value Setup](/posts/ai/2026-02-15-mac-mini-local-image-generation/)
- [Claude Code Browser Automation: 5 Methods Compared (2026)](/posts/ai/2026-01-28-claude-code-browser-automation/)
- [My AI Development Workflow: From Requirements to Deployment](/posts/ai/2026-01-19-ai-dev-workflow/)
- [Claude Code Best Practices Guide](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Claude Code Skills Complete Guide](/posts/ai/2026-01-08-claudecode-skill-guide/)
