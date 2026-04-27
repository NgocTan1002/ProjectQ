# Hướng Dẫn Sửa Dark/Light Mode HOÀN CHỈNH

## VẤN ĐỀ CHÍNH

File base.html hiện tại có các vấn đề sau:
1. ❌ Sử dụng `.light` class selector - KHÔNG hoạt động với Tailwind CDN
2. ❌ Nhiều component vẫn hardcode dark mode (bg-slate-900, text-slate-300)
3. ❌ Theme toggle button có thể bị che khuất
4. ❌ Text colors không đúng trong light mode

## GIẢI PHÁP ĐÚNG

### 1. XÓA TẤT CẢ `.light` SELECTORS

Thay vì:
```css
.light .nav-link {
  @apply text-slate-600;
}
```

Dùng trực tiếp trong HTML:
```html
<a class="text-slate-600 dark:text-slate-400">Link</a>
```

### 2. REFACTOR TẤT CẢ COMPONENTS

#### Body
```css
body {
  @apply font-sans antialiased transition-colors duration-300
         bg-white text-slate-900
         dark:bg-[#080d12] dark:text-slate-300;
}
```

#### Buttons
```css
.btn-ghost {
  @apply inline-flex items-center gap-2 border font-semibold px-6 py-3 rounded-lg
         bg-transparent transition-all duration-200 text-sm
         border-slate-300 text-slate-700 hover:border-brand-500 hover:text-brand-600
         dark:border-slate-700 dark:text-slate-400 dark:hover:border-brand-500/60 dark:hover:text-brand-300;
}
```

#### Nav Links
```css
.nav-link {
  @apply relative text-sm font-medium px-3 py-2 rounded-md transition-colors duration-150
         text-slate-600 hover:text-slate-900
         dark:text-slate-400 dark:hover:text-white;
}
```

#### Cards
```css
.card-industrial {
  @apply rounded-xl border transition-all duration-300
         bg-white border-slate-200 hover:border-brand-400 hover:bg-slate-50
         dark:bg-slate-900/60 dark:border-slate-800 dark:hover:border-brand-500/40 dark:hover:bg-slate-900;
}
```

### 3. SỬA HEADER

```html
<header id="site-header" class="fixed top-0 inset-x-0 z-50 transition-all duration-300">
  <!-- Logo text -->
  <span class="font-display font-bold text-lg uppercase tracking-widest leading-none
               text-slate-900 dark:text-white">
    {{ COMPANY_NAME }}
  </span>
  
  <!-- Nav links -->
  <a href="..." class="nav-link text-slate-600 hover:text-slate-900
                       dark:text-slate-400 dark:hover:text-white">
    Trang chủ
  </a>
  
  <!-- Theme toggle - ĐẢM BẢO KHÔNG BỊ CHE -->
  <button id="theme-toggle" class="w-8 h-8 flex items-center justify-center rounded-md
                                   text-slate-500 hover:text-brand-600 hover:bg-slate-100
                                   dark:text-slate-500 dark:hover:text-brand-400 dark:hover:bg-slate-800/60
                                   transition-all duration-150 z-10">
    <!-- Icons -->
  </button>
</header>
```

### 4. SỬA SEARCH OVERLAY

```html
<div id="search-overlay" class="fixed inset-0 z-[60] ... 
                                bg-white/95 dark:bg-[rgba(5,10,15,.92)]"
     style="backdrop-filter: blur(12px);">
  
  <input class="w-full px-4 py-3 rounded-2xl border outline-none
                bg-white border-slate-300 text-slate-900 placeholder-slate-400
                focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20
                dark:bg-slate-900 dark:border-slate-700 dark:text-white dark:placeholder-slate-500
                dark:focus:border-brand-600 dark:focus:ring-brand-700/40">
</div>
```

### 5. SỬA FOOTER

```html
<footer class="border-t mt-24 transition-colors
               bg-slate-50 border-slate-200
               dark:bg-[#050a0f] dark:border-slate-800/60">
  
  <!-- Ticker -->
  <div class="border-b overflow-hidden py-2.5
              bg-brand-50 border-slate-200
              dark:bg-brand-950/20 dark:border-slate-800/60">
    <span class="text-brand-600/60 dark:text-brand-500/60">...</span>
  </div>
  
  <!-- Links -->
  <a class="text-slate-500 hover:text-brand-600
            dark:text-slate-500 dark:hover:text-brand-400">Link</a>
</footer>
```

### 6. SỬA JAVASCRIPT - HEADER BACKGROUND

