# CÁC THAY ĐỔI CẦN ÁP DỤNG VÀO templates/base.html

## 1. THÊM THEME INIT SCRIPT (sau dòng 6)

Tìm:
```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
```

Thay bằng:
```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  {# Theme initialization script - prevents FOUC #}
  <script>
    (function() {
      const theme = localStorage.getItem('theme') || 
                   (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.classList.toggle('dark', theme === 'dark');
    })();
  </script>
```

## 2. THÊM darkMode CONFIG

Tìm:
```javascript
    tailwind.config = {
      theme: {
```

Thay bằng:
```javascript
    tailwind.config = {
      darkMode: 'class',
      theme: {
```

## 3. SỬA BODY STYLES

Tìm:
```css
      body { @apply font-sans text-slate-300 bg-[#080d12] antialiased; }
```

Thay bằng:
```css
      body { 
        @apply font-sans antialiased transition-colors duration-300
               bg-white text-slate-900
               dark:bg-[#080d12] dark:text-slate-300;
      }
```

## 4. SỬA SELECTION

Tìm:
```css
      ::selection { @apply bg-brand-500/30 text-brand-200; }
```

Thay bằng:
```css
      ::selection { 
        @apply bg-brand-500/20 text-brand-700
               dark:bg-brand-500/30 dark:text-brand-200;
      }
```

## 5. SỬA SCROLLBAR

Tìm:
```css
      ::-webkit-scrollbar-track { @apply bg-slate-950; }
      ::-webkit-scrollbar-thumb { @apply bg-slate-700 rounded-full; }
```

Thay bằng:
```css
      ::-webkit-scrollbar-track { 
        @apply bg-slate-100 dark:bg-slate-950;
      }
      ::-webkit-scrollbar-thumb { 
        @apply bg-slate-400 dark:bg-slate-700 rounded-full;
      }
```

## 6. SỬA BTN-GHOST

Tìm:
```css
      .btn-ghost {
        @apply inline-flex items-center gap-2 border border-slate-700
               hover:border-brand-500/60 text-slate-400 hover:text-brand-300
               font-semibold px-6 py-3 rounded-lg bg-transparent
               transition-all duration-200 text-sm;
      }
```

Thay bằng:
```css
      .btn-ghost {
        @apply inline-flex items-center gap-2 border font-semibold px-6 py-3 rounded-lg
               bg-transparent transition-all duration-200 text-sm
               border-slate-300 text-slate-700 hover:border-brand-500 hover:text-brand-600
               dark:border-slate-700 dark:text-slate-400 dark:hover:border-brand-500/60 dark:hover:text-brand-300;
      }
```

## 7. SỬA NAV-LINK

Tìm:
```css
      .nav-link {
        @apply relative text-slate-400 hover:text-white text-sm font-medium
               px-3 py-2 rounded-md transition-colors duration-150;
      }
```

Thay bằng:
```css
      .nav-link {
        @apply relative text-sm font-medium px-3 py-2 rounded-md transition-colors duration-150
               text-slate-600 hover:text-slate-900
               dark:text-slate-400 dark:hover:text-white;
      }
```

## 8. SỬA NAV-LINK ACTIVE

Tìm:
```css
      .nav-link.active { @apply text-white; }
```

Thay bằng:
```css
      .nav-link.active { 
        @apply text-slate-900 dark:text-white;
      }
```

## 9. SỬA SECTION-LABEL

Tìm:
```css
      .section-label {
        @apply font-mono text-[10px] uppercase tracking-[.2em] text-brand-400
               flex items-center gap-2;
      }
      .section-label::before {
        content: '';
        @apply inline-block w-4 h-px bg-brand-400;
      }
```

Thay bằng:
```css
      .section-label {
        @apply font-mono text-[10px] uppercase tracking-[.2em] flex items-center gap-2
               text-brand-600 dark:text-brand-400;
      }
      .section-label::before {
        content: '';
        @apply inline-block w-4 h-px bg-brand-600 dark:bg-brand-400;
      }
```

## 10. SỬA CARD-INDUSTRIAL

