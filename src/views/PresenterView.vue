<template>
  <div class="presenter-theme h-screen w-screen overflow-hidden flex flex-col fixed top-0 left-0 z-[100]"
       :style="{
         '--arabic-size': currentArabicSize + 'rem',
         '--trans-size': currentTransSize + 'rem',
         '--translit-size': currentTranslitSize + 'rem'
       }">
    <!-- Top Bar -->
    <div class="top-bar">
      <div class="top-left">
        <button @click="exitPresenter" class="back-btn" title="Back to input (Esc)">← Back</button>
        <span class="slide-counter">{{ currentIndex + 1 }} / {{ lines.length }}</span>
      </div>
      <div class="top-right flex gap-3">
        <!-- Fullscreen Button -->
        <button @click="toggleFullscreen" class="icon-btn" :title="isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'">
          <svg v-if="!isFullscreen" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
        </button>

        <!-- Help Button -->
        <button @click="showShortcuts = true" class="icon-btn" title="Keyboard Shortcuts (?)">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </button>

        <!-- Settings Dropdown -->
        <div class="dropdown dropdown-end">
          <div tabindex="0" role="button" class="icon-btn" title="Display Settings">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
          </div>
          <ul tabindex="0" class="dropdown-content menu p-4 shadow-2xl rounded-box w-72 mt-4 z-[100]" style="background: var(--bar-bg); border: 1px solid var(--border-subtle); backdrop-filter: blur(10px);">
            
            <li class="menu-title" style="color: var(--gold); padding-left: 0.5rem;"><span>Fonts</span></li>
            <li>
              <div class="flex flex-col gap-1 py-1 px-2 hover:bg-transparent cursor-default active:bg-transparent">
                <span class="text-xs" style="color: var(--cream-dim);">Arabic Font</span>
                <select v-model="arabicFont" class="select select-bordered select-xs w-full bg-base-300 text-base-content">
                  <option value="Al-Qalam">Al-Qalam</option>
                  <option value="ShiaEssentials">ShiaEssentials</option>
                </select>
              </div>
            </li>
            <li>
              <div class="flex flex-col gap-1 py-1 px-2 hover:bg-transparent cursor-default active:bg-transparent">
                <span class="text-xs" style="color: var(--cream-dim);">English Font</span>
                <select v-model="englishFont" class="select select-bordered select-xs w-full bg-base-300 text-base-content">
                  <option value="RobotoFlex">RobotoFlex</option>
                  <option value="NotoSans">NotoSans</option>
                </select>
              </div>
            </li>
            <li>
              <div class="flex flex-col gap-1 py-1 px-2 hover:bg-transparent cursor-default active:bg-transparent">
                <span class="text-xs" style="color: var(--cream-dim);">Urdu Font</span>
                <select v-model="urduFont" class="select select-bordered select-xs w-full bg-base-300 text-base-content">
                  <option value="NotoNastaliqUrdu">NotoNastaliqUrdu</option>
                  <option value="NotoSans">NotoSans</option>
                </select>
              </div>
            </li>

            <div class="my-2" style="height: 1px; background: var(--border-subtle);"></div>

            <li class="menu-title" style="color: var(--gold); padding-left: 0.5rem;"><span>Elements</span></li>
            <li>
              <label class="label cursor-pointer justify-start gap-4 hover:bg-white/5 rounded-lg">
                <input type="checkbox" v-model="showArabic" class="checkbox checkbox-sm checkbox-warning" />
                <span class="label-text text-base" style="color: var(--cream);">Arabic</span>
              </label>
            </li>
            <li>
              <label class="label cursor-pointer justify-start gap-4 hover:bg-white/5 rounded-lg">
                <input type="checkbox" v-model="showTranslation" class="checkbox checkbox-sm checkbox-warning" />
                <span class="label-text text-base" style="color: var(--cream);">Translation</span>
              </label>
            </li>
            <li>
              <label class="label cursor-pointer justify-start gap-4 hover:bg-white/5 rounded-lg">
                <input type="checkbox" v-model="showTransliteration" class="checkbox checkbox-sm checkbox-warning" />
                <span class="label-text text-base" style="color: var(--cream);">Transliteration</span>
              </label>
            </li>

            <div class="my-2" style="height: 1px; background: var(--border-subtle);"></div>

            <li class="menu-title" style="color: var(--gold); padding-left: 0.5rem;"><span>Text Sizing</span></li>
            <li class="flex flex-row justify-between items-center py-2 px-2 hover:bg-white/5 rounded-lg cursor-default active:bg-transparent">
              <span style="color: var(--cream-dim);">Auto-fit text</span>
              <button @click.stop="autoFit = !autoFit" class="btn btn-xs" :class="autoFit ? 'btn-warning' : 'btn-outline'" style="width: 50px;">
                {{ autoFit ? 'ON' : 'OFF' }}
              </button>
            </li>
            <li class="flex flex-row justify-between items-center py-2 px-2 hover:bg-white/5 rounded-lg cursor-default active:bg-transparent">
              <span style="color: var(--cream-dim);">Arabic</span>
              <div class="flex items-center gap-2">
                <button @click.stop="changeSize('arabic', -0.2)" class="btn btn-xs btn-square btn-outline text-white">-</button>
                <span style="color: var(--cream); width: 24px; text-align: center;">{{ baseArabicSize.toFixed(1) }}</span>
                <button @click.stop="changeSize('arabic', 0.2)" class="btn btn-xs btn-square btn-outline text-white">+</button>
              </div>
            </li>
            <li class="flex flex-row justify-between items-center py-2 px-2 hover:bg-white/5 rounded-lg cursor-default active:bg-transparent">
              <span style="color: var(--cream-dim);">Translation</span>
              <div class="flex items-center gap-2">
                <button @click.stop="changeSize('trans', -0.2)" class="btn btn-xs btn-square btn-outline text-white">-</button>
                <span style="color: var(--cream); width: 24px; text-align: center;">{{ baseTransSize.toFixed(1) }}</span>
                <button @click.stop="changeSize('trans', 0.2)" class="btn btn-xs btn-square btn-outline text-white">+</button>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- Slide Area -->
    <div class="slide-area" ref="slideAreaRef" @click="handleTouch">
      <div v-if="lines.length === 0" class="loading-spinner"></div>

      <div v-else class="slide-content" ref="slideContentRef" :class="{ 'fading': isFading }">
        <!-- Description block if available on first slide -->
        <div v-if="currentLine.description" class="description-text" :style="{ fontFamily: fontConfig.translation }" :dir="isRtl ? 'rtl' : 'ltr'">
          {{ currentLine.description }}
        </div>

        <div v-if="currentLine.arabic && showArabic" class="arabic-text" :style="{ fontFamily: fontConfig.arabic }" dir="rtl">
          {{ currentLine.arabic }}
        </div>
        <div v-if="currentLine.translation && showTranslation" class="translation-text" :style="{ fontFamily: fontConfig.translation }" :dir="isRtl ? 'rtl' : 'ltr'">
          {{ currentLine.translation }}
        </div>
        <div v-if="currentLine.transliteration && showTransliteration" class="translit-text" :style="{ fontFamily: fontConfig.transliteration }">
          {{ currentLine.transliteration }}
        </div>
      </div>
    </div>

    <!-- Progress Bar -->
    <div class="progress-bar-container" @click="seekProgress">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
      </div>
    </div>

    <!-- Shortcuts Overlay -->
    <div v-if="showShortcuts" class="shortcuts-overlay" @click="showShortcuts = false">
      <div class="shortcuts-panel" @click.stop>
        <div class="flex justify-between items-center mb-6">
          <h3 class="text-2xl font-bold" style="color: var(--gold);">Keyboard Shortcuts</h3>
          <button @click="showShortcuts = false" class="btn btn-sm btn-circle btn-ghost text-white">✕</button>
        </div>
        <div class="space-y-4 text-lg">
          <div class="flex justify-between"><span class="text-base-content/70">Next slide</span><span class="font-mono bg-base-300 px-2 py-1 rounded">→ / Space</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Previous slide</span><span class="font-mono bg-base-300 px-2 py-1 rounded">←</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">First slide</span><span class="font-mono bg-base-300 px-2 py-1 rounded">Home</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Last slide</span><span class="font-mono bg-base-300 px-2 py-1 rounded">End</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Toggle Auto-fit</span><span class="font-mono bg-base-300 px-2 py-1 rounded">A</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Toggle Fullscreen</span><span class="font-mono bg-base-300 px-2 py-1 rounded">F</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Font Size +/-</span><span class="font-mono bg-base-300 px-2 py-1 rounded">+ / -</span></div>
          <div class="flex justify-between"><span class="text-base-content/70">Back / Exit</span><span class="font-mono bg-base-300 px-2 py-1 rounded">Esc</span></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchLines } from '../services/api'
