/**
 * Web Toolbox - 公共组件
 * 自动注入 header（面包屑 + 语言切换器）和 footer（类目导航 + 版权）
 * 提供 i18n 基础设施
 *
 * 用法：
 * <script src="common/common.js"
 *   data-tool-id="image-converter"
 *   data-tool-name="Image Converter"
 *   data-category="image"
 * ></script>
 * <script>
 *   WebToolbox.init(translations);
 * </script>
 */
(function () {
    'use strict';

    // 统一 localStorage 键名
    var LANG_KEY = 'toolbox_lang';

    // 类目配置
    var CATEGORIES = [
        { key: 'home',      emoji: '🏠', label: 'Magic ToolBox', href: 'index.html' },
        { key: 'pdf',       emoji: '📄', label: 'PDF',           href: 'pdf-tools.html' },
        { key: 'image',     emoji: '🖼️', label: 'Image',         href: 'image-tools.html' },
        { key: 'developer', emoji: '💻', label: 'Dev',           href: 'developer-tools.html' },
        { key: 'text',      emoji: '📝', label: 'Text',          href: 'text-tools.html' },
        { key: 'media',     emoji: '🎬', label: 'Media',         href: 'media-tools.html' },
        { key: 'utility',   emoji: '⚡', label: 'Utility',       href: 'utility-tools.html' }
    ];

    // 类目 → 面包屑显示名 & 链接
    var CATEGORY_BREADCRUMB = {
        pdf:       { name: 'PDF Tools',       href: 'pdf-tools.html' },
        image:     { name: 'Image Tools',     href: 'image-tools.html' },
        developer: { name: 'Developer Tools', href: 'developer-tools.html' },
        text:      { name: 'Text Tools',      href: 'text-tools.html' },
        media:     { name: 'Media Tools',     href: 'media-tools.html' },
        utility:   { name: 'Utility Tools',   href: 'utility-tools.html' }
    };

    // 语言显示名称
    var LANG_NAMES = {
        'en':    '🇺🇸 English',
        'zh-CN': '🇨🇳 中文',
        'fr':    '🇫🇷 Français',
        'es':    '🇪🇸 Español'
    };

    // 读取 <script> 标签上的 data-* 属性
    function getConfig() {
        var scripts = document.querySelectorAll('script[src*="common.js"]');
        var script = scripts[scripts.length - 1]; // 取最后一个匹配
        if (!script) return {};
        return {
            toolId:   script.getAttribute('data-tool-id')   || '',
            toolName: script.getAttribute('data-tool-name') || '',
            category: script.getAttribute('data-category')  || 'utility'
        };
    }

    // 检测浏览器语言
    function detectLanguage() {
        var browserLang = navigator.language || navigator.userLanguage || 'en';
        if (browserLang.startsWith('zh')) return 'zh-CN';
        if (browserLang.startsWith('fr')) return 'fr';
        if (browserLang.startsWith('es')) return 'es';
        return 'en';
    }

    // 兼容旧键名：自动迁移到统一键名
    function migrateOldLangKey(toolId) {
        if (localStorage.getItem(LANG_KEY)) return;
        // 尝试读取旧键名
        var oldKeys = [
            toolId + '_lang',
            toolId.replace(/-/g, '_') + '_lang',
            'svd_lang', 'pdf_merge_lang', 'json_viewer_lang'
        ];
        for (var i = 0; i < oldKeys.length; i++) {
            var val = localStorage.getItem(oldKeys[i]);
            if (val) {
                localStorage.setItem(LANG_KEY, val);
                return;
            }
        }
    }

    // 获取当前语言
    function getCurrentLang() {
        return localStorage.getItem(LANG_KEY) || detectLanguage();
    }

    // 生成面包屑 + 语言切换器 HTML
    function buildHeader(config) {
        var cat = CATEGORY_BREADCRUMB[config.category];
        var catPart = cat
            ? '<a href="' + cat.href + '">' + cat.name + '</a><span class="bc-sep">›</span>'
            : '';

        return '<nav class="bc-nav" aria-label="Breadcrumb">' +
            '<div class="bc-left">' +
                '<a href="/">Home</a><span class="bc-sep">›</span>' +
                '<a href="index.html">Web Toolbox</a><span class="bc-sep">›</span>' +
                catPart +
                '<span class="bc-cur">' + config.toolName + '</span>' +
            '</div>' +
            '<div class="lang-switcher">' +
                '<div class="lang-dropdown" id="langDropdown">' +
                    '<div class="lang-current" id="langCurrent">🌐 English</div>' +
                    '<div class="lang-menu">' +
                        '<button class="lang-btn" data-lang="en">🇺🇸 English</button>' +
                        '<button class="lang-btn" data-lang="zh-CN">🇨🇳 中文</button>' +
                        '<button class="lang-btn" data-lang="fr">🇫🇷 Français</button>' +
                        '<button class="lang-btn" data-lang="es">🇪🇸 Español</button>' +
                    '</div>' +
                '</div>' +
            '</div>' +
        '</nav>';
    }

    // 生成类目导航 HTML
    function buildCategoryNav(activeCategory) {
        var items = CATEGORIES.map(function (c) {
            var cls = c.key === activeCategory ? ' active' : '';
            return '<a href="' + c.href + '" class="cat-nav-item' + cls + '">' + c.emoji + ' ' + c.label + '</a>';
        }).join('\n        ');
        return '<nav class="category-nav">\n        ' + items + '\n    </nav>';
    }

    // 生成 footer HTML
    function buildFooter(activeCategory) {
        return buildCategoryNav(activeCategory) +
            '\n    <footer class="site-footer">' +
            '<p>© 2024-2026 <a href="https://github.com/heyuan110" target="_blank" rel="noopener">heyuan110</a>. All rights reserved.</p>' +
            '</footer>';
    }

    // 注入 header（在 <body> 开始处）
    function injectHeader(config) {
        // 已有 bc-nav 则不注入
        if (document.querySelector('.bc-nav')) return;
        var html = buildHeader(config);
        document.body.insertAdjacentHTML('afterbegin', html);
    }

    // 注入 footer（在 .container 末尾或 </body> 前）
    function injectFooter(config) {
        // 已有 category-nav 则不注入
        if (document.querySelector('.category-nav')) return;
        var container = document.querySelector('.container');
        var footerHtml = buildFooter(config.category);
        if (container) {
            container.insertAdjacentHTML('beforeend', footerHtml);
        } else {
            document.body.insertAdjacentHTML('beforeend', footerHtml);
        }
    }

    // 绑定语言切换器交互
    function bindLangSwitcher(translations) {
        var dropdown = document.getElementById('langDropdown');
        var current = document.getElementById('langCurrent');
        if (!dropdown || !current) return;

        current.addEventListener('click', function (e) {
            e.stopPropagation();
            dropdown.classList.toggle('open');
        });

        document.addEventListener('click', function () {
            dropdown.classList.remove('open');
        });

        document.querySelectorAll('.lang-btn').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                switchLanguage(btn.getAttribute('data-lang'), translations);
            });
        });
    }

    // 应用翻译
    function applyTranslations(lang, translations) {
        var t = translations[lang] || translations['en'];
        if (!t) return;

        // 更新 <html lang>
        document.documentElement.lang = lang;

        // data-i18n
        document.querySelectorAll('[data-i18n]').forEach(function (el) {
            var key = el.getAttribute('data-i18n');
            if (t[key] !== undefined) {
                el.innerHTML = t[key];
            }
        });

        // data-i18n-placeholder
        document.querySelectorAll('[data-i18n-placeholder]').forEach(function (el) {
            var key = el.getAttribute('data-i18n-placeholder');
            if (t[key] !== undefined) {
                el.placeholder = t[key];
            }
        });
    }

    // 切换语言
    function switchLanguage(lang, translations) {
        localStorage.setItem(LANG_KEY, lang);
        applyTranslations(lang, translations);

        // 更新显示
        var current = document.getElementById('langCurrent');
        if (current) {
            current.textContent = LANG_NAMES[lang] || LANG_NAMES['en'];
        }

        // 关闭菜单
        var dropdown = document.getElementById('langDropdown');
        if (dropdown) dropdown.classList.remove('open');

        // 更新 active 状态
        document.querySelectorAll('.lang-btn').forEach(function (btn) {
            btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
        });
    }

    // 绑定 FAQ 手风琴
    function bindFaqAccordion() {
        document.querySelectorAll('.faq-question').forEach(function (btn) {
            // 避免重复绑定
            if (btn._faqBound) return;
            btn._faqBound = true;
            btn.addEventListener('click', function () {
                var item = btn.parentElement;
                var isOpen = item.classList.contains('active');
                document.querySelectorAll('.faq-item').forEach(function (it) {
                    it.classList.remove('active');
                });
                if (!isOpen) item.classList.add('active');
            });
        });
    }

    // 公开 API
    window.WebToolbox = {
        LANG_KEY: LANG_KEY,

        getCurrentLang: getCurrentLang,

        applyTranslations: applyTranslations,

        switchLanguage: switchLanguage,

        /**
         * 初始化：注入 DOM + 绑定事件 + 首次翻译
         * @param {Object} translations - 翻译字典 { en: {...}, 'zh-CN': {...}, ... }
         */
        init: function (translations) {
            var config = getConfig();

            // 兼容旧键名
            migrateOldLangKey(config.toolId);

            // 注入 header & footer
            injectHeader(config);
            injectFooter(config);

            // 绑定语言切换器
            bindLangSwitcher(translations || {});

            // 绑定 FAQ 手风琴
            bindFaqAccordion();

            // 首次翻译
            var lang = getCurrentLang();
            if (translations) {
                applyTranslations(lang, translations);
            }

            // 设置语言切换器初始显示
            var current = document.getElementById('langCurrent');
            if (current) {
                current.textContent = LANG_NAMES[lang] || LANG_NAMES['en'];
            }

            // 设置 active 按钮
            document.querySelectorAll('.lang-btn').forEach(function (btn) {
                btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
            });

            return lang;
        }
    };
})();
