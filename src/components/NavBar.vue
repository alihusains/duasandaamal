<template>
  <div class="navbar bg-base-100 shadow-sm mb-4 px-4 sticky top-0 z-50">
    <div class="flex-none">
      <button v-if="!isHome" @click="goBack" class="btn btn-square btn-ghost">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-6 h-6 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
      </button>
    </div>
    <div class="flex-1">
      <router-link to="/categories" class="btn btn-ghost normal-case text-xl font-bold p-0 ml-2">
        <img :src="logoUrl" alt="Duas And Aamal" class="h-10 w-auto" />
      </router-link>
    </div>
    <div class="flex-none">
      <div class="form-control relative">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search..."
          class="input input-bordered input-sm w-32 sm:w-64"
        />

        <!-- Search Results Dropdown -->
        <ul v-if="searchResults.length > 0" class="absolute top-10 right-0 menu bg-base-100 w-72 shadow-xl rounded-box z-[100] max-h-96 flex-nowrap overflow-y-auto border border-base-200">
          <li v-for="(result, index) in searchResults" :key="index">
            <a @click="goToResult(result.SubindexId)">
              <div class="flex flex-col gap-1 w-full overflow-hidden">
                <span class="text-sm truncate text-base-content/80 w-full block">{{ getTranslation(result) }}</span>
              </div>
            </a>
          </li>
        </ul>
        <ul v-else-if="searchQuery && hasSearched" class="absolute top-10 right-0 menu bg-base-100 w-72 shadow-xl rounded-box z-[100] border border-base-200">
          <li class="disabled"><span class="py-4 text-center">No results found</span></li>
        </ul>
      </div>
      <!-- Bookmarks Icon -->
      <router-link to="/bookmarks" class="btn btn-ghost btn-circle ml-1" title="Bookmarks">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
      </router-link>

      <!-- Settings Icon -->
      <router-link to="/settings" class="btn btn-ghost btn-circle" title="Settings">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { searchGlobal } from '../services/api'
import logoUrl from '../assets/logo.png'

const router = useRouter()
const route = useRoute()

const isHome = computed(() => route.path === '/' || route.path === '/categories')
const searchQuery = ref('')
const searchResults = ref([])
const hasSearched = ref(false)

let searchTimeout = null

const handleSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)

  if (!searchQuery.value.trim()) {
    searchResults.value = []
    hasSearched.value = false
    return
  }

  searchTimeout = setTimeout(() => {
    performSearch()
  }, 300)
}

const performSearch = async () => {
  const term = searchQuery.value.trim();
  const lang = localStorage.getItem('selectedLanguage') || 'en';
  try {
    const results = await searchGlobal(term, lang);
    searchResults.value = results;
    hasSearched.value = true;
  } catch (error) {
    console.error('Search failed:', error)
    searchResults.value = []
  }
}

const getTranslation = (result) => {
  const lang = localStorage.getItem('selectedLanguage') || 'en'
  if (lang === 'ur') return result.UrduTitle || result.EnglishTitle
  if (lang === 'ro') return result.RUrduTitle || result.EnglishTitle
  if (lang === 'gu') return result.GujaratiTitle || result.EnglishTitle
  return result.EnglishTitle
}

const goToResult = (subindexId) => {
  searchQuery.value = ''
  searchResults.value = []
  hasSearched.value = false
  router.push(`/lines/${subindexId}`)
}

const goBack = () => {
  router.back()
}
</script>