Tìm:
```css
      .card-industrial {
        @apply bg-slate-900/60 border border-slate-800 rounded-xl
               hover:border-brand-500/40 hover:bg-slate-900
               transition-all duration-300 backdrop-blur-sm;
      }
```

Thay bằng:
```css
      .card-industrial {
        @apply rounded-xl border transition-all duration-300
               bg-white border-slate-200 hover:border-brand-400 hover:bg-slate-50
               dark:bg-slate-900/60 dark:border-slate-800 dark:hover:border-brand-500/40 dark:hover:bg-slate-900 dark:backdrop-blur-sm;
      }
```

## 11. SỬA TAGS

Tìm:
```css
      .tag-blue  { @apply bg-brand-950/60  text-brand-300  border-brand-800/60; }
      .tag-green { @apply bg-emerald-950/60 text-emerald-300 border-emerald-800/60; }
      .tag-amber { @apply bg-amber-950/60  text-amber-300  border-amber-800/60; }
      .tag-red   { @apply bg-red-950/60    text-red-300    border-red-800/60; }
```

Thay bằng:
```css
      .tag-blue  { 
        @apply bg-brand-50 text-brand-700 border-brand-200
               dark:bg-brand-950/60 dark:text-brand-300 dark:border-brand-800/60;
      }
      .tag-green { 
        @apply bg-emerald-50 text-emerald-700 border-emerald-200
               dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/60;
      }
      .tag-amber { 
        @apply bg-amber-50 text-amber-700 border-amber-200
               dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/60;
      }
      .tag-red { 
        @apply bg-red-50 text-red-700 border-red-200
               dark:bg-red-950/60 dark:text-red-300 dark:border-red-800/60;
      }
```

## 12. SỬA MESSAGES

Tìm:
```css
      .msg-success { @apply bg-emerald-950/60 text-emerald-300 border border-emerald-800/60; }
      .msg-error   { @apply bg-red-950/60    text-red-300    border border-red-800/60; }
      .msg-warning { @apply bg-amber-950/60  text-amber-300  border border-amber-800/60; }
      .msg-info    { @apply bg-brand-950/60  text-brand-300  border border-brand-700/60; }
```

Thay bằng:
```css
      .msg-success { 
        @apply border bg-emerald-50 text-emerald-800 border-emerald-200
               dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-800/60;
      }
      .msg-error { 
        @apply border bg-red-50 text-red-800 border-red-200
               dark:bg-red-950/60 dark:text-red-300 dark:border-red-800/60;
      }
      .msg-warning { 
        @apply border bg-amber-50 text-amber-800 border-amber-200
               dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/60;
      }
      .msg-info { 
        @apply border bg-brand-50 text-brand-800 border-brand-200
               dark:bg-brand-950/60 dark:text-brand-300 dark:border-brand-700/60;
      }
```

## 13. SỬA AUTOCOMPLETE-ITEM

Tìm:
```css
      .autocomplete-item {
        @apply flex items-center gap-3 px-4 py-3 hover:bg-slate-800/80
               cursor-pointer transition-colors border-b border-slate-800/60 last:border-0;
      }
```

Thay bằng:
```css
      .autocomplete-item {
        @apply flex items-center gap-3 px-4 py-3 cursor-pointer transition-colors
               border-b last:border-0
               hover:bg-slate-100 border-slate-200
               dark:hover:bg-slate-800/80 dark:border-slate-800/60;
      }
```

## 14. SỬA USER-MENU-ITEM

Tìm:
```css
      .user-menu-item {
        @apply flex items-center gap-2.5 px-4 py-2.5 text-sm text-slate-400
               hover:text-white hover:bg-slate-800/60 transition-colors w-full text-left;
      }
```

Thay bằng:
```css
      .user-menu-item {
        @apply flex items-center gap-2.5 px-4 py-2.5 text-sm transition-colors w-full text-left
               text-slate-600 hover:text-slate-900 hover:bg-slate-100
               dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800/60;
      }
```

## 15. THÊM THEME TOGGLE BUTTON

Tìm dòng:
```html
        {# ── Right actions ── #}
        <div class="flex items-center gap-1.5 flex-shrink-0">

          {# ── Search Button + Overlay ── #}
```

