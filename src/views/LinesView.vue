<template>
  <!-- Full page background with Islamic Theme -->
  <div class="min-h-screen bg-[#0d0a06] text-[#f5e6c8]">
    <!-- Responsive Container -->
    <div class="mx-auto w-[95%] sm:w-[90%] max-w-5xl py-8 pb-24">
      <!-- Header -->
      <div class="flex justify-between items-start mb-8 bg-[#1a1008] p-6 rounded-2xl shadow-sm border border-[#c8a951]/20">
        <div>
          <h1 class="text-3xl font-bold text-[#c8a951] mb-2">{{ title || (loading ? 'Loading...' : 'Details') }}</h1>
        </div>
        <div class="flex gap-3">
          <button @click="toggleBookmark" class="btn btn-circle bg-transparent border-[#c8a951]/30 text-[#a89070] hover:border-[#c8a951] hover:bg-[#c8a951]/10 hover:text-[#c8a951] transition-colors" :class="{'text-[#c8a951] border-[#c8a951] bg-[#c8a951]/10': isBookmarked}" title="Toggle Bookmark">
            <svg v-if="!isBookmarked" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" /></svg>
          </button>
          <button @click="openPresenter" class="btn bg-[#c8a951] text-[#0d0a06] border-none hover:bg-[#f5d680] gap-2 shadow-md" :disabled="lines.length === 0">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
            Present
          </button>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center py-20">
        <span class="loading loading-spinner loading-lg text-[#c8a951]"></span>
      </div>

      <!-- Content -->
      <div v-else class="space-y-6">
        <div
          v-for="(line, index) in lines"
          :key="index"
        >
          <!-- Description Block (if present) -->
          <div v-if="line.description" class="bg-[#1a1008] text-[#a89070] p-6 rounded-2xl mb-6 shadow-inner border border-[#c8a951]/10" :dir="isRtl ? 'rtl' : 'ltr'">
            <p class="text-lg leading-relaxed font-medium" :style="{ fontFamily: fontConfig.translation }">
              {{ line.description }}
            </p>
          </div>

          <!-- Line Content Block -->
          <div v-if="line.arabic || line.translation || line.transliteration" class="card bg-[#1a1008] shadow-md border border-[#c8a951]/20 hover:shadow-lg hover:border-[#c8a951]/50 transition-all duration-300 relative overflow-hidden">

            <!-- Decorative Numbering -->
            <div class="absolute top-4 left-4 w-9 h-9 flex items-center justify-center rounded-full border border-[#c8a951]/40 bg-[#0d0a06] text-[#c8a951] font-semibold text-sm shadow-sm z-10">
              {{ index + 1 }}
            </div>

            <div class="card-body p-6 sm:p-10 pt-12 sm:pt-10">
              <p v-if="line.arabic" class="text-3xl sm:text-4xl text-right mb-6 leading-loose font-arabic text-[#f5e6c8]" :style="{ fontFamily: fontConfig.arabic, letterSpacing: '0' }" dir="rtl">
                {{ line.arabic }}
              </p>
              <div class="divider before:bg-[#c8a951]/20 after:bg-[#c8a951]/20" v-if="line.arabic && (line.translation || line.transliteration)"></div>
              <p v-if="line.translation" class="text-xl sm:text-2xl font-medium mb-4 font-translation text-[#c8a951] mt-2" :style="{ fontFamily: fontConfig.translation }" :dir="isRtl ? 'rtl' : 'ltr'">
                {{ line.translation }}
              </p>
              <p v-if="line.transliteration" class="text-lg text-[#a89070] font-transliteration italic" :style="{ fontFamily: fontConfig.transliteration }">
                {{ line.transliteration }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="!loading && lines.length === 0" class="text-center py-20 bg-[#1a1008] rounded-2xl border border-[#c8a951]/20 border-dashed">
        <p class="text-lg text-[#a89070]">No content found.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchLines } from '../services/api'
import { getFontConfig } from '../services/fonts'

const router = useRouter()
const route = useRoute()

const lines = ref([])
const title = ref('')
const loading = ref(true)
const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'
const isRtl = selectedLanguage === 'ur'
const fontConfig = getFontConfig(selectedLanguage)

const isBookmarked = ref(false)

const openPresenter = () => {
  router.push(`/presenter/${route.params.id}`)
}

const toggleBookmark = () => {
  const id = parseInt(route.params.id)
  let bookmarks = []
  try {
    bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
  } catch (e) {}

  if (isBookmarked.value) {
    bookmarks = bookmarks.filter(b => b !== id)
  } else {
    if (!bookmarks.includes(id)) bookmarks.push(id)
  }

  localStorage.setItem('bookmarks', JSON.stringify(bookmarks))
  isBookmarked.value = !isBookmarked.value
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
  const id = parseInt(route.params.id);

  try {
    const bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '[]')
    isBookmarked.value = bookmarks.includes(id)
  } catch (e) {}

  try {
    const results = await fetchLines(id);

    lines.value = results.map(row => ({
      arabic: buildArabicText(row),
      translation: getTranslationText(row),
      transliteration: getTransliterationText(row),
      description: getDescriptionText(row)
    })).filter(line => line.arabic || line.translation || line.transliteration || line.description);

    if (results.length > 0) {
      if (selectedLanguage === 'ur') title.value = results[0].UrduTitle || results[0].EnglishTitle;
      else if (selectedLanguage === 'ro') title.value = results[0].RUrduTitle || results[0].EnglishTitle;
      else title.value = results[0].EnglishTitle;
    }
  } catch (error) {
    console.error('Error fetching lines:', error);
  } finally {
    loading.value = false;
  }
})
</script>