```javascript
function onScroll() {
  const isDark = html.classList.contains('dark');
  if (window.scrollY > 40) {
    header.style.background = isDark
      ? 'rgba(8,13,18,.96)'
      : 'rgba(255,255,255,.97)';
    header.style.borderBottom = isDark
      ? '1px solid rgba(255,255,255,.06)'
      : '1px solid rgba(0,0,0,.08)';
    header.style.backdropFilter = 'blur(16px)';
  } else {
    header.style.background = 'transparent';
    header.style.borderBottom = 'none';
    header.style.backdropFilter = 'none';
  }
}
```

### 7. SỬA MOBILE MENU

```html
<div id="mobile-menu" class="lg:hidden overflow-hidden transition-all duration-300 max-h-0
                             bg-white/97 border-slate-200
                             dark:bg-[rgba(8,13,18,.97)] dark:border-slate-800/60">
  <nav class="...">
    <a class="nav-link text-slate-600 hover:text-slate-900
              dark:text-slate-400 dark:hover:text-white">...</a>
  </nav>
</div>
```

### 8. SỬA USER DROPDOWN

```html
<button id="user-menu-btn" class="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-lg border
                                  bg-white border-slate-300 text-slate-700 hover:bg-slate-50
                                  dark:bg-slate-900/40 dark:border-slate-700/60 dark:text-slate-300 dark:hover:bg-slate-800/60">
  ...
</button>

<div id="user-dropdown" class="... bg-white border-slate-200
                                dark:bg-slate-900 dark:border-slate-700/60">
  <a class="user-menu-item text-slate-600 hover:text-slate-900 hover:bg-slate-100
            dark:text-slate-400 dark:hover:text-white dark:hover:bg-slate-800/60">
    ...
  </a>
</div>
```

## CHECKLIST SỬA CHỮA

- [ ] Xóa TẤT CẢ `.light` selectors trong `<style>`
- [ ] Sửa `body` - light mode là default
- [ ] Sửa `.btn-ghost` - light mode trước, dark sau
- [ ] Sửa `.nav-link` - light mode trước, dark sau
- [ ] Sửa `.card-industrial` - light mode trước, dark sau
- [ ] Sửa `.tag-*` classes - light mode trước, dark sau
- [ ] Sửa `.msg-*` classes - light mode trước, dark sau
- [ ] Sửa header logo text colors
- [ ] Sửa header nav links colors
- [ ] Sửa header buttons colors
- [ ] Sửa theme toggle button - thêm z-10
- [ ] Sửa search overlay background
- [ ] Sửa search input colors
- [ ] Sửa search results colors
- [ ] Sửa mobile menu background
- [ ] Sửa user dropdown colors
- [ ] Sửa footer background
- [ ] Sửa footer links colors
- [ ] Sửa JavaScript onScroll function
- [ ] Test theme toggle hoạt động
- [ ] Test tất cả trang (home, products, solutions, etc.)

## QUY TẮC QUAN TRỌNG

1. **LUÔN ĐẶT LIGHT MODE TRƯỚC, DARK MODE SAU**
   ```html
   <div class="bg-white text-slate-900 dark:bg-slate-900 dark:text-slate-300">
   ```

2. **KHÔNG DÙNG `.light` CLASS**
   - Tailwind CDN không hỗ trợ custom class selectors
   - Chỉ dùng utility classes trực tiếp

3. **DÙNG `dark:` MODIFIER CHO MỌI THỨ**
   - Background: `bg-white dark:bg-slate-900`
   - Text: `text-slate-900 dark:text-slate-300`
   - Border: `border-slate-200 dark:border-slate-800`

4. **ĐẢM BẢO CONTRAST TỐT**
   - Light mode: text-slate-900, text-slate-700, text-slate-600
   - Dark mode: text-white, text-slate-300, text-slate-400

5. **TEST TRÊN TẤT CẢ TRANG**
   - Home
   - Products list
   - Solutions list
   - Product detail
   - Solution detail
   - Cart
   - Checkout

## KẾT QUẢ MONG ĐỢI

Sau khi sửa:
- ✅ Light mode: nền trắng, text đen, đọc rõ ràng
- ✅ Dark mode: nền tối, text sáng (giữ nguyên design hiện tại)
- ✅ Theme toggle button luôn hiển thị, không bị che
- ✅ Tất cả components đều chuyển đổi đúng
- ✅ Không có text khó đọc
- ✅ Smooth transitions
- ✅ Theme persist sau reload
