<template>
  <div class="container mx-auto p-4">
    <div v-if="loading" class="flex flex-col items-center justify-center py-20 min-h-[50vh]">
      <span class="loading loading-spinner loading-lg text-primary"></span>
      <p class="mt-4 text-lg font-medium text-base-content/80">{{ loadingMessage }}</p>
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="cat in categories"
        :key="cat.Id"
        @click="goToSubindex(cat.Id)"
        class="card bg-base-100 shadow hover:shadow-xl transition-all cursor-pointer border border-base-200"
      >
        <div class="card-body p-6 items-center text-center">
          <h2 class="card-title text-2xl">{{ getLanguageName(cat) }}</h2>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { fetchCategories } from '../services/api'

const router = useRouter()
const categories = ref([])
const loading = ref(true)
const loadingMessage = ref('Loading categories...')
const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'

const getLanguageName = (category) => {
  if (selectedLanguage === 'ur') return category.UrduName || category.EnglishName;
  if (selectedLanguage === 'ro') return category.RUrduName || category.EnglishName;
  if (selectedLanguage === 'gu') return category.GujaratiName || category.EnglishName;
  return category.EnglishName;
}

const goToSubindex = (id) => {
  router.push(`/category/${id}`)
}

onMounted(async () => {
  try {
    const results = await fetchCategories();
    categories.value = results;
  } catch (error) {
    console.error('Failed to load categories', error);
    loadingMessage.value = 'Error loading content';
  } finally {
    loading.value = false;
  }
})
</script>
