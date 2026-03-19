import { ref } from 'vue'

// A global stack for breadcrumbs: [{ title: 'Home', path: '/categories' }, ...]
export const breadcrumbs = ref([
  { title: 'Home', path: '/categories' }
])

export const setBreadcrumbs = (crumbs) => {
  breadcrumbs.value = crumbs
}
