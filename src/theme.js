import { ref, watch } from 'vue'

export const currentTheme = ref(localStorage.getItem('appTheme') || 'divinepearls')

export function initTheme() {
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  watch(currentTheme, (newTheme) => {
    localStorage.setItem('appTheme', newTheme)
    document.documentElement.setAttribute('data-theme', newTheme)
  })
}
