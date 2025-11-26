<script>
import Header from "./components/Header.vue";
import { useRoute } from "vue-router";
import { computed } from "vue";

export default {
    components: { Header },
    setup() {
        const route = useRoute();
        const isLogin = computed(() => route.name === "login");
        return { isLogin };
    },
};
</script>

<template>
    <Header v-if="!isLogin" />
    <router-view />
</template>

<style scoped></style>
