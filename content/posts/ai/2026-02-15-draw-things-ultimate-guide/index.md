+++
date = '2026-02-15T01:00:00+08:00'
draft = false
title = 'Draw Things on Mac 2026: Tutorial + 40% Faster than ComfyUI'
description = "Draw Things is a free Mac/iOS app for local AI image generation, 20-40% faster than ComfyUI on Apple Silicon. Setup, LoRA training, Flux, and Claude Code MCP."
toc = true
tags = ['Draw Things', 'AI Image Generation', 'Mac', 'LoRA', 'ControlNet']
categories = ['AI Guides']
keywords = ['draw things mac', 'draw things macos', 'draw things ai', 'drawthings mac', 'draw things apple silicon', 'Draw Things review', 'Draw Things tutorial 2026', 'Draw Things vs ComfyUI', 'comfyui vs draw things', 'comfyui vs drawthings', 'local AI image generation Mac', 'Apple Silicon AI image generation', 'Metal FlashAttention', 'Flux on Mac', 'Draw Things LoRA training', 'Draw Things MCP', 'best Mac AI art tool 2026']

[[params.faqItems]]
question = "What is Draw Things and what makes it different from ComfyUI or Midjourney?"
answer = "Draw Things is a free macOS/iOS native AI image generation app — no Python, no Docker, no subscription, no cloud uploads. The differentiator is the engine: it is built on SwiftUI plus a custom inference runtime (s4nnc) with Metal FlashAttention v2, optimized end-to-end for Apple Silicon. On identical hardware it runs 20-40% faster than ComfyUI's PyTorch MPS backend, and image generation latency drops 43-120%. Unlike ComfyUI it ships local LoRA training, a JavaScript scripting API, and an official MCP server out of the box. Versus Midjourney: no $30/month bill, no Discord prompts, no upload of your reference images to someone else's server."

[[params.faqItems]]
question = "How much Mac memory do I need? Can a 16GB Mac Mini M4 really run this?"
answer = "Yes — 16GB is the sweet spot in 2026 thanks to quantization. Realistic configs by tier: 8GB Mac (M1 Air) runs SD 1.5 8-bit with Tiled Decoding at 512x512; 16GB Mac Mini M4 runs SDXL 8-bit or Flux.1 Schnell at 1024x1024 comfortably, and can even train SDXL LoRAs via QLoRA; 24GB+ Mac runs Flux.1 Dev Q6_K (~10GB on disk) at full quality. The key tricks are 8-bit/Q6_K quantization, Tiled Decoding for the VAE step, and Memory Saver mode during training. QLoRA can squeeze SD 1.5 LoRA training onto a 6GB iPhone 15 Pro."

[[params.faqItems]]
question = "Draw Things vs ComfyUI vs Midjourney — which one should I pick in 2026?"
answer = "Pick Draw Things if you are on Mac, want zero setup, value privacy, and need local LoRA training or MCP/Claude Code integration. Pick ComfyUI if you live inside complex node graphs, need bleeding-edge custom nodes from the community, or run a non-Mac GPU box. Pick Midjourney if you only want best-in-class aesthetics on a single prompt and do not care about cost, control, or local data. For most Mac users in 2026, Draw Things wins on the price-performance-privacy triangle — and it is the only one of the three that lets Claude Code generate images for you directly via MCP."

[[params.faqItems]]
question = "How do I train a local LoRA in Draw Things and integrate it with Claude Code via MCP?"
answer = "Local LoRA: open the PEFT tab, pick a base model (SDXL Base 1.0 is the safest start), load 5-20 consistent training images, set a unique trigger word, run 500-1000 steps first and test the checkpoint before going further (overfitting is the #1 beginner mistake). QLoRA support means a 16GB Mac Mini M4 handles SDXL fine. MCP integration: enable API Server in Draw Things settings (default port 7860), then run `claude mcp add -s user drawthings -- npx -y mcp-drawthings`. After that Claude Code can call generate_image and transform_image directly — you stay in the terminal, images land in ~/Pictures/drawthings-mcp/."

