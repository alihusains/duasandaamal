import { createRouter, createWebHashHistory } from 'vue-router'
import LanguageSelection from './views/LanguageSelection.vue'
import Categories from './views/Categories.vue'
import Subcategories from './views/Subcategories.vue'
import LinesView from './views/LinesView.vue'
import PresenterView from './views/PresenterView.vue'
import Settings from './views/Settings.vue'
import Bookmarks from './views/Bookmarks.vue'

const routes = [
  {
    path: '/',
    name: 'LanguageSelection',
    component: LanguageSelection,
    beforeEnter: (to, from, next) => {
      const selectedLanguage = localStorage.getItem('selectedLanguage')
      if (selectedLanguage) {
        next('/categories')
      } else {
        next()
      }
    }
  },
  {
    path: '/categories',
    name: 'Categories',
    component: Categories
  },
  {
    path: '/category/:id',
    name: 'Subcategories',
    component: Subcategories,
    props: route => ({ type: route.query.type || 'category' })
  },
  {
    path: '/lines/:id',
    name: 'LinesView',
    component: LinesView
  },
  {
    path: '/presenter/:id',
    name: 'PresenterView',
    component: PresenterView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/bookmarks',
    name: 'Bookmarks',
    component: Bookmarks
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