import { getFontConfig } from '../services/fonts'

const router = useRouter()
const route = useRoute()

const lines = ref([])
const currentIndex = ref(0)
const isFading = ref(false)
const slideAreaRef = ref(null)
const slideContentRef = ref(null)
const showShortcuts = ref(false)
const isFullscreen = ref(false)

const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen().catch((err) => {
      console.error(`Error attempting to enable fullscreen: ${err.message}`);
    });
  } else {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    }
  }
}

const handleFullscreenChange = () => {
  isFullscreen.value = !!document.fullscreenElement;
}

const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'
const isRtl = selectedLanguage === 'ur'

const arabicFont = ref(localStorage.getItem('arabicFont') || 'Al-Qalam')
const englishFont = ref(localStorage.getItem('englishFont') || 'RobotoFlex')
const urduFont = ref(localStorage.getItem('urduFont') || 'NotoNastaliqUrdu')

watch(arabicFont, (val) => localStorage.setItem('arabicFont', val))
watch(englishFont, (val) => localStorage.setItem('englishFont', val))
watch(urduFont, (val) => localStorage.setItem('urduFont', val))

const fontConfig = computed(() => {
  return {
    arabic: arabicFont.value,
    transliteration: englishFont.value,
    english: englishFont.value,
    translation: selectedLanguage === 'ur' ? urduFont.value :
                 selectedLanguage === 'gu' ? 'DnaGujarati' : englishFont.value
  }
})