[[params.faqItems]]
question = "Can Draw Things generate video like Wan 2.2 or Hunyuan on a Mac?"
answer = "Yes, Draw Things supports Wan 2.2 5B (text-to-video), Hunyuan Video (high-quality video), and Stable Video Diffusion (image-to-video). Use the DDIM Trailing sampler for best motion coherence. Realistic hardware bar: 24GB+ unified memory is recommended — 16GB technically works for shorter Wan 2.2 5B clips at low resolution but you will fight memory pressure. This is currently the cleanest way to do local video generation on a Mac without spinning up a separate ComfyUI workflow."

[[params.faqItems]]
question = "Does Draw Things run on Intel Macs or only Apple Silicon?"
answer = "Draw Things is built for Apple Silicon: Metal FlashAttention v2 and the 20-40% speed edge over ComfyUI require an M1 or newer chip, and every memory-tier recommendation in this guide (8GB M1 Air up to 24GB+ Mac) assumes an M-series Mac. It can be installed on Intel Macs from the App Store, but without Metal FlashAttention generation is far slower, so treat an M1 with 8GB as the realistic entry point."

[[params.faqItems]]
question = "Is Draw Things free on Mac?"
answer = "Yes. Draw Things is completely free on macOS and iOS — no subscription, no paywall for local generation, no cloud uploads — and everything in this guide (LoRA training, JavaScript scripting, the MCP server for Claude Code, Wan 2.2 video) runs locally at no cost. The only money question is the Mac under it."
+++

![Draw Things Ultimate Guide: Local AI Image Generation on Mac cover image](cover.webp)

Your Mac is a **free AI art workstation** — no Midjourney subscription, no cloud uploads, no privacy concerns. All you need is a free app called **Draw Things**, and you can generate any style of AI image locally on your Mac.

Most people stop at "install it, type a prompt, hit generate." But Draw Things goes far deeper: **local LoRA training, JavaScript scripting for batch automation, ControlNet for precise control, and MCP integration that lets Claude Code generate images directly**. Even long-time users miss these capabilities.

This guide is the complete roadmap from beginner to power user. Whether you are brand new to AI image generation or already experienced, you will find something new here.

## What Is Draw Things and Why Choose It?

### One-Line Summary

Draw Things is a **completely free** macOS/iOS native AI image generation app. All computation runs locally — no internet required, no subscription needed.

### How It Compares to Alternatives

Several tools can run AI image generation on Mac — ComfyUI, DiffusionBee, Mochi Diffusion — but Draw Things has unique advantages:

| Feature | Draw Things | ComfyUI | DiffusionBee |
|---------|-----------|---------|-------------|
| **Apple Optimization** | Metal FlashAttention (20-40% faster) | PyTorch MPS (generic) | No special optimization |
| **Installation** | One-click App Store | Homebrew / DMG | DMG download |
| **Local LoRA Training** | Supported | Not supported | Not supported |
| **Script Automation** | JavaScript API | Node workflows | Not supported |
| **MCP Integration** | Ready-made MCP Server | None | None |
| **Video Generation** | Wan 2.2 / Hunyuan supported | Supported | Not supported |
| **Development Activity** | Actively updated | Actively updated | Stalled 1.5 years |
| **Price** | Free | Free | Free |

The key differentiator: Draw Things is not a Python wrapper. It uses **SwiftUI + a custom inference engine (s4nnc)** built from the ground up for Apple Silicon. Think of it as the difference between running a game through an emulator versus a native port — the performance gap is fundamental.

### Metal FlashAttention: The Speed Secret

Draw Things achieves its performance edge through a proprietary technology — **Metal FlashAttention**.

Standard attention computation materializes the entire attention matrix in memory before performing multiplication. This is like spreading all your scratch paper across the desk — run out of desk space and everything breaks.

Metal FlashAttention computes **row by row**: calculate a row, use it, discard it. You only need desk space for one row at a time, but the final answer is identical.

Real-world results:

- M1 Pro and above: **20-40% faster** than standard CoreML GPU
- Image generation latency reduced by **43-120%**
- Significantly lower memory usage

This means **on identical hardware, Draw Things runs faster than ComfyUI**.

## Getting Started: Your First Image in 5 Minutes

### Installation

Open the App Store, search for **"Draw Things"**, and install. That is it.

No Python, no terminal, no environment variables. This is the primary reason I recommend it to beginners.

### Downloading Your First Model

When you first open Draw Things, you need to select a model. Models are like an artist's "style" — different models excel at different things:

