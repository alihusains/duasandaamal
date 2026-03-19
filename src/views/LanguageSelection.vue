<template>
  <div class="min-h-screen flex items-center justify-center bg-base-200 p-4">
    <div class="card w-full max-w-sm bg-base-100 shadow-xl">
      <div class="card-body items-center text-center">
        <h2 class="card-title text-2xl font-bold mb-6">Select Language</h2>
        <div class="flex flex-col gap-4 w-full">
          <button class="btn btn-primary w-full" @click="selectLanguage('en')">English</button>
          <button class="btn btn-secondary w-full" @click="selectLanguage('ur')">Urdu</button>
          <button class="btn btn-accent w-full" @click="selectLanguage('ro')">Roman Urdu</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const selectLanguage = (lang) => {
  localStorage.setItem('selectedLanguage', lang)
  router.push('/categories')
}
</script>