const currentArabicSize = ref(3.5)
const currentTransSize = ref(2.0)
const currentTranslitSize = ref(1.5)

// Display settings with persistence
const showArabic = ref(localStorage.getItem('presenter_showArabic') !== 'false')
const showTranslation = ref(localStorage.getItem('presenter_showTranslation') !== 'false')
const showTransliteration = ref(localStorage.getItem('presenter_showTransliteration') !== 'false')
const autoFit = ref(localStorage.getItem('presenter_autoFit') !== 'false')
const baseArabicSize = ref(parseFloat(localStorage.getItem('presenter_arabicSize')) || 3.5)
const baseTransSize = ref(parseFloat(localStorage.getItem('presenter_transSize')) || 2.0)

watch(showArabic, (val) => localStorage.setItem('presenter_showArabic', val))
watch(showTranslation, (val) => localStorage.setItem('presenter_showTranslation', val))
watch(showTransliteration, (val) => localStorage.setItem('presenter_showTransliteration', val))
watch(autoFit, (val) => localStorage.setItem('presenter_autoFit', val))

const currentLine = computed(() => {
  if (lines.value.length === 0) return {}
  return lines.value[currentIndex.value]
})

const progressPercentage = computed(() => {
  if (lines.value.length <= 1) return 100
  return (currentIndex.value / (lines.value.length - 1)) * 100
})

const exitPresenter = () => {
  router.back()
}

const triggerTransition = async (callback) => {
  isFading.value = true;
  setTimeout(async () => {
    callback();
    await nextTick();
    applySizes();
    setTimeout(() => {
      isFading.value = false;
    }, 50);
  }, 150);
}

const nextSlide = () => {
  if (currentIndex.value < lines.value.length - 1) {
    triggerTransition(() => {
      currentIndex.value++
    });
  }
}

const prevSlide = () => {
  if (currentIndex.value > 0) {
    triggerTransition(() => {
      currentIndex.value--
    });
  }
}

const goToSlide = (idx) => {
  if (idx !== currentIndex.value && idx >= 0 && idx < lines.value.length) {
    triggerTransition(() => {
      currentIndex.value = idx;
    });
  }
}

const handleTouch = (e) => {
  // Only handle touch if we didn't click inside a dropdown or overlay
  if (e.target.closest('.top-bar') || e.target.closest('.dropdown') || showShortcuts.value) return;

  const midpoint = window.innerWidth / 2;
  if (e.clientX > midpoint) nextSlide();
  else prevSlide();
}

const seekProgress = (e) => {
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = (e.clientX - rect.left) / rect.width;
  const idx = Math.round(ratio * (lines.value.length - 1));
  goToSlide(idx);
}

