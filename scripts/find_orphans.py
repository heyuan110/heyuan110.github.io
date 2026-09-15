import glob
import re
import os

def find_orphan_pages():
    all_md_files = glob.glob("content/posts/*/*/*.md")
    
    # 我们映射所有的文章：文件的 slug -> 路径和语言
    # 例如：/posts/ai/2025-01-23-claude-code-commands/
    # 或者 /zh/posts/ai/2025-01-23-claude-code-commands/
    
    pages = {}
    for f in all_md_files:
        if "index" not in f:
            continue
        parts = f.split('/')
        if len(parts) < 4:
            continue
        section = parts[2] # e.g. ai, linux, docker
        slug = parts[3]    # e.g. 2025-01-23-claude-code-commands
        is_zh = f.endswith("index.zh.md")
        
        path_en = f"/posts/{section}/{slug}/"
        path_zh = f"/zh/posts/{section}/{slug}/"
        
        if is_zh:
            pages[path_zh] = f
        else:
            pages[path_en] = f

    # 扫描每个文件，抓取里面指向其他文件的所有链接
    link_counts = {p: 0 for p in pages.keys()}
    
    link_pattern = re.compile(r'\[.*?\]\((/.*?)\)')
    
    for path, filepath in pages.items():
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            # 匹配所有形如 [xxx](/posts/...) 或 [xxx](/zh/posts/...) 的链接
            found_links = link_pattern.findall(content)
            for link in found_links:
                # 剔除尾斜杠的干扰，统一定义
                clean_link = link.split('#')[0].split('?')[0]
                if not clean_link.endswith('/'):
                    clean_link += '/'
                if clean_link in link_counts:
                    # 避免自我引用
                    if clean_link != path:
                        link_counts[clean_link] += 1

    # 找出所有 link_counts 为 0 的孤儿页
    orphans = [p for p, count in link_counts.items() if count == 0]
    
    print(f"Total pages: {len(pages)}")
    print(f"Total orphans found: {len(orphans)}")
    print("\n--- Orphan Pages List ---")
    for o in sorted(orphans):
        print(f"{o} -> {pages[o]}")

if __name__ == "__main__":
    find_orphan_pages()
