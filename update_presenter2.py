import re

with open('src/views/PresenterView.vue', 'r') as f:
    content = f.read()

# 1. Add inline styles to root div
content = content.replace(
    '<div class="presenter-theme h-screen w-screen overflow-hidden flex flex-col fixed top-0 left-0 z-[100]">',
    '''<div class="presenter-theme h-screen w-screen overflow-hidden flex flex-col fixed top-0 left-0 z-[100]"
       :style="{
         '--arabic-size': currentArabicSize + 'rem',
         '--trans-size': currentTransSize + 'rem',
         '--translit-size': currentTranslitSize + 'rem'
       }">'''
)

# 2. Add Fonts section to the dropdown
fonts_html = '''
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
'''

content = content.replace(
    '<li class="menu-title" style="color: var(--gold); padding-left: 0.5rem;"><span>Elements</span></li>',
    fonts_html + '\n            <li class="menu-title" style="color: var(--gold); padding-left: 0.5rem;"><span>Elements</span></li>'
)

# 3. Update the script setup logic for dynamic fontConfig and size refs
script_find = '''const isRtl = selectedLanguage === 'ur'
const fontConfig = getFontConfig(selectedLanguage)

// Display settings with persistence'''

script_replace = '''const isRtl = selectedLanguage === 'ur'

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

// Display settings with persistence'''

content = content.replace(script_find, script_replace)

# 4. Update applySizes
apply_sizes_find = '''const applySizes = async () => {
  await nextTick()
  const area = slideAreaRef.value;
  const content = slideContentRef.value;
  if (!area || !content) return;

  // Set to base sizes
  document.documentElement.style.setProperty('--arabic-size', baseArabicSize.value + 'rem');
  document.documentElement.style.setProperty('--trans-size', baseTransSize.value + 'rem');
  document.documentElement.style.setProperty('--translit-size', (baseTransSize.value * 0.75) + 'rem');

  if (!autoFit.value) return;

  await nextTick()

  const maxH = area.clientHeight * 0.88;
  if (content.scrollHeight <= maxH) return;

  let scale = maxH / content.scrollHeight;
  scale = Math.max(scale, 0.4); // don't go below 40%

  document.documentElement.style.setProperty('--arabic-size', (baseArabicSize.value * scale) + 'rem');
  document.documentElement.style.setProperty('--trans-size', (baseTransSize.value * scale) + 'rem');
  document.documentElement.style.setProperty('--translit-size', (baseTransSize.value * 0.75 * scale) + 'rem');
}'''

apply_sizes_replace = '''const applySizes = async () => {
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
}'''

content = content.replace(apply_sizes_find, apply_sizes_replace)

with open('src/views/PresenterView.vue', 'w') as f:
    f.write(content)
