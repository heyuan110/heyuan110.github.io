+++
date = '{{ .Date }}'
draft = true
# SEO 标题建议：45-65 字，主关键词前置（A/B 规则见 docs/seo/title-description-playbook.md）
title = '{{ replace .File.ContentBaseName "-" " " | title }}'
# SEO 描述建议：120-160 字，覆盖核心意图与结果
# description = ''
# keywords = ['关键词1', '关键词2']
+++
