<template>
  <div class="card h-100 shadow-sm">
    <div
      class="card-img-top bg-primary bg-opacity-10 d-flex align-items-center justify-content-center"
      style="height: 140px;"
    >
      <i class="bi bi-image text-primary" style="font-size: 2.5rem;"></i>
    </div>
    <div class="card-body d-flex flex-column">
      <h5 class="card-title mb-1">{{ trek.name }}</h5>
      <p class="text-muted mb-2"><i class="bi bi-geo-alt"></i> {{ trek.location }}</p>
      <p class="mb-1">{{ trek.difficulty }} &bull; {{ trek.duration }} Days</p>
      <p class="mb-3" :class="trek.available_slots > 0 ? 'text-success' : 'text-danger'">
        Slots Left: {{ trek.available_slots }}
      </p>
      <button
        class="btn mt-auto"
        :class="disabled ? 'btn-outline-secondary' : 'btn-primary'"
        :disabled="disabled"
        @click="$emit('action', trek)"
      >
        {{ actionLabel }}
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TrekCard',
  props: {
    trek: { type: Object, required: true },
    actionLabel: { type: String, default: 'View Details' },
    disabled: { type: Boolean, default: false }
  }
}
</script>