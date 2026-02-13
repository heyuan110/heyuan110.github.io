#!/usr/bin/env python3
"""
批量迁移工具页面到公共组件（common/common.css + common/common.js）
- 删除内联公共 CSS（bc-nav / lang-switcher / category-nav / footer / related / trust-bar / fade-in）
- 删除内联公共 HTML（bc-nav / category-nav / footer）
- 删除内联公共 JS（detectLanguage / applyTranslations / switchLanguage / lang-switcher 交互 / FAQ 手风琴）
- 注入 <link href="common/common.css"> 和 <script src="common/common.js">
- 添加 WebToolbox.init(translations) 调用
- 统一 localStorage 键名为 toolbox_lang
"""

import re
import os
import sys

TOOLBOX_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 排除首页和类目页（它们有自己的布局）
EXCLUDE = {
    'index.html', 'pdf-tools.html', 'image-tools.html',
    'developer-tools.html', 'text-tools.html', 'media-tools.html',
    'utility-tools.html'
}

# 工具 → 类目映射
CATEGORY_MAP = {
    'pdf':       ['pdf-merge', 'pdf-split', 'pdf-compress', 'pdf-to-image', 'image-to-pdf', 'pdf-protect', 'e-sign'],
    'image':     ['image-compressor', 'image-converter', 'image-editor', 'ico-maker', 'id-photo-tool', 'paint-board', 'color-palette', 'qr-code-generator', 'ocr-tool', 'bg-remover', 'watermark-tool'],
    'developer': ['json-viewer', 'sqlite-viewer', 'crypto-tools', 'websocket-tester', 'regex-tester', 'ip-lookup', 'whois-query', 'timestamp-converter', 'base64-tool', 'url-encoder', 'csv-json', 'cron-generator', 'api-tester', 'hex-viewer', 'code-formatter', 'yaml-editor'],
    'text':      ['markdown-editor', 'text-diff', 'word-counter', 'lorem-ipsum', 'chinese-converter'],
    'media':     ['m3u8-downloader', 'audio-cutter', 'screen-recorder', 'social-video-downloader', 'file-converter'],
    'utility':   ['calculator', 'unit-converter', 'password-generator', 'world-clock', 'pomodoro', 'page-refresher', 'file-renamer', 'relative-calculator', 'handheld-danmaku', 'metronome', 'invoice-generator', 'claude-history-viewer', 'angel-number', 'numerology']
}

# 反转映射
TOOL_TO_CAT = {}
for cat, tools in CATEGORY_MAP.items():
    for tool in tools:
        TOOL_TO_CAT[tool] = cat


def get_tool_files():
    """获取所有工具 HTML 文件"""
    files = []
    for f in sorted(os.listdir(TOOLBOX_DIR)):
        if f.endswith('.html') and f not in EXCLUDE:
            files.append(os.path.join(TOOLBOX_DIR, f))
    return files


def extract_tool_name(content, filename):
    """从面包屑 HTML 中提取工具显示名"""
    # 尝试从 bc-cur 中提取
    m = re.search(r'<span\s+class="bc-cur"[^>]*>(.*?)</span>', content)
    if m:
        return m.group(1).strip()
    # 退回到文件名
    name = filename.replace('.html', '').replace('-', ' ').title()
    return name


def inject_css_link(content):
    """在 <head> 中注入公共 CSS 引用"""
    if 'common/common.css' in content:
        return content, False

    # 在 </head> 前插入，或在最后一个 <link> 后插入
    marker = '</head>'
    idx = content.find(marker)
    if idx == -1:
        return content, False

    link_tag = '    <link rel="stylesheet" href="common/common.css">\n'
    content = content[:idx] + link_tag + content[idx:]
    return content, True


