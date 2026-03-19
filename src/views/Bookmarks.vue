<template>
  <div class="container mx-auto p-4 max-w-4xl pb-24">
    <h1 class="text-3xl font-bold mb-6">Bookmarks</h1>

    <div v-if="bookmarks.length === 0" class="text-center py-20">
      <div class="inline-flex justify-center items-center w-24 h-24 rounded-full bg-base-200 mb-6 text-base-content/30">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="currentColor" viewBox="0 0 24 24" stroke="none"><path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>
      </div>
      <h2 class="text-xl font-medium mb-2">No bookmarks yet</h2>
      <p class="text-base-content/60">Your saved Duas and Ziyarats will appear here.</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="sub in bookmarkedItems"
        :key="sub.Id"
        class="card bg-base-100 shadow border border-base-200 cursor-pointer hover:shadow-md transition-shadow"
        @click="goToBookmark(sub)"
      >
        <div class="card-body p-6 flex flex-row justify-between items-center">
          <h2 class="card-title text-xl font-normal">{{ getLanguageName(sub) }}</h2>
          <button @click.stop="removeBookmark(sub.Id)" class="btn btn-ghost btn-circle text-error" title="Remove Bookmark">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchBookmarkItems } from '../services/api'

const router = useRouter()
const bookmarks = ref([])
const bookmarkedItems = ref([])
const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'

const getLanguageName = (sub) => {
  if (selectedLanguage === 'ur') return sub.UrduIndexName || sub.EnglishIndexName;
  if (selectedLanguage === 'ro') return sub.RUrduIndexName || sub.EnglishIndexName;
  if (selectedLanguage === 'gu') return sub.GujaratiIndexName || sub.EnglishIndexName;
  return sub.EnglishIndexName;
}

const loadBookmarks = async () => {
  const saved = localStorage.getItem('bookmarks')
  if (saved) {
    try {
      bookmarks.value = JSON.parse(saved)
      if (bookmarks.value.length > 0) {
        // Query the static API to get the names for these subindex IDs
        bookmarkedItems.value = await fetchBookmarkItems(bookmarks.value)
      } else {
        bookmarkedItems.value = []
      }
    } catch (e) {
      console.error('Failed to load bookmarks:', e)
      bookmarks.value = []
      bookmarkedItems.value = []
    }
  }
}

onMounted(() => {
  loadBookmarks()
})

const goToBookmark = (sub) => {
  router.push({ path: `/lines/${sub.Id}`, query: { title: getLanguageName(sub) } })
}

const removeBookmark = (id) => {
  bookmarks.value = bookmarks.value.filter(b => b !== id)
  localStorage.setItem('bookmarks', JSON.stringify(bookmarks.value))
  loadBookmarks() // Reload the list
}
</script>