| Model | Best For | Speed | Memory |
|-------|---------|-------|--------|
| **Flux.1 Schnell** | General-purpose fast generation | Fastest | 16GB usable |
| **Juggernaut XL** | Photorealistic portraits | Medium | 16GB+ |
| **DreamShaper XL** | Illustration / concept art | Medium | 16GB+ |
| **Flux.1 Dev** | Maximum image quality | Slower | 24GB+ |
| **SD 1.5** | Lightweight entry-level | Fastest | 8GB usable |

**Beginner recommendation**: Start with **Flux.1 Schnell**. It only needs 4 steps to generate high-quality images, is fast, and produces great results — the ideal starting point.

Steps:
1. Click the model dropdown on the left panel
2. Find "Flux.1 Schnell" in the list
3. Click the cloud icon to download
4. Wait for the download to finish (approximately 5-10GB)

### Generating Your First Image

Once the model is downloaded:

1. Type your desired scene description in the **positive prompt** field (English works best)
2. Click the **Generate** button
3. Wait a few seconds to a minute
4. Your image appears!

A simple example:

```
a cozy coffee shop interior, warm lighting, wooden tables,
bookshelves on walls, rain outside the window, anime style
```

Congratulations — you are now using Draw Things. But this is just the tip of the iceberg.

## Prompt Engineering: From "It Works" to "It Looks Amazing"

Prompts are the soul of AI image generation. The same model can produce wildly different results depending on how well you write your prompt.

### Prompt Structure

Good prompts follow this formula:

```
[Subject] + [Environment/Scene] + [Style] + [Lighting] + [Quality Modifiers] + [Composition]
```

**Example**:

```
# Basic (mediocre results)
a cat sitting on a table

# Advanced (stunning results)
a fluffy orange tabby cat sitting on a rustic wooden table,
cozy kitchen background with morning sunlight streaming through window,
soft bokeh, warm color palette, professional photography,
shallow depth of field, 8k resolution
```

### Negative Prompts: Telling AI What You Don't Want

Negative prompts are equally important. They tell the AI "don't paint it like this":

```
# Universal negative prompt template
blurry, low quality, deformed, ugly, bad anatomy,
bad hands, extra fingers, mutated hands, poorly drawn face,
watermark, text, signature, cropped
```

> **Tip**: Flux models are less sensitive to negative prompts, while SDXL models rely heavily on them. If you are using SDXL, invest time in your negative prompt.

### Advanced Prompt Techniques

**Weight Adjustment**

Draw Things supports bracket-based keyword weighting:

```
# Increase weight (more emphasis)
(golden hour lighting:1.3)

# Decrease weight (less emphasis)
(background:0.7)
```

Values range from 0.1 to 2.0, with 1.0 as default. A value of 1.3 means 30% stronger than normal.

**Style Keyword Quick Reference**

| Desired Effect | Recommended Keywords |
|---------------|---------------------|
| Cinematic | cinematic lighting, film grain, anamorphic |
| Anime | anime style, cel shading, vibrant colors |
| Oil Painting | oil painting, thick brushstrokes, impressionist |
| Cyberpunk | cyberpunk, neon lights, rain-soaked streets |
| Minimalist | minimalist, clean lines, white space |
| Photorealistic | photorealistic, RAW photo, 35mm film |

**SDXL Hidden Parameter**

SDXL models support a second prompt area (typically labeled "Additional Prompt" or "Prompt 2"). Many users overlook this. Use the first prompt for **content** and the second for **style and quality** — separating concerns produces better results:

```
# Prompt 1 (content)
a samurai standing on a cliff overlooking a misty valley

# Prompt 2 (style)
masterpiece, best quality, extremely detailed, sharp focus,
professional digital painting, dramatic lighting
```

## Parameter Tuning: Master These to Outperform 80% of Users

### Core Parameters Explained

| Parameter | Purpose | Recommended Range | Analogy |
|-----------|---------|-------------------|---------|
| **Steps** | Generation iterations | 20-30 | Number of revision passes. More is finer, but diminishing returns |
| **CFG Scale** | Prompt adherence | 4.0-7.0 | "How obedient." Too high causes over-fitting and artifacts |
| **Seed** | Random seed | -1 (random) | Same seed + same params = same image. Note the seed when you find a good result |
| **Image Size** | Output resolution | 1024×1024 | Larger is slower. Start small, upscale later |

