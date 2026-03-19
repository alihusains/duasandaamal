<template>
  <div class="container mx-auto p-4">
    <div v-if="loading" class="flex justify-center py-20">
      <span class="loading loading-spinner loading-lg text-primary"></span>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="sub in subcategories"
        :key="sub.Id"
        @click="handleSubcategoryClick(sub)"
        class="card bg-base-100 shadow hover:shadow-xl transition-all cursor-pointer border border-base-200"
      >
        <div class="card-body p-6">
          <h2 class="card-title text-xl mb-2">{{ getLanguageName(sub) }}</h2>
          <p class="text-sm text-base-content/60">{{ sub.EnglishIndexName }}</p>
        </div>
      </div>
    </div>

    <div v-if="!loading && subcategories.length === 0" class="text-center py-10">
      <p class="text-base-content/60">No items found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchCategoryItems, fetchSubindexItems, fetchItemById } from '../services/api'
import { setBreadcrumbs } from '../store'

const router = useRouter()
const route = useRoute()

const subcategories = ref([])
const loading = ref(true)
const selectedLanguage = localStorage.getItem('selectedLanguage') || 'en'

const getLanguageName = (sub) => {
  if (selectedLanguage === 'ur') return sub.UrduIndexName || sub.EnglishIndexName;
  if (selectedLanguage === 'ro') return sub.RUrduIndexName || sub.EnglishIndexName;
  if (selectedLanguage === 'gu') return sub.GujaratiIndexName || sub.EnglishIndexName;
  return sub.EnglishIndexName;
}

const getLanguageTitle = (item) => {
  if (selectedLanguage === 'ur') return item.UrduTitle || item.EnglishTitle;
  if (selectedLanguage === 'ro') return item.RUrduTitle || item.EnglishTitle;
  if (selectedLanguage === 'gu') return item.GujaratiTitle || item.EnglishTitle;
  return item.EnglishTitle;
}

const updateBreadcrumbs = async (title) => {
  const crumbs = [
    { title: 'Home', path: '/categories' }
  ]

  let displayTitle = title;
  if (!displayTitle) {
    const item = await fetchItemById(route.params.id);
    if (item) {
      displayTitle = getLanguageTitle(item);
    }
  }

  if (displayTitle) {
    crumbs.push({ title: displayTitle, path: route.fullPath })
  }
  setBreadcrumbs(crumbs)
}

const fetchSubcategories = async () => {
  loading.value = true;
  const id = route.params.id;
  const isSubcategory = route.query.type === 'subindex';
  const titleFromQuery = route.query.title;

  updateBreadcrumbs(titleFromQuery)

  try {
    if (isSubcategory) {
      subcategories.value = await fetchSubindexItems(id);
    } else {
      subcategories.value = await fetchCategoryItems(id);
    }
  } catch (error) {
    console.error('Error fetching subcategories:', error);
    subcategories.value = [];
  } finally {
    loading.value = false;
  }
}

const handleSubcategoryClick = (sub) => {
  if (sub.HasChildren) {
    router.push({ path: `/category/${sub.Id}`, query: { type: 'subindex' } });
  } else {
    router.push({ path: `/lines/${sub.Id}`, query: { title: getLanguageName(sub) } });
  }
}

onMounted(() => {
  fetchSubcategories()
})

// Re-fetch when route changes (e.g. navigating deeper)
watch(() => route.params.id, () => {
  fetchSubcategories()
})
</script>
