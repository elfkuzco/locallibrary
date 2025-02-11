<script setup lang="ts">
import { getGoogleOauthUrl } from "@/services/api/auth"
import SignupComponent from "../components/SignupComponent.vue"
const urlParams = new URLSearchParams(window.location.search)
const nextUrl = urlParams.get("next") || "/"
</script>

<template>
    <SignupComponent :registerGoogleUrl="getGoogleOauthUrl(nextUrl)" />
</template>