### Sampler Selection Guide

Samplers are the algorithms AI uses to "paint." Draw Things offers 19 samplers, but you only need to know these:

| Your Model | Recommended Sampler | Reason |
|-----------|-------------------|--------|
| **SD 1.5 / v2** | DPM++ 2M Karras | Classic, stable, great quality |
| **SDXL** | DPM++ SDE Karras | Rich detail, great for realism |
| **Flux.1** | Euler A Trailing | Optimized for Flow models |
| **SD3** | Euler A Trailing | Same as above |
| **Video (Wan 2.2)** | DDIM Trailing | Best motion coherence |

> **Sampler name decoder**:
> - **Karras**: Noise scheduler that accelerates convergence, saves ~20% steps
> - **SDE**: Stochastic Differential Equation, increases variety and detail
> - **AYS**: Adaptive step size, achieves equal quality with fewer steps
> - **Trailing**: Designed specifically for Flow models (Flux, SD3)

### Overlooked Acceleration Settings

**Optimize for Faster Loading**

In model settings, there is an "Optimize for Faster Loading" option. When enabled, Draw Things preprocesses the model once, significantly speeding up every subsequent load. On 8GB devices, this is **essential**.

**Tiled Decoding**

By default, the decoder processes the entire image at once, which is memory-intensive. Tiled Decoding splits the image into small blocks and decodes them one at a time, dramatically reducing peak memory usage.

Best for:
- 8GB / 16GB memory devices
- Large image generation (e.g., 2048×2048)
- When running other applications simultaneously

**Tiled Diffusion**

Similar to Tiled Decoding, but operates during the generation phase rather than decoding. It splits large image generation into multiple blocks, each generated independently and then stitched together. This makes **generating 4K images on a 16GB Mac possible**.

## ControlNet: Making AI Follow Your Direction

ControlNet is the technology that transforms "random generation" into "precise control." It lets you **provide a reference image** and tell the AI "follow this structure/pose/outline."

### Understanding Control Types

| Control Type | Input | Use Case | Difficulty |
|-------------|-------|----------|-----------|
| **Scribble** | Hand-drawn sketch | Turn rough sketches into polished artwork | Beginner |
| **Canny** | Edge detection | Keep original contours, change style | Beginner |
| **Depth** | Depth map | Preserve 3D spatial structure | Intermediate |
| **Pose** | Skeleton map | Control character poses | Intermediate |
| **Color Palette** | Color reference | Control color scheme | Beginner |
| **IP Adapter** | Reference image | Maintain style consistency | Advanced |

### Practical Example: Scribble to Illustration

This is the most useful workflow for **content creators** — draw a rough composition on paper, photograph it, and let AI refine it into a polished illustration.

Steps:
1. Draw a simple composition sketch on paper (stick figures are fine)
2. Photograph or screenshot it
3. Open the **Control** tab in Draw Things
4. Select the **Scribble** model
5. Upload your sketch
6. Write a prompt describing the desired final result
7. Generate!

**Key parameter adjustments**:

- **Weight**: Start at **0.7**. 1.0 sticks too rigidly to the original; 0.5 is too loose
- **Control Importance**: Choose **Balanced** for a good trade-off between control and creativity
- **Start/End**: Set to **0-0.7**. This means the AI references the control image for the first 70% of generation and adds its own detail for the final 30%

### Power Move: Multi-Control Stacking

Draw Things supports **stacking multiple ControlNets simultaneously**. For example:

```
Depth (spatial structure) + Canny (outlines) + Color Palette (colors)
```

This is like giving an artist three reference sheets at once — "here's the room layout," "here are the object outlines," "here's the color scheme" — dramatically improving controllability.

> **Note**: The **order in which you add controls matters**. Place the most important control first. When stacking, lower each control's weight (e.g., 0.5-0.6 each) to avoid over-constraining and producing stiff results.

## Local LoRA Training: Build Your Own Custom Model

This is Draw Things' most impressive hidden feature — **train LoRA fine-tuned models directly on your Mac or iPhone**.

### What Is LoRA?

LoRA (Low-Rank Adaptation) is like installing a "style plugin" on a base model. The base model is a "generalist artist," and LoRA transforms it into "a specialist who paints your specific style/character/scene."

