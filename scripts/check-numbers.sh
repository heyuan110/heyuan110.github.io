#!/bin/bash
# 用法: numcheck.sh <file>  — 比对工作区版本与 git HEAD 版本的数字集合
f="$1"
diff <(git show HEAD:"$f" | grep -oE '[0-9][0-9,.]*' | sort -u) \
     <(grep -oE '[0-9][0-9,.]*' "$f" | sort -u) \
  && echo "✅ 数字集合一致" || echo "⚠️ 上面是差异(< 丢失 / > 新增)"
