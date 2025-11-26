<template>
  <dialog :open="open" class="modal">
    <form method="dialog" class="modal-box" @submit.prevent="submit">
      <h3 class="font-bold text-lg mb-4">Edit Endpoint</h3>

      <div class="form-control mb-2 flex items-center">
        <label class="label w-26 text-sm">Name</label>
        <input v-model="name" placeholder="Endpoint name" class="input input-bordered w-full" required />
      </div>

      <div class="form-control mb-2 flex items-center">
        <label class="label w-26 text-sm">Path</label>
        <input v-model="path" placeholder="URL Path" class="input input-bordered w-full" required />
      </div>

      <div class="form-control mb-4 flex items-center">
        <label class="label w-26 text-sm">Description</label>
        <input v-model="description" placeholder="Description" class="input input-bordered w-full" />
      </div>

      <div class="form-control mb-2">
        <label class="label">
          <span class="label-text">Response</span>
        </label>
        <select v-model="responseType" class="select select-bordered w-full">
          <option value="NOT_FOUND">Not found</option>
          <option value="REDIRECT">Redirect</option>
          <option value="IMAGE">Image</option>
          <option value="REFERER">Referer</option>
        </select>
      </div>

      <div v-if="responseType === 'REDIRECT'" class="form-control mb-2">
        <input v-model="responseTarget" placeholder="Redirect URL (https://...)" class="input input-bordered w-full" />
      </div>

      <div v-if="responseType === 'IMAGE'" class="form-control mb-2">
        <input ref="fileInput" type="file" accept="image/*" class="file-input file-input-bordered w-full" />
        <div v-if="existingImage" class="mt-2">
          <span class="text-sm">Current image:</span>
          <img :src="existingImage" class="max-h-32 rounded block mt-2" />
        </div>
      </div>

      <div v-if="responseType === 'REFERER'" class="form-control mb-2">
        <input v-model="refererUrl" placeholder="Referer URL (https://...)" class="input input-bordered w-full mb-2" />
        <label class="label mb-1">
          <span class="label-text">Success Image</span>
        </label>
        <input ref="fileInputSuccess" type="file" accept="image/*" class="file-input file-input-bordered w-full mb-2" />
        <div v-if="existingSuccessImage" class="mt-2">
          <span class="text-sm">Current success image:</span>
          <img :src="existingSuccessImage" class="max-h-32 rounded block mt-2" />
        </div>
        <label class="label mb-1">
          <span class="label-text">Failure Image</span>
        </label>
        <input ref="fileInputFailure" type="file" accept="image/*" class="file-input file-input-bordered w-full" />
        <div v-if="existingFailureImage" class="mt-2">
          <span class="text-sm">Current failure image:</span>
          <img :src="existingFailureImage" class="max-h-32 rounded block mt-2" />
        </div>
      </div>

      <div class="flex flex-row items-center justify-between gap-4 mt-2">
        <div class="form-control m-0 mt-4">
          <label class="cursor-pointer label m-0">
            <span class="label-text">Active</span>
            <input type="checkbox" v-model="isActive" class="checkbox ml-2" />
          </label>
        </div>
        <div class="modal-action m-0">
          <button type="submit" class="btn btn-sm btn-success">Save</button>
          <button type="button" class="btn btn-sm" @click="close">Cancel</button>
        </div>
      </div>

      <div v-if="message" :class="isError ? 'text-error mt-3' : 'text-success mt-3'">{{ message }}</div>
    </form>
  </dialog>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import axios from 'axios'

const props = defineProps({
  open: Boolean,
  endpoint: Object
})
const emit = defineEmits(['close','updated'])

const name = ref('')
const path = ref('')
const description = ref('')
const isActive = ref(true)
const responseType = ref('NOT_FOUND')
const responseTarget = ref('')
const fileInput = ref(null)
const existingImage = ref(null)
const refererUrl = ref('')
const fileInputSuccess = ref(null)
const existingSuccessImage = ref(null)
const fileInputFailure = ref(null)
const existingFailureImage = ref(null)

const message = ref('')
const isError = ref(false)

watch(() => props.endpoint, (ep) => {
  if (ep) {
    name.value = ep.name || ''
    path.value = ep.path || ''
    description.value = ep.description || ''
    isActive.value = !!ep.is_active
    responseType.value = ep.response_type || 'NOT_FOUND'
    responseTarget.value = ep.response_redirect_url || ''
    refererUrl.value = ep.response_referer_url || ''
    existingImage.value = ep.response_image || null
    existingSuccessImage.value = ep.response_image_referer_success || null
    existingFailureImage.value = ep.response_image_referer_failure || null
    if (fileInput.value) fileInput.value.value = null
    if (fileInputSuccess.value) fileInputSuccess.value.value = null
    if (fileInputFailure.value) fileInputFailure.value.value = null
    message.value = ''
    isError.value = false
  }
}, { immediate: true })

const close = () => emit('close')

const submit = async () => {
  if (!props.endpoint) return
  isError.value = false
  message.value = ''

  if (responseType.value === 'REDIRECT' && !responseTarget.value) {
    isError.value = true
    message.value = 'Redirect URL required for Redirect response.'
    return
  }

  try {
    const form = new FormData()
    form.append('name', name.value)
    form.append('path', path.value)
    form.append('description', description.value || '')
    form.append('is_active', isActive.value ? 'true' : 'false')
    form.append('response_type', responseType.value)
    form.append('response_redirect_url', responseTarget.value || '')
    form.append('response_referer_url', refererUrl.value || '')

    const file = fileInput.value?.files?.[0]
    if (file && responseType.value === 'IMAGE') form.append('response_image', file)

    const fileSuccess = fileInputSuccess.value?.files?.[0]
    if (fileSuccess && responseType.value === 'REFERER') {
      form.append('response_image_referer_success', fileSuccess)
    }

    const fileFailure = fileInputFailure.value?.files?.[0]
    if (fileFailure && responseType.value === 'REFERER') {
      form.append('response_image_referer_failure', fileFailure)
    }

    await axios.patch(`/api/endpoints/${props.endpoint.id}/`, form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    emit('updated')
    close()
  } catch (err) {
    isError.value = true
    message.value = err?.response?.data || err?.message || 'Error updating endpoint'
  }
}
</script>