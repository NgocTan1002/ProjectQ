#!/usr/bin/env python3
"""
Script để sửa Dark/Light mode trong base.html
Chạy: python fix_theme.py
"""

import re

# Đọc file gốc
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.content()

print("Đang sửa file base.html...")

# 1. Thêm theme initialization script
if '{# Theme initialization script' not in content:
    content = content.replace(
        '<head>\n  <meta charset="UTF-8">',
        '''<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  {# Theme initialization script - prevents FOUC #}
  <script>
    (function() {
      const theme = localStorage.getItem('theme') || 
                   (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.classList.toggle('dark', theme === 'dark');
    })();
  </script>'''
    )

# 2. Thêm darkMode: 'class' vào Tailwind config
content = content.replace(
    'tailwind.config = {',
    '''tailwind.config = {
      darkMode: 'class','''
)

# 3. Thêm theme toggle button vào header
if 'theme-toggle' not in content:
    # Tìm vị trí để chèn button (trước search button)
    search_button_pattern = r'(\{# ── Search Button)'
    replacement = r'''{# ── Theme Toggle Button ── #}
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

          \1'''
    content = re.sub(search_button_pattern, replacement, content)

print("✅ Đã sửa xong!")
print("File đã được cập nhật: templates/base.html")
print("\nVui lòng:")
print("1. Kiểm tra file templates/base.html")
print("2. Test theme toggle trên trình duyệt")
print("3. Kiểm tra tất cả các trang")
