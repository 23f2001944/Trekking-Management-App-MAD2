<template>
  <div v-if="visible">
    <div class="modal d-block" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <form @submit.prevent="handleSubmit">
            <div class="modal-header">
              <h5 class="modal-title">
                {{ isEdit ? 'Edit Trek' : 'Add New Trek' }}
              </h5>
              <button type="button" class="btn-close" @click="$emit('close')"></button>
            </div>

            <div class="modal-body">
              <div v-if="error" class="alert alert-danger">{{ error }}</div>

              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label">Trek Name</label>
                  <input v-model="form.name" type="text" class="form-control" :disabled="isStaff" required>
                </div>
                <div class="col-md-6">
                  <label class="form-label">Location</label>
                  <input v-model="form.location" type="text" class="form-control" :disabled="isStaff" required>
                </div>

                <div class="col-md-4">
                  <label class="form-label">Difficulty</label>
                  <select v-model="form.difficulty" class="form-select" :disabled="isStaff" required>
                    <option value="" disabled>Select difficulty</option>
                    <option value="Easy">Easy</option>
                    <option value="Moderate">Moderate</option>
                    <option value="Hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Start Date</label>
                  <input v-model="form.start_date" type="date" class="form-control" :disabled="isStaff" required>
                </div>
                <div class="col-md-4">
                  <label class="form-label">End Date</label>
                  <input v-model="form.end_date" type="date" class="form-control" :disabled="isStaff" required>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Total Slots</label>
                  <input v-model.number="form.total_slots" type="number" min="1" class="form-control" required>
                </div>

                <div class="col-md-6">
                  <label class="form-label">Assigned Staff</label>
                  <select v-model="form.assigned_staff_id" class="form-select" :disabled="isStaff">
                    <option :value="null">-- Unassigned --</option>
                    <option v-for="staff in staffOptions" :key="staff.id" :value="staff.id">
                      {{ staff.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6" v-if="isEdit">
                  <label class="form-label">Status</label>
                  <select v-model="form.status" class="form-select">
                    <option v-for="s in statusOptions" :key="s" :value="s">{{ s }}</option>
                  </select>
                </div>

                <div class="col-12">
                  <label class="form-label">Description</label>
                  <textarea v-model="form.description" class="form-control" rows="3" :disabled="isStaff"></textarea>
                </div>
              </div>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="$emit('close')">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                {{ saving ? 'Saving...' : 'Save' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import api from '@/api/axios'

const STATUS_OPTIONS = ['Pending', 'Approved', 'Open', 'Closed', 'Completed']

export default {
  name: 'TrekFormModal',
  props: {
    visible: { type: Boolean, default: false },
    trek: { type: Object, default: null },       // null = create mode, object = edit mode
    role: { type: String, default: 'admin' },     // 'admin' | 'staff'
    staffOptions: { type: Array, default: () => [] }
  },
  emits: ['close', 'saved'],
  data() {
    return {
      form: this.emptyForm(),
      saving: false,
      error: null,
      statusOptions: STATUS_OPTIONS
    }
  },
  computed: {
    isEdit() {
      return !!this.trek
    },
    isStaff() {
      return this.role === 'staff'
    }
  },
  watch: {
    visible(isVisible) {
      if (isVisible) {
        this.form = this.trek ? this.trekToForm(this.trek) : this.emptyForm()
        this.error = null
      }
    }
  },
  methods: {
    emptyForm() {
      return {
        name: '',
        location: '',
        difficulty: '',
        description: '',
        start_date: '',
        end_date: '',
        total_slots: null,
        assigned_staff_id: null,
        status: 'Pending'
      }
    },
    trekToForm(trek) {
      return {
        name: trek.name,
        location: trek.location,
        difficulty: trek.difficulty,
        description: trek.description || '',
        start_date: this.toInputDate(trek.start_date),
        end_date: this.toInputDate(trek.end_date),
        total_slots: trek.total_slots,
        assigned_staff_id: trek.assigned_staff_id,
        status: trek.status
      }
    },
    // backend uses DD-MM-YYYY, <input type="date"> needs YYYY-MM-DD
    toInputDate(ddmmyyyy) {
      if (!ddmmyyyy) return ''
      const [d, m, y] = ddmmyyyy.split('-')
      return `${y}-${m}-${d}`
    },
    toApiDate(yyyymmdd) {
      if (!yyyymmdd) return ''
      const [y, m, d] = yyyymmdd.split('-')
      return `${d}-${m}-${y}`
    },
    async handleSubmit() {
      this.error = null
      this.saving = true
      try {
        if (this.isStaff) {
          // Staff can only touch status and total_slots (enforced by backend too)
          await api.put(`/update/trek/${this.trek.id}`, {
            status: this.form.status,
            total_slots: this.form.total_slots
          })
        } else if (this.isEdit) {
          await api.put(`/update/trek/${this.trek.id}`, {
            name: this.form.name,
            description: this.form.description,
            location: this.form.location,
            difficulty: this.form.difficulty,
            status: this.form.status,
            start_date: this.toApiDate(this.form.start_date),
            end_date: this.toApiDate(this.form.end_date),
            total_slots: this.form.total_slots,
            assigned_staff_id: this.form.assigned_staff_id
          })
        } else {
          await api.post('/create/trek', {
            name: this.form.name,
            description: this.form.description,
            location: this.form.location,
            difficulty: this.form.difficulty,
            start_date: this.toApiDate(this.form.start_date),
            end_date: this.toApiDate(this.form.end_date),
            total_slots: this.form.total_slots,
            assigned_staff_id: this.form.assigned_staff_id
          })
        }
        this.$emit('saved')
      } catch (err) {
        this.error = err.response?.data?.message || 'Failed to save trek'
      } finally {
        this.saving = false
      }
    }
  }
}
</script>