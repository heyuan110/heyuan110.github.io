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

    // ==================== 公共 UI 翻译 ====================
    var COMMON_I18N = {
        en: {
            home: 'Home',
            toolbox: 'Web Toolbox',
            cat_pdf: 'PDF Tools',
            cat_image: 'Image Tools',
            cat_developer: 'Developer Tools',
            cat_text: 'Text Tools',
            cat_media: 'Media Tools',
            cat_utility: 'Utility Tools',
            nav_home: 'Magic ToolBox',
            nav_pdf: 'PDF',
            nav_image: 'Image',
            nav_developer: 'Dev',
            nav_text: 'Text',
            nav_media: 'Media',
            nav_utility: 'Utility',
            copyright: '© 2024-2026 <a href="https://github.com/heyuan110" target="_blank" rel="noopener">heyuan110.com</a>. All rights reserved.'
        },
        'zh-CN': {
            home: '首页',
            toolbox: '在线工具箱',
            cat_pdf: 'PDF 工具',
            cat_image: '图片工具',
            cat_developer: '开发者工具',
            cat_text: '文本工具',
            cat_media: '媒体工具',
            cat_utility: '实用工具',
            nav_home: '工具箱首页',
            nav_pdf: 'PDF',
            nav_image: '图片',
            nav_developer: '开发',
            nav_text: '文本',
            nav_media: '媒体',
            nav_utility: '实用',
            copyright: '© 2024-2026 <a href="https://github.com/heyuan110" target="_blank" rel="noopener">heyuan110.com</a>. 保留所有权利。'
        },
        fr: {
            home: 'Accueil',
            toolbox: 'Boîte à Outils',
            cat_pdf: 'Outils PDF',
            cat_image: 'Outils Image',
            cat_developer: 'Outils Dev',
            cat_text: 'Outils Texte',
            cat_media: 'Outils Média',
            cat_utility: 'Outils Utilitaires',
            nav_home: 'Boîte à Outils',
            nav_pdf: 'PDF',
            nav_image: 'Image',
            nav_developer: 'Dev',
            nav_text: 'Texte',
            nav_media: 'Média',
            nav_utility: 'Utilitaire',
            copyright: '© 2024-2026 <a href="https://github.com/heyuan110" target="_blank" rel="noopener">heyuan110.com</a>. Tous droits réservés.'
        },
        es: {
            home: 'Inicio',
            toolbox: 'Caja de Herramientas',
            cat_pdf: 'Herramientas PDF',
            cat_image: 'Herramientas Imagen',
            cat_developer: 'Herramientas Dev',
            cat_text: 'Herramientas Texto',
            cat_media: 'Herramientas Medios',
            cat_utility: 'Herramientas Utilidad',
            nav_home: 'Herramientas',
            nav_pdf: 'PDF',
            nav_image: 'Imagen',
            nav_developer: 'Dev',
            nav_text: 'Texto',
            nav_media: 'Medios',
            nav_utility: 'Utilidad',
            copyright: '© 2024-2026 <a href="https://github.com/heyuan110" target="_blank" rel="noopener">heyuan110.com</a>. Todos los derechos reservados.'
        }
    };

    // 公共翻译辅助函数
    function ct(lang, key) {
        var t = COMMON_I18N[lang] || COMMON_I18N['en'];
        return t[key] || COMMON_I18N['en'][key] || key;
    }

    // 类目配置
    var CATEGORIES = [
        { key: 'home',      emoji: '🏠', i18nKey: 'nav_home',      href: 'index.html' },
        { key: 'pdf',       emoji: '📄', i18nKey: 'nav_pdf',       href: 'category/pdf-tools.html' },
        { key: 'image',     emoji: '🖼️', i18nKey: 'nav_image',     href: 'category/image-tools.html' },
        { key: 'developer', emoji: '💻', i18nKey: 'nav_developer', href: 'category/developer-tools.html' },
        { key: 'text',      emoji: '📝', i18nKey: 'nav_text',      href: 'category/text-tools.html' },
        { key: 'media',     emoji: '🎬', i18nKey: 'nav_media',     href: 'category/media-tools.html' },
        { key: 'utility',   emoji: '⚡', i18nKey: 'nav_utility',   href: 'category/utility-tools.html' }
    ];

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
            category: script.getAttribute('data-category')  || 'utility',
            pageType: script.getAttribute('data-page-type') || 'tool',
            showThemeToggle: script.getAttribute('data-show-theme-toggle') === 'true'
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

    // ==================== DOM 构建 ====================

    // 生成面包屑 + 语言切换器 HTML
    function buildHeader(config, lang) {
        var catKey = 'cat_' + config.category;
        var catHref = '';
        CATEGORIES.forEach(function (c) {
            if (c.key === config.category) catHref = c.href;
        });

        // 分类页在 category/ 子目录，需要 ../index.html
        var indexHref = config.pageType === 'category' ? '../index.html' : 'index.html';

        var breadcrumb;
        if (config.pageType === 'category') {
            // 分类页：3 级面包屑 Home > Web Toolbox > 分类名
            breadcrumb =
                '<a href="/" data-common-i18n="home">' + ct(lang, 'home') + '</a><span class="bc-sep">›</span>' +
                '<a href="' + indexHref + '" data-common-i18n="toolbox">' + ct(lang, 'toolbox') + '</a><span class="bc-sep">›</span>' +
                '<span class="bc-cur" data-common-i18n="' + catKey + '">' + ct(lang, catKey) + '</span>';
        } else {
            // 工具页：4 级面包屑 Home > Web Toolbox > 分类 > 工具名
            var catPart = catHref
                ? '<a href="' + catHref + '" data-common-i18n="' + catKey + '">' + ct(lang, catKey) + '</a><span class="bc-sep">›</span>'
                : '';
            breadcrumb =
                '<a href="/" data-common-i18n="home">' + ct(lang, 'home') + '</a><span class="bc-sep">›</span>' +
                '<a href="index.html" data-common-i18n="toolbox">' + ct(lang, 'toolbox') + '</a><span class="bc-sep">›</span>' +
                catPart +
                '<span class="bc-cur" data-i18n="tool_name">' + config.toolName + '</span>';
        }

        var themeBtn = config.showThemeToggle
            ? '<button class="theme-toggle" id="themeToggle" title="Toggle theme">🌙</button>'
            : '';

        return '<nav class="bc-nav" aria-label="Breadcrumb">' +
            '<div class="bc-left">' + breadcrumb + '</div>' +
            '<div class="bc-right">' +
                themeBtn +
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
            '</div>' +
        '</nav>';
    }

    // 生成类目导航 HTML
    function buildCategoryNav(activeCategory, lang) {
        var items = CATEGORIES.map(function (c) {
            var cls = c.key === activeCategory ? ' active' : '';
            return '<a href="' + c.href + '" class="cat-nav-item' + cls + '" data-common-i18n="' + c.i18nKey + '">' + c.emoji + ' ' + ct(lang, c.i18nKey) + '</a>';
        }).join('\n        ');
        return '<nav class="category-nav">\n        ' + items + '\n    </nav>';
    }

    // 生成 footer HTML
    function buildFooter(config, lang) {
        if (config.pageType === 'category') {
            // 分类页：仅版权行，无类目导航
            return '<footer class="site-footer">' +
                '<p data-common-i18n="copyright">' + ct(lang, 'copyright') + '</p>' +
                '</footer>';
        }
        // 工具页：类目导航 + 版权
        return buildCategoryNav(config.category, lang) +
            '\n    <footer class="site-footer">' +
            '<p data-common-i18n="copyright">' + ct(lang, 'copyright') + '</p>' +
            '</footer>';
    }

    // 注入 header（在 <body> 开始处）
    function injectHeader(config, lang) {
        if (document.querySelector('.bc-nav')) return;
        var html = buildHeader(config, lang);
        var container = document.querySelector('.container');
        if (container) {
            container.insertAdjacentHTML('afterbegin', html);
        } else {
            document.body.insertAdjacentHTML('afterbegin', html);
        }
    }

    // 注入 footer（在 .container 末尾或 </body> 前）
    function injectFooter(config, lang) {
        if (document.querySelector('.category-nav') || document.querySelector('.site-footer')) return;
        var container = document.querySelector('.container');
        var footerHtml = buildFooter(config, lang);
        if (container) {
            container.insertAdjacentHTML('beforeend', footerHtml);
        } else {
            document.body.insertAdjacentHTML('beforeend', footerHtml);
        }
    }

    // 主题切换
    function bindThemeToggle() {
        var toggle = document.getElementById('themeToggle');
        if (!toggle) return;
        var saved = localStorage.getItem('magic_toolbox_theme');
        if (saved === 'light') {
            document.body.setAttribute('data-theme', 'light');
            toggle.textContent = '☀️';
        }
        toggle.addEventListener('click', function () {
            var isLight = document.body.getAttribute('data-theme') === 'light';
            if (isLight) {
                document.body.removeAttribute('data-theme');
                toggle.textContent = '🌙';
                localStorage.setItem('magic_toolbox_theme', 'dark');
            } else {
                document.body.setAttribute('data-theme', 'light');
                toggle.textContent = '☀️';
                localStorage.setItem('magic_toolbox_theme', 'light');
            }
        });
    }

    // ==================== 语言切换 ====================

    // 更新公共 UI 翻译（面包屑、类目导航、版权）
    function applyCommonTranslations(lang) {
        document.querySelectorAll('[data-common-i18n]').forEach(function (el) {
            var key = el.getAttribute('data-common-i18n');
            var val = ct(lang, key);
            // 类目导航带 emoji 前缀
            if (key.indexOf('nav_') === 0) {
                CATEGORIES.forEach(function (c) {
                    if (c.i18nKey === key) {
                        val = c.emoji + ' ' + val;
                    }
                });
            }
            if (key === 'copyright') {
                el.innerHTML = val;
            } else {
                el.textContent = val;
            }
        });
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

    // 应用工具翻译
    function applyTranslations(lang, translations) {
        var t = translations[lang] || translations['en'];
        if (!t) return;

        document.documentElement.lang = lang;

        document.querySelectorAll('[data-i18n]').forEach(function (el) {
            var key = el.getAttribute('data-i18n');
            if (t[key] !== undefined) {
                el.innerHTML = t[key];
            }
        });

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

        // 更新工具翻译
        applyTranslations(lang, translations);

        // 更新公共 UI 翻译
        applyCommonTranslations(lang);

        // 更新语言切换器显示
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

    // ==================== 公开 API ====================
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
            migrateOldLangKey(config.toolId);

            var lang = getCurrentLang();

            // 注入 header & footer（带当前语言）
            injectHeader(config, lang);
            injectFooter(config, lang);

            // 绑定主题切换
            bindThemeToggle();

            // 绑定语言切换器
            bindLangSwitcher(translations || {});

            // 绑定 FAQ 手风琴
            bindFaqAccordion();

            // 首次翻译
            if (translations) {
                applyTranslations(lang, translations);
            }
            applyCommonTranslations(lang);

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
