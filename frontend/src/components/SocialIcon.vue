<script setup lang="ts">
import { computed } from 'vue'
import { Icon, type IconifyIcon } from '@iconify/vue'
import home from '@iconify-icons/mdi/home-outline'
import child from '@iconify-icons/mdi/human-child'
import senior from '@iconify-icons/mdi/human-cane'
import sun from '@iconify-icons/mdi/weather-sunny'
import access from '@iconify-icons/el/wheelchair'
import family from '@iconify-icons/mdi/human-male-female-child'
import shield from '@iconify-icons/mdi/shield-account-outline'
import compass from '@iconify-icons/mdi/compass-outline'
import pin from '@iconify-icons/mdi/map-marker-outline'
import chevronRight from '@iconify-icons/mdi/chevron-right'
import chevronLeft from '@iconify-icons/mdi/chevron-left'
import chevronDown from '@iconify-icons/mdi/chevron-down'
import search from '@iconify-icons/mdi/magnify'
import locate from '@iconify-icons/mdi/crosshairs-gps'
import list from '@iconify-icons/mdi/format-list-bulleted'
import map from '@iconify-icons/mdi/map-outline'
import close from '@iconify-icons/mdi/close'
import check from '@iconify-icons/mdi/check'
import external from '@iconify-icons/mdi/open-in-new'
import homeHeart from '@iconify-icons/mdi/home-heart'
import heart from '@iconify-icons/mdi/heart-outline'
import wallet from '@iconify-icons/mdi/wallet-outline'
import coins from '@iconify-icons/mdi/cash-multiple'
import lifebuoy from '@iconify-icons/mdi/lifebuoy'
import graduation from '@iconify-icons/mdi/school-outline'
import briefcase from '@iconify-icons/mdi/briefcase-outline'
import handHeart from '@iconify-icons/mdi/hand-heart-outline'
import badge from '@iconify-icons/mdi/badge-account-outline'
import message from '@iconify-icons/mdi/message-text-outline'
import community from '@iconify-icons/mdi/account-group-outline'
import clipboard from '@iconify-icons/mdi/clipboard-check-outline'
import grid from '@iconify-icons/mdi/view-grid-outline'
import edit from '@iconify-icons/mdi/pencil-outline'
import reset from '@iconify-icons/mdi/restore'
import clear from '@iconify-icons/mdi/eraser'
import refresh from '@iconify-icons/mdi/refresh'
import info from '@iconify-icons/mdi/information-outline'
import filters from '@iconify-icons/mdi/tune-variant'
import download from '@iconify-icons/mdi/tray-arrow-down'
import polygon from '@iconify-icons/mdi/vector-polygon'
import help from '@iconify-icons/mdi/help-circle-outline'

const props = withDefaults(defineProps<{ name: string; size?: number }>(), { size: 24 })
const icons: Record<string, IconifyIcon> = {
  home, child, senior, sun, access, family, shield, compass, pin,
  'chevron-right': chevronRight,
  'chevron-left': chevronLeft,
  'chevron-down': chevronDown,
  search, locate, list, map, close, check, external,
  nursery: homeHeart,
  heart,
  'heart-home': homeHeart,
  wallet, coins, lifebuoy, graduation, briefcase,
  'hand-heart': handHeart,
  badge, message, community, clipboard, grid, edit, reset, clear, refresh, info,
  filters, download, polygon, help,
}
const icon = computed(() => icons[props.name] || help)
</script>

<template>
  <Icon :icon="icon" :width="size" :height="size" :ssr="true" class="app-icon" aria-hidden="true" focusable="false" />
</template>

<style scoped>
.app-icon{display:inline-block;flex-shrink:0;vertical-align:middle}
</style>
