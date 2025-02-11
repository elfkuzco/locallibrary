<script setup lang="ts">
import { Icon } from "@iconify/vue"
defineProps<{
    registerGoogleUrl: string
}>()
</script>

<template>
    <div class="max-w-md w-full mx-auto space-y-8 p-8">
        <!-- Title -->
        <div class="text-center">
            <h2 class="text-2xl font-bold text-gray-900">Create your account</h2>
            <p class="mt-2 text-sm text-gray-600">Join our community of readers</p>
        </div>

        <!-- Sign-up Options -->
        <div class="space-y-8">
            <!-- Google Sign-up -->
            <a
                :href="registerGoogleUrl"
                class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-lg text-gray-700 bg-white hover:bg-gray-50 hover:border-gray-400 shadow-sm hover:shadow-md transition-all duration-200"
            >
                <Icon icon="mdi:google-plus" class="h-5 w-5 mr-3" />
                <span class="text-base font-medium">Sign in with Google</span>
            </a>
        </div>

        <!-- Terms Notice -->
        <p class="text-xs text-center text-gray-500">
            By signing up, you agree to our
            <a href="/terms" class="text-indigo-600 hover:text-indigo-500">Terms of Service</a>
            and
            <a href="/privacy" class="text-indigo-600 hover:text-indigo-500">Privacy Policy</a>
        </p>
    </div>
</template>
