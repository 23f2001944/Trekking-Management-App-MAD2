<template>
    <span class="badge" :class="badgeClass">{{ status }}</span>
</template>

<script>
    const STATUS_COLORS = {
        Pending: 'bg-secondary',
        Approved: 'bg-info text-dark',
        Open: 'bg-success',
        Closed: 'bg-danger',
        Completed: 'bg-primary',
        
        Booked: 'bg-success',
        Cancelled: 'bg-danger',

        Active: 'bg-success',
        Blacklisted: 'bg-danger'
    }

    export default {
        name: 'StatusBadge',
        props: {
            status: { type: String, required: true }
        },
        computed: {
            badgeClass() {
            return STATUS_COLORS[this.status] || 'bg-secondary'
            }
        }
    }
</script>