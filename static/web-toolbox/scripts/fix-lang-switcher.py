#!/usr/bin/env python3
"""将 lang-switcher 移入 bc-nav（面包屑左 + 语言切换器右，同行 flex 布局）"""

import re
import os

TOOLBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 排除首页、类目页、已完成的参考页
EXCLUDE = {
    'index.html', 'pdf-tools.html', 'image-tools.html',
    'developer-tools.html', 'text-tools.html', 'media-tools.html',
    'utility-tools.html', 'social-video-downloader.html'
}

# 标准的 lang-switcher HTML（用于插入 bc-nav）
LANG_SWITCHER_HTML = '''<div class="lang-switcher" id="langSwitcher">
        <div class="lang-dropdown" id="langDropdown">
            <div class="lang-current" id="langCurrent">🌐 English</div>
            <div class="lang-menu">
                <button class="lang-btn" data-lang="en">🇺🇸 English</button>
                <button class="lang-btn" data-lang="zh-CN">🇨🇳 中文</button>
                <button class="lang-btn" data-lang="fr">🇫🇷 Français</button>
                <button class="lang-btn" data-lang="es">🇪🇸 Español</button>
            </div>
        </div>
    </div>'''


def find_lang_switcher(content):
    """找到 lang-switcher 完整的 HTML 块（通过计数 div 标签）"""
    # 匹配 lang-switcher 开始标签
    start_match = re.search(
        r'<div\s+class="lang-switcher"[^>]*>',
        content
    )
    if not start_match:
        return None, None, None

    start_pos = start_match.start()
    pos = start_match.end()
    depth = 1  # 已经进入了一层 div

    while depth > 0 and pos < len(content):
        # 找下一个 <div 或 </div>
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)

        if next_close == -1:
            break

        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            if depth == 0:
                end_pos = next_close + len('</div>')
                return start_pos, end_pos, content[start_pos:end_pos]
            pos = next_close + 6

    return None, None, None


def find_surrounding_context(content, start_pos, end_pos):
    """检查 lang-switcher 周围是否有需要一起移除的包裹元素"""
    # 检查前面是否有注释 "<!-- 语言切换器 -->" 等
    before = content[:start_pos]
    comment_match = re.search(r'([ \t]*<!-- ?语言切换[器者].*?-->\s*)$', before)
    if comment_match:
        start_pos = comment_match.start()

    # 检查是否被 <nav class="top-nav"> 包裹且只包含 lang-switcher
    # 向前找 <nav class="top-nav">
    before_trimmed = content[:start_pos].rstrip()
    top_nav_match = re.search(r'([ \t]*<!-- ?顶部导航.*?-->\s*)?<nav\s+class="top-nav"[^>]*>\s*$', before_trimmed)
    if top_nav_match:
        # 向后找 </nav>
        after = content[end_pos:]
        nav_close_match = re.match(r'\s*</nav>', after)
        if nav_close_match:
            start_pos = top_nav_match.start()
            end_pos = end_pos + nav_close_match.end()

    return start_pos, end_pos


def process_file(filepath):
    """处理单个文件：将 lang-switcher 移入 bc-nav"""
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. 检查 bc-nav 是否已有 bc-left（说明已处理）
    bc_nav_match = re.search(
        r'(<nav\s+class="bc-nav"[^>]*>)(.*?)(</nav>)',
        content, re.DOTALL
    )
    if not bc_nav_match:
        return filename, '无 bc-nav'

    if '<div class="bc-left">' in bc_nav_match.group():
        return filename, '已处理（有 bc-left）'

    # 2. 找到 lang-switcher
    start_pos, end_pos, lang_html = find_lang_switcher(content)
    if not lang_html:
        return filename, '无 lang-switcher'

    # 3. 检查 lang-switcher 是否已在 bc-nav 内
    bc_start = bc_nav_match.start()
    bc_end = bc_nav_match.end()
    if bc_start <= start_pos <= bc_end:
        return filename, 'lang-switcher 已在 bc-nav 内'

    # 4. 扩展移除范围（包含注释和 top-nav 包裹）
    remove_start, remove_end = find_surrounding_context(content, start_pos, end_pos)

    # 5. 从原位置删除 lang-switcher
    content = content[:remove_start] + content[remove_end:]

    # 6. 清理可能留下的多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 7. 重新查找 bc-nav（位置可能已变化）
    bc_nav_match = re.search(
        r'(<nav\s+class="bc-nav"[^>]*>)(.*?)(</nav>)',
        content, re.DOTALL
    )
    if not bc_nav_match:
        return filename, '错误：删除后找不到 bc-nav'

    # 8. 构建新的 bc-nav：<bc-left>面包屑</bc-left> + lang-switcher
    bc_inner = bc_nav_match.group(2).strip()
    new_bc_nav = (
        f'{bc_nav_match.group(1)}\n'
        f'    <div class="bc-left">{bc_inner}</div>\n'
        f'    {LANG_SWITCHER_HTML}\n'
        f'{bc_nav_match.group(3)}'
    )
    content = content.replace(bc_nav_match.group(), new_bc_nav, 1)

    # 9. 确保 lang-switcher CSS 是 relative（不是 absolute/fixed）
    content = re.sub(
        r'(\.lang-switcher\s*\{[^}]*?)position:\s*(absolute|fixed)\s*;[^}]*?(top:\s*\d+px\s*;\s*)?(right:\s*\d+px\s*;\s*)?(z-index:\s*\d+\s*;)?',
        lambda m: re.sub(
            r'position:\s*(absolute|fixed)\s*;\s*(top:\s*\d+px\s*;\s*)?(right:\s*\d+px\s*;\s*)?(z-index:\s*\d+\s*;)?',
            'position: relative; flex-shrink: 0;',
            m.group()
        ),
        content, count=1
    )

    # 10. 移除 inline style 中的 position absolute（如 calculator 等）
    # 针对 HTML 中 lang-switcher 上已有 inline style 的情况（已在步骤 5 中删除，新插入的没有 inline style）
    # 不需要额外处理

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename, '✅ 已迁移'
    return filename, '无需修改'


def main():
    files = []
    for f in os.listdir(TOOLBOX_DIR):
        if f.endswith('.html') and f not in EXCLUDE:
            files.append(os.path.join(TOOLBOX_DIR, f))
    files.sort()

    print(f"检查 {len(files)} 个工具页面\n")

    migrated = 0
    already_done = 0
    skipped = 0

    for filepath in files:
        try:
            filename, status = process_file(filepath)
            if '✅' in status:
                print(f"  ✅ {filename}: {status}")
                migrated += 1
            elif '已处理' in status:
                print(f"  ⏭️  {filename}: {status}")
                already_done += 1
            else:
                print(f"  ⚠️  {filename}: {status}")
                skipped += 1
        except Exception as e:
            print(f"  ❌ {os.path.basename(filepath)}: {e}")
            skipped += 1

    print(f"\n=== 完成 ===")
    print(f"已迁移: {migrated}, 已处理: {already_done}, 跳过/异常: {skipped}")


if __name__ == '__main__':
    main()
