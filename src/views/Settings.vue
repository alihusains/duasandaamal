<template>
  <div class="container mx-auto p-4 max-w-md mt-10 pb-24">
    <h1 class="text-3xl font-bold mb-6 text-center">Settings</h1>

    <!-- Theme Settings -->
    <div class="card bg-base-100 shadow-xl border border-base-200 mb-6">
      <div class="card-body">
        <h2 class="card-title text-xl mb-4">App Theme</h2>

        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="theme" value="light" v-model="currentTheme" class="radio radio-primary" />
            <span class="label-text text-lg">Light</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="theme" value="dark" v-model="currentTheme" class="radio radio-primary" />
            <span class="label-text text-lg">Dark</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="theme" value="duasandaamal" v-model="currentTheme" class="radio radio-primary" />
            <span class="label-text text-lg">Duas and Aamal</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="theme" value="divinepearls" v-model="currentTheme" class="radio radio-primary" />
            <span class="label-text text-lg">Divine Pearls</span>
          </label>
        </div>
      </div>
    </div>

    <!-- App Language -->
    <div class="card bg-base-100 shadow-xl border border-base-200 mb-6">
      <div class="card-body">
        <h2 class="card-title text-xl mb-4">App Language</h2>

        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="language" value="en" v-model="selectedLanguage" class="radio radio-primary" />
            <span class="label-text text-lg">English</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="language" value="ur" v-model="selectedLanguage" class="radio radio-primary" />
            <span class="label-text text-lg">Urdu</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="language" value="ro" v-model="selectedLanguage" class="radio radio-primary" />
            <span class="label-text text-lg">Roman Urdu</span>
          </label>
        </div>
        <div class="form-control">
          <label class="label cursor-pointer justify-start gap-4">
            <input type="radio" name="language" value="gu" v-model="selectedLanguage" class="radio radio-primary" />
            <span class="label-text text-lg">Gujarati</span>
          </label>
        </div>
      </div>
    </div>

    <div class="card bg-base-100 shadow-xl border border-base-200 mb-6">
      <div class="card-body">
        <h2 class="card-title text-xl mb-4">Font Settings</h2>

        <div class="form-control w-full max-w-xs mb-4">
          <label class="label">
            <span class="label-text font-bold text-lg">Arabic Font</span>
          </label>
          <select v-model="arabicFont" class="select select-bordered w-full">
            <option value="Al-Qalam">Al-Qalam</option>
            <option value="ShiaEssentials">ShiaEssentials</option>
          </select>
        </div>

        <div class="form-control w-full max-w-xs mb-4">
          <label class="label">
            <span class="label-text font-bold text-lg">English Font</span>
          </label>
          <select v-model="englishFont" class="select select-bordered w-full">
            <option value="RobotoFlex">RobotoFlex</option>
            <option value="NotoSans">NotoSans</option>
          </select>
        </div>

        <div class="form-control w-full max-w-xs">
          <label class="label">
            <span class="label-text font-bold text-lg">Urdu Font</span>
          </label>
          <select v-model="urduFont" class="select select-bordered w-full">
            <option value="NotoNastaliqUrdu">NotoNastaliqUrdu</option>
            <option value="NotoSans">NotoSans</option>
          </select>
        </div>
      </div>
    </div>

    <div class="flex justify-end mt-8">
      <button @click="saveSettings" class="btn btn-primary px-8 btn-lg">Save Settings</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { currentTheme } from '../theme.js'

const selectedLanguage = ref(localStorage.getItem('selectedLanguage') || 'en')
const arabicFont = ref(localStorage.getItem('arabicFont') || 'Al-Qalam')
const englishFont = ref(localStorage.getItem('englishFont') || 'RobotoFlex')
const urduFont = ref(localStorage.getItem('urduFont') || 'NotoNastaliqUrdu')

const saveSettings = () => {
  localStorage.setItem('selectedLanguage', selectedLanguage.value)
  localStorage.setItem('arabicFont', arabicFont.value)
  localStorage.setItem('englishFont', englishFont.value)
  localStorage.setItem('urduFont', urduFont.value)

  window.location.hash = '#/categories'
  window.location.reload()
}
</script>
