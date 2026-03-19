<template>
  <NavBar v-if="showNavBar" />

  <!-- Breadcrumbs -->
  <div v-if="showNavBar && breadcrumbs.length > 1" class="px-4 py-2 bg-base-200/50">
    <div class="text-sm breadcrumbs">
      <ul>
        <li v-for="(crumb, index) in breadcrumbs" :key="index">
          <router-link :to="crumb.path" v-if="index < breadcrumbs.length - 1">
            {{ crumb.title }}
          </router-link>
          <span v-else class="font-bold text-primary">{{ crumb.title }}</span>
        </li>
      </ul>
    </div>
  </div>

  <router-view></router-view>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'
import { breadcrumbs } from './store'

const route = useRoute()
const showNavBar = computed(() => route.path !== '/')
</script>

<style>
/* Global styles */
</style>
