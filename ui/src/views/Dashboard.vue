<template>
    <div class="p-6 space-y-6">
        <!-- Page Title -->
        <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold">Dashboard</h2>
        </div>

        <!-- Cards Row-->
        <div class="grid lg:grid-cols-2 gap-6">
            <!-- Endpoints Card -->
            <div class="card bg-base-200 shadow-md">
                <div class="card-body">
                    <div class="flex justify-between items-center mb-6">
                        <h2 class="text-2xl font-bold">Endpoints</h2>
                        <button
                            class="btn btn-sm btn-primary"
                            @click="showCreateModal = true"
                        >
                            Create New Endpoint
                        </button>
                    </div>
                    <h3 class="card-title">Endpoints</h3>
                    <div class="grid grid-cols-1 gap-4">
                        <div
                            v-for="ep in endpoints"
                            :key="ep.id"
                            class="card bg-base-100 shadow border border-base-300 cursor-pointer hover:shadow-lg transition"
                            @click.stop="openEditModal(ep)"
                        >
                            <div class="card-body space-y-2">
                                <div class="flex justify-between items-center">
                                    <span class="text-lg"
                                        >Name: {{ ep.name }}</span
                                    >
                                    <span
                                        class="badge badge-success"
                                        v-if="ep.is_active"
                                        >Active</span
                                    >
                                    <span class="badge badge-error" v-else
                                        >Inactive</span
                                    >
                                </div>
                                <div class="flex justify-between items-center">
                                    <span class="font-semibold"
                                        >Description:
                                        {{ ep.description || "N/A" }}</span
                                    >
                                </div>
                                <div class="flex justify-between items-center">
                                    <span class="font-semibold"
                                        >Created:
                                        {{
                                            new Date(
                                                ep.created_at
                                            ).toUTCString() || "N/A"
                                        }}</span
                                    >
                                    <span class="text-sm"
                                        >Endpoint ID: {{ ep.id }}</span
                                    >
                                </div>
                                <div class="flex justify-between items-center">
                                    <span class="font-semibold"
                                        >Path:
                                        <span class="text-blue-600">{{
                                            ep.path
                                        }}</span></span
                                    >
                                    <span class="text-sm"
                                        >Response Type:
                                        <span class="text-blue-600">{{
                                            ep.response_type
                                        }}</span></span
                                    >
                                </div>
                                <div
                                    v-if="
                                        ep.response_type === 'IMAGE' &&
                                        ep.response_image
                                    "
                                    class="mt-2"
                                >
                                    <img
                                        :src="ep.response_image"
                                        alt="Response Image"
                                        class="max-h-48 rounded-lg border border-base-300"
                                    />
                                </div>
                                <div
                                    v-else-if="ep.response_type === 'REDIRECT'"
                                    class="mt-2"
                                >
                                    <span class="font-semibold"
                                        >Redirect URL:</span
                                    >
                                    <p
                                        class="p-2 mt-2 rounded bg-base-300 break-all whitespace-pre-line"
                                    >
                                        {{ short(ep.response_redirect_url) }}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent API Calls Card -->
            <div class="card bg-base-200 shadow-md">
                <div class="card-body">
                    <h3 class="card-title">Recent API Calls</h3>
                    <div class="grid grid-cols-1 gap-4">
                        <div
                            v-for="call in apicalls"
                            :key="call.id"
                            class="card bg-base-100 shadow border border-base-300"
                            @click="toggleCall(call.id)"
                        >
                            <div
                                class="card-body space-y-2 cursor-pointer hover:shadow-lg transition"
                            >
                                <div class="flex justify-between items-center">
                                    <span class="text-blue-600 font-semibold">{{
                                        call.method
                                    }}</span>
                                    <span class="font-medium">{{
                                        new Date(call.timestamp).toUTCString()
                                    }}</span>
                                </div>
                                <div class="flex justify-between items-center">
                                    <span class="font-semibold">{{
                                        call.remote_ip
                                    }}</span>
                                    <span class="font-semibold"
                                        >Endpoint ID:
                                        {{ call.endpoint || "Unknown" }}</span
                                    >
                                </div>

                                <transition name="expand">
                                    <div
                                        v-if="expandedCalls === call.id"
                                        class="expand-content p-4 rounded-lg bg-base-300"
                                    >
                                        <div
                                            v-for="(value, key) in call"
                                            :key="key"
                                            class="space-y-2"
                                        >
                                            <span class="font-semibold"
                                                >{{ key }}:</span
                                            >
                                            <span
                                                v-if="
                                                    typeof value === 'object' &&
                                                    value !== null
                                                "
                                            >
                                                <pre
                                                    class="p-2 rounded text-xs break-all whitespace-pre-line"
                                                    >{{
                                                        JSON.stringify(
                                                            value,
                                                            null,
                                                            2
                                                        )
                                                    }}</pre
                                                >
                                            </span>
                                            <span v-else>{{ value }}</span>
                                        </div>
                                    </div>
                                </transition>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <CreateEndpointModal
        :open="showCreateModal"
        @close="showCreateModal = false"
        @created="reloadEndpoints"
    />
    <EditEndpointModal
        :open="showEditModal"
        :endpoint="selectedEndpoint"
        @close="showEditModal = false"
        @updated="reloadEndpoints"
    />
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import CreateEndpointModal from "../components/CreateEndpointModal.vue";
import EditEndpointModal from "../components/EditEndpointModal.vue";

export default {
    components: { CreateEndpointModal, EditEndpointModal },
    setup() {
        const endpoints = ref([]);
        const apicalls = ref([]);
        const loading = ref(true);
        const error = ref("");

        const fetchData = async () => {
            try {
                loading.value = true;

                const endpointsResponse = await axios.get("/api/endpoints/");
                endpoints.value = endpointsResponse.data;

                const callsResponse = await axios.get("/api/apicalls/");
                apicalls.value = callsResponse.data;

                console.log("Data fetched successfully");
            } catch (err) {
                console.error("Error fetching data:", err);
                error.value =
                    err.response?.data?.detail || "Failed to load data";

                if (err.response?.status === 401) {
                    router.push({ name: "login" });
                }
            } finally {
                loading.value = false;
            }
        };

        const short = (val) => {
            if (!val) return "";
            const s = JSON.stringify(val);
            return s.length > 80 ? s.slice(0, 80) + "…" : s;
        };

        const expandedCalls = ref(null);

        function toggleCall(id) {
            expandedCalls.value = expandedCalls.value === id ? null : id;
        }

        const showCreateModal = ref(false);
        const showEditModal = ref(false);
        const selectedEndpoint = ref(null);

        const openEditModal = (ep) => {
            selectedEndpoint.value = ep;
            showEditModal.value = true;
        };

        const reloadEndpoints = async () => {
            const eRes = await axios.get("/api/endpoints/");
            endpoints.value = eRes.data;
        };

        onMounted(fetchData);

        return {
            endpoints,
            apicalls,
            short,
            expandedCalls,
            toggleCall,
            showCreateModal,
            reloadEndpoints,
            showEditModal,
            selectedEndpoint,
            openEditModal,
        };
    },
};
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
    transition: max-height 0.2s ease, opacity 0.2s;
    overflow: hidden;
}
.expand-enter-from,
.expand-leave-to {
    max-height: 0;
    opacity: 0;
}
.expand-enter-to,
.expand-leave-from {
    max-height: 500px;
    opacity: 1;
}
</style>
