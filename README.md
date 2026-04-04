# Bruce's Blog

Bruce 的个人技术博客，使用 [Hugo](https://gohugo.io/) 构建，部署在 GitHub Pages。

🌐 **访问地址**: [www.heyuan110.com](https://www.heyuan110.com/)

## 技术栈

- **静态网站生成器**: Hugo v0.153.2+ (Extended 版本)
- **主题**: [hermit-V2](https://github.com/1bl4z3r/hermit-V2)
- **部署**: GitHub Pages + GitHub Actions

## 多语言

博客支持**英文（默认）**和**中文**，每篇文章默认中英文双版本：

| 语言 | URL | 文件 |
|------|-----|------|
| English | `/posts/ai/slug/` | `index.md` |
| 中文 | `/zh/posts/ai/slug/` | `index.zh.md` |

## 内容分类

| 分类 | 说明 |
|------|------|
| **AI** | 工具评测、教程指南、架构设计、趋势分析、工具对比 |
| Java / Go / Docker / Linux / macOS | 归档 |

## 本地开发

### 前置要求

- [Hugo Extended](https://gohugo.io/installation/) v0.153.2 或更高版本
- Git

### 克隆项目

```bash
git clone --recursive https://github.com/heyuan110/heyuan110.github.io.git
cd heyuan110.github.io
```

### 常用命令

```bash
# 本地预览（包含草稿）
hugo server -D

# 本地预览（不含草稿）
hugo server

# 创建新文章
hugo new posts/<分类>/<文章名>.md

# 构建生产版本
hugo --minify

# 更新主题子模块
git submodule update --remote
```

访问 http://localhost:1313 预览博客。

## 部署

推送到 `code` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

配置文件：`.github/workflows/hugo.yml`

## 目录结构

```
.
├── content/
│   ├── posts/           # 博客文章
│   │   ├── ai/          # AI 系列（主要更新）
│   │   ├── java/        # Java 系列（归档）
│   │   ├── go/          # Go 系列（归档）
│   │   ├── docker/      # Docker 系列（归档）
│   │   ├── linux/       # Linux 系列（归档）
│   │   └── macos/       # macOS 系列（归档）
│   └── about.md         # 关于页面
├── static/              # 静态资源
├── themes/hermit-V2/    # 主题（git submodule）
├── hugo.toml            # Hugo 主配置
└── .github/             # GitHub Actions 配置
```

## AI 辅助运营

博客通过 Claude Code Skill 体系实现 AI 辅助运营：

| Skill | 功能 |
|-------|------|
| `blog-growth` | GSC + GA 数据诊断、中英文差异化选题、热搜追踪 |
| `blog-writer` | 深度文章写作（自动素材收集、SEO 优化、FAQ 生成） |
| `blog-cover-image` | AI 封面图生成（五维度风格系统） |
| `blog-illustrator` | 文章配图（自动识别需要配图的位置） |
| `blog-diagram` | 架构图/信息图（12 种布局 × 8 种风格） |
| `blog-distributor` | 自动分发到 dev.to、掘金、HN |

## 联系方式

- GitHub: [@heyuan110](https://github.com/heyuan110)
- X: [@heyuan110](https://x.com/heyuan110)

## License

内容版权归作者所有。