const changeSize = (type, amount) => {
  if (type === 'arabic') {
    baseArabicSize.value = Math.max(1, parseFloat((baseArabicSize.value + amount).toFixed(1)));
    localStorage.setItem('presenter_arabicSize', baseArabicSize.value);
  } else {
    baseTransSize.value = Math.max(0.5, parseFloat((baseTransSize.value + amount).toFixed(1)));
    localStorage.setItem('presenter_transSize', baseTransSize.value);
  }
  applySizes();
}

const handleKeydown = (e) => {
  if (showShortcuts.value && e.key !== '?') {
    showShortcuts.value = false;
  }

  if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'ArrowDown') {
    nextSlide()
  } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
    prevSlide()
  } else if (e.key === 'Home') {
    goToSlide(0)
  } else if (e.key === 'End') {
    goToSlide(lines.value.length - 1)
  } else if (e.key === 'Escape') {
    exitPresenter()
  } else if (e.key === '?') {
    showShortcuts.value = !showShortcuts.value
  } else if (e.key === 'a' || e.key === 'A') {
    autoFit.value = !autoFit.value
  } else if (e.key === '=' || e.key === '+') {
    changeSize('arabic', 0.2);
    changeSize('trans', 0.2);
  } else if (e.key === '-' || e.key === '_') {
    changeSize('arabic', -0.2);
    changeSize('trans', -0.2);
  } else if (e.key === 'f' || e.key === 'F') {
    toggleFullscreen();
  }
}

const applySizes = async () => {
  await nextTick()
  const area = slideAreaRef.value;
  const content_el = slideContentRef.value;

  if (!area || !content_el) {
    currentArabicSize.value = baseArabicSize.value;
    currentTransSize.value = baseTransSize.value;
    currentTranslitSize.value = baseTransSize.value * 0.75;
    return;
  }

  // Reset to base sizes to calculate natural height
  currentArabicSize.value = baseArabicSize.value;
  currentTransSize.value = baseTransSize.value;
  currentTranslitSize.value = baseTransSize.value * 0.75;

  if (!autoFit.value) return;

  await nextTick()

  const maxH = area.clientHeight * 0.88;
  if (content_el.scrollHeight <= maxH) return;

  let scale = maxH / content_el.scrollHeight;
  scale = Math.max(scale, 0.4); // don't go below 40%

  currentArabicSize.value = baseArabicSize.value * scale;
  currentTransSize.value = baseTransSize.value * scale;
  currentTranslitSize.value = baseTransSize.value * 0.75 * scale;
}

watch([showArabic, showTranslation, showTransliteration, autoFit, arabicFont, englishFont, urduFont, currentIndex], () => {
  applySizes();
})

let resizeTimeout;
const handleResize = () => {
  clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    applySizes();
  }, 200);
}

const buildArabicText = (row) => {
  let arabic = '';
  for (let i = 1; i <= 20; i++) {
    const text = row[`ArabicText${i}`];
    if (text) arabic += text;
  }
  return arabic.trim();
}

const getTranslationText = (row) => {
  let text = '';
  if (selectedLanguage === 'ur') text = row.Urdu;
  else if (selectedLanguage === 'ro') text = row.RUrdu;
  else if (selectedLanguage === 'gu') text = row.Gujarati;
  else text = row.English;
  return text ? text.trim() : '';
}

const getTransliterationText = (row) => {
  let text = '';
  if (selectedLanguage === 'ro') text = row.English;
  else text = row.RUrdu || row.English;
  return text ? text.trim() : '';
}

const getDescriptionText = (row) => {
  let text = '';
  if (selectedLanguage === 'ur') text = row.UrduDescription;
  else if (selectedLanguage === 'ro') text = row.RUrduDescription;
  else if (selectedLanguage === 'gu') text = row.GujaratiDescription;
  else text = row.EnglishDescription;
  return text ? text.trim() : '';
}

onMounted(async () => {
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', handleKeydown)
  window.addEventListener('resize', handleResize)
  document.addEventListener('fullscreenchange', handleFullscreenChange)

  const id = route.params.id;
  try {
    const results = await fetchLines(id);

    lines.value = results.map(row => ({
      arabic: buildArabicText(row),
      translation: getTranslationText(row),
      transliteration: getTransliterationText(row),
      description: getDescriptionText(row)
    })).filter(line => line.arabic || line.translation || line.transliteration || line.description);

    await nextTick();
    applySizes();
  } catch (error) {
    console.error('Error fetching lines for presenter:', error);
  }
})

