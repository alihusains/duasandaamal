# Raazoneyaz Web Application Architecture & Design

## 1. Understanding Summary
- **What is being built:** A responsive web application version of the Raazoneyaz Flutter mobile app. It will live in the `website/` directory and be hosted on GitHub Pages.
- **Why it exists:** To provide desktop and web users identical access to the Duas/Ziyarats, while adding new web-first features like Global Search and a Presentation (Slide) mode.
- **Who it is for:** End users seeking to read or present the app's content from a browser.
- **Key Constraints:** Must load the 84MB `ron.db` directly in the browser. Must use specific fonts exactly as mapped in `font_settings.dart`.
- **Explicit Non-Goals:** No backend server infrastructure. No API limits.

## 2. Assumptions
- Because `ron.db` is an 84MB file, the app requires a "Download Once, Load Instantly" strategy using `localforage` (IndexedDB) and `sql.js`.
- The user's device has enough local storage to cache the 84MB file.
- The UI will mirror the mobile app's flow as closely as possible using responsive web components.

## 3. Decision Log

| Decision | Alternatives Considered | Why Chosen |
|---|---|---|
| **Tech Stack:** Vite + Vue 3 + Tailwind CSS + DaisyUI | CDN-only HTML/JS (No Build Step) <br> Nuxt 3 (Static Generation) | Provides a robust, component-based developer experience. DaisyUI eliminates the need to build buttons/navbars from scratch, serving as our "readymade template." Vite provides highly optimized builds for GitHub pages. |
| **Database Engine:** `sql.js` + IndexedDB | HTTP Range Requests (`sqlite3-wasm`) <br> JSON Export | Range requests are complex to configure on static GitHub Pages. Caching the full DB in IndexedDB ensures flawless "Offline First" performance after the initial load. |
| **Routing:** `vue-router` matching Flutter's flow | Single component state switching | Allows users to bookmark and share specific Duas or Ziyarats. Perfectly maps to Flutter's `Navigator.push` logic. |

## 4. Final Design

### 4.1 Architecture & Automated Deployment
- The app is built using Vite and Vue 3.
- A GitHub Actions workflow (`deploy.yml`) will be created to automatically run `npm run build` and push the `dist/` folder to GitHub Pages upon every commit.

### 4.2 Data Flow (Offline-First)
1. **Initial Load:** App checks IndexedDB for `ron.db`. If missing, shows a loading screen, fetches `ron.db` via HTTP, and saves it.
2. **Execution:** Initializes `sql.js` using the cached ArrayBuffer. All future queries (Categories, Lines, Search) execute synchronously in memory.

### 4.3 Navigation & Routing
- **`/` (Language Selection):** Checks `localStorage` for `selectedLanguage`. If present, redirects to `/categories`. If missing, shows the selection screen (English, Urdu, Roman Urdu).
- **`/categories`:** Main categories list (fetched via SQL: `SELECT * FROM Categories`).
- **`/subcategories/:id`:** Children of a category (fetched via SQL: `SELECT * FROM Subindex`).
- **`/lines/:id`:** Scrolling list of Arabic, Translation, Transliteration (fetched via SQL `JOIN` on `LinesMetadata` and `Lines`).

### 4.4 Global Search
- A search bar in the global navigation header.
- Executes `SELECT * FROM Lines WHERE ... LIKE '%search%'` across all languages and arabic text columns.
- Clicking a result instantly routes to the specific line in `/lines/:id`.

### 4.5 Slide View (Presenter Mode)
- Accessed via a "Present" button on the `/lines/:id` page.
- URL: `/presenter/:id`
- Full-screen layout replicating `alihusains/presenter`.
- Displays one line at a time. Keyboard navigation (Left/Right arrows) updates a `currentIndex` reactive variable.
- Fonts are injected dynamically based on a JavaScript translation of `font_settings.dart` (e.g., `ShiaEssentials`, `DnaGujarati`).