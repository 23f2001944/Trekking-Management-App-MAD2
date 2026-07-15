<template>
  <div class="card text-center shadow-sm">
    <div class="card-body">
      <i :class="icon" class="fs-2 text-primary"></i>
      <h3 class="mt-2 mb-0">{{ value }}</h3>
      <p class="text-muted mb-0">{{ label }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StatCard',
  props: {
    label: { type: String, required: true },
    value: { type: [Number, String], required: true },
    icon: { type: String, default: 'bi bi-bar-chart' }
  }
}
</script>