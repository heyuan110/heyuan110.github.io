#!/usr/bin/env python3
"""批量重构工具页面布局 - 以 social-video-downloader.html 为参考标准"""

import re
import os
import sys

TOOLBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 排除首页、类目页、已完成页
EXCLUDE = {
    'index.html', 'pdf-tools.html', 'image-tools.html',
    'developer-tools.html', 'text-tools.html', 'media-tools.html',
    'utility-tools.html', 'social-video-downloader.html'
}

def get_tool_files():
    """获取所有需要处理的工具文件"""
    files = []
    for f in os.listdir(TOOLBOX_DIR):
        if f.endswith('.html') and f not in EXCLUDE:
            files.append(os.path.join(TOOLBOX_DIR, f))
    return sorted(files)


def refactor_file(filepath):
    """对单个文件执行所有重构操作"""
    filename = os.path.basename(filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # === 1. bc-nav CSS: max-width → 1200px, padding → 40px, 加 flex 布局 ===
    old_bc = re.search(
        r'\.bc-nav\{[^}]*\}',
        content
    )
    if old_bc:
        old_css = old_bc.group()
        # 替换 max-width
        new_css = re.sub(r'max-width:\s*\d+px', 'max-width:1200px', old_css)
        # 替换 padding
        new_css = re.sub(r'padding:\s*12px\s+\d+px\s+0', 'padding:12px 40px 0', new_css)
        # 加 flex 布局（如果还没有）
        if 'display:flex' not in new_css and 'display: flex' not in new_css:
            new_css = new_css.rstrip('}') + 'display:flex;align-items:center;justify-content:space-between;}'
        # 加 .bc-left 样式（如果还没有）
        if '.bc-left' not in content:
            new_css += '.bc-nav .bc-left{display:flex;align-items:center;flex-wrap:wrap;}'
        content = content.replace(old_css, new_css)
        changes.append('bc-nav CSS')

    # === 2. container max-width → 1200px, padding → 40px ===
    content, n = re.subn(
        r'(\.container\s*\{[^}]*?)max-width:\s*\d+px',
        r'\g<1>max-width: 1200px',
        content, count=1
    )
    if n:
        # 也更新 padding（如果是 Xpx 20px 格式）
        content = re.sub(
            r'(\.container\s*\{[^}]*?)padding:\s*\d+px\s+\d+px\s*;',
            r'\g<1>padding: 40px 40px;',
            content, count=1
        )
        changes.append('container width')

    # === 3. lang-switcher CSS: position → relative ===
    content, n = re.subn(
        r'(\.lang-switcher\s*\{[^}]*?)position:\s*(absolute|fixed)\s*;[^}]*?(top:\s*\d+px\s*;\s*)?[^}]*?(right:\s*\d+px\s*;\s*)?',
        lambda m: re.sub(
            r'position:\s*(absolute|fixed)\s*;\s*(top:\s*\d+px\s*;\s*)?(right:\s*\d+px\s*;\s*)?(z-index:\s*\d+\s*;\s*)?',
            'position: relative; flex-shrink: 0;',
            m.group()
        ),
        content, count=1
    )
    if n:
        changes.append('lang-switcher CSS')

    # === 4. 面包屑 HTML: 包裹 .bc-left + 移入 lang-switcher ===
    # 查找当前 bc-nav 结构
    bc_nav_match = re.search(
        r'(<nav\s+class="bc-nav"[^>]*>)(.*?)(</nav>)',
        content, re.DOTALL
    )
    if bc_nav_match and '.bc-left' not in bc_nav_match.group():
        bc_inner = bc_nav_match.group(2).strip()
        # 提取 lang-switcher HTML（从 header 或其他位置）
        lang_switcher_match = re.search(
            r'([ \t]*<!-- 语言切换器.*?-->\s*)?<div\s+class="lang-switcher"\s+id="langSwitcher">\s*'
            r'<div\s+class="lang-dropdown"\s+id="langDropdown">\s*'
            r'<div\s+class="lang-current"[^>]*>.*?</div>\s*'
            r'<div\s+class="lang-menu">.*?</div>\s*'
            r'</div>\s*</div>',
            content, re.DOTALL
        )

        if lang_switcher_match:
            lang_html = lang_switcher_match.group()
            # 从原位置删除 lang-switcher
            content = content.replace(lang_html, '')

            # 清理 lang-switcher HTML（去除多余缩进和注释）
            clean_lang = re.search(
                r'<div\s+class="lang-switcher".*?</div>\s*</div>\s*</div>',
                lang_html, re.DOTALL
            )
            if clean_lang:
                lang_block = clean_lang.group()
            else:
                lang_block = lang_html.strip()

            # 重新构建 bc-nav
            # 重新查找 bc-nav（内容可能已变化）
            bc_nav_match2 = re.search(
                r'(<nav\s+class="bc-nav"[^>]*>)(.*?)(</nav>)',
                content, re.DOTALL
            )
            if bc_nav_match2:
                bc_inner2 = bc_nav_match2.group(2).strip()
                new_bc_nav = (
                    f'{bc_nav_match2.group(1)}\n'
                    f'    <div class="bc-left">{bc_inner2}</div>\n'
                    f'    {lang_block}\n'
                    f'{bc_nav_match2.group(3)}'
                )
                content = content.replace(bc_nav_match2.group(), new_bc_nav)
                changes.append('lang-switcher → bc-nav')

    # === 5. category-nav: 从顶部移到 footer 前 ===
    cat_nav_match = re.search(
        r'(\s*<!-- 类目导航 -->\s*)?<nav\s+class="category-nav">\s*'
        r'(.*?)</nav>',
        content, re.DOTALL
    )
    if cat_nav_match:
        cat_html = cat_nav_match.group()
        cat_pos = cat_nav_match.start()

        # 查找 footer 位置
        footer_match = re.search(
            r'(\s*)<footer\s+class="footer"',
            content
        )

        if footer_match:
            footer_pos = footer_match.start()
            # 只有当 category-nav 在 footer 之前很远时才移动（说明在顶部）
            # 如果已经紧挨 footer 则不移动
            between = content[cat_pos:footer_pos]
            if len(between) > 500:  # 在顶部，需要移动
                # 从原位置删除
                content = content.replace(cat_html, '', 1)
                # 在 footer 前插入
                footer_match2 = re.search(
                    r'(\s*)<footer\s+class="footer"',
                    content
                )
                if footer_match2:
                    indent = '        '
                    clean_cat = cat_html.strip()
                    # 标准化缩进
                    clean_cat = re.sub(r'\n\s+', f'\n{indent}    ', clean_cat)
                    insert_text = f'\n{indent}{clean_cat}\n\n'
                    pos = footer_match2.start()
                    content = content[:pos] + insert_text + content[pos:]
                    changes.append('category-nav → bottom')

    # === 6. footer 简化为版权信息 ===
    footer_block = re.search(
        r'<footer\s+class="footer"[^>]*>.*?</footer>',
        content, re.DOTALL
    )
    if footer_block:
        old_footer = footer_block.group()
        # 检查是否已经是简化版
        if 'All rights reserved' not in old_footer:
            new_footer = (
                '<footer class="footer">\n'
                '            <p>&copy; 2024-2026 <a href="https://github.com/heyuan110" '
                'target="_blank" rel="noopener">heyuan110</a>. All rights reserved.</p>\n'
                '        </footer>'
            )
            content = content.replace(old_footer, new_footer, 1)
            changes.append('footer → copyright')

    # 也处理容器外的重复 footer（inline style 版本）
    extra_footer = re.search(
        r'\n\s*<footer\s+style="[^"]*"[^>]*>.*?</footer>',
        content, re.DOTALL
    )
    if extra_footer:
        content = content.replace(extra_footer.group(), '')
        changes.append('remove extra footer')

    # 也处理容器外的重复 related-tools（inline style 版本）
    extra_related = re.search(
        r'\n\s*<!-- 相关工具推荐 -->\s*<section\s+class="related-tools"\s+style="[^"]*">.*?</section>',
        content, re.DOTALL
    )
    if extra_related:
        content = content.replace(extra_related.group(), '')
        changes.append('remove extra related-tools')

    # === 7. 补全 hreflang ===
    if 'hreflang="x-default"' not in content:
        # 找到最后一个 hreflang 标签
        last_hreflang = None
        for m in re.finditer(r'<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="([^"]+)">', content):
            last_hreflang = m

        if last_hreflang:
            base_url = last_hreflang.group(1)
            insert_after = last_hreflang.group()
            new_tags = insert_after

            if 'hreflang="fr"' not in content:
                new_tags += f'\n    <link rel="alternate" hreflang="fr" href="{base_url}">'
            if 'hreflang="es"' not in content:
                new_tags += f'\n    <link rel="alternate" hreflang="es" href="{base_url}">'
            new_tags += f'\n    <link rel="alternate" hreflang="x-default" href="{base_url}">'

            content = content.replace(insert_after, new_tags, 1)
            changes.append('hreflang')

    # === 8. 添加入场动画 CSS（如果缺失） ===
    if '.fade-in' not in content and '@keyframes fadeInUp' not in content:
        # 在 </style> 前添加
        anim_css = """
        /* 入场动画 */
        .fade-in { opacity: 0; transform: translateY(20px); animation: fadeInUp 0.6s ease forwards; }
        .fade-in-delay1 { animation-delay: 0.15s; }
        .fade-in-delay2 { animation-delay: 0.3s; }
        .fade-in-delay3 { animation-delay: 0.45s; }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
    """
        # 找到最后一个 </style>
        last_style = content.rfind('</style>')
        if last_style != -1:
            content = content[:last_style] + anim_css + content[last_style:]
            changes.append('animation CSS')

    # 保存
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename, changes
    return filename, []


def main():
    files = get_tool_files()
    print(f"共 {len(files)} 个工具页面需要处理\n")

    success = 0
    skipped = 0
    errors = []

    for filepath in files:
        try:
            filename, changes = refactor_file(filepath)
            if changes:
                print(f"✅ {filename}: {', '.join(changes)}")
                success += 1
            else:
                print(f"⏭️  {filename}: 无需修改")
                skipped += 1
        except Exception as e:
            print(f"❌ {os.path.basename(filepath)}: {e}")
            errors.append((os.path.basename(filepath), str(e)))

    print(f"\n=== 完成 ===")
    print(f"已修改: {success}, 跳过: {skipped}, 错误: {len(errors)}")
    if errors:
        print("\n错误列表:")
        for name, err in errors:
            print(f"  {name}: {err}")


if __name__ == '__main__':
    main()
