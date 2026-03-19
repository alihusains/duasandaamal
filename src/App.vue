<template>
  <NavBar v-if="showNavBar" />
  <router-view></router-view>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from './components/NavBar.vue'

const route = useRoute()
const showNavBar = computed(() => route.path !== '/')
</script>

<style>
/* Global styles */
</style>