Thay bằng:
```html
        {# ── Right actions ── #}
        <div class="flex items-center gap-1.5 flex-shrink-0">

          {# ── Theme Toggle Button ── #}
          <button id="theme-toggle"
                  type="button"
                  class="w-8 h-8 flex items-center justify-center rounded-md z-10
                         text-slate-500 hover:text-brand-600 hover:bg-slate-100
                         dark:text-slate-500 dark:hover:text-brand-400 dark:hover:bg-slate-800/60
                         transition-all duration-150"
                  aria-label="Toggle theme">
            <svg id="theme-icon-sun" class="w-4 h-4 hidden dark:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" 
                    d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
            </svg>
            <svg id="theme-icon-moon" class="w-4 h-4 block dark:hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" stroke-linejoin="round" 
                    d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
            </svg>
          </button>

          {# ── Search Button + Overlay ── #}
```

## 16. SỬA LOGO TEXT

Tìm:
```html
            <span class="font-display font-bold text-white text-lg uppercase tracking-widest leading-none">
              {{ COMPANY_NAME|default:"IoTech" }}
            </span>
            <span class="block font-mono text-[8px] text-brand-400 tracking-[.25em] uppercase leading-none">
              Industrial IoT
            </span>
```

Thay bằng:
```html
            <span class="font-display font-bold text-lg uppercase tracking-widest leading-none
                         text-slate-900 dark:text-white">
              {{ COMPANY_NAME|default:"IoTech" }}
            </span>
            <span class="block font-mono text-[8px] tracking-[.25em] uppercase leading-none
                         text-brand-600 dark:text-brand-400">
              Industrial IoT
            </span>
```

## 17. THÊM JAVASCRIPT THEME TOGGLE

Tìm dòng:
```javascript
  <script>
  (function () {

    // ─── 1. Sticky header ────────────────────────────────────────────────
```

Thay bằng:
```javascript
  <script>
  (function () {

    // ─── 0. Theme Toggle ─────────────────────────────────────────────────
    const html = document.documentElement;
    const themeBtn = document.getElementById('theme-toggle');
    const header = document.getElementById('site-header');

    function isDark() {
      return html.classList.contains('dark');
    }

    function applyTheme(theme) {
      html.classList.toggle('dark', theme === 'dark');
      localStorage.setItem('theme', theme);
      setTimeout(() => onScroll(), 50);
    }

    themeBtn?.addEventListener('click', () => {
      applyTheme(isDark() ? 'light' : 'dark');
    });


    // ─── 1. Sticky header ────────────────────────────────────────────────
```

## 18. SỬA ONSCROLL FUNCTION

Tìm:
```javascript
    const header = document.getElementById('site-header');
    const onScroll = () => {
      if (window.scrollY > 40) {
        header.style.background     = 'rgba(8,13,18,.96)';
        header.style.borderBottom   = '1px solid rgba(255,255,255,.06)';
        header.style.backdropFilter = 'blur(16px)';
      } else {
        header.style.background     = 'rgba(8,13,18,0)';
        header.style.borderBottom   = 'none';
        header.style.backdropFilter = 'none';
      }
    };
```

Thay bằng:
```javascript
    const onScroll = () => {
      if (!header) return;
      const scrolled = window.scrollY > 40;
      
      if (scrolled) {
        header.style.background = isDark()
          ? 'rgba(8,13,18,.96)'
          : 'rgba(255,255,255,.97)';
        header.style.borderBottom = isDark()
          ? '1px solid rgba(255,255,255,.06)'
          : '1px solid rgba(0,0,0,.08)';
        header.style.backdropFilter = 'blur(16px)';
      } else {
        header.style.background = 'transparent';
        header.style.borderBottom = 'none';
        header.style.backdropFilter = 'none';
      }
    };
```

---

**LƯU Ý:** Đây là TẤT CẢ các thay đổi cần thiết. Hãy áp dụng từng thay đổi một cách cẩn thận.

Sau khi hoàn thành, test kỹ trên trình duyệt!
