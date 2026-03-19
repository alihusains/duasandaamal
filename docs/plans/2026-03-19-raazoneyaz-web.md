# Raazoneyaz Web Application Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a production-ready, offline-first Vue 3 + Tailwind CSS web application mirroring the Raazoneyaz mobile app, adding Global Search and Presenter Slide View functionality, powered by a browser-loaded `ron.db`.

**Architecture:** Vite + Vue 3 SPA. Uses `sql.js` (WebAssembly SQLite) to read `ron.db` directly in the browser after fetching and caching it via `localforage` (IndexedDB) for offline performance. DaisyUI provides readymade Tailwind components.

**Tech Stack:** Vite, Vue 3, Vue Router, Tailwind CSS, DaisyUI, sql.js, localforage.

---

### Task 1: Scaffold Vite Project & Install Dependencies

**Files:**
- Create: `website/package.json`
- Create: `website/vite.config.js`
- Create: `website/index.html`

**Step 1: Initialize Vite Vue Project**
Run: `cd website && npm create vite@latest . -- --template vue`
Expected: PASS (Scaffolds base files)

**Step 2: Install Dependencies**
Run: `npm install vue-router tailwindcss @tailwindcss/vite daisyui sql.js localforage`
Expected: PASS

**Step 3: Configure Tailwind and Vite**
Create `vite.config.js` adding the `@tailwindcss/vite` plugin.
Add `@import "tailwindcss";` to `src/style.css`.
Add DaisyUI plugin to Tailwind config.

**Step 4: Commit**
Run: `git add website/ && git commit -m "chore: scaffold vue vite project with tailwind and daisyui"`

---

### Task 2: Setup Database Service (IndexedDB + sql.js)

**Files:**
- Create: `website/public/ron.db` (copy from existing)
- Create: `website/src/services/db.js`

**Step 1: Copy Database**
Run: `cp ron.db website/public/ron.db` (Ensure the 84MB file is in the public assets).

**Step 2: Write Database Service**
Implement `db.js` using `localforage` to check if `ron.db` exists in IndexedDB. If not, fetch it as an `ArrayBuffer` from `/ron.db`, save it, and initialize `sql.js`. Create helper methods: `query(sql, params)`.

**Step 3: Verify Compilation**
Run: `npm run build`
Expected: PASS

**Step 4: Commit**
Run: `git add website/public/ron.db website/src/services/db.js && git commit -m "feat: setup offline-first sql.js database service"`

---

### Task 3: Setup Router & Language Selection

**Files:**
- Create: `website/src/router.js`
- Create: `website/src/views/LanguageSelection.vue`
- Modify: `website/src/main.js`

**Step 1: Configure Vue Router**
Set up `router.js` with a single route `/` pointing to `LanguageSelection.vue`. Check `localStorage` in a navigation guard; if `selectedLanguage` exists, redirect to `/categories`.

**Step 2: Implement LanguageSelection.vue**
Create a clean DaisyUI card layout with three buttons: English, Urdu, Roman Urdu. On click, save to `localStorage` and push to `/categories`.

**Step 3: Commit**
Run: `git add website/src/ && git commit -m "feat: setup router and language selection flow"`

---

### Task 4: Main Navigation & Categories Grid

**Files:**
- Create: `website/src/App.vue`
- Create: `website/src/components/NavBar.vue`
- Create: `website/src/views/Categories.vue`

**Step 1: Implement App Layout & NavBar**
Add a persistent Top Navbar in `App.vue`. Include a back button (if not on root) and the Global Search input placeholder.

**Step 2: Implement Categories.vue**
On mount, query `db.query("SELECT * FROM Categories")`. Display as a responsive CSS Grid using DaisyUI cards.

**Step 3: Commit**
Run: `git add website/src/ && git commit -m "feat: implement main layout and categories grid"`

---

### Task 5: Subcategories & Lines Reading View

**Files:**
- Create: `website/src/views/Subcategories.vue`
- Create: `website/src/views/LinesView.vue`
- Create: `website/src/services/fonts.js`

**Step 1: Port Font Settings**
Translate `font_settings.dart` into `fonts.js` mapping language codes to font families. Add CSS `@font-face` rules for `ShiaEssentials` and language-specific fonts in `style.css`. Copy font files to `public/fonts/`.

**Step 2: Implement Subcategories**
Route `/category/:id`. Query `Subindex` table where `ParentId = id`. Display list.

**Step 3: Implement Lines View**
Route `/lines/:id`. Query `LinesMetadata` joined with `Lines`. Render Arabic, Translation, and Transliteration stacked vertically per row using the dynamic fonts. Include a prominent "Present" button.

**Step 4: Commit**
Run: `git add website/src/ && git commit -m "feat: implement subcategories and lines reading views with dynamic fonts"`

---

### Task 6: Global Search

**Files:**
- Modify: `website/src/components/NavBar.vue`
- Create: `website/src/components/SearchResults.vue`

**Step 1: Implement SQL LIKE Search**
Add a debounced input to `NavBar.vue`. On type, query the DB searching across `English`, `ArabicText1`, `Urdu` (etc) columns using `LIKE '%term%'`.

**Step 2: Display Results Dropdown**
Show an absolute positioned DaisyUI dropdown under the search bar with instant results. Clicking routes to `/lines/:id` and auto-scrolls to the line.

**Step 3: Commit**
Run: `git add website/src/components/ && git commit -m "feat: implement instant global search across database"`

---

### Task 7: Presenter Slide View

**Files:**
- Create: `website/src/views/PresenterView.vue`

**Step 1: Implement Fullscreen Component**
Route `/presenter/:id`. Fetch lines. Keep a `currentIndex` ref. Display ONLY the current line. Arabic (text-5xl), Translation (text-3xl), Transliteration (text-2xl).

**Step 2: Implement Keyboard & Touch Navigation**
Listen for `keydown` (ArrowRight, ArrowLeft, Space) and add on-screen floating chevron buttons to increment/decrement `currentIndex`.

**Step 3: Commit**
Run: `git add website/src/views/PresenterView.vue && git commit -m "feat: implement fullscreen slide view presenter mode"`

---

### Task 8: GitHub Actions Automated Deployment

**Files:**
- Create: `.github/workflows/deploy-pages.yml`

**Step 1: Write Workflow File**
Create standard GitHub Actions workflow that runs `npm install`, `npm run build`, and uses `actions/upload-pages-artifact` & `actions/deploy-pages` on every push to the `main` or `release` branch.

**Step 2: Commit**
Run: `git add .github/ && git commit -m "ci: add automated github pages deployment workflow"`