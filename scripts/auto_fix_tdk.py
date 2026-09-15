import glob
import re
import os

LIMITS = {
    False: { # 英文
        "title": (40, 60),
        "desc": (120, 160)
    },
    True: { # 中文
        "title": (20, 40),
        "desc": (70, 110)
    }
}

def smart_trim_en_desc(desc: str, max_len: int = 150) -> str:
    if len(desc) <= 160: # 只要原长不超过160就允许（不截断），若超过则修剪至 max_len
        return desc
    trimmed = desc[:max_len]
    last_space = trimmed.rfind(' ')
    if last_space > max_len - 30: # 避免回溯太多
        trimmed = trimmed[:last_space]
    trimmed = trimmed.rstrip(".,;! ")
    return trimmed + "..."

def smart_trim_zh_desc(desc: str, max_len: int = 100) -> str:
    if len(desc) <= 110: # 只要原长不超过110就允许（不截断），若超过则修剪至 max_len
        return desc
    trimmed = desc[:max_len]
    trimmed = trimmed.rstrip("，。；！、,.;! ")
    return trimmed + "..."

def smart_trim_en_title(title: str, max_len: int = 58) -> str:
    if len(title) <= 60: # 不超 60 就保留
        return title
    # 精简：移除常见的冗余尾巴，如 " - A Complete Guide 2026"
    title = re.sub(r'\s*-\s*A\s+Complete\s+Guide\s+2026.*$', '', title, flags=re.I)
    title = re.sub(r'\s*:\s*A\s+Complete\s+Guide\s+2026.*$', '', title, flags=re.I)
    title = re.sub(r'\s*-\s*Complete\s+Guide.*$', '', title, flags=re.I)
    title = re.sub(r'\s*:\s*Complete\s+Guide.*$', '', title, flags=re.I)
    title = re.sub(r'\s*-\s*Guide.*$', '', title, flags=re.I)
    title = re.sub(r'\s*:\s*Guide.*$', '', title, flags=re.I)
    title = re.sub(r'\s*:\s*Tutorial.*$', '', title, flags=re.I)
    title = re.sub(r'\s*-\s*Tutorial.*$', '', title, flags=re.I)
    
    if len(title) <= 60:
        return title
        
    trimmed = title[:max_len]
    last_space = trimmed.rfind(' ')
    if last_space > max_len - 15:
        trimmed = trimmed[:last_space]
    return trimmed.rstrip(" -:")

def smart_trim_zh_title(title: str, max_len: int = 38) -> str:
    if len(title) <= 40: # 不超 40 就保留
        return title
    # 精简常见的冗余尾巴，如“：从入门到精通与生产实战指南”
    title = re.sub(r'：从入门到精通与生产.*$', '', title)
    title = re.sub(r'：从入门到精通.*$', '', title)
    title = re.sub(r'：从入门到实战.*$', '', title)
    title = re.sub(r'：安装配置与.*$', '', title)
    title = re.sub(r'：完整指南.*$', '', title)
    title = re.sub(r'：完全指南.*$', '', title)
    
    if len(title) <= 40:
        return title
        
    return title[:max_len].rstrip(" ：-")

def auto_fix_file(filepath: str) -> bool:
    raw = open(filepath, encoding="utf-8").read()
    if not raw.startswith("+++"):
        return False
        
    parts = raw.split("+++", 2)
    if len(parts) < 3:
        return False
        
    fm = parts[1]
    body = parts[2]
    
    is_zh = filepath.endswith("index.zh.md")
    limits = LIMITS[is_zh]
    
    # 提取 title
    t_match = re.search(r"^title\s*=\s*['\"](.*?)['\"]\s*$", fm, re.M)
    d_match = re.search(r"^description\s*=\s*['\"](.*?)['\"]\s*$", fm, re.M)
    
    if not t_match:
        return False
        
    title = t_match.group(1)
    desc = d_match.group(1) if d_match else ""
    
    changed = False
    
    # 校验 Title 是否超标
    if len(title) > limits["title"][1]:
        new_title = smart_trim_zh_title(title, 38) if is_zh else smart_trim_en_title(title, 58)
        if new_title != title:
            # 安全转义单双引号
            quote = t_match.group(0)[t_match.group(0).find("=")+1:].strip()[0]
            new_title_line = f"title = {quote}{new_title}{quote}"
            fm = fm.replace(t_match.group(0), new_title_line)
            changed = True
            print(f"  [Title] Trimmed: '{title}' -> '{new_title}' ({filepath})")
            
    # 校验 Description 是否超标
    if desc and len(desc) > limits["desc"][1]:
        new_desc = smart_trim_zh_desc(desc, 100) if is_zh else smart_trim_en_desc(desc, 150)
        if new_desc != desc:
            quote = d_match.group(0)[d_match.group(0).find("=")+1:].strip()[0]
            new_desc_line = f"description = {quote}{new_desc}{quote}"
            fm = fm.replace(d_match.group(0), new_desc_line)
            changed = True
            print(f"  [Desc] Trimmed: '{desc}' -> '{new_desc}' ({filepath})")
            
    if changed:
        # 回写文件
        new_raw = "+++" + fm + "+++" + body
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_raw)
        return True
        
    return False

def main():
    all_md_files = glob.glob("content/posts/*/*/*.md")
    fixed_count = 0
    for filepath in all_md_files:
        if "index" not in filepath:
            continue
        try:
            if auto_fix_file(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
            
    print(f"\nSuccessfully optimized TDK for {fixed_count} files!")

if __name__ == "__main__":
    main()