For example, you can train a LoRA to make AI specifically generate your cat, your cartoon avatar, or a particular illustration style you love.

### Training Preparation

**Requirements**:
- 5-20 high-quality training images (same subject/style)
- Mac with at least 16GB memory (24GB+ is more comfortable)
- 30 minutes to 4.5 hours of training time (depending on configuration)

**Image preparation tips**:
- Style, lighting, and quality should be **consistent** across images
- For character training, include photos from different angles
- Minimum resolution of 512×512
- Avoid watermarks and text interference

### Training Steps

1. Open Draw Things and go to the **PEFT** tab
2. Select a base model:
   - **SDXL Base 1.0**: Recommended, well-balanced
   - **Flux.1 Dev**: Highest quality, but memory-hungry
   - **Kwai Kolors**: Efficient, trains faster
3. Set the LoRA name and **trigger word**

```
# Example: Training a LoRA for your cat
LoRA name: my_cat_mimi
Trigger word: mimi_cat

# When generating, just include mimi_cat in your prompt
# and the AI will produce images of your cat
```

4. Import training images and configure captions

**Auto-captioning tip**: Draw Things includes two built-in captioning models — **Blip2** and **Moondream2**:
- Blip2: Brief descriptions, suitable for simple subjects
- Moondream2: Detailed descriptions, suitable for complex scenes

After generating captions, prepend your **trigger word** to each caption.

5. Set training parameters

| Parameter | SDXL Recommended | Flux Recommended |
|-----------|-----------------|-----------------|
| Network Dimension | 16 | 16 |
| Training Steps | 1500-2000 | 1500-2000 |
| Learning Rate | 0.0001 | 0.0004 |
| Image Resolution | 512×512 minimum | 512×512 minimum |

6. Start training and wait for completion

### Advanced Training Tips

**The 500-Step Checkpoint Rule**

Do not blindly wait for 2000 steps to finish. Pause at around 500-1000 steps and test the current checkpoint. If it already looks good, stop there. **Overfitting is the most common beginner mistake** — symptoms include generated images with fixed poses, noise artifacts, and repetitive patterns.

**QLoRA for Memory Savings**

A technical breakthrough in Draw Things is **QLoRA** support — training LoRA directly on quantized model weights. The LoRA network runs at FP32 precision while the base model runs at FP16. This means:

- **iPhone 15 Pro (6GB usable memory)** can train SD 1.5 LoRAs
- **Mac Mini M4 16GB** can comfortably train SDXL LoRAs
- Training speed exceeds theoretical predictions thanks to Metal FlashAttention optimization

**Memory Saver Setting**

If memory runs tight during training, enable **Memory Saver** in training settings:
- **Balanced**: Trade-off between speed and memory
- **Minimal**: Maximum memory savings (slower)

### Processing Training Results

After training completes:
1. Find your LoRA in the LoRA Manager
2. Quantize to **16-bit** or **8-bit** format (reduces file size)
3. Load the LoRA when generating images and include the trigger word in your prompt

```
# Using a trained LoRA for generation
mimi_cat sitting on a windowsill, sunset background,
warm lighting, cozy atmosphere
```

## Script Automation: The Batch Processing Secret

This is a feature 90% of Draw Things users do not know about — the **JavaScript scripting API**.

### What Can Scripts Do?

- Automatically load specific model + LoRA combinations
- Batch-generate images with different prompts and parameters
- Auto-save to designated directories
- Create interactive parameter panels
- Implement custom workflows

### Four Global Objects

The Draw Things scripting API provides four core objects:

```javascript
// 1. pipeline - Image generation pipeline
pipeline.run({
  prompt: "a beautiful sunset over mountains",
  negativePrompt: "blurry, low quality",
  width: 1024,
  height: 1024,
  steps: 20,
  guidanceScale: 7.0,
  seed: -1  // -1 = random
});

// 2. canvas - Infinite canvas control
canvas.clear();           // Clear canvas
canvas.saveImage("output.png");  // Save current image

// 3. filesystem - File system access
const picDir = filesystem.pictures.path;  // Get pictures directory path

// 4. requestFromUser - User interaction
// Creates parameter input panels (detailed below)
```

### Practical Script: Blog Cover Batch Generator

This script generates cover images for multiple blog posts in one run:

