<template>
    <dialog :open="open" class="modal">
        <form method="dialog" class="modal-box" @submit.prevent="submit">
            <h3 class="font-bold text-lg mb-4">Create New Endpoint</h3>

            <div class="form-control mb-2 flex items-center">
                <label class="label w-26 text-sm">Name</label>
                <input
                    id="name"
                    v-model="name"
                    placeholder="Endpoint name"
                    class="input input-bordered w-full"
                    required
                />
            </div>

            <div class="form-control mb-2 flex items-center">
                <label class="label w-26 text-sm">Path</label>
                <input
                    id="path"
                    v-model="path"
                    placeholder="URL Path"
                    class="input input-bordered w-full"
                    required
                />
            </div>

            <div class="form-control mb-4 flex items-center">
                <label class="label w-26 text-sm">Description</label>
                <input
                    id="description"
                    v-model="description"
                    placeholder="Description"
                    class="input input-bordered w-full"
                />
            </div>

            <div class="form-control mb-2">
                <label class="label">
                    <span class="label-text">Response</span>
                </label>
                <select
                    v-model="responseMethod"
                    class="select select-bordered w-full"
                >
                    <option value="NOT_FOUND">Not found</option>
                    <option value="REDIRECT">Redirect</option>
                    <option value="IMAGE">Image</option>
                    <option value="REFERER">Referer</option>
                </select>
            </div>

            <div v-if="responseMethod === 'REDIRECT'" class="form-control mb-2">
                <input
                    v-model="responseTarget"
                    placeholder="Redirect URL (https://...)"
                    class="input input-bordered w-full"
                />
            </div>

            <div v-if="responseMethod === 'IMAGE'" class="form-control mb-2">
                <input
                    ref="fileInput"
                    type="file"
                    accept="image/*"
                    class="file-input file-input-bordered w-full"
                />
            </div>

            <div v-if="responseMethod === 'REFERER'" class="form-control mb-2">
                <input
                    v-model="refererUrl"
                    placeholder="Referer URL (https://...)"
                    class="input input-bordered w-full mb-2"
                />
                <label class="label mb-1">
                    <span class="label-text">Success Image</span>
                </label>
                <input
                    ref="fileInputSuccess"
                    type="file"
                    accept="image/*"
                    class="file-input file-input-bordered w-full mb-2"
                />
                <label class="label mb-1">
                    <span class="label-text">Failure Image</span>
                </label>
                <input
                    ref="fileInputFailure"
                    type="file"
                    accept="image/*"
                    class="file-input file-input-bordered w-full"
                />
            </div>

            <div class="flex flex-row items-center justify-between gap-4 mt-2">
                <div class="form-control m-0 mt-4">
                    <label class="cursor-pointer label m-0">
                        <span class="label-text">Active</span>
                        <input
                            type="checkbox"
                            v-model="isActive"
                            class="checkbox ml-2"
                        />
                    </label>
                </div>
                <div class="modal-action m-0">
                    <button type="submit" class="btn btn-sm btn-success">
                        Create
                    </button>
                    <button type="button" class="btn btn-sm" @click="close">
                        Cancel
                    </button>
                </div>
            </div>

            <div
                v-if="message"
                :class="isError ? 'text-error' : 'text-success'"
            >
                {{ message }}
            </div>
        </form>
    </dialog>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from "vue";
import axios from "axios";

const props = defineProps({ open: Boolean });
const emit = defineEmits(["close", "created"]);

const name = ref("");
const path = ref("");
const description = ref("");
const isActive = ref(true);
const responseMethod = ref("NOT_FOUND");
const responseTarget = ref("");
const fileInput = ref(null);
const refererUrl = ref("");
const fileInputSuccess = ref(null);
const fileInputFailure = ref(null);

const message = ref("");
const isError = ref(false);

watch(
    () => props.open,
    (val) => {
        if (val) {
            name.value = "";
            path.value = "";
            description.value = "";
            isActive.value = true;
            responseMethod.value = "NOT_FOUND";
            responseTarget.value = "";
            if (fileInput.value) fileInput.value.value = null;

            message.value = "";
            isError.value = false;
        }
    }
);

const close = () => emit("close");

const submit = async () => {
    isError.value = false;
    message.value = "";

    // Simple check for redirect
    if (responseMethod.value === "REDIRECT" && !responseTarget.value) {
        isError.value = true;
        message.value = "Redirect URL required for Redirect response.";
        return;
    }

    if (responseMethod.value === "REFERER" && !refererUrl.value) {
        isError.value = true;
        message.value = "Referer URL required for Referer response.";
        return;
    }

    if (responseMethod.value === "IMAGE") {
        const file = fileInput.value?.files?.[0];
        if (!file) {
            isError.value = true;
            message.value = "Image file required for Image response.";
            return;
        }
    }

    if (responseMethod.value === "REFERER") {
        const fileSuccess = fileInputSuccess.value?.files?.[0];
        const fileFailure = fileInputFailure.value?.files?.[0];
        if (!fileSuccess || !fileFailure) {
            isError.value = true;
            message.value =
                "Both success and failure images are required for Referer response.";
            return;
        }
    }

    try {
        const form = new FormData();
        form.append("name", name.value);
        form.append("path", path.value);
        form.append("description", description.value || "");
        form.append("is_active", isActive.value ? "true" : "false");
        form.append("response_type", responseMethod.value);
        form.append("response_redirect_url", responseTarget.value || "");
        form.append("response_referer_url", refererUrl.value || "");

        const file = fileInput.value?.files?.[0];
        if (file && responseMethod.value === "IMAGE") {
            form.append("response_image", file);
        }

        const fileSuccess = fileInputSuccess.value?.files?.[0];
        if (fileSuccess && responseMethod.value === "REFERER") {
            form.append("response_image_referer_success", fileSuccess);
        }

        const fileFailure = fileInputFailure.value?.files?.[0];
        if (fileFailure && responseMethod.value === "REFERER") {
            form.append("response_image_referer_failure", fileFailure);
        }

        await axios.post("/api/endpoints/", form, {
            headers: { "Content-Type": "multipart/form-data" },
        });

        emit("created");
        close();
    } catch (err) {
        isError.value = true;
        message.value =
            err?.response?.data || err?.message || "Error creating endpoint";
    }
};
</script>