onUnmounted(() => {
  document.body.style.overflow = ''
  window.removeEventListener('keydown', handleKeydown)
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('fullscreenchange', handleFullscreenChange)
  if (document.fullscreenElement) {
    document.exitFullscreen().catch(err => console.log(err));
  }
})
</script>

<style scoped>
/* ========== PRESENTER THEME ========== */
.presenter-theme {
  --gold: #c8a951;
  --gold-light: #f5d680;
  --cream: #f5e6c8;
  --cream-dim: #a89070;
  --bg-dark: #0d0a06;
  --bg-warm: #1a1008;
  --bar-bg: rgba(26, 15, 10, 0.95);
  --border-subtle: rgba(200, 169, 81, 0.15);


  background: var(--bg-dark);
  color: var(--cream);
  font-family: 'Roboto', sans-serif;
}

/* Top Bar */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: var(--bar-bg);
  border-bottom: 1px solid var(--border-subtle);
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  opacity: 0;
  transform: translateY(-100%);
  transition: all 0.3s ease;
}
.presenter-theme:hover .top-bar, .top-bar:focus-within {
  opacity: 1;
  transform: translateY(0);
}

.top-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  background: none;
  border: 1px solid var(--border-subtle);
  color: var(--cream-dim);
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}
.back-btn:hover {
  color: var(--gold-light);
  border-color: var(--gold);
  background: rgba(200, 169, 81, 0.1);
}

.slide-counter {
  color: var(--gold);
  font-family: monospace;
  font-size: 1.1rem;
  letter-spacing: 2px;
}

.icon-btn {
  background: none;
  border: 1px solid var(--border-subtle);
  color: var(--cream-dim);
  padding: 6px 14px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 36px;
  width: 48px;
  transition: all 0.2s;
}
.icon-btn:hover, .icon-btn:focus {
  color: var(--gold-light);
  border-color: var(--gold);
  background: rgba(200, 169, 81, 0.1);
  outline: none;
}
.icon-btn svg {
  width: 20px;
  height: 20px;
}

/* Slide Area */
.slide-area {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px 5% 40px 5%;
  position: relative;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
}

.slide-content {
  width: 100%;
  max-width: 90%;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  text-align: center;
  transition: opacity 0.15s ease-in-out;
  opacity: 1;
}

.slide-content.fading {
  opacity: 0;
}

.description-text {
  font-size: var(--trans-size);
  line-height: 1.8;
  color: var(--cream-dim);
  max-width: 90%;
  margin: 0 auto;
  font-style: italic;
  opacity: 0.8;
}

.arabic-text {
  font-size: var(--arabic-size);
  color: var(--cream);
  line-height: 1.6;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
  letter-spacing: 0;
}

.translation-text {
  font-size: var(--trans-size);
  line-height: 1.8;
  color: var(--gold);
  max-width: 90%;
  margin: 0 auto;
}

.translit-text {
  font-size: var(--translit-size);
  line-height: 1.6;
  color: var(--cream-dim);
  max-width: 85%;
  margin: 0 auto;
  font-style: italic;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 3px solid var(--border-subtle);
  border-top-color: var(--gold);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
@keyframes spin { 100% { transform: rotate(360deg); } }

/* Progress Bar */
.progress-bar-container {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 16px;
  padding-bottom: 8px;
  cursor: pointer;
  z-index: 10;
  background: transparent;
}

.progress-bar {
  height: 4px;
  background: var(--bg-warm);
  width: 100%;
  transition: height 0.2s;
  position: absolute;
  bottom: 0;
}

.progress-bar-container:hover .progress-bar {
  height: 8px;
}

.progress-fill {
  height: 100%;
  background: var(--gold);
  transition: width 0.3s ease;
  box-shadow: 0 0 10px rgba(200, 169, 81, 0.5);
}

/* Shortcuts Overlay */
.shortcuts-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.shortcuts-panel {
  background: var(--bar-bg);
  border: 1px solid var(--border-subtle);
  border-radius: 12px;
  padding: 32px;
  width: 100%;
  max-width: 450px;
  cursor: default;
  color: var(--cream);
  box-shadow: 0 10px 40px rgba(0,0,0,0.8);
}

/* Global Reset overrides for Presenter */
</style>