```javascript
// Blog cover batch generation script
const covers = [
  {
    name: "ai-workflow",
    prompt: "futuristic workspace with holographic displays, " +
            "clean minimalist design, blue ambient lighting, " +
            "tech blog cover style, no text"
  },
  {
    name: "python-tips",
    prompt: "a python snake made of golden code characters, " +
            "dark background, matrix-style digital rain, " +
            "cinematic lighting, no text"
  },
  {
    name: "docker-guide",
    prompt: "blue whale carrying colorful containers on its back, " +
            "ocean scene, sunset, digital art style, " +
            "professional illustration, no text"
  }
];

// Generate one by one
for (const cover of covers) {
  pipeline.run({
    prompt: cover.prompt,
    negativePrompt: "text, watermark, blurry, low quality",
    width: 1200,
    height: 630,  // Optimal social media ratio
    steps: 20,
    guidanceScale: 6.0,
    seed: -1
  });
  // Images appear on canvas automatically
  // Save manually or via canvas API
}
```

### Script Installation

1. Write a `.js` script file in any text editor
2. Open Draw Things → Scripts tab
3. Click "Add Script" → select your file
4. Run!

Script file path on Mac:
```
~/Library/Containers/Draw Things/Data/Scripts/
```

> **Community scripts**: Draw Things maintains an official [community-scripts](https://github.com/drawthingsai/community-scripts) repository with ready-to-use scripts.

## MCP Integration: Let Claude Code Generate Images for You

This is the most exciting workflow — using **MCP (Model Context Protocol)** to let Claude Code call Draw Things directly. When writing blog posts, you never need to switch apps; your AI assistant generates images on demand.

### Setup Steps

**Step 1: Enable the Draw Things API Server**

1. Open Draw Things
2. Click Settings (gear icon)
3. Enable **"API Server"**
4. Default port: `7860`

Verify it is working:
```bash
curl http://localhost:7860
# If you get a response, the API is running
```

**Step 2: Install the MCP Server**

Run in your terminal:
```bash
# Global install (available across all projects, recommended)
claude mcp add -s user drawthings -- npx -y mcp-drawthings
```

Then restart Claude Code.

**Step 3: Start Using It**

In Claude Code, you can now say:

```
Generate a blog cover image, theme: Python programming,
tech style, dark background, 1200x630 dimensions
```

Claude Code will automatically invoke the Draw Things MCP tool to generate the image and save it to `~/Pictures/drawthings-mcp/`.

### MCP Tools Available

| Tool | Function | Use Case |
|------|----------|----------|
| `check_status` | Check API connection | Troubleshooting |
| `get_config` | Get current model and settings | Confirm configuration |
| `generate_image` | Text-to-image | Most common |
| `transform_image` | Image-to-image | Style transfer, modifications |

### Environment Variable Configuration

For custom settings, configure these environment variables:

```bash
DRAWTHINGS_HOST=localhost     # API host (default)
DRAWTHINGS_PORT=7860          # API port (default)
DRAWTHINGS_OUTPUT_DIR=~/Pictures/drawthings-mcp  # Output directory
```

> **Real workflow**: My current blog writing process — write the article in Claude Code, when I need images I ask it to call Draw Things, images save automatically, I review the results, and reference them in the article if satisfied. The entire process **never leaves the terminal**. This is an experience ComfyUI cannot match.

## Model Selection In-Depth Guide

### Model Family Quick Reference

| Model Family | Strengths | Memory | Recommended For |
|-------------|-----------|--------|----------------|
| **SD 1.5** | Classic, rich ecosystem | 8GB+ | Lightweight use, many LoRAs available |
| **SDXL** | Quality leap, rich detail | 16GB+ | Daily creative workhorse |
| **Flux.1 Schnell** | 4-step fast generation | 16GB+ | Rapid iteration, drafting |
| **Flux.1 Dev** | Maximum quality | 24GB+ | Final output, high-quality needs |
| **Z-Image-Turbo** | Low resource, fast | 16GB+ | Resource-constrained environments |
| **Kwai Kolors** | Strong Chinese understanding | 16GB+ | Chinese prompt scenarios |

### Quantized Models: The Low-Memory Solution

If your Mac has limited memory (16GB), **quantized models** are essential knowledge.

Quantization is like image compression — the original is a BMP (huge but lossless), quantized becomes JPEG (much smaller, slight quality trade-off). Applied to models:

| Quantization Level | Size (Flux Dev example) | Quality | Recommended Config |
|-------------------|------------------------|---------|-------------------|
| FP16 original | ~24GB | Best | 48GB+ |
| 8-bit | ~13GB | Near-lossless | 32GB+ |
| **Q6_K** | **~10GB** | **Recommended** | **24GB** |
| Q4_KS | ~7GB | Noticeable loss | 16GB |

To use quantized models in Draw Things: Settings → Model → select the **8-bit** option, or choose the quantized version when downloading.

### Where to Get LoRAs

| Source | Characteristics | URL |
|--------|----------------|-----|
| **Civitai** | Largest LoRA community | [civitai.com](https://civitai.com/) |
| **HuggingFace** | Developer-friendly | [huggingface.co](https://huggingface.co/) |
| **Draw Things Built-in** | Direct download, no import needed | Browse in-app |

To import external LoRAs: Settings → LoRA → Manage → Import → select file or paste URL.

## Performance Optimization: Maximize Your Mac

### Best Configuration by Memory Tier

**8GB Mac (M1 Air, etc.)**:

```
Model: SD 1.5 (8-bit quantized)
Sampler: DPM++ 2M Karras
Steps: 15-20
Resolution: 512×512
Must enable: Tiled Decoding, Optimize for Faster Loading
```

**16GB Mac (M2/M4 Mac Mini base)**:

```
Model: SDXL (8-bit) or Flux.1 Schnell
Sampler: DPM++ SDE Karras (SDXL) / Euler A Trailing (Flux)
Steps: 20-25
Resolution: 1024×1024
Recommended: Tiled Decoding
```

**24GB+ Mac (M4 Pro, etc.)**:

```
Model: Flux.1 Dev (Q6_K quantized) or SDXL (FP16)
Sampler: Choose based on model recommendation
Steps: 20-30
Resolution: 1024×1024 - 2048×2048
Tiled Diffusion: Optional, enable for very large images
```

### The "Small-Then-Large" Workflow

Experienced users follow this process to save time:

1. **Small image rapid prototyping** (512×512, 15 steps) — find the right composition and colors
2. **Record the Seed value** — lock in that random seed
3. **Regenerate at higher resolution** (1024×1024, 25 steps) — use the same seed for an HD version
4. **Upscale** (if needed) — use the built-in ESRGAN upscaler to reach 2048 or even 4096

This is **3-5x more efficient** than starting with high resolution from the beginning.

### Confirm Metal FlashAttention v2

Make sure your Draw Things version has Metal FlashAttention v2 enabled. Check the related option in Settings. If your device supports it (M1 and above), this optimization is enabled by default, but it is worth confirming.

v2 reduces memory usage by an additional **20-25%** compared to v1, especially noticeable during LoRA training.

## Hardware That Makes Draw Things Fly

Draw Things is free — the only money question is the Mac under it:

- **[Mac mini M4, 24GB](https://www.amazon.com/s?k=Mac+mini+M4+24GB&tag=heyuan110-20)** — this guide's benchmark machine; SDXL and quantized Flux run comfortably
- **[Portable SSD, 2TB](https://www.amazon.com/s?k=portable+NVMe+SSD+2TB&tag=heyuan110-20)** — LoRA training sets and model collections outgrow internal storage fast

*As an Amazon Associate I earn from qualifying purchases. Links open Amazon search so you can pick the exact configuration.*

## Hidden Power-User Features

### Moodboard Multi-Image Reference

Draw Things has a powerful but little-known feature — **Moodboard**. You can place multiple reference images, and the AI will synthesize style elements from all of them to generate a new image.

Use case: You have 3-4 illustration styles you like and want the AI to blend them into a new piece. Place them all in the Moodboard and combine with IP Adapter for remarkable results.

### PuLID Face Transfer

PuLID is a face control technology supported by Draw Things. It preserves specific facial features in generated characters while changing scenes, clothing, and style. Ideal for creating illustration series that require character consistency.

### Video Generation

Yes, Draw Things does not just generate images — it can **generate video**. Supported models include:

- **Wan 2.2 5B**: Text-to-video generation
- **Hunyuan Video**: High-quality video generation
- **Stable Video Diffusion**: Image-to-video conversion

Video generation has higher hardware requirements — 24GB+ memory recommended.

### Bridge Mode

The Draw Things API Server supports **Bridge Mode**. This lets you use a powerful Mac (such as a Mac Studio) as a rendering server while other devices (MacBook, iPad, iPhone) send generation requests over the network.

Example setup for users with two Macs:
- Mac Mini M4 Pro running the Draw Things API Server
- MacBook Air sending remote generation requests while coding or writing

### iCloud Sync

Draw Things supports syncing settings and presets via iCloud. Parameters you configure on your Mac are instantly available when you open Draw Things on your iPad or iPhone. Capture inspiration on the go with quick mobile generation.

## Troubleshooting Common Issues

### Q1: Generated characters always have deformed hands?

This is a classic AI image generation problem. Solutions:
1. Add `bad hands, extra fingers, mutated hands` to your negative prompt
2. Use SDXL or Flux models (significantly better than SD 1.5)
3. Apply **Pose ControlNet** to constrain hand positioning
4. Increase Steps slightly (25-30)

### Q2: Images always look too dark or washed out?

Explicitly specify lighting and color in your prompt:
```
vibrant colors, bright lighting, high contrast, colorful
```
Also check if CFG Scale is set too high (above 10 tends to produce gray results).

### Q3: Downloaded LoRA has no effect after loading?

Check two things:
1. Does the LoRA match the **base model**? (An SDXL LoRA will not work on SD 1.5)
2. Does your prompt include the LoRA's **trigger word**?

### Q4: LoRA training crashes with out-of-memory error?

1. Reduce training resolution to 512×512
2. Enable **Memory Saver (Minimal)**
3. Close other applications to free memory
4. Use an 8-bit quantized base model
5. Reduce Network Dimension (8 instead of 16)

### Q5: Claude Code cannot connect to the API Server?

Troubleshoot in order:
1. Is Draw Things running? Is API Server enabled?
2. Does `curl http://localhost:7860` return a response?
3. Is a model loaded? (Generation fails with no model loaded)
4. Is the MCP Server installed correctly? Try restarting Claude Code

### Q6: Does Draw Things run on Intel Macs or only Apple Silicon?

Draw Things is built for Apple Silicon. Metal FlashAttention v2 — the source of the 20-40% speed edge over ComfyUI — requires an M1 or newer chip, and every memory-tier recommendation above assumes an M-series Mac. It can be installed on Intel Macs from the App Store, but without Metal FlashAttention generation is far slower, so treat an M1 with 8GB as the realistic entry point.

### Q7: Is Draw Things free on Mac?

Yes. Draw Things is completely free on macOS and iOS — no subscription, no paywall for local generation, no cloud uploads. LoRA training, JavaScript scripting, the MCP server, and video generation all run locally at no cost. The only money question is the Mac under it.

## Conclusion

Draw Things is the most **underrated** AI image generation tool on Mac. It is not just "an app that generates pictures" — it is a complete local AI image creation platform:

- **Beginners**: App Store install → download model → type prompt → generate. Up and running in 5 minutes
- **Intermediate**: Master ControlNet for precise control, sampler tuning, and prompt engineering to dramatically improve output quality
- **Advanced**: Train custom LoRAs locally, automate batch workflows with JavaScript, integrate with Claude Code via MCP
- **Power users**: Build a local rendering cluster with Bridge Mode, connect the API Server to any toolchain

Most importantly — **all of this is completely free, completely local, and completely private**.

If this guide helped you, bookmark it and start experimenting. AI image generation is a skill that only clicks after you have generated your first 100 images. Start creating!

## Related Reading

- [Mac Mini Local AI Image Generation: ComfyUI vs DiffusionBee vs Draw Things](/posts/ai/2026-02-15-mac-mini-local-image-generation/)
- [AI Workflow Practical Guide: Not the Future, It's Now](/posts/ai/2026-01-30-ai-workflow-real-guide/)
- [Claude Code Best Practices: Complete Guide from Beginner to Expert](/posts/ai/2026-01-06-claudecode-best-practices/)
- [Claude Code Browser Automation: Complete Guide to AI Web Control](/posts/ai/2026-01-28-claude-code-browser-automation/)
