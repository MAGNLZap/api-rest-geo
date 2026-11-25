<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps<{ value: number }>()
const formatted = computed(() => props.value.toLocaleString('es-EC'))
const visible = ref(formatted.value)
let frame = 0
let preference: MediaQueryList | undefined
let mounted = false

function settle() {
  cancelAnimationFrame(frame)
  frame = 0
  visible.value = formatted.value
}
function animate() {
  settle()
  if (!mounted || preference?.matches || props.value === 0) return
  const started = performance.now()
  const target = formatted.value
  let previousTick = -1
  function update(now: number) {
    const elapsed = now - started
    if (elapsed >= 480) { settle(); return }
    const tick = Math.floor(elapsed / 60)
    if (tick !== previousTick) {
      visible.value = target.replace(/\d/g, () => String(Math.floor(Math.random() * 10)))
      previousTick = tick
    }
    frame = requestAnimationFrame(update)
  }
  frame = requestAnimationFrame(update)
}
function preferenceChanged() { if (preference?.matches) settle() }
watch(() => props.value, animate, { flush: 'sync' })
onMounted(() => {
  mounted = true
  preference = window.matchMedia('(prefers-reduced-motion: reduce)')
  preference.addEventListener('change', preferenceChanged)
  animate()
})
onBeforeUnmount(() => {
  mounted = false
  cancelAnimationFrame(frame)
  preference?.removeEventListener('change', preferenceChanged)
})
</script>

<template>
  <span class="animated-number"><span class="animated-number-accessible">{{ formatted }}</span><span aria-hidden="true">{{ visible }}</span></span>
</template>

<style scoped>
.animated-number{display:inline-block;font-variant-numeric:tabular-nums;white-space:nowrap}
.animated-number-accessible{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap;border:0}
</style>