def remove_inline_bc_nav_css(content):
    """删除内联的 bc-nav 相关 CSS（通常是压缩后的一行 style 块）"""
    # 模式1：<style> 块中单独一行的压缩 bc-nav CSS
    # 例如 <style>.bc-nav{...}.bc-nav .bc-left{...}.bc-nav a{...}...bc-cur{...}
    content = re.sub(
        r'<style>\.bc-nav\{[^<]*?\.bc-cur\{[^}]*\}\s*\n?',
        '',
        content
    )

    # 模式2：也可能在 <style> 块内（非独立标签）
    content = re.sub(
        r'\.bc-nav\{[^}]*\}[^<]*?\.bc-nav \.bc-left\{[^}]*\}[^<]*?\.bc-nav a\{[^}]*\}[^<]*?\.bc-nav a:hover\{[^}]*\}[^<]*?\.bc-sep\{[^}]*\}[^<]*?\.bc-cur\{[^}]*\}\s*\n?',
        '',
        content
    )

    return content


def remove_inline_lang_switcher_css(content):
    """删除内联的语言切换器 CSS"""
    # 移除 .lang-switcher 及其所有子选择器
    patterns = [
        r'/\*\s*语言切换器.*?\*/\s*\n?',
        r'/\*\s*Language [Ss]witcher.*?\*/\s*\n?',
        r'\.lang-switcher\s*\{[^}]*\}\s*\n?',
        r'\.lang-dropdown\s*\{[^}]*\}\s*\n?',
        r'\.lang-current\s*\{[^}]*\}\s*\n?',
        r'\.lang-current:hover\s*\{[^}]*\}\s*\n?',
        r'\.lang-current::after\s*\{[^}]*\}\s*\n?',
        r'\.lang-dropdown\.open\s+\.lang-current::after\s*\{[^}]*\}\s*\n?',
        r'\.lang-menu\s*\{[^}]*\}\s*\n?',
        r'\.lang-dropdown\.open\s+\.lang-menu\s*\{[^}]*\}\s*\n?',
        r'\.lang-btn\s*\{[^}]*\}\s*\n?',
        r'\.lang-btn:hover\s*\{[^}]*\}\s*\n?',
        r'\.lang-btn\.active\s*\{[^}]*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)
    return content


def remove_inline_category_nav_css(content):
    """删除内联的类目导航 CSS"""
    patterns = [
        r'/\*\s*={0,3}\s*类目导航\s*={0,3}\s*\*/\s*\n?',
        r'\.category-nav\s*\{[^}]*\}\s*\n?',
        r'\.cat-nav-item\s*\{[^}]*\}\s*\n?',
        r'\.cat-nav-item:hover\s*\{[^}]*\}\s*\n?',
        r'\.cat-nav-item\.active\s*\{[^}]*\}\s*\n?',
        r'\[data-theme="light"\]\s*\.category-nav\s*\{[^}]*\}\s*\n?',
        r'\[data-theme="light"\]\s*\.cat-nav-item\s*\{[^}]*\}\s*\n?',
        r'\[data-theme="light"\]\s*\.cat-nav-item:hover\s*\{[^}]*\}\s*\n?',
        r'\[data-theme="light"\]\s*\.cat-nav-item\.active\s*\{[^}]*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)

    # 移除 @media 块中的 category-nav 规则
    content = re.sub(
        r'[ \t]*\.category-nav\s*\{[^}]*\}\s*\n?\s*\.cat-nav-item\s*\{[^}]*\}\s*\n?',
        '',
        content
    )

    return content


def remove_inline_footer_css(content):
    """删除内联的 footer CSS"""
    patterns = [
        r'/\*\s*页脚\s*\*/\s*\n?',
        r'/\*\s*Footer\s*\*/\s*\n?',
        r'\.footer\s*\{[^}]*\}\s*\n?',
        r'\.footer\s+a\s*\{[^}]*\}\s*\n?',
        r'\.footer\s+a:hover\s*\{[^}]*\}\s*\n?',
        r'\.footer\s+p\s*\{[^}]*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)
    return content


def remove_inline_related_css(content):
    """删除内联的相关工具 CSS"""
    patterns = [
        r'/\*\s*相关工具\s*\*/\s*\n?',
        r'\.related-tools\s*\{[^}]*\}\s*\n?',
        r'\.related-tools\s+h3\s*\{[^}]*\}\s*\n?',
        r'\.related-grid\s*\{[^}]*\}\s*\n?',
        r'\.related-card\s*\{[^}]*\}\s*\n?',
        r'\.related-card:hover\s*\{[^}]*\}\s*\n?',
        r'\.related-icon\s*\{[^}]*\}\s*\n?',
        r'\.related-name\s*\{[^}]*\}\s*\n?',
        r'\.related-desc\s*\{[^}]*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)
    return content


def remove_inline_trust_bar_css(content):
    """删除内联的 trust-bar CSS"""
    patterns = [
        r'\.trust-bar\s*\{[^}]*\}\s*\n?',
        r'\.trust-item\s*\{[^}]*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)
    return content


def remove_inline_fade_in_css(content):
    """删除内联的入场动画 CSS"""
    patterns = [
        r'/\*\s*入场动画\s*\*/\s*\n?',
        r'\.fade-in\s*\{[^}]*\}\s*\n?',
        r'\.fade-in-delay1\s*\{[^}]*\}\s*\n?',
        r'\.fade-in-delay2\s*\{[^}]*\}\s*\n?',
        r'\.fade-in-delay3\s*\{[^}]*\}\s*\n?',
        r'@keyframes\s+fadeInUp\s*\{[^}]*\{[^}]*\}[^}]*\{[^}]*\}\s*\}\s*\n?',
    ]
    for pat in patterns:
        content = re.sub(pat, '', content)
    return content


def remove_bc_nav_html(content):
    """删除 bc-nav HTML 块"""
    # 删除整个 <nav class="bc-nav"> 块
    content = re.sub(
        r'\s*<nav\s+class="bc-nav"[^>]*>[\s\S]*?</nav>\s*',
        '\n',
        content
    )
    return content


def remove_category_nav_html(content):
    """删除 category-nav HTML 块"""
    # 删除注释 + nav 块
    content = re.sub(
        r'\s*<!--\s*类目导航\s*-->\s*\n?\s*<nav\s+class="category-nav"[^>]*>[\s\S]*?</nav>\s*',
        '\n',
        content
    )
    # 无注释的
    content = re.sub(
        r'\s*<nav\s+class="category-nav"[^>]*>[\s\S]*?</nav>\s*',
        '\n',
        content
    )
    return content


def remove_footer_html(content):
    """删除 footer HTML 块（class="footer"）"""
    content = re.sub(
        r'\s*<footer\s+class="footer"[^>]*>[\s\S]*?</footer>\s*',
        '\n',
        content
    )
    return content


def remove_inline_lang_js(content):
    """删除内联的语言相关 JS 函数和交互代码"""
    # 删除 detectLanguage 函数定义
    content = re.sub(
        r'\s*function\s+detectLanguage\s*\(\)\s*\{[^}]*\}\s*\n?',
        '\n',
        content
    )

    # 删除 applyTranslations 函数定义（可能有多种变体名）
    for fn_name in ['applyTranslations', 'applyLanguage']:
        # 多行函数体：使用递归匹配花括号
        pattern = re.compile(
            r'\s*function\s+' + fn_name + r'\s*\([^)]*\)\s*\{',
            re.DOTALL
        )
        m = pattern.search(content)
        if m:
            start = m.start()
            # 找到匹配的右花括号
            brace_start = m.end() - 1
            end = find_matching_brace(content, brace_start)
            if end:
                content = content[:start] + '\n' + content[end + 1:]

    # 删除 switchLanguage 函数定义
    pattern = re.compile(r'\s*function\s+switchLanguage\s*\([^)]*\)\s*\{', re.DOTALL)
    m = pattern.search(content)
    if m:
        start = m.start()
        brace_start = m.end() - 1
        end = find_matching_brace(content, brace_start)
        if end:
            content = content[:start] + '\n' + content[end + 1:]

    # 删除 langNames 定义
    content = re.sub(
        r'\s*(?:const|var|let)\s+langNames\s*=\s*\{[^}]*\}\s*;?\s*\n?',
        '\n',
        content
    )

    # 删除 langDropdown/langCurrent 变量声明（只删除公共部分的声明）
    content = re.sub(
        r'\s*(?:const|var|let)\s+langDropdown\s*=\s*document\.getElementById\([\'"]langDropdown[\'"]\)\s*;?\s*\n?',
        '\n',
        content
    )
    content = re.sub(
        r'\s*(?:const|var|let)\s+langCurrent\s*=\s*document\.getElementById\([\'"]langCurrent[\'"]\)\s*;?\s*\n?',
        '\n',
        content
    )

    # 删除 langCurrent click 事件绑定
    content = re.sub(
        r'\s*(?:if\s*\(langCurrent\s*&&\s*langDropdown\)\s*\{)?\s*langCurrent\.addEventListener\([\'"]click[\'"]\s*,\s*(?:function\s*\([^)]*\)|[\w()\s=>]*)\s*\{[^}]*langDropdown\.classList\.toggle[^}]*\}\s*\)\s*;?\s*\}?\s*\n?',
        '\n',
        content
    )

    # 删除外部 click 关闭下拉菜单
    content = re.sub(
        r'\s*document\.addEventListener\([\'"]click[\'"]\s*,\s*(?:function\s*\(\)|[\w()\s=>]*)\s*\{\s*langDropdown\.classList\.remove[^}]*\}\s*\)\s*;?\s*\n?',
        '\n',
        content
    )

    # 删除 lang-btn 事件绑定
    content = re.sub(
        r"\s*document\.querySelectorAll\(['\"]\.lang-btn['\"]\)\.forEach\s*\(\s*(?:function\s*\(\s*btn\s*\)|[\w()\s=>]*)\s*\{[\s\S]*?switchLanguage\([\s\S]*?\}\s*\)\s*;?\s*\n?",
        '\n',
        content
    )
    content = re.sub(
        r"\s*document\.querySelectorAll\(['\"]\.lang-btn['\"]\)\.forEach\s*\(\s*(?:function\s*\(\s*btn\s*\)|[\w()\s=>]*)\s*\{[\s\S]*?applyLanguage\([\s\S]*?\}\s*\)\s*;?\s*\n?",
        '\n',
        content
    )

    # 删除初始 applyTranslations/applyLanguage 调用
    content = re.sub(
        r'\s*applyTranslations\(\s*currentLang\s*\)\s*;?\s*\n?',
        '\n',
        content
    )
    content = re.sub(
        r'\s*applyLanguage\(\s*currentLang\s*\)\s*;?\s*\n?',
        '\n',
        content
    )

    # 删除初始语言显示设置
    content = re.sub(
        r'\s*if\s*\(\s*langCurrent\s*\)\s*\{\s*langCurrent\.textContent\s*=\s*langNames\[.*?\]\s*;?\s*\}\s*\n?',
        '\n',
        content
    )

    # 删除 currentLang 变量声明（需要小心，有些页面可能还在用）
    # 只删除使用 detectLanguage 或旧键名的
    content = re.sub(
        r"\s*(?:let|var|const)\s+currentLang\s*=\s*localStorage\.getItem\(['\"][^'\"]*['\"\)]+\s*\|\|\s*(?:detectLanguage\(\)|'en')\s*;?\s*\n?",
        '\n',
        content
    )

    return content


def remove_faq_accordion_js(content):
    """删除 FAQ 手风琴 JS（由 common.js 统一处理）"""
    content = re.sub(
        r"\s*document\.querySelectorAll\(['\"]\.faq-question['\"]\)\.forEach\s*\(\s*(?:function\s*\(\s*btn\s*\)|[\w()\s=>]*)\s*\{[\s\S]*?classList\.(?:toggle|remove)\(['\"]active['\"]\)[\s\S]*?\}\s*\)\s*;?\s*\n?",
        '\n',
        content
    )
    return content


def find_matching_brace(content, pos):
    """找到与 pos 处的 { 匹配的 }"""
    if pos >= len(content) or content[pos] != '{':
        return None
    depth = 1
    i = pos + 1
    while i < len(content) and depth > 0:
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
        i += 1
    return i - 1 if depth == 0 else None


def replace_old_lang_key(content, tool_id):
    """替换旧的 localStorage 键名为 toolbox_lang"""
    # 各种旧键名模式
    old_keys = [
        tool_id.replace('-', '_') + '_lang',
        tool_id + '_lang',
        tool_id + '-lang',
        'preferred-lang',
        'preferredLanguage',
        'preferredLang',
    ]

    # 额外的特殊映射
    SPECIAL_KEYS = {
        'calculator': ['calc_lang'],
        'lorem-ipsum': ['lorem_lang'],
        'claude-history-viewer': ['claude-history-lang'],
        'qr-code-generator': ['qrgen_lang'],
        'url-encoder': ['urlenc_lang'],
        'base64-tool': ['base64_lang'],
        'social-video-downloader': ['svd_lang'],
    }
    old_keys.extend(SPECIAL_KEYS.get(tool_id, []))

    for key in old_keys:
        content = content.replace(f"'{key}'", "'toolbox_lang'")
        content = content.replace(f'"{key}"', '"toolbox_lang"')
    return content


def inject_common_js(content, tool_id, tool_name, category):
    """注入 common.js 引用和 WebToolbox.init 调用"""
    if 'common/common.js' in content:
        return content, False

    script_tag = (
        f'    <script src="common/common.js" '
        f'data-tool-id="{tool_id}" '
        f'data-tool-name="{tool_name}" '
        f'data-category="{category}"'
        f'></script>\n'
    )

    # 在第一个 <script>（非 JSON-LD、非 GA）前插入
    # 找到 </head> 前或 <body> 后的第一个非结构化数据 <script>
    # 策略：在 </body> 前插入
    body_close = content.rfind('</body>')
    if body_close == -1:
        return content, False

    # 找到最后一个 </script> 标签前
    last_script_close = content.rfind('</script>', 0, body_close)
    if last_script_close == -1:
        return content, False

    # 在最后一个 </script> 之后插入
    insert_pos = last_script_close + len('</script>')

    # 检查是否已有 WebToolbox.init
    if 'WebToolbox.init' in content:
        # 只注入 script 标签
        content = content[:insert_pos] + '\n' + script_tag + content[insert_pos:]
        return content, True

    # 查找 translations 对象是否存在
    has_translations = 'translations' in content and (
        re.search(r'(?:const|var|let)\s+translations\s*=', content) is not None
    )

    if has_translations:
        init_call = '    <script>WebToolbox.init(translations);</script>\n'
    else:
        # 有些页面的翻译对象叫 i18n
        has_i18n = re.search(r'(?:const|var|let)\s+i18n\s*=', content) is not None
        if has_i18n:
            init_call = '    <script>WebToolbox.init(i18n);</script>\n'
        else:
            init_call = '    <script>WebToolbox.init({});</script>\n'

    content = content[:insert_pos] + '\n' + script_tag + init_call + content[insert_pos:]
    return content, True


def remove_old_lang_switcher_html(content):
    """删除旧的独立 lang-switcher HTML（不在 bc-nav 内的）"""
    # 删除 top-bar 中的 lang-dropdown
    content = re.sub(
        r'\s*<div\s+class="top-bar"[^>]*>\s*\n?\s*<div\s+class="lang-dropdown"[^>]*>[\s\S]*?</div>\s*\n?\s*</div>\s*\n?\s*</div>\s*',
        '\n',
        content
    )
    return content


def clean_residual_js(content):
    """清理被删除函数后残留的注释、空行、孤立花括号"""
    # 删除只包含注释的行（JS 单行注释 //）
    # 只删除连续的纯注释块（不紧跟代码的）
    content = re.sub(
        r'(\n\s*//[^\n]*){2,}(?=\s*\n\s*(?://|}\s*$|\n))',
        '',
        content
    )

    # 删除孤立的闭花括号（前面是空行或注释，不是代码）
    content = re.sub(r'\n\s*//[^\n]*\n\s*\}\s*\n', '\n', content)
    content = re.sub(r'\n\s*//[^\n]*\n\s*\}\s*\)\s*;?\s*\n', '\n', content)

    # 删除连续的空注释行
    content = re.sub(r'(\s*//[^\n]*\n){2,}', '\n', content)

    # 删除孤立的 }); 行（IIFE 中被掏空后的残留）
    # 但要小心不要删除正常的 });
    # 只删除前后都是空行的孤立 });
    content = re.sub(r'\n\n\s*\}\);\s*\n\n', '\n\n', content)

    return content


def clean_empty_style(content):
    """清理空的 <style> 标签和多余空行"""
    # 删除空的 <style></style>
    content = re.sub(r'<style>\s*</style>\s*', '', content)
    # 减少连续空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    return content


def process_file(filepath, dry_run=False):
    """处理单个文件"""
    filename = os.path.basename(filepath)
    tool_id = filename.replace('.html', '')

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changes = []

    # 确定类目
    category = TOOL_TO_CAT.get(tool_id, 'utility')

    # 提取工具名
    tool_name = extract_tool_name(content, filename)

    # 1. 注入公共 CSS
    content, changed = inject_css_link(content)
    if changed:
        changes.append('CSS link')

    # 2. 删除内联公共 CSS
    before = content
    content = remove_inline_bc_nav_css(content)
    content = remove_inline_lang_switcher_css(content)
    content = remove_inline_category_nav_css(content)
    content = remove_inline_footer_css(content)
    content = remove_inline_related_css(content)
    content = remove_inline_trust_bar_css(content)
    content = remove_inline_fade_in_css(content)
    if content != before:
        changes.append('inline CSS')

    # 3. 删除内联公共 HTML
    before = content
    content = remove_bc_nav_html(content)
    content = remove_category_nav_html(content)
    content = remove_footer_html(content)
    content = remove_old_lang_switcher_html(content)
    if content != before:
        changes.append('inline HTML')

    # 4. 删除内联公共 JS
    before = content
    content = remove_inline_lang_js(content)
    content = remove_faq_accordion_js(content)
    if content != before:
        changes.append('inline JS')

    # 5. 替换旧 localStorage 键名
    before = content
    content = replace_old_lang_key(content, tool_id)
    if content != before:
        changes.append('lang key')

    # 6. 注入 common.js 引用 + WebToolbox.init
    content, changed = inject_common_js(content, tool_id, tool_name, category)
    if changed:
        changes.append('common.js')

    # 7. 清理
    content = clean_residual_js(content)
    content = clean_empty_style(content)

    if content != original:
        if not dry_run:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        return filename, f"✅ {', '.join(changes)}"
    return filename, '⏭️ 无需修改'


def main():
    dry_run = '--dry-run' in sys.argv
    single = None
    for arg in sys.argv[1:]:
        if arg.endswith('.html'):
            single = arg
            break

    if single:
        # 处理单个文件
        filepath = os.path.join(TOOLBOX_DIR, single) if not os.path.isabs(single) else single
        if not os.path.exists(filepath):
            print(f"文件不存在: {filepath}")
            sys.exit(1)
        print(f"处理单个文件: {os.path.basename(filepath)}")
        if dry_run:
            print("(干运行模式，不写入文件)")
        filename, status = process_file(filepath, dry_run)
        print(f"  {status}")
        return

    files = get_tool_files()
    print(f"=== 迁移到公共组件 ===")
    if dry_run:
        print("(干运行模式，不写入文件)")
    print(f"找到 {len(files)} 个工具页面\n")

    migrated = 0
    skipped = 0
    errors = 0

    for filepath in files:
        try:
            filename, status = process_file(filepath, dry_run)
            print(f"  {status} - {filename}")
            if '✅' in status:
                migrated += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ❌ {os.path.basename(filepath)}: {e}")
            errors += 1

    print(f"\n=== 完成 ===")
    print(f"已迁移: {migrated}, 跳过: {skipped}, 错误: {errors}")


if __name__ == '__main__':
    main()
